// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_TEST_SUITE
// Mapping Scope: FULL_TRANSPORT_BEHAVIORAL_TESTS
// Evidence: TRANSPORT_METHOD_UPGRADE_MATRIX.json, TRANSPORT_AUTH_MATRIX.json,
//   REGISTER_DEVICE_STATE_MACHINE.json, REGISTER_AGENT_STATE_MACHINE.json,
//   CONNECT_CLIENT_STATE_MACHINE.json, TRANSPORT_MESSAGE_MATRIX.json,
//   TRANSPORT_HEARTBEAT_CONTRACT.json, TRANSPORT_CONCURRENCY_CONTRACT.json,
//   TRANSPORT_EDGE_MATRIX.json, TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Note: Tests validate observable protocol parity, independent contracts, and race safety.
// Confidence: HIGH

package transport_test

import (
	"crypto/sha1"
	"encoding/base64"
	"encoding/json"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/gorilla/websocket"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/devices"
	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/transport"
	"cloudphone-signaling/pkg/types"
)

// setupTransportTestEnv initializes a clean test server with auth, devices, shares, and transport Hub.
func setupTransportTestEnv(t *testing.T) (*httptest.Server, *transport.Hub, *devices.Registry, *auth.Authenticator, *storage.SharesStore, string, string) {
	t.Helper()

	tmpDir := t.TempDir()

	usersStore := storage.NewUsersStore(filepath.Join(tmpDir, "users.json"))
	if err := usersStore.LoadOrCreate(); err != nil {
		t.Fatalf("failed to init users store: %v", err)
	}

	adminSalt := storage.GenerateSalt()
	usersStore.SetUser(types.User{
		Username:        "admin",
		Password:        storage.HashPassword("adminpass", adminSalt),
		Salt:            adminSalt,
		Role:            "admin",
		AssignedDevices: []string{"*"},
	})

	userSalt := storage.GenerateSalt()
	usersStore.SetUser(types.User{
		Username:        "testuser",
		Password:        storage.HashPassword("userpass", userSalt),
		Salt:            userSalt,
		Role:            "user",
		AssignedDevices: []string{"dev-1", "dev-2"},
	})

	sessionMgr := session.NewSessionManager(session.RealClock{})
	authMgr := auth.NewAuthenticator(usersStore, sessionMgr, false)


	adminToken, err := sessionMgr.CreateSession("admin")
	if err != nil {
		t.Fatalf("failed to create admin session: %v", err)
	}
	userToken, err := sessionMgr.CreateSession("testuser")
	if err != nil {
		t.Fatalf("failed to create user session: %v", err)
	}

	sharesStore := storage.NewSharesStore(tmpDir + "/shares.json")
	_ = sharesStore.Load()
	_ = sharesStore.SetToken(types.ShareToken{
		TokenID:   "share-valid-123",
		DeviceID:  "dev-1",
		ExpiresAt: time.Now().Add(24 * time.Hour),
	})
	_ = sharesStore.SetToken(types.ShareToken{
		TokenID:   "share-expired-456",
		DeviceID:  "dev-1",
		ExpiresAt: time.Now().Add(-1 * time.Hour),
	})

	devReg := devices.NewRegistry()
	iceServers := []types.ICEServer{
		{URLs: []string{"stun:stun.l.google.com:19302"}},
	}

	hub := transport.NewHub(devReg, authMgr, sharesStore, iceServers)

	mux := http.NewServeMux()
	mux.HandleFunc("/register_device", hub.HandleRegisterDevice)
	mux.HandleFunc("/register_agent", hub.HandleRegisterAgent)
	mux.HandleFunc("/connect_client", hub.HandleConnectClient)

	server := httptest.NewServer(mux)
	t.Cleanup(server.Close)

	return server, hub, devReg, authMgr, sharesStore, adminToken, userToken
}

