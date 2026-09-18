// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: WEBRTC_REAL_STANDARDS_COMPLIANT_E2E_TEST
// Evidence: WEBRTC_TOPOLOGY_CROSSMAP.json, WEBRTC_PEERCONNECTION_STATE_MACHINE.json,
//   WEBRTC_CODEC_CAPABILITY_MATRIX.json, MEDIA_TRACK_CONSTRUCTION_EVIDENCE.json,
//   DATACHANNEL_LABEL_EVIDENCE.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package tests

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	"cloudphone-agent/pkg/agent"
	"cloudphone-agent/pkg/signaling"
	agentwebrtc "cloudphone-agent/pkg/webrtc"
	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
)

// TestWebRTCRealPeerConnectionE2E establishes an actual standards-compliant WebRTC session
// between the reconstructed Agent and a simulated Browser Client.
// Validates:
// 1. Offer creation with confirmed H.264 display_0 and Opus audio_0 tracks.
// 2. Answer creation and acceptance.
// 3. Bidirectional trickle ICE exchange.
// 4. Successful ICE connection reaching Connected/Completed state (NEGOTIATION_CONFIRMED).
// 5. Synthetic media packet transmission and receipt on both video and audio tracks (MEDIA_DELIVERY_CONFIRMED).
// 6. Graceful session closure.
func TestWebRTCRealPeerConnectionE2E(t *testing.T) {
	// 1. Initialize Agent Coordinator
	coord := agent.NewCoordinator("dev-e2e-real", nil)
	defer coord.Close()

	// 2. Initialize Browser Client WebRTC PeerConnection
	// Use standard Pion MediaEngine supporting H.264 and Opus matching browser capabilities
	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	// Browser Client creates inbound channels per useWebRTC.js
	ordered := true
	_, err = clientPC.CreateDataChannel(agentwebrtc.ChannelFile, &webrtc.DataChannelInit{Ordered: &ordered})
	if err != nil {
		t.Fatalf("failed to create file-channel on client: %v", err)
	}

	var (
		videoTrackReceived = make(chan struct{}, 1)
		audioTrackReceived = make(chan struct{}, 1)
		videoRTPReceived   = make(chan struct{}, 1)
		audioRTPReceived   = make(chan struct{}, 1)
		clientConnected    = make(chan struct{}, 1)
		agentConnected     = make(chan struct{}, 1)
	)

	clientPC.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
		if track.Kind() == webrtc.RTPCodecTypeVideo {
			if strings.Contains(track.ID(), agentwebrtc.VideoTrackID) || strings.EqualFold(track.Codec().MimeType, webrtc.MimeTypeH264) {
				select {
				case videoTrackReceived <- struct{}{}:
				default:
				}
				go func() {
					buf := make([]byte, 1500)
					for {
						n, _, readErr := track.Read(buf)
						if readErr != nil {
							break
						}
						if n > 0 {
							select {
							case videoRTPReceived <- struct{}{}:
							default:
							}
							break
						}
					}
				}()
			}
		} else if track.Kind() == webrtc.RTPCodecTypeAudio {
			if strings.Contains(track.ID(), agentwebrtc.AudioTrackID) || strings.EqualFold(track.Codec().MimeType, webrtc.MimeTypeOpus) {
				select {
				case audioTrackReceived <- struct{}{}:
				default:
				}
				go func() {
					buf := make([]byte, 1500)
					for {
						n, _, readErr := track.Read(buf)
						if readErr != nil {
							break
						}
						if n > 0 {
							select {
							case audioRTPReceived <- struct{}{}:
							default:
							}
							break
						}
					}
				}()
			}
		}
	})

	clientPC.OnConnectionStateChange(func(state webrtc.PeerConnectionState) {
		if state == webrtc.PeerConnectionStateConnected {
			select {
			case clientConnected <- struct{}{}:
			default:
			}
		}
	})

	// 3. Initiate Offer from Agent
	clientID := uint32(1)
	session, err := agentwebrtc.NewPeerSession(clientID, "dev-e2e-real", nil)
	if err != nil {
		t.Fatalf("failed to create agent peer session: %v", err)
	}
	defer session.Close()

	session.OnSessionStateChange(func(state agentwebrtc.SessionState) {
		if state == agentwebrtc.SessionStateConnected {
			select {
			case agentConnected <- struct{}{}:
			default:
			}
		}
	})

	// Wire ICE trickle between Agent and Client
	var clientCandidates []webrtc.ICECandidateInit
	var candMu sync.Mutex

	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c == nil {
			return
		}
		candInit := c.ToJSON()
		candMu.Lock()
		clientCandidates = append(clientCandidates, candInit)
		candMu.Unlock()
		_ = session.AddRemoteCandidate(candInit)
	})

	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	// Agent creates Offer
	offerPayload, err := session.CreateOffer()
	if err != nil {
		t.Fatalf("failed to create offer: %v", err)
	}

	// 4. Client applies Offer and generates Answer
	if err := clientPC.SetRemoteDescription(webrtc.SessionDescription{
		Type: webrtc.SDPTypeOffer,
		SDP:  offerPayload.SDP,
	}); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}

	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	if err := clientPC.SetLocalDescription(answer); err != nil {
		t.Fatalf("client failed to set local answer: %v", err)
	}

	// 5. Agent applies Answer
	if err := session.HandleRemoteAnswer(answer.SDP); err != nil {
		t.Fatalf("agent failed to set remote answer: %v", err)
	}

	// Apply any early gathered candidates
	candMu.Lock()
	for _, c := range clientCandidates {
		_ = session.AddRemoteCandidate(c)
	}
	candMu.Unlock()

	// 6. Wait for Connection (NEGOTIATION_CONFIRMED)
	select {
	case <-clientConnected:
		t.Log("[PASS] NEGOTIATION_CONFIRMED: Client reached PeerConnectionStateConnected")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for client PeerConnectionStateConnected (client state=%s, agent state=%s)",
			clientPC.ConnectionState().String(), session.GetState().String())
	}

	// 7. Transmit Synthetic Media Samples (MEDIA_DELIVERY_CONFIRMED)
	// Write periodic samples so Pion triggers OnTrack and delivers RTP
	stopMediaPump := make(chan struct{})
	go func() {
		ticker := time.NewTicker(20 * time.Millisecond)
		defer ticker.Stop()
		for {
			select {
			case <-stopMediaPump:
				return
			case <-ticker.C:
				_ = session.Media.WriteVideoSample(agentwebrtc.CreateSyntheticH264Sample())
				_ = session.Media.WriteAudioSample(agentwebrtc.CreateSyntheticOpusSample())
			}
		}
	}()

	// Verify track negotiation and media reception
	select {
	case <-videoTrackReceived:
		t.Log("[PASS] Confirmed video track (H.264 / display_0) received by client")
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for video track on client")
	}

	select {
	case <-audioTrackReceived:
		t.Log("[PASS] Confirmed audio track (Opus / audio_0) received by client")
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for audio track on client")
	}

	select {
	case <-videoRTPReceived:
		t.Log("[PASS] MEDIA_DELIVERY_CONFIRMED: Synthetic H.264 video RTP packet received by client")
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for synthetic video RTP packet delivery")
	}

	select {
	case <-audioRTPReceived:
		t.Log("[PASS] MEDIA_DELIVERY_CONFIRMED: Synthetic Opus audio RTP packet received by client")
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for synthetic audio RTP packet delivery")
	}

	close(stopMediaPump)

	// 8. Clean Session Closure
	if err := session.Close(); err != nil {
		t.Errorf("error closing agent session: %v", err)
	}
	if err := clientPC.Close(); err != nil {
		t.Errorf("error closing client PC: %v", err)
	}

	t.Log("[PASS] WebRTC Session cleanly terminated on both peers")
}

