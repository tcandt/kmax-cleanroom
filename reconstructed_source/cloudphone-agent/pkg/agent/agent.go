// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: AGENT_COORDINATOR_AND_SESSION_MULTIPLEXER
// Evidence: WEBRTC_PEERCONNECTION_CALLGRAPH.json, WEBRTC_TOPOLOGY_CROSSMAP.json,
//   WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Disassembly:
//   Signaling Dispatcher: main.(*IDhLgq).dizwnNrpwv (0x9c1540)
//   Session Coordinator: main.(*IDhLgq).f1PF7qVxR (0x9e59e0)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package agent

import (
	"encoding/json"
	"sync"

	agentwebrtc "cloudphone-agent/pkg/webrtc"
	"cloudphone-agent/pkg/signaling"
	"github.com/pion/webrtc/v3"
)

// FileSinkFactory constructs an isolated FileSink for a newly negotiated PeerSession.
// Classification: GENERATED_ADAPTER.
type FileSinkFactory func(clientID uint32) agentwebrtc.FileSink

// Coordinator orchestrates WebRTC sessions and binds them to the signaling transport.
// Classification: RECONSTRUCTED_FROM_BINARY.
type Coordinator struct {
	mu sync.RWMutex

	DeviceID   string
	ICEServers []webrtc.ICEServer

	signalingClient *signaling.Client
	sessions        map[uint32]*agentwebrtc.PeerSession

	controlSink       agentwebrtc.ControlSink
	clipboardProvider agentwebrtc.ClipboardProvider
	fileSinkFactory   FileSinkFactory
	postUploadAction  agentwebrtc.PostUploadActionHandler

	cameraConfig  agentwebrtc.CameraConfig
	cameraSupport bool
	cameraDialer  agentwebrtc.CameraBridgeDialer

	closed bool
}

// NewCoordinator initializes the agent coordinator.
// Probes default camera HAL bridge to establish cameraSupport status.
// Classification: GENERATED_ADAPTER.
func NewCoordinator(deviceID string, iceServers []webrtc.ICEServer) *Coordinator {
	cfg := agentwebrtc.DefaultCameraConfig()
	cfg = agentwebrtc.ResolveCameraConfig(cfg)
	support := agentwebrtc.ProbeCameraBridge(cfg)
	return &Coordinator{
		DeviceID:      deviceID,
		ICEServers:    iceServers,
		sessions:      make(map[uint32]*agentwebrtc.PeerSession),
		cameraConfig:  cfg,
		cameraSupport: support,
	}
}

// SetCameraConfig updates the camera configuration and refreshes the camera probe.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetCameraConfig(cfg agentwebrtc.CameraConfig) {
	c.mu.Lock()
	defer c.mu.Unlock()
	normCfg := agentwebrtc.NormalizeCameraConfig(cfg)
	c.cameraConfig = normCfg
	c.cameraSupport = agentwebrtc.ProbeCameraBridge(normCfg)
}

// SetCameraSupport explicitly overrides the camera support state (e.g. for testing).
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetCameraSupport(support bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.cameraSupport = support
}

// SetCameraDialer configures an injected dialer for the camera bridge (e.g. for testing).
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetCameraDialer(dialer agentwebrtc.CameraBridgeDialer) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.cameraDialer = dialer
}

// SetSignalingClient binds the active signaling WebSocket client.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetSignalingClient(client *signaling.Client) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.signalingClient = client
}

// SetControlSink binds the ControlSink adapter to the coordinator and all active sessions.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetControlSink(sink agentwebrtc.ControlSink) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.controlSink = sink
	for _, s := range c.sessions {
		s.SetControlSink(sink)
	}
}

// SetClipboardProvider binds the ClipboardProvider adapter to the coordinator and all active sessions.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetClipboardProvider(provider agentwebrtc.ClipboardProvider) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.clipboardProvider = provider
	for _, s := range c.sessions {
		s.SetClipboardProvider(provider)
	}
}

// SetFileSinkFactory configures the per-session FileSink factory on the coordinator.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetFileSinkFactory(factory FileSinkFactory) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.fileSinkFactory = factory
}

// SetPostUploadActionHandler configures the post-upload install action handler.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetPostUploadActionHandler(handler agentwebrtc.PostUploadActionHandler) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.postUploadAction = handler
}

// HandleConfig updates the ICE servers dynamically pushed from signaling.
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
func (c *Coordinator) HandleConfig(iceServers []webrtc.ICEServer) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.ICEServers = iceServers
}

// HandleForward processes WebRTC signaling messages multiplexed per client_id.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (c *Coordinator) HandleForward(clientID uint32, rawPayload json.RawMessage) {
	var payload agentwebrtc.SignalingPayload
	if err := json.Unmarshal(rawPayload, &payload); err != nil {
		return
	}

	switch payload.Type {
	case "request-offer":
		c.handleRequestOffer(clientID)

	case "answer":
		c.handleAnswer(clientID, payload.SDP)

	case "ice-candidate":
		c.handleRemoteCandidate(clientID, payload.Candidate)
	}
}

