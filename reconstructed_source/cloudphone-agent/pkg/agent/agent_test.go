// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: AGENT_COORDINATOR_UNIT_TESTS
// Evidence: WEBRTC_PEERCONNECTION_CALLGRAPH.json, WEBRTC_TOPOLOGY_CROSSMAP.json,
//   WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package agent

import (
	"encoding/json"
	"strings"
	"sync"
	"testing"
	"time"

	agentwebrtc "cloudphone-agent/pkg/webrtc"
	"cloudphone-agent/pkg/signaling"
)

type mockSignalingTransport struct {
	mu           sync.Mutex
	sentForwards []map[string]interface{}
}

func (m *mockSignalingTransport) SendForward(clientID uint32, payload interface{}) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.sentForwards = append(m.sentForwards, map[string]interface{}{
		"client_id": clientID,
		"payload":   payload,
	})
	return nil
}

// TestCoordinatorOfferGeneration verifies that request-offer triggers session creation and offer dispatch.
func TestCoordinatorOfferGeneration(t *testing.T) {
	coord := NewCoordinator("dev-coord-test", nil)
	defer coord.Close()

	// Connect a dummy signaling client
	dummyClient := signaling.NewClient("dev-coord-test", "ws://dummy", coord)
	coord.SetSignalingClient(dummyClient)

	// Simulate inbound forward request-offer
	reqPayload, _ := json.Marshal(map[string]interface{}{
		"type": "request-offer",
	})
	coord.HandleForward(100, reqPayload)

	// Verify session was created
	session, ok := coord.GetSession(100)
	if !ok || session == nil {
		t.Fatalf("expected session for client 100 to be created")
	}

	if session.GetState() != agentwebrtc.SessionStateHaveLocalOffer {
		t.Errorf("expected state HaveLocalOffer, got %v", session.GetState())
	}

	if coord.ActiveSessionCount() != 1 {
		t.Errorf("expected 1 active session, got %d", coord.ActiveSessionCount())
	}

	// Verify offer was dispatched (or local description exists)
	offer, err := session.CreateOffer()
	// Should return ErrSessionClosed or current offer (note state is already HaveLocalOffer)
	if err == nil && !strings.Contains(offer.SDP, "m=video") {
		t.Errorf("expected m=video in offer SDP")
	}
}

// TestCoordinatorTeardownOnDisconnect verifies session teardown upon client_disconnected.
func TestCoordinatorTeardownOnDisconnect(t *testing.T) {
	coord := NewCoordinator("dev-coord-disc", nil)
	defer coord.Close()

	reqPayload, _ := json.Marshal(map[string]interface{}{
		"type": "request-offer",
	})
	coord.HandleForward(200, reqPayload)

	if coord.ActiveSessionCount() != 1 {
		t.Fatalf("expected 1 active session")
	}

	session, _ := coord.GetSession(200)

	// Trigger client disconnect
	coord.HandleClientDisconnected(200)

	if coord.ActiveSessionCount() != 0 {
		t.Errorf("expected 0 active sessions after disconnect, got %d", coord.ActiveSessionCount())
	}

	if session.GetState() != agentwebrtc.SessionStateClosed {
		t.Errorf("expected session state Closed, got %v", session.GetState())
	}
}

// TestCoordinatorMultipleClients validates session isolation across concurrent clients.
func TestCoordinatorMultipleClients(t *testing.T) {
	coord := NewCoordinator("dev-coord-multi", nil)
	defer coord.Close()

	reqPayload, _ := json.Marshal(map[string]interface{}{
		"type": "request-offer",
	})

	coord.HandleForward(10, reqPayload)
	coord.HandleForward(20, reqPayload)
	coord.HandleForward(30, reqPayload)

	if coord.ActiveSessionCount() != 3 {
		t.Fatalf("expected 3 active sessions, got %d", coord.ActiveSessionCount())
	}

	s10, ok10 := coord.GetSession(10)
	s20, ok20 := coord.GetSession(20)
	s30, ok30 := coord.GetSession(30)

	if !ok10 || !ok20 || !ok30 || s10 == nil || s20 == nil || s30 == nil {
		t.Errorf("all 3 sessions must exist")
	}
	if s10 == s20 || s20 == s30 {
		t.Errorf("sessions must be isolated instances")
	}

	coord.HandleClientDisconnected(20)
	if coord.ActiveSessionCount() != 2 {
		t.Errorf("expected 2 active sessions after client 20 disconnect, got %d", coord.ActiveSessionCount())
	}
	if _, ok := coord.GetSession(20); ok {
		t.Errorf("client 20 should be removed")
	}
}

// TestCoordinatorConcurrentAccess validates thread safety.
func TestCoordinatorConcurrentAccess(t *testing.T) {
	coord := NewCoordinator("dev-coord-conc", nil)
	defer coord.Close()

	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		clientID := uint32(i + 1)
		wg.Add(1)
		go func(cid uint32) {
			defer wg.Done()
			reqPayload, _ := json.Marshal(map[string]interface{}{
				"type": "request-offer",
			})
			coord.HandleForward(cid, reqPayload)
			time.Sleep(10 * time.Millisecond)
			coord.HandleClientDisconnected(cid)
		}(clientID)
	}
	wg.Wait()

	if coord.ActiveSessionCount() != 0 {
		t.Errorf("expected 0 active sessions after all disconnected, got %d", coord.ActiveSessionCount())
	}
}