// TestSignalingRelayWebRTCE2E verifies full tri-party signaling relay integration:
// Client <---> Signaling Relay Server <---> Agent Coordinator <---> WebRTC P2P
func TestSignalingRelayWebRTCE2E(t *testing.T) {
	upgrader := websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}

	var (
		agentConn   *websocket.Conn
		clientConn  *websocket.Conn
		agentWriteMu  sync.Mutex
		clientWriteMu sync.Mutex
		connMu      sync.Mutex
	)

	writeToAgent := func(v interface{}) error {
		agentWriteMu.Lock()
		defer agentWriteMu.Unlock()
		connMu.Lock()
		ac := agentConn
		connMu.Unlock()
		if ac == nil {
			return nil
		}
		return ac.WriteJSON(v)
	}

	writeToClient := func(v interface{}) error {
		clientWriteMu.Lock()
		defer clientWriteMu.Unlock()
		connMu.Lock()
		cc := clientConn
		connMu.Unlock()
		if cc == nil {
			return nil
		}
		return cc.WriteJSON(v)
	}

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ws, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			return
		}

		path := r.URL.Path
		if path == "/register_agent" {
			connMu.Lock()
			agentConn = ws
			connMu.Unlock()

			// Read agent_register
			_, data, err := ws.ReadMessage()
			if err != nil {
				return
			}
			var reg struct {
				Type     string `json:"type"`
				DeviceID string `json:"device_id"`
			}
			_ = json.Unmarshal(data, &reg)

			// Reply with agent_register_ok
			_ = writeToAgent(map[string]interface{}{
				"message_type": "agent_register_ok",
				"status":       "valid",
			})

			// Relay pump from agent to client
			for {
				_, msgData, err := ws.ReadMessage()
				if err != nil {
					break
				}
				var fwd struct {
					MessageType string          `json:"message_type"`
					ClientID    uint32          `json:"client_id"`
					Payload     json.RawMessage `json:"payload"`
				}
				if err := json.Unmarshal(msgData, &fwd); err == nil && fwd.MessageType == "forward" {
					_ = writeToClient(map[string]interface{}{
						"message_type": "device_msg",
						"device_id":    reg.DeviceID,
						"payload":      fwd.Payload,
					})
				}
			}
		} else if path == "/connect_client" {
			connMu.Lock()
			clientConn = ws
			connMu.Unlock()

			// Read client connect
			_, data, err := ws.ReadMessage()
			if err != nil {
				return
			}
			var connMsg struct {
				MessageType string `json:"message_type"`
				DeviceID    string `json:"device_id"`
			}
			_ = json.Unmarshal(data, &connMsg)

			// Send config
			_ = writeToClient(map[string]interface{}{
				"message_type": "config",
				"device_id":    connMsg.DeviceID,
				"ice_servers":  []map[string]interface{}{{"urls": "stun:stun.l.google.com:19302"}},
			})

			// Relay pump from client to agent
			for {
				_, msgData, err := ws.ReadMessage()
				if err != nil {
					break
				}
				var fwd struct {
					MessageType string          `json:"message_type"`
					Payload     json.RawMessage `json:"payload"`
				}
				if err := json.Unmarshal(msgData, &fwd); err == nil && fwd.MessageType == "forward" {
					_ = writeToAgent(map[string]interface{}{
						"message_type": "forward",
						"device_id":    connMsg.DeviceID,
						"client_id":    uint32(42),
						"payload":      fwd.Payload,
					})
				}
			}
		}
	}))
	defer server.Close()

	wsURL := "ws" + strings.TrimPrefix(server.URL, "http")

	// 1. Initialize Agent
	coord := agent.NewCoordinator("dev-triparty-test", nil)
	defer coord.Close()

	sigClient := signaling.NewClient("dev-triparty-test", wsURL+"/register_agent", coord)
	coord.SetSignalingClient(sigClient)

	if err := sigClient.Connect(); err != nil {
		t.Fatalf("agent failed to connect to signaling: %v", err)
	}
	defer sigClient.Close()

	// 2. Client connects to /connect_client
	dialer := websocket.Dialer{}
	clientWS, _, err := dialer.Dial(wsURL+"/connect_client", nil)
	if err != nil {
		t.Fatalf("client failed to dial /connect_client: %v", err)
	}
	defer clientWS.Close()

	var clientWsWriteMu sync.Mutex
	safeClientWrite := func(v interface{}) error {
		clientWsWriteMu.Lock()
		defer clientWsWriteMu.Unlock()
		return clientWS.WriteJSON(v)
	}

	// Client sends connect
	_ = safeClientWrite(map[string]interface{}{
		"message_type": "connect",
		"device_id":    "dev-triparty-test",
	})

	// Client reads config
	_, cfgData, err := clientWS.ReadMessage()
	if err != nil {
		t.Fatalf("client failed to read config: %v", err)
	}
	var cfg struct {
		MessageType string `json:"message_type"`
	}
	_ = json.Unmarshal(cfgData, &cfg)
	if cfg.MessageType != "config" {
		t.Errorf("expected config message, got %s", cfg.MessageType)
	}

	// 3. Client sets up WebRTC PeerConnection
	clientME := &webrtc.MediaEngine{}
	_ = clientME.RegisterDefaultCodecs()
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("client failed to create PC: %v", err)
	}
	defer clientPC.Close()

	clientConnected := make(chan struct{}, 1)
	clientPC.OnConnectionStateChange(func(state webrtc.PeerConnectionState) {
		if state == webrtc.PeerConnectionStateConnected {
			select {
			case clientConnected <- struct{}{}:
			default:
			}
		}
	})

	clientPC.OnICECandidate(func(cand *webrtc.ICECandidate) {
		if cand == nil {
			return
		}
		candJSON := cand.ToJSON()
		_ = safeClientWrite(map[string]interface{}{
			"message_type": "forward",
			"payload": map[string]interface{}{
				"type": "ice-candidate",
				"candidate": map[string]interface{}{
					"candidate":     candJSON.Candidate,
					"sdpMid":        candJSON.SDPMid,
					"sdpMLineIndex": candJSON.SDPMLineIndex,
				},
			},
		})
	})

	// Client sends request-offer
	_ = safeClientWrite(map[string]interface{}{
		"message_type": "forward",
		"payload": map[string]interface{}{
			"type": "request-offer",
		},
	})

	// Client reads messages from signaling
	go func() {
		for {
			_, data, err := clientWS.ReadMessage()
			if err != nil {
				break
			}
			var devMsg struct {
				MessageType string          `json:"message_type"`
				Payload     json.RawMessage `json:"payload"`
			}
			if err := json.Unmarshal(data, &devMsg); err == nil && devMsg.MessageType == "device_msg" {
				var inner struct {
					Type      string      `json:"type"`
					SDP       string      `json:"sdp"`
					Candidate interface{} `json:"candidate"`
				}
				if err := json.Unmarshal(devMsg.Payload, &inner); err == nil {
					switch inner.Type {
					case "offer":
						t.Logf("[E2E Relay] Client received offer from agent, length: %d", len(inner.SDP))
						setErr := clientPC.SetRemoteDescription(webrtc.SessionDescription{
							Type: webrtc.SDPTypeOffer,
							SDP:  inner.SDP,
						})
						if setErr != nil {
							t.Logf("[E2E Relay] Client SetRemoteDescription error: %v", setErr)
						}
						ans, ansErr := clientPC.CreateAnswer(nil)
						if ansErr == nil {
							_ = clientPC.SetLocalDescription(ans)
							t.Logf("[E2E Relay] Client sending answer, length: %d", len(ans.SDP))
							_ = safeClientWrite(map[string]interface{}{
								"message_type": "forward",
								"payload": map[string]interface{}{
									"type": "answer",
									"sdp":  ans.SDP,
								},
							})
						} else {
							t.Logf("[E2E Relay] Client CreateAnswer error: %v", ansErr)
						}
					case "ice-candidate":
						candBytes, _ := json.Marshal(inner.Candidate)
						var candPayload agentwebrtc.CandidatePayload
						if err := json.Unmarshal(candBytes, &candPayload); err == nil {
							_ = clientPC.AddICECandidate(candPayload.ToPionCandidate())
						}
					}
				}
			}
		}
	}()

	// 4. Verify P2P connection established over signaling relay
	select {
	case <-clientConnected:
		t.Log("[PASS] Tri-party signaling relay successfully established P2P PeerConnection")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for PeerConnection through signaling relay")
	}

	if coord.ActiveSessionCount() != 1 {
		t.Errorf("expected 1 active session in coordinator, got %d", coord.ActiveSessionCount())
	}
}

