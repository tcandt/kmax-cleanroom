// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Thread-safe License & Entitlement State Manager
// Evidence:
//   - LICENSE_CRYPTO_VERIFICATION_CONTRACT.json
//   - LICENSE_PUBLIC_VERIFIER_EVIDENCE.json
//   - LICENSE_MACHINE_ID_CONTRACT.json
//   - LICENSE_STATUS_CONTRACT.json
//   - LICENSE_STARTUP_FILE_MATRIX.json
// Confidence: HIGH

package license

import (
	"crypto"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"sync"
	"time"

	"cloudphone-signaling/pkg/types"
)

// embeddedPublicKey is the 32-byte Ed25519 public verification key embedded in main.PmtRXo (0x733c40)
// and deobfuscated via byte-wise XOR with 0x5a at VA 0x733dbf.
// SHA-256 Fingerprint: 4ec41f373e3d920fb155df761a8cd47b453659a8aeba799f46818ac3575dd91c
var embeddedPublicKey = ed25519.PublicKey([]byte{
	0x73, 0x17, 0xbe, 0xd3, 0x8c, 0xc0, 0xd9, 0x6b,
	0xd5, 0xff, 0x35, 0xc4, 0x8f, 0xc5, 0x78, 0x22,
	0x08, 0x37, 0x57, 0x82, 0x3e, 0xba, 0xc1, 0x81,
	0xe4, 0xad, 0x0b, 0x08, 0xe4, 0x60, 0xe8, 0x20,
})

// licenseClaims represents the JSON payload structure embedded in the base64 part of the license token.
// Statically recovered from main.PmtRXo unmarshaling target descriptor 0x7ed2a0 (size 56 bytes).
type licenseClaims struct {
	MachineID  string `json:"machine_id"` // offset 0 (16B) - FLdrjU
	MaxDevices int    `json:"max_devices"`// offset 16 (8B) - FzadFNPQCB
	ExpiresAt  string `json:"expires_at"` // offset 24 (16B) - TF9svpC2ha
	Customer   string `json:"customer"`   // offset 40 (16B) - M6ofLo6ey
}

