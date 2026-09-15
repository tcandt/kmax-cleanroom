// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: HTTP server routing for authentication endpoints using Go standard library net/http.ServeMux
// Confidence: HIGH

package httpapi

import (
	"net/http"

	"cloudphone-signaling/pkg/auth"
)

// Server encapsulates the HTTP handler router and associated auth/session services.
type Server struct {
	mux    *http.ServeMux
	auth   *auth.Authenticator
	noAuth bool
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Instantiates Server and registers HTTP routes on standard library ServeMux
// Source Behavior: Registers /api/login, /api/logout, /api/auth-status, /api/me on ServeMux
// Confidence: HIGH
func NewServer(authenticator *auth.Authenticator, noAuth bool) *Server {
	s := &Server{
		mux:    http.NewServeMux(),
		auth:   authenticator,
		noAuth: noAuth,
	}

	// Register the four core auth routes matching original binary
	s.mux.HandleFunc("/api/login", s.HandleLogin)
	s.mux.HandleFunc("/api/logout", s.HandleLogout)
	s.mux.HandleFunc("/api/auth-status", s.HandleAuthStatus)
	s.mux.HandleFunc("/api/me", s.HandleMe)

	return s
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Implements http.Handler interface by delegating to internal ServeMux
// Source Behavior: Delegates to mux.ServeHTTP(w, r)
// Confidence: HIGH
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	s.mux.ServeHTTP(w, r)
}
