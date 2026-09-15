// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol:
//   - main.ltOjwqsMl5q8 (VA: 0x73dd00, size: 2752 bytes) -> Login verification, expiration check, credential evaluation
//   - main.lYKp_Iuf (VA: 0x73b080, size: 1120 bytes) -> Token validation, noAuth bypass, lazy eviction, user expiry check
//   - main.bjWkHiittd (VA: 0x7409a0, size: 1440 bytes) -> Logout and token revocation
//   - main.gJ0OHScnGnWZ (VA: 0x73f100, size: 2816 bytes) -> Sanitized user profile resolution without password/salt
// Evidence:
//   - Error strings: "Username and password are required", "Invalid username or password", "账号已到期，请联系管理员延时", "Unauthorized"
//   - JSON response schema: {"assigned_devices": [...], "role": "...", "token": "...", "username": "..."}
//   - Zero net/http handlers in this core package (HTTP layer deferred to Phase 2C.3)
// Confidence: HIGH

package auth

import (
	"errors"
	"strings"
	"time"

	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

var (
	ErrCredentialsRequired = errors.New("Username and password are required")
	ErrInvalidCredentials  = errors.New("Invalid username or password")
	ErrAccountExpired      = errors.New("\u8d26\u53f7\u5df2\u5230\u671f\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\u5ef6\u65f6")
	ErrUnauthorized        = errors.New("Unauthorized")
)

// LoginResult represents the successful JSON response payload of the login endpoint.
// Confirmed via VA 0x73e526 - 0x73e6a4.
type LoginResult struct {
	AssignedDevices []string `json:"assigned_devices"`
	Role            string   `json:"role"`
	Token           string   `json:"token"`
	Username        string   `json:"username"`
}

// Authenticator orchestrates authentication and session management matching original binary semantics.
type Authenticator struct {
	usersStore *storage.UsersStore
	sessionMgr *session.SessionManager
	noAuth     bool
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: constructs Authenticator with usersStore and sessionMgr
// Confidence: N/A
func NewAuthenticator(usersStore *storage.UsersStore, sessionMgr *session.SessionManager, noAuth bool) *Authenticator {
	return &Authenticator{
		usersStore: usersStore,
		sessionMgr: sessionMgr,
		noAuth:     noAuth,
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ltOjwqsMl5q8
// VA: 0x73dd00
// Evidence: trims username, verifies required fields, checks user.ExpiresAt, verifies SHA256(password+salt), issues token
// Confidence: HIGH
func (a *Authenticator) AuthenticateCredentials(username, password string) (*LoginResult, error) {
	trimmedUser := strings.TrimSpace(username)
	if trimmedUser == "" || password == "" {
		return nil, ErrCredentialsRequired
	}

	user, exists := a.usersStore.GetUser(trimmedUser)
	if !exists {
		return nil, ErrInvalidCredentials
	}

	// User account expiration check (VA 0x73e263)
	now := time.Now()
	if !user.ExpiresAt.IsZero() && now.After(user.ExpiresAt) {
		return nil, ErrAccountExpired
	}

	// Password verification using shared verified primitive (VA 0x73e28d)
	computedHash := storage.HashPassword(password, user.Salt)
	if computedHash != user.Password {
		return nil, ErrInvalidCredentials
	}

	// Session token issuance (VA 0x73e2c0)
	token, err := a.sessionMgr.CreateSession(user.Username)
	if err != nil {
		return nil, err
	}

	devices := user.AssignedDevices
	if devices == nil {
		devices = []string{}
	}

	return &LoginResult{
		AssignedDevices: devices,
		Role:            user.Role,
		Token:           token,
		Username:        user.Username,
	}, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.lYKp_Iuf
// VA: 0x73b080
// Evidence: checks noAuth flag/env, resolves token from sessionMap with lazy eviction, checks user.ExpiresAt
// Confidence: HIGH
func (a *Authenticator) ValidateToken(token string) (string, error) {
	// Global auth bypass evaluation (VA 0x73b09d - 0x73b0cb)
	if a.noAuth {
		return "admin", nil
	}

	if token == "" {
		return "", ErrUnauthorized
	}

	// Token lookup with lazy TTL eviction (VA 0x73b230 - 0x73b2d0)
	sess, ok := a.sessionMgr.GetSession(token)
	if !ok {
		return "", ErrUnauthorized
	}

	// User account lookup & expiration check (VA 0x73b346 - 0x73b448)
	user, exists := a.usersStore.GetUser(sess.Username)
	if !exists {
		return "", ErrUnauthorized
	}

	if !user.ExpiresAt.IsZero() && time.Now().After(user.ExpiresAt) {
		return "", ErrUnauthorized
	}

	return user.Username, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.bjWkHiittd
// VA: 0x7409a0
// Evidence: deletes token from sessionMap under mutex lock (runtime.mapdelete_faststr)
// Confidence: HIGH
func (a *Authenticator) Logout(token string) {
	if token != "" {
		a.sessionMgr.RevokeSession(token)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.gJ0OHScnGnWZ
// VA: 0x73f100
// Evidence: fetches user from store, omits password and salt, returns sanitized profile
// Confidence: HIGH
func (a *Authenticator) GetUserProfile(username string) (*types.User, error) {
	user, exists := a.usersStore.GetUser(username)
	if !exists {
		return nil, ErrUnauthorized
	}

	// Sanitized copy without password or salt
	clean := user
	clean.Password = ""
	clean.Salt = ""
	if clean.AssignedDevices == nil {
		clean.AssignedDevices = []string{}
	}
	return &clean, nil
}
