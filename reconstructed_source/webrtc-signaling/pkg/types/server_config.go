// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Server Configuration Types & Struct Definitions
// Evidence:
//   - ICE Server Struct: main.Py1TDt at VA 0x7e24e0 (size 56B, fields: KWpyoL []string @ 0, Do87J_ string @ 24, G4kKJB5xuff string @ 40)
//   - Server Addresses Response: SERVER_ADDRESSES_CONTRACT.json (handler main.vz0hZo0q1IzM @ 0x7632a0)
//   - Version Globals: VERSION_CONTRACT.json (handler main.ys0CAJV5f5k @ 0x769840)
// Confidence: HIGH

package types

// ICEServer represents a WebRTC STUN/TURN server configuration element.
// Directly mapped from binary struct main.Py1TDt at VA 0x7e24e0 (AMD64 56 bytes).
type ICEServer struct {
	URLs       []string `json:"urls"`
	Username   string   `json:"username,omitempty"`
	Credential string   `json:"credential,omitempty"`
}

// ServerAddressesData represents the internal data payload for /api/server/addresses.
type ServerAddressesData struct {
	Addresses []string `json:"addresses"`
	Current   string   `json:"current"`
}

// ServerAddressesResponse represents the envelope for /api/server/addresses.
type ServerAddressesResponse struct {
	Code int                 `json:"code"`
	Data ServerAddressesData `json:"data"`
}

// VersionInfo represents the system version and build metadata for /api/version.
type VersionInfo struct {
	BuildTime string `json:"build_time"`
	GitCommit string `json:"git_commit"`
	Version   string `json:"version"`
}