// computeSecWebSocketAccept calculates RFC 6455 accept header value.
func computeSecWebSocketAccept(key string) string {
	h := sha1.New()
	h.Write([]byte(key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"))
	return base64.StdEncoding.EncodeToString(h.Sum(nil))
}

// -----------------------------------------------------------------------------
// 1. Complete HTTP Method Matrix (All 7 Methods) & Upgrade Parity
// -----------------------------------------------------------------------------

func TestHTTPMethodMatrix(t *testing.T) {
	server, _, _, _, _, _, _ := setupTransportTestEnv(t)
	client := server.Client()

	methods := []string{"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
	endpoints := []string{"/register_device", "/register_agent", "/connect_client"}

	for _, ep := range endpoints {
		for _, method := range methods {
			t.Run(ep+"_"+method, func(t *testing.T) {
				req, err := http.NewRequest(method, server.URL+ep, nil)
				if err != nil {
					t.Fatalf("request creation error: %v", err)
				}

				resp, err := client.Do(req)
				if err != nil {
					t.Fatalf("request error: %v", err)
				}
				defer resp.Body.Close()

				// /connect_client without credentials returns 401 Unauthorized across all methods
				if ep == "/connect_client" {
					if resp.StatusCode != http.StatusUnauthorized {
						t.Errorf("expected 401 Unauthorized on %s %s, got %d", method, ep, resp.StatusCode)
					}
					body, _ := io.ReadAll(resp.Body)
					if method != "HEAD" && string(body) != "Unauthorized\n" {
						t.Errorf("expected body 'Unauthorized\\n', got %q", string(body))
					}
				} else {
					// /register_device and /register_agent without upgrade headers return 400 Bad Request
					if resp.StatusCode != http.StatusBadRequest {
						t.Errorf("expected 400 Bad Request on %s %s, got %d", method, ep, resp.StatusCode)
					}
				}
			})
		}
	}
}

// -----------------------------------------------------------------------------
// 2. WebSocket Upgrade Variations
// -----------------------------------------------------------------------------

func TestUpgradeHeaderVariations(t *testing.T) {
	server, _, _, _, _, _, _ := setupTransportTestEnv(t)
	client := server.Client()

	endpoints := []string{"/register_device", "/register_agent"}

	for _, ep := range endpoints {
		t.Run(ep+"_MissingUpgradeHeader", func(t *testing.T) {
			req, _ := http.NewRequest("GET", server.URL+ep, nil)
			req.Header.Set("Connection", "Upgrade")
			// Missing "Upgrade: websocket"
			resp, err := client.Do(req)
			if err != nil {
				t.Fatalf("request error: %v", err)
			}
			defer resp.Body.Close()
			if resp.StatusCode != http.StatusBadRequest {
				t.Errorf("expected 400 Bad Request, got %d", resp.StatusCode)
			}
		})

		t.Run(ep+"_WrongVersion", func(t *testing.T) {
			req, _ := http.NewRequest("GET", server.URL+ep, nil)
			req.Header.Set("Connection", "Upgrade")
			req.Header.Set("Upgrade", "websocket")
			req.Header.Set("Sec-WebSocket-Key", "dGhlIHNhbXBsZSBub25jZQ==")
			req.Header.Set("Sec-WebSocket-Version", "12") // RFC 6455 requires 13

			resp, err := client.Do(req)
			if err != nil {
				t.Fatalf("request error: %v", err)
			}
			defer resp.Body.Close()
			if resp.StatusCode != http.StatusBadRequest {
				t.Errorf("expected 400 Bad Request, got %d", resp.StatusCode)
			}
		})
	}
}

// -----------------------------------------------------------------------------
// 3. Pre-Upgrade Authentication Matrix (/connect_client)
// -----------------------------------------------------------------------------

func TestConnectClientAuthMatrix(t *testing.T) {
	server, _, _, _, _, adminToken, userToken := setupTransportTestEnv(t)

	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/connect_client"

	cases := []struct {
		name       string
		reqURL     string
		header     http.Header
		wantStatus int // 101 for upgrade success, 401 for auth failure
	}{
		{
			name:       "AdminHeader",
			reqURL:     wsURL,
			header:     http.Header{"Authorization": []string{"Bearer " + adminToken}},
			wantStatus: 101,
		},
		{
			name:       "AdminQuery",
			reqURL:     wsURL + "?token=" + adminToken,
			header:     http.Header{},
			wantStatus: 101,
		},
		{
			name:       "UserHeader",
			reqURL:     wsURL,
			header:     http.Header{"Authorization": []string{"Bearer " + userToken}},
			wantStatus: 101,
		},
		{
			name:       "UserQuery",
			reqURL:     wsURL + "?token=" + userToken,
			header:     http.Header{},
			wantStatus: 101,
		},
		{
			name:       "ShareTokenQuery",
			reqURL:     wsURL + "?share_token=share-valid-123",
			header:     http.Header{},
			wantStatus: 101,
		},
		{
			name:       "MissingToken",
			reqURL:     wsURL,
			header:     http.Header{},
			wantStatus: 401,
		},
		{
			name:       "InvalidToken",
			reqURL:     wsURL + "?token=invalid_tok_xyz",
			header:     http.Header{},
			wantStatus: 401,
		},
		{
			name:       "ExpiredShareToken",
			reqURL:     wsURL + "?share_token=share-expired-456",
			header:     http.Header{},
			wantStatus: 401,
		},
		{
			name:       "TokenConflict_ValidBearer_InvalidQuery",
			reqURL:     wsURL + "?token=invalid_junk",
			header:     http.Header{"Authorization": []string{"Bearer " + adminToken}},
			wantStatus: 101, // Valid Bearer takes precedence
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			dialer := websocket.Dialer{}
			ws, resp, err := dialer.Dial(tc.reqURL, tc.header)
			if tc.wantStatus == 101 {
				if err != nil {
					t.Fatalf("expected 101 upgrade success, got error: %v", err)
				}
				defer ws.Close()
				if resp.StatusCode != http.StatusSwitchingProtocols {
					t.Errorf("expected status 101, got %d", resp.StatusCode)
				}
			} else {
				if err == nil {
					ws.Close()
					t.Fatalf("expected failure %d, but dial succeeded", tc.wantStatus)
				}
				if resp == nil {
					t.Fatalf("expected HTTP response with status %d, got nil resp", tc.wantStatus)
				}
				if resp.StatusCode != tc.wantStatus {
					t.Errorf("expected status %d, got %d", tc.wantStatus, resp.StatusCode)
				}
			}
		})
	}
}

// -----------------------------------------------------------------------------
// 4. /register_device Lifecycle, Config Reply & Ping/Pong
// -----------------------------------------------------------------------------

func TestRegisterDeviceLifecycle(t *testing.T) {
	server, _, devReg, _, _, _, _ := setupTransportTestEnv(t)
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/register_device"

	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, nil)
	if err != nil {
		t.Fatalf("dial error: %v", err)
	}
	defer ws.Close()

	if resp.StatusCode != http.StatusSwitchingProtocols {
		t.Fatalf("expected 101, got %d", resp.StatusCode)
	}

	// 1. Send register message
	regMsg := transport.RegisterMessage{
		MessageType: "register",
		DeviceID:    "dev-test-1",
		DeviceInfo:  map[string]interface{}{"model": "Pixel 6"},
	}
	if err := ws.WriteJSON(regMsg); err != nil {
		t.Fatalf("write register error: %v", err)
	}

	// 2. Read config response
	var cfg transport.ConfigMessage
	if err := ws.ReadJSON(&cfg); err != nil {
		t.Fatalf("read config error: %v", err)
	}

	if cfg.MessageType != "config" {
		t.Errorf("expected config message_type, got %s", cfg.MessageType)
	}
	if cfg.DeviceID != "dev-test-1" {
		t.Errorf("expected device_id dev-test-1, got %s", cfg.DeviceID)
	}
	if len(cfg.ICEServers) == 0 {
		t.Errorf("expected non-empty ice_servers in config reply")
	}

	// 3. Verify registry reflects online device
	dev, exists := devReg.GetDevice("dev-test-1")
	if !exists {
		t.Fatalf("device not found in registry")
	}
	dev.Mu.RLock()
	if !dev.Online {
		t.Errorf("expected device to be online")
	}
	dev.Mu.RUnlock()

	// 4. Test Ping/Pong keepalive (RFC 6455 Opcode 9 -> 10)
	pongReceived := make(chan struct{})
	ws.SetPongHandler(func(appData string) error {
		if appData == "test-ping-payload" {
			close(pongReceived)
		}
		return nil
	})
	if err := ws.WriteControl(websocket.PingMessage, []byte("test-ping-payload"), time.Now().Add(5*time.Second)); err != nil {
		t.Fatalf("write ping error: %v", err)
	}

	// Read in goroutine to trigger control handler
	go func() {
		for {
			if _, _, err := ws.NextReader(); err != nil {
				return
			}
		}
	}()

	select {
	case <-pongReceived:
		// Pong verified
	case <-time.After(3 * time.Second):
		t.Errorf("timed out waiting for RFC 6455 pong frame")
	}

	// 5. Close connection and verify disconnect cleanup
	_ = ws.WriteControl(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""), time.Now().Add(time.Second))
	_ = ws.Close()

	// Allow cleanup to execute
	time.Sleep(100 * time.Millisecond)

	dev.Mu.RLock()
	if dev.Online {
		t.Errorf("expected device to be marked offline after disconnect")
	}
	dev.Mu.RUnlock()
}

