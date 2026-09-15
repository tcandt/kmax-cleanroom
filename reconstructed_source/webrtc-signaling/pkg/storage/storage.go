// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol: main.main (VA: 0x7647a0), main.aOfaLG (VA: 0x736ae0), main.w3H7BXxDC (VA: 0x737880)
// Evidence:
//   - Directory initialization in main.main (-data flag, downloads/ and snapshots/ creation)
//   - Global file paths table in .data section at 0xbeedb0 (users.json), 0xbeedc0 (device_tags.json), 0xbeedf0 (shares.json)
//   - First-run lifecycle verified by first_run_persistence_oracle.py
// Confidence: HIGH

package storage

import (
	"fmt"
	"os"
	"path/filepath"
)

// StorageManager coordinates file persistence and directory structures for the signaling service.
type StorageManager struct {
	DataDir     string
	UsersStore  *UsersStore
	TagsStore   *TagsStore
	SharesStore *SharesStore
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: constructs StorageManager coordinator around reconstructed stores
// Confidence: N/A
func NewStorageManager(dataDir string) (*StorageManager, error) {
	if dataDir == "" {
		dataDir = "./data"
	}

	// Ensure root data directory exists
	if err := os.MkdirAll(dataDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create data directory: %w", err)
	}

	// Ensure downloads and snapshots directories exist (observed during binary bootstrap)
	downloadsDir := filepath.Join(dataDir, "downloads")
	if err := os.MkdirAll(downloadsDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create downloads directory: %w", err)
	}

	snapshotsDir := filepath.Join(dataDir, "snapshots")
	if err := os.MkdirAll(snapshotsDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create snapshots directory: %w", err)
	}

	sm := &StorageManager{
		DataDir:     dataDir,
		UsersStore:  NewUsersStore(filepath.Join(dataDir, "users.json")),
		TagsStore:   NewTagsStore(filepath.Join(dataDir, "device_tags.json")),
		SharesStore: NewSharesStore(filepath.Join(dataDir, "shares.json")),
	}

	return sm, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BEHAVIOR
// Binary Symbol: main.main
// VA: 0x7647a0
// Evidence: bootstrap sequence creating downloads/, snapshots/ and calling users/tags store loaders
// Confidence: HIGH
func (sm *StorageManager) InitBootstrap() error {
	if err := sm.UsersStore.LoadOrCreate(); err != nil {
		return fmt.Errorf("users store bootstrap failed: %w", err)
	}
	if err := sm.TagsStore.LoadOrCreate(); err != nil {
		return fmt.Errorf("tags store bootstrap failed: %w", err)
	}
	return nil
}
