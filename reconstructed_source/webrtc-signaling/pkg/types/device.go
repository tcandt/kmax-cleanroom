// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Type Descriptor VA: 0x7ff0e0 (struct size: 120 bytes)
// Field Descriptor Array VA: 0x7ff140 (7 fields)
// Evidence:
//   - .rodata structType header at 0x7ff0e0, fields array at 0x7ff140
//   - Field name descriptors and exact json tags parsed in DEVICE_TYPE_EVIDENCE.json
//   - Dynamic oracle response serialization on /devices endpoint
// Confidence: HIGH

package types

import (
	"sync"
	"time"
)

// DeviceDTO represents the public JSON structure returned by GET /devices.
// Struct layout recovered directly from binary .rodata type descriptor at VA 0x7ff0e0.
// Classification: DIRECT_TYPE_RECOVERY
type DeviceDTO struct {
	DeviceID    string        `json:"device_id"`
	DeviceInfo  interface{}   `json:"device_info"`
	Online      bool          `json:"online"`
	FirstSeen   time.Time     `json:"first_seen"`
	LastSeen    time.Time     `json:"last_seen"`
	ClientCount int           `json:"client_count"`
	Clients     []interface{} `json:"clients,omitempty"`
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BEHAVIOR
// Mapping Scope: CLEANROOM_BEHAVIORAL_REGISTRY_MODEL
// Original Function Mapping: NONE
// Original Binary Struct: main.AoIDVQHamcx at VA 0x805760 (128 bytes, 10 fields)
// Relationship to Original: NOT_LAYOUT_EQUIVALENT_TO_ORIGINAL_DEVICEENTRY
// Description: Simplified cleanroom in-memory representation capturing the fields required
//   for REST API behavior (/devices listing, filtering, and deletion).
// Deferred Internal Fields:
//   - webrtc_flag (offset 0x34): DEFERRED_INTERNAL_FIELD / PHASE_2C4_OR_2C6
//     Proven via binary disassembly of main.i2EgUTaLmQs and dynamic oracle testing to have
//     zero effect on /devices REST output or deletion lifecycle.
//   - ws_connection (offset 0x20): WebSocket peer connection pointer (deferred to Phase 2C.4)
//   - connected_clients (offset 0x28): map[uint32]*client (deferred to Phase 2C.4)
// Confidence: HIGH

// DeviceEntry represents the simplified cleanroom internal registry record.
type DeviceEntry struct {
	DeviceID    string
	DeviceInfo  interface{}
	Online      bool
	FirstSeen   time.Time
	LastSeen    time.Time
	ClientCount int
	Clients     []interface{}
	Mu          sync.RWMutex
}
