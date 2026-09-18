// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY / GENERATED_ADAPTER / IMPLEMENTATION_CHOICE / RECONSTRUCTED_SEMANTIC_MODEL
// Mapping Scope: WEBRTC_CAMERA_CHANNEL_AND_VIRTUAL_CAMERA_DATA_PLANE
// Evidence: CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json, CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json,
//   CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json, DISASSEMBLY_FACTS.json, STRINGS.json
// Disassembly:
//   Outbound DataChannel: ARM64 0x53e704-0x53e750, AMD64 0x9e216d (ordered=true)
//   HAL Bridge Dial & Probe: ARM64 0x51ee80-0x51ef94, 0x51a764
//   Lifecycle Binding: ARM64 0x51a024-0x51a0f8 (OnOpen 0x51a3d0, OnMessage 0x51a2e0, OnClose 0x51a120)
//   HAL Inbound Event Framing: ARM64 0x51aa8c-0x51af50 (io.ReadFull LE uint32, ASCII event compare)
//   HAL Handshake: ARM64 0x51a9c4-0x51a9e0 (width, height, frame_rate JSON, 4-byte LE framing)
//   Start/Stop Command Dispatch: ARM64 0x51c980 (JSON text {"action":"start"}/{"action":"stop"})
//   Snapshot Cache & Queue: ARM64 0x51a318-0x51a388 (mutex update latestCameraJpeg before selectnbsend)
//   Queue Capacity: ARM64 0x51ea3c (runtime.makechan64 size=1)
//   JPEG Decode & I420 Stride: ARM64 0x51c250-0x51c780 (image/jpeg.Decode, planar YUV420P fast+stride+Rec.601)
//   YUV Framing & Snapshot: ARM64 0x51c0a8, 0x51af40-0x51b170 (4-byte LE length prefix)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"bytes"
	"context"
	"encoding/binary"
	"encoding/json"
	"errors"
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"io"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/pion/webrtc/v3"
)

// Confirmed Camera HAL Inbound Event Strings (ASCII).
// Classification: RECONSTRUCTED_FROM_BINARY.
const (
	HALEventStartCameraSession = "VIRTUAL_DEVICE_START_CAMERA_SESSION" // 35 bytes (0x23)
	HALEventStopCameraSession  = "VIRTUAL_DEVICE_STOP_CAMERA_SESSION"  // 34 bytes (0x22)
	HALEventCaptureImage       = "VIRTUAL_DEVICE_CAPTURE_IMAGE"        // 28 bytes (0x1c)
)

// Evidence-backed defaults.
// Classification: RECONSTRUCTED_FROM_BINARY.
const (
	DefaultCameraAddress   = "127.0.0.1:9001"
	DefaultCameraWidth     = 640
	DefaultCameraHeight    = 480
	DefaultCameraFrameRate = 30.0
	DefaultCameraTimeout   = 1 * time.Second
)

// Defensive frame length limit for incoming HAL messages.
// Classification: IMPLEMENTATION_CHOICE.
const MaxCameraHALMessageLen uint32 = 10 * 1024 * 1024 // 10 MB bounded maximum

// CameraState models observable lifecycle states of the camera bridge handler.
// Classification: RECONSTRUCTED_SEMANTIC_MODEL.
type CameraState int

const (
	StateUninitialized CameraState = iota
	StateConnectingHAL
	StateHALHandshake
	StateIdleWaitHAL
	StateActiveStreaming
	StatePaused
	StateClosed
)

func (s CameraState) String() string {
	switch s {
	case StateUninitialized:
		return "STATE_UNINITIALIZED"
	case StateConnectingHAL:
		return "STATE_CONNECTING_HAL"
	case StateHALHandshake:
		return "STATE_HAL_HANDSHAKE"
	case StateIdleWaitHAL:
		return "STATE_IDLE_WAIT_HAL"
	case StateActiveStreaming:
		return "STATE_ACTIVE_STREAMING"
	case StatePaused:
		return "STATE_PAUSED"
	case StateClosed:
		return "STATE_CLOSED"
	default:
		return "STATE_UNKNOWN"
	}
}

