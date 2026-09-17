// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: SIGNALING_CLIENT_UNIT_AND_LIFECYCLE_TESTS
// Evidence: TRANSPORT_MESSAGE_MATRIX.json, TRANSPORT_HEARTBEAT_CONTRACT.json,
//   WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package signaling

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
)

type mockInboundHandler struct {
	mu           sync.Mutex
	forwards     []map[string]interface{}
	disconnects  []uint32
	configEvents [][]webrtc.ICEServer
}

func (m *mockInboundHandler) HandleForward(clientID uint32, payload json.RawMessage) {
	m.mu.Lock()
	defer m.mu.Unlock()
	var parsed map[string]interface{}
	_ = json.Unmarshal(payload, &parsed)
	m.forwards = append(m.forwards, map[string]interface{}{
		"client_id": clientID,
		"payload":   parsed,
	})
}

func (m *mockInboundHandler) HandleClientDisconnected(clientID uint32) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.disconnects = append(m.disconnects, clientID)
}

func (m *mockInboundHandler) HandleConfig(iceServers []webrtc.ICEServer) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.configEvents = append(m.configEvents, iceServers)
}

// TestSignalingClientRegistration validates handshake and registration flow matching TR-DIFF-AGT-REGISTER-OK.
func TestSignalingClientRegistration(t *testing.T) {
	upgrader := websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}

	var regReceived bool
	var mu sync.Mutex

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ws, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			return
		}
		defer ws.Close()

		// Read agent_register frame
		_, data, err := ws.ReadMessage()
		if err != nil {
			return
		}

		var reg struct {
			Type     string `json:"type"`
			DeviceID string `json:"device_id"`
			IsWebRTC bool   `json:"is_webrtc"`
		}
		if err := json.Unmarshal(data, &reg); err == nil && reg.Type == "agent_register" && reg.DeviceID == "dev-test-reg" && reg.IsWebRTC {
			mu.Lock()
			regReceived = true
			mu.Unlock()

			// Send agent_register_ok
			_ = ws.WriteJSON(map[string]interface{}{
				"message_type": "agent_register_ok",
				"status":       "valid",
			})
		}

		// Keep open until client disconnects
		for {
			if _, _, err := ws.ReadMessage(); err != nil {
				break
			}
		}
	}))
	defer server.Close()

	wsURL := "ws" + strings.TrimPrefix(server.URL, "http")
	handler := &mockInboundHandler{}
	client := NewClient("dev-test-reg", wsURL, handler)

	if err := client.Connect(); err != nil {
		t.Fatalf("client.Connect failed: %v", err)
	}
	defer client.Close()

	mu.Lock()
	received := regReceived
	mu.Unlock()

	if !received {
		t.Errorf("server did not receive expected agent_register payload")
	}
}

