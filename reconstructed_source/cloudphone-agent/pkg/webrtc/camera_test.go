// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY / GENERATED_ADAPTER / IMPLEMENTATION_CHOICE / RECONSTRUCTED_SEMANTIC_MODEL
// Mapping Scope: WEBRTC_CAMERA_UNIT_TESTS
// Evidence: CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json, CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json,
//   CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"bytes"
	"context"
	"encoding/binary"
	"encoding/json"
	"errors"
	"image"
	"image/color"
	"image/jpeg"
	"io"
	"net"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/pion/webrtc/v3"
)

// TestCameraWireFramingVectors tests exact little-endian length prefixes for evidence vectors:
// 0, 6, 28, 34, 35, 460800.
func TestCameraWireFramingVectors(t *testing.T) {
	testVectors := []struct {
		length         uint32
		expectedPrefix [4]byte
	}{
		{0, [4]byte{0x00, 0x00, 0x00, 0x00}},
		{6, [4]byte{0x06, 0x00, 0x00, 0x00}},
		{28, [4]byte{0x1c, 0x00, 0x00, 0x00}},
		{34, [4]byte{0x22, 0x00, 0x00, 0x00}},
		{35, [4]byte{0x23, 0x00, 0x00, 0x00}},
		{460800, [4]byte{0x00, 0x08, 0x07, 0x00}},
	}

	for _, tc := range testVectors {
		var buf bytes.Buffer
		payload := make([]byte, tc.length)
		if err := writeCameraFrame(&buf, payload); err != nil {
			t.Fatalf("failed to write camera frame of length %d: %v", tc.length, err)
		}

		wireBytes := buf.Bytes()
		if len(wireBytes) != int(tc.length)+4 {
			t.Fatalf("expected wire bytes %d, got %d", tc.length+4, len(wireBytes))
		}

		if !bytes.Equal(wireBytes[:4], tc.expectedPrefix[:]) {
			t.Errorf("vector %d: expected prefix %x, got %x", tc.length, tc.expectedPrefix, wireBytes[:4])
		}

		// Read back frame
		readPayload, err := readCameraFrame(&buf, tc.length+10)
		if err != nil {
			t.Fatalf("failed to read back camera frame of length %d: %v", tc.length, err)
		}
		if len(readPayload) != int(tc.length) {
			t.Errorf("vector %d: expected read payload length %d, got %d", tc.length, tc.length, len(readPayload))
		}
	}
}

// TestCameraWireFramingDefensiveLimit tests that oversized frames are rejected before allocation.
func TestCameraWireFramingDefensiveLimit(t *testing.T) {
	var buf bytes.Buffer
	var oversizedPrefix [4]byte
	binary.LittleEndian.PutUint32(oversizedPrefix[:], 20*1024*1024) // 20 MB > 10 MB limit
	buf.Write(oversizedPrefix[:])

	_, err := readCameraFrame(&buf, MaxCameraHALMessageLen)
	if err == nil {
		t.Fatal("expected error on oversized message length, got nil")
	}
	if !strings.Contains(err.Error(), "exceeds maximum limit") {
		t.Errorf("expected 'exceeds maximum limit' in error, got %v", err)
	}
}

// TestCameraHandshakeSerialization validates JSON structure and semantic values.
func TestCameraHandshakeSerialization(t *testing.T) {
	hs := CameraHandshake{
		Width:     640,
		Height:    480,
		FrameRate: 30.0,
	}

	data, err := json.Marshal(hs)
	if err != nil {
		t.Fatalf("failed to marshal handshake: %v", err)
	}

	var parsed map[string]interface{}
	if err := json.Unmarshal(data, &parsed); err != nil {
		t.Fatalf("failed to unmarshal handshake: %v", err)
	}

	if w, ok := parsed["width"].(float64); !ok || int(w) != 640 {
		t.Errorf("expected width 640, got %v", parsed["width"])
	}
	if h, ok := parsed["height"].(float64); !ok || int(h) != 480 {
		t.Errorf("expected height 480, got %v", parsed["height"])
	}
	if fps, ok := parsed["frame_rate"].(float64); !ok || fps != 30.0 {
		t.Errorf("expected frame_rate 30.0, got %v", parsed["frame_rate"])
	}
}

