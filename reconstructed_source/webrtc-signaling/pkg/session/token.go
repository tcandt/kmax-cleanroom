// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol: main.d2SHxnu
// VA: 0x739240
// File Offset: 0x339240
// Size: 224 bytes
// Evidence:
//   - 32-byte buffer allocation on stack (rsp + 0x18)
//   - crypto/rand.Read invocation at VA 0x73926b (Y4_aOVf1Fz.ES8BvDO6y1V)
//   - 64-byte slice allocation at VA 0x739281 (runtime.makeslice)
//   - Hex lowercase encoding lookup table at VA 0x827245 ("0123456789abcdef")
//   - 64-character string creation at VA 0x7392e1 (runtime.slicebytetostring)
// Confidence: HIGH

package session

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
)

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.d2SHxnu
// VA: 0x739240
// Evidence: 32 random bytes read from crypto/rand, hex encoded to 64 lowercase ASCII characters
// Confidence: HIGH
func GenerateToken() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", fmt.Errorf("failed to read random bytes: %w", err)
	}
	return hex.EncodeToString(b), nil
}
