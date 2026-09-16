// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Thread-safe in-memory and on-disk ShortcutsStore
// Evidence:
//   - Loader: main.iXiPYH2zBLTK (VA: 0x76bf20, size: 640 bytes)
//   - Saver: main.jk9A26 (VA: 0x76c2c0, size: 608 bytes)
//   - Persistence: shortcuts.json, mode 0644 (0x1a4), direct os.WriteFile, 2-space json.MarshalIndent
//   - Top-level type: *map[string][]main.KXuCJAAi60 (VA: 0x7bfc40)
// Confidence: HIGH

package storage

import (
	"encoding/json"
	"os"
	"sync"

	"cloudphone-signaling/pkg/types"
)

// ShortcutsStore manages per-user shortcut configurations with disk persistence.
type ShortcutsStore struct {
	mu        sync.RWMutex
	shortcuts map[string][]types.Shortcut
	filePath  string
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_FUNCTION
// Mapping Scope: GENERATED_BUILD_FUNCTION
// Original Function Mapping: NONE
// Purpose: Constructs a new ShortcutsStore bound to a specific file path
// Confidence: HIGH
func NewShortcutsStore(filePath string) *ShortcutsStore {
	return &ShortcutsStore{
		shortcuts: make(map[string][]types.Shortcut),
		filePath:  filePath,
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.iXiPYH2zBLTK
// VA: 0x76bf20
// Size: 640 bytes
// Evidence: SHORTCUT_HTTP_FUNCTION_SLICES.json, SHORTCUT_PERSISTENCE_CONTRACT.json
//   - Checks os.Stat / os.IsNotExist on shortcuts.json
//   - Reads file with os.ReadFile
//   - Unmarshals into map[string][]Shortcut
// Confidence: HIGH
func (s *ShortcutsStore) LoadOrCreate() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	data, err := os.ReadFile(s.filePath)
	if err != nil {
		if os.IsNotExist(err) {
			if s.shortcuts == nil {
				s.shortcuts = make(map[string][]types.Shortcut)
			}
			return nil
		}
		return err
	}

	var loaded map[string][]types.Shortcut
	if err := json.Unmarshal(data, &loaded); err != nil {
		return err
	}
	if loaded == nil {
		loaded = make(map[string][]types.Shortcut)
	}
	s.shortcuts = loaded
	return nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.jk9A26
// VA: 0x76c2c0
// Size: 608 bytes
// Evidence: SHORTCUT_HTTP_FUNCTION_SLICES.json, SHORTCUT_PERSISTENCE_CONTRACT.json
//   - Marshals in-memory map with json.MarshalIndent(..., "", "  ")
//   - Writes directly to disk using os.WriteFile with permissions 0644 (0x1a4)
// Confidence: HIGH
func (s *ShortcutsStore) Save() error {
	s.mu.RLock()
	defer s.mu.RUnlock()

	return s.saveLocked()
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_FUNCTION
// Mapping Scope: GENERATED_BUILD_FUNCTION
// Original Function Mapping: NONE
// Purpose: Internal locked persistence helper executing direct WriteFile
// Confidence: HIGH
func (s *ShortcutsStore) saveLocked() error {
	data, err := json.MarshalIndent(s.shortcuts, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(s.filePath, data, 0644)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.yHBQWSpi (GET branch)
// VA: 0x76c640
// Size: 1856 bytes
// Evidence: SHORTCUT_HTTP_FUNCTION_SLICES.json, SHORTCUT_OPERATION_CONTRACTS.json
//   - Looks up shortcuts slice for username in map
//   - If absent or empty, returns empty slice [] types.Shortcut{}
// Confidence: HIGH
func (s *ShortcutsStore) Get(username string) []types.Shortcut {
	s.mu.RLock()
	defer s.mu.RUnlock()

	list, exists := s.shortcuts[username]
	if !exists || list == nil {
		return []types.Shortcut{}
	}
	// Return a copy to prevent external race conditions
	result := make([]types.Shortcut, len(list))
	copy(result, list)
	return result
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.yHBQWSpi (POST branch)
// VA: 0x76c640
// Size: 1856 bytes
// Evidence: SHORTCUT_HTTP_FUNCTION_SLICES.json, SHORTCUT_OPERATION_CONTRACTS.json
//   - Replaces user's slice in map: shortcuts[username] = list
//   - Immediately invokes main.jk9A26 (saveShortcuts) to persist to disk
// Confidence: HIGH
func (s *ShortcutsStore) Set(username string, list []types.Shortcut) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if list == nil {
		list = []types.Shortcut{}
	}
	s.shortcuts[username] = list
	return s.saveLocked()
}