// TestI420ContiguousGolden tests fast-path planar I420 conversion on contiguous YCbCr 4:2:0 images.
func TestI420ContiguousGolden(t *testing.T) {
	// 4x4 image
	w, h := 4, 4
	rect := image.Rect(0, 0, w, h)
	yuv := image.NewYCbCr(rect, image.YCbCrSubsampleRatio420)

	// Populate known values
	for i := range yuv.Y {
		yuv.Y[i] = uint8(10 + i)
	}
	for i := range yuv.Cb {
		yuv.Cb[i] = uint8(50 + i)
	}
	for i := range yuv.Cr {
		yuv.Cr[i] = uint8(100 + i)
	}

	i420, err := ConvertImageToI420(yuv)
	if err != nil {
		t.Fatalf("failed to convert YCbCr to I420: %v", err)
	}

	expectedLen := w*h + (w/2)*(h/2) + (w/2)*(h/2) // 16 + 4 + 4 = 24
	if len(i420) != expectedLen {
		t.Fatalf("expected I420 length %d, got %d", expectedLen, len(i420))
	}

	// Verify Y plane
	if !bytes.Equal(i420[0:16], yuv.Y[:16]) {
		t.Errorf("Y plane mismatch: expected %v, got %v", yuv.Y[:16], i420[0:16])
	}
	// Verify U (Cb) plane
	if !bytes.Equal(i420[16:20], yuv.Cb[:4]) {
		t.Errorf("U plane mismatch: expected %v, got %v", yuv.Cb[:4], i420[16:20])
	}
	// Verify V (Cr) plane
	if !bytes.Equal(i420[20:24], yuv.Cr[:4]) {
		t.Errorf("V plane mismatch: expected %v, got %v", yuv.Cr[:4], i420[20:24])
	}
}

// TestI420StrideGolden tests planar I420 conversion with row stride offsets.
func TestI420StrideGolden(t *testing.T) {
	w, h := 4, 4
	rect := image.Rect(0, 0, w, h)
	yuv := image.NewYCbCr(rect, image.YCbCrSubsampleRatio420)

	// Simulate padded strides: YStride > width, CStride > width/2
	yuv.YStride = 8
	yuv.CStride = 4
	yuv.Y = make([]uint8, yuv.YStride*h)
	yuv.Cb = make([]uint8, yuv.CStride*(h/2))
	yuv.Cr = make([]uint8, yuv.CStride*(h/2))

	// Populate row 0 and row 1 with stride padding
	for r := 0; r < h; r++ {
		for c := 0; c < w; c++ {
			yuv.Y[r*yuv.YStride+c] = uint8(r*10 + c)
		}
	}
	for r := 0; r < h/2; r++ {
		for c := 0; c < w/2; c++ {
			yuv.Cb[r*yuv.CStride+c] = uint8(50 + r*10 + c)
			yuv.Cr[r*yuv.CStride+c] = uint8(80 + r*10 + c)
		}
	}

	i420, err := ConvertImageToI420(yuv)
	if err != nil {
		t.Fatalf("failed to convert stride YCbCr to I420: %v", err)
	}

	// Verify extracted rows match without stride padding
	for r := 0; r < h; r++ {
		for c := 0; c < w; c++ {
			expected := uint8(r*10 + c)
			actual := i420[r*w+c]
			if actual != expected {
				t.Errorf("Y[%d,%d] expected %d, got %d", r, c, expected, actual)
			}
		}
	}

	uOffset := w * h
	for r := 0; r < h/2; r++ {
		for c := 0; c < w/2; c++ {
			expected := uint8(50 + r*10 + c)
			actual := i420[uOffset+r*(w/2)+c]
			if actual != expected {
				t.Errorf("U[%d,%d] expected %d, got %d", r, c, expected, actual)
			}
		}
	}

	vOffset := uOffset + (w/2)*(h/2)
	for r := 0; r < h/2; r++ {
		for c := 0; c < w/2; c++ {
			expected := uint8(80 + r*10 + c)
			actual := i420[vOffset+r*(w/2)+c]
			if actual != expected {
				t.Errorf("V[%d,%d] expected %d, got %d", r, c, expected, actual)
			}
		}
	}
}

