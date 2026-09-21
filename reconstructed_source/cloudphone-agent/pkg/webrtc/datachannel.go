// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_DATACHANNEL_CREATION_AND_LIFECYCLE_REGISTRATION
// Evidence: DATACHANNEL_LABEL_EVIDENCE.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Disassembly:
//   Outbound: main.(*IDhLgq).woxaqqFN5Km (0x9e1f4f input, 0x9e1ff7 clipboard, 0x9e216d camera)
//   Inbound: main.(*IDhLgq).woxaqqFN5Km.func11 (0x9e2f40 dispatch)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// STRICT B1 BOUNDARY: Instantiates inert lifecycle hooks only for negotiation parity.
// Full business logic (touch injection, clipboard sync, virtual camera, file chunking,
// AI commands, ADB) is explicitly DEFERRED to subsequent subphases (B2-B4).
// Confidence: HIGH

package webrtc

import (
	"encoding/json"
	"fmt"
	"log"
	"sync"

	"github.com/pion/webrtc/v3"
)

// Confirmed DataChannel labels from DATACHANNEL_LABEL_EVIDENCE.json
const (
	// Outbound channels created by the Agent
	ChannelInput     = "input-channel"
	ChannelClipboard = "clipboard-channel"
	ChannelCamera    = "camera-channel"

	// Inbound channels created by the Browser Client
	ChannelFile      = "file-channel"
	ChannelAICommand = "ai-command-channel"
	ChannelADB       = "adb-channel"
)

// DataChannels holds references to all 6 confirmed WebRTC DataChannels.
// Classification: RECONSTRUCTED_FROM_BINARY.
type DataChannels struct {
	mu sync.RWMutex

	ClientID uint32

	// Outbound
	InputChannel     *webrtc.DataChannel
	ClipboardChannel *webrtc.DataChannel
	CameraChannel    *webrtc.DataChannel

	// Inbound
	FileChannel      *webrtc.DataChannel
	AICommandChannel *webrtc.DataChannel
	ADBChannel       *webrtc.DataChannel

	ControlSink       ControlSink
	ClipboardProvider ClipboardProvider
	FileHandler       *FileChannelHandler
	CameraHandler     *CameraHandler
}

// NewDataChannels initializes the container for the 6 confirmed DataChannels.
// Classification: GENERATED_ADAPTER.
func NewDataChannels() *DataChannels {
	return &DataChannels{}
}

// SetControlSink configures the sink for incoming input-channel control messages.
func (dc *DataChannels) SetControlSink(sink ControlSink) {
	dc.mu.Lock()
	defer dc.mu.Unlock()
	dc.ControlSink = sink
}

// SetClipboardProvider configures the provider for incoming clipboard-channel requests.
func (dc *DataChannels) SetClipboardProvider(provider ClipboardProvider) {
	dc.mu.Lock()
	defer dc.mu.Unlock()
	dc.ClipboardProvider = provider
}

// SetFileHandler configures the handler for incoming file-channel uploads.
// Classification: GENERATED_ADAPTER.
func (dc *DataChannels) SetFileHandler(handler *FileChannelHandler) {
	dc.mu.Lock()
	defer dc.mu.Unlock()
	dc.FileHandler = handler
	if handler != nil && dc.FileChannel != nil {
		handler.Attach(dc.FileChannel)
	}
}

// SetCameraHandler binds a CameraHandler to the outbound camera DataChannel.
// Classification: GENERATED_ADAPTER.
func (dc *DataChannels) SetCameraHandler(handler *CameraHandler) {
	dc.mu.Lock()
	defer dc.mu.Unlock()
	dc.CameraHandler = handler
	if handler != nil && dc.CameraChannel != nil {
		handler.Attach(dc.CameraChannel)
	}
}

