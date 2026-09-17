// CLEANROOM-PROVENANCE:
// Classification: IMPLEMENTATION_CHOICE / TEST_SUITE
// Mapping Scope: WEBRTC_INPUT_CONTROL_TESTS
// Evidence: CONTROL_INPUT_PROTOCOL_CROSSMAP.json, DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json,
//   raw_extraction/android/jadx/sources/com/android/helper/control/ControlMessageReader.java

package webrtc

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"sync"
	"testing"
)

// TestGoldenTouchEvent validates exact byte-level binary framing against independent
// forensic specification (AMD64 0x9cfb54-0x9cfc0e and ControlMessageReader.parseInjectTouchEvent).
// Expected bytes are constructed independently without invoking EncodeTouchEvent.
func TestGoldenTouchEvent(t *testing.T) {
	// Case 1: ACTION_DOWN (action=0, pointer=123456789, x=540, y=960, w=1080, h=1920)
	// Pressure must be 0xffff for DOWN.
	evDown := &TouchEvent{
		Type:   "inject_touch",
		Action: 0,
		ID:     123456789,
		X:      540,
		Y:      960,
		Width:  1080,
		Height: 1920,
	}
	actualDown := EncodeTouchEvent(evDown)

	expectedDown := make([]byte, 32)
	expectedDown[0] = 2                                              // TYPE_INJECT_TOUCH_EVENT
	expectedDown[1] = 0                                              // Action DOWN
	binary.BigEndian.PutUint64(expectedDown[2:10], uint64(123456789)) // Pointer ID
	binary.BigEndian.PutUint32(expectedDown[10:14], 540)             // X
	binary.BigEndian.PutUint32(expectedDown[14:18], 960)             // Y
	binary.BigEndian.PutUint16(expectedDown[18:20], 1080)            // Width
	binary.BigEndian.PutUint16(expectedDown[20:22], 1920)            // Height
	binary.BigEndian.PutUint16(expectedDown[22:24], 0xffff)          // Pressure (DOWN = 0xffff)
	binary.BigEndian.PutUint32(expectedDown[24:28], 0)               // actionButton
	binary.BigEndian.PutUint32(expectedDown[28:32], 0)               // buttons

	if len(actualDown) != 32 {
		t.Fatalf("expected 32 bytes for touch packet, got %d", len(actualDown))
	}
	if !bytes.Equal(actualDown, expectedDown) {
		t.Fatalf("touch DOWN golden frame mismatch.\nExpected: %x\nActual:   %x", expectedDown, actualDown)
	}

	// Case 2: ACTION_UP (action=1). Pressure must be 0x0000.
	evUp := &TouchEvent{
		Type:   "inject_touch",
		Action: 1,
		ID:     99,
		X:      100,
		Y:      200,
		W:      720,
		H:      1280,
	}
	actualUp := EncodeTouchEvent(evUp)

	expectedUp := make([]byte, 32)
	expectedUp[0] = 2
	expectedUp[1] = 1 // Action UP
	binary.BigEndian.PutUint64(expectedUp[2:10], 99)
	binary.BigEndian.PutUint32(expectedUp[10:14], 100)
	binary.BigEndian.PutUint32(expectedUp[14:18], 200)
	binary.BigEndian.PutUint16(expectedUp[18:20], 720)
	binary.BigEndian.PutUint16(expectedUp[20:22], 1280)
	binary.BigEndian.PutUint16(expectedUp[22:24], 0x0000) // Pressure UP = 0
	binary.BigEndian.PutUint32(expectedUp[24:28], 0)
	binary.BigEndian.PutUint32(expectedUp[28:32], 0)

	if !bytes.Equal(actualUp, expectedUp) {
		t.Fatalf("touch UP golden frame mismatch.\nExpected: %x\nActual:   %x", expectedUp, actualUp)
	}
}

