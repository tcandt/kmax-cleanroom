// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Type Descriptor VA: 0x80a0c0 (struct size: 152 bytes)
// Field Descriptor Array VA: 0x80a120 (13 fields)
// Evidence:
//   - .rodata structType header at 0x80a0c0, fields array at 0x80a120
//   - Field name descriptors and exact json tags parsed in TYPE_FIELD_EVIDENCE.json
//   - users.json fixture and dynamic first-run oracle serialization
// Confidence: HIGH

package types

import (
	"time"
)

// User represents a user account stored in users.json.
// Struct layout recovered directly from binary .rodata type descriptor at VA 0x80a0c0.
type User struct {
	Username         string                 `json:"username"`
	Password         string                 `json:"password"`
	Salt             string                 `json:"salt"`
	Role             string                 `json:"role"`
	AssignedDevices  []string               `json:"assigned_devices"`
	Note             string                 `json:"note"`
	ForbidBitrate    bool                   `json:"forbid_bitrate"`
	ForbidFPS        bool                   `json:"forbid_fps"`
	ForbidResolution bool                   `json:"forbid_resolution"`
	ForbidAudio      bool                   `json:"forbid_audio"`
	Settings         map[string]interface{} `json:"settings,omitempty"`
	ExpiresAt        time.Time              `json:"expires_at"`
	AIConfig         *map[string]interface{} `json:"ai_config,omitempty"`
}