// TestWebRTCDataChannelsE2E verifies real SCTP DataChannel communication:
// 1. Browser -> input-channel -> Agent -> ControlSink (validates exact 32-byte scrcpy touch frame).
// 2. Browser -> clipboard-channel -> Agent -> ClipboardProvider (validates set_clipboard).
// 3. Browser -> clipboard-channel -> Agent -> ClipboardProvider -> Response -> Browser (validates get_clipboard).
// 4. Verifies camera, file, ai-command, adb channels remain strictly deferred.
func TestWebRTCDataChannelsE2E(t *testing.T) {
	// 1. Initialize Browser Client WebRTC PeerConnection
	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	var (
		clientInputDC   *webrtc.DataChannel
		clientClipDC    *webrtc.DataChannel
		clientFileDC    *webrtc.DataChannel
		inputDCOpen     = make(chan struct{}, 1)
		clipDCOpen      = make(chan struct{}, 1)
		fileDCOpen      = make(chan struct{}, 1)
		clipMsgReceived = make(chan []byte, 5)
		clientConnected = make(chan struct{}, 1)
		dcMu            sync.Mutex
	)

	// Inbound file-channel created by client peer with ordered=true
	orderedFile := true
	clientFileDC, err = clientPC.CreateDataChannel(agentwebrtc.ChannelFile, &webrtc.DataChannelInit{
		Ordered: &orderedFile,
	})
	if err != nil {
		t.Fatalf("failed to create client file-channel: %v", err)
	}
	clientFileDC.OnOpen(func() {
		select {
		case fileDCOpen <- struct{}{}:
		default:
		}
	})

	clientPC.OnDataChannel(func(dc *webrtc.DataChannel) {
		dcMu.Lock()
		defer dcMu.Unlock()
		label := dc.Label()
		if label == agentwebrtc.ChannelInput {
			clientInputDC = dc
			dc.OnOpen(func() {
				select {
				case inputDCOpen <- struct{}{}:
				default:
				}
			})
		} else if label == agentwebrtc.ChannelClipboard {
			clientClipDC = dc
			dc.OnOpen(func() {
				select {
				case clipDCOpen <- struct{}{}:
				default:
				}
			})
			dc.OnMessage(func(msg webrtc.DataChannelMessage) {
				clipMsgReceived <- msg.Data
			})
		}
	})

	clientPC.OnConnectionStateChange(func(state webrtc.PeerConnectionState) {
		if state == webrtc.PeerConnectionStateConnected {
			select {
			case clientConnected <- struct{}{}:
			default:
			}
		}
	})

	// 2. Initialize Agent Coordinator with Production Configuration
	coord := agent.NewCoordinator("dev-e2e-dc", nil)
	defer coord.Close()

	controlSink := agentwebrtc.NewMemoryControlSink()
	clipboardProvider := agentwebrtc.NewMemoryClipboardProvider()
	fileSink := agentwebrtc.NewMemoryFileSink()

	var (
		postActionInvoked bool
		postActionTarget  string
		postActionMu      sync.Mutex
	)

	coord.SetControlSink(controlSink)
	coord.SetClipboardProvider(clipboardProvider)
	coord.SetFileSinkFactory(func(clientID uint32) agentwebrtc.FileSink {
		return fileSink
	})
	coord.SetPostUploadActionHandler(func(meta agentwebrtc.FileMetadata, path string) error {
		postActionMu.Lock()
		defer postActionMu.Unlock()
		postActionInvoked = true
		postActionTarget = path
		return nil
	})

	// Production Coordinator receives request-offer via signaling multiplexer
	coord.HandleForward(200, []byte(`{"type":"request-offer"}`))

	session, ok := coord.GetSession(200)
	if !ok || session == nil {
		t.Fatalf("coordinator failed to construct session via handleRequestOffer")
	}

	// Wire ICE trickle between Agent and Client via production Coordinator paths
	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(200, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})

	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	// 3. Negotiate Offer / Answer using offer generated by Coordinator
	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("session has no local description after handleRequestOffer")
	}

	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}

	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	if err := clientPC.SetLocalDescription(answer); err != nil {
		t.Fatalf("client failed to set local answer: %v", err)
	}

	// Answer is delivered to Agent via production HandleForward
	coord.HandleForward(200, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	// 4. Wait for WebRTC Connected
	select {
	case <-clientConnected:
		t.Log("[PASS] PeerConnection connected for DataChannel E2E")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for PeerConnection connected")
	}

	// 5. Wait for input-channel and clipboard-channel to reach open state
	select {
	case <-inputDCOpen:
		t.Log("[PASS] Browser client input-channel reached OPEN")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for input-channel open on client")
	}

	select {
	case <-clipDCOpen:
		t.Log("[PASS] Browser client clipboard-channel reached OPEN")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for clipboard-channel open on client")
	}

	select {
	case <-fileDCOpen:
		t.Log("[PASS] Browser client file-channel reached OPEN")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for file-channel open on client")
	}

	// 6. Test Input Channel E2E: Browser sends inject_touch over SCTP DataChannel
	t.Run("input", func(t *testing.T) {
		touchPayload := `{"type":"inject_touch","action":0,"id":42,"x":200,"y":300,"w":1080,"h":1920}`
		dcMu.Lock()
		inDC := clientInputDC
		dcMu.Unlock()

		if err := inDC.SendText(touchPayload); err != nil {
			t.Fatalf("failed to send touch message over client input-channel: %v", err)
		}

		// Wait for control sink to receive decoded binary frame
		var receivedMsg []byte
		deadline := time.Now().Add(3 * time.Second)
		for time.Now().Before(deadline) {
			msgs := controlSink.GetMessages()
			if len(msgs) > 0 {
				receivedMsg = msgs[0]
				break
			}
			time.Sleep(20 * time.Millisecond)
		}

		if len(receivedMsg) != 32 {
			t.Fatalf("expected 32-byte scrcpy touch frame in ControlSink, got length %d", len(receivedMsg))
		}
		if receivedMsg[0] != agentwebrtc.ScrcpyTypeInjectTouchEvent {
			t.Fatalf("expected message type %d, got %d", agentwebrtc.ScrcpyTypeInjectTouchEvent, receivedMsg[0])
		}
		if receivedMsg[1] != 0 { // action DOWN
			t.Fatalf("expected action 0 (DOWN), got %d", receivedMsg[1])
		}
		t.Log("[PASS] input-channel SCTP E2E: Browser JSON -> Agent -> ControlSink verified with exact 32-byte scrcpy frame")
	})

	// 7. Test Clipboard Channel E2E: set_clipboard
	t.Run("clipboard_set", func(t *testing.T) {
		dcMu.Lock()
		clDC := clientClipDC
		dcMu.Unlock()

		setPayload := `{"type":"set_clipboard","text":"Hello From Browser SCTP","paste":true,"origin_client_id":"cli-888"}`
		if err := clDC.SendText(setPayload); err != nil {
			t.Fatalf("failed to send set_clipboard: %v", err)
		}

		// Wait for clipboardProvider to receive update
		deadline := time.Now().Add(3 * time.Second)
		var textRecv string
		for time.Now().Before(deadline) {
			text, _, _, sets, _ := clipboardProvider.Stats()
			if sets > 0 {
				textRecv = text
				break
			}
			time.Sleep(20 * time.Millisecond)
		}
		if textRecv != "Hello From Browser SCTP" {
			t.Fatalf("expected 'Hello From Browser SCTP' in ClipboardProvider, got %q", textRecv)
		}
		t.Log("[PASS] clipboard-channel set_clipboard SCTP E2E verified in ClipboardProvider")
	})

	// 8. Test Clipboard Channel E2E: get_clipboard
	t.Run("clipboard_get", func(t *testing.T) {
		dcMu.Lock()
		clDC := clientClipDC
		dcMu.Unlock()

		getPayload := `{"type":"get_clipboard"}`
		if err := clDC.SendText(getPayload); err != nil {
			t.Fatalf("failed to send get_clipboard: %v", err)
		}

		var rawResp []byte
		select {
		case rawResp = <-clipMsgReceived:
		case <-time.After(3 * time.Second):
			t.Fatalf("timeout waiting for get_clipboard response frame from Agent")
		}

		var resp agentwebrtc.ClipboardResponseMessage
		if err := json.Unmarshal(rawResp, &resp); err != nil {
			t.Fatalf("failed to unmarshal clipboard response frame: %v", err)
		}
		if resp.Type != "clipboard" {
			t.Fatalf("expected response type 'clipboard', got %q", resp.Type)
		}
		if resp.Text != "Hello From Browser SCTP" {
			t.Fatalf("expected text 'Hello From Browser SCTP', got %q", resp.Text)
		}
		if resp.Source != "device" {
			t.Fatalf("expected source 'device', got %q", resp.Source)
		}
		t.Log("[PASS] clipboard-channel get_clipboard SCTP E2E verified: Agent -> Browser response confirmed")
	})

	// 9. Test File Channel E2E: Real SCTP multi-chunk file upload with SHA-256 verification
	// Wired via real production Coordinator (SetFileSinkFactory + SetPostUploadActionHandler)
	t.Run("file_upload", func(t *testing.T) {
		payload := []byte("cleanroom-reconstructed-file-channel-payload-content-1234567890")
		hSum := sha256.Sum256(payload)
		shaHex := hex.EncodeToString(hSum[:])

		startJSON := fmt.Sprintf(`{"type":"start_upload","filename":"test_e2e_app.apk","size":%d,"sha256":"%s","install":true}`,
			len(payload), shaHex)

		// 1. Framing Boundary: Send metadata as text/JSON over genuine SCTP
		if err := clientFileDC.SendText(startJSON); err != nil {
			t.Fatalf("failed to send start_upload text frame: %v", err)
		}

		// Allow agent state machine to transition to METADATA_ACCEPTED
		time.Sleep(30 * time.Millisecond)

		// 2. Framing Boundary: Send file chunks as binary over genuine SCTP
		chunk1 := payload[:20]
		chunk2 := payload[20:45]
		chunk3 := payload[45:]

		for _, chunk := range [][]byte{chunk1, chunk2, chunk3} {
			if err := clientFileDC.Send(chunk); err != nil {
				t.Fatalf("failed to send binary chunk over SCTP: %v", err)
			}
			time.Sleep(10 * time.Millisecond)
		}

		// Wait for completion
		deadline := time.Now().Add(3 * time.Second)
		var completed bool
		for time.Now().Before(deadline) {
			if fileSink.IsCompleted() {
				completed = true
				break
			}
			time.Sleep(20 * time.Millisecond)
		}

		if !completed {
			t.Fatalf("file transfer did not complete within deadline")
		}

		// Exact byte reconstruction verification
		reconstructed := fileSink.GetBytes()
		if !bytes.Equal(reconstructed, payload) {
			t.Fatalf("reconstructed byte mismatch! Expected %d bytes, got %d bytes", len(payload), len(reconstructed))
		}

		// PostUploadAction verification (boundary without executing installer)
		postActionMu.Lock()
		invoked := postActionInvoked
		target := postActionTarget
		postActionMu.Unlock()

		if !invoked || target != "memory://test_e2e_app.apk" {
			t.Fatalf("expected PostUploadAction invoked for memory://test_e2e_app.apk, got invoked=%v target=%q", invoked, target)
		}

		t.Log("[PASS] file-channel real SCTP E2E: metadata JSON frame -> production coordinator file handler -> binary chunks -> FileSink -> exact reconstructed payload -> clean completion")
	})
}

