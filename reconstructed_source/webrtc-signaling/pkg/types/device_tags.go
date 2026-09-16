// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Type Descriptor VAs:
//   - Tag: 0x7e25a0 (main.UeyzO4kumc, struct size: 48 bytes, 3 fields: id, name, color)
//   - DeviceTagsConfig: 0x7d6f80 (main.Svdju9, struct size: 32 bytes, 2 fields: tags, deviceTags)
// Evidence:
//   - .rodata structType header at 0x7e25a0 (Tag) and 0x7d6f80 (DeviceTagsConfig)
//   - GET /api/tags wire response schema: {"tags": [{"id": "...", "name": "...", "color": "..."}], "deviceTags": {"dev-id": ["tag-id"]}}
// Confidence: HIGH

package types

// Tag represents a single device category tag.
// Struct layout recovered directly from binary .rodata type descriptor at VA 0x7e25a0 (main.UeyzO4kumc).
type Tag struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Color string `json:"color"`
}

// DeviceTagsConfig represents the configuration stored in device_tags.json and returned by /api/tags.
// Struct layout recovered directly from binary .rodata type descriptor at VA 0x7d6f80 (main.Svdju9).
type DeviceTagsConfig struct {
	Tags       []Tag               `json:"tags"`
	DeviceTags map[string][]string `json:"deviceTags"`
}