// TestI420GenericFallbackGolden tests Rec.601 conversion on non-YCbCr (RGBA) images.
func TestI420GenericFallbackGolden(t *testing.T) {
	w, h := 2, 2
	img := image.NewRGBA(image.Rect(0, 0, w, h))

	// Set pure colors
	img.Set(0, 0, color.RGBA{R: 255, G: 0, B: 0, A: 255})     // Red
	img.Set(1, 0, color.RGBA{R: 0, G: 255, B: 0, A: 255})     // Green
	img.Set(0, 1, color.RGBA{R: 0, G: 0, B: 255, A: 255})     // Blue
	img.Set(1, 1, color.RGBA{R: 255, G: 255, B: 255, A: 255}) // White

	i420, err := ConvertImageToI420(img)
	if err != nil {
		t.Fatalf("failed to convert RGBA to I420: %v", err)
	}

	expectedLen := 2*2 + 1 + 1 // 6 bytes
	if len(i420) != expectedLen {
		t.Fatalf("expected length %d, got %d", expectedLen, len(i420))
	}

	// Verify Y values are Rec.601 expected
	// Red Y ~= 76, Green Y ~= 149, Blue Y ~= 29, White Y ~= 255
	yRed, _, _ := color.RGBToYCbCr(255, 0, 0)
	yGreen, _, _ := color.RGBToYCbCr(0, 255, 0)
	yBlue, _, _ := color.RGBToYCbCr(0, 0, 255)
	yWhite, _, _ := color.RGBToYCbCr(255, 255, 255)

	if i420[0] != yRed {
		t.Errorf("Y[0,0] expected %d, got %d", yRed, i420[0])
	}
	if i420[1] != yGreen {
		t.Errorf("Y[1,0] expected %d, got %d", yGreen, i420[1])
	}
	if i420[2] != yBlue {
		t.Errorf("Y[0,1] expected %d, got %d", yBlue, i420[2])
	}
	if i420[3] != yWhite {
		t.Errorf("Y[1,1] expected %d, got %d", yWhite, i420[3])
	}
}

// TestJPEGDecodeIntegration tests end-to-end small JPEG encode, decode, and I420 conversion.
func TestJPEGDecodeIntegration(t *testing.T) {
	w, h := 16, 16
	img := image.NewRGBA(image.Rect(0, 0, w, h))
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			img.Set(x, y, color.RGBA{R: uint8(x * 15), G: uint8(y * 15), B: 128, A: 255})
		}
	}

	var jpegBuf bytes.Buffer
	if err := jpeg.Encode(&jpegBuf, img, &jpeg.Options{Quality: 80}); err != nil {
		t.Fatalf("failed to encode JPEG: %v", err)
	}

	decoded, err := jpeg.Decode(&jpegBuf)
	if err != nil {
		t.Fatalf("failed to decode JPEG: %v", err)
	}

	i420, err := ConvertImageToI420(decoded)
	if err != nil {
		t.Fatalf("failed to convert decoded JPEG to I420: %v", err)
	}

	expectedLen := w*h + (w/2)*(h/2) + (w/2)*(h/2)
	if len(i420) != expectedLen {
		t.Errorf("expected I420 length %d, got %d", expectedLen, len(i420))
	}
}

