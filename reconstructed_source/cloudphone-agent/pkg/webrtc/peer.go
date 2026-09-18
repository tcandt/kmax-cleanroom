// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_PEERCONNECTION_LIFECYCLE_AND_CALLGRAPH
// Evidence: WEBRTC_PEERCONNECTION_CALLGRAPH.json, WEBRTC_PEERCONNECTION_STATE_MACHINE.json,
//   WEBRTC_TOPOLOGY_CROSSMAP.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Disassembly:
//   PeerConnection Setup: main.(*IDhLgq).woxaqqFN5Km (0x9df9c0)
//   CreateOffer: v6LoFegGUKTA.(*BtQfb9).CreateOffer (0x93d540)
//   SetLocalDescription: v6LoFegGUKTA.(*BtQfb9).SetLocalDescription (0x93f7a0)
//   SetRemoteDescription: v6LoFegGUKTA.(*BtQfb9).SetRemoteDescription (0x93fd80)
//   AddICECandidate: v6LoFegGUKTA.(*BtQfb9).AddICECandidate (0x947140)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"errors"
	"fmt"
	"sync"

	"github.com/pion/webrtc/v3"
)

var (
	ErrSessionClosed   = errors.New("webrtc peer session is closed")
	ErrInvalidState    = errors.New("operation invalid for current session state")
	ErrEmptyRemoteSDP  = errors.New("remote sdp description is empty")
)

// PeerSessionOptions parameterizes the creation of a PeerSession.
// Classification: GENERATED_ADAPTER / IMPLEMENTATION_CHOICE.
type PeerSessionOptions struct {
	ClientID      uint32
	DeviceID      string
	ICEServers    []webrtc.ICEServer
	CameraSupport bool
	CameraConfig  CameraConfig
	CameraDialer  CameraBridgeDialer
}

// PeerSession encapsulates the state and lifecycle of an active WebRTC PeerConnection
// between the cloudphone-agent and a connected client.
// Classification: RECONSTRUCTED_FROM_BINARY.
type PeerSession struct {
	mu sync.RWMutex

	ClientID uint32
	DeviceID string

	PC            *webrtc.PeerConnection
	Media         *MediaTracks
	Channels      *DataChannels
	CameraHandler *CameraHandler
	CameraSupport bool
	CameraConfig  CameraConfig
	State         SessionState
	closedOnce    sync.Once

	onCandidateCb func(webrtc.ICECandidateInit)
	onStateCb     func(SessionState)
	onCloseCb     func()
}

// NewPeerSession initializes a PeerSession with default cameraSupport=false.
// Classification: GENERATED_ADAPTER.
func NewPeerSession(clientID uint32, deviceID string, iceServers []webrtc.ICEServer) (*PeerSession, error) {
	return NewPeerSessionWithOptions(PeerSessionOptions{
		ClientID:      clientID,
		DeviceID:      deviceID,
		ICEServers:    iceServers,
		CameraSupport: false,
		CameraConfig:  DefaultCameraConfig(),
	})
}

// NewPeerSessionWithOptions initializes a fully configured PeerSession matching the original binary lifecycle:
// 1. Instantiates Pion API with evidence-bound MediaEngine (H.264 / Opus only).
// 2. Creates PeerConnection with ICE server configuration.
// 3. Adds confirmed video (display_0) and audio (audio_0) tracks.
// 4. Creates outbound DataChannels (input, clipboard, and conditionally camera if CameraSupport==true).
// 5. If CameraSupport==true, instantiates and attaches CameraHandler to camera-channel.
// 6. Registers OnDataChannel callback for inbound channels (file, ai, adb).
// 7. Configures ICE candidate and connection state monitoring.
// Classification: RECONSTRUCTED_FROM_BINARY.
func NewPeerSessionWithOptions(opts PeerSessionOptions) (*PeerSession, error) {
	api, err := NewAPIWithEvidenceBoundEngine()
	if err != nil {
		return nil, fmt.Errorf("failed to build webrtc API: %w", err)
	}

	rtcConfig := BuildRTCConfiguration(opts.ICEServers)
	pc, err := api.NewPeerConnection(rtcConfig)
	if err != nil {
		return nil, fmt.Errorf("failed to create PeerConnection: %w", err)
	}

	// Attach confirmed MediaTracks
	mediaTracks, err := NewConfirmedMediaTracks()
	if err != nil {
		_ = pc.Close()
		return nil, fmt.Errorf("failed to create media tracks: %w", err)
	}

	if _, err := pc.AddTrack(mediaTracks.VideoTrack); err != nil {
		_ = pc.Close()
		return nil, fmt.Errorf("failed to add video track: %w", err)
	}

	if _, err := pc.AddTrack(mediaTracks.AudioTrack); err != nil {
		_ = pc.Close()
		return nil, fmt.Errorf("failed to add audio track: %w", err)
	}

	// Setup confirmed DataChannels
	channels := NewDataChannels()

	var camHandler *CameraHandler
	if opts.CameraSupport {
		camHandler = NewCameraHandler(opts.CameraConfig, opts.CameraDialer)
		channels.SetCameraHandler(camHandler)
	}

	if err := channels.SetupOutboundChannels(pc, opts.CameraSupport); err != nil {
		_ = pc.Close()
		if camHandler != nil {
			_ = camHandler.Close()
		}
		return nil, fmt.Errorf("failed to setup outbound datachannels: %w", err)
	}
	channels.RegisterInboundHandler(pc)

	session := &PeerSession{
		ClientID:      opts.ClientID,
		DeviceID:      opts.DeviceID,
		PC:            pc,
		Media:         mediaTracks,
		Channels:      channels,
		CameraHandler: camHandler,
		CameraSupport: opts.CameraSupport,
		CameraConfig:  opts.CameraConfig,
		State:         SessionStateConnecting,
	}

	// ICE Candidate listener
	pc.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c == nil {
			return
		}
		init := c.ToJSON()
		session.mu.RLock()
		cb := session.onCandidateCb
		session.mu.RUnlock()

		if cb != nil {
			cb(init)
		}
	})

	// Connection State listener
	pc.OnConnectionStateChange(func(pcs webrtc.PeerConnectionState) {
		session.mu.Lock()
		switch pcs {
		case webrtc.PeerConnectionStateConnected:
			session.State = SessionStateConnected
		case webrtc.PeerConnectionStateFailed:
			session.State = SessionStateFailed
		case webrtc.PeerConnectionStateClosed:
			session.State = SessionStateClosed
		}
		currentState := session.State
		stateCb := session.onStateCb
		session.mu.Unlock()

		if stateCb != nil {
			stateCb(currentState)
		}

		if pcs == webrtc.PeerConnectionStateFailed {
			// Trigger cleanup on failure per cleanup trigger matrix
			_ = session.Close()
		}
	})

	return session, nil
}

