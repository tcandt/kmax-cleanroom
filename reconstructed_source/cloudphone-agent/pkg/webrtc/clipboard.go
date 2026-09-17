// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: WEBRTC_DATACHANNEL_CLIPBOARD
// Evidence: DATACHANNEL_LABEL_EVIDENCE.json, DATACHANNEL_FRAMING_MATRIX.json, DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json, reports/30_PHASE2C5A_WEBRTC_DATACHANNEL_MEDIA_FORENSICS.md
// Note: Clean-room behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// origin_client_id is verified from binary rodata. Handlers at 0x9e3860 / 0x9e38ce.

package webrtc

import (
	"encoding/json"
	"fmt"
	"sync"
)

// Maximum clipboard text length matching ControlMessageReader.CLIPBOARD_TEXT_MAX_LENGTH (262130)
const MaxClipboardTextLength = 262130

// ClipboardProvider defines the boundary abstraction for interaction with the device clipboard.
type ClipboardProvider interface {
	Get() (string, error)
	Set(text string, paste bool, originClientID string) error
}

// MemoryClipboardProvider is a thread-safe in-memory provider used in testing and local execution.
type MemoryClipboardProvider struct {
	mu         sync.RWMutex
	text       string
	lastPaste  bool
	lastOrigin string
	setCount   int
	getCount   int
}

// NewMemoryClipboardProvider creates a fresh in-memory clipboard provider.
func NewMemoryClipboardProvider() *MemoryClipboardProvider {
	return &MemoryClipboardProvider{}
}

// Get returns the current clipboard text.
func (p *MemoryClipboardProvider) Get() (string, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.getCount++
	return p.text, nil
}

// Set updates the clipboard text.
func (p *MemoryClipboardProvider) Set(text string, paste bool, originClientID string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.text = text
	p.lastPaste = paste
	p.lastOrigin = originClientID
	p.setCount++
	return nil
}

// Stats returns usage counters and latest state.
func (p *MemoryClipboardProvider) Stats() (text string, paste bool, origin string, sets int, gets int) {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return p.text, p.lastPaste, p.lastOrigin, p.setCount, p.getCount
}

// RawClipboardEnvelope is used to inspect the message discriminator.
type RawClipboardEnvelope struct {
	Type string `json:"type"`
}

// SetClipboardMessage represents an ingress request to set device clipboard.
type SetClipboardMessage struct {
	Type              string `json:"type"`
	Text              string `json:"text"`
	Paste             bool   `json:"paste,omitempty"`
	Source            string `json:"source,omitempty"`
	SuppressBroadcast bool   `json:"suppress_broadcast,omitempty"`
	OriginClientID    string `json:"origin_client_id,omitempty"`
}

// GetClipboardMessage represents an ingress request to read device clipboard.
type GetClipboardMessage struct {
	Type string `json:"type"`
}

// ClipboardResponseMessage represents the outbound frame sent over clipboard-channel.
type ClipboardResponseMessage struct {
	Type           string  `json:"type"`
	Text           string  `json:"text"`
	Source         string  `json:"source"`
	OriginClientID *string `json:"origin_client_id"`
}

// HandleClipboardMessage parses an incoming message on clipboard-channel and dispatches it.
// If the message is "get_clipboard", it queries the provider and transmits a response frame via sender.
// It is defensive and will never panic on malformed input.
func HandleClipboardMessage(raw []byte, provider ClipboardProvider, sender func([]byte) error) error {
	if len(raw) == 0 {
		return fmt.Errorf("empty clipboard message")
	}
	if len(raw) > MaxClipboardTextLength+1024 {
		return fmt.Errorf("clipboard payload exceeds maximum bound")
	}
	if provider == nil {
		return fmt.Errorf("nil clipboard provider")
	}

	var env RawClipboardEnvelope
	if err := json.Unmarshal(raw, &env); err != nil {
		return fmt.Errorf("unmarshal envelope error: %w", err)
	}

	switch env.Type {
	case "set_clipboard":
		var msg SetClipboardMessage
		if err := json.Unmarshal(raw, &msg); err != nil {
			return fmt.Errorf("unmarshal set_clipboard error: %w", err)
		}
		return provider.Set(msg.Text, msg.Paste, msg.OriginClientID)

	case "get_clipboard":
		text, err := provider.Get()
		if err != nil {
			text = ""
		}
		resp := ClipboardResponseMessage{
			Type:           "clipboard",
			Text:           text,
			Source:         "device",
			OriginClientID: nil,
		}
		data, err := json.Marshal(resp)
		if err != nil {
			return fmt.Errorf("marshal clipboard response error: %w", err)
		}
		if sender != nil {
			return sender(data)
		}
		return nil

	case "clipboard":
		// Peer notification of clipboard content (can update local provider)
		var msg ClipboardResponseMessage
		if err := json.Unmarshal(raw, &msg); err != nil {
			return fmt.Errorf("unmarshal clipboard error: %w", err)
		}
		var origin string
		if msg.OriginClientID != nil {
			origin = *msg.OriginClientID
		}
		return provider.Set(msg.Text, false, origin)

	default:
		// Unknown discriminator safely dropped without panic
		return nil
	}
}