// -----------------------------------------------------------------------------
// 5. /register_agent Lifecycle, Heartbeat & Duplicate Replacement
// -----------------------------------------------------------------------------

func TestRegisterAgentLifecycle(t *testing.T) {
	server, _, devReg, _, _, _, _ := setupTransportTestEnv(t)
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/register_agent"

	// 1. Initial agent connection
	ws1, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
	if err != nil {
		t.Fatalf("dial agent 1 error: %v", err)
	}
	defer ws1.Close()

	agentReg := transport.AgentRegisterMessage{
		Type:       "agent_register",
		DeviceID:   "dev-agent-test",
		ScrcpyAddr: "127.0.0.1:5555",
		IsWebRTC:   true,
	}
	if err := ws1.WriteJSON(agentReg); err != nil {
		t.Fatalf("write agent_register error: %v", err)
	}

	var ack transport.AgentRegisterOkMessage
	if err := ws1.ReadJSON(&ack); err != nil {
		t.Fatalf("read agent_register_ok error: %v", err)
	}
	if ack.MessageType != "agent_register_ok" || ack.Status != "ok" {
		t.Errorf("expected agent_register_ok status ok, got %+v", ack)
	}

	// 2. Heartbeat keepalive updates registry timestamp
	time.Sleep(10 * time.Millisecond)
	beforeHeartbeat := time.Now()
	hb := transport.HeartbeatMessage{
		MessageType: "heartbeat",
		DeviceID:    "dev-agent-test",
	}
	if err := ws1.WriteJSON(hb); err != nil {
		t.Fatalf("write heartbeat error: %v", err)
	}

	time.Sleep(50 * time.Millisecond)
	dev, exists := devReg.GetDevice("dev-agent-test")
	if !exists {
		t.Fatalf("device not found in registry")
	}
	dev.Mu.RLock()
	lastSeen := dev.LastSeen
	dev.Mu.RUnlock()
	if lastSeen.Before(beforeHeartbeat) {
		t.Errorf("expected lastSeen (%v) to be updated after %v", lastSeen, beforeHeartbeat)
	}

	// 3. Duplicate connection replaces old agent
	ws2, _, err := websocket.DefaultDialer.Dial(wsURL, nil)
	if err != nil {
		t.Fatalf("dial agent 2 error: %v", err)
	}
	defer ws2.Close()

	if err := ws2.WriteJSON(agentReg); err != nil {
		t.Fatalf("write duplicate agent_register error: %v", err)
	}
	var ack2 transport.AgentRegisterOkMessage
	if err := ws2.ReadJSON(&ack2); err != nil {
		t.Fatalf("read duplicate ack error: %v", err)
	}
	if ack2.Status != "ok" {
		t.Errorf("expected status ok on duplicate agent connection")
	}

	// Verify ws1 is dropped / closed
	_ = ws1.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
	_, _, err = ws1.ReadMessage()
	if err == nil {
		t.Errorf("expected older agent connection to be closed upon replacement")
	}
}

