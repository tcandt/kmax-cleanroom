// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Device registry management and access control for WebRTC signaling
// Confidence: HIGH

package devices

import (
	"errors"
	"sync"
	"time"

	"cloudphone-signaling/pkg/types"
)

var (
	ErrDeviceNotFound = errors.New("Device not found")
	ErrDeviceOnline   = errors.New("Device is online, disconnect it first")
)

// Registry maintains the in-memory map of active and offline devices.
type Registry struct {
	mu      sync.RWMutex
	devices map[string]*types.DeviceEntry
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Instantiates an empty in-memory device registry
// Source Behavior: Initializes device map with RWMutex
// Confidence: HIGH
func NewRegistry() *Registry {
	return &Registry{
		devices: make(map[string]*types.DeviceEntry),
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling
// Binary Symbol: main.pVOasuBli
// VA: 0x73d8a0
// Whole Function VA: 0x73d8a0
// Evidence VA Range: 0x73d8a0-0x73dcbc
// Evidence: DEVICE_HTTP_FUNCTION_SLICES.json, DEVICE_VISIBILITY_AUTH_MATRIX.json
// Confidence: HIGH
func CanAccessDevice(role string, assignedDevices []string, deviceID string) bool {
	if role == "admin" {
		return true
	}
	for _, assigned := range assignedDevices {
		if assigned == "*" || assigned == deviceID {
			return true
		}
	}
	return false
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling
// Binary Symbol: main.i2EgUTaLmQs
// VA: 0x74cf80
// Whole Function VA: 0x74cf80
// Evidence VA Range: 0x74d27a-0x74d74d
// Excluded Behavior: HTTP CORS headers, HTTP token extraction, and JSON response encoding (pkg/httpapi)
// Evidence: DEVICE_HTTP_FUNCTION_SLICES.json, DEVICE_TYPE_EVIDENCE.json, DEVICE_POPULATED_REGISTRY_CONTRACT.json
// Confidence: HIGH
func (r *Registry) GetDevices(role string, assignedDevices []string) []types.DeviceDTO {
	r.mu.RLock()
	defer r.mu.RUnlock()

	result := make([]types.DeviceDTO, 0)
	for _, entry := range r.devices {
		if !CanAccessDevice(role, assignedDevices, entry.DeviceID) {
			continue
		}

		entry.Mu.RLock()
		dto := types.DeviceDTO{
			DeviceID:    entry.DeviceID,
			DeviceInfo:  entry.DeviceInfo,
			Online:      entry.Online,
			FirstSeen:   entry.FirstSeen,
			LastSeen:    entry.LastSeen,
			ClientCount: entry.ClientCount,
			Clients:     entry.Clients,
		}
		entry.Mu.RUnlock()

		result = append(result, dto)
	}

	return result
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Registers or reconnects a device into the registry
// Source Behavior: Updates device record or creates new entry
// Confidence: HIGH
func (r *Registry) RegisterDevice(deviceID string, deviceInfo interface{}, isWebRTC bool) *types.DeviceEntry {
	r.mu.Lock()
	defer r.mu.Unlock()

	now := time.Now()
	entry, exists := r.devices[deviceID]
	if exists {
		entry.Mu.Lock()
		entry.DeviceInfo = deviceInfo
		entry.Online = true
		entry.LastSeen = now
		entry.Mu.Unlock()
		return entry
	}

	newEntry := &types.DeviceEntry{
		DeviceID:    deviceID,
		DeviceInfo:  deviceInfo,
		Online:      true,
		FirstSeen:   now,
		LastSeen:    now,
		ClientCount: 0,
		Clients:     nil,
	}
	r.devices[deviceID] = newEntry
	return newEntry
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Marks a device offline when connection terminates
// Source Behavior: Sets Online flag to false while retaining record
// Confidence: HIGH
func (r *Registry) DisconnectDevice(deviceID string) {
	r.mu.Lock()
	defer r.mu.Unlock()

	if entry, exists := r.devices[deviceID]; exists {
		entry.Mu.Lock()
		entry.Online = false
		entry.Mu.Unlock()
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 webrtc-signaling
// Binary Symbol: main.rXQMyuE
// VA: 0x74da60
// Whole Function VA: 0x74da60
// Evidence VA Range: 0x74df80-0x74e042
// Excluded Behavior: HTTP route prefix stripping, admin role check, and JSON response encoding (pkg/httpapi)
// Evidence: DEVICE_HTTP_FUNCTION_SLICES.json, DEVICE_REGISTRY_LIFECYCLE_MATRIX.json
// Confidence: HIGH
func (r *Registry) DeleteDevice(deviceID string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	entry, exists := r.devices[deviceID]
	if !exists {
		return ErrDeviceNotFound
	}

	entry.Mu.RLock()
	isOnline := entry.Online
	entry.Mu.RUnlock()

	if isOnline {
		return ErrDeviceOnline
	}

	delete(r.devices, deviceID)
	return nil
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Retrieves a single device entry by device ID
// Source Behavior: Map lookup with RLock
// Confidence: HIGH
func (r *Registry) GetDevice(deviceID string) (*types.DeviceEntry, bool) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	entry, exists := r.devices[deviceID]
	return entry, exists
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Resets the registry map for test isolation
// Source Behavior: Clears internal devices map
// Confidence: HIGH
func (r *Registry) Clear() {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.devices = make(map[string]*types.DeviceEntry)
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Returns the total count of registered online devices
// Confidence: HIGH
func (r *Registry) GetDeviceCount() int {
	r.mu.RLock()
	defer r.mu.RUnlock()

	count := 0
	for _, entry := range r.devices {
		entry.Mu.RLock()
		if entry.Online {
			count++
		}
		entry.Mu.RUnlock()
	}
	return count
}
