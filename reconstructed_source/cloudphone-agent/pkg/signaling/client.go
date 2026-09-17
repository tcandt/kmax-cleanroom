// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_PROTOCOL
// Mapping Scope: AGENT_SIGNALING_WEBSOCKET_CLIENT
// Evidence: TRANSPORT_MESSAGE_MATRIX.json, WEBRTC_SIGNALING_CONTRACT.json,
//   TRANSPORT_HEARTBEAT_CONTRACT.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package signaling

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
)

var (
	ErrClientClosed        = errors.New("signaling client is closed")
	ErrRegistrationFailed  = errors.New("agent registration failed on signaling server")
	ErrRegistrationTimeout = errors.New("agent registration response timed out")
)

// InboundHandler callbacks for signaling events.
// Classification: GENERATED_ADAPTER.
type InboundHandler interface {
	HandleForward(clientID uint32, payload json.RawMessage)
	HandleClientDisconnected(clientID uint32)
	HandleConfig(iceServers []webrtc.ICEServer)
}

// Client represents the WebSocket signaling client running inside the cloudphone-agent.
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
type Client struct {
	deviceID string
	wsURL    string

	ws      *websocket.Conn
	writeMu sync.Mutex

	handler InboundHandler

	closed     bool
	closedMu   sync.RWMutex
	closedOnce sync.Once
	stopChan   chan struct{}
}

// NewClient creates a new signaling client configured for the target device and server URL.
// Classification: GENERATED_ADAPTER.
func NewClient(deviceID string, wsURL string, handler InboundHandler) *Client {
	return &Client{
		deviceID: deviceID,
		wsURL:    wsURL,
		handler:  handler,
		stopChan: make(chan struct{}),
	}
}

// Connect dials the signaling server, upgrades to WebSocket, and performs agent registration.
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
func (c *Client) Connect() error {
	u, err := url.Parse(c.wsURL)
	if err != nil {
		return fmt.Errorf("invalid signaling url: %w", err)
	}

	// Dial WebSocket endpoint /register_agent
	dialer := websocket.Dialer{
		HandshakeTimeout: 10 * time.Second,
	}
	ws, resp, err := dialer.Dial(u.String(), http.Header{})
	if err != nil {
		if resp != nil {
			return fmt.Errorf("failed to connect to signaling server (status %d): %w", resp.StatusCode, err)
		}
		return fmt.Errorf("failed to dial signaling server: %w", err)
	}
	c.ws = ws

	// 1. Send Agent Registration Envelope matching TR-DIFF-AGT-REGISTER-OK
	regMsg := map[string]interface{}{
		"type":        "agent_register",
		"device_id":   c.deviceID,
		"scrcpy_addr": "",
		"is_webrtc":   true,
	}
	if err := c.WriteJSON(regMsg); err != nil {
		_ = ws.Close()
		return fmt.Errorf("failed to send agent_register: %w", err)
	}

	// 2. Await agent_register_ok frame (with 5s bounded timeout)
	_ = ws.SetReadDeadline(time.Now().Add(5 * time.Second))
	_, ackData, err := ws.ReadMessage()
	if err != nil {
		_ = ws.Close()
		return fmt.Errorf("error reading agent_register_ok: %w", err)
	}

	var ack struct {
		MessageType string `json:"message_type"`
		Status      string `json:"status"`
	}
	if err := json.Unmarshal(ackData, &ack); err != nil || ack.MessageType != "agent_register_ok" || ack.Status != "valid" {
		_ = ws.Close()
		return fmt.Errorf("%w: response=%s", ErrRegistrationFailed, string(ackData))
	}

	// Start pump and heartbeat routines
	go c.readPump()
	go c.heartbeatLoop()

	return nil
}

// WriteJSON sends a JSON-encoded payload over the WebSocket connection with concurrency protection.
// Classification: IMPLEMENTATION_CHOICE (safe mutex-guarded write).
func (c *Client) WriteJSON(v interface{}) error {
	c.closedMu.RLock()
	if c.closed || c.ws == nil {
		c.closedMu.RUnlock()
		return ErrClientClosed
	}
	c.closedMu.RUnlock()

	c.writeMu.Lock()
	defer c.writeMu.Unlock()
	return c.ws.WriteJSON(v)
}

