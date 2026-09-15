// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: provides clock abstraction to enable deterministic TTL expiration testing
// Confidence: N/A

package session

import (
	"time"
)

// Clock defines a time source for session management.
type Clock interface {
	Now() time.Time
}

// RealClock provides real wall-clock time using time.Now, matching original production binary runtime.
type RealClock struct{}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: returns time.Now()
// Confidence: N/A
func (RealClock) Now() time.Time {
	return time.Now()
}

// MockClock provides a controllable clock for deterministic testing of session TTL expiration.
type MockClock struct {
	current time.Time
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: constructs MockClock with initial time
// Confidence: N/A
func NewMockClock(initial time.Time) *MockClock {
	return &MockClock{current: initial}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: returns mock current time
// Confidence: N/A
func (m *MockClock) Now() time.Time {
	return m.current
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: sets mock current time
// Confidence: N/A
func (m *MockClock) Set(t time.Time) {
	m.current = t
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: advances mock time by duration
// Confidence: N/A
func (m *MockClock) Add(d time.Duration) {
	m.current = m.current.Add(d)
}
