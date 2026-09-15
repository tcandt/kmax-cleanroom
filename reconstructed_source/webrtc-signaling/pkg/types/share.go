// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Type Descriptor VA: 0x80f700 (struct size: 192 bytes)
// Field Descriptor Array VA: 0x80f760 (18 fields)
// Evidence:
//   - .rodata structType header at 0x80f700, fields array at 0x80f760
//   - All 18 field names and json tags verified in TYPE_FIELD_EVIDENCE.json
//   - shares.json serialization routine in main.fomL4ATwVV1 at VA 0x739900
// Confidence: HIGH

package types

import (
	"time"
)

// ShareToken represents a device sharing token stored in shares.json.
// Struct layout recovered directly from binary .rodata type descriptor at VA 0x80f700.
type ShareToken struct {
	TokenID          string                 `json:"token_id"`
	CardCode         string                 `json:"card_code"`
	DeviceID         string                 `json:"device_id"`
	Creator          string                 `json:"creator"`
	CreatedAt        time.Time              `json:"created_at"`
	ExpiresAt        time.Time              `json:"expires_at"`
	AccessMode       string                 `json:"access_mode"`
	RequirePassword  bool                   `json:"require_password"`
	PasswordHash     string                 `json:"password_hash,omitempty"`
	AllowClipboard   bool                   `json:"allow_clipboard"`
	AllowFileTx      bool                   `json:"allow_file_tx"`
	ForbidBitrate    bool                   `json:"forbid_bitrate"`
	ForbidFPS        bool                   `json:"forbid_fps"`
	ForbidResolution bool                   `json:"forbid_resolution"`
	ForbidAudio      bool                   `json:"forbid_audio"`
	GuestSettings    map[string]interface{} `json:"guest_settings,omitempty"`
	Description      string                 `json:"description"`
	UseCount         int64                  `json:"use_count"`
}
