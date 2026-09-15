// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Unit tests for reconstructed HTTP API endpoints and middleware
// Confidence: HIGH

package httpapi

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
	"time"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Test fixture setup helper for HTTP tests
// Source Behavior: Initializes UsersStore, SessionManager, Authenticator, and HTTP Server
// Confidence: HIGH
func setupTestServer(t *testing.T) (*Server, func()) {
	tmpDir, err := os.MkdirTemp("", "httpapi_test_*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}

	usersFilePath := filepath.Join(tmpDir, "users.json")
	usersStore := storage.NewUsersStore(usersFilePath)
	_ = usersStore.LoadOrCreate()
	salt := "test_salt_12345"

	// Create test users
	_ = usersStore.SetUser(types.User{
		Username:        "admin",
		Password:        storage.HashPassword("admin123", salt),
		Salt:            salt,
		Role:            "admin",
		AssignedDevices: []string{"*"},
	})
	_ = usersStore.SetUser(types.User{
		Username:        "test_user",
		Password:        storage.HashPassword("user123", salt),
		Salt:            salt,
		Role:            "user",
		AssignedDevices: []string{"dev1"},
	})
	_ = usersStore.SetUser(types.User{
		Username:        "expired_user",
		Password:        storage.HashPassword("expired123", salt),
		Salt:            salt,
		Role:            "user",
		AssignedDevices: []string{},
		ExpiresAt:       time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC),
	})

	sm := session.NewSessionManager(session.RealClock{})
	authenticator := auth.NewAuthenticator(usersStore, sm, false)
	server := NewServer(authenticator, false)

	cleanup := func() {
		_ = os.RemoveAll(tmpDir)
	}

	return server, cleanup
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests successful login and response JSON schema
// Source Behavior: POST /api/login with valid admin credentials returns 200 OK
// Confidence: HIGH
func TestHandleLogin_Success(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	body, _ := json.Marshal(map[string]string{"username": "admin", "password": "admin123"})
	req := httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	server.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Expected status 200, got %d: %s", w.Code, w.Body.String())
	}

	var resp auth.LoginResult
	if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
		t.Fatalf("Failed to parse login response: %v", err)
	}
	if resp.Username != "admin" || resp.Role != "admin" || len(resp.Token) != 64 {
		t.Fatalf("Invalid login result: %+v", resp)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests login with invalid credentials and method rejection
// Source Behavior: GET returns 405; invalid credentials return 401; expired user returns 403
// Confidence: HIGH
func TestHandleLogin_Errors(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	// GET method not allowed
	reqGet := httptest.NewRequest(http.MethodGet, "/api/login", nil)
	wGet := httptest.NewRecorder()
	server.ServeHTTP(wGet, reqGet)
	if wGet.Code != http.StatusMethodNotAllowed {
		t.Errorf("Expected 405 on GET, got %d", wGet.Code)
	}

	// Missing credentials
	reqMissing := httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader([]byte("{}")))
	wMissing := httptest.NewRecorder()
	server.ServeHTTP(wMissing, reqMissing)
	if wMissing.Code != http.StatusBadRequest {
		t.Errorf("Expected 400 on missing credentials, got %d", wMissing.Code)
	}

	// Invalid password
	bodyBadPwd, _ := json.Marshal(map[string]string{"username": "admin", "password": "wrongpassword"})
	reqBad := httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader(bodyBadPwd))
	wBad := httptest.NewRecorder()
	server.ServeHTTP(wBad, reqBad)
	if wBad.Code != http.StatusUnauthorized {
		t.Errorf("Expected 401 on bad password, got %d", wBad.Code)
	}

	// Expired user
	bodyExp, _ := json.Marshal(map[string]string{"username": "expired_user", "password": "expired123"})
	reqExp := httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader(bodyExp))
	wExp := httptest.NewRecorder()
	server.ServeHTTP(wExp, reqExp)
	if wExp.Code != http.StatusForbidden {
		t.Errorf("Expected 403 on expired user, got %d", wExp.Code)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests token extraction and precedence rules on /api/me
// Source Behavior: Tests Bearer casing, query fallback, and header precedence over query
// Confidence: HIGH
func TestHandleMe_TokenPrecedence(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	// Login admin
	bodyAdmin, _ := json.Marshal(map[string]string{"username": "admin", "password": "admin123"})
	wAdmin := httptest.NewRecorder()
	server.ServeHTTP(wAdmin, httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader(bodyAdmin)))
	var resAdmin auth.LoginResult
	_ = json.Unmarshal(wAdmin.Body.Bytes(), &resAdmin)

	// Login test_user
	bodyUser, _ := json.Marshal(map[string]string{"username": "test_user", "password": "user123"})
	wUser := httptest.NewRecorder()
	server.ServeHTTP(wUser, httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader(bodyUser)))
	var resUser auth.LoginResult
	_ = json.Unmarshal(wUser.Body.Bytes(), &resUser)

	// 1. Valid Canonical Bearer
	req1 := httptest.NewRequest(http.MethodGet, "/api/me", nil)
	req1.Header.Set("Authorization", "Bearer "+resAdmin.Token)
	w1 := httptest.NewRecorder()
	server.ServeHTTP(w1, req1)
	if w1.Code != http.StatusOK {
		t.Errorf("Canonical Bearer failed: %d", w1.Code)
	}

	// 2. Mixed-case bearer
	req2 := httptest.NewRequest(http.MethodGet, "/api/me", nil)
	req2.Header.Set("Authorization", "bEaReR "+resAdmin.Token)
	w2 := httptest.NewRecorder()
	server.ServeHTTP(w2, req2)
	if w2.Code != http.StatusOK {
		t.Errorf("Mixed-case bearer failed: %d", w2.Code)
	}

	// 3. Query fallback (?token=)
	req3 := httptest.NewRequest(http.MethodGet, "/api/me?token="+resAdmin.Token, nil)
	w3 := httptest.NewRecorder()
	server.ServeHTTP(w3, req3)
	if w3.Code != http.StatusOK {
		t.Errorf("Query fallback failed: %d", w3.Code)
	}

	// 4. Header precedence over query (Header admin, query test_user) -> should be admin
	req4 := httptest.NewRequest(http.MethodGet, "/api/me?token="+resUser.Token, nil)
	req4.Header.Set("Authorization", "Bearer "+resAdmin.Token)
	w4 := httptest.NewRecorder()
	server.ServeHTTP(w4, req4)
	if w4.Code != http.StatusOK {
		t.Errorf("Precedence request failed: %d", w4.Code)
	}
	var prof4 UserProfileResponse
	_ = json.Unmarshal(w4.Body.Bytes(), &prof4)
	if prof4.Username != "admin" {
		t.Errorf("Expected header user 'admin' to take precedence, got %s", prof4.Username)
	}

	// 5. Invalid header with valid query -> should fail (header evaluated first, query ignored)
	req5 := httptest.NewRequest(http.MethodGet, "/api/me?token="+resAdmin.Token, nil)
	req5.Header.Set("Authorization", "Bearer invalidtoken")
	w5 := httptest.NewRecorder()
	server.ServeHTTP(w5, req5)
	if w5.Code != http.StatusUnauthorized {
		t.Errorf("Expected 401 when invalid bearer overrides valid query, got %d", w5.Code)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests logout idempotency and auth-status endpoint
// Source Behavior: Logout returns 200 with status:success unconditionally; auth-status returns noAuth:false
// Confidence: HIGH
func TestHandleLogout_And_AuthStatus(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	// Auth status
	wStatus := httptest.NewRecorder()
	server.ServeHTTP(wStatus, httptest.NewRequest(http.MethodGet, "/api/auth-status", nil))
	if wStatus.Code != http.StatusOK {
		t.Fatalf("auth-status failed: %d", wStatus.Code)
	}

	// Logout with no token -> 200 OK idempotent
	wLg1 := httptest.NewRecorder()
	server.ServeHTTP(wLg1, httptest.NewRequest(http.MethodPost, "/api/logout", nil))
	if wLg1.Code != http.StatusOK {
		t.Fatalf("logout without token failed: %d", wLg1.Code)
	}

	// OPTIONS preflight check
	wOpt := httptest.NewRecorder()
	server.ServeHTTP(wOpt, httptest.NewRequest(http.MethodOptions, "/api/login", nil))
	if wOpt.Code != http.StatusOK {
		t.Fatalf("OPTIONS preflight failed: %d", wOpt.Code)
	}
	if wOpt.Header().Get("Access-Control-Allow-Origin") != "*" {
		t.Errorf("Missing CORS header on OPTIONS")
	}
}
