// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Unit tests for Device Registry core and filtering
// Confidence: HIGH

package devices

import (
	"testing"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests CanAccessDevice permission rules matching main.pVOasuBli
// Source Behavior: Validates admin, wildcard, and specific device assignment checks
// Confidence: HIGH
func TestCanAccessDevice(t *testing.T) {
	if !CanAccessDevice("admin", nil, "dev-1") {
		t.Fatalf("Admin should have access to any device")
	}

	if !CanAccessDevice("user", []string{"*"}, "dev-1") {
		t.Fatalf("Wildcard assignment should grant access to any device")
	}

	if !CanAccessDevice("user", []string{"dev-1", "dev-2"}, "dev-1") {
		t.Fatalf("Matching device assignment should grant access")
	}

	if CanAccessDevice("user", []string{"dev-2"}, "dev-1") {
		t.Fatalf("Non-matching device assignment should NOT grant access")
	}

	if CanAccessDevice("user", nil, "dev-1") {
		t.Fatalf("Nil assignment should NOT grant access")
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Mapping Scope: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Tests Registry lifecycle operations
// Source Behavior: Validates register, get, disconnect, and delete semantics
// Confidence: HIGH
func TestRegistryLifecycle(t *testing.T) {
	reg := NewRegistry()

	// 1. Initially empty
	devs := reg.GetDevices("admin", nil)
	if len(devs) != 0 {
		t.Fatalf("Expected 0 devices, got %d", len(devs))
	}

	// 2. Register device 1
	reg.RegisterDevice("dev-alpha", map[string]string{"model": "Pixel 7"}, true)
	devs = reg.GetDevices("admin", nil)
	if len(devs) != 1 || devs[0].DeviceID != "dev-alpha" || !devs[0].Online {
		t.Fatalf("Expected 1 online device dev-alpha, got %+v", devs)
	}

	// 3. User filtering
	userDevs := reg.GetDevices("user", []string{"dev-beta"})
	if len(userDevs) != 0 {
		t.Fatalf("Unassigned user should see 0 devices, got %d", len(userDevs))
	}

	userDevs = reg.GetDevices("user", []string{"dev-alpha"})
	if len(userDevs) != 1 {
		t.Fatalf("Assigned user should see 1 device, got %d", len(userDevs))
	}

	// 4. Online delete rejection (409 logic)
	err := reg.DeleteDevice("dev-alpha")
	if err != ErrDeviceOnline {
		t.Fatalf("Expected ErrDeviceOnline, got %v", err)
	}

	// 5. Disconnect device
	reg.DisconnectDevice("dev-alpha")
	devs = reg.GetDevices("admin", nil)
	if len(devs) != 1 || devs[0].Online {
		t.Fatalf("Device should now be offline")
	}

	// 6. Offline delete success
	err = reg.DeleteDevice("dev-alpha")
	if err != nil {
		t.Fatalf("Expected nil error on offline delete, got %v", err)
	}

	// 7. Not found delete
	err = reg.DeleteDevice("dev-alpha")
	if err != ErrDeviceNotFound {
		t.Fatalf("Expected ErrDeviceNotFound, got %v", err)
	}
}
