package license

import (
	"encoding/base64"
	"encoding/hex"
	"net"
	"os"
	"path/filepath"
	"regexp"
	"sync"
	"testing"
)

func TestDeriveMachineIDControlled(t *testing.T) {
	// Controlled inputs verifying interface filtering, MAC sorting, UUID selection, and formatting
	ifaces := []InterfaceInfo{
		{Name: "lo", HardwareAddr: "00:00:00:00:00:00", Flags: net.FlagLoopback},
		{Name: "docker0", HardwareAddr: "02:42:1a:2b:3c:4d", Flags: net.FlagUp},
		{Name: "tun0", HardwareAddr: "00:11:22:33:44:55", Flags: net.FlagUp},
		{Name: "eth1", HardwareAddr: "52:54:00:12:34:56", Flags: net.FlagUp},
		{Name: "eth0", HardwareAddr: "00:11:22:33:44:55", Flags: net.FlagUp},
		{Name: "veth_xyz", HardwareAddr: "0a:1b:2c:3d:4e:5f", Flags: net.FlagUp},
	}

	filteredMACs := filterAndSortMACs(ifaces)
	expectedMACs := []string{"00:11:22:33:44:55", "52:54:00:12:34:56"}
	if len(filteredMACs) != len(expectedMACs) {
		t.Fatalf("expected %d MACs, got %d: %v", len(expectedMACs), len(filteredMACs), filteredMACs)
	}
	for i, m := range expectedMACs {
		if filteredMACs[i] != m {
			t.Errorf("MAC index %d mismatch: got %s, want %s", i, filteredMACs[i], m)
		}
	}

	// Test deterministic derivation from parts
	mid := deriveMachineIDFromParts("test-uuid-1234", filteredMACs, 4)
	expectedMID := "ED5C-35D0-6087-44A2"
	if mid != expectedMID {
		t.Errorf("Controlled machine ID mismatch: got %s, want %s", mid, expectedMID)
	}

	// Test fallback derivation when parts are empty
	fallbackMID := deriveMachineIDFromParts("", nil, 0)
	expectedFallback := "33A1-1E0C-C09E-646B"
	if fallbackMID != expectedFallback {
		t.Errorf("Fallback machine ID mismatch: got %s, want %s", fallbackMID, expectedFallback)
	}
}

func TestHostMachineIDFormat(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "lic_test_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpDir)

	mgr := NewManager(tmpDir)
	mid := mgr.GetMachineID()
	if len(mid) != 19 {
		t.Fatalf("machine ID length mismatch: got %d (val %q), want 19", len(mid), mid)
	}

	matched, err := regexp.MatchString(`^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$`, mid)
	if err != nil || !matched {
		t.Errorf("machine ID does not match 4x4 hex uppercase pattern: %s", mid)
	}
}

func TestActivateLockOrderConcurrency(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "lic_test_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpDir)

	mgr := NewManager(tmpDir)

	// Invariant: Failed activations do not acquire the lock or block concurrent status queries
	const concurrency = 20
	var wg sync.WaitGroup
	wg.Add(concurrency * 2)

	for i := 0; i < concurrency; i++ {
		go func(idx int) {
			defer wg.Done()
			badKey := "invalid.key.payload"
			if err := mgr.Activate(badKey); err == nil {
				t.Errorf("expected activation failure on invalid key")
			}
		}(i)

		go func(idx int) {
			defer wg.Done()
			status := mgr.GetStatus(idx)
			if status.Activated {
				t.Errorf("expected activated=false during concurrent invalid activation")
			}
			if status.Status != "valid" {
				t.Errorf("expected status=valid promo default, got %s", status.Status)
			}
		}(i)
	}

	wg.Wait()

	finalStatus := mgr.GetStatus(0)
	if finalStatus.Activated {
		t.Errorf("final state mutated: activated must remain false")
	}
}

func TestVerifyLicenseRejections(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "lic_test_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpDir)

	mgr := NewManager(tmpDir)

	tests := []struct {
		name    string
		key     string
		wantErr string
	}{
		{"empty", "", "授权码格式错误"},
		{"whitespace", "   ", "授权码格式错误"},
		{"no_dot", "SOMEKEYWITHOUTDOT", "授权码格式错误"},
		{"too_many_dots", "part1.part2.part3", "授权码格式错误"},
		{"invalid_base64", "!!!badbase64.0123456789abcdef", "非法的 Base64 编码"},
		{"invalid_hex_sig", base64.StdEncoding.EncodeToString([]byte("{}")) + ".nothex", "数字签名格式无效"},
		{"short_hex_sig", base64.StdEncoding.EncodeToString([]byte("{}")) + ".1234", "数字签名格式无效"},
		{
			"bad_signature",
			base64.StdEncoding.EncodeToString([]byte(`{"machine_id":"8AD9-A7EF-87FB-E780"}`)) + "." + hex.EncodeToString(make([]byte, 64)),
			"授权数字签名校验失败，可能已被篡改",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := mgr.verifyLicense(tt.key)
			if err == nil {
				t.Fatalf("expected error %q, got nil", tt.wantErr)
			}
			if err.Error() != tt.wantErr {
				t.Errorf("error mismatch: got %q, want %q", err.Error(), tt.wantErr)
			}
		})
	}
}

func TestStartupInvalidFileHandling(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "lic_test_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpDir)

	licFile := filepath.Join(tmpDir, "license.txt")
	if err := os.WriteFile(licFile, []byte("invalid-license-content"), 0644); err != nil {
		t.Fatal(err)
	}

	mgr := NewManager(tmpDir)
	status := mgr.GetStatus(0)

	// Invariant: Invalid file falls back to built-in promo
	if status.LicenseSource != "built-in" {
		t.Errorf("expected license_source=built-in, got %s", status.LicenseSource)
	}
	if status.Status != "valid" {
		t.Errorf("expected status=valid, got %s", status.Status)
	}
	if status.Activated != false {
		t.Errorf("expected activated=false, got %v", status.Activated)
	}
	if status.ErrorMsg != "" {
		t.Errorf("expected error_msg='', got %s", status.ErrorMsg)
	}
}
