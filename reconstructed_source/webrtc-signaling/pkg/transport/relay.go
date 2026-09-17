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

	return agentConn.WriteJSON(envelope)
}

// RelayAgentToClient forwards a WebRTC signaling payload (offer, candidate)
// from an agent to the specific target client identified by clientID.
// The payload is wrapped into a device_msg envelope before delivery to the client.
func (h *Hub) RelayAgentToClient(deviceID string, clientID uint32, payload json.RawMessage) error {
	if clientID == 0 {
		return ErrInvalidEnvelope
	}
	clientConn, ok := h.GetClientConn(clientID)
	if !ok || clientConn == nil {
		return ErrPeerNotFound
	}

	envelope := DeviceMsgEnvelope{
		MessageType: "device_msg",
		DeviceID:    deviceID,
		Payload:     payload,
	}

	return clientConn.WriteJSON(envelope)
}