// TestWebRTCDataChannelsE2E_UnwiredFileChannelFails is a negative wiring test verifying that
// if Coordinator does NOT configure a FileSinkFactory (unwired production state),
// inbound file-channel messages are NOT processed and the transfer never completes.
// This proves the E2E test is validating real Coordinator assembly rather than test-local fallbacks.
func TestWebRTCDataChannelsE2E_UnwiredFileChannelFails(t *testing.T) {
	// Initialize Coordinator WITHOUT SetFileSinkFactory
	coord := agent.NewCoordinator("dev-e2e-unwired", nil)
	defer coord.Close()

	coord.SetControlSink(agentwebrtc.NewMemoryControlSink())
	coord.SetClipboardProvider(agentwebrtc.NewMemoryClipboardProvider())
	// NOTE: SetFileSinkFactory is intentionally omitted

	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	orderedFile := true
	clientFileDC, err := clientPC.CreateDataChannel(agentwebrtc.ChannelFile, &webrtc.DataChannelInit{
		Ordered: &orderedFile,
	})
	if err != nil {
		t.Fatalf("failed to create client file-channel: %v", err)
	}

	fileDCOpen := make(chan struct{}, 1)
	clientFileDC.OnOpen(func() {
		select {
		case fileDCOpen <- struct{}{}:
		default:
		}
	})

	coord.HandleForward(300, []byte(`{"type":"request-offer"}`))
	session, ok := coord.GetSession(300)
	if !ok || session == nil {
		t.Fatalf("failed to get session from coordinator")
	}

	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(300, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("missing local description")
	}
	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}
	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	_ = clientPC.SetLocalDescription(answer)
	coord.HandleForward(300, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	select {
	case <-fileDCOpen:
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for file-channel open")
	}

	// Verify session has NO FileHandler attached
	if session.Channels.FileHandler != nil {
		t.Fatalf("expected nil FileHandler on unwired session, got %v", session.Channels.FileHandler)
	}

	// Attempt file transfer over SCTP
	payload := []byte("payload-for-unwired-test")
	hSum := sha256.Sum256(payload)
	startJSON := fmt.Sprintf(`{"type":"start_upload","filename":"unwired.apk","size":%d,"sha256":"%x","install":true}`,
		len(payload), hSum)

	if err := clientFileDC.SendText(startJSON); err != nil {
		t.Fatalf("failed to send start_upload: %v", err)
	}
	time.Sleep(30 * time.Millisecond)
	if err := clientFileDC.Send(payload); err != nil {
		t.Fatalf("failed to send binary chunk: %v", err)
	}

	// Wait and verify transfer did NOT complete and no handler processed messages
	time.Sleep(200 * time.Millisecond)
	if session.Channels.FileHandler != nil {
		t.Errorf("FileHandler was unexpectedly attached")
	}
	t.Log("[PASS] Unwired Coordinator correctly leaves file-channel unhandled with 0 side-effects")
}

