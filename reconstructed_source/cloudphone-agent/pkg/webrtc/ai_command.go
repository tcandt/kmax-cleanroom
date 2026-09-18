package webrtc

import (
	"encoding/json"
	"errors"
	"fmt"
)

var (
	// ErrNilEnvelope is returned when validating a nil command envelope.
	// Provenance: IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION
	ErrNilEnvelope = errors.New("ai command envelope is nil")

	// ErrEmptyRequestID is returned when validating an envelope with an empty request_id.
	// Provenance: IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION
	ErrEmptyRequestID = errors.New("ai command request_id is empty")

	// ErrEmptyCommand is returned when validating an envelope with an empty command string.
	// Provenance: IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION
	ErrEmptyCommand = errors.New("ai command string is empty")

	// ErrNilResponse is returned when marshaling a nil response pointer.
	// Provenance: IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION
	ErrNilResponse = errors.New("ai command response is nil")
)

// AICommandEnvelope represents an inbound AI command request decoded from JSON.
// In the original binary, this was an anonymous struct at ARM64 0x60e660 / AMD64 0xab0be0.
// Provenance: RECONSTRUCTED_FROM_BINARY
type AICommandEnvelope struct {
	RequestID string `json:"request_id"`
	Command   string `json:"command"`
}

// AICommandResponse represents an outbound AI command execution response before binary serialization.
// In the original binary, keys were inserted into a response map at ARM64 0x53f868 / AMD64 0x9e35b6.
// Provenance: RECONSTRUCTED_FROM_BINARY
type AICommandResponse struct {
	RequestID string `json:"request_id"`
	ExitCode  int    `json:"exit_code"`
	Stdout    string `json:"stdout"`
	Stderr    string `json:"stderr"`
}

// ParseAICommand decodes an inbound AI command payload from JSON.
// In the original binary, the DataChannel OnMessage callback receives msg.Data ([]byte)
// and unmarshals it into the request struct.
// Provenance: RECONSTRUCTED_FROM_PROTOCOL
func ParseAICommand(data []byte) (*AICommandEnvelope, error) {
	var env AICommandEnvelope
	if err := json.Unmarshal(data, &env); err != nil {
		return nil, fmt.Errorf("error parsing request JSON: %w", err)
	}
	return &env, nil
}

// ValidateAICommand validates that envelope fields are non-empty.
//
// FORENSIC NOTE: Disassembly of the original binary (ARM64 0x53f630-0x53f66c and AMD64 0x9e3328-0x9e336b)
// demonstrates that the original agent performs zero non-empty validation checks on request fields after
// json.Unmarshal succeeds. Rejecting empty values here is strictly an IMPLEMENTATION_CHOICE added for
// clean-room defensive validation and hardening; it is not counted toward original binary parity.
// Provenance: IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION
func ValidateAICommand(cmd *AICommandEnvelope) error {
	if cmd == nil {
		return ErrNilEnvelope
	}
	if cmd.RequestID == "" {
		return ErrEmptyRequestID
	}
	if cmd.Command == "" {
		return ErrEmptyCommand
	}
	return nil
}

// MarshalAICommandResponse serializes an AICommandResponse into JSON bytes.
//
// FORENSIC NOTE: In the original binary (ARM64 0x53f9e8 and AMD64 0x9e374a), the agent transmits
// the serialized response via (*DataChannel).Send ([]byte), NOT (*DataChannel).SendText. Therefore,
// the response framing across the wire is strictly BINARY_JSON_BYTES.
// Provenance: RECONSTRUCTED_FROM_PROTOCOL
func MarshalAICommandResponse(resp *AICommandResponse) ([]byte, error) {
	if resp == nil {
		return nil, ErrNilResponse
	}
	return json.Marshal(resp)
}
