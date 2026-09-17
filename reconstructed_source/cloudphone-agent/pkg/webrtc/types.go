// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: WEBRTC_CORE_TYPES_AND_SIGNALING_ENVELOPES
// Evidence: WEBRTC_TOPOLOGY_CROSSMAP.json, WEBRTC_PEERCONNECTION_STATE_MACHINE.json,
//   WEBRTC_SIGNALING_CONTRACT.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"encoding/json"
	"github.com/pion/webrtc/v3"
)

// SessionState models the observable internal lifecycle states of a WebRTC session.
// Classification: GENERATED_ADAPTER / IMPLEMENTATION_CHOICE.
// The states map to observable protocol events rather than claimed literal original enums.
type SessionState int

const (
	SessionStateNew SessionState = iota
	SessionStateConnecting
	SessionStateHaveLocalOffer
	SessionStateHaveRemoteAnswer
	SessionStateConnected
	SessionStateFailed
	SessionStateClosed
)

func (s SessionState) String() string {
	switch s {
	case SessionStateNew:
		return "New"
	case SessionStateConnecting:
		return "Connecting"
	case SessionStateHaveLocalOffer:
		return "HaveLocalOffer"
	case SessionStateHaveRemoteAnswer:
		return "HaveRemoteAnswer"
	case SessionStateConnected:
		return "Connected"
	case SessionStateFailed:
		return "Failed"
	case SessionStateClosed:
		return "Closed"
	default:
		return "Unknown"
	}
}

// SignalingPayload represents the inner WebRTC message transmitted within a forward envelope.
// Classification: RECONSTRUCTED_FROM_PROTOCOL (Phase 2C.4B/2C.5A).
type SignalingPayload struct {
	Type          string      `json:"type"`
	SDP           string      `json:"sdp,omitempty"`
	Candidate     interface{} `json:"candidate,omitempty"`
	CameraSupport *bool       `json:"camera_support,omitempty"`
	IPPreference  string      `json:"ip_preference,omitempty"`
}

// ForwardEnvelope matches the closed Phase 2C.4 transport relay envelope.
// Classification: RECONSTRUCTED_FROM_BINARY (main.jdUaLc5NMO5, main.id8ybRmw69lm).
type ForwardEnvelope struct {
	MessageType string          `json:"message_type"`
	DeviceID    string          `json:"device_id"`
	ClientID    uint32          `json:"client_id,omitempty"`
	Payload     json.RawMessage `json:"payload"`
}

// ClientDisconnectedMessage matches the closed Phase 2C.4 client teardown notification.
// Classification: RECONSTRUCTED_FROM_BINARY (main.lv6Xh7 / TR-DIFF-CLI-DISCONNECT-NOTIF).
type ClientDisconnectedMessage struct {
	MessageType string `json:"message_type"`
	DeviceID    string `json:"device_id"`
	ClientID    uint32 `json:"client_id"`
}

// CandidatePayload represents an individual ICE candidate payload exchanged over signaling.
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
type CandidatePayload struct {
	Candidate     string  `json:"candidate"`
	SDPMid        *string `json:"sdpMid,omitempty"`
	SDPMLineIndex *uint16 `json:"sdpMLineIndex,omitempty"`
}

// ToPionCandidate converts the CandidatePayload to a Pion webrtc.ICECandidateInit.
// Classification: GENERATED_ADAPTER.
func (c *CandidatePayload) ToPionCandidate() webrtc.ICECandidateInit {
	init := webrtc.ICECandidateInit{
		Candidate: c.Candidate,
	}
	if c.SDPMid != nil {
		init.SDPMid = c.SDPMid
	}
	if c.SDPMLineIndex != nil {
		init.SDPMLineIndex = c.SDPMLineIndex
	}
	return init
}
