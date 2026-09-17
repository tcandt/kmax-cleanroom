// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: LEVEL_C_ORIGINAL_ORACLE_SIGNALING_COMPATIBILITY_TEST
// Evidence: TRANSPORT_MESSAGE_MATRIX.json, WEBRTC_SIGNALING_CONTRACT.json,
//   WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Target Oracle: cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe
// Canonical SHA256: 374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package tests

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
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

const canonicalOracleSHA256 = "374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917"

func getFreePort() (int, error) {
	l, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		return 0, err
	}
	defer l.Close()
	return l.Addr().(*net.TCPAddr).Port, nil
}

// TestOriginalSignalingOracleCompatibility runs Level C testing of the reconstructed Agent
// directly against the running original Windows binary (webrtc-signaling.exe).
func TestOriginalSignalingOracleCompatibility(t *testing.T) {
	if runtime.GOOS != "windows" {
		t.Skip("Original binary is Windows AMD64 PE; skipping on non-Windows environment (ENVIRONMENT_UNAVAILABLE)")
	}

	// Locate original executable relative to workspace
	// From reconstructed_source/cloudphone-agent/tests -> root is ../../../
	wd, err := os.Getwd()
	if err != nil {
		t.Fatalf("failed to get working dir: %v", err)
	}
	repoRoot := filepath.Clean(filepath.Join(wd, "..", "..", ".."))
	oracleExe := filepath.Join(repoRoot, "cloudphone-v0.3.6 (1)", "bin", "windows_amd64", "webrtc-signaling.exe")
	assetsDir := filepath.Join(repoRoot, "cloudphone-v0.3.6 (1)", "assets")

	if _, err := os.Stat(oracleExe); os.IsNotExist(err) {
		t.Skipf("Original oracle binary not found at %s (ENVIRONMENT_UNAVAILABLE)", oracleExe)
	}

	// Verify SHA-256 matches canonical hash
	oracleBytes, err := os.ReadFile(oracleExe)
	if err != nil {
		t.Fatalf("failed to read oracle binary: %v", err)
	}
	h := sha256.Sum256(oracleBytes)
	actualHash := hex.EncodeToString(h[:])
	if actualHash != canonicalOracleSHA256 {
		t.Fatalf("oracle binary SHA-256 mismatch: got %s, expected %s", actualHash, canonicalOracleSHA256)
	}
	t.Logf("[PASS] Original Oracle SHA-256 verified: %s", actualHash)

	// Prepare temp data directory with deterministic users.json
	tmpDir, err := os.MkdirTemp("", "oracle_compat_test_*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	salt := "test_salt_123"
	pwdHash := func(pwd string) string {
		sh := sha256.Sum256([]byte(pwd + salt))
		return hex.EncodeToString(sh[:])
	}

	usersData := map[string]interface{}{
		"admin": map[string]interface{}{
			"username":         "admin",
			"password":         pwdHash("admin123"),
			"salt":             salt,
			"role":             "admin",
			"assigned_devices": []string{"*"},
			"expires_at":       "0001-01-01T00:00:00Z",
		},
	}
	usersBytes, _ := json.MarshalIndent(usersData, "", "  ")
	_ = os.WriteFile(filepath.Join(tmpDir, "users.json"), usersBytes, 0644)

	port, err := getFreePort()
	if err != nil {
		t.Fatalf("failed to get free port: %v", err)
	}

	// Launch oracle process
	cmd := exec.Command(oracleExe, "-tls=false", fmt.Sprintf("-port=%d", port), fmt.Sprintf("-data=%s", tmpDir), fmt.Sprintf("-assets=%s", assetsDir))
	cmd.Dir = tmpDir
	if err := cmd.Start(); err != nil {
		t.Fatalf("failed to start oracle binary: %v", err)
	}
	defer func() {
		if cmd.Process != nil {
			_ = cmd.Process.Kill()
		}
	}()

	// Wait for health check
	healthURL := fmt.Sprintf("http://127.0.0.1:%d/api/version", port)
	healthy := false
	for i := 0; i < 30; i++ {
		resp, err := http.Get(healthURL)
		if err == nil && resp.StatusCode == 200 {
			_ = resp.Body.Close()
			healthy = true
			break
		}
		if resp != nil {
			_ = resp.Body.Close()
		}
		time.Sleep(100 * time.Millisecond)
	}
	if !healthy {
		t.Fatalf("oracle binary failed health check on port %d", port)
	}
	t.Logf("[PASS] Original Oracle is healthy on port %d", port)

	// Obtain JWT auth token for client connection
	loginURL := fmt.Sprintf("http://127.0.0.1:%d/api/login", port)
	loginBody := strings.NewReader(`{"username":"admin","password":"admin123"}`)
	loginResp, err := http.Post(loginURL, "application/json", loginBody)
	if err != nil || loginResp.StatusCode != 200 {
		t.Fatalf("failed to login to oracle: %v (status %v)", err, loginResp.StatusCode)
	}
	loginData, _ := io.ReadAll(loginResp.Body)
	_ = loginResp.Body.Close()

	var loginResult struct {
		Token string `json:"token"`
	}
	_ = json.Unmarshal(loginData, &loginResult)
	if loginResult.Token == "" {
		t.Fatalf("empty token from oracle login")
	}

	// 1. Reconstructed Agent registers with Original Oracle via /register_agent
	agentDeviceID := "oracle-compat-dev-01"
	coord := agent.NewCoordinator(agentDeviceID, nil)
	defer coord.Close()

	agentWSURL := fmt.Sprintf("ws://127.0.0.1:%d/register_agent", port)
	sigClient := signaling.NewClient(agentDeviceID, agentWSURL, coord)
	coord.SetSignalingClient(sigClient)

	if err := sigClient.Connect(); err != nil {
		t.Fatalf("reconstructed agent failed to register with original oracle: %v", err)
	}
	defer sigClient.Close()
	t.Log("[PASS] Reconstructed Agent registered with Original Oracle (TR-DIFF-AGT-REGISTER-OK)")

	// 2. Client connects to Original Oracle via /connect_client?token=...
	clientWSURL := fmt.Sprintf("ws://127.0.0.1:%d/connect_client?token=%s", port, url.QueryEscape(loginResult.Token))
	dialer := websocket.Dialer{}
	clientWS, _, err := dialer.Dial(clientWSURL, nil)
	if err != nil {
		t.Fatalf("client failed to connect to oracle /connect_client: %v", err)
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
		"device_id":    agentDeviceID,
	})

	// Client reads config from oracle
	_, cfgData, err := clientWS.ReadMessage()
	if err != nil {
		t.Fatalf("client failed to read config from oracle: %v", err)
	}
	var cfg struct {
		MessageType string `json:"message_type"`
	}
	_ = json.Unmarshal(cfgData, &cfg)
	if cfg.MessageType != "config" {
		t.Errorf("expected config message, got %s", cfg.MessageType)
	}
	t.Log("[PASS] Client connected to Original Oracle and received config")

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

	// Client sends request-offer to oracle
	_ = safeClientWrite(map[string]interface{}{
		"message_type": "forward",
		"payload": map[string]interface{}{
			"type": "request-offer",
		},
	})

	// Client message pump reading from oracle
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
						_ = clientPC.SetRemoteDescription(webrtc.SessionDescription{
							Type: webrtc.SDPTypeOffer,
							SDP:  inner.SDP,
						})
						ans, ansErr := clientPC.CreateAnswer(nil)
						if ansErr == nil {
							_ = clientPC.SetLocalDescription(ans)
							_ = safeClientWrite(map[string]interface{}{
								"message_type": "forward",
								"payload": map[string]interface{}{
									"type": "answer",
									"sdp":  ans.SDP,
								},
							})
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

	// 4. Await P2P connection through Original Oracle
	select {
	case <-clientConnected:
		t.Log("[PASS] EXACT_PROTOCOL_PARITY: Reconstructed Agent successfully negotiated PeerConnection via Original Oracle!")
	case <-time.After(5 * time.Second):
		t.Fatalf("timeout waiting for PeerConnection through original oracle signaling")
	}

	if coord.ActiveSessionCount() != 1 {
		t.Errorf("expected 1 active session, got %d", coord.ActiveSessionCount())
	}
}
