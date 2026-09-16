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
	"cloudphone-signaling/pkg/devices"
)

// Server encapsulates the HTTP handler router and associated auth/session/device services.
type Server struct {
	mux       *http.ServeMux
	auth      *auth.Authenticator
	noAuth    bool
	deviceReg *devices.Registry
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Instantiates Server and registers HTTP routes on standard library ServeMux
// Source Behavior: Registers auth and device endpoints on ServeMux
// Confidence: HIGH
func NewServer(authenticator *auth.Authenticator, noAuth bool, deviceReg ...*devices.Registry) *Server {
	var dReg *devices.Registry
	if len(deviceReg) > 0 && deviceReg[0] != nil {
		dReg = deviceReg[0]
	} else {
		dReg = devices.NewRegistry()
	}

	s := &Server{
		mux:       http.NewServeMux(),
		auth:      authenticator,
		noAuth:    noAuth,
		deviceReg: dReg,
	}

	// Register auth routes matching original binary
	s.mux.HandleFunc("/api/login", s.HandleLogin)
	s.mux.HandleFunc("/api/logout", s.HandleLogout)
	s.mux.HandleFunc("/api/auth-status", s.HandleAuthStatus)
	s.mux.HandleFunc("/api/me", s.HandleMe)

	// Register device REST routes matching original binary
	s.mux.HandleFunc("/devices", s.HandleDevices)
	s.mux.HandleFunc("/api/devices/", s.HandleDeviceDelete)

	// Register user & admin REST routes matching original binary
	s.mux.HandleFunc("/api/admin/users", s.HandleAdminUsers)
	s.mux.HandleFunc("/api/admin/users/create", s.HandleAdminCreateUser)
	s.mux.HandleFunc("/api/admin/users/delete", s.HandleAdminDeleteUser)
	s.mux.HandleFunc("/api/admin/users/update", s.HandleAdminUpdateUser)
	s.mux.HandleFunc("/api/admin/users/update_note", s.HandleAdminUpdateNote)
	s.mux.HandleFunc("/api/admin/users/reset_password", s.HandleAdminResetPassword)
	s.mux.HandleFunc("/api/admin/users/rename", s.HandleAdminRenameUser)
	s.mux.HandleFunc("/api/admin/users/kick", s.HandleAdminKickUser)
	s.mux.HandleFunc("/api/admin/assign", s.HandleAdminAssign)
	s.mux.HandleFunc("/api/register", s.HandleRegister)
	s.mux.HandleFunc("/api/user/ai-config", s.HandleUserAIConfig)

	// Register differential test fixture endpoints
	s.mux.HandleFunc("/_test/register_device", s.HandleTestRegisterDevice)
	s.mux.HandleFunc("/_test/disconnect_device", s.HandleTestDisconnectDevice)
	s.mux.HandleFunc("/_test/reset", s.HandleTestReset)

	return s
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Returns the internal device registry instance
// Source Behavior: Accessor for Server.deviceReg
// Confidence: HIGH
func (s *Server) GetDeviceRegistry() *devices.Registry {
	return s.deviceReg
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