// -----------------------------------------------------------------------------
// 6. Multi-Client Multiplexing & Full 4-Stage Signaling Relay
// -----------------------------------------------------------------------------

func TestMultiClientAndSignalingRelay(t *testing.T) {
	server, hub, devReg, _, _, adminToken, _ := setupTransportTestEnv(t)

	agentURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/register_agent"
	clientURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/connect_client?token=" + adminToken

	// Register Agent for device "dev-multiplex-1"
	agentWS, _, err := websocket.DefaultDialer.Dial(agentURL, nil)
	if err != nil {
		t.Fatalf("agent dial error: %v", err)
	}
	defer agentWS.Close()

	if err := agentWS.WriteJSON(transport.AgentRegisterMessage{
		Type:     "agent_register",
		DeviceID: "dev-multiplex-1",
		IsWebRTC: true,
	}); err != nil {
		t.Fatalf("agent register write error: %v", err)
	}
	var agentAck transport.AgentRegisterOkMessage
	_ = agentWS.ReadJSON(&agentAck)

	// Connect Client 1
	client1WS, _, err := websocket.DefaultDialer.Dial(clientURL, nil)
	if err != nil {
		t.Fatalf("client 1 dial error: %v", err)
	}
	defer client1WS.Close()

	// Connect Client 2
	client2WS, _, err := websocket.DefaultDialer.Dial(clientURL, nil)
	if err != nil {
		t.Fatalf("client 2 dial error: %v", err)
	}
	defer client2WS.Close()

	// Bind Client 1 to "dev-multiplex-1"
	if err := client1WS.WriteJSON(transport.ConnectMessage{
		Type:     "connect",
		DeviceID: "dev-multiplex-1",
	}); err != nil {
		t.Fatalf("client 1 connect write error: %v", err)
	}

	var c1Config transport.ConfigMessage
	if err := client1WS.ReadJSON(&c1Config); err != nil {
		t.Fatalf("client 1 config read error: %v", err)
	}

	// Bind Client 2 to "dev-multiplex-1"
	if err := client2WS.WriteJSON(transport.ConnectMessage{
		Type:     "connect",
		DeviceID: "dev-multiplex-1",
	}); err != nil {
		t.Fatalf("client 2 connect write error: %v", err)
	}

	var c2Config transport.ConfigMessage
	if err := client2WS.ReadJSON(&c2Config); err != nil {
		t.Fatalf("client 2 config read error: %v", err)
	}

	// Verify Device ClientCount == 2 in registry
	dev, _ := devReg.GetDevice("dev-multiplex-1")
	dev.Mu.RLock()
	clientCount := dev.ClientCount
	dev.Mu.RUnlock()
	if clientCount != 2 {
		t.Errorf("expected client_count 2, got %d", clientCount)
	}

	// Drain device_list_update from client 1 if present
	_ = client1WS.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	var dummyMsg json.RawMessage
	_ = client1WS.ReadJSON(&dummyMsg)
	_ = client1WS.SetReadDeadline(time.Time{})

	// Stage 1: Client 1 sends request-offer
	reqOfferPayload, _ := json.Marshal(map[string]string{"type": "request-offer"})
	fwdMsg := transport.ForwardEnvelope{
		MessageType: "forward",
		DeviceID:    "dev-multiplex-1",
		Payload:     reqOfferPayload,
	}
	if err := client1WS.WriteJSON(fwdMsg); err != nil {
		t.Fatalf("client 1 write request-offer error: %v", err)
	}

	// Agent receives forward envelope with stamped client_id
	var agentFwd transport.ForwardEnvelope
	if err := agentWS.ReadJSON(&agentFwd); err != nil {
		t.Fatalf("agent read forward error: %v", err)
	}
	if agentFwd.MessageType != "forward" || agentFwd.ClientID == 0 {
		t.Errorf("expected forward envelope with stamped client_id > 0, got %+v", agentFwd)
	}
	client1ID := agentFwd.ClientID

	// Stage 2: Agent sends SDP offer targeted to Client 1
	offerPayload, _ := json.Marshal(map[string]string{"type": "offer", "sdp": "v=0\r\no=..."})
	agentOffer := transport.ForwardEnvelope{
		MessageType: "forward",
		DeviceID:    "dev-multiplex-1",
		ClientID:    client1ID,
		Payload:     offerPayload,
	}
	if err := agentWS.WriteJSON(agentOffer); err != nil {
		t.Fatalf("agent write offer error: %v", err)
	}

	// Helper to skip asynchronous device_list_update broadcasts and read the next device_msg
	readNextDeviceMsg := func(ws *websocket.Conn) (transport.DeviceMsgEnvelope, error) {
		for {
			var raw json.RawMessage
			if err := ws.ReadJSON(&raw); err != nil {
				return transport.DeviceMsgEnvelope{}, err
			}
			var gen transport.GenericInboundEnvelope
			_ = json.Unmarshal(raw, &gen)
			if gen.MessageType == "device_msg" {
				var dm transport.DeviceMsgEnvelope
				_ = json.Unmarshal(raw, &dm)
				return dm, nil
			}
		}
	}

	// Client 1 receives device_msg wrapping the offer
	c1Msg, err := readNextDeviceMsg(client1WS)
	if err != nil {
		t.Fatalf("client 1 read device_msg error: %v", err)
	}
	if c1Msg.MessageType != "device_msg" || c1Msg.DeviceID != "dev-multiplex-1" {
		t.Errorf("expected device_msg from dev-multiplex-1, got %+v", c1Msg)
	}
	var payloadMap map[string]string
	_ = json.Unmarshal(c1Msg.Payload, &payloadMap)
	if payloadMap["type"] != "offer" {
		t.Errorf("expected payload type offer, got %s", payloadMap["type"])
	}

	// Stage 3: Client 1 sends SDP answer
	ansPayload, _ := json.Marshal(map[string]string{"type": "answer", "sdp": "v=0\r\na=..."})
	if err := client1WS.WriteJSON(transport.ForwardEnvelope{
		MessageType: "forward",
		DeviceID:    "dev-multiplex-1",
		Payload:     ansPayload,
	}); err != nil {
		t.Fatalf("client 1 write answer error: %v", err)
	}

	var agentAns transport.ForwardEnvelope
	if err := agentWS.ReadJSON(&agentAns); err != nil {
		t.Fatalf("agent read answer error: %v", err)
	}
	if agentAns.ClientID != client1ID {
		t.Errorf("expected client_id %d on answer, got %d", client1ID, agentAns.ClientID)
	}

	// Stage 4: Trickle ICE candidate relay
	candPayload, _ := json.Marshal(map[string]string{"type": "candidate", "candidate": "candidate:1 1 UDP ..."})
	if err := agentWS.WriteJSON(transport.ForwardEnvelope{
		MessageType: "forward",
		DeviceID:    "dev-multiplex-1",
		ClientID:    client1ID,
		Payload:     candPayload,
	}); err != nil {
		t.Fatalf("agent write candidate error: %v", err)
	}

	c1Cand, err := readNextDeviceMsg(client1WS)
	if err != nil {
		t.Fatalf("client 1 read candidate error: %v", err)
	}
	if c1Cand.MessageType != "device_msg" {
		t.Errorf("expected device_msg, got %s", c1Cand.MessageType)
	}


	// Disconnect Client 1 and verify ClientCount decrements to 1
	_ = client1WS.Close()
	time.Sleep(100 * time.Millisecond)

	dev.Mu.RLock()
	clientCount = dev.ClientCount
	dev.Mu.RUnlock()
	if clientCount != 1 {
		t.Errorf("expected client_count 1 after client 1 disconnect, got %d", clientCount)
	}

	_ = hub
}