// SendForward sends a WebRTC payload destined for a specific client wrapped in a forward envelope.
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
func (c *Client) SendForward(clientID uint32, payload interface{}) error {
	raw, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal forward payload: %w", err)
	}

	envelope := map[string]interface{}{
		"message_type": "forward",
		"device_id":    c.deviceID,
		"client_id":    clientID,
		"payload":      json.RawMessage(raw),
	}
	return c.WriteJSON(envelope)
}

// SendHeartbeat sends a heartbeat keepalive frame.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (c *Client) SendHeartbeat() error {
	hb := map[string]interface{}{
		"message_type": "heartbeat",
		"device_id":    c.deviceID,
	}
	return c.WriteJSON(hb)
}

// readPump receives and dispatches inbound signaling messages.
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
func (c *Client) readPump() {
	defer func() {
		_ = c.Close()
	}()

	for {
		_ = c.ws.SetReadDeadline(time.Now().Add(60 * time.Second))
		messageType, data, err := c.ws.ReadMessage()
		if err != nil {
			break
		}
		if messageType != websocket.TextMessage {
			continue
		}

		var envelope struct {
			MessageType string          `json:"message_type"`
			Type        string          `json:"type"`
			DeviceID    string          `json:"device_id"`
			ClientID    uint32          `json:"client_id"`
			Payload     json.RawMessage `json:"payload"`
			ICEServers  []struct {
				URLs       interface{} `json:"urls"`
				Username   string      `json:"username,omitempty"`
				Credential string      `json:"credential,omitempty"`
			} `json:"ice_servers,omitempty"`
		}

		if err := json.Unmarshal(data, &envelope); err != nil {
			continue
		}

		msgType := envelope.MessageType
		if msgType == "" {
			msgType = envelope.Type
		}

		switch msgType {
		case "forward":
			if c.handler != nil && envelope.ClientID != 0 {
				c.handler.HandleForward(envelope.ClientID, envelope.Payload)
			}
		case "client_disconnected":
			if c.handler != nil && envelope.ClientID != 0 {
				c.handler.HandleClientDisconnected(envelope.ClientID)
			}
		case "config":
			if c.handler != nil && len(envelope.ICEServers) > 0 {
				servers := make([]webrtc.ICEServer, 0, len(envelope.ICEServers))
				for _, s := range envelope.ICEServers {
					var urls []string
					switch u := s.URLs.(type) {
					case string:
						urls = []string{u}
					case []interface{}:
						for _, item := range u {
							if str, ok := item.(string); ok {
								urls = append(urls, str)
							}
						}
					}
					servers = append(servers, webrtc.ICEServer{
						URLs:           urls,
						Username:       s.Username,
						Credential:     s.Credential,
						CredentialType: webrtc.ICECredentialTypePassword,
					})
				}
				c.handler.HandleConfig(servers)
			}
		}
	}
}

// heartbeatLoop periodically sends heartbeat keepalive messages every 25 seconds
// (safely inside the 60s read deadline confirmed in TRANSPORT_HEARTBEAT_CONTRACT.json).
// Classification: RECONSTRUCTED_FROM_PROTOCOL.
func (c *Client) heartbeatLoop() {
	ticker := time.NewTicker(25 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-c.stopChan:
			return
		case <-ticker.C:
			if err := c.SendHeartbeat(); err != nil {
				return
			}
		}
	}
}

// Close terminates the signaling client and shuts down socket connections.
// Classification: IMPLEMENTATION_CHOICE (idempotent shutdown).
func (c *Client) Close() error {
	var closeErr error
	c.closedOnce.Do(func() {
		c.closedMu.Lock()
		c.closed = true
		c.closedMu.Unlock()

		close(c.stopChan)
		if c.ws != nil {
			closeErr = c.ws.Close()
		}
	})
	return closeErr
}