// CameraConfig holds configuration for the camera HAL/bridge endpoint.
// Classification: GENERATED_ADAPTER / IMPLEMENTATION_CHOICE.
type CameraConfig struct {
	Address     string
	ForceCamera bool
	Width       int
	Height      int
	FrameRate   float64
	DialTimeout time.Duration
}

// DefaultCameraConfig returns configuration populated with evidence-backed defaults.
// Classification: GENERATED_ADAPTER.
func DefaultCameraConfig() CameraConfig {
	return CameraConfig{
		Address:     DefaultCameraAddress,
		ForceCamera: false,
		Width:       DefaultCameraWidth,
		Height:      DefaultCameraHeight,
		FrameRate:   DefaultCameraFrameRate,
		DialTimeout: DefaultCameraTimeout,
	}
}

// NormalizeCameraConfig ensures all fields have non-zero evidence-backed defaults.
// Classification: GENERATED_ADAPTER / IMPLEMENTATION_CHOICE.
func NormalizeCameraConfig(cfg CameraConfig) CameraConfig {
	if cfg.Address == "" {
		cfg.Address = DefaultCameraAddress
	}
	if cfg.Width <= 0 {
		cfg.Width = DefaultCameraWidth
	}
	if cfg.Height <= 0 {
		cfg.Height = DefaultCameraHeight
	}
	if cfg.FrameRate <= 0 {
		cfg.FrameRate = DefaultCameraFrameRate
	}
	if cfg.DialTimeout <= 0 {
		cfg.DialTimeout = DefaultCameraTimeout
	}
	return cfg
}

// ResolveCameraConfigFromSources resolves camera configuration from CLI flags, env vars, and defaults.
// Evidence:
//   -camera-addr, -force-camera (STRINGS.json lines 23796, 23852)
//   CP_AGENT_CAMERA_ADDR (STRINGS.json line 23852)
// Note: CP_AGENT_FORCE_CAMERA is an optional extension classified as IMPLEMENTATION_CHOICE_EXTENSION.
// Classification: GENERATED_ADAPTER / RECONSTRUCTED_FROM_BINARY.
func ResolveCameraConfigFromSources(base CameraConfig, args []string, getenv func(string) string) CameraConfig {
	cfg := base
	if getenv == nil {
		getenv = os.Getenv
	}

	// 1. Environment variables
	if envAddr := getenv("CP_AGENT_CAMERA_ADDR"); envAddr != "" {
		cfg.Address = envAddr
	}
	if envForce := getenv("CP_AGENT_FORCE_CAMERA"); envForce != "" {
		if b, err := strconv.ParseBool(envForce); err == nil {
			cfg.ForceCamera = b
		}
	}

	// 2. CLI flags (precedence over env)
	for i := 0; i < len(args); i++ {
		arg := args[i]
		if arg == "-camera-addr" || arg == "--camera-addr" {
			if i+1 < len(args) {
				cfg.Address = args[i+1]
				i++
			}
		} else if strings.HasPrefix(arg, "-camera-addr=") {
			cfg.Address = strings.TrimPrefix(arg, "-camera-addr=")
		} else if strings.HasPrefix(arg, "--camera-addr=") {
			cfg.Address = strings.TrimPrefix(arg, "--camera-addr=")
		} else if arg == "-force-camera" || arg == "--force-camera" {
			cfg.ForceCamera = true
		} else if strings.HasPrefix(arg, "-force-camera=") {
			val := strings.TrimPrefix(arg, "-force-camera=")
			if b, err := strconv.ParseBool(val); err == nil {
				cfg.ForceCamera = b
			}
		} else if strings.HasPrefix(arg, "--force-camera=") {
			val := strings.TrimPrefix(arg, "--force-camera=")
			if b, err := strconv.ParseBool(val); err == nil {
				cfg.ForceCamera = b
			}
		}
	}

	return NormalizeCameraConfig(cfg)
}

