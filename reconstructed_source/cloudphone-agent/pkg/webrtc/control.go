// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: WEBRTC_DATACHANNEL_INPUT_CONTROL
// Evidence: DATACHANNEL_LABEL_EVIDENCE.json, DATACHANNEL_FRAMING_MATRIX.json, DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json, CONTROL_INPUT_PROTOCOL_CROSSMAP.json, AGENT_HELPER_IPC_SOCKET_MATRIX.json
// Note: Clean-room behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Big-endian scrcpy binary encoding is proven from disassembly at 0x9cfb54-0x9cfc0e (bswap/rol instructions).

package webrtc

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"sync"
)

// Scrcpy ControlMessage types matching com.android.helper.control.ControlMessage
const (
	ScrcpyTypeInjectKeycode             byte = 0
	ScrcpyTypeInjectText                byte = 1
	ScrcpyTypeInjectTouchEvent          byte = 2
	ScrcpyTypeInjectScrollEvent         byte = 3
	ScrcpyTypeBackOrScreenOn            byte = 4
	ScrcpyTypeGetClipboard              byte = 8
	ScrcpyTypeSetClipboard              byte = 9
	ScrcpyTypeOpenHardKeyboardSettings  byte = 15
)

// Touch action constants
const (
	TouchActionDown int = 0
	TouchActionUp   int = 1
	TouchActionMove int = 2
)

// ControlSink defines the narrow boundary adapter for transmitting serialized
// scrcpy control frames toward the Android helper (e.g. abstract UDS @uds_sys_t_).
type ControlSink interface {
	WriteControlMessage(data []byte) error
}

// MemoryControlSink is an in-memory thread-safe implementation of ControlSink used in tests.
type MemoryControlSink struct {
	mu       sync.Mutex
	messages [][]byte
}

// NewMemoryControlSink creates a fresh in-memory control sink.
func NewMemoryControlSink() *MemoryControlSink {
	return &MemoryControlSink{
		messages: make([][]byte, 0),
	}
}

// WriteControlMessage stores the message copy into memory.
func (s *MemoryControlSink) WriteControlMessage(data []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	cp := make([]byte, len(data))
	copy(cp, data)
	s.messages = append(s.messages, cp)
	return nil
}

// GetMessages returns a snapshot of all written messages.
func (s *MemoryControlSink) GetMessages() [][]byte {
	s.mu.Lock()
	defer s.mu.Unlock()
	out := make([][]byte, len(s.messages))
	copy(out, s.messages)
	return out
}

// Clear clears all recorded messages.
func (s *MemoryControlSink) Clear() {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.messages = s.messages[:0]
}

// RawInputEnvelope is used to inspect the discriminator "type" field.
type RawInputEnvelope struct {
	Type string `json:"type"`
}

// TouchEvent represents touch input sent over input-channel.
type TouchEvent struct {
	Type     string  `json:"type"`
	Action   int     `json:"action"` // 0=DOWN, 1=UP, 2=MOVE
	ID       int64   `json:"id"`
	Seq      int64   `json:"seq,omitempty"`
	ClientTs int64   `json:"client_ts_ms,omitempty"`
	X        int32   `json:"x"`
	Y        int32   `json:"y"`
	Width    uint16  `json:"width,omitempty"`
	Height   uint16  `json:"height,omitempty"`
	W        uint16  `json:"w,omitempty"`
	H        uint16  `json:"h,omitempty"`
	Pressure float64 `json:"pressure,omitempty"`
}

// KeycodeEvent represents key input sent over input-channel.
type KeycodeEvent struct {
	Type    string `json:"type"`
	Action  int    `json:"action"` // 0=DOWN, 1=UP
	Keycode int32  `json:"keycode"`
	Repeat  int32  `json:"repeat,omitempty"`
	Meta    int32  `json:"meta,omitempty"`
}

// TextEvent represents direct text input sent over input-channel.
type TextEvent struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

// ScrollEvent represents scroll input sent over input-channel.
type ScrollEvent struct {
	Type     string  `json:"type"`
	Seq      int64   `json:"seq,omitempty"`
	ClientTs int64   `json:"client_ts_ms,omitempty"`
	X        int32   `json:"x"`
	Y        int32   `json:"y"`
	Width    uint16  `json:"width,omitempty"`
	Height   uint16  `json:"height,omitempty"`
	W        uint16  `json:"w,omitempty"`
	H        uint16  `json:"h,omitempty"`
	ScrollH  float64 `json:"scroll_h"`
	ScrollV  float64 `json:"scroll_v"`
}

// HardKeyboardEvent represents opening hard keyboard settings.
type HardKeyboardEvent struct {
	Type    string `json:"type"`
	Enabled bool   `json:"enabled,omitempty"`
}

// EncodeTouchEvent converts TouchEvent into exact 32-byte big-endian scrcpy frame.
// Disassembly reference: AMD64 0x9cfb54 - 0x9cfc0e (packet size = 32 bytes, mov ecx, 0x20).
func EncodeTouchEvent(ev *TouchEvent) []byte {
	buf := make([]byte, 32)
	buf[0] = ScrcpyTypeInjectTouchEvent
	buf[1] = byte(ev.Action)
	binary.BigEndian.PutUint64(buf[2:10], uint64(ev.ID))
	binary.BigEndian.PutUint32(buf[10:14], uint32(ev.X))
	binary.BigEndian.PutUint32(buf[14:18], uint32(ev.Y))

	w := ev.Width
	if w == 0 {
		w = ev.W
	}
	h := ev.Height
	if h == 0 {
		h = ev.H
	}
	binary.BigEndian.PutUint16(buf[18:20], w)
	binary.BigEndian.PutUint16(buf[20:22], h)

	// Pressure: 0x0000 on UP (action=1), 0xffff on DOWN/MOVE
	if ev.Action == TouchActionUp {
		binary.BigEndian.PutUint16(buf[22:24], 0x0000)
	} else {
		binary.BigEndian.PutUint16(buf[22:24], 0xffff)
	}

	// actionButton and buttons = 0 (big-endian int32)
	binary.BigEndian.PutUint32(buf[24:28], 0)
	binary.BigEndian.PutUint32(buf[28:32], 0)

	return buf
}

