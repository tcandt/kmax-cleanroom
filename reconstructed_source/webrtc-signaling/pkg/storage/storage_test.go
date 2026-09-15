// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Project: KMAX / CloudPhone Clean-Room Source Recovery
// Purpose: Unit tests validating reconstructed persistence data structures and lifecycles.
// Evidence: Binary behaviors in main.aOfaLG, main.rAJGaVlvfajr, main.w3H7BXxDC, main.rCajRnfJZ, main.fomL4ATwVV1.
// Confidence: HIGH

package storage

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"

	"cloudphone-signaling/pkg/types"
)

func TestStorageManagerBootstrap(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "storage_test_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	sm, err := NewStorageManager(tempDir)
	if err != nil {
		t.Fatalf("NewStorageManager failed: %v", err)
	}

	if err := sm.InitBootstrap(); err != nil {
		t.Fatalf("InitBootstrap failed: %v", err)
	}

	// Verify downloads and snapshots directories exist
	if fi, err := os.Stat(filepath.Join(tempDir, "downloads")); err != nil || !fi.IsDir() {
		t.Errorf("downloads directory was not created eagerly")
	}
	if fi, err := os.Stat(filepath.Join(tempDir, "snapshots")); err != nil || !fi.IsDir() {
		t.Errorf("snapshots directory was not created eagerly")
	}

	// Verify users.json and device_tags.json are created eagerly
	if _, err := os.Stat(filepath.Join(tempDir, "users.json")); err != nil {
		t.Errorf("users.json was not created eagerly: %v", err)
	}
	if _, err := os.Stat(filepath.Join(tempDir, "device_tags.json")); err != nil {
		t.Errorf("device_tags.json was not created eagerly: %v", err)
	}

	// Verify shares.json is NOT created eagerly (lazy creation)
	if _, err := os.Stat(filepath.Join(tempDir, "shares.json")); !os.IsNotExist(err) {
		t.Errorf("shares.json should not be created eagerly at boot")
	}
}

func TestUsersStoreDefaultAdmin(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "users_test_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	uPath := filepath.Join(tempDir, "users.json")
	store := NewUsersStore(uPath)

	if err := store.LoadOrCreate(); err != nil {
		t.Fatalf("LoadOrCreate failed: %v", err)
	}

	admin, exists := store.GetUser("admin")
	if !exists {
		t.Fatalf("admin user was not created")
	}

	if admin.Role != "admin" {
		t.Errorf("expected role 'admin', got '%s'", admin.Role)
	}

	if len(admin.AssignedDevices) != 1 || admin.AssignedDevices[0] != "*" {
		t.Errorf("expected assigned_devices ['*'], got %v", admin.AssignedDevices)
	}

	// Verify password hash formula: SHA256(password + salt)
	expectedHash := HashPassword("admin123", admin.Salt)
	if admin.Password != expectedHash {
		t.Errorf("password hash mismatch: expected %s, got %s", expectedHash, admin.Password)
	}

	// Verify file mode
	if fi, err := os.Stat(uPath); err == nil {
		mode := fi.Mode().Perm()
		if mode != 0600 && os.PathSeparator != '\\' {
			t.Errorf("expected 0600 permissions, got %o", mode)
		}
	}
}

func TestUsersStoreMalformedRecovery(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "users_corrupt_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	uPath := filepath.Join(tempDir, "users.json")
	if err := os.WriteFile(uPath, []byte("{ malformed json content !!!"), 0600); err != nil {
		t.Fatalf("failed to write corrupted file: %v", err)
	}

	store := NewUsersStore(uPath)
	// Must recover by resetting to default admin account
	if err := store.LoadOrCreate(); err != nil {
		t.Fatalf("LoadOrCreate should have recovered from corrupted file: %v", err)
	}

	admin, exists := store.GetUser("admin")
	if !exists {
		t.Fatalf("expected admin user after corruption reset")
	}
	if admin.Role != "admin" {
		t.Errorf("expected role 'admin', got '%s'", admin.Role)
	}
}

