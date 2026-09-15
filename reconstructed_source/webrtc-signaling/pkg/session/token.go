// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: WHOLE_FUNCTION
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
// Mapping Scope: BEHAVIOR_SLICE
// Binary Target: Linux AMD64 (SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol: main.d2SHxnu
// VA: 0x739240
// File Offset: 0x339240
// Size: 224 bytes
// Binary Behavior: 32 random bytes read from crypto/rand, hex encoded to 64 lowercase ASCII characters
// Excluded Binary Behavior: Inlined error-ignore semantics (original discarded error return in disassembly at 0x739270)
// Evidence: 32 random bytes read from crypto/rand, hex encoded to 64 lowercase ASCII characters
// Evidence VA Range: 0x739240-0x739320
// Error Handling Provenance:
//   - Static Binary Disassembly: VA 0x73926b calls rand.Read; instructions at 0x739270-0x739272 overwrite return registers without testing error
//   - TOKEN_RANDOM_FAILURE_BEHAVIOR: ORIGINAL_DISCARDS_ERROR / RECONSTRUCTED_GENERATED_ERROR_ADAPTER
// Confidence: HIGH
func GenerateToken() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", fmt.Errorf("failed to read random bytes: %w", err)
	}
	return hex.EncodeToString(b), nil
}
