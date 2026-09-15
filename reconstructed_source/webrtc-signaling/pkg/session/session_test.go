// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: unit tests for session manager, token generation, lazy expiry, and user session revocation
// Confidence: N/A

package session

import (
	"regexp"
	"testing"
	"time"
)

func TestTokenGenerator(t *testing.T) {
	token, err := GenerateToken()
	if err != nil {
		t.Fatalf("GenerateToken failed: %v", err)
	}

	if len(token) != 64 {
		t.Errorf("expected token length 64, got %d", len(token))
	}

	matched, _ := regexp.MatchString("^[0-9a-f]{64}$", token)
	if !matched {
		t.Errorf("token does not match lowercase hex regex: %s", token)
	}

	token2, _ := GenerateToken()
	if token == token2 {
		t.Errorf("expected consecutive tokens to be unique, got identical: %s", token)
	}
}

func TestSessionManagerLifecycle(t *testing.T) {
	baseTime := time.Date(2026, 9, 15, 12, 0, 0, 0, time.UTC)
	mockClock := NewMockClock(baseTime)
	sm := NewSessionManager(mockClock)

	// 1. Create session
	token, err := sm.CreateSession("alice")
	if err != nil {
		t.Fatalf("CreateSession failed: %v", err)
	}

	// 2. Lookup valid session
	sess, ok := sm.GetSession(token)
	if !ok {
		t.Fatalf("expected session to be found")
	}
	if sess.Username != "alice" {
		t.Errorf("expected username alice, got %s", sess.Username)
	}
	expectedExpiry := baseTime.Add(24 * time.Hour)
	if !sess.ExpiresAt.Equal(expectedExpiry) {
		t.Errorf("expected expiry %v, got %v", expectedExpiry, sess.ExpiresAt)
	}

	// 3. Fast forward clock 23h (still valid)
	mockClock.Add(23 * time.Hour)
	if _, ok := sm.GetSession(token); !ok {
		t.Errorf("session should still be valid after 23 hours")
	}

	// 4. Fast forward clock another 2h (25h total -> expired)
	mockClock.Add(2 * time.Hour)
	if _, ok := sm.GetSession(token); ok {
		t.Errorf("session should be expired after 25 hours")
	}

	// 5. Verify lazy eviction deleted token from map
	if _, exists := sm.sessions[token]; exists {
		t.Errorf("token should have been lazily evicted from memory map")
	}
}

func TestMultipleSessionsPerUser(t *testing.T) {
	sm := NewSessionManager(nil)

	tokenA, _ := sm.CreateSession("bob")
	tokenB, _ := sm.CreateSession("bob")

	if tokenA == tokenB {
		t.Fatalf("expected different tokens for same user")
	}

	if sm.CountUserSessions("bob") != 2 {
		t.Errorf("expected 2 active sessions for bob, got %d", sm.CountUserSessions("bob"))
	}

	// Revoke tokenA
	sm.RevokeSession(tokenA)

	if _, ok := sm.GetSession(tokenA); ok {
		t.Errorf("tokenA should be revoked")
	}
	if _, ok := sm.GetSession(tokenB); !ok {
		t.Errorf("tokenB should still be valid")
	}

	if sm.CountUserSessions("bob") != 1 {
		t.Errorf("expected 1 active session for bob, got %d", sm.CountUserSessions("bob"))
	}
}
