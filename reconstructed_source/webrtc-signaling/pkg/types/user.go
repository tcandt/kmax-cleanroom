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
	AIConfig         *AIConfig              `json:"ai_config,omitempty"`
}

// AIConfig represents the AI service configuration for a user.
// Layout recovered from binary type descriptor at VA 0x7ed060.
type AIConfig struct {
	APIURL   string `json:"ai_api_url"`
	APIKey   string `json:"ai_api_key"`
	Model    string `json:"ai_model"`
	Provider string `json:"ai_provider"`
}

// CreateUserRequest represents the payload for /api/admin/users/create.
// Binary Type Descriptor VA: 0x7f3020 (72 bytes).
type CreateUserRequest struct {
	Username      string `json:"username"`
	Password      string `json:"password"`
	Role          string `json:"role"`
	Note          string `json:"note"`
	ExpireSeconds int64  `json:"expire_seconds"`
}

// UpdateUserRequest represents the payload for /api/admin/users/update.
// Binary Type Descriptor VA: 0x7fe6c0 (40 bytes).
type UpdateUserRequest struct {
	Username         string                 `json:"username"`
	ForbidBitrate    bool                   `json:"forbid_bitrate"`
	ForbidFPS        bool                   `json:"forbid_fps"`
	ForbidResolution bool                   `json:"forbid_resolution"`
	ForbidAudio      bool                   `json:"forbid_audio"`
	Settings         map[string]interface{} `json:"settings"`
	ExpireSeconds    int64                  `json:"expire_seconds"`
}

// AssignDevicesRequest represents the payload for /api/admin/assign.
// Binary Type Descriptor VA: 0x7caba0 (40 bytes).
type AssignDevicesRequest struct {
	Username string   `json:"username"`
	Devices  []string `json:"devices"`
}

// UpdateNoteRequest represents the payload for /api/admin/users/update_note.
// Binary Type Descriptor VA: 0x7cac20 (32 bytes).
type UpdateNoteRequest struct {
	Username string `json:"username"`
	Note     string `json:"note"`
}

// ResetPasswordRequest represents the payload for /api/admin/users/reset_password.
// Binary Type Descriptor VA: 0x7cada0 (32 bytes).
type ResetPasswordRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// KickUserRequest represents the payload for /api/admin/users/kick.
// Binary Type Descriptor VA: 0x7cae20 (32 bytes).
type KickUserRequest struct {
	Username string `json:"username"`
	DeviceID string `json:"device_id"`
}

// RenameUserRequest represents the payload for /api/admin/users/rename.
// Binary Type Descriptor VA: 0x7caf20 (32 bytes).
type RenameUserRequest struct {
	OldUsername string `json:"old_username"`
	NewUsername string `json:"new_username"`
}

// DeleteUserRequest represents the payload for /api/admin/users/delete.
// Binary Type Descriptor VA: 0x7bd600 (16 bytes).
type DeleteUserRequest struct {
	Username string `json:"username"`
}