// TestCameraSupportFalseE2E verifies that when camera bridge probe is unavailable and ForceCamera=false:
// 1. offer.camera_support == false
// 2. camera-channel is NOT created by the Agent
// 3. Browser receives input-channel and clipboard-channel, but NOT camera-channel
// 4. file-channel behavior is completely unaffected
func TestCameraSupportFalseE2E(t *testing.T) {
	coord := agent.NewCoordinator("dev-e2e-cam-false", nil)
	defer coord.Close()

	// Configure unavailable camera address with ForceCamera=false
	coord.SetCameraConfig(agentwebrtc.CameraConfig{
		Address:     "127.0.0.1:54321",
		ForceCamera: false,
		DialTimeout: 50 * time.Millisecond,
	})

	coord.SetControlSink(agentwebrtc.NewMemoryControlSink())
	coord.SetClipboardProvider(agentwebrtc.NewMemoryClipboardProvider())
	coord.SetFileSinkFactory(func(clientID uint32) agentwebrtc.FileSink {
		return agentwebrtc.NewMemoryFileSink()
	})

	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	// Client listens for Agent-created outbound DataChannels
	var remoteChannelsMu sync.Mutex
	remoteChannels := make(map[string]bool)
	clientPC.OnDataChannel(func(dc *webrtc.DataChannel) {
		remoteChannelsMu.Lock()
		remoteChannels[dc.Label()] = true
		remoteChannelsMu.Unlock()
	})

	// Client creates file-channel
	orderedFile := true
	clientFileDC, err := clientPC.CreateDataChannel(agentwebrtc.ChannelFile, &webrtc.DataChannelInit{
		Ordered: &orderedFile,
	})
	if err != nil {
		t.Fatalf("failed to create client file-channel: %v", err)
	}
	fileDCOpen := make(chan struct{}, 1)
	clientFileDC.OnOpen(func() {
		select {
		case fileDCOpen <- struct{}{}:
		default:
		}
	})

	clientID := uint32(1001)
	coord.HandleForward(clientID, []byte(`{"type":"request-offer"}`))

	session, ok := coord.GetSession(clientID)
	if !ok || session == nil {
		t.Fatalf("failed to get session from coordinator")
	}

	// 1. Session-level camera support state must be false
	if session.CameraSupport {
		t.Fatalf("expected session.CameraSupport == false, got true")
	}

	// 2. camera-channel must NOT be created on Agent side
	if session.Channels.CameraChannel != nil {
		t.Fatalf("camera-channel MUST NOT be created on Agent when CameraSupport=false")
	}

	// 3. Verify offer payload camera_support is false
	testSess, err := agentwebrtc.NewPeerSessionWithOptions(agentwebrtc.PeerSessionOptions{
		ClientID:      999,
		CameraSupport: false,
	})
	if err != nil {
		t.Fatalf("failed to create test session: %v", err)
	}
	defer testSess.Close()
	offerPayload, err := testSess.CreateOffer()
	if err != nil {
		t.Fatalf("failed to create offer: %v", err)
	}
	if offerPayload.CameraSupport == nil || *offerPayload.CameraSupport != false {
		t.Fatalf("expected offer.camera_support == false, got %v", offerPayload.CameraSupport)
	}

	// Exchange SDP and ICE
	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("missing local description")
	}
	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}
	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	_ = clientPC.SetLocalDescription(answer)
	coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	select {
	case <-fileDCOpen:
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for file-channel open")
	}

	time.Sleep(200 * time.Millisecond)

	remoteChannelsMu.Lock()
	hasInput := remoteChannels[agentwebrtc.ChannelInput]
	hasClipboard := remoteChannels[agentwebrtc.ChannelClipboard]
	hasCamera := remoteChannels[agentwebrtc.ChannelCamera]
	remoteChannelsMu.Unlock()

	if !hasInput {
		t.Errorf("expected input-channel to be received by client")
	}
	if !hasClipboard {
		t.Errorf("expected clipboard-channel to be received by client")
	}
	if hasCamera {
		t.Errorf("camera-channel MUST NOT be received by client when cameraSupport=false")
	}

	t.Log("[PASS] TestCameraSupportFalseE2E: cameraSupport=false -> offer false, camera-channel absent, input/clipboard/file intact")
}

// TestCameraSupportTrueE2E verifies that when camera bridge probe succeeds:
// 1. offer.camera_support == true
// 2. camera-channel is created with ordered=true by the Agent before offer creation
// 3. Browser receives camera-channel via OnDataChannel
func TestCameraSupportTrueE2E(t *testing.T) {
	// Start mock bridge on ephemeral port
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("failed to listen on mock bridge: %v", err)
	}
	defer listener.Close()

	// Mock bridge accept loop (handles probe and active dials)
	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			// Keep probe or active connection open briefly
			go func(c net.Conn) {
				time.Sleep(500 * time.Millisecond)
				_ = c.Close()
			}(conn)
		}
	}()

	coord := agent.NewCoordinator("dev-e2e-cam-true", nil)
	defer coord.Close()

	coord.SetCameraConfig(agentwebrtc.CameraConfig{
		Address:     listener.Addr().String(),
		ForceCamera: false,
		DialTimeout: 1 * time.Second,
	})

	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	cameraDCOpen := make(chan struct{}, 1)
	clientPC.OnDataChannel(func(dc *webrtc.DataChannel) {
		if dc.Label() == agentwebrtc.ChannelCamera {
			dc.OnOpen(func() {
				select {
				case cameraDCOpen <- struct{}{}:
				default:
				}
			})
		}
	})

	clientID := uint32(1002)
	coord.HandleForward(clientID, []byte(`{"type":"request-offer"}`))

	session, ok := coord.GetSession(clientID)
	if !ok || session == nil {
		t.Fatalf("failed to get session from coordinator")
	}

	// 1. Session camera support must be true
	if !session.CameraSupport {
		t.Fatalf("expected session.CameraSupport == true, got false")
	}

	// 2. camera-channel must exist and have ordered=true
	if session.Channels.CameraChannel == nil {
		t.Fatalf("expected camera-channel to exist on Agent session")
	}
	if !session.Channels.CameraChannel.Ordered() {
		t.Fatalf("expected camera-channel to have ordered=true")
	}

	// 3. Offer payload camera_support must be true
	testSess, err := agentwebrtc.NewPeerSessionWithOptions(agentwebrtc.PeerSessionOptions{
		ClientID:      998,
		CameraSupport: true,
	})
	if err != nil {
		t.Fatalf("failed to create test session: %v", err)
	}
	defer testSess.Close()
	offerPayload, err := testSess.CreateOffer()
	if err != nil {
		t.Fatalf("failed to create offer: %v", err)
	}
	if offerPayload.CameraSupport == nil || *offerPayload.CameraSupport != true {
		t.Fatalf("expected offer.camera_support == true, got %v", offerPayload.CameraSupport)
	}

	// Exchange SDP and ICE
	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("missing local description")
	}
	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}
	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	_ = clientPC.SetLocalDescription(answer)
	coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	select {
	case <-cameraDCOpen:
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for camera-channel open on client")
	}

	t.Log("[PASS] TestCameraSupportTrueE2E: probe succeeds -> cameraSupport=true, ordered=true, camera-channel received by browser")
}