// TestBackpressureQueueCapacityAndSnapshotOrdering validates:
// 1. cameraFrameChan capacity is strictly 1.
// 2. Fast producer does not block when queue is saturated.
// 3. latestCameraJpeg is updated to the newest frame even when enqueuing is dropped.
func TestBackpressureQueueCapacityAndSnapshotOrdering(t *testing.T) {
	handler := NewCameraHandler(DefaultCameraConfig(), nil)
	defer handler.Close()

	if cap(handler.cameraFrameChan) != 1 {
		t.Fatalf("expected cameraFrameChan capacity 1, got %d", cap(handler.cameraFrameChan))
	}

	// Prepare 3 distinct frames
	jpegA := []byte{0xff, 0xd8, 0xff, 0xe0, 0x01, 0xAA}
	jpegB := []byte{0xff, 0xd8, 0xff, 0xe0, 0x01, 0xBB}
	jpegC := []byte{0xff, 0xd8, 0xff, 0xe0, 0x01, 0xCC}

	// Simulate incoming DataChannel binary messages
	handler.onMessage(webrtc.DataChannelMessage{IsString: false, Data: jpegA})
	// Channel now has 1 frame
	if len(handler.cameraFrameChan) != 1 {
		t.Errorf("expected queue length 1 after first message, got %d", len(handler.cameraFrameChan))
	}

	// Send second message while queue is full (do not consume)
	handler.onMessage(webrtc.DataChannelMessage{IsString: false, Data: jpegB})

	// Verify producer did NOT block and queue still has length 1
	if len(handler.cameraFrameChan) != 1 {
		t.Errorf("queue should still have length 1, got %d", len(handler.cameraFrameChan))
	}

	// Send third message
	handler.onMessage(webrtc.DataChannelMessage{IsString: false, Data: jpegC})

	// CRITICAL INVARIANT: latestCameraJpeg MUST be updated to jpegC despite drops
	latest := handler.GetLatestCameraJpeg()
	if !bytes.Equal(latest, jpegC) {
		t.Fatalf("expected latestCameraJpeg to be jpegC, got %x", latest)
	}

	// Verify text frames are rejected as camera frame data
	textMsg := webrtc.DataChannelMessage{IsString: true, Data: []byte("some-text")}
	handler.onMessage(textMsg)
	latestAfterText := handler.GetLatestCameraJpeg()
	if !bytes.Equal(latestAfterText, jpegC) {
		t.Errorf("text frame should NOT overwrite latestCameraJpeg")
	}
}

// TestCameraHandlerHALBridgeInteraction validates complete HAL event loop:
// Handshake, START event -> action:start, CAPTURE event -> snapshot JPEG, STOP event -> action:stop.
func TestCameraHandlerHALBridgeInteraction(t *testing.T) {
	// Start ephemeral mock HAL bridge
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("failed to listen on mock bridge: %v", err)
	}
	defer listener.Close()

	bridgeAddr := listener.Addr().String()

	cfg := CameraConfig{
		Address:     bridgeAddr,
		Width:       640,
		Height:      480,
		FrameRate:   30.0,
		DialTimeout: 1 * time.Second,
	}

	handler := NewCameraHandler(cfg, nil)
	defer handler.Close()

	var serverConn net.Conn
	var connOnce sync.Once
	connChan := make(chan net.Conn, 1)

	go func() {
		conn, err := listener.Accept()
		if err == nil {
			connOnce.Do(func() {
				connChan <- conn
			})
		}
	}()

	// Trigger onOpen
	go handler.onOpen()

	select {
	case serverConn = <-connChan:
		defer serverConn.Close()
	case <-time.After(3 * time.Second):
		t.Fatal("timed out waiting for handler to connect to mock bridge")
	}

	// 1. Mock bridge receives length-prefixed handshake
	hsPayload, err := readCameraFrame(serverConn, MaxCameraHALMessageLen)
	if err != nil {
		t.Fatalf("failed to read handshake from handler: %v", err)
	}

	var hs CameraHandshake
	if err := json.Unmarshal(hsPayload, &hs); err != nil {
		t.Fatalf("invalid handshake JSON: %v", err)
	}
	if hs.Width != 640 || hs.Height != 480 || hs.FrameRate != 30.0 {
		t.Errorf("unexpected handshake values: %+v", hs)
	}

	// 2. Set snapshot in handler
	testSnapshot := []byte{0xff, 0xd8, 0xff, 0xe0, 0x12, 0x34, 0x56, 0x78}
	handler.mu.Lock()
	handler.latestCameraJpeg = testSnapshot
	handler.mu.Unlock()

	// 3. Mock sends VIRTUAL_DEVICE_CAPTURE_IMAGE event
	if err := writeCameraFrame(serverConn, []byte(HALEventCaptureImage)); err != nil {
		t.Fatalf("failed to send capture event: %v", err)
	}

	// 4. Mock receives snapshot response
	snapPayload, err := readCameraFrame(serverConn, MaxCameraHALMessageLen)
	if err != nil {
		t.Fatalf("failed to read snapshot response: %v", err)
	}
	if !bytes.Equal(snapPayload, testSnapshot) {
		t.Errorf("snapshot mismatch: expected %x, got %x", testSnapshot, snapPayload)
	}

	// 5. Mock sends VIRTUAL_DEVICE_START_CAMERA_SESSION event
	if err := writeCameraFrame(serverConn, []byte(HALEventStartCameraSession)); err != nil {
		t.Fatalf("failed to send start event: %v", err)
	}

	// Verify state transitioned to ActiveStreaming
	time.Sleep(50 * time.Millisecond)
	if handler.GetState() != StateActiveStreaming {
		t.Errorf("expected state StateActiveStreaming, got %v", handler.GetState())
	}

	// 6. Mock sends VIRTUAL_DEVICE_STOP_CAMERA_SESSION event
	if err := writeCameraFrame(serverConn, []byte(HALEventStopCameraSession)); err != nil {
		t.Fatalf("failed to send stop event: %v", err)
	}

	// Verify state transitioned to Paused
	time.Sleep(50 * time.Millisecond)
	if handler.GetState() != StatePaused {
		t.Errorf("expected state StatePaused, got %v", handler.GetState())
	}
}

