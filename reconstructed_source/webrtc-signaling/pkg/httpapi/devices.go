// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Reconstructed HTTP request handlers for device registry REST endpoints
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"cloudphone-signaling/pkg/devices"
)

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.i2EgUTaLmQs
// VA: 0x74cf80
// Whole Function VA: 0x74cf80
// Evidence VA Range: 0x74cfe2-0x74d355, 0x74d784-0x74d8c0
// Excluded Behavior: In-memory map iteration and permission checks (pkg/devices)
// Excluded WS Behavior: None (REST endpoint only; WebSocket peer streaming / agent message dispatch excluded)
// Evidence: DEVICE_HTTP_FUNCTION_SLICES.json, DEVICE_ROUTE_FAMILY.json, DEVICE_EMPTY_REGISTRY_CONTRACT.json, DEVICE_POPULATED_REGISTRY_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleDevices(w http.ResponseWriter, r *http.Request) {
	SetCORS(w, "GET, OPTIONS")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	var role string = "admin"
	var assigned []string = nil
	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			WriteError(w, http.StatusUnauthorized, "Unauthorized")
			return
		}
		role = user.Role
		assigned = user.AssignedDevices
	}

	devs := s.deviceReg.GetDevices(role, assigned)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(devs)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling / Windows AMD64 webrtc-signaling.exe
// Binary Symbol: main.rXQMyuE
// VA: 0x74da60
// Whole Function VA: 0x74da60
// Evidence VA Range: 0x74dab0-0x74de88, 0x74def3-0x74e3b8
// Excluded Behavior: In-memory registry mutation and online check (pkg/devices)
// Excluded WS Behavior: None (REST endpoint only)
// Evidence: DEVICE_HTTP_FUNCTION_SLICES.json, DEVICE_ROUTE_IDENTITY_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleDeviceDelete(w http.ResponseWriter, r *http.Request) {
	SetCORS(w, "DELETE, OPTIONS")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodDelete {
		WriteError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			WriteError(w, http.StatusUnauthorized, "Unauthorized")
			return
		}

		if user.Role != "admin" {
			WriteError(w, http.StatusForbidden, "Forbidden")
			return
		}
	}

	deviceID := strings.TrimPrefix(r.URL.Path, "/api/devices/")
	if deviceID == "" {
		WriteError(w, http.StatusBadRequest, "Invalid device id")
		return
	}

	err := s.deviceReg.DeleteDevice(deviceID)
	if err != nil {
		if errors.Is(err, devices.ErrDeviceNotFound) {
			WriteError(w, http.StatusNotFound, "Device not found")
			return
		}
		if errors.Is(err, devices.ErrDeviceOnline) {
			WriteError(w, http.StatusConflict, "Device is online, disconnect it first")
			return
		}
		WriteError(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("{\"status\":\"deleted\"}\n"))
}

// TestRegisterRequest defines the payload for registering mock devices in differential tests.
type TestRegisterRequest struct {
	DeviceID   string      `json:"device_id"`
	DeviceInfo interface{} `json:"device_info"`
	IsWebRTC   bool        `json:"is_webrtc"`
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Test fixture endpoint to register a mock device in the reconstructed server
// Source Behavior: Calls s.deviceReg.RegisterDevice
// Confidence: HIGH
func (s *Server) HandleTestRegisterDevice(w http.ResponseWriter, r *http.Request) {
	var req TestRegisterRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		WriteError(w, http.StatusBadRequest, "Invalid JSON")
		return
	}
	s.deviceReg.RegisterDevice(req.DeviceID, req.DeviceInfo, req.IsWebRTC)
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("OK"))
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Test fixture endpoint to simulate agent disconnect in differential tests
// Source Behavior: Calls s.deviceReg.DisconnectDevice
// Confidence: HIGH
func (s *Server) HandleTestDisconnectDevice(w http.ResponseWriter, r *http.Request) {
	var req struct {
		DeviceID string `json:"device_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		WriteError(w, http.StatusBadRequest, "Invalid JSON")
		return
	}
	s.deviceReg.DisconnectDevice(req.DeviceID)
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("OK"))
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Test fixture endpoint to reset the device registry in differential tests
// Source Behavior: Calls s.deviceReg.Clear
// Confidence: HIGH
func (s *Server) HandleTestReset(w http.ResponseWriter, r *http.Request) {
	s.deviceReg.Clear()
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("OK"))
}