// TestGoldenKeycodeEvent validates exact byte-level framing for inject_keycode.
func TestGoldenKeycodeEvent(t *testing.T) {
	// keycode 4 = KEYCODE_BACK, action 0 = DOWN, repeat 1, meta 2
	ev := &KeycodeEvent{
		Type:    "inject_keycode",
		Action:  0,
		Keycode: 4,
		Repeat:  1,
		Meta:    2,
	}
	actual := EncodeKeycodeEvent(ev)

	expected := make([]byte, 14)
	expected[0] = 0 // TYPE_INJECT_KEYCODE
	expected[1] = 0 // Action DOWN
	binary.BigEndian.PutUint32(expected[2:6], 4)
	binary.BigEndian.PutUint32(expected[6:10], 1)
	binary.BigEndian.PutUint32(expected[10:14], 2)

	if len(actual) != 14 {
		t.Fatalf("expected 14 bytes for keycode packet, got %d", len(actual))
	}
	if !bytes.Equal(actual, expected) {
		t.Fatalf("keycode golden frame mismatch.\nExpected: %x\nActual:   %x", expected, actual)
	}
}

// TestGoldenTextEvent validates exact byte-level framing for inject_text.
func TestGoldenTextEvent(t *testing.T) {
	text := "Hello, Cleanroom!"
	ev := &TextEvent{
		Type: "inject_text",
		Text: text,
	}
	actual := EncodeTextEvent(ev)

	expected := make([]byte, 5+len(text))
	expected[0] = 1 // TYPE_INJECT_TEXT
	binary.BigEndian.PutUint32(expected[1:5], uint32(len(text)))
	copy(expected[5:], []byte(text))

	if len(actual) != 5+len(text) {
		t.Fatalf("expected %d bytes, got %d", 5+len(text), len(actual))
	}
	if !bytes.Equal(actual, expected) {
		t.Fatalf("text golden frame mismatch.\nExpected: %x\nActual:   %x", expected, actual)
	}
}

// TestGoldenScrollEvent validates exact byte-level framing for inject_scroll.
func TestGoldenScrollEvent(t *testing.T) {
	ev := &ScrollEvent{
		Type:    "inject_scroll",
		X:       300,
		Y:       400,
		Width:   1080,
		Height:  1920,
		ScrollH: 0.0,
		ScrollV: -1.0,
	}
	actual := EncodeScrollEvent(ev)

	expected := make([]byte, 21)
	expected[0] = 3 // TYPE_INJECT_SCROLL_EVENT
	binary.BigEndian.PutUint32(expected[1:5], 300)
	binary.BigEndian.PutUint32(expected[5:9], 400)
	binary.BigEndian.PutUint16(expected[9:11], 1080)
	binary.BigEndian.PutUint16(expected[11:13], 1920)
	hVal := int16(0)
	vVal := int16(-2048)
	binary.BigEndian.PutUint16(expected[13:15], uint16(hVal))
	binary.BigEndian.PutUint16(expected[15:17], uint16(vVal))
	binary.BigEndian.PutUint32(expected[17:21], 0)

	if len(actual) != 21 {
		t.Fatalf("expected 21 bytes for scroll packet, got %d", len(actual))
	}
	if !bytes.Equal(actual, expected) {
		t.Fatalf("scroll golden frame mismatch.\nExpected: %x\nActual:   %x", expected, actual)
	}
}

// TestGoldenHardKeyboardEvent validates 1-byte framing for hard_keyboard.
func TestGoldenHardKeyboardEvent(t *testing.T) {
	actual := EncodeHardKeyboardEvent()
	expected := []byte{15} // TYPE_OPEN_HARD_KEYBOARD_SETTINGS = 15 (0x0f)
	if !bytes.Equal(actual, expected) {
		t.Fatalf("hard keyboard mismatch: expected %x, got %x", expected, actual)
	}
}