// TestCameraProbeBehavior validates probe behavior on available and unavailable ports.
func TestCameraProbeBehavior(t *testing.T) {
	// 1. Probe unavailable port with ForceCamera = false -> false
	cfg := CameraConfig{
		Address:     "127.0.0.1:54321", // unused port
		ForceCamera: false,
		DialTimeout: 50 * time.Millisecond,
	}
	if ProbeCameraBridge(cfg) {
		t.Errorf("probe should return false when endpoint unavailable and ForceCamera=false")
	}

	// 2. Probe unavailable port with ForceCamera = true -> true
	cfgForce := CameraConfig{
		Address:     "127.0.0.1:54321",
		ForceCamera: true,
		DialTimeout: 50 * time.Millisecond,
	}
	if !ProbeCameraBridge(cfgForce) {
		t.Errorf("probe should return true when ForceCamera=true")
	}

	// 3. Probe available port -> true
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("failed to start listener: %v", err)
	}
	defer listener.Close()

	cfgAvail := CameraConfig{
		Address:     listener.Addr().String(),
		ForceCamera: false,
		DialTimeout: 500 * time.Millisecond,
	}
	if !ProbeCameraBridge(cfgAvail) {
		t.Errorf("probe should return true when endpoint is listening")
	}
}

type chunkWriter struct {
	maxChunk int
	buf      bytes.Buffer
}

func (w *chunkWriter) Write(p []byte) (int, error) {
	if len(p) == 0 {
		return 0, nil
	}
	n := len(p)
	if n > w.maxChunk {
		n = w.maxChunk
	}
	return w.buf.Write(p[:n])
}

type noProgressWriter struct{}

func (w *noProgressWriter) Write(p []byte) (int, error) {
	return 0, nil
}

type failingWriter struct {
	failAfter int
	written   int
}

func (w *failingWriter) Write(p []byte) (int, error) {
	if w.written >= w.failAfter {
		return 0, errors.New("write error injected")
	}
	remain := w.failAfter - w.written
	toWrite := len(p)
	if toWrite > remain {
		toWrite = remain
	}
	w.written += toWrite
	return toWrite, nil
}

// TestCameraShortWriterFraming validates that partial prefix and partial payload writes
// loop until complete and produce exact wire framing, while permanent short-writes fail cleanly.
func TestCameraShortWriterFraming(t *testing.T) {
	payload := []byte("hello-virtual-camera-stream")

	// 1. Partial writes (1 byte per write) must succeed and produce full framed message
	cw := &chunkWriter{maxChunk: 1}
	if err := writeCameraFrame(cw, payload); err != nil {
		t.Fatalf("writeCameraFrame with chunkWriter failed: %v", err)
	}
	expectedLen := 4 + len(payload)
	if cw.buf.Len() != expectedLen {
		t.Fatalf("expected total length %d, got %d", expectedLen, cw.buf.Len())
	}
	readPayload, err := readCameraFrame(&cw.buf, MaxCameraHALMessageLen)
	if err != nil {
		t.Fatalf("failed to read back frame written via chunkWriter: %v", err)
	}
	if !bytes.Equal(readPayload, payload) {
		t.Fatalf("payload mismatch after chunkWriter writes: expected %s, got %s", payload, readPayload)
	}

	// 2. Zero-progress writer must return io.ErrNoProgress
	np := &noProgressWriter{}
	if err := writeCameraFrame(np, payload); !errors.Is(err, io.ErrNoProgress) {
		t.Fatalf("expected io.ErrNoProgress on zero-progress writer, got %v", err)
	}

	// 3. Failing writer mid-prefix must fail cleanly
	fwPrefix := &failingWriter{failAfter: 2}
	if err := writeCameraFrame(fwPrefix, payload); err == nil {
		t.Fatal("expected error on failing writer mid-prefix, got nil")
	}

	// 4. Failing writer mid-payload must fail cleanly
	fwPayload := &failingWriter{failAfter: 10}
	if err := writeCameraFrame(fwPayload, payload); err == nil {
		t.Fatal("expected error on failing writer mid-payload, got nil")
	}
}