// EncodeKeycodeEvent converts KeycodeEvent into exact 14-byte big-endian scrcpy frame.
// Matching ControlMessageReader.parseInjectKeycode: [type:1, action:1, keycode:4, repeat:4, meta:4].
func EncodeKeycodeEvent(ev *KeycodeEvent) []byte {
	buf := make([]byte, 14)
	buf[0] = ScrcpyTypeInjectKeycode
	buf[1] = byte(ev.Action)
	binary.BigEndian.PutUint32(buf[2:6], uint32(ev.Keycode))
	binary.BigEndian.PutUint32(buf[6:10], uint32(ev.Repeat))
	binary.BigEndian.PutUint32(buf[10:14], uint32(ev.Meta))
	return buf
}

// EncodeTextEvent converts TextEvent into scrcpy frame [type:1, length:4 (BE), text:N].
// Matching ControlMessageReader.parseInjectText: [type:1, length:4, bytes:N].
func EncodeTextEvent(ev *TextEvent) []byte {
	textBytes := []byte(ev.Text)
	length := len(textBytes)
	buf := make([]byte, 5+length)
	buf[0] = ScrcpyTypeInjectText
	binary.BigEndian.PutUint32(buf[1:5], uint32(length))
	copy(buf[5:], textBytes)
	return buf
}

// EncodeScrollEvent converts ScrollEvent into exact 21-byte big-endian scrcpy frame.
// Matching ControlMessageReader.parseInjectScrollEvent:
// [type:1, X:4, Y:4, W:2, H:2, hScroll:2, vScroll:2, buttons:4].
func EncodeScrollEvent(ev *ScrollEvent) []byte {
	buf := make([]byte, 21)
	buf[0] = ScrcpyTypeInjectScrollEvent
	binary.BigEndian.PutUint32(buf[1:5], uint32(ev.X))
	binary.BigEndian.PutUint32(buf[5:9], uint32(ev.Y))

	w := ev.Width
	if w == 0 {
		w = ev.W
	}
	h := ev.Height
	if h == 0 {
		h = ev.H
	}
	binary.BigEndian.PutUint16(buf[9:11], w)
	binary.BigEndian.PutUint16(buf[11:13], h)

	// Fixed-point scaling: helper reader multiplies i16FixedPointToFloat by 16.0f
	// i16 fixed point: s / 32768.0f. So s = float * 2048.0f.
	hFixed := int16(ev.ScrollH * 2048.0)
	vFixed := int16(ev.ScrollV * 2048.0)
	binary.BigEndian.PutUint16(buf[13:15], uint16(hFixed))
	binary.BigEndian.PutUint16(buf[15:17], uint16(vFixed))

	// buttons = 0
	binary.BigEndian.PutUint32(buf[17:21], 0)
	return buf
}

// EncodeHardKeyboardEvent converts HardKeyboardEvent into 1-byte scrcpy frame (type=15).
func EncodeHardKeyboardEvent() []byte {
	return []byte{ScrcpyTypeOpenHardKeyboardSettings}
}

// HandleInputMessage decodes raw JSON payload from input-channel and emits
// the corresponding binary scrcpy control message to the ControlSink.
// It is defensive and will never panic on malformed input.
func HandleInputMessage(raw []byte, sink ControlSink) error {
	if len(raw) == 0 {
		return fmt.Errorf("empty input message")
	}
	if sink == nil {
		return fmt.Errorf("nil control sink")
	}

	var env RawInputEnvelope
	if err := json.Unmarshal(raw, &env); err != nil {
		return fmt.Errorf("unmarshal envelope error: %w", err)
	}

	var frame []byte
	switch env.Type {
	case "inject_touch", "touch":
		var ev TouchEvent
		if err := json.Unmarshal(raw, &ev); err != nil {
			return fmt.Errorf("unmarshal touch error: %w", err)
		}
		frame = EncodeTouchEvent(&ev)

	case "inject_keycode":
		var ev KeycodeEvent
		if err := json.Unmarshal(raw, &ev); err != nil {
			return fmt.Errorf("unmarshal keycode error: %w", err)
		}
		frame = EncodeKeycodeEvent(&ev)

	case "inject_text":
		var ev TextEvent
		if err := json.Unmarshal(raw, &ev); err != nil {
			return fmt.Errorf("unmarshal text error: %w", err)
		}
		frame = EncodeTextEvent(&ev)

	case "inject_scroll":
		var ev ScrollEvent
		if err := json.Unmarshal(raw, &ev); err != nil {
			return fmt.Errorf("unmarshal scroll error: %w", err)
		}
		frame = EncodeScrollEvent(&ev)

	case "hard_keyboard":
		frame = EncodeHardKeyboardEvent()

	default:
		// Unsupported / unknown event type is safely dropped without panic
		return nil
	}

	if len(frame) > 0 {
		return sink.WriteControlMessage(frame)
	}
	return nil
}
