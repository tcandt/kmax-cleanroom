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
	"time"

	"cloudphone-signaling/pkg/types"
)

// SharesStore provides thread-safe persistence for device share tokens stored in shares.json.
type SharesStore struct {
	mu       sync.RWMutex
	filePath string
	shares   map[string]types.ShareToken
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: constructs SharesStore around shares file path
// Confidence: N/A
func NewSharesStore(filePath string) *SharesStore {
	return &SharesStore{
		filePath: filePath,
		shares:   make(map[string]types.ShareToken),
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.wRVYHLD_
// VA: 0x7395c0
// Evidence: shares.json load lifecycle, os.ReadFile, unmarshal into in-memory map
// Confidence: HIGH
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

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.fomL4ATwVV1
// VA: 0x739900
// Evidence: atomic serialization to <file>.tmp with 0600 mode and os.Rename
// Confidence: HIGH
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

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: retrieves share token by ID under read lock
// Confidence: N/A
func (s *SharesStore) GetToken(tokenID string) (types.ShareToken, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	tok, exists := s.shares[tokenID]
	return tok, exists
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: lists all share tokens under read lock
// Confidence: N/A
func (s *SharesStore) ListTokens() []types.ShareToken {
	s.mu.RLock()
	defer s.mu.RUnlock()
	res := make([]types.ShareToken, 0, len(s.shares))
	for _, v := range s.shares {
		res = append(res, v)
	}
	return res
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: sets or updates share token under write lock followed by atomic save
// Confidence: N/A
func (s *SharesStore) SetToken(token types.ShareToken) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.shares[token.TokenID] = token
	return s.saveLocked()
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: removes share token by ID under write lock followed by atomic save
// Confidence: N/A
func (s *SharesStore) DeleteToken(tokenID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.shares, tokenID)
	return s.saveLocked()
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: finds active share token by device ID under read lock
// Confidence: N/A
func (s *SharesStore) GetTokenByDeviceID(deviceID string) (types.ShareToken, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, tok := range s.shares {
		if tok.DeviceID == deviceID {
			return tok, true
		}
	}
	return types.ShareToken{}, false
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: finds share token by card code under read lock
// Confidence: N/A
func (s *SharesStore) GetTokenByCardCode(cardCode string) (types.ShareToken, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, tok := range s.shares {
		if tok.CardCode == cardCode {
			return tok, true
		}
	}
	return types.ShareToken{}, false
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: extends share expiration by seconds under write lock followed by save
// Confidence: N/A
func (s *SharesStore) ExtendToken(tokenID string, extendSeconds int64) (types.ShareToken, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	tok, exists := s.shares[tokenID]
	if !exists {
		return types.ShareToken{}, fmt.Errorf("token not found")
	}
	if tok.ExpiresAt.IsZero() {
		return tok, fmt.Errorf("permanent share")
	}
	tok.ExpiresAt = tok.ExpiresAt.Add(time.Duration(extendSeconds) * time.Second)
	s.shares[tokenID] = tok
	if err := s.saveLocked(); err != nil {
		return types.ShareToken{}, err
	}
	return tok, nil
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: updates mutable share fields under write lock followed by save
// Confidence: N/A
func (s *SharesStore) UpdateToken(tokenID string, req types.UpdateShareRequest) (types.ShareToken, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	tok, exists := s.shares[tokenID]
	if !exists {
		return types.ShareToken{}, fmt.Errorf("token not found")
	}

	tok.ForbidBitrate = req.ForbidBitrate
	tok.ForbidFPS = req.ForbidFPS
	tok.ForbidResolution = req.ForbidResolution
	tok.ForbidAudio = req.ForbidAudio
	if req.GuestSettings != nil {
		tok.GuestSettings = req.GuestSettings
	}

	s.shares[tokenID] = tok
	if err := s.saveLocked(); err != nil {
		return types.ShareToken{}, err
	}
	return tok, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.dYBSRoVh.func1
// VA: 0x73a120
// Evidence: SHARE_HTTP_FUNCTION_SLICES.json, SHARE_EXPIRY_CONTRACT.json
// Confidence: HIGH
func (s *SharesStore) ReapExpired(now time.Time) (int, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	reaped := 0
	for id, tok := range s.shares {
		if !tok.ExpiresAt.IsZero() && now.After(tok.ExpiresAt) {
			delete(s.shares, id)
			reaped++
		}
	}
	if reaped > 0 {
		return reaped, s.saveLocked()
	}
	return 0, nil
}