// ResolveCameraConfig resolves camera configuration using os.Args and os.Getenv.
// Classification: GENERATED_ADAPTER.
func ResolveCameraConfig(base CameraConfig) CameraConfig {
	var args []string
	if len(os.Args) > 1 {
		args = os.Args[1:]
	}
	return ResolveCameraConfigFromSources(base, args, os.Getenv)
}

// ProbeCameraBridge performs an independent TCP probe of the Camera HAL endpoint.
// Returns true if probe succeeds or if ForceCamera override is active.
// Classification: RECONSTRUCTED_FROM_BINARY.
func ProbeCameraBridge(cfg CameraConfig) bool {
	cfg = NormalizeCameraConfig(cfg)
	conn, err := net.DialTimeout("tcp", cfg.Address, cfg.DialTimeout)
	if err == nil {
		_ = conn.Close()
		return true
	}
	return cfg.ForceCamera
}

// CameraBridge represents a bidirectional communication channel to the Camera HAL.
// Classification: GENERATED_ADAPTER / IMPLEMENTATION_CHOICE.
type CameraBridge interface {
	io.ReadWriteCloser
}

// CameraBridgeDialer establishes a connection to the Camera HAL endpoint.
// Classification: GENERATED_ADAPTER / IMPLEMENTATION_CHOICE.
type CameraBridgeDialer func(ctx context.Context, network, address string) (net.Conn, error)

// DefaultCameraBridgeDialer uses standard net.Dialer.
// Classification: GENERATED_ADAPTER.
var DefaultCameraBridgeDialer CameraBridgeDialer = func(ctx context.Context, network, address string) (net.Conn, error) {
	var d net.Dialer
	return d.DialContext(ctx, network, address)
}

// CameraHandshake represents the initial configuration sent to the Camera HAL.
// Classification: RECONSTRUCTED_FROM_BINARY.
type CameraHandshake struct {
	Width     int     `json:"width"`
	Height    int     `json:"height"`
	FrameRate float64 `json:"frame_rate"`
}

// writeAll guarantees that all bytes of buf are written to w, looping until written == len(buf).
// Returns io.ErrNoProgress if a Write returns n == 0 with err == nil.
// Classification: IMPLEMENTATION_CHOICE / DEFENSIVE_ROBUSTNESS.
func writeAll(w io.Writer, buf []byte) error {
	written := 0
	for written < len(buf) {
		n, err := w.Write(buf[written:])
		if n > 0 {
			written += n
		}
		if err != nil {
			return err
		}
		if n == 0 && err == nil {
			return io.ErrNoProgress
		}
	}
	return nil
}

// writeCameraFrame transmits a 4-byte little-endian length prefix followed by the payload
// with complete-write semantics.
// Wire vectors:
//   0      => 00 00 00 00
//   6      => 06 00 00 00
//   28     => 1c 00 00 00
//   34     => 22 00 00 00
//   35     => 23 00 00 00
//   460800 => 00 08 07 00
// Classification: RECONSTRUCTED_FROM_BINARY.
func writeCameraFrame(w io.Writer, payload []byte) error {
	var lenBuf [4]byte
	binary.LittleEndian.PutUint32(lenBuf[:], uint32(len(payload)))
	if err := writeAll(w, lenBuf[:]); err != nil {
		return err
	}
	if len(payload) > 0 {
		if err := writeAll(w, payload); err != nil {
			return err
		}
	}
	return nil
}

