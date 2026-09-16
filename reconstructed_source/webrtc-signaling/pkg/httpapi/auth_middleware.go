// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Authentication token extraction and middleware evaluation
// Confidence: HIGH

package httpapi

import (
	"net/http"
	"strings"

	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.lYKp_Iuf (Linux) / main.mLWT3o (Windows)
// VA: 0x73b080 (Linux) / 0x140344260 (Windows)
// Whole Function VA: 0x73b080 (Linux) / 0x140344260 (Windows)
// Evidence VA Range: 0x73b0ed-0x73b1b6 (Linux) / 0x1403442cd-0x1403443a0 (Windows)
// Phase 2C.2 Shared Range: 0x73b1ca-0x73b4a5 (Linux) / 0x1403443b7-0x1403446aa (Windows)
// Excluded Behavior: In-memory session store map lookup runtime.mapaccess2_faststr and TTL expiration check (pkg/session, pkg/auth)
// Evidence: AUTH_TOKEN_SOURCE_MATRIX.json, AUTH_HTTP_FUNCTION_SLICES.json
// Confidence: HIGH
func ExtractToken(r *http.Request) string {
	authHeader := r.Header.Get("Authorization")
	token := ""
	if authHeader != "" {
		parts := strings.Split(authHeader, " ")
		if len(parts) == 2 && strings.ToLower(parts[0]) == "bearer" {
			token = parts[1]
		} else {
			token = authHeader
		}
	}
	if token == "" {
		token = r.URL.Query().Get("token")
	}
	if token == "" {
		if cookie, err := r.Cookie("token"); err == nil {
			token = cookie.Value
		}
	}
	return token
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Request authentication adapter connecting HTTP token extraction to Authenticator
// Source Behavior: Extracts token via ExtractToken and delegates validation to Authenticator
// Confidence: HIGH
func (s *Server) Authenticate(r *http.Request) (*types.User, error) {
	token := ExtractToken(r)
	username, err := s.auth.ValidateToken(token)
	if err != nil {
		return nil, err
	}
	return s.auth.GetUserProfile(username)
}
