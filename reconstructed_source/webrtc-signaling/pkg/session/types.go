// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Symbol:
//   - Type descriptor at VA: 0x7d6ee0 (size: 40 bytes, kind: struct, 2 fields)
//   - Map descriptor at VA: 0x7c01c0 (kind: map[string]Session)
// Evidence:
//   - rodata reflection structures recovering struct size 40 bytes, field 0 HDz5Nf (string, offset 0), field 1 GkWDh_Jc_q (time.Time, offset 16)
//   - Instruction-local TTL constant: 0x4e94914f0000 ns (24 hours) at VA 0x739365
//   - Instruction-local sweeper ticker: 0xdf8475800 ns (1 minute) at VA 0x73a50e
// Confidence: HIGH

package session

import (
	"time"
)

const (
	// DefaultSessionTTL is 24 hours, recovered from binary constant 0x4e94914f0000 ns at VA 0x739365.
	DefaultSessionTTL = 24 * time.Hour

	// DefaultSweepInterval is 1 minute, recovered from binary constant 0xdf8475800 ns at VA 0x73a50e.
	DefaultSweepInterval = 1 * time.Minute
)

// Session models the in-memory session record stored in the global session map.
// Recovers exact 40-byte binary struct descriptor at VA 0x7d6ee0:
// - Field 0 (HDz5Nf, offset 0, 16 bytes): Username string
// - Field 1 (GkWDh_Jc_q, offset 16, 24 bytes): ExpiresAt time.Time
type Session struct {
	Username  string    `json:"username"`
	ExpiresAt time.Time `json:"expires_at"`
}