func TestUsersStoreAdminWildcardUpgrade(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "users_upgrade_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	uPath := filepath.Join(tempDir, "users.json")
	// Admin without wildcard
	initialUsers := map[string]types.User{
		"admin": {
			Username:        "admin",
			Password:        "hash",
			Salt:            "salt",
			Role:            "admin",
			AssignedDevices: []string{"dev_1"},
		},
	}
	raw, _ := json.Marshal(initialUsers)
	_ = os.WriteFile(uPath, raw, 0600)

	store := NewUsersStore(uPath)
	if err := store.LoadOrCreate(); err != nil {
		t.Fatalf("LoadOrCreate failed: %v", err)
	}

	admin, _ := store.GetUser("admin")
	hasWildcard := false
	for _, d := range admin.AssignedDevices {
		if d == "*" {
			hasWildcard = true
			break
		}
	}
	if !hasWildcard {
		t.Errorf("expected admin assigned_devices to be upgraded with '*', got %v", admin.AssignedDevices)
	}
}

func TestTagsStoreLifecycle(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "tags_test_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	tPath := filepath.Join(tempDir, "device_tags.json")
	store := NewTagsStore(tPath)

	if err := store.LoadOrCreate(); err != nil {
		t.Fatalf("LoadOrCreate failed: %v", err)
	}

	cfg := store.GetConfig()
	if len(cfg.Tags) != 0 || len(cfg.DeviceTags) != 0 {
		t.Errorf("expected empty tags on first run, got %v", cfg)
	}

	// Update configuration
	cfg.Tags = []string{"office", "testing"}
	cfg.DeviceTags["dev_1"] = []string{"office"}
	if err := store.SetConfig(cfg); err != nil {
		t.Fatalf("SetConfig failed: %v", err)
	}

	// Reload from disk to verify round-trip persistence
	store2 := NewTagsStore(tPath)
	if err := store2.LoadOrCreate(); err != nil {
		t.Fatalf("reload failed: %v", err)
	}
	cfg2 := store2.GetConfig()
	if len(cfg2.Tags) != 2 || cfg2.DeviceTags["dev_1"][0] != "office" {
		t.Errorf("persisted config mismatch: %v", cfg2)
	}
}

func TestSharesStoreAtomicLifecycle(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "shares_test_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	sPath := filepath.Join(tempDir, "shares.json")
	store := NewSharesStore(sPath)

	// Verify lazy loading: file absent initially
	if err := store.Load(); err != nil {
		t.Fatalf("Load failed: %v", err)
	}
	if len(store.ListTokens()) != 0 {
		t.Errorf("expected 0 tokens initially")
	}
	if _, err := os.Stat(sPath); !os.IsNotExist(err) {
		t.Errorf("shares.json should not exist before any tokens are created")
	}

	// Create a token and save atomically
	now := time.Now().UTC().Truncate(time.Second)
	token := types.ShareToken{
		TokenID:         "tok_test_123",
		CardCode:        "card_456",
		DeviceID:        "dev_789",
		Creator:         "admin",
		CreatedAt:       now,
		ExpiresAt:       now.Add(24 * time.Hour),
		AccessMode:      "view",
		RequirePassword: false,
		AllowClipboard:  true,
		AllowFileTx:     true,
		Description:     "Test share token",
		UseCount:        0,
	}

	if err := store.SetToken(token); err != nil {
		t.Fatalf("SetToken failed: %v", err)
	}

	// Verify file now exists
	if _, err := os.Stat(sPath); err != nil {
		t.Fatalf("shares.json was not created on token save: %v", err)
	}

	// Verify temp file .tmp is cleaned up
	if _, err := os.Stat(sPath + ".tmp"); !os.IsNotExist(err) {
		t.Errorf("temp file .tmp should have been renamed")
	}

	// Reload from disk
	store2 := NewSharesStore(sPath)
	if err := store2.Load(); err != nil {
		t.Fatalf("reload failed: %v", err)
	}

	loadedTok, exists := store2.GetToken("tok_test_123")
	if !exists {
		t.Fatalf("token tok_test_123 not found after reload")
	}
	if loadedTok.DeviceID != "dev_789" || loadedTok.Creator != "admin" {
		t.Errorf("token fields corrupted on round-trip: %+v", loadedTok)
	}
}

func hashHelper(s string) string {
	h := sha256.Sum256([]byte(s))
	return hex.EncodeToString(h[:])
}