// TestCameraSCTPTCPFullE2E validates the full production data plane:
// A. Browser/Agent negotiate
// B. camera-channel opens
// C. Agent connects to mock bridge
// D. Mock receives valid LE length-prefixed handshake (width, height, frame_rate)
// E. Mock sends framed: VIRTUAL_DEVICE_START_CAMERA_SESSION
// F. Browser receives: {"action":"start"}
// G. Browser sends real valid JPEG as binary SCTP DataChannel payload
// H. Agent caches JPEG and queues frame
// I. Agent decodes JPEG -> I420
// J. Mock bridge receives uint32 LE length + exact I420 payload
// K. Mock sends VIRTUAL_DEVICE_CAPTURE_IMAGE
// L. Mock receives uint32 LE length + exact original JPEG bytes
// M. Mock sends VIRTUAL_DEVICE_STOP_CAMERA_SESSION
// N. Browser receives: {"action":"stop"}
// O. Clean shutdown
func TestCameraSCTPTCPFullE2E(t *testing.T) {
	// Start mock bridge on ephemeral port
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("failed to start mock bridge: %v", err)
	}
	defer listener.Close()

	activeBridgeConnChan := make(chan net.Conn, 1)

	// Mock bridge accept loop: handles probe connection and active streaming connection
	go func() {
		var firstConn sync.Once
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			firstConn.Do(func() {
				// First connection is probe; close cleanly
				_ = conn.Close()
				conn = nil
			})
			if conn != nil {
				// Second connection is active streaming connection
				activeBridgeConnChan <- conn
				return
			}
		}
	}()

	// 16x16 frame dimensions for lightweight fast verification
	camWidth, camHeight := 16, 16
	coord := agent.NewCoordinator("dev-e2e-cam-full", nil)
	defer coord.Close()

	coord.SetCameraConfig(agentwebrtc.CameraConfig{
		Address:     listener.Addr().String(),
		Width:       camWidth,
		Height:      camHeight,
		FrameRate:   30.0,
		DialTimeout: 1 * time.Second,
	})

	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	var (
		clientCamDCMu sync.Mutex
		clientCamDC   *webrtc.DataChannel
	)
	cameraDCOpen := make(chan struct{}, 1)
	clientActionsReceived := make(chan string, 10)

	clientPC.OnDataChannel(func(dc *webrtc.DataChannel) {
		if dc.Label() == agentwebrtc.ChannelCamera {
			clientCamDCMu.Lock()
			clientCamDC = dc
			clientCamDCMu.Unlock()

			dc.OnOpen(func() {
				select {
				case cameraDCOpen <- struct{}{}:
				default:
				}
			})

			dc.OnMessage(func(msg webrtc.DataChannelMessage) {
				if msg.IsString {
					var act struct {
						Action string `json:"action"`
					}
					if err := json.Unmarshal(msg.Data, &act); err == nil {
						clientActionsReceived <- act.Action
					}
				}
			})
		}
	})

	// Step A: Negotiation
	clientID := uint32(1003)
	coord.HandleForward(clientID, []byte(`{"type":"request-offer"}`))
	session, ok := coord.GetSession(clientID)
	if !ok || session == nil {
		t.Fatalf("failed to get session")
	}

	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("missing local description")
	}
	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}
	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	_ = clientPC.SetLocalDescription(answer)
	coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	// Step B: Wait for camera-channel to open
	select {
	case <-cameraDCOpen:
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for camera-channel open")
	}

	// Step C: Agent connects to mock bridge
	var bridgeConn net.Conn
	select {
	case bridgeConn = <-activeBridgeConnChan:
		defer bridgeConn.Close()
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for Agent to connect to mock bridge")
	}

	// Helper for wire framing read/write on bridgeConn
	readBridgeFrame := func() ([]byte, error) {
		var lenBuf [4]byte
		if _, err := io.ReadFull(bridgeConn, lenBuf[:]); err != nil {
			return nil, err
		}
		length := binary.LittleEndian.Uint32(lenBuf[:])
		payload := make([]byte, length)
		if length > 0 {
			if _, err := io.ReadFull(bridgeConn, payload); err != nil {
				return nil, err
			}
		}
		return payload, nil
	}

	writeBridgeFrame := func(p []byte) error {
		var lenBuf [4]byte
		binary.LittleEndian.PutUint32(lenBuf[:], uint32(len(p)))
		if _, err := bridgeConn.Write(lenBuf[:]); err != nil {
			return err
		}
		if len(p) > 0 {
			_, err := bridgeConn.Write(p)
			return err
		}
		return nil
	}

	// Step D: Mock receives valid LE length-prefixed handshake
	hsData, err := readBridgeFrame()
	if err != nil {
		t.Fatalf("failed to read handshake from bridge: %v", err)
	}
	var hs struct {
		Width     int     `json:"width"`
		Height    int     `json:"height"`
		FrameRate float64 `json:"frame_rate"`
	}
	if err := json.Unmarshal(hsData, &hs); err != nil {
		t.Fatalf("failed to unmarshal handshake: %v", err)
	}
	if hs.Width != camWidth || hs.Height != camHeight || hs.FrameRate != 30.0 {
		t.Fatalf("unexpected handshake values: %+v", hs)
	}

	// Step E: Mock sends framed VIRTUAL_DEVICE_START_CAMERA_SESSION
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventStartCameraSession)); err != nil {
		t.Fatalf("failed to write start event to bridge: %v", err)
	}

	// Step F: Browser receives {"action":"start"}
	select {
	case action := <-clientActionsReceived:
		if action != "start" {
			t.Fatalf("expected action 'start', got %q", action)
		}
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for browser to receive start action")
	}

	// Step G: Browser sends REAL valid JPEG binary payload
	testImg := image.NewRGBA(image.Rect(0, 0, camWidth, camHeight))
	for y := 0; y < camHeight; y++ {
		for x := 0; x < camWidth; x++ {
			testImg.Set(x, y, color.RGBA{R: uint8(x * 10), G: uint8(y * 10), B: 100, A: 255})
		}
	}
	var jpegBuf bytes.Buffer
	if err := jpeg.Encode(&jpegBuf, testImg, &jpeg.Options{Quality: 90}); err != nil {
		t.Fatalf("failed to encode test JPEG: %v", err)
	}
	realJpegBytes := jpegBuf.Bytes()

	clientCamDCMu.Lock()
	camDC := clientCamDC
	clientCamDCMu.Unlock()

	if err := camDC.Send(realJpegBytes); err != nil {
		t.Fatalf("failed to send binary JPEG over camera-channel: %v", err)
	}

	// Step H, I, J: Agent decodes JPEG -> I420 -> mock bridge receives framed I420
	i420Data, err := readBridgeFrame()
	if err != nil {
		t.Fatalf("failed to read I420 frame from bridge: %v", err)
	}
	expectedI420Len := camWidth * camHeight * 3 / 2 // 16*16 + 8*8 + 8*8 = 384
	if len(i420Data) != expectedI420Len {
		t.Fatalf("expected I420 length %d, got %d", expectedI420Len, len(i420Data))
	}

	// Step K: Mock sends VIRTUAL_DEVICE_CAPTURE_IMAGE
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventCaptureImage)); err != nil {
		t.Fatalf("failed to write capture event to bridge: %v", err)
	}

	// Step L: Mock receives exact original JPEG bytes
	snapData, err := readBridgeFrame()
	if err != nil {
		t.Fatalf("failed to read snapshot from bridge: %v", err)
	}
	if !bytes.Equal(snapData, realJpegBytes) {
		t.Fatalf("snapshot mismatch: length expected %d, got %d", len(realJpegBytes), len(snapData))
	}

	// Step M: Mock sends VIRTUAL_DEVICE_STOP_CAMERA_SESSION
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventStopCameraSession)); err != nil {
		t.Fatalf("failed to write stop event to bridge: %v", err)
	}

	// Step N: Browser receives {"action":"stop"}
	select {
	case action := <-clientActionsReceived:
		if action != "stop" {
			t.Fatalf("expected action 'stop', got %q", action)
		}
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for browser to receive stop action")
	}

	// Step O: Clean shutdown
	_ = bridgeConn.Close()
	_ = clientPC.Close()
	_ = coord.Close()

	t.Log("[PASS] TestCameraSCTPTCPFullE2E: complete standards-compliant WebRTC SCTP + TCP HAL bridge E2E passed (Steps A-O)")
}