// handleRequestOffer constructs a new WebRTC session, attaches tracks, creates an offer,
// and transmits the offer back to the requesting client via signaling.
// Classification: RECONSTRUCTED_FROM_BINARY (main.(*IDhLgq).f1PF7qVxR).
func (c *Coordinator) handleRequestOffer(clientID uint32) {
	c.mu.Lock()
	if c.closed {
		c.mu.Unlock()
		return
	}

	// If an existing session exists for this client, cleanly close it first
	if existing, ok := c.sessions[clientID]; ok && existing != nil {
		_ = existing.Close()
		delete(c.sessions, clientID)
	}

	iceServers := c.ICEServers
	sigClient := c.signalingClient
	sink := c.controlSink
	provider := c.clipboardProvider
	sinkFactory := c.fileSinkFactory
	postAction := c.postUploadAction
	cameraSupport := c.cameraSupport
	cameraCfg := c.cameraConfig
	cameraDialer := c.cameraDialer
	c.mu.Unlock()

	opts := agentwebrtc.PeerSessionOptions{
		ClientID:      clientID,
		DeviceID:      c.DeviceID,
		ICEServers:    iceServers,
		CameraSupport: cameraSupport,
		CameraConfig:  cameraCfg,
		CameraDialer:  cameraDialer,
	}
	session, err := agentwebrtc.NewPeerSessionWithOptions(opts)
	if err != nil {
		return
	}

	if sink != nil {
		session.SetControlSink(sink)
	}
	if provider != nil {
		session.SetClipboardProvider(provider)
	}
	if sinkFactory != nil {
		sessionSink := sinkFactory(clientID)
		session.SetFileHandler(agentwebrtc.NewFileChannelHandler(sessionSink, postAction))
	}

	// Attach local ICE candidate listener to dispatch trickle ICE to signaling
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		if sigClient != nil {
			candPayload := map[string]interface{}{
				"type": "ice-candidate",
				"candidate": map[string]interface{}{
					"candidate":     cand.Candidate,
					"sdpMid":        cand.SDPMid,
					"sdpMLineIndex": cand.SDPMLineIndex,
				},
			}
			_ = sigClient.SendForward(clientID, candPayload)
		}
	})

	// Create offer and local description
	offerPayload, err := session.CreateOffer()
	if err != nil {
		_ = session.Close()
		return
	}

	c.mu.Lock()
	c.sessions[clientID] = session
	c.mu.Unlock()

	// Dispatch offer to client over signaling
	if sigClient != nil {
		_ = sigClient.SendForward(clientID, offerPayload)
	}
}

// handleAnswer delivers the remote SDP answer to the active PeerConnection session.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (c *Coordinator) handleAnswer(clientID uint32, sdp string) {
	c.mu.RLock()
	session, ok := c.sessions[clientID]
	c.mu.RUnlock()

	if ok && session != nil {
		_ = session.HandleRemoteAnswer(sdp)
	}
}

// handleRemoteCandidate applies a remote trickle ICE candidate to the active session.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (c *Coordinator) handleRemoteCandidate(clientID uint32, rawCandidate interface{}) {
	c.mu.RLock()
	session, ok := c.sessions[clientID]
	c.mu.RUnlock()

	if !ok || session == nil {
		return
	}

	data, err := json.Marshal(rawCandidate)
	if err != nil {
		return
	}

	var candPayload agentwebrtc.CandidatePayload
	if err := json.Unmarshal(data, &candPayload); err != nil {
		return
	}

	_ = session.AddRemoteCandidate(candPayload.ToPionCandidate())
}

// HandleClientDisconnected executes cleanup of the session bound to clientID.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (c *Coordinator) HandleClientDisconnected(clientID uint32) {
	c.mu.Lock()
	session, ok := c.sessions[clientID]
	if ok && session != nil {
		_ = session.Close()
		delete(c.sessions, clientID)
	}
	c.mu.Unlock()
}

// GetSession retrieves the active PeerSession for a given clientID.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) GetSession(clientID uint32) (*agentwebrtc.PeerSession, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	session, ok := c.sessions[clientID]
	return session, ok
}

// ActiveSessionCount returns the number of concurrent active WebRTC sessions.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) ActiveSessionCount() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.sessions)
}

// Close gracefully terminates all active WebRTC sessions and releases coordinator resources.
// Classification: IMPLEMENTATION_CHOICE.
func (c *Coordinator) Close() error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.closed {
		return nil
	}
	c.closed = true

	for _, session := range c.sessions {
		if session != nil {
			_ = session.Close()
		}
	}
	c.sessions = make(map[uint32]*agentwebrtc.PeerSession)

	if c.signalingClient != nil {
		_ = c.signalingClient.Close()
	}

	return nil
}
