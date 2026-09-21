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
	"encoding/binary"
	"encoding/json"
	"errors"

	"cloudphone-signaling/pkg/types"
)

// RegisterMessage represents the device registration frame sent by a physical/emulated device.
// Observed in oracle case TR-E2E-DEV-REGISTER; confirmed in binary symbol main.rQffYkwYhw.
type RegisterMessage struct {
	MessageType string      `json:"message_type"`
	DeviceID    string      `json:"device_id"`
	DeviceInfo  interface{} `json:"device_info,omitempty"`
}

// DeviceInfoMessage represents the server-to-client frame delivering device metadata (R5.3.3).
// Consumed by upstream useWebRTC.js: case "device_info": handleDeviceInfo(msg.device_info).
type DeviceInfoMessage struct {
	MessageType string      `json:"message_type"`
	DeviceID    string      `json:"device_id"`
	DeviceInfo  interface{} `json:"device_info"`
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

// StartPreviewMessage represents client request to start screen preview streaming.
// Classification: RECONSTRUCTED_FROM_BINARY.
type StartPreviewMessage struct {
	MessageType string `json:"message_type,omitempty"`
	Type        string `json:"type,omitempty"`
	DeviceID    string `json:"device_id"`
	FPS         int    `json:"fps,omitempty"`
	MaxSize     int    `json:"max_size,omitempty"`
	Bitrate     int    `json:"bitrate,omitempty"`
	StayAwake   bool   `json:"stay_awake,omitempty"`
}

// StopPreviewMessage represents client request to terminate preview streaming.
// Classification: RECONSTRUCTED_FROM_BINARY.
type StopPreviewMessage struct {
	MessageType string `json:"message_type,omitempty"`
	Type        string `json:"type,omitempty"`
	DeviceID    string `json:"device_id"`
}

// GroupControlEnvelope represents multi-device or single-device control events (touch, keycode, scroll, text).
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
type GroupControlEnvelope struct {
	MessageType     string                 `json:"message_type"`
	TargetDeviceIDs []string               `json:"target_device_ids"`
	Event           map[string]interface{} `json:"event"`
}

// CommandMessage represents a shell/adb command request dispatched to the agent.
// Classification: RECONSTRUCTED_FROM_BINARY.
type CommandMessage struct {
	MessageType string `json:"message_type"`
	DeviceID    string `json:"device_id"`
	RequestID   string `json:"request_id"`
	Command     string `json:"command"`
}

// CommandResultMessage represents the agent's execution response for a command.
// Classification: RECONSTRUCTED_FROM_BINARY.
type CommandResultMessage struct {
	MessageType string `json:"message_type"`
	ClientID    uint32 `json:"client_id,omitempty"`
	RequestID   string `json:"request_id"`
	Output      string `json:"output"`
	Error       string `json:"error,omitempty"`
}

// InjectDataMessage represents custom channel data injection.
// Classification: RECONSTRUCTED_FROM_BINARY.
type InjectDataMessage struct {
	MessageType     string   `json:"message_type"`
	TargetDeviceIDs []string `json:"target_device_ids,omitempty"`
	Channel         string   `json:"channel"`
	Payload         string   `json:"payload"`
}

// QuitAgentMessage represents a request to gracefully terminate the agent process.
// Classification: RECONSTRUCTED_FROM_BINARY.
type QuitAgentMessage struct {
	MessageType string `json:"message_type"`
	DeviceID    string `json:"device_id"`
}

// SnapshotUpdateMessage represents base64 snapshot pushed from agent.
// Classification: RECONSTRUCTED_FROM_BINARY.
type SnapshotUpdateMessage struct {
	MessageType string `json:"message_type"`
	DeviceID    string `json:"device_id"`
	Data        string `json:"data"`
}

// Preview Frame Binary Layout & Errors
// Layout: [magic: 4B ("PREV")][device_id: 32B (null-padded)][key: 1B][pts: 8B (BE uint64)][len: 4B (BE uint32)][payload: NALU]
var (
	ErrInvalidPreviewFrame   = errors.New("preview frame smaller than 49 bytes")
	ErrInvalidPreviewMagic   = errors.New("invalid preview magic header")
	ErrInvalidPreviewLength  = errors.New("payload length exceeds frame buffer")
	ErrPreviewDeviceMismatch = errors.New("preview device_id does not match bound agent device")
)

// ParsePreviewDeviceID parses and extracts device_id from a PREV binary frame.
func ParsePreviewDeviceID(data []byte) (string, error) {
	if len(data) < 49 {
		return "", ErrInvalidPreviewFrame
	}
	if string(data[:4]) != "PREV" {
		return "", ErrInvalidPreviewMagic
	}
	payloadLen := binary.BigEndian.Uint32(data[45:49])
	if int(payloadLen) > len(data)-49 {
		return "", ErrInvalidPreviewLength
	}
	rawID := data[4:36]
	for i, b := range rawID {
		if b == 0 {
			rawID = rawID[:i]
			break
		}
	}
	return string(rawID), nil
}

