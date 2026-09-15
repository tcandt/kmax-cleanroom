// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Reconstructed HTTP request handlers for the four core auth endpoints
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"errors"
	"net/http"
	"time"

	"cloudphone-signaling/pkg/auth"
)

// LoginRequest defines the expected JSON body for /api/login.
type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// UserProfileResponse defines the exact 10-field JSON response structure for /api/me.
type UserProfileResponse struct {
	AIConfig         interface{} `json:"ai_config"`
	AssignedDevices  []string    `json:"assigned_devices"`
	ExpiresAt        time.Time   `json:"expires_at"`
	ForbidAudio      bool        `json:"forbid_audio"`
	ForbidBitrate    bool        `json:"forbid_bitrate"`
	ForbidFPS        bool        `json:"forbid_fps"`
	ForbidResolution bool        `json:"forbid_resolution"`
	Role             string      `json:"role"`
	Settings         interface{} `json:"settings"`
	Username         string      `json:"username"`
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.ltOjwqsMl5q8 (Linux) / main.u4r2NulQUnF (Windows)
// VA: 0x73dd00 (Linux) / 0x140346f00 (Windows)
// Whole Function VA: 0x73dd00 (Linux) / 0x140346f00 (Windows)
// Evidence VA Range: 0x73dd23-0x73df7f, 0x73e2d1-0x73e790 (Linux) / 0x140346f23-0x1403471bf, 0x1403474f1-0x1403479b0 (Windows)
// Phase 2C.2 Shared Range: 0x73df80-0x73e2d0 (Linux) / 0x1403471c0-0x1403474f0 (Windows)
// Excluded Behavior: Storage user lookup and SHA256 password hash comparison (pkg/auth)
// Evidence: AUTH_HTTP_FUNCTION_SLICES.json, AUTH_ROUTE_METHOD_MATRIX.json, LOGIN_REQUEST_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleLogin(w http.ResponseWriter, r *http.Request) {
	SetCORS(w, "POST, OPTIONS")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}
	if r.Method != http.MethodPost {
		WriteError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	var req LoginRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		WriteError(w, http.StatusBadRequest, "Invalid JSON")
		return
	}

	if req.Username == "" || req.Password == "" {
		WriteError(w, http.StatusBadRequest, "Username and password are required")
		return
	}

	result, err := s.auth.AuthenticateCredentials(req.Username, req.Password)
	if err != nil {
		if errors.Is(err, auth.ErrAccountExpired) {
			WriteError(w, http.StatusForbidden, "\u8d26\u53f7\u5df2\u5230\u671f\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\u5ef6\u65f6")
			return
		}
		WriteError(w, http.StatusUnauthorized, "Invalid username or password")
		return
	}

	_ = WriteJSON(w, http.StatusOK, result)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.bjWkHiittd (Linux) / main.blPINsMc3 (Windows)
// VA: 0x7409a0 (Linux) / 0x140349bc0 (Windows)
// Whole Function VA: 0x7409a0 (Linux) / 0x140349bc0 (Windows)
// Evidence VA Range: 0x7409c0-0x740b1f, 0x740be1-0x740f10 (Linux) / 0x140349be0-0x140349d3f, 0x140349e01-0x14034a130 (Windows)
// Phase 2C.2 Shared Range: 0x740b20-0x740be0 (Linux) / 0x140349d40-0x140349e00 (Windows)
// Excluded Behavior: Session map deletion and mutex handling (pkg/session, pkg/auth)
// Evidence: AUTH_HTTP_FUNCTION_SLICES.json, AUTH_ROUTE_METHOD_MATRIX.json, AUTH_HTTP_RESPONSE_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleLogout(w http.ResponseWriter, r *http.Request) {
	SetCORS(w, "POST, OPTIONS")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	token := ExtractToken(r)
	if token != "" {
		s.auth.Logout(token)
	}

	_ = WriteJSON(w, http.StatusOK, map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.bwvBd1LWVr (Linux) / main.waSrU4iH (Windows)
// VA: 0x73ec40 (Linux) / 0x140347e60 (Windows)
// Whole Function VA: 0x73ec40 (Linux) / 0x140347e60 (Windows)
// Evidence VA Range: 0x73ec60-0x73f0d0 (Linux) / 0x140347e80-0x1403482f0 (Windows)
// Phase 2C.2 Shared Range: NONE
// Excluded Behavior: NONE (pure HTTP endpoint handler)
// Evidence: AUTH_HTTP_FUNCTION_SLICES.json, AUTH_ROUTE_METHOD_MATRIX.json, AUTH_HTTP_RESPONSE_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleAuthStatus(w http.ResponseWriter, r *http.Request) {
	SetCORS(w, "GET, OPTIONS")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_ = WriteJSON(w, http.StatusOK, map[string]bool{"noAuth": s.noAuth})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.gJ0OHScnGnWZ (Linux) / main.k0Ckv2FQUr (Windows)
// VA: 0x73f100 (Linux) / 0x140348320 (Windows)
// Whole Function VA: 0x73f100 (Linux) / 0x140348320 (Windows)
// Evidence VA Range: 0x73f120-0x73f290, 0x73f291-0x73fbd0 (Linux) / 0x140348340-0x1403484b0, 0x1403484b1-0x140348df0 (Windows)
// Phase 2C.2 Shared Range: NONE
// Excluded Behavior: User profile sanitization in storage (pkg/auth)
// Evidence: AUTH_HTTP_FUNCTION_SLICES.json, AUTH_ROUTE_METHOD_MATRIX.json, AUTH_HTTP_RESPONSE_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleMe(w http.ResponseWriter, r *http.Request) {
	SetCORS(w, "GET, OPTIONS")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	user, err := s.Authenticate(r)
	if err != nil {
		WriteError(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	resp := UserProfileResponse{
		AIConfig:         user.AIConfig,
		AssignedDevices:  user.AssignedDevices,
		ExpiresAt:        user.ExpiresAt,
		ForbidAudio:      user.ForbidAudio,
		ForbidBitrate:    user.ForbidBitrate,
		ForbidFPS:        user.ForbidFPS,
		ForbidResolution: user.ForbidResolution,
		Role:             user.Role,
		Settings:         user.Settings,
		Username:         user.Username,
	}

	_ = WriteJSON(w, http.StatusOK, resp)
}
