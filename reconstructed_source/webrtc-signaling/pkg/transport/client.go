// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: ROUTE_HANDLER_AND_STATE_MACHINE
// Endpoint: /connect_client
// Binary Symbol: main.id8ybRmw69lm (VA: 0x7507c0)
// Evidence: CONNECT_CLIENT_STATE_MACHINE.json, TRANSPORT_METHOD_UPGRADE_MATRIX.json,
//   TRANSPORT_AUTH_MATRIX.json, DEVICE_AGENT_CLIENT_ASSOCIATION_CONTRACT.json,
//   TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"

	"github.com/gorilla/websocket"

	"cloudphone-signaling/pkg/devices"
)

// HandleConnectClient handles pre-upgrade authentication, WebSocket upgrade,
// client binding, and signaling relay for /connect_client.
func (h *Hub) HandleConnectClient(w http.ResponseWriter, r *http.Request) {
	// Pre-upgrade authentication check (REQUIRED before Upgrade per TRANSPORT_AUTH_MATRIX.json)
	userRole, assignedDevices, authed := h.authenticateClient(r)
	if !authed {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusUnauthorized)
		_, _ = w.Write([]byte("Unauthorized\n"))
		return
	}

	// Upgrade connection to WebSocket
	ws, err := h.upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}

	clientID := h.AllocateClientID()
	clientConn := &ClientConn{
		ClientID:        clientID,
		UserRole:        userRole,
		AssignedDevices: assignedDevices,
		Conn:            ws,
	}

	h.RegisterClientConn(clientConn)

	var boundDeviceID string

	// Ensure cleanup executes once on close/EOF/error
	defer func() {
		h.CleanupClient(boundDeviceID, clientConn)
	}()

	// 60-second read deadline per TRANSPORT_HEARTBEAT_CONTRACT.json
	_ = ws.SetReadDeadline(time.Now().Add(60 * time.Second))
	ws.SetPongHandler(func(string) error {
		_ = ws.SetReadDeadline(time.Now().Add(60 * time.Second))
		return nil
	})

	// Message read pump
	for {
		messageType, data, err := ws.ReadMessage()
		if err != nil {
			break
		}

		_ = ws.SetReadDeadline(time.Now().Add(60 * time.Second))

		if messageType != websocket.TextMessage {
			continue
		}

		var generic GenericInboundEnvelope
		if err := json.Unmarshal(data, &generic); err != nil {
			continue
		}

		msgType := generic.MessageType
		if msgType == "" {
			msgType = generic.Type
		}

		switch msgType {
		case "connect":
			var connMsg ConnectMessage
			if err := json.Unmarshal(data, &connMsg); err != nil {
				continue
			}
			if connMsg.DeviceID == "" {
				continue
			}

			// Validate user access permission to target device
			if !devices.CanAccessDevice(clientConn.UserRole, clientConn.AssignedDevices, connMsg.DeviceID) {
				continue
			}

			boundDeviceID = connMsg.DeviceID
			clientConn.DeviceID = boundDeviceID
			h.BindClientToDevice(clientConn, boundDeviceID)

			// Update device registry client count and active clients
			if h.deviceReg != nil {
				if dev, exists := h.deviceReg.GetDevice(boundDeviceID); exists {
					dev.Mu.Lock()
					dev.ClientCount++
					dev.Clients = append(dev.Clients, clientID)
					dev.Mu.Unlock()
				}
			}

			// Reply with config message containing ICE servers
			cfg := ConfigMessage{
				MessageType: "config",
				DeviceID:    boundDeviceID,
				ICEServers:  h.GetICEServers(),
			}
			_ = clientConn.WriteJSON(cfg)

			// Broadcast updated device list to all clients
			h.BroadcastDeviceListUpdate()

		case "forward":
			var fwd ForwardEnvelope
			if err := json.Unmarshal(data, &fwd); err != nil {
				continue
			}
			targetDev := boundDeviceID
			if targetDev == "" {
				targetDev = fwd.DeviceID
			}
			_ = h.RelayClientToAgent(targetDev, clientID, fwd.Payload)
		}
	}

}

// authenticateClient inspects request headers and query parameters for valid credentials.
// Corresponds to TRANSPORT_AUTH_MATRIX.json:
// 1. Authorization: Bearer <token>
// 2. ?token=<token>
// 3. ?share_token=<token>
func (h *Hub) authenticateClient(r *http.Request) (role string, assignedDevices []string, ok bool) {
	// Source 1: Authorization header
	authHeader := r.Header.Get("Authorization")
	token := ""
	if authHeader != "" {
		parts := strings.Split(authHeader, " ")
		if len(parts) == 2 && strings.ToLower(parts[0]) == "bearer" {
			token = parts[1]
		} else {
			token = authHeader
		}
	}

	// Source 2: Query param ?token=
	if token == "" {
		token = r.URL.Query().Get("token")
	}

	if h.authMgr != nil {
		if username, err := h.authMgr.ValidateToken(token); err == nil {
			if profile, err := h.authMgr.GetUserProfile(username); err == nil && profile != nil {
				return profile.Role, profile.AssignedDevices, true
			}
			return "user", nil, true
		}
	}

	// Source 3: Query param ?share_token=
	shareToken := r.URL.Query().Get("share_token")
	if shareToken != "" && h.sharesStore != nil {
		if share, exists := h.sharesStore.GetToken(shareToken); exists {
			// Validate share expiration
			if share.ExpiresAt.IsZero() || share.ExpiresAt.After(time.Now()) {
				// Share token grants guest access scoped strictly to assigned device
				return "guest", []string{share.DeviceID}, true
			}
		}
	}


	return "", nil, false
}

