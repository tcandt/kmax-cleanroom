// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol:
//   - main.w3H7BXxDC (VA: 0x737880, size: 928 bytes) -> Load, default initialization, parse recovery
//   - main.rCajRnfJZ (VA: 0x737da0, size: 608 bytes) -> Thread-safe serialization and direct file write
// Evidence:
//   - Exact log message: "[Tags] Initialized device_tags.json with empty list"
//   - File mode argument: 0x1a4 (0644 octal) statically confirmed at VA 0x737f15 (mov r8d, 0x1a4)
//   - Eager creation on first run verified by first_run_persistence_oracle.py
// Confidence: HIGH

package storage

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"

	"cloudphone-signaling/pkg/types"
)

// TagsStore provides thread-safe persistence for device tags configuration stored in device_tags.json.
type TagsStore struct {
	mu       sync.RWMutex
	filePath string
	config   types.DeviceTagsConfig
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: constructs TagsStore around device tags file path
// Confidence: N/A
func NewTagsStore(filePath string) *TagsStore {
	return &TagsStore{
		filePath: filePath,
		config: types.DeviceTagsConfig{
			Tags:       []string{},
			DeviceTags: make(map[string][]string),
		},
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.w3H7BXxDC
// VA: 0x737880
// Evidence: device_tags.json load lifecycle, empty list initialization, malformed recovery
// Confidence: HIGH
func (s *TagsStore) LoadOrCreate() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	data, err := os.ReadFile(s.filePath)
	if os.IsNotExist(err) {
		s.config = types.DeviceTagsConfig{
			Tags:       []string{},
			DeviceTags: make(map[string][]string),
		}
		log.Printf("[Tags] Initialized device_tags.json with empty list")
		return s.saveLocked()
	} else if err != nil {
		log.Printf("[Tags] Failed to read device tags file: %v", err)
		return fmt.Errorf("failed to read device tags file: %w", err)
	}

	var loaded types.DeviceTagsConfig
	if err := json.Unmarshal(data, &loaded); err != nil {
		log.Printf("[Tags] Failed to parse device tags file: %v", err)
		s.config = types.DeviceTagsConfig{
			Tags:       []string{},
			DeviceTags: make(map[string][]string),
		}
		log.Printf("[Tags] Initialized device_tags.json with empty list")
		return s.saveLocked()
	}

	if loaded.Tags == nil {
		loaded.Tags = []string{}
	}
	if loaded.DeviceTags == nil {
		loaded.DeviceTags = make(map[string][]string)
	}
	s.config = loaded
	return nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.rCajRnfJZ
// VA: 0x737da0
// Evidence: device_tags.json serialization via json.MarshalIndent, direct write with 0644 permissions
// Confidence: HIGH
func (s *TagsStore) saveLocked() error {
	bytes, err := json.MarshalIndent(s.config, "", "  ")
	if err != nil {
		log.Printf("[Tags] Failed to marshal device tags: %v", err)
		return fmt.Errorf("failed to marshal device tags: %w", err)
	}

	// Direct os.WriteFile with 0644 mode (VA 0x737f15: mov r8d, 0x1a4)
	if err := os.WriteFile(s.filePath, bytes, 0644); err != nil {
		log.Printf("[Tags] Failed to write device tags file: %v", err)
		return fmt.Errorf("failed to write device tags file: %w", err)
	}

	return nil
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: deep copy of device tags configuration under read lock
// Confidence: N/A
func (s *TagsStore) GetConfig() types.DeviceTagsConfig {
	s.mu.RLock()
	defer s.mu.RUnlock()

	tagsCopy := make([]string, len(s.config.Tags))
	copy(tagsCopy, s.config.Tags)

	dtCopy := make(map[string][]string, len(s.config.DeviceTags))
	for k, v := range s.config.DeviceTags {
		vCopy := make([]string, len(v))
		copy(vCopy, v)
		dtCopy[k] = vCopy
	}

	return types.DeviceTagsConfig{
		Tags:       tagsCopy,
		DeviceTags: dtCopy,
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: updates device tags configuration under write lock followed by persistence
// Confidence: N/A
func (s *TagsStore) SetConfig(cfg types.DeviceTagsConfig) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if cfg.Tags == nil {
		cfg.Tags = []string{}
	}
	if cfg.DeviceTags == nil {
		cfg.DeviceTags = make(map[string][]string)
	}

	s.config = cfg
	return s.saveLocked()
}
