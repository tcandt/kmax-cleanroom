// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIORAL_MESSAGE_ENVELOPES
// Evidence: TRANSPORT_MESSAGE_TYPE_EVIDENCE.json, TRANSPORT_MESSAGE_MATRIX.json,
//   TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Binary Symbols: main.rQffYkwYhw, main.jdUaLc5NMO5, main.id8ybRmw69lm
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

import (
	"encoding/json"

	"cloudphone-signaling/pkg/types"
)

// RegisterMessage represents the device registration frame sent by a physical/emulated device.
// Observed in oracle case TR-E2E-DEV-REGISTER; confirmed in binary symbol main.rQffYkwYhw.
type RegisterMessage struct {
	MessageType string      `json:"message_type"`
	DeviceID    string      `json:"device_id"`
	DeviceInfo  interface{} `json:"device_info,omitempty"`
}

// ConfigMessage represents the server configuration response pushing STUN/TURN ICE servers.
// Observed in oracle case TR-E2E-DEV-REGISTER; confirmed in binary symbol main.rQffYkwYhw.
type ConfigMessage struct {
	MessageType string            `json:"message_type"`
	DeviceID    string            `json:"device_id"`
	ICEServers  []types.ICEServer `json:"ice_servers"`
}

// AgentRegisterMessage represents the initial registration frame sent by the device agent.
// Observed in oracle case TR-E2E-AGENT-REGISTER; confirmed in binary symbol main.jdUaLc5NMO5.
type AgentRegisterMessage struct {
	Type       string `json:"type"`
	DeviceID   string `json:"device_id"`
	ScrcpyAddr string `json:"scrcpy_addr"`
	IsWebRTC   bool   `json:"is_webrtc"`
}

// AgentRegisterOkMessage represents the registration confirmation frame sent to the agent.
// Observed in oracle case TR-E2E-AGENT-REGISTER; confirmed in binary symbol main.jdUaLc5NMO5.
type AgentRegisterOkMessage struct {
	MessageType string `json:"message_type"`
	Status      string `json:"status"`
}

// ConnectMessage represents the client binding frame requesting session association with a device.
// Observed in oracle case TR-E2E-CLI-CONNECT; confirmed in binary symbol main.id8ybRmw69lm.
type ConnectMessage struct {
	Type     string `json:"type"`
	DeviceID string `json:"device_id"`
}

// ForwardEnvelope represents the bidirectional multiplexed signaling envelope.
// Between client, server, and agent. Payload is json.RawMessage to preserve passthrough WebRTC payloads.
// Observed in oracle cases TR-E2E-CLI-FORWARD-REQ-OFFER, TR-E2E-AGENT-FORWARD-OFFER.
type ForwardEnvelope struct {
	MessageType string          `json:"message_type"`
	DeviceID    string          `json:"device_id"`
	ClientID    uint32          `json:"client_id,omitempty"`
	Payload     json.RawMessage `json:"payload"`
}

// DeviceMsgEnvelope represents the server-to-client frame wrapping an agent payload.
// Observed in oracle case TR-E2E-AGENT-FORWARD-OFFER; confirmed in binary symbol main.id8ybRmw69lm.
type DeviceMsgEnvelope struct {
	MessageType string          `json:"message_type"`
	DeviceID    string          `json:"device_id"`
	Payload     json.RawMessage `json:"payload"`
}

// DeviceListUpdateMessage represents the broadcast notification to clients containing device summaries.
// Observed in oracle case TR-E2E-CLI-CONNECT; confirmed in binary symbol main.lv6Xh7.
type DeviceListUpdateMessage struct {
	MessageType string            `json:"message_type"`
	Devices     []types.DeviceDTO `json:"devices"`
}

// HeartbeatMessage represents the keepalive frame sent periodically by the agent.
// Observed in oracle case TR-E2E-AGENT-REGISTER; confirmed in binary symbol main.jdUaLc5NMO5.
type HeartbeatMessage struct {
	MessageType string `json:"message_type"`
	DeviceID    string `json:"device_id"`
}

// SignalingPayload represents the inner WebRTC signaling message structure.
// Validated types: "request-offer", "offer", "answer", "candidate".
type SignalingPayload struct {
	Type      string      `json:"type"`
	SDP       string      `json:"sdp,omitempty"`
	Candidate interface{} `json:"candidate,omitempty"`
}

// GenericInboundEnvelope is used for initial message type discrimination.
type GenericInboundEnvelope struct {
	Type        string `json:"type"`
	MessageType string `json:"message_type"`
	DeviceID    string `json:"device_id"`
	ClientID    uint32 `json:"client_id"`
}