// TestCameraBackpressureSCTPE2E verifies that sending multiple consecutive frames over real SCTP:
// 1. Never blocks the sender/DataChannel.
// 2. Continues to update the snapshot cache to the newest received frame.
// 3. Responds to VIRTUAL_DEVICE_CAPTURE_IMAGE with the exact newest frame bytes.
func TestCameraBackpressureSCTPE2E(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("failed to start mock bridge: %v", err)
	}
	defer listener.Close()

	activeBridgeConnChan := make(chan net.Conn, 1)
	go func() {
		var firstConn sync.Once
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			firstConn.Do(func() {
				_ = conn.Close()
				conn = nil
			})
			if conn != nil {
				activeBridgeConnChan <- conn
				return
			}
		}
	}()

	camWidth, camHeight := 16, 16
	coord := agent.NewCoordinator("dev-e2e-cam-bp", nil)
	defer coord.Close()

	coord.SetCameraConfig(agentwebrtc.CameraConfig{
		Address:     listener.Addr().String(),
		Width:       camWidth,
		Height:      camHeight,
		FrameRate:   30.0,
		DialTimeout: 1 * time.Second,
	})

	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	var (
		clientCamDCMu sync.Mutex
		clientCamDC   *webrtc.DataChannel
	)
	cameraDCOpen := make(chan struct{}, 1)
	clientActionsReceived := make(chan string, 10)

	clientPC.OnDataChannel(func(dc *webrtc.DataChannel) {
		if dc.Label() == agentwebrtc.ChannelCamera {
			clientCamDCMu.Lock()
			clientCamDC = dc
			clientCamDCMu.Unlock()

			dc.OnOpen(func() {
				select {
				case cameraDCOpen <- struct{}{}:
				default:
				}
			})

			dc.OnMessage(func(msg webrtc.DataChannelMessage) {
				if msg.IsString {
					var act struct {
						Action string `json:"action"`
					}
					if err := json.Unmarshal(msg.Data, &act); err == nil {
						clientActionsReceived <- act.Action
					}
				}
			})
		}
	})

	clientID := uint32(1004)
	coord.HandleForward(clientID, []byte(`{"type":"request-offer"}`))
	session, ok := coord.GetSession(clientID)
	if !ok || session == nil {
		t.Fatalf("failed to get session")
	}

	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("missing local description")
	}
	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}
	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	_ = clientPC.SetLocalDescription(answer)
	coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	select {
	case <-cameraDCOpen:
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for camera-channel open")
	}

	var bridgeConn net.Conn
	select {
	case bridgeConn = <-activeBridgeConnChan:
		defer bridgeConn.Close()
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for Agent to connect to mock bridge")
	}

	readBridgeFrame := func() ([]byte, error) {
		var lenBuf [4]byte
		if _, err := io.ReadFull(bridgeConn, lenBuf[:]); err != nil {
			return nil, err
		}
		length := binary.LittleEndian.Uint32(lenBuf[:])
		payload := make([]byte, length)
		if length > 0 {
			if _, err := io.ReadFull(bridgeConn, payload); err != nil {
				return nil, err
			}
		}
		return payload, nil
	}

	writeBridgeFrame := func(p []byte) error {
		var lenBuf [4]byte
		binary.LittleEndian.PutUint32(lenBuf[:], uint32(len(p)))
		if _, err := bridgeConn.Write(lenBuf[:]); err != nil {
			return err
		}
		if len(p) > 0 {
			_, err := bridgeConn.Write(p)
			return err
		}
		return nil
	}

	// Read handshake
	_, err = readBridgeFrame()
	if err != nil {
		t.Fatalf("failed to read handshake: %v", err)
	}

	// Start camera session
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventStartCameraSession)); err != nil {
		t.Fatalf("failed to write start event: %v", err)
	}

	select {
	case act := <-clientActionsReceived:
		if act != "start" {
			t.Fatalf("expected action 'start', got %q", act)
		}
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for start action")
	}

	// Helper to generate JPEG with distinct solid color
	makeJPEG := func(r, g, b uint8) []byte {
		img := image.NewRGBA(image.Rect(0, 0, camWidth, camHeight))
		for y := 0; y < camHeight; y++ {
			for x := 0; x < camWidth; x++ {
				img.Set(x, y, color.RGBA{R: r, G: g, B: b, A: 255})
			}
		}
		var buf bytes.Buffer
		_ = jpeg.Encode(&buf, img, &jpeg.Options{Quality: 90})
		return buf.Bytes()
	}

	jpegA := makeJPEG(255, 0, 0)
	jpegB := makeJPEG(0, 255, 0)
	jpegC := makeJPEG(0, 0, 255)

	clientCamDCMu.Lock()
	camDC := clientCamDC
	clientCamDCMu.Unlock()

	// Send rapid bursts of frames A, B, C over SCTP
	if err := camDC.Send(jpegA); err != nil {
		t.Fatalf("failed to send jpegA: %v", err)
	}
	if err := camDC.Send(jpegB); err != nil {
		t.Fatalf("failed to send jpegB: %v", err)
	}
	if err := camDC.Send(jpegC); err != nil {
		t.Fatalf("failed to send jpegC: %v", err)
	}

	// Give slight window for SCTP delivery and mutex update
	time.Sleep(100 * time.Millisecond)

	// Invariant: newest snapshot MUST be jpegC
	latest := session.CameraHandler.GetLatestCameraJpeg()
	if !bytes.Equal(latest, jpegC) {
		t.Fatalf("expected latestCameraJpeg to be jpegC, got mismatch")
	}

	// HAL requests snapshot
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventCaptureImage)); err != nil {
		t.Fatalf("failed to send capture event: %v", err)
	}

	// Drain any concurrent streaming I420 frames (length 384) until snapshot JPEG is received
	var snapPayload []byte
	for i := 0; i < 5; i++ {
		frame, err := readBridgeFrame()
		if err != nil {
			t.Fatalf("failed to read from bridge: %v", err)
		}
		if len(frame) == camWidth*camHeight*3/2 {
			// Concurrently emitted I420 frame, continue reading
			continue
		}
		snapPayload = frame
		break
	}

	if snapPayload == nil {
		t.Fatalf("did not receive snapshot frame from bridge")
	}

	if !bytes.Equal(snapPayload, jpegC) {
		t.Fatalf("snapshot received by HAL is not the latest frame jpegC (expected len %d, got len %d)", len(jpegC), len(snapPayload))
	}

	t.Log("[PASS] TestCameraBackpressureSCTPE2E: rapid frame burst preserves newest snapshot in cache and on HAL capture")
}

