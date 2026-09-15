// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: unit tests for authenticator credential validation, user expiry, token resolution, and noAuth bypass
// Confidence: N/A

package auth

import (
	"path/filepath"
	"testing"
	"time"

	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

func TestAuthenticatorCredentials(t *testing.T) {
	tmpDir := t.TempDir()
	usersStore := storage.NewUsersStore(filepath.Join(tmpDir, "users.json"))
	if err := usersStore.LoadOrCreate(); err != nil {
		t.Fatalf("LoadOrCreate failed: %v", err)
	}

	// Add test users
	salt := storage.GenerateSalt()
	usersStore.SetUser(types.User{
		Username:        "charlie",
		Password:        storage.HashPassword("secret123", salt),
		Salt:            salt,
		Role:            "user",
		AssignedDevices: []string{"dev-100"},
		ExpiresAt:       time.Time{},
	})

	usersStore.SetUser(types.User{
		Username:        "expired",
		Password:        storage.HashPassword("expired123", salt),
		Salt:            salt,
		Role:            "user",
		AssignedDevices: []string{},
		ExpiresAt:       time.Now().Add(-1 * time.Hour), // in the past
	})

	sm := session.NewSessionManager(nil)
	auth := NewAuthenticator(usersStore, sm, false)

	// 1. Valid login
	res, err := auth.AuthenticateCredentials("charlie", "secret123")
	if err != nil {
		t.Fatalf("AuthenticateCredentials failed: %v", err)
	}
	if res.Username != "charlie" || res.Role != "user" || len(res.Token) != 64 {
		t.Errorf("unexpected login result: %+v", res)
	}

	// 2. Invalid password
	_, err = auth.AuthenticateCredentials("charlie", "wrongpass")
	if err != ErrInvalidCredentials {
		t.Errorf("expected ErrInvalidCredentials, got %v", err)
	}

	// 3. Unknown user
	_, err = auth.AuthenticateCredentials("unknown", "secret123")
	if err != ErrInvalidCredentials {
		t.Errorf("expected ErrInvalidCredentials, got %v", err)
	}

	// 4. Empty fields
	_, err = auth.AuthenticateCredentials("", "secret123")
	if err != ErrCredentialsRequired {
		t.Errorf("expected ErrCredentialsRequired for empty username, got %v", err)
	}
	_, err = auth.AuthenticateCredentials("charlie", "")
	if err != ErrCredentialsRequired {
		t.Errorf("expected ErrCredentialsRequired for empty password, got %v", err)
	}

	// 5. Expired user
	_, err = auth.AuthenticateCredentials("expired", "expired123")
	if err != ErrAccountExpired {
		t.Errorf("expected ErrAccountExpired, got %v", err)
	}

	// 6. Token validation
	user, err := auth.ValidateToken(res.Token)
	if err != nil || user != "charlie" {
		t.Errorf("expected token validation to return charlie, got %s, err: %v", user, err)
	}

	// 7. Token validation with invalid token
	_, err = auth.ValidateToken("invalid_token")
	if err != ErrUnauthorized {
		t.Errorf("expected ErrUnauthorized, got %v", err)
	}

	// 8. Logout
	auth.Logout(res.Token)
	_, err = auth.ValidateToken(res.Token)
	if err != ErrUnauthorized {
		t.Errorf("expected ErrUnauthorized after logout, got %v", err)
	}
}

func TestAuthBypassMode(t *testing.T) {
	tmpDir := t.TempDir()
	usersStore := storage.NewUsersStore(filepath.Join(tmpDir, "users.json"))
	_ = usersStore.LoadOrCreate()

	sm := session.NewSessionManager(nil)
	bypassAuth := NewAuthenticator(usersStore, sm, true) // noAuth = true

	user, err := bypassAuth.ValidateToken("")
	if err != nil || user != "admin" {
		t.Errorf("expected noAuth mode to return admin with nil error, got %s, %v", user, err)
	}
}