// SetupOutboundChannels creates the Agent-initiated DataChannels with ordered=true
// before the local SDP offer is created, matching original binary assembly.
// Outbound input-channel and clipboard-channel are always created.
// Outbound camera-channel is created ONLY IF cameraSupport == true.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (dc *DataChannels) SetupOutboundChannels(pc *webrtc.PeerConnection, cameraSupport bool) error {
	dc.mu.Lock()
	defer dc.mu.Unlock()

	ordered := true
	initOptions := &webrtc.DataChannelInit{
		Ordered: &ordered,
	}

	// 1. input-channel (Active in B2: translates JSON to 32-byte scrcpy binary frames)
	inputCh, err := pc.CreateDataChannel(ChannelInput, initOptions)
	if err != nil {
		return fmt.Errorf("failed to create %s: %w", ChannelInput, err)
	}
	attachInertLifecycleHooks(inputCh)
	inputCh.OnMessage(func(msg webrtc.DataChannelMessage) {
		dc.mu.RLock()
		sink := dc.ControlSink
		clientID := dc.ClientID
		dc.mu.RUnlock()

		var env RawInputEnvelope
		_ = json.Unmarshal(msg.Data, &env)
		var rawMap map[string]interface{}
		var seq interface{} = "none"
		if err := json.Unmarshal(msg.Data, &rawMap); err == nil {
			if s, ok := rawMap["control_seq"]; ok {
				seq = s
			} else if s, ok := rawMap["seq"]; ok {
				seq = s
			}
		}

		log.Printf("[DC-RX] clientID=%d channel=input-channel bytes=%d type=%s seq=%v sinkNil=%t",
			clientID, len(msg.Data), env.Type, seq, sink == nil)

		if sink == nil {
			log.Printf("[TOUCH-DROP-AGENT] reason=CONTROL_SINK_NIL clientID=%d seq=%v", clientID, seq)
			return
		}

		_ = HandleInputMessage(msg.Data, sink)
	})
	dc.InputChannel = inputCh

	// 2. clipboard-channel (Active in B2: handles get/set clipboard via ClipboardProvider)
	clipCh, err := pc.CreateDataChannel(ChannelClipboard, initOptions)
	if err != nil {
		return fmt.Errorf("failed to create %s: %w", ChannelClipboard, err)
	}
	attachInertLifecycleHooks(clipCh)
	clipCh.OnMessage(func(msg webrtc.DataChannelMessage) {
		dc.mu.RLock()
		provider := dc.ClipboardProvider
		dc.mu.RUnlock()
		if provider != nil {
			_ = HandleClipboardMessage(msg.Data, provider, func(out []byte) error {
				return clipCh.Send(out)
			})
		}
	})
	dc.ClipboardChannel = clipCh

	// 3. camera-channel (Created ONLY IF cameraSupport == true)
	if cameraSupport {
		camCh, err := pc.CreateDataChannel(ChannelCamera, initOptions)
		if err != nil {
			return fmt.Errorf("failed to create %s: %w", ChannelCamera, err)
		}
		attachInertLifecycleHooks(camCh)
		dc.CameraChannel = camCh
		if dc.CameraHandler != nil {
			dc.CameraHandler.Attach(camCh)
		}
	}

	return nil
}

// RegisterInboundHandler sets up the pc.OnDataChannel listener to register incoming
// browser-initiated DataChannels (file-channel, ai-command-channel, adb-channel).
// This is the ONE authoritative pc.OnDataChannel listener.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (dc *DataChannels) RegisterInboundHandler(pc *webrtc.PeerConnection) {
	pc.OnDataChannel(func(remoteDC *webrtc.DataChannel) {
		dc.mu.Lock()
		defer dc.mu.Unlock()

		label := remoteDC.Label()
		attachInertLifecycleHooks(remoteDC)

		switch label {
		case ChannelFile:
			dc.FileChannel = remoteDC
			if dc.FileHandler != nil {
				dc.FileHandler.Attach(remoteDC)
			}
		case ChannelAICommand:
			dc.AICommandChannel = remoteDC
		case ChannelADB:
			dc.ADBChannel = remoteDC
		default:
			// Unrecognized or auxiliary channel
		}
	})
}

// attachInertLifecycleHooks attaches minimal logging and lifecycle listeners.
// Business payload processing is DEFERRED to Phases B2-B4.
// Classification: GENERATED_ADAPTER.
func attachInertLifecycleHooks(d *webrtc.DataChannel) {
	d.OnOpen(func() {
		// Inert hook: State reached open
	})
	d.OnClose(func() {
		// Inert hook: State reached close
	})
	d.OnError(func(err error) {
		// Inert hook: Error logging
	})
	// In Phase B1, OnMessage is intentionally NOT attached with business logic
	// to prevent fake success returns. Business logic handlers are DEFERRED.
}

// GetChannel retrieves a DataChannel by its canonical label.
// Classification: GENERATED_ADAPTER.
func (dc *DataChannels) GetChannel(label string) *webrtc.DataChannel {
	dc.mu.RLock()
	defer dc.mu.RUnlock()

	switch label {
	case ChannelInput:
		return dc.InputChannel
	case ChannelClipboard:
		return dc.ClipboardChannel
	case ChannelCamera:
		return dc.CameraChannel
	case ChannelFile:
		return dc.FileChannel
	case ChannelAICommand:
		return dc.AICommandChannel
	case ChannelADB:
		return dc.ADBChannel
	default:
		return nil
	}
}