// readCameraFrame reads a 4-byte little-endian length prefix followed by bounded payload.
// Classification: RECONSTRUCTED_FROM_BINARY (io.ReadFull + binary.LittleEndian).
func readCameraFrame(r io.Reader, maxLen uint32) ([]byte, error) {
	var lenBuf [4]byte
	if _, err := io.ReadFull(r, lenBuf[:]); err != nil {
		return nil, err
	}
	length := binary.LittleEndian.Uint32(lenBuf[:])
	if length > maxLen {
		return nil, fmt.Errorf("camera frame length %d exceeds maximum limit %d", length, maxLen)
	}
	payload := make([]byte, length)
	if length > 0 {
		if _, err := io.ReadFull(r, payload); err != nil {
			return nil, err
		}
	}
	return payload, nil
}

// ConvertImageToI420 converts a decoded image.Image to contiguous Planar I420 (YUV420P).
// Memory layout:
//   Y plane:  width * height bytes
//   U (Cb):   (width/2) * (height/2) bytes
//   V (Cr):   (width/2) * (height/2) bytes
//   Total:    width * height * 3 / 2 bytes
// Supports fast contiguous copy, row-by-row stride handling, and Rec.601 generic fallback.
// Enforces exact parity: dimensions must be even (integer division w/2, h/2).
// Disassembly: ARM64 0x51c2cc-0x51c2f8.
// Classification: RECONSTRUCTED_FROM_BINARY.
func ConvertImageToI420(img image.Image) ([]byte, error) {
	if img == nil {
		return nil, errors.New("cannot convert nil image to I420")
	}

	bounds := img.Bounds()
	w := bounds.Dx()
	h := bounds.Dy()
	if w <= 0 || h <= 0 {
		return nil, fmt.Errorf("invalid image dimensions: %dx%d", w, h)
	}
	if w%2 != 0 || h%2 != 0 {
		return nil, fmt.Errorf("image dimensions must be even for exact I420 conversion: %dx%d", w, h)
	}

	ySize := w * h
	uvWidth := w / 2
	uvHeight := h / 2
	uvSize := uvWidth * uvHeight
	totalSize := ySize + 2*uvSize

	out := make([]byte, totalSize)

	// Fast path and stride path for *image.YCbCr with 4:2:0 subsampling
	if yuv, ok := img.(*image.YCbCr); ok && yuv.SubsampleRatio == image.YCbCrSubsampleRatio420 {
		// Contiguous fast path: YStride == width, CStride == width/2, min bounds at 0,0
		if yuv.YStride == w && yuv.CStride == uvWidth && bounds.Min.X == 0 && bounds.Min.Y == 0 {
			copy(out[0:ySize], yuv.Y[:ySize])
			copy(out[ySize:ySize+uvSize], yuv.Cb[:uvSize])
			copy(out[ySize+uvSize:totalSize], yuv.Cr[:uvSize])
			return out, nil
		}

		// Stride path: row-by-row copy respecting stride offsets
		for y := 0; y < h; y++ {
			srcY := yuv.YOffset(bounds.Min.X, bounds.Min.Y+y)
			copy(out[y*w:(y+1)*w], yuv.Y[srcY:srcY+w])
		}
		for y := 0; y < uvHeight; y++ {
			srcC := yuv.COffset(bounds.Min.X, bounds.Min.Y+y*2)
			uDest := ySize + y*uvWidth
			vDest := ySize + uvSize + y*uvWidth
			copy(out[uDest:uDest+uvWidth], yuv.Cb[srcC:srcC+uvWidth])
			copy(out[vDest:vDest+uvWidth], yuv.Cr[srcC:srcC+uvWidth])
		}
		return out, nil
	}

	// Generic fallback: Rec.601 RGB-to-YUV conversion
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			r, g, b, _ := img.At(bounds.Min.X+x, bounds.Min.Y+y).RGBA()
			r8, g8, b8 := uint8(r>>8), uint8(g>>8), uint8(b>>8)
			yVal, _, _ := color.RGBToYCbCr(r8, g8, b8)
			out[y*w+x] = yVal
		}
	}

	for y := 0; y < uvHeight; y++ {
		for x := 0; x < uvWidth; x++ {
			srcX := bounds.Min.X + x*2
			srcY := bounds.Min.Y + y*2
			if srcX >= bounds.Max.X {
				srcX = bounds.Max.X - 1
			}
			if srcY >= bounds.Max.Y {
				srcY = bounds.Max.Y - 1
			}
			r, g, b, _ := img.At(srcX, srcY).RGBA()
			r8, g8, b8 := uint8(r>>8), uint8(g>>8), uint8(b>>8)
			_, uVal, vVal := color.RGBToYCbCr(r8, g8, b8)

			out[ySize+y*uvWidth+x] = uVal
			out[ySize+uvSize+y*uvWidth+x] = vVal
		}
	}

	return out, nil
}