// TestHandleInputMessageEndToEnd tests parsing of all 5 event types through HandleInputMessage.
func TestHandleInputMessageEndToEnd(t *testing.T) {
	sink := NewMemoryControlSink()

	cases := []struct {
		name         string
		jsonPayload  string
		expectedType byte
		expectedLen  int
	}{
		{
			name:         "touch_down",
			jsonPayload:  `{"type":"inject_touch","action":0,"id":1,"x":100,"y":200,"w":1080,"h":1920}`,
			expectedType: ScrcpyTypeInjectTouchEvent,
			expectedLen:  32,
		},
		{
			name:         "touch_alias_type",
			jsonPayload:  `{"type":"touch","action":2,"id":1,"x":105,"y":205,"width":1080,"height":1920}`,
			expectedType: ScrcpyTypeInjectTouchEvent,
			expectedLen:  32,
		},
		{
			name:         "keycode",
			jsonPayload:  `{"type":"inject_keycode","action":0,"keycode":3,"repeat":0,"meta":0}`,
			expectedType: ScrcpyTypeInjectKeycode,
			expectedLen:  14,
		},
		{
			name:         "text",
			jsonPayload:  `{"type":"inject_text","text":"antigravity"}`,
			expectedType: ScrcpyTypeInjectText,
			expectedLen:  5 + len("antigravity"),
		},
		{
			name:         "scroll",
			jsonPayload:  `{"type":"inject_scroll","x":500,"y":500,"w":1080,"h":1920,"scroll_h":0,"scroll_v":-2.5}`,
			expectedType: ScrcpyTypeInjectScrollEvent,
			expectedLen:  21,
		},
		{
			name:         "hard_keyboard",
			jsonPayload:  `{"type":"hard_keyboard","enabled":true}`,
			expectedType: ScrcpyTypeOpenHardKeyboardSettings,
			expectedLen:  1,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			sink.Clear()
			err := HandleInputMessage([]byte(tc.jsonPayload), sink)
			if err != nil {
				t.Fatalf("unexpected error for %s: %v", tc.name, err)
			}
			msgs := sink.GetMessages()
			if len(msgs) != 1 {
				t.Fatalf("expected 1 message in sink, got %d", len(msgs))
			}
			if msgs[0][0] != tc.expectedType {
				t.Fatalf("expected type %d, got %d", tc.expectedType, msgs[0][0])
			}
			if len(msgs[0]) != tc.expectedLen {
				t.Fatalf("expected length %d, got %d", tc.expectedLen, len(msgs[0]))
			}
		})
	}
}

// TestInputParserRobustnessAndFuzz verifies that malformed inputs do not panic.
func TestInputParserRobustnessAndFuzz(t *testing.T) {
	sink := NewMemoryControlSink()

	fuzzCases := []struct {
		name string
		raw  []byte
	}{
		{"nil_bytes", nil},
		{"empty_bytes", []byte{}},
		{"whitespace_only", []byte("   \n\t  ")},
		{"malformed_json_brace", []byte("{")},
		{"malformed_json_truncated", []byte(`{"type":"inject_touch","action":`)},
		{"numeric_json", []byte("12345")},
		{"array_json", []byte("[1, 2, 3]")},
		{"missing_type", []byte(`{"action":0,"x":100}`)},
		{"unknown_type", []byte(`{"type":"future_unsupported_gesture","foo":"bar"}`)},
		{"wrong_field_types", []byte(`{"type":"inject_touch","action":"NOT_AN_INT","x":"ABC"}`)},
		{"oversized_payload", bytes.Repeat([]byte("A"), 100000)},
		{"binary_garbage", []byte{0x00, 0xff, 0xfe, 0x80, 0x12, 0x34}},
	}

	for _, tc := range fuzzCases {
		t.Run(tc.name, func(t *testing.T) {
			defer func() {
				if r := recover(); r != nil {
					t.Fatalf("PANIC detected during parsing %s: %v", tc.name, r)
				}
			}()
			// Should return an error or nil, but never panic
			_ = HandleInputMessage(tc.raw, sink)
		})
	}
}

// TestInputConcurrency ensures thread-safety under heavy concurrent input events.
func TestInputConcurrency(t *testing.T) {
	sink := NewMemoryControlSink()
	var wg sync.WaitGroup
	numWorkers := 10
	eventsPerWorker := 50

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for j := 0; j < eventsPerWorker; j++ {
				payload := fmt.Sprintf(`{"type":"inject_touch","action":2,"id":%d,"x":%d,"y":%d,"w":1080,"h":1920}`,
					workerID, j*10, j*20)
				_ = HandleInputMessage([]byte(payload), sink)
			}
		}(i)
	}

	wg.Wait()
	msgs := sink.GetMessages()
	expectedTotal := numWorkers * eventsPerWorker
	if len(msgs) != expectedTotal {
		t.Fatalf("expected %d messages in sink, got %d", expectedTotal, len(msgs))
	}
}
