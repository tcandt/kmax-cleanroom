// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol:
//   - main.aOfaLG (VA: 0x736ae0, size: 2112 bytes) -> Load, default initialization, parse recovery, admin upgrade
//   - main.rAJGaVlvfajr (VA: 0x737500, size: 608 bytes) -> Thread-safe serialization and direct file write
// Evidence:
//   - Exact log messages: "[Auth] Initialized users.json with default account admin/admin123",
//     "[Auth] Reset users.json with default account admin/admin123",
//     "[Auth] Upgraded admin user permissions in users.json"
//   - File mode argument: 0x180 (0600 octal) statically confirmed at VA 0x737666 (mov r8d, 0x180)
//   - Default admin hashing: SHA256(password + salt) with 16-byte random hex salt
// Confidence: HIGH

package storage

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	"cloudphone-signaling/pkg/types"
)

// UsersStore provides thread-safe persistence for user accounts stored in users.json.
type UsersStore struct {
	mu       sync.RWMutex
	filePath string
	users    map[string]types.User
}

// NewUsersStore creates a new UsersStore instance pointing to the specified file path.
func NewUsersStore(filePath string) *UsersStore {
	return &UsersStore{
		filePath: filePath,
		users:    make(map[string]types.User),
	}
}

// GenerateSalt creates a 16-byte cryptographically secure random hexadecimal string (32 characters).
func GenerateSalt() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

// HashPassword calculates SHA256(password + salt) matching original binary password derivation.
// Note: This is a data-model derivation function required to populate persisted records.
// Authentication/login verification logic is strictly excluded.
func HashPassword(password, salt string) string {
	h := sha256.Sum256([]byte(password + salt))
	return hex.EncodeToString(h[:])
}

// LoadOrCreate loads users.json or initializes it with the default administrator account.
// Reconstructs the exact lifecycle of binary function main.aOfaLG (VA 0x736ae0).
func (s *UsersStore) LoadOrCreate() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	data, err := os.ReadFile(s.filePath)
	if os.IsNotExist(err) {
		// First-run bootstrap: initialize default admin
		s.users = make(map[string]types.User)
		salt := GenerateSalt()
		admin := types.User{
			Username:         "admin",
			Password:         HashPassword("admin123", salt),
			Salt:             salt,
			Role:             "admin",
			AssignedDevices:  []string{"*"},
			Note:             "",
			ForbidBitrate:    false,
			ForbidFPS:        false,
			ForbidResolution: false,
			ForbidAudio:      false,
			ExpiresAt:        time.Time{}, // 0001-01-01T00:00:00Z
		}
		s.users["admin"] = admin
		log.Printf("[Auth] Initialized users.json with default account admin/admin123")
		return s.saveLocked()
	} else if err != nil {
		log.Printf("[Auth] Failed to read users file: %v", err)
		return fmt.Errorf("failed to read users file: %w", err)
	}

	// File exists: attempt parse
	loaded := make(map[string]types.User)
	if err := json.Unmarshal(data, &loaded); err != nil {
		log.Printf("[Auth] Failed to parse users file: %v", err)
		// Binary recovery behavior: reset corrupted file with default account
		s.users = make(map[string]types.User)
		salt := GenerateSalt()
		admin := types.User{
			Username:         "admin",
			Password:         HashPassword("admin123", salt),
			Salt:             salt,
			Role:             "admin",
			AssignedDevices:  []string{"*"},
			Note:             "",
			ForbidBitrate:    false,
			ForbidFPS:        false,
			ForbidResolution: false,
			ForbidAudio:      false,
			ExpiresAt:        time.Time{},
		}
		s.users["admin"] = admin
		log.Printf("[Auth] Reset users.json with default account admin/admin123")
		return s.saveLocked()
	}

	s.users = loaded

	// Check admin user assigned devices wildcard upgrade (VA 0x736eee in main.aOfaLG)
	if admin, exists := s.users["admin"]; exists {
		hasWildcard := false
		for _, dev := range admin.AssignedDevices {
			if dev == "*" {
				hasWildcard = true
				break
			}
		}
		if !hasWildcard {
			admin.AssignedDevices = append(admin.AssignedDevices, "*")
			s.users["admin"] = admin
			log.Printf("[Auth] Upgraded admin user permissions in users.json")
			_ = s.saveLocked()
		}
	}

	return nil
}

// saveLocked writes the in-memory map to users.json with 0600 permissions.
// Reconstructs binary function main.rAJGaVlvfajr (VA 0x737500).
func (s *UsersStore) saveLocked() error {
	bytes, err := json.MarshalIndent(s.users, "", "  ")
	if err != nil {
		log.Printf("[Auth] Failed to marshal users: %v", err)
		return fmt.Errorf("failed to marshal users: %w", err)
	}

	// Direct os.WriteFile with 0600 mode (VA 0x737666: mov r8d, 0x180)
	if err := os.WriteFile(s.filePath, bytes, 0600); err != nil {
		log.Printf("[Auth] Failed to write users file: %v", err)
		return fmt.Errorf("failed to write users file: %w", err)
	}

	return nil
}

// GetUser retrieves a copy of a user record by username under read lock.
func (s *UsersStore) GetUser(username string) (types.User, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	u, exists := s.users[username]
	return u, exists
}

// ListUsers retrieves all user records under read lock.
func (s *UsersStore) ListUsers() map[string]types.User {
	s.mu.RLock()
	defer s.mu.RUnlock()
	res := make(map[string]types.User, len(s.users))
	for k, v := range s.users {
		res[k] = v
	}
	return res
}

// SetUser saves or updates a user record under write lock and persists to disk.
func (s *UsersStore) SetUser(user types.User) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.users[user.Username] = user
	return s.saveLocked()
}

// DeleteUser removes a user record under write lock and persists to disk.
func (s *UsersStore) DeleteUser(username string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.users, username)
	return s.saveLocked()
}
