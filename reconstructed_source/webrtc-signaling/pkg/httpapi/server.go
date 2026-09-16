// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: HTTP server routing for authentication endpoints using Go standard library net/http.ServeMux
// Confidence: HIGH

package httpapi

import (
	"net/http"
	"sync"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/devices"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// Server encapsulates the HTTP handler router and associated auth/session/device services.
type Server struct {
	mux       *http.ServeMux
	auth      *auth.Authenticator
	noAuth    bool
	deviceReg *devices.Registry

	tagsStore      *storage.TagsStore
	sharesStore    *storage.SharesStore
	shortcutsStore *storage.ShortcutsStore

	// Server Configuration state (Phase 2C.3G)
	iceServersMu      sync.RWMutex
	iceServers        []types.ICEServer
	defaultSettingsMu sync.RWMutex
	defaultSettings   map[string]interface{}
	versionInfo       types.VersionInfo
	listeningPort     string
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
		mux:             http.NewServeMux(),
		auth:            authenticator,
		noAuth:          noAuth,
		deviceReg:       dReg,
		defaultSettings: make(map[string]interface{}),
		iceServers: []types.ICEServer{
			{URLs: []string{"stun:stun.l.google.com:19302"}},
		},
		versionInfo: types.VersionInfo{
			BuildTime: "2026-09-07T09:58:25Z",
			GitCommit: "2693ef1",
			Version:   "v0.3.6",
		},
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

	// Register device tags route matching original binary
	s.mux.HandleFunc("/api/tags", s.HandleTags)

	// Register device share routes matching original binary
	s.mux.HandleFunc("/api/share/create", s.HandleShareCreate)
	s.mux.HandleFunc("/api/share/list", s.HandleShareList)
	s.mux.HandleFunc("/api/share/revoke", s.HandleShareRevoke)
	s.mux.HandleFunc("/api/share/extend", s.HandleShareExtend)
	s.mux.HandleFunc("/api/share/update", s.HandleShareUpdate)
	s.mux.HandleFunc("/api/share/info", s.HandleShareInfo)
	s.mux.HandleFunc("/api/share/redeem_card", s.HandleShareRedeemCard)

	// Register shortcuts route matching original binary
	s.mux.HandleFunc("/api/shortcuts", s.HandleShortcuts)

	// Register server configuration routes matching original binary (Phase 2C.3G)
	s.mux.HandleFunc("/api/server/addresses", s.HandleServerAddresses)
	s.mux.HandleFunc("/api/default_settings", s.HandleDefaultSettings)
	s.mux.HandleFunc("/api/ice_servers", s.HandleICEServers)
	s.mux.HandleFunc("/api/version", s.HandleVersion)

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