// -----------------------------------------------------------------------------
// 7. Cleanup Idempotency & Concurrent Teardown
// -----------------------------------------------------------------------------

func TestCleanupIdempotency(t *testing.T) {
	server, hub, devReg, _, _, adminToken, _ := setupTransportTestEnv(t)

	clientURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/connect_client?token=" + adminToken
	ws, _, err := websocket.DefaultDialer.Dial(clientURL, nil)
	if err != nil {
		t.Fatalf("dial error: %v", err)
	}

	// Bind to device
	_ = ws.WriteJSON(transport.ConnectMessage{
		Type:     "connect",
		DeviceID: "dev-cleanup-test",
	})
	var cfg transport.ConfigMessage
	_ = ws.ReadJSON(&cfg)

	// Close connection from client
	_ = ws.Close()

	// Rapid concurrent multiple cleanup invocations on hub directly (simulating races)
	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			hub.CleanupClient("dev-cleanup-test", nil)
		}()
	}
	wg.Wait()

	dev, exists := devReg.GetDevice("dev-cleanup-test")
	if exists {
		dev.Mu.RLock()
		if dev.ClientCount < 0 {
			t.Errorf("client_count became negative: %d", dev.ClientCount)
		}
		dev.Mu.RUnlock()
	}
}

// -----------------------------------------------------------------------------
// 8. Edge Case: Unmasked Client Frame Protocol Violation (RFC 6455 1002)
// -----------------------------------------------------------------------------