// CameraHandler manages the lifecycle and data plane of camera-channel and Camera HAL bridge.
// Classification: RECONSTRUCTED_FROM_BINARY / GENERATED_ADAPTER.
type CameraHandler struct {
	mu            sync.RWMutex
	bridgeWriteMu sync.Mutex // Serializes all framed writes (prefix + payload) to bridgeConn

	config CameraConfig
	dialer CameraBridgeDialer

	dataChannel *webrtc.DataChannel
	bridgeConn  net.Conn

	state CameraState

	latestCameraJpeg []byte
	cameraFrameChan  chan []byte // Capacity strictly 1

	ctx            context.Context
	cancel         context.CancelFunc
	wg             sync.WaitGroup
	closedOnce     sync.Once
	workersStarted bool
}

// NewCameraHandler creates a new CameraHandler for an active PeerSession.
// Classification: GENERATED_ADAPTER / RECONSTRUCTED_FROM_BINARY.
func NewCameraHandler(cfg CameraConfig, dialer CameraBridgeDialer) *CameraHandler {
	if dialer == nil {
		dialer = DefaultCameraBridgeDialer
	}
	ctx, cancel := context.WithCancel(context.Background())
	return &CameraHandler{
		config:          NormalizeCameraConfig(cfg),
		dialer:          dialer,
		state:           StateUninitialized,
		cameraFrameChan: make(chan []byte, 1), // Strictly single-element capacity
		ctx:             ctx,
		cancel:          cancel,
	}
}

// Attach binds the camera-channel DataChannel and registers active lifecycle handlers.
// Classification: RECONSTRUCTED_FROM_BINARY (ARM64 0x51a024-0x51a0f8).
func (h *CameraHandler) Attach(dc *webrtc.DataChannel) {
	h.mu.Lock()
	h.dataChannel = dc
	h.mu.Unlock()

	dc.OnOpen(h.onOpen)
	dc.OnMessage(h.onMessage)
	dc.OnClose(h.onClose)
}

// writeBridgeFrame serializes all framed message writes (prefix + payload) to the bridge connection.
// Prevents interleaving of concurrent YUV stream writes and snapshot responses.
// Classification: DEFENSIVE_ROBUSTNESS / IMPLEMENTATION_CHOICE.
func (h *CameraHandler) writeBridgeFrame(payload []byte) error {
	h.bridgeWriteMu.Lock()
	defer h.bridgeWriteMu.Unlock()

	h.mu.RLock()
	conn := h.bridgeConn
	closed := (h.state == StateClosed)
	h.mu.RUnlock()

	if closed || conn == nil {
		return net.ErrClosed
	}
	return writeCameraFrame(conn, payload)
}

// signalFailure centralizes fatal bridge failure signaling.
// Transitions state, cancels context, and closes bridge connection without self-waiting on wg.
// Classification: DEFENSIVE_ROBUSTNESS / IMPLEMENTATION_CHOICE.
func (h *CameraHandler) signalFailure(err error) {
	h.closedOnce.Do(func() {
		h.mu.Lock()
		h.state = StateClosed
		conn := h.bridgeConn
		h.bridgeConn = nil
		h.mu.Unlock()

		h.cancel()

		if conn != nil {
			_ = conn.Close()
		}
	})
}

