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

// CreateShareRequest represents the payload for POST /api/share/create.
type CreateShareRequest struct {
	DeviceID         string                 `json:"device_id"`
	ExpireSeconds    int64                  `json:"expire_seconds"`
	Password         string                 `json:"password"`
	AccessMode       string                 `json:"access_mode"`
	AllowClipboard   bool                   `json:"allow_clipboard"`
	AllowFileTx      bool                   `json:"allow_file_tx"`
	ForbidBitrate    bool                   `json:"forbid_bitrate"`
	ForbidFPS        bool                   `json:"forbid_fps"`
	ForbidResolution bool                   `json:"forbid_resolution"`
	ForbidAudio      bool                   `json:"forbid_audio"`
	GuestSettings    map[string]interface{} `json:"guest_settings,omitempty"`
	Description      string                 `json:"description"`
}

// CreateShareResponseData represents the data payload returned on share creation.
type CreateShareResponseData struct {
	AccessMode string    `json:"access_mode"`
	CardCode   string    `json:"card_code"`
	DeviceID   string    `json:"device_id"`
	ExpiresAt  time.Time `json:"expires_at"`
	ShareURL   string    `json:"share_url"`
	Token      string    `json:"token"`
}

// ShareListItem represents a share token with active connection count in /api/share/list.
type ShareListItem struct {
	ShareToken
	ActiveConnections int `json:"active_connections"`
}

// ShareInfoResponseData represents the data payload returned by /api/share/info.
type ShareInfoResponseData struct {
	AccessMode       string                 `json:"access_mode"`
	AllowClipboard   bool                   `json:"allow_clipboard"`
	AllowFileTx      bool                   `json:"allow_file_tx"`
	CardCode         string                 `json:"card_code"`
	Description      string                 `json:"description"`
	DeviceID         string                 `json:"device_id"`
	DeviceName       string                 `json:"device_name"`
	ExpiresAt        time.Time              `json:"expires_at"`
	ForbidAudio      bool                   `json:"forbid_audio"`
	ForbidBitrate    bool                   `json:"forbid_bitrate"`
	ForbidFPS        bool                   `json:"forbid_fps"`
	ForbidResolution bool                   `json:"forbid_resolution"`
	GuestSettings    map[string]interface{} `json:"guest_settings"`
	Online           bool                   `json:"online"`
	RemainingSeconds int64                  `json:"remaining_seconds"`
	RequirePassword  bool                   `json:"require_password"`
	Token            string                 `json:"token"`
}

// ExtendShareRequest represents the payload for POST /api/share/extend.
type ExtendShareRequest struct {
	Token         string `json:"token"`
	ExtendSeconds int64  `json:"extend_seconds"`
}

// UpdateShareRequest represents the payload for POST /api/share/update.
// Directly recovered from binary type descriptor 0x7f9640:
// - token (string)
// - forbid_bitrate (bool)
// - forbid_fps (bool)
// - forbid_resolution (bool)
// - forbid_audio (bool)
// - guest_settings (*map[string]interface{})
type UpdateShareRequest struct {
	Token            string                 `json:"token"`
	ForbidBitrate    bool                   `json:"forbid_bitrate"`
	ForbidFPS        bool                   `json:"forbid_fps"`
	ForbidResolution bool                   `json:"forbid_resolution"`
	ForbidAudio      bool                   `json:"forbid_audio"`
	GuestSettings    map[string]interface{} `json:"guest_settings,omitempty"`
}

// RevokeShareRequest represents the payload for POST /api/share/revoke.
type RevokeShareRequest struct {
	Token string `json:"token"`
}

// RedeemCardRequest represents the payload for POST /api/share/redeem_card.
type RedeemCardRequest struct {
	CardCode string `json:"card_code"`
}