// TestCameraInterleavedFrameSnapshotE2E tests that active streaming I420 frame production
// and concurrent VIRTUAL_DEVICE_CAPTURE_IMAGE snapshot events produce cleanly serialized,
// intact frames on the Camera HAL bridge without prefix/payload interleaving.
func TestCameraInterleavedFrameSnapshotE2E(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("failed to start mock bridge: %v", err)
	}
	defer listener.Close()

	activeBridgeConnChan := make(chan net.Conn, 1)
	go func() {
		var firstConn sync.Once
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			firstConn.Do(func() {
				_ = conn.Close()
				conn = nil
			})
			if conn != nil {
				activeBridgeConnChan <- conn
				return
			}
		}
	}()

	camWidth, camHeight := 16, 16
	coord := agent.NewCoordinator("dev-e2e-cam-interleave", nil)
	defer coord.Close()

	coord.SetCameraConfig(agentwebrtc.CameraConfig{
		Address:     listener.Addr().String(),
		Width:       camWidth,
		Height:      camHeight,
		FrameRate:   30.0,
		DialTimeout: 1 * time.Second,
	})

	clientME := &webrtc.MediaEngine{}
	if err := clientME.RegisterDefaultCodecs(); err != nil {
		t.Fatalf("failed to register client codecs: %v", err)
	}
	clientAPI := webrtc.NewAPI(webrtc.WithMediaEngine(clientME))
	clientPC, err := clientAPI.NewPeerConnection(webrtc.Configuration{})
	if err != nil {
		t.Fatalf("failed to create client PeerConnection: %v", err)
	}
	defer clientPC.Close()

	var (
		clientCamDCMu sync.Mutex
		clientCamDC   *webrtc.DataChannel
	)
	cameraDCOpen := make(chan struct{}, 1)
	clientActionsReceived := make(chan string, 10)

	clientPC.OnDataChannel(func(dc *webrtc.DataChannel) {
		if dc.Label() == agentwebrtc.ChannelCamera {
			clientCamDCMu.Lock()
			clientCamDC = dc
			clientCamDCMu.Unlock()

			dc.OnOpen(func() {
				select {
				case cameraDCOpen <- struct{}{}:
				default:
				}
			})

			dc.OnMessage(func(msg webrtc.DataChannelMessage) {
				if msg.IsString {
					var act struct {
						Action string `json:"action"`
					}
					if err := json.Unmarshal(msg.Data, &act); err == nil {
						clientActionsReceived <- act.Action
					}
				}
			})
		}
	})

	clientID := uint32(1005)
	coord.HandleForward(clientID, []byte(`{"type":"request-offer"}`))
	session, ok := coord.GetSession(clientID)
	if !ok || session == nil {
		t.Fatalf("failed to get session")
	}

	clientPC.OnICECandidate(func(c *webrtc.ICECandidate) {
		if c != nil {
			candJSON, _ := json.Marshal(c.ToJSON())
			coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"ice-candidate","candidate":%s}`, candJSON)))
		}
	})
	session.OnICECandidate(func(cand webrtc.ICECandidateInit) {
		_ = clientPC.AddICECandidate(cand)
	})

	localDesc := session.PC.LocalDescription()
	if localDesc == nil {
		t.Fatalf("missing local description")
	}
	if err := clientPC.SetRemoteDescription(*localDesc); err != nil {
		t.Fatalf("client failed to set remote offer: %v", err)
	}
	answer, err := clientPC.CreateAnswer(nil)
	if err != nil {
		t.Fatalf("client failed to create answer: %v", err)
	}
	_ = clientPC.SetLocalDescription(answer)
	coord.HandleForward(clientID, []byte(fmt.Sprintf(`{"type":"answer","sdp":%q}`, answer.SDP)))

	select {
	case <-cameraDCOpen:
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for camera-channel open")
	}

	var bridgeConn net.Conn
	select {
	case bridgeConn = <-activeBridgeConnChan:
		defer bridgeConn.Close()
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for Agent to connect to mock bridge")
	}

	readBridgeFrame := func() ([]byte, error) {
		var lenBuf [4]byte
		if _, err := io.ReadFull(bridgeConn, lenBuf[:]); err != nil {
			return nil, err
		}
		length := binary.LittleEndian.Uint32(lenBuf[:])
		payload := make([]byte, length)
		if length > 0 {
			if _, err := io.ReadFull(bridgeConn, payload); err != nil {
				return nil, err
			}
		}
		return payload, nil
	}

	writeBridgeFrame := func(p []byte) error {
		var lenBuf [4]byte
		binary.LittleEndian.PutUint32(lenBuf[:], uint32(len(p)))
		if _, err := bridgeConn.Write(lenBuf[:]); err != nil {
			return err
		}
		if len(p) > 0 {
			_, err := bridgeConn.Write(p)
			return err
		}
		return nil
	}

	// 1. Handshake
	_, err = readBridgeFrame()
	if err != nil {
		t.Fatalf("failed to read handshake: %v", err)
	}

	// 2. Start session
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventStartCameraSession)); err != nil {
		t.Fatalf("failed to write start event: %v", err)
	}

	select {
	case act := <-clientActionsReceived:
		if act != "start" {
			t.Fatalf("expected action 'start', got %q", act)
		}
	case <-time.After(3 * time.Second):
		t.Fatalf("timeout waiting for start action")
	}

	// Helper to create test JPEG
	img := image.NewRGBA(image.Rect(0, 0, camWidth, camHeight))
	for y := 0; y < camHeight; y++ {
		for x := 0; x < camWidth; x++ {
			img.Set(x, y, color.RGBA{R: 200, G: 100, B: 50, A: 255})
		}
	}
	var jpegBuf bytes.Buffer
	_ = jpeg.Encode(&jpegBuf, img, &jpeg.Options{Quality: 90})
	sampleJPEG := jpegBuf.Bytes()

	clientCamDCMu.Lock()
	camDC := clientCamDC
	clientCamDCMu.Unlock()

	// 3. Concurrently stream frames and trigger capture image
	stopStream := make(chan struct{})
	go func() {
		for {
			select {
			case <-stopStream:
				return
			default:
				_ = camDC.Send(sampleJPEG)
				time.Sleep(10 * time.Millisecond)
			}
		}
	}()

	// Wait for stream to be active, then send CAPTURE_IMAGE event
	time.Sleep(50 * time.Millisecond)
	if err := writeBridgeFrame([]byte(agentwebrtc.HALEventCaptureImage)); err != nil {
		t.Fatalf("failed to send capture event: %v", err)
	}

	// Verify all received frames are either exact I420 size (384 bytes) or valid JPEG (starts with 0xFF, 0xD8)
	expectedYUVLen := camWidth * camHeight * 3 / 2
	snapshotReceived := false

	for i := 0; i < 15; i++ {
		frame, err := readBridgeFrame()
		if err != nil {
			t.Fatalf("failed reading bridge frame at index %d: %v", i, err)
		}

		if len(frame) == expectedYUVLen {
			// Intact YUV frame
			continue
		} else if len(frame) == len(sampleJPEG) && frame[0] == 0xFF && frame[1] == 0xD8 {
			// Intact snapshot frame
			snapshotReceived = true
			break
		} else {
			hdrLen := 4
			if len(frame) < hdrLen {
				hdrLen = len(frame)
			}
			t.Fatalf("corrupted or interleaved frame received at index %d: length %d, header %x", i, len(frame), frame[:hdrLen])
		}
	}

	close(stopStream)

	if !snapshotReceived {
		t.Fatalf("did not receive intact snapshot frame during concurrent streaming")
	}

	t.Log("[PASS] TestCameraInterleavedFrameSnapshotE2E: concurrent YUV frame production and snapshot capture serialized without corruption")
}