// onOpen establishes the bridge connection, sends handshake, and starts workers.
func (h *CameraHandler) onOpen() {
	h.mu.Lock()
	if h.state == StateClosed || h.ctx.Err() != nil {
		h.mu.Unlock()
		return
	}
	h.state = StateConnectingHAL
	cfg := h.config
	dialer := h.dialer
	h.mu.Unlock()

	// Apply DialTimeout to active bridge connect
	dialTimeout := cfg.DialTimeout
	if dialTimeout <= 0 {
		dialTimeout = DefaultCameraTimeout
	}
	dialCtx, dialCancel := context.WithTimeout(h.ctx, dialTimeout)
	conn, err := dialer(dialCtx, "tcp", cfg.Address)
	dialCancel()
	if err != nil {
		log.Printf("[Camera] ERROR: failed to connect to Camera HAL at %s: %v", cfg.Address, err)
		_ = h.Close()
		return
	}

	h.mu.Lock()
	if h.state == StateClosed || h.ctx.Err() != nil {
		h.mu.Unlock()
		_ = conn.Close()
		return
	}
	h.bridgeConn = conn
	h.state = StateHALHandshake
	h.mu.Unlock()

	// Send length-prefixed JSON handshake: width, height, frame_rate
	handshake := CameraHandshake{
		Width:     cfg.Width,
		Height:    cfg.Height,
		FrameRate: cfg.FrameRate,
	}
	handshakeBytes, err := json.Marshal(handshake)
	if err != nil {
		_ = h.Close()
		return
	}

	if err := h.writeBridgeFrame(handshakeBytes); err != nil {
		log.Printf("[Camera] ERROR: failed to send handshake to Camera HAL: %v", err)
		_ = h.Close()
		return
	}

	// Atomically verify lifecycle state before launching background workers
	h.mu.Lock()
	if h.state == StateClosed || h.ctx.Err() != nil {
		h.mu.Unlock()
		return
	}
	h.state = StateIdleWaitHAL
	h.wg.Add(2)
	h.workersStarted = true
	h.mu.Unlock()

	// Launch background workers
	go h.readBridgeEvents(conn)
	go h.processFrames(conn)
}

// onMessage processes incoming WebRTC messages from the browser client.
// Binary frames are cached under mutex protection BEFORE non-blocking enqueue.
// Text frames are safely ignored as frame data.
// Classification: RECONSTRUCTED_FROM_BINARY (ARM64 0x51a318-0x51a388).
func (h *CameraHandler) onMessage(msg webrtc.DataChannelMessage) {
	if msg.IsString {
		// Reject or ignore inbound text payloads as camera frame data
		return
	}

	// 1. Copy incoming JPEG bytes safely (do not retain Pion buffer)
	dataCopy := make([]byte, len(msg.Data))
	copy(dataCopy, msg.Data)

	// 2. Snapshot cache ordering: Update latestCameraJpeg under mutex BEFORE enqueue
	h.mu.Lock()
	h.latestCameraJpeg = dataCopy
	h.mu.Unlock()

	// 3. Non-blocking enqueue to cameraFrameChan (capacity=1)
	select {
	case h.cameraFrameChan <- dataCopy:
	default:
		// Frame dropped from streaming queue to minimize latency; snapshot cache is already updated!
	}
}

// onClose terminates the bridge session and cleans up resources.
func (h *CameraHandler) onClose() {
	_ = h.Close()
}