// OnICECandidate sets the callback invoked when the local peer gathers an ICE candidate.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) OnICECandidate(cb func(webrtc.ICECandidateInit)) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.onCandidateCb = cb
}

// OnSessionStateChange sets the callback invoked when the session state changes.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) OnSessionStateChange(cb func(SessionState)) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.onStateCb = cb
}

// OnClose sets the callback invoked when the session is closed.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) OnClose(cb func()) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.onCloseCb = cb
}

// CreateOffer generates the SDP offer, applies it locally via SetLocalDescription,
// and packages it into a SignalingPayload with camera_support=true.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (s *PeerSession) CreateOffer() (*SignalingPayload, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.State == SessionStateClosed {
		return nil, ErrSessionClosed
	}

	offer, err := s.PC.CreateOffer(nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create offer: %w", err)
	}

	if err := s.PC.SetLocalDescription(offer); err != nil {
		return nil, fmt.Errorf("failed to set local description: %w", err)
	}

	s.State = SessionStateHaveLocalOffer
	cameraSupport := s.CameraSupport

	return &SignalingPayload{
		Type:          "offer",
		SDP:           offer.SDP,
		CameraSupport: &cameraSupport,
	}, nil
}

// HandleRemoteAnswer applies the remote client's SDP answer via SetRemoteDescription.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (s *PeerSession) HandleRemoteAnswer(sdp string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.State == SessionStateClosed {
		return ErrSessionClosed
	}
	if sdp == "" {
		return ErrEmptyRemoteSDP
	}

	desc := webrtc.SessionDescription{
		Type: webrtc.SDPTypeAnswer,
		SDP:  sdp,
	}

	if err := s.PC.SetRemoteDescription(desc); err != nil {
		return fmt.Errorf("failed to set remote description: %w", err)
	}

	s.State = SessionStateHaveRemoteAnswer
	return nil
}

// AddRemoteCandidate applies a remote trickle ICE candidate to the PeerConnection.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (s *PeerSession) AddRemoteCandidate(candidate webrtc.ICECandidateInit) error {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if s.State == SessionStateClosed {
		return ErrSessionClosed
	}

	return s.PC.AddICECandidate(candidate)
}

// Close gracefully and idempotently terminates the PeerConnection and local resources.
// Classification: RECONSTRUCTED_FROM_BEHAVIOR.
func (s *PeerSession) Close() error {
	var closeErr error
	s.closedOnce.Do(func() {
		s.mu.Lock()
		s.State = SessionStateClosed
		camHandler := s.CameraHandler
		closeCb := s.onCloseCb
		s.mu.Unlock()

		if camHandler != nil {
			_ = camHandler.Close()
		}

		if s.PC != nil {
			closeErr = s.PC.Close()
		}

		if closeCb != nil {
			closeCb()
		}
	})
	return closeErr
}

// GetState returns the current internal session state.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) GetState() SessionState {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.State
}

// SetControlSink binds a ControlSink to the session's DataChannels container.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) SetControlSink(sink ControlSink) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.Channels != nil {
		s.Channels.SetControlSink(sink)
	}
}

// SetClipboardProvider binds a ClipboardProvider to the session's DataChannels container.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) SetClipboardProvider(provider ClipboardProvider) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.Channels != nil {
		s.Channels.SetClipboardProvider(provider)
	}
}

// SetFileHandler binds a FileChannelHandler to the session's DataChannels container.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) SetFileHandler(handler *FileChannelHandler) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.Channels != nil {
		s.Channels.SetFileHandler(handler)
	}
}

// SetCameraHandler binds a CameraHandler to the session's DataChannels container.
// Classification: GENERATED_ADAPTER.
func (s *PeerSession) SetCameraHandler(handler *CameraHandler) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.CameraHandler = handler
	if s.Channels != nil {
		s.Channels.SetCameraHandler(handler)
	}
}

