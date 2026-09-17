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

// Coordinator orchestrates WebRTC sessions and binds them to the signaling transport.
// Classification: RECONSTRUCTED_FROM_BINARY.
type Coordinator struct {
	mu sync.RWMutex

	DeviceID   string
	ICEServers []webrtc.ICEServer

	signalingClient *signaling.Client
	sessions        map[uint32]*agentwebrtc.PeerSession

	closed bool
}

// NewCoordinator initializes the agent coordinator.
// Classification: GENERATED_ADAPTER.
func NewCoordinator(deviceID string, iceServers []webrtc.ICEServer) *Coordinator {
	return &Coordinator{
		DeviceID:   deviceID,
		ICEServers: iceServers,
		sessions:   make(map[uint32]*agentwebrtc.PeerSession),
	}
}

// SetSignalingClient binds the active signaling WebSocket client.
// Classification: GENERATED_ADAPTER.
func (c *Coordinator) SetSignalingClient(client *signaling.Client) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.signalingClient = client
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
	c.mu.Unlock()

	session, err := agentwebrtc.NewPeerSession(clientID, c.DeviceID, iceServers)
	if err != nil {
		return
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