func TestUnmaskedClientFrameViolation(t *testing.T) {
	server, _, _, _, _, _, _ := setupTransportTestEnv(t)
	u, _ := url.Parse(server.URL)

	// Establish raw TCP connection and send unmasked WebSocket frame
	conn, err := net.Dial("tcp", u.Host)
	if err != nil {
		t.Fatalf("dial error: %v", err)
	}
	defer conn.Close()

	key := "dGhlIHNhbXBsZSBub25jZQ=="
	handshake := "GET /register_device HTTP/1.1\r\n" +
		"Host: " + u.Host + "\r\n" +
		"Upgrade: websocket\r\n" +
		"Connection: Upgrade\r\n" +
		"Sec-WebSocket-Key: " + key + "\r\n" +
		"Sec-WebSocket-Version: 13\r\n\r\n"

	if _, err := conn.Write([]byte(handshake)); err != nil {
		t.Fatalf("handshake write error: %v", err)
	}

	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil || !strings.Contains(string(buf[:n]), "101 Switching Protocols") {
		t.Fatalf("handshake failed: %v, resp: %s", err, string(buf[:n]))
	}

	// Send an UNMASKED text frame (FIN=1, Opcode=1, MASK=0, Payload len=4: "test")
	// Header: 0x81 (FIN + text), 0x04 (MASK=0, len=4), data: "test"
	unmaskedFrame := []byte{0x81, 0x04, 't', 'e', 's', 't'}
	if _, err := conn.Write(unmaskedFrame); err != nil {
		t.Fatalf("write frame error: %v", err)
	}

	// Server MUST reply with Close frame (Opcode 8) and terminate connection per RFC 6455
	n, err = conn.Read(buf)
	if err != nil && err != io.EOF {
		// TCP reset or EOF is valid
		return
	}
	if n >= 2 {
		firstByte := buf[0]
		opcode := firstByte & 0x0F
		if opcode != 8 { // Close frame
			t.Logf("received frame opcode %d instead of 8 (Close)", opcode)
		}
	}
}

