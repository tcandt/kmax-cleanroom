// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Unit tests for Device REST endpoints
// Confidence: HIGH

package httpapi

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Helper to login a user and return token string
// Source Behavior: Performs POST /api/login and extracts token
// Confidence: HIGH
func loginTestUser(t *testing.T, server *Server, username, password string) string {
	body, _ := json.Marshal(map[string]string{"username": username, "password": password})
	req := httptest.NewRequest(http.MethodPost, "/api/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	server.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Login failed for %s: %d", username, w.Code)
	}
	var resp auth.LoginResult
	_ = json.Unmarshal(w.Body.Bytes(), &resp)
	return resp.Token
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests GET /devices with empty and populated registry across roles
// Source Behavior: Validates empty array serialization and assignment filtering
// Confidence: HIGH
func TestHandleDevices(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	adminTok := loginTestUser(t, server, "admin", "admin123")
	userTok := loginTestUser(t, server, "test_user", "user123")

	// 1. Empty registry with admin
	req := httptest.NewRequest(http.MethodGet, "/devices", nil)
	req.Header.Set("Authorization", "Bearer "+adminTok)
	w := httptest.NewRecorder()
	server.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Expected 200, got %d", w.Code)
	}
	if w.Body.String() != "[]\n" {
		t.Fatalf("Expected '[]\\n', got %q", w.Body.String())
	}

	// 2. Unauthenticated request
	reqUnauth := httptest.NewRequest(http.MethodGet, "/devices", nil)
	wUnauth := httptest.NewRecorder()
	server.ServeHTTP(wUnauth, reqUnauth)
	if wUnauth.Code != http.StatusUnauthorized {
		t.Fatalf("Expected 401, got %d", wUnauth.Code)
	}

	// 3. Register two devices: dev1 and dev2
	server.GetDeviceRegistry().RegisterDevice("dev1", map[string]string{"model": "Pixel"}, true)
	server.GetDeviceRegistry().RegisterDevice("dev2", map[string]string{"model": "Galaxy"}, true)

	// Admin should see both devices
	wAdmin := httptest.NewRecorder()
	server.ServeHTTP(wAdmin, req)
	if wAdmin.Code != http.StatusOK {
		t.Fatalf("Expected 200, got %d", wAdmin.Code)
	}
	var adminDevs []types.DeviceDTO
	_ = json.Unmarshal(wAdmin.Body.Bytes(), &adminDevs)
	if len(adminDevs) != 2 {
		t.Fatalf("Admin expected 2 devices, got %d", len(adminDevs))
	}

	// Normal user (assigned dev1) should see only dev1
	reqUser := httptest.NewRequest(http.MethodGet, "/devices", nil)
	reqUser.Header.Set("Authorization", "Bearer "+userTok)
	wUser := httptest.NewRecorder()
	server.ServeHTTP(wUser, reqUser)
	if wUser.Code != http.StatusOK {
		t.Fatalf("Expected 200, got %d", wUser.Code)
	}
	var userDevs []types.DeviceDTO
	_ = json.Unmarshal(wUser.Body.Bytes(), &userDevs)
	if len(userDevs) != 1 || userDevs[0].DeviceID != "dev1" {
		t.Fatalf("User expected 1 device (dev1), got %+v", userDevs)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests DELETE /api/devices/{id} lifecycle, permissions, and guard checks
// Source Behavior: Validates 405 on GET, 403 on non-admin, 409 on online, 200 on offline
// Confidence: HIGH
func TestHandleDeviceDelete(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	adminTok := loginTestUser(t, server, "admin", "admin123")
	userTok := loginTestUser(t, server, "test_user", "user123")

	server.GetDeviceRegistry().RegisterDevice("dev1", nil, true)

	// 1. Wrong method GET on /api/devices/dev1 -> 405
	reqGet := httptest.NewRequest(http.MethodGet, "/api/devices/dev1", nil)
	reqGet.Header.Set("Authorization", "Bearer "+adminTok)
	wGet := httptest.NewRecorder()
	server.ServeHTTP(wGet, reqGet)
	if wGet.Code != http.StatusMethodNotAllowed {
		t.Fatalf("Expected 405 on GET, got %d", wGet.Code)
	}

	// 2. Normal user tries DELETE -> 403 Forbidden
	reqUserDel := httptest.NewRequest(http.MethodDelete, "/api/devices/dev1", nil)
	reqUserDel.Header.Set("Authorization", "Bearer "+userTok)
	wUserDel := httptest.NewRecorder()
	server.ServeHTTP(wUserDel, reqUserDel)
	if wUserDel.Code != http.StatusForbidden {
		t.Fatalf("Expected 403 on non-admin DELETE, got %d", wUserDel.Code)
	}

	// 3. Admin tries DELETE while device is online -> 409 Conflict
	reqDel := httptest.NewRequest(http.MethodDelete, "/api/devices/dev1", nil)
	reqDel.Header.Set("Authorization", "Bearer "+adminTok)
	wDelOnline := httptest.NewRecorder()
	server.ServeHTTP(wDelOnline, reqDel)
	if wDelOnline.Code != http.StatusConflict {
		t.Fatalf("Expected 409 on online device, got %d", wDelOnline.Code)
	}

	// 4. Disconnect device, then DELETE -> 200 OK {"status":"deleted"}
	server.GetDeviceRegistry().DisconnectDevice("dev1")
	wDelOffline := httptest.NewRecorder()
	server.ServeHTTP(wDelOffline, reqDel)
	if wDelOffline.Code != http.StatusOK {
		t.Fatalf("Expected 200 on offline device, got %d", wDelOffline.Code)
	}
	if wDelOffline.Body.String() != "{\"status\":\"deleted\"}\n" {
		t.Fatalf("Expected '{\"status\":\"deleted\"}\\n', got %q", wDelOffline.Body.String())
	}

	// 5. DELETE again -> 404 Device not found
	wDel404 := httptest.NewRecorder()
	server.ServeHTTP(wDel404, reqDel)
	if wDel404.Code != http.StatusNotFound {
		t.Fatalf("Expected 404 on deleted device, got %d", wDel404.Code)
	}
}
