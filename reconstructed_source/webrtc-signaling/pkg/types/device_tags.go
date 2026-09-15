// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Type Descriptor VA: 0x7d6f80 (struct size: 32 bytes)
// Field Descriptor Array VA: 0x7d6fe0 (2 fields)
// Evidence:
//   - .rodata structType header at 0x7d6f80, fields array at 0x7d6fe0
//   - Field 0: offset 0, name 'tags', type slice (size 24) VA 0x7969a0
//   - Field 1: offset 24, name 'deviceTags', type map (size 8) VA 0x7bf9c0
//   - device_tags.json fixture and dynamic first-run oracle serialization
// Confidence: HIGH

package types

// DeviceTagsConfig represents the configuration stored in device_tags.json.
// Struct layout recovered directly from binary .rodata type descriptor at VA 0x7d6f80.
type DeviceTagsConfig struct {
	Tags       []string            `json:"tags"`
	DeviceTags map[string][]string `json:"deviceTags"`
}
