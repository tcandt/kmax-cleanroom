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

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: constructs UsersStore around persistence file path
// Confidence: N/A
func NewUsersStore(filePath string) *UsersStore {
	return &UsersStore{
		filePath: filePath,
		users:    make(map[string]types.User),
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.b1g4g23Z
// VA: 0x736c40
// Evidence: 16-byte cryptographically secure random hexadecimal generation
// Confidence: HIGH
func GenerateSalt() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.h72nXa_b
// VA: 0x736d80
// Evidence: sha256.Sum256(password + salt) hex-encoded derivation for stored records
// Confidence: HIGH
func HashPassword(password, salt string) string {
	h := sha256.Sum256([]byte(password + salt))
	return hex.EncodeToString(h[:])
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.aOfaLG
// VA: 0x736ae0
// Evidence: users.json load lifecycle, admin/admin123 initialization, wildcard upgrade, malformed recovery
// Confidence: HIGH
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

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.rAJGaVlvfajr
// VA: 0x737500
// Evidence: users.json serialization via json.MarshalIndent, direct write with 0600 permissions
// Confidence: HIGH
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

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: wraps in-memory user lookup under read lock
// Confidence: N/A
func (s *UsersStore) GetUser(username string) (types.User, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	u, exists := s.users[username]
	return u, exists
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: wraps in-memory user map snapshot under read lock
// Confidence: N/A
func (s *UsersStore) ListUsers() map[string]types.User {
	s.mu.RLock()
	defer s.mu.RUnlock()
	res := make(map[string]types.User, len(s.users))
	for k, v := range s.users {
		res[k] = v
	}
	return res
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: in-memory user upsert under write lock followed by persistence
// Confidence: N/A
func (s *UsersStore) SetUser(user types.User) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.users[user.Username] = user
	return s.saveLocked()
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: in-memory user deletion under write lock followed by persistence
// Confidence: N/A
func (s *UsersStore) DeleteUser(username string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.users, username)
	return s.saveLocked()
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.sGuPXW2D
// VA: 0x740f40
// Evidence: user key swap, avoiding the original binary's self-deadlock
// Confidence: HIGH
func (s *UsersStore) RenameUser(oldName, newName string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	user, exists := s.users[oldName]
	if !exists {
		return fmt.Errorf("user not found")
	}
	if _, exists := s.users[newName]; exists {
		return fmt.Errorf("username already exists")
	}

	delete(s.users, oldName)
	user.Username = newName
	s.users[newName] = user
	return s.saveLocked()
}
