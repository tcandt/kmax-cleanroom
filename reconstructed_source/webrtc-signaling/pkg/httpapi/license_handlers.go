// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: License & Entitlement REST Route Family (/api/activate, /api/license_status, /debug/license)
// Evidence:
//   - Route registrations: ROUTE_HANDLER_MAP.json
//       * /api/activate       (call VA 0x7659b8, handler main.jcraNgV8Jg @ 0x74b6c0)
//       * /api/license_status (call VA 0x7659d0, handler main.xdGI1n @ 0x74c220)
//       * /debug/license      (call VA 0x7659e8, handler main.yyDyfaokeO @ 0x74bf60)
//   - Contracts & Type Descriptors:
//       * LICENSE_ROUTE_METHOD_MATRIX.json, LICENSE_AUTH_MATRIX.json
//       * LICENSE_TYPE_EVIDENCE.json, LICENSE_STATUS_CONTRACT.json
//       * LICENSE_ACTIVATION_REJECTION_CONTRACT.json, LICENSE_PERSISTENCE_CONTRACT.json
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"net/http"

	"cloudphone-signaling/pkg/license"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets or updates the License Manager instance on Server
// Confidence: HIGH
func (s *Server) SetLicenseManager(mgr *license.Manager) {
	s.licenseMu.Lock()
	defer s.licenseMu.Unlock()
	s.licenseMgr = mgr
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for the License Manager instance
// Confidence: HIGH
func (s *Server) GetLicenseManager() *license.Manager {
	s.licenseMu.RLock()
	defer s.licenseMu.RUnlock()
	return s.licenseMgr
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets the debug flag on Server to control /debug/ endpoints
// Confidence: HIGH
func (s *Server) SetDebug(debug bool) {
	s.debugMu.Lock()
	defer s.debugMu.Unlock()
	s.debug = debug
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for the debug flag
// Confidence: HIGH
func (s *Server) IsDebug() bool {
	s.debugMu.RLock()
	defer s.debugMu.RUnlock()
	return s.debug
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.jcraNgV8Jg
// VA: 0x74b6c0
// Size: 2208 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_ROUTE_FAMILY.json, LICENSE_ROUTE_METHOD_MATRIX.json, LICENSE_ACTIVATION_REJECTION_CONTRACT.json
// Purpose: HTTP handler for /api/activate: validates request payload, CORS preflight, and processes activation
// Confidence: HIGH
func (s *Server) HandleActivate(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Method not allowed\n"))
		return
	}

	var req types.ActivationRequest
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&req); err != nil {
		// Empty body or malformed JSON
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid JSON payload\n"))
		return
	}

	mgr := s.GetLicenseManager()
	var actErr error
	if mgr != nil {
		actErr = mgr.Activate(req.License)
	} else {
		actErr = http.ErrHandlerTimeout
	}

	if actErr != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(types.ActivationErrorResponse{
			Error: actErr.Error(),
		})
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(types.ActivationSuccessResponse{
		Status:  "success",
		Message: "激活码更新成功",
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.xdGI1n
// VA: 0x74c220
// Size: 1056 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_ROUTE_FAMILY.json, LICENSE_ROUTE_METHOD_MATRIX.json, LICENSE_STATUS_CONTRACT.json
// Purpose: HTTP handler for /api/license_status: returns 13-field entitlement status JSON
// Confidence: HIGH
func (s *Server) HandleLicenseStatus(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	currentDevices := 0
	if s.deviceReg != nil {
		currentDevices = s.deviceReg.GetDeviceCount()
	}

	mgr := s.GetLicenseManager()
	var resp types.LicenseStatusResponse
	if mgr != nil {
		resp = mgr.GetStatus(currentDevices)
	}

	w.WriteHeader(http.StatusOK)
	// Go's net/http automatically retains Content-Length for HEAD while suppressing wire body bytes
	json.NewEncoder(w).Encode(resp)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.yyDyfaokeO
// VA: 0x74bf60
// Size: 704 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_ROUTE_FAMILY.json, LICENSE_ROUTE_METHOD_MATRIX.json, LICENSE_STATUS_CONTRACT.json
// Purpose: HTTP handler for /debug/license: returns 13-field entitlement status JSON when debug mode is enabled across all HTTP verbs without CORS headers
// Confidence: HIGH
func (s *Server) HandleDebugLicense(w http.ResponseWriter, r *http.Request) {
	if !s.IsDebug() {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not found\n"))
		return
	}

	// In original binary, /debug/license emits NO Access-Control-* CORS headers,
	// and accepts all standard verbs (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
	w.Header().Set("Content-Type", "application/json")

	currentDevices := 0
	if s.deviceReg != nil {
		currentDevices = s.deviceReg.GetDeviceCount()
	}

	mgr := s.GetLicenseManager()
	var resp types.LicenseStatusResponse
	if mgr != nil {
		resp = mgr.GetStatus(currentDevices)
	}

	w.WriteHeader(http.StatusOK)
	// Go's net/http automatically retains Content-Length for HEAD while suppressing wire body bytes
	json.NewEncoder(w).Encode(resp)
}
