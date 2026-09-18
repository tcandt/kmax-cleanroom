package webrtc

import (
	"encoding/json"
	"testing"
)

func TestParseAICommand_Valid(t *testing.T) {
	raw := []byte(`{"request_id":"req-12345","command":"echo hello"}`)
	env, err := ParseAICommand(raw)
	if err != nil {
		t.Fatalf("unexpected error parsing valid AI command: %v", err)
	}
	if env.RequestID != "req-12345" {
		t.Errorf("expected RequestID 'req-12345', got '%s'", env.RequestID)
	}
	if env.Command != "echo hello" {
		t.Errorf("expected Command 'echo hello', got '%s'", env.Command)
	}
}

func TestParseAICommand_MalformedJSON(t *testing.T) {
	malformed := []byte(`{"request_id":"req-1",`)
	env, err := ParseAICommand(malformed)
	if err == nil {
		t.Fatalf("expected error parsing malformed JSON, got nil (env=%+v)", env)
	}
}

func TestParseAICommand_EmptyJSON(t *testing.T) {
	// Original Go json.Unmarshal into struct leaves fields as empty strings
	raw := []byte(`{}`)
	env, err := ParseAICommand(raw)
	if err != nil {
		t.Fatalf("unexpected error parsing empty JSON: %v", err)
	}
	if env.RequestID != "" || env.Command != "" {
		t.Errorf("expected empty fields, got RequestID='%s', Command='%s'", env.RequestID, env.Command)
	}
}

func TestValidateAICommand_DefensiveChecks(t *testing.T) {
	tests := []struct {
		name    string
		env     *AICommandEnvelope
		wantErr error
	}{
		{
			name:    "nil envelope",
			env:     nil,
			wantErr: ErrNilEnvelope,
		},
		{
			name:    "empty request_id",
			env:     &AICommandEnvelope{RequestID: "", Command: "ls -la"},
			wantErr: ErrEmptyRequestID,
		},
		{
			name:    "empty command",
			env:     &AICommandEnvelope{RequestID: "req-1", Command: ""},
			wantErr: ErrEmptyCommand,
		},
		{
			name:    "valid envelope",
			env:     &AICommandEnvelope{RequestID: "req-1", Command: "pm list packages"},
			wantErr: nil,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			err := ValidateAICommand(tc.env)
			if tc.wantErr == nil {
				if err != nil {
					t.Fatalf("unexpected validation error: %v", err)
				}
			} else {
				if err != tc.wantErr {
					t.Fatalf("expected error %v, got %v", tc.wantErr, err)
				}
			}
		})
	}
}

func TestMarshalAICommandResponse_Valid(t *testing.T) {
	resp := &AICommandResponse{
		RequestID: "req-999",
		ExitCode:  0,
		Stdout:    "output text",
		Stderr:    "",
	}

	bytes, err := MarshalAICommandResponse(resp)
	if err != nil {
		t.Fatalf("unexpected error marshaling response: %v", err)
	}

	var parsed map[string]interface{}
	if err := json.Unmarshal(bytes, &parsed); err != nil {
		t.Fatalf("marshaled bytes are not valid JSON: %v", err)
	}

	if parsed["request_id"] != "req-999" {
		t.Errorf("expected request_id 'req-999', got '%v'", parsed["request_id"])
	}
	if exitCode, ok := parsed["exit_code"].(float64); !ok || int(exitCode) != 0 {
		t.Errorf("expected exit_code 0, got '%v'", parsed["exit_code"])
	}
	if parsed["stdout"] != "output text" {
		t.Errorf("expected stdout 'output text', got '%v'", parsed["stdout"])
	}
	if parsed["stderr"] != "" {
		t.Errorf("expected stderr '', got '%v'", parsed["stderr"])
	}
}

func TestMarshalAICommandResponse_Nil(t *testing.T) {
	_, err := MarshalAICommandResponse(nil)
	if err != ErrNilResponse {
		t.Fatalf("expected ErrNilResponse, got %v", err)
	}
}

func TestAICommand_CorrelationEcho(t *testing.T) {
	// Verifies that a synthetic response correctly echoes the request ID
	reqPayload := []byte(`{"request_id":"corr-session-777","command":"id"}`)
	req, err := ParseAICommand(reqPayload)
	if err != nil {
		t.Fatalf("parse failed: %v", err)
	}
	if err := ValidateAICommand(req); err != nil {
		t.Fatalf("validation failed: %v", err)
	}

	syntheticResp := &AICommandResponse{
		RequestID: req.RequestID, // Echo
		ExitCode:  0,
		Stdout:    "uid=2000(shell) gid=2000(shell)",
		Stderr:    "",
	}

	respBytes, err := MarshalAICommandResponse(syntheticResp)
	if err != nil {
		t.Fatalf("marshal failed: %v", err)
	}

	var roundtrip AICommandResponse
	if err := json.Unmarshal(respBytes, &roundtrip); err != nil {
		t.Fatalf("unmarshal roundtrip failed: %v", err)
	}

	if roundtrip.RequestID != req.RequestID {
		t.Errorf("correlation broken: expected %s, got %s", req.RequestID, roundtrip.RequestID)
	}
}
