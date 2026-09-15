// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol:
//   - main.vT6rYK_v (VA: 0x739320, size: 288 bytes) -> Session creation, 24h TTL addition, map insertion
//   - main.lYKp_Iuf (VA: 0x73b080, size: 1120 bytes) -> Token lookup, lazy TTL check & deletion
//   - main.bjWkHiittd (VA: 0x7409a0, size: 1440 bytes) -> Token revocation under mutex lock
//   - main.cFpPBbFet (VA: 0x73a500, size: 128 bytes) -> 1-minute ticker sweeper spawner
//   - main.cFpPBbFet.func1 (VA: 0x73a580, size: 1600 bytes) -> Expired account token revocation
// Evidence:
//   - Map descriptor 0x7c01c0 (map[string]Session where Session is 40-byte struct)
//   - Mutex lock/unlock sequences surrounding map access (sync.(*Mutex).Lock/Unlock at VA 0x739356, 0x73b478, 0x740d00)
//   - time.Time.After lazy comparison at VA 0x73b2c9 followed by mapdelete_faststr at VA 0x73b495
// Confidence: HIGH

package session

import (
	"log"
	"sync"
	"time"

	"cloudphone-signaling/pkg/storage"
)

// SessionManager provides thread-safe in-memory session management matching original binary behavior.
type SessionManager struct {
	mu       sync.RWMutex
	sessions map[string]Session
	clock    Clock
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: constructs SessionManager with optional Clock
// Confidence: N/A
func NewSessionManager(clock Clock) *SessionManager {
	if clock == nil {
		clock = RealClock{}
	}
	return &SessionManager{
		sessions: make(map[string]Session),
		clock:    clock,
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.vT6rYK_v
// VA: 0x739320
// Evidence: generates random 64-char token, adds 24 hours to now, stores Session in map under lock
// Confidence: HIGH
func (m *SessionManager) CreateSession(username string) (string, error) {
	token, err := GenerateToken()
	if err != nil {
		return "", err
	}

	expiresAt := m.clock.Now().Add(DefaultSessionTTL)

	m.mu.Lock()
	m.sessions[token] = Session{
		Username:  username,
		ExpiresAt: expiresAt,
	}
	m.mu.Unlock()

	return token, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.lYKp_Iuf
// VA: 0x73b080
// Evidence: lookup in map under RLock; if time.Now().After(session.ExpiresAt), acquires Lock and deletes token
// Confidence: HIGH
func (m *SessionManager) GetSession(token string) (Session, bool) {
	m.mu.RLock()
	sess, exists := m.sessions[token]
	m.mu.RUnlock()

	if !exists {
		return Session{}, false
	}

	// Lazy expiration check matching binary VA 0x73b2c9
	now := m.clock.Now()
	if now.After(sess.ExpiresAt) {
		m.mu.Lock()
		// Double check under write lock
		if cur, ok := m.sessions[token]; ok && now.After(cur.ExpiresAt) {
			delete(m.sessions, token)
		}
		m.mu.Unlock()
		return Session{}, false
	}

	return sess, true
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.bjWkHiittd
// VA: 0x7409a0
// Evidence: explicit token deletion from session map under mutex lock (runtime.mapdelete_faststr)
// Confidence: HIGH
func (m *SessionManager) RevokeSession(token string) {
	m.mu.Lock()
	delete(m.sessions, token)
	m.mu.Unlock()
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.cFpPBbFet.func1
// VA: 0x73a580
// Evidence: iterates session map, deletes all tokens where session.Username == expiredUser.Username
// Confidence: HIGH
func (m *SessionManager) RevokeUserSessions(username string) int {
	m.mu.Lock()
	defer m.mu.Unlock()

	revoked := 0
	for token, sess := range m.sessions {
		if sess.Username == username {
			delete(m.sessions, token)
			revoked++
		}
	}
	return revoked
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: returns active token count for user (used for testing and diagnostics)
// Confidence: N/A
func (m *SessionManager) CountUserSessions(username string) int {
	m.mu.RLock()
	defer m.mu.RUnlock()

	count := 0
	for _, sess := range m.sessions {
		if sess.Username == username {
			count++
		}
	}
	return count
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.cFpPBbFet
// VA: 0x73a500
// Evidence: spawns 1-minute ticker worker checking UsersStore and revoking expired user tokens
// Confidence: HIGH
func (m *SessionManager) StartExpiryWorker(stopCh <-chan struct{}, usersStore *storage.UsersStore, interval time.Duration) {
	if interval <= 0 {
		interval = DefaultSweepInterval
	}
	ticker := time.NewTicker(interval)

	go func() {
		defer ticker.Stop()
		for {
			select {
			case <-stopCh:
				return
			case <-ticker.C:
				m.SweepExpiredUsers(usersStore)
			}
		}
	}()
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.cFpPBbFet.func1
// VA: 0x73a580
// Evidence: checks user.ExpiresAt against time.Now(), revokes tokens, logs eviction notice
// Confidence: HIGH
func (m *SessionManager) SweepExpiredUsers(usersStore *storage.UsersStore) int {
	if usersStore == nil {
		return 0
	}

	users := usersStore.ListUsers()
	now := m.clock.Now()
	totalRevoked := 0

	for _, user := range users {
		if !user.ExpiresAt.IsZero() && now.After(user.ExpiresAt) {
			revoked := m.RevokeUserSessions(user.Username)
			if revoked > 0 {
				log.Printf("[User] Account %s expired, tokens revoked and sessions kicked", user.Username)
				totalRevoked += revoked
			}
		}
	}

	return totalRevoked
}