// readBridgeEvents processes inbound event frames from the Camera HAL socket.
// Recognizes VIRTUAL_DEVICE_START_CAMERA_SESSION, VIRTUAL_DEVICE_STOP_CAMERA_SESSION,
// and VIRTUAL_DEVICE_CAPTURE_IMAGE.
// Classification: RECONSTRUCTED_FROM_BINARY (ARM64 0x51aa8c-0x51af50).
func (h *CameraHandler) readBridgeEvents(conn net.Conn) {
	defer h.wg.Done()

	for {
		payload, err := readCameraFrame(conn, MaxCameraHALMessageLen)
		if err != nil {
			// Read error or EOF: signal centralized failure to terminate sibling worker
			h.signalFailure(err)
			return
		}

		event := string(payload)
		switch event {
		case HALEventStartCameraSession:
			h.mu.Lock()
			if h.state != StateClosed {
				h.state = StateActiveStreaming
			}
			dc := h.dataChannel
			h.mu.Unlock()

			if dc != nil {
				_ = dc.SendText(`{"action":"start"}`)
			}

		case HALEventStopCameraSession:
			h.mu.Lock()
			if h.state != StateClosed {
				h.state = StatePaused
			}
			dc := h.dataChannel
			h.mu.Unlock()

			if dc != nil {
				_ = dc.SendText(`{"action":"stop"}`)
			}

		case HALEventCaptureImage:
			h.mu.RLock()
			snapshot := h.latestCameraJpeg
			h.mu.RUnlock()

			// Snapshot response: serialized framed write via writeBridgeFrame
			if err := h.writeBridgeFrame(snapshot); err != nil {
				h.signalFailure(err)
				return
			}

		default:
			// Unknown HAL event: must not panic; safe ignore/log (IMPLEMENTATION_CHOICE)
			log.Printf("[Camera] WARN: unrecognized HAL event: %s", event)
		}
	}
}

// processFrames consumes queued JPEG frames, decodes them, converts to Planar I420,
// and writes them framed to the Camera HAL connection.
// Classification: RECONSTRUCTED_FROM_BINARY (ARM64 0x51c250-0x51c780).
func (h *CameraHandler) processFrames(conn net.Conn) {
	defer h.wg.Done()

	for {
		select {
		case <-h.ctx.Done():
			return
		case frameData, ok := <-h.cameraFrameChan:
			if !ok {
				return
			}

			// Decode JPEG
			img, err := jpeg.Decode(bytes.NewReader(frameData))
			if err != nil {
				// Malformed JPEG: record error safely, do not panic, do not send corrupt YUV
				continue
			}

			// Convert to Planar I420
			i420, err := ConvertImageToI420(img)
			if err != nil {
				continue
			}

			// Write 4-byte LE length-prefixed Planar I420 frame to HAL via writeBridgeFrame
			if err := h.writeBridgeFrame(i420); err != nil {
				h.signalFailure(err)
				return
			}
		}
	}
}

// GetState returns the current observable semantic state.
// Classification: GENERATED_ADAPTER.
func (h *CameraHandler) GetState() CameraState {
	h.mu.RLock()
	defer h.mu.RUnlock()
	return h.state
}

// GetLatestCameraJpeg returns a copy of the latest cached snapshot JPEG.
// Classification: GENERATED_ADAPTER.
func (h *CameraHandler) GetLatestCameraJpeg() []byte {
	h.mu.RLock()
	defer h.mu.RUnlock()
	if len(h.latestCameraJpeg) == 0 {
		return nil
	}
	cp := make([]byte, len(h.latestCameraJpeg))
	copy(cp, h.latestCameraJpeg)
	return cp
}

// Close gracefully and idempotently shuts down the CameraHandler.
// Classification: RECONSTRUCTED_FROM_BEHAVIOR.
func (h *CameraHandler) Close() error {
	var closeErr error
	h.closedOnce.Do(func() {
		h.mu.Lock()
		h.state = StateClosed
		conn := h.bridgeConn
		h.bridgeConn = nil
		h.mu.Unlock()

		h.cancel()

		if conn != nil {
			closeErr = conn.Close()
		}
	})
	h.wg.Wait()
	return closeErr
}
