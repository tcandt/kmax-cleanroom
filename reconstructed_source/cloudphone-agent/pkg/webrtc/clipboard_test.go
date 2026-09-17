// CLEANROOM-PROVENANCE:
// Classification: IMPLEMENTATION_CHOICE / TEST_SUITE
// Mapping Scope: WEBRTC_CLIPBOARD_TESTS
// Evidence: DATACHANNEL_LABEL_EVIDENCE.json, DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json,
//   evidence/reference/raw/web-app/src/composables/useWebRTC.js:761-786, 1195-1215

package webrtc

import (
	"bytes"
	"encoding/json"
	"fmt"
	"sync"
	"testing"
)

// TestSetClipboard validates that set_clipboard updates the provider with text, paste, and origin.
func TestSetClipboard(t *testing.T) {
	provider := NewMemoryClipboardProvider()

	raw := `{"type":"set_clipboard","text":"Copied Text from Client","paste":true,"source":"local","origin_client_id":"client-123"}`
	err := HandleClipboardMessage([]byte(raw), provider, nil)
	if err != nil {
		t.Fatalf("HandleClipboardMessage failed: %v", err)
	}

	text, paste, origin, sets, _ := provider.Stats()
	if text != "Copied Text from Client" {
		t.Fatalf("expected text 'Copied Text from Client', got %q", text)
	}
	if !paste {
		t.Fatalf("expected paste=true, got %v", paste)
	}
	if origin != "client-123" {
		t.Fatalf("expected origin 'client-123', got %q", origin)
	}
	if sets != 1 {
		t.Fatalf("expected 1 set call, got %d", sets)
	}
}

// TestGetClipboard validates that get_clipboard queries provider and transmits a formatted response.
func TestGetClipboard(t *testing.T) {
	provider := NewMemoryClipboardProvider()
	_ = provider.Set("Existing Device Text", false, "")

	var responseBytes []byte
	sender := func(out []byte) error {
		responseBytes = out
		return nil
	}

	raw := `{"type":"get_clipboard"}`
	err := HandleClipboardMessage([]byte(raw), provider, sender)
	if err != nil {
		t.Fatalf("HandleClipboardMessage failed: %v", err)
	}

	if len(responseBytes) == 0 {
		t.Fatalf("expected response frame to be sent")
	}

	var resp ClipboardResponseMessage
	if err := json.Unmarshal(responseBytes, &resp); err != nil {
		t.Fatalf("failed to unmarshal response frame: %v", err)
	}

	if resp.Type != "clipboard" {
		t.Fatalf("expected type 'clipboard', got %q", resp.Type)
	}
	if resp.Text != "Existing Device Text" {
		t.Fatalf("expected text 'Existing Device Text', got %q", resp.Text)
	}
	if resp.Source != "device" {
		t.Fatalf("expected source 'device', got %q", resp.Source)
	}
	if resp.OriginClientID != nil {
		t.Fatalf("expected nil OriginClientID, got %v", *resp.OriginClientID)
	}
}

// TestEmptyClipboard validates behavior when the clipboard is empty.
func TestEmptyClipboard(t *testing.T) {
	provider := NewMemoryClipboardProvider()

	var responseBytes []byte
	sender := func(out []byte) error {
		responseBytes = out
		return nil
	}

	raw := `{"type":"get_clipboard"}`
	err := HandleClipboardMessage([]byte(raw), provider, sender)
	if err != nil {
		t.Fatalf("failed: %v", err)
	}

	var resp ClipboardResponseMessage
	if err := json.Unmarshal(responseBytes, &resp); err != nil {
		t.Fatalf("failed to parse: %v", err)
	}
	if resp.Text != "" {
		t.Fatalf("expected empty clipboard text, got %q", resp.Text)
	}
}

// TestPeerClipboardNotification validates that peer clipboard updates local provider.
func TestPeerClipboardNotification(t *testing.T) {
	provider := NewMemoryClipboardProvider()

	origin := "client-456"
	raw := `{"type":"clipboard","text":"Remote text","source":"device","origin_client_id":"client-456"}`
	err := HandleClipboardMessage([]byte(raw), provider, nil)
	if err != nil {
		t.Fatalf("failed: %v", err)
	}

	text, _, lastOrigin, sets, _ := provider.Stats()
	if text != "Remote text" {
		t.Fatalf("expected 'Remote text', got %q", text)
	}
	if lastOrigin != origin {
		t.Fatalf("expected origin %q, got %q", origin, lastOrigin)
	}
	if sets != 1 {
		t.Fatalf("expected 1 set call, got %d", sets)
	}
}

// TestClipboardParserRobustnessAndFuzz verifies resilience against malformed inputs.
func TestClipboardParserRobustnessAndFuzz(t *testing.T) {
	provider := NewMemoryClipboardProvider()

	fuzzCases := []struct {
		name string
		raw  []byte
	}{
		{"nil_bytes", nil},
		{"empty_bytes", []byte{}},
		{"whitespace_only", []byte("   \n\t  ")},
		{"malformed_json_brace", []byte("{")},
		{"malformed_json_truncated", []byte(`{"type":"set_clipboard","text":`)},
		{"numeric_json", []byte("12345")},
		{"array_json", []byte("[1, 2, 3]")},
		{"missing_type", []byte(`{"text":"hello"}`)},
		{"unknown_type", []byte(`{"type":"unsupported_clipboard_op"}`)},
		{"wrong_field_types", []byte(`{"type":"set_clipboard","text":12345,"paste":"NOT_A_BOOL"}`)},
		{"oversized_payload", bytes.Repeat([]byte("A"), MaxClipboardTextLength+5000)},
		{"binary_garbage", []byte{0x00, 0xff, 0xfe, 0x80, 0x12, 0x34}},
	}

	for _, tc := range fuzzCases {
		t.Run(tc.name, func(t *testing.T) {
			defer func() {
				if r := recover(); r != nil {
					t.Fatalf("PANIC detected during parsing %s: %v", tc.name, r)
				}
			}()
			_ = HandleClipboardMessage(tc.raw, provider, func(b []byte) error { return nil })
		})
	}
}

// TestClipboardConcurrency tests thread safety under concurrent operations.
func TestClipboardConcurrency(t *testing.T) {
	provider := NewMemoryClipboardProvider()
	var wg sync.WaitGroup
	numWorkers := 10
	opsPerWorker := 30

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for j := 0; j < opsPerWorker; j++ {
				if j%2 == 0 {
					payload := fmt.Sprintf(`{"type":"set_clipboard","text":"text-%d-%d","origin_client_id":"c-%d"}`,
						workerID, j, workerID)
					_ = HandleClipboardMessage([]byte(payload), provider, nil)
				} else {
					payload := `{"type":"get_clipboard"}`
					_ = HandleClipboardMessage([]byte(payload), provider, func(b []byte) error { return nil })
				}
			}
		}(i)
	}

	wg.Wait()
	_, _, _, sets, gets := provider.Stats()
	if sets == 0 || gets == 0 {
		t.Fatalf("expected sets > 0 and gets > 0, got sets=%d gets=%d", sets, gets)
	}
}