// TestSignalingClientForwardAndDisconnect validates message dispatching to InboundHandler.
func TestSignalingClientForwardAndDisconnect(t *testing.T) {
	upgrader := websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ws, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			return
		}
		defer ws.Close()

		// Handshake
		_, _, _ = ws.ReadMessage()
		_ = ws.WriteJSON(map[string]interface{}{
			"message_type": "agent_register_ok",
			"status":       "valid",
		})

		// Send config
		_ = ws.WriteJSON(map[string]interface{}{
			"message_type": "config",
			"ice_servers": []map[string]interface{}{
				{"urls": "stun:stun.example.com:19302"},
			},
		})

		// Send forward request-offer
		_ = ws.WriteJSON(map[string]interface{}{
			"message_type": "forward",
			"device_id":    "dev-fwd-test",
			"client_id":    uint32(77),
			"payload": map[string]interface{}{
				"type": "request-offer",
			},
		})

		// Send client_disconnected
		_ = ws.WriteJSON(map[string]interface{}{
			"message_type": "client_disconnected",
			"device_id":    "dev-fwd-test",
			"client_id":    uint32(77),
		})

		// Read client responses
		for {
			if _, _, err := ws.ReadMessage(); err != nil {
				break
			}
		}
	}))
	defer server.Close()

	wsURL := "ws" + strings.TrimPrefix(server.URL, "http")
	handler := &mockInboundHandler{}
	client := NewClient("dev-fwd-test", wsURL, handler)

	if err := client.Connect(); err != nil {
		t.Fatalf("client.Connect failed: %v", err)
	}
	defer client.Close()

	// Allow read pump to process inbound messages
	time.Sleep(100 * time.Millisecond)

	handler.mu.Lock()
	defer handler.mu.Unlock()

	if len(handler.configEvents) == 0 {
		t.Errorf("expected config event, got none")
	}
	if len(handler.forwards) == 0 {
		t.Fatalf("expected forward event, got none")
	}
	if handler.forwards[0]["client_id"] != uint32(77) {
		t.Errorf("expected client_id 77, got %v", handler.forwards[0]["client_id"])
	}
	if len(handler.disconnects) == 0 || handler.disconnects[0] != uint32(77) {
		t.Errorf("expected client_disconnected for client 77")
	}
}

// TestSignalingClientHeartbeatEmission validates heartbeat keepalive emission.
func TestSignalingClientHeartbeatEmission(t *testing.T) {
	upgrader := websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}

	var hbReceived bool
	var mu sync.Mutex

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ws, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			return
		}
		defer ws.Close()

		// Handshake
		_, _, _ = ws.ReadMessage()
		_ = ws.WriteJSON(map[string]interface{}{
			"message_type": "agent_register_ok",
			"status":       "valid",
		})

		for {
			_, data, err := ws.ReadMessage()
			if err != nil {
				break
			}
			var hb struct {
				MessageType string `json:"message_type"`
				DeviceID    string `json:"device_id"`
			}
			if err := json.Unmarshal(data, &hb); err == nil && hb.MessageType == "heartbeat" {
				mu.Lock()
				hbReceived = true
				mu.Unlock()
				break
			}
		}
	}))
	defer server.Close()

	wsURL := "ws" + strings.TrimPrefix(server.URL, "http")
	client := NewClient("dev-hb-test", wsURL, nil)

	if err := client.Connect(); err != nil {
		t.Fatalf("client.Connect failed: %v", err)
	}
	defer client.Close()

	// Send an explicit heartbeat
	if err := client.SendHeartbeat(); err != nil {
		t.Fatalf("SendHeartbeat failed: %v", err)
	}

	time.Sleep(50 * time.Millisecond)

	mu.Lock()
	received := hbReceived
	mu.Unlock()

	if !received {
		t.Errorf("server did not receive expected heartbeat message")
	}
}

// TestSignalingDisconnectDuringNegotiation tests socket termination while negotiation messages are in flight.
func TestSignalingDisconnectDuringNegotiation(t *testing.T) {
	upgrader := websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ws, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			return
		}
		// Read agent_register
		_, _, _ = ws.ReadMessage()
		_ = ws.WriteJSON(map[string]interface{}{
			"message_type": "agent_register_ok",
			"status":       "valid",
		})
		// Immediately close server socket during negotiation
		_ = ws.Close()
	}))
	defer server.Close()

	wsURL := "ws" + strings.TrimPrefix(server.URL, "http")
	client := NewClient("dev-disc-neg", wsURL, nil)

	if err := client.Connect(); err != nil {
		t.Fatalf("client.Connect failed: %v", err)
	}

	// Sending after server drop should fail safely without panic or deadlock
	time.Sleep(50 * time.Millisecond)
	_ = client.SendForward(999, map[string]interface{}{"type": "offer"})
	_ = client.SendHeartbeat()

	// Client close should be idempotent
	if err := client.Close(); err != nil {
		t.Errorf("expected clean close: %v", err)
	}
	_ = client.Close()
}

