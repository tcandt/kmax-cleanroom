package license

import (
	"encoding/base64"
	"encoding/hex"
	"os"
	"path/filepath"
	"testing"
)

func TestMachineIDExact(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "lic_test_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpDir)

	mgr := NewManager(tmpDir)
	mid := mgr.GetMachineID()
	if mid != "8AD9-A7EF-87FB-E780" {
		t.Errorf("Machine ID mismatch: got %s, expected 8AD9-A7EF-87FB-E780", mid)
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
