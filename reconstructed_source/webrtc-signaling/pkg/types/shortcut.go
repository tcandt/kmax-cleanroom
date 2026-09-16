// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Shortcut Struct Definition (main.KXuCJAAi60 @ 0x7d70c0)
// Evidence: SHORTCUT_TYPE_EVIDENCE.json, SHORTCUT_OPERATION_CONTRACTS.json
// Size: 32 bytes (2 fields, string each 16 bytes: DIHvMDn / name, MTkDoTKb / cmd)
// Confidence: HIGH

package types

// Shortcut represents an individual remote control action shortcut.
type Shortcut struct {
	Name string `json:"name"`
	Cmd  string `json:"cmd"`
}