// TestCameraBridgeWriteConcurrency verifies that simultaneous framed writes from multiple workers
// (such as streaming YUV frames and snapshot responses) are serialized without prefix/payload interleaving.
func TestCameraBridgeWriteConcurrency(t *testing.T) {
	clientConn, serverConn := net.Pipe()
	defer serverConn.Close()

	handler := NewCameraHandler(CameraConfig{Width: 640, Height: 480}, nil)
	handler.mu.Lock()
	handler.bridgeConn = clientConn
	handler.state = StateActiveStreaming
	handler.mu.Unlock()
	defer handler.Close()

	yuvPayload := bytes.Repeat([]byte{0xAA}, 1024)
	snapPayload := bytes.Repeat([]byte{0xBB}, 512)
	numIterations := 50

	startBarrier := make(chan struct{})
	var wg sync.WaitGroup
	wg.Add(2)

	// Writer 1: Simulates processFrames writing YUV
	go func() {
		defer wg.Done()
		<-startBarrier
		for i := 0; i < numIterations; i++ {
			if err := handler.writeBridgeFrame(yuvPayload); err != nil {
				return
			}
		}
	}()

	// Writer 2: Simulates readBridgeEvents writing snapshot
	go func() {
		defer wg.Done()
		<-startBarrier
		for i := 0; i < numIterations; i++ {
			if err := handler.writeBridgeFrame(snapPayload); err != nil {
				return
			}
		}
	}()

	// Release both writers simultaneously
	close(startBarrier)

	// Receiver: Read all 2 * numIterations frames
	totalExpected := numIterations * 2
	for i := 0; i < totalExpected; i++ {
		frame, err := readCameraFrame(serverConn, MaxCameraHALMessageLen)
		if err != nil {
			t.Fatalf("failed reading frame %d/%d: %v", i, totalExpected, err)
		}

		if len(frame) == 1024 {
			if !bytes.Equal(frame, yuvPayload) {
				t.Fatalf("corrupted YUV frame at index %d: bytes mixed or altered", i)
			}
		} else if len(frame) == 512 {
			if !bytes.Equal(frame, snapPayload) {
				t.Fatalf("corrupted Snapshot frame at index %d: bytes mixed or altered", i)
			}
		} else {
			t.Fatalf("unexpected frame size %d at index %d (interleaved framing!)", len(frame), i)
		}
	}

	wg.Wait()
}