// Manager manages license state, built-in promotional entitlements,
// hardware machine fingerprinting, and persistence.
type Manager struct {
	mu                  sync.RWMutex
	dataDir             string
	filePath            string
	activated           bool
	customer            string
	errorMsg            string
	expiresAt           string
	licenseExpired      bool
	licenseSource       string
	machineID           string
	maxDevices          int
	postPromoMaxDevices int
	promo               bool
	status              string
	rawLicenseKey       string // Recovered from global at 0xc06f78 (main.ODSX7KW)
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_FUNCTION
// Mapping Scope: GENERATED_BUILD_FUNCTION
// Original Function Mapping: NONE
// Purpose: Constructs a new thread-safe license Manager with built-in promotional defaults
// Confidence: HIGH
func NewManager(dataDir string) *Manager {
	mgr := &Manager{
		dataDir:             dataDir,
		filePath:            filepath.Join(dataDir, "license.txt"),
		activated:           false,
		customer:            "",
		errorMsg:            "",
		expiresAt:           "2026-11-01", // Recovered from 0xbeed90 in .data
		licenseExpired:      false,
		licenseSource:       "built-in",   // Recovered from 0x81ff75 in .rodata
		maxDevices:          20,           // Recovered from 0xbb0260 in .data
		postPromoMaxDevices: 10,           // Recovered from 0x8b92c0 in .rodata
		promo:               true,
		status:              "valid",
	}

	mgr.machineID = mgr.generateMachineID()
	mgr.loadLicenseFile()
	return mgr
}

// InterfaceInfo captures network interface metadata required for hardware fingerprinting.
type InterfaceInfo struct {
	Name         string
	HardwareAddr string
	Flags        net.Flags
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ZbJsqTIiz3ML
// VA: 0x732ec0
// Evidence: LICENSE_MACHINE_ID_CONTRACT.json, LICENSE_VALIDATION_FUNCTION_SLICES.json
// Purpose: Filters out loopback, empty MACs, and virtual/tunnel interfaces, then sorts ascending
// Confidence: HIGH
func filterAndSortMACs(ifaces []InterfaceInfo) []string {
	var macs []string
	ignored := []string{
		"utun", "tun", "tap", "docker", "veth",
		"br-", "bridge", "awdl", "llw", "p2p",
		"gif", "stf", "vlan",
	}
	for _, iface := range ifaces {
		if iface.Flags&net.FlagLoopback != 0 {
			continue
		}
		mac := iface.HardwareAddr
		if mac == "" {
			continue
		}
		lowerName := strings.ToLower(iface.Name)
		skip := false
		for _, ig := range ignored {
			if strings.HasPrefix(lowerName, ig) {
				skip = true
				break
			}
		}
		if skip {
			continue
		}
		macs = append(macs, mac)
	}
	sort.Strings(macs)
	return macs
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ZbJsqTIiz3ML
// VA: 0x732ec0
// Evidence: LICENSE_MACHINE_ID_CONTRACT.json, LICENSE_VALIDATION_FUNCTION_SLICES.json
// Purpose: Deterministically combines UUID/machine-id, filtered MAC list, and CPU cores into XXXX-XXXX-XXXX-XXXX
// Confidence: HIGH
func deriveMachineIDFromParts(uuid string, macs []string, numCPU int) string {
	var parts []string
	if uuid != "" {
		parts = append(parts, uuid)
	}
	if len(macs) > 0 {
		parts = append(parts, strings.Join(macs, ","))
	}
	if numCPU > 0 {
		parts = append(parts, fmt.Sprintf("cores:%d", numCPU))
	}
	if len(parts) == 0 {
		parts = append(parts, "FALLBACK_CLOUDPHONE_ID")
	}

	raw := strings.Join(parts, "|")
	sum := sha256.Sum256([]byte(raw))
	hexStr := fmt.Sprintf("%x", sum)

	res := fmt.Sprintf("%s-%s-%s-%s", hexStr[0:4], hexStr[4:8], hexStr[8:12], hexStr[12:16])
	return strings.ToUpper(res)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ZbJsqTIiz3ML
// VA: 0x732ec0
// Size: 3456 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_MACHINE_ID_CONTRACT.json, LICENSE_VALIDATION_FUNCTION_SLICES.json
// Purpose: Computes deterministic hardware machine fingerprint formatted as XXXX-XXXX-XXXX-XXXX
// Confidence: HIGH
func (m *Manager) generateMachineID() string {
	var uuid string

	// 1. UUID / Machine ID files (product_uuid, machine-id, dbus machine-id)
	for _, p := range []string{"/sys/class/dmi/id/product_uuid", "/etc/machine-id", "/var/lib/dbus/machine-id"} {
		data, err := os.ReadFile(p)
		if err == nil {
			s := strings.TrimSpace(string(data))
			if s != "" {
				uuid = s
				break
			}
		}
	}

	// 2. Network interfaces
	var ifaceInfos []InterfaceInfo
	ifaces, err := net.Interfaces()
	if err == nil {
		for _, iface := range ifaces {
			ifaceInfos = append(ifaceInfos, InterfaceInfo{
				Name:         iface.Name,
				HardwareAddr: iface.HardwareAddr.String(),
				Flags:        iface.Flags,
			})
		}
	}
	macs := filterAndSortMACs(ifaceInfos)

	// 3. Cores & formatting
	return deriveMachineIDFromParts(uuid, macs, runtime.NumCPU())
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.LvbcDRl_uhc4
// VA: 0x733fe0
// Size: 1696 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_STARTUP_FILE_MATRIX.json, LICENSE_PERSISTENCE_CONTRACT.json
// Purpose: Reads and validates local license.txt on daemon initialization; ignores invalid files
// Confidence: HIGH
func (m *Manager) loadLicenseFile() {
	if m.filePath == "" {
		return
	}
	data, err := os.ReadFile(m.filePath)
	if err != nil {
		// File does not exist: remain in default built-in promo mode
		return
	}

	key := strings.TrimSpace(string(data))
	if key == "" {
		// Empty/whitespace file: remain in built-in promo mode without mutating file
		return
	}

	claims, err := m.verifyLicense(key)
	if err != nil {
		// Proven via differential oracle: invalid persisted key does NOT set expired state,
		// but safely falls back to default built-in promotional entitlement.
		return
	}

	// Valid cryptographic license loaded from file
	m.applyValidLicense(claims, key)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.PmtRXo
// VA: 0x733c40
// Size: 928 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_CRYPTO_VERIFICATION_CONTRACT.json, LICENSE_PUBLIC_VERIFIER_EVIDENCE.json
// Purpose: Original cryptographic verification pipeline: base64 payload, hex Ed25519 signature,
// JSON claims unmarshaling, and hardware machine ID binding.
// Confidence: HIGH
func (m *Manager) verifyLicense(key string) (*licenseClaims, error) {
	trimmed := strings.TrimSpace(key)
	if trimmed == "" {
		return nil, errors.New("授权码格式错误")
	}

	parts := strings.Split(trimmed, ".")
	if len(parts) != 2 {
		return nil, errors.New("授权码格式错误")
	}

	payloadBytes, err := base64.StdEncoding.DecodeString(parts[0])
	if err != nil {
		return nil, errors.New("非法的 Base64 编码")
	}

	sigBytes, err := hex.DecodeString(parts[1])
	if err != nil || len(sigBytes) != ed25519.SignatureSize {
		return nil, errors.New("数字签名格式无效")
	}

	// Verify cryptographic signature against embedded public key using exact options
	// Statically proven from main.PmtRXo (0x733dd7-0x733df4): Options struct has Hash = 0, Context = ""
	opts := &ed25519.Options{
		Hash:    crypto.Hash(0),
		Context: "",
	}
	if err := ed25519.VerifyWithOptions(embeddedPublicKey, payloadBytes, sigBytes, opts); err != nil {
		return nil, errors.New("授权数字签名校验失败，可能已被篡改")
	}

	var claims licenseClaims
	if err := json.Unmarshal(payloadBytes, &claims); err != nil {
		return nil, errors.New("无效的授权声明内容")
	}

	if claims.MachineID != m.machineID {
		return nil, fmt.Errorf("机器码不匹配: 授权绑定 %s, 当前系统为 %s", claims.MachineID, m.machineID)
	}

	return &claims, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ODSX7KW
// VA: 0x7347a0
// Evidence: LICENSE_PERSISTENCE_CONTRACT.json, LICENSE_VALIDATION_FUNCTION_SLICES.json, LICENSE_SUCCESS_PATH_STATIC_CONTRACT.json
// Purpose: Updates manager state upon successful cryptographic verification, preserving raw key at global 0xc06f78
// Confidence: HIGH
func (m *Manager) applyValidLicense(claims *licenseClaims, rawKey string) {
	m.activated = true
	m.customer = claims.Customer
	m.expiresAt = claims.ExpiresAt
	m.maxDevices = claims.MaxDevices
	m.licenseSource = "license-file"
	m.rawLicenseKey = strings.TrimSpace(rawKey)
	m.errorMsg = ""

	// Evaluate expiration
	if expTime, err := time.Parse("2006-01-02", claims.ExpiresAt); err == nil {
		now := time.Now()
		expMidnight := time.Date(expTime.Year(), expTime.Month(), expTime.Day(), 23, 59, 59, 0, time.UTC)
		nowMidnight := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, time.UTC)
		if expMidnight.Before(nowMidnight) {
			m.status = "expired"
			m.licenseExpired = true
			m.errorMsg = "授权已过期"
		} else {
			m.status = "valid"
			m.licenseExpired = false
		}
	} else {
		m.status = "valid"
		m.licenseExpired = false
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ODSX7KW
// VA: 0x7347a0
// Size: 960 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_SUCCESS_PATH_STATIC_CONTRACT.json, LICENSE_ACTIVATION_REJECTION_CONTRACT.json
// Purpose: Validates incoming license key cryptographically before acquiring mutex, persists to license.txt (mode 0644) on success, or returns original rejection
// Confidence: HIGH
func (m *Manager) Activate(licenseKey string) error {
	claims, err := m.verifyLicense(licenseKey)
	if err != nil {
		// Rejection does NOT mutate in-memory state or disk, and does not block concurrent readers
		return err
	}

	m.mu.Lock()
	defer m.mu.Unlock()

	// Persist to license.txt with mode 0644 (0x1a4)
	if m.filePath != "" {
		trimmed := strings.TrimSpace(licenseKey)
		if writeErr := os.WriteFile(m.filePath, []byte(trimmed), 0644); writeErr != nil {
			fmt.Fprintf(os.Stderr, "[License] 写入本地授权文件失败：%v\n", writeErr)
		}
	}

	m.applyValidLicense(claims, licenseKey)
	return nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.J_5lH4w6CU
// VA: 0x735400
// Size: 2048 bytes
// Mapping Scope: BEHAVIOR_SLICE
// Evidence: LICENSE_STATUS_CONTRACT.json, LICENSE_CURRENT_DEVICES_CROSS_CONTRACT.json
// Purpose: Calculates active entitlement state, remaining days, and returns 13-field response
// Confidence: HIGH
func (m *Manager) GetStatus(currentDevices int) types.LicenseStatusResponse {
	m.mu.RLock()
	defer m.mu.RUnlock()

	daysRemaining := 0
	isExpired := m.licenseExpired
	statusStr := m.status

	if expTime, err := time.Parse("2006-01-02", m.expiresAt); err == nil {
		now := time.Now()
		expMidnight := time.Date(expTime.Year(), expTime.Month(), expTime.Day(), 23, 59, 59, 0, time.UTC)
		nowMidnight := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, time.UTC)
		diff := expMidnight.Sub(nowMidnight)
		days := int(diff.Hours() / 24)
		if days < 0 {
			daysRemaining = 0
			isExpired = true
			statusStr = "expired"
		} else {
			daysRemaining = days
		}
	}

	return types.LicenseStatusResponse{
		Activated:           m.activated,
		CurrentDevices:      currentDevices,
		Customer:            m.customer,
		DaysRemaining:       daysRemaining,
		ErrorMsg:            m.errorMsg,
		ExpiresAt:           m.expiresAt,
		LicenseExpired:      isExpired,
		LicenseSource:       m.licenseSource,
		MachineID:           m.machineID,
		MaxDevices:          m.maxDevices,
		PostPromoMaxDevices: m.postPromoMaxDevices,
		Promo:               m.promo,
		Status:              statusStr,
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Purpose: Thread-safe accessor for machine ID used in testing and verification
// Confidence: HIGH
func (m *Manager) GetMachineID() string {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return m.machineID
}
