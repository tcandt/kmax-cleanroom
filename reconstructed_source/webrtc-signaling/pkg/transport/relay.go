// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_SIGNALING_RELAY_ROUTING
// Evidence: WEBRTC_SIGNALING_CONTRACT.json, DEVICE_AGENT_CLIENT_ASSOCIATION_CONTRACT.json,
//   TRANSPORT_MESSAGE_MATRIX.json, TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Binary Symbols: main.id8ybRmw69lm, main.jdUaLc5NMO5
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

import (
	"encoding/json"
	"errors"
	"log"
)

var (
	ErrPeerNotFound      = errors.New("target signaling peer not connected")
	ErrInvalidEnvelope   = errors.New("invalid signaling envelope")
	ErrDeviceNotBound    = errors.New("connection not bound to a device")
)

// RelayClientToAgent forwards a WebRTC signaling payload (request-offer, answer, candidate)
// from a connected browser client to the registered agent for the given device.
func (h *Hub) RelayClientToAgent(deviceID string, clientID uint32, payload json.RawMessage) error {
	if deviceID == "" {
		return ErrDeviceNotBound
	}
	agentConn, ok := h.GetAgentConn(deviceID)
	if !ok || agentConn == nil {
		return ErrPeerNotFound
	}

	envelope := ForwardEnvelope{
		MessageType: "forward",
		DeviceID:    deviceID,
		ClientID:    clientID,
		Payload:     payload,
	}

	// Parse payload type to detect initial session request vs in-session trickle ICE / answer
	var sigHeader struct {
		Type       string `json:"type"`
		Generation uint64 `json:"generation"`
		AttemptID  uint32 `json:"attempt_id"`
	}
	_ = json.Unmarshal(payload, &sigHeader)

	if sigHeader.Type == "request-offer" {
		// Increment or align device generation for this new WebRTC attempt
		gen := sigHeader.Generation
		if gen == 0 {
			gen = h.NextDeviceGeneration(deviceID)
		} else {
			h.SetDeviceGeneration(deviceID, gen)
		}

		if cc, exists := h.GetClientConn(clientID); exists && cc != nil {
			cc.Generation = gen
			cc.IsWebRTC = true
		}

		if tracker := h.GetCoreTracker(deviceID); tracker != nil {
			// Bidirectional handoff check: If device currently has active WS preview, begin handoff WS -> WebRTC
			if tracker.WSCount() > 0 {
				tracker.BeginHandoff("websocket", "webrtc", gen, sigHeader.AttemptID, 0, clientID)
			}
			tracker.OnAddWebRTCClient(clientID, gen)
		}
	}

	log.Printf("[Signaling-Relay] Forwarding client %d -> agent %s: %s", clientID, deviceID, string(payload))
	return agentConn.WriteJSON(envelope)
}

// RelayAgentToClient forwards a WebRTC signaling payload (offer, candidate)
// from an agent to the specific target client identified by clientID.
// The payload is wrapped into a device_msg envelope before delivery to the client.
func (h *Hub) RelayAgentToClient(deviceID string, clientID uint32, payload json.RawMessage) error {
	if clientID == 0 {
		log.Printf("[Signaling-Relay] RelayAgentToClient error: clientID is 0 for device %s", deviceID)
		return ErrInvalidEnvelope
	}
	clientConn, ok := h.GetClientConn(clientID)
	if !ok || clientConn == nil {
		log.Printf("[Signaling-Relay] RelayAgentToClient error: target client %d not found for device %s", clientID, deviceID)
		return ErrPeerNotFound
	}

	envelope := DeviceMsgEnvelope{
		MessageType: "device_msg",
		DeviceID:    deviceID,
		Payload:     payload,
	}

	log.Printf("[Signaling-Relay] Forwarding agent %s -> client %d: %s", deviceID, clientID, string(payload))
	return clientConn.WriteJSON(envelope)
}