// TestCameraBridgeLifecycleAndCancellation verifies centralized error signaling:
// bridge EOF or write error terminates all workers, sets state to closed, without leaks or deadlocks.
func TestCameraBridgeLifecycleAndCancellation(t *testing.T) {
	// Case 1: Bridge EOF while event reader active terminates sibling worker
	t.Run("ReaderEOFSignalsFailure", func(t *testing.T) {
		clientConn, serverConn := net.Pipe()

		handler := NewCameraHandler(CameraConfig{Width: 640, Height: 480}, nil)
		handler.mu.Lock()
		handler.bridgeConn = clientConn
		handler.state = StateActiveStreaming
		handler.wg.Add(2)
		handler.workersStarted = true
		handler.mu.Unlock()

		go handler.readBridgeEvents(clientConn)
		go handler.processFrames(clientConn)

		// Close server connection -> causes EOF in readBridgeEvents
		_ = serverConn.Close()

		// Wait for handler to cancel and transition state
		deadline := time.Now().Add(2 * time.Second)
		for time.Now().Before(deadline) {
			if handler.GetState() == StateClosed {
				break
			}
			time.Sleep(10 * time.Millisecond)
		}

		if handler.GetState() != StateClosed {
			t.Errorf("expected handler state StateClosed after bridge EOF, got %v", handler.GetState())
		}

		// Close must return without hanging or deadlock
		closeDone := make(chan struct{})
		go func() {
			_ = handler.Close()
			close(closeDone)
		}()

		select {
		case <-closeDone:
			// OK
		case <-time.After(1 * time.Second):
			t.Fatal("handler.Close() deadlocked or hung after worker failure")
		}
	})

	// Case 2: Frame worker write failure terminates sibling worker
	t.Run("WriterFailureSignalsFailure", func(t *testing.T) {
		clientConn, serverConn := net.Pipe()

		handler := NewCameraHandler(CameraConfig{Width: 640, Height: 480}, nil)
		handler.mu.Lock()
		handler.bridgeConn = clientConn
		handler.state = StateActiveStreaming
		handler.wg.Add(2)
		handler.workersStarted = true
		handler.mu.Unlock()

		go handler.readBridgeEvents(clientConn)
		go handler.processFrames(clientConn)

		// Close server connection -> next frame write fails
		_ = serverConn.Close()

		// Create a small valid JPEG
		img := image.NewRGBA(image.Rect(0, 0, 4, 4))
		var jpegBuf bytes.Buffer
		_ = jpeg.Encode(&jpegBuf, img, nil)

		// Trigger frame processing
		handler.onMessage(webrtc.DataChannelMessage{IsString: false, Data: jpegBuf.Bytes()})

		// Wait for handler to cancel and transition state
		deadline := time.Now().Add(2 * time.Second)
		for time.Now().Before(deadline) {
			if handler.GetState() == StateClosed {
				break
			}
			time.Sleep(10 * time.Millisecond)
		}

		if handler.GetState() != StateClosed {
			t.Errorf("expected handler state StateClosed after write failure, got %v", handler.GetState())
		}

		// Close must return without deadlock
		closeDone := make(chan struct{})
		go func() {
			_ = handler.Close()
			close(closeDone)
		}()

		select {
		case <-closeDone:
			// OK
		case <-time.After(1 * time.Second):
			t.Fatal("handler.Close() deadlocked or hung after writer failure")
		}
	})

	// Case 3: Close during startup / handshake does not leak workers
	t.Run("CloseDuringStartup", func(t *testing.T) {
		dialStarted := make(chan struct{})
		unblockDial := make(chan struct{})
		dialer := func(ctx context.Context, network, address string) (net.Conn, error) {
			close(dialStarted)
			<-unblockDial
			return nil, errors.New("dial aborted")
		}

		handler := NewCameraHandler(CameraConfig{Address: "127.0.0.1:9001"}, dialer)

		onOpenDone := make(chan struct{})
		go func() {
			handler.onOpen()
			close(onOpenDone)
		}()

		<-dialStarted
		// External close while dial is blocked
		_ = handler.Close()
		close(unblockDial)

		<-onOpenDone

		if handler.GetState() != StateClosed {
			t.Errorf("expected state StateClosed, got %v", handler.GetState())
		}
	})
}

// TestCameraActiveDialTimeout tests that active bridge connection dialing respects cfg.DialTimeout.
func TestCameraActiveDialTimeout(t *testing.T) {
	blockingDialer := func(ctx context.Context, network, address string) (net.Conn, error) {
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		case <-time.After(5 * time.Second):
			return nil, errors.New("timeout not applied")
		}
	}

	cfg := CameraConfig{
		Address:     "127.0.0.1:9001",
		DialTimeout: 50 * time.Millisecond,
	}

	handler := NewCameraHandler(cfg, blockingDialer)
	start := time.Now()
	handler.onOpen()
	elapsed := time.Since(start)

	if elapsed > 1*time.Second {
		t.Fatalf("onOpen took %v, expected timeout around 50ms", elapsed)
	}
	if handler.GetState() != StateClosed {
		t.Errorf("expected StateClosed after dial timeout, got %v", handler.GetState())
	}
}

