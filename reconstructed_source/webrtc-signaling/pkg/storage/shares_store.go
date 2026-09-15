// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol:
//   - main.fomL4ATwVV1 (VA: 0x739900, size: 1664 bytes) -> Thread-safe serialization, temp file write, and atomic rename
// Evidence:
//   - Exact log messages: "[Share] Failed to marshal share tokens: %v", "[Share] Failed to rename %s -> %s: %v"
//   - File mode argument: 0x180 (0600 octal) statically confirmed at VA 0x739cd9 (mov r8d, 0x180)
//   - Atomic temp-file write pattern: runtime.concatstring2 with ".tmp", os.WriteFile, then os.Rename at VA 0x739e12
//   - Lazy first-run lifecycle verified by first_run_persistence_oracle.py (NOT eagerly created at boot)
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

// SharesStore provides thread-safe persistence for device share tokens stored in shares.json.
type SharesStore struct {
	mu       sync.RWMutex
	filePath string
	shares   map[string]types.ShareToken
}

// NewSharesStore creates a new SharesStore instance pointing to the specified file path.
func NewSharesStore(filePath string) *SharesStore {
	return &SharesStore{
		filePath: filePath,
		shares:   make(map[string]types.ShareToken),
	}
}

// Load reads shares.json if it exists.
// Matches observed lifecycle: if shares.json does not exist, it remains absent (lazy creation).
func (s *SharesStore) Load() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	data, err := os.ReadFile(s.filePath)
	if os.IsNotExist(err) {
		s.shares = make(map[string]types.ShareToken)
		return nil
	} else if err != nil {
		return fmt.Errorf("failed to read shares file: %w", err)
	}

	var list []types.ShareToken
	if err := json.Unmarshal(data, &list); err != nil {
		s.shares = make(map[string]types.ShareToken)
		return fmt.Errorf("failed to parse shares file: %w", err)
	}

	s.shares = make(map[string]types.ShareToken, len(list))
	for _, item := range list {
		s.shares[item.TokenID] = item
	}
	return nil
}

// saveLocked writes the in-memory shares to <file>.tmp with 0600 permissions,
// then atomically renames to <file>.
// Reconstructs binary function main.fomL4ATwVV1 (VA 0x739900).
func (s *SharesStore) saveLocked() error {
	list := make([]types.ShareToken, 0, len(s.shares))
	for _, v := range s.shares {
		list = append(list, v)
	}

	bytes, err := json.MarshalIndent(list, "", "  ")
	if err != nil {
		log.Printf("[Share] Failed to marshal share tokens: %v", err)
		return fmt.Errorf("failed to marshal share tokens: %w", err)
	}

	tmpPath := s.filePath + ".tmp"
	// Direct os.WriteFile to .tmp with 0600 mode (VA 0x739cd9: mov r8d, 0x180)
	if err := os.WriteFile(tmpPath, bytes, 0600); err != nil {
		return fmt.Errorf("failed to write shares temp file: %w", err)
	}

	// Atomic rename from .tmp to target file (VA 0x739e12)
	if err := os.Rename(tmpPath, s.filePath); err != nil {
		log.Printf("[Share] Failed to rename %s -> %s: %v", tmpPath, s.filePath, err)
		return fmt.Errorf("failed to rename %s -> %s: %w", tmpPath, s.filePath, err)
	}

	return nil
}

// GetToken retrieves a share token by token ID under read lock.
func (s *SharesStore) GetToken(tokenID string) (types.ShareToken, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	tok, exists := s.shares[tokenID]
	return tok, exists
}

// ListTokens retrieves all share tokens under read lock.
func (s *SharesStore) ListTokens() []types.ShareToken {
	s.mu.RLock()
	defer s.mu.RUnlock()
	res := make([]types.ShareToken, 0, len(s.shares))
	for _, v := range s.shares {
		res = append(res, v)
	}
	return res
}

// SetToken adds or updates a share token under write lock and persists atomically to disk.
func (s *SharesStore) SetToken(token types.ShareToken) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.shares[token.TokenID] = token
	return s.saveLocked()
}

// DeleteToken removes a share token by token ID under write lock and persists atomically to disk.
func (s *SharesStore) DeleteToken(tokenID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.shares, tokenID)
	return s.saveLocked()
}
