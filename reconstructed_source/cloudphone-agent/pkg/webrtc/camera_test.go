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
	"encoding/binary"
	"encoding/json"
	"image"
	"image/color"
	"image/jpeg"
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