// TestCameraConfigNormalizationAndSources tests configuration normalization,
// CLI flag parsing, and env variable resolution.
func TestCameraConfigNormalizationAndSources(t *testing.T) {
	// 1. Zero values normalized to defaults
	cfg := NormalizeCameraConfig(CameraConfig{})
	if cfg.Address != DefaultCameraAddress {
		t.Errorf("expected default address %s, got %s", DefaultCameraAddress, cfg.Address)
	}
	if cfg.Width != 640 || cfg.Height != 480 || cfg.FrameRate != 30.0 || cfg.DialTimeout != 1*time.Second {
		t.Errorf("unexpected normalized config: %+v", cfg)
	}

	// 2. CP_AGENT_CAMERA_ADDR resolution
	mockEnv := map[string]string{
		"CP_AGENT_CAMERA_ADDR": "192.168.1.100:9999",
	}
	getenv := func(key string) string { return mockEnv[key] }

	cfgEnv := ResolveCameraConfigFromSources(CameraConfig{}, nil, getenv)
	if cfgEnv.Address != "192.168.1.100:9999" {
		t.Errorf("expected address from env 192.168.1.100:9999, got %s", cfgEnv.Address)
	}
	if cfgEnv.Width != 640 {
		t.Errorf("expected normalized width 640, got %d", cfgEnv.Width)
	}

	// 3. -camera-addr flag overrides env
	args := []string{"-camera-addr", "10.0.0.1:8888"}
	cfgFlag := ResolveCameraConfigFromSources(CameraConfig{}, args, getenv)
	if cfgFlag.Address != "10.0.0.1:8888" {
		t.Errorf("expected address from flag 10.0.0.1:8888, got %s", cfgFlag.Address)
	}

	// 4. --camera-addr=VALUE syntax
	argsEq := []string{"--camera-addr=10.0.0.2:7777", "-force-camera"}
	cfgEq := ResolveCameraConfigFromSources(CameraConfig{}, argsEq, nil)
	if cfgEq.Address != "10.0.0.2:7777" {
		t.Errorf("expected address from flag 10.0.0.2:7777, got %s", cfgEq.Address)
	}
	if !cfgEq.ForceCamera {
		t.Errorf("expected ForceCamera true from -force-camera")
	}

	// 5. Partial non-zero config preserved
	customCfg := CameraConfig{Address: "127.0.0.1:5555"}
	normCustom := NormalizeCameraConfig(customCfg)
	if normCustom.Address != "127.0.0.1:5555" || normCustom.Width != 640 || normCustom.Height != 480 {
		t.Errorf("unexpected config: %+v", normCustom)
	}
}

// TestOddCameraDimensionsRejection validates that odd dimensions are rejected
// with a deterministic error in exact-parity mode (disassembly w/2, h/2).
func TestOddCameraDimensionsRejection(t *testing.T) {
	// Odd width
	imgOddW := image.NewRGBA(image.Rect(0, 0, 641, 480))
	_, err := ConvertImageToI420(imgOddW)
	if err == nil {
		t.Fatal("expected error on odd width, got nil")
	}
	if !strings.Contains(err.Error(), "image dimensions must be even") {
		t.Errorf("expected 'image dimensions must be even' in error, got %v", err)
	}

	// Odd height
	imgOddH := image.NewRGBA(image.Rect(0, 0, 640, 481))
	_, err = ConvertImageToI420(imgOddH)
	if err == nil {
		t.Fatal("expected error on odd height, got nil")
	}
	if !strings.Contains(err.Error(), "image dimensions must be even") {
		t.Errorf("expected 'image dimensions must be even' in error, got %v", err)
	}

	// Even dimensions succeed
	imgEven := image.NewRGBA(image.Rect(0, 0, 640, 480))
	data, err := ConvertImageToI420(imgEven)
	if err != nil {
		t.Fatalf("expected even dimensions to succeed, got %v", err)
	}
	expectedSize := 640 * 480 * 3 / 2
	if len(data) != expectedSize {
		t.Errorf("expected size %d, got %d", expectedSize, len(data))
	}
}
