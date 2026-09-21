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
	"fmt"
	"log"
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
	username, userRole, assignedDevices, authed := h.authenticateClient(r)
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
		Username:        username,
		UserRole:        userRole,
		AssignedDevices: assignedDevices,
		Conn:            ws,
	}

	h.RegisterClientConn(clientConn)

	var boundDeviceID string

	// Ping ticker to keep connection alive when client is passively consuming WebRTC stream
	pingTicker := time.NewTicker(20 * time.Second)
	stopPing := make(chan struct{})
	go func() {
		for {
			select {
			case <-pingTicker.C:
				if err := clientConn.WritePing(); err != nil {
					return
				}
			case <-stopPing:
				return
			}
		}
	}()

	// Ensure cleanup executes once on close/EOF/error
	defer func() {
		pingTicker.Stop()
		close(stopPing)

		// Clean up preview subscriptions with debounce protection (Phase R3)
		emptyDevices := h.UnsubscribeClientFromAllPreviews(clientID)
		for _, devID := range emptyDevices {
			tracker := h.GetCoreTracker(devID)
			if tracker != nil {
				tracker.OnStopPreviewSubscriber(clientID, 1500*time.Millisecond, func() {
					stopMsg := StopPreviewMessage{
						MessageType: "stop_preview",
						Type:        "stop_preview",
						DeviceID:    devID,
					}
					_ = h.RelayToAgent(devID, stopMsg)
					log.Printf("[Signaling] Client %d disconnected, debounced auto-stopped preview on empty device %s", clientID, devID)
				})
			} else {
				stopMsg := StopPreviewMessage{
					MessageType: "stop_preview",
					Type:        "stop_preview",
					DeviceID:    devID,
				}
				_ = h.RelayToAgent(devID, stopMsg)
				log.Printf("[Signaling] Client %d disconnected, auto-stopped preview on empty device %s", clientID, devID)
			}
		}

		if boundDeviceID != "" {
			if tracker := h.GetCoreTracker(boundDeviceID); tracker != nil {
				tracker.OnRemoveControlClient(clientID)
				tracker.OnRemoveWebRTCClient(clientID)
			}
		}

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

			// Update device registry client count and active clients, and retrieve DeviceInfo
			var devInfo interface{}
			if h.deviceReg != nil {
				if dev, exists := h.deviceReg.GetDevice(boundDeviceID); exists {
					dev.Mu.Lock()
					dev.ClientCount++
					dev.Clients = append(dev.Clients, clientID)
					if dev.DeviceInfo == nil {
						dev.DeviceInfo = devices.ResolveDeviceGeometry(boundDeviceID)
					}
					devInfo = dev.DeviceInfo
					dev.Mu.Unlock()
				} else {
					devInfo = devices.ResolveDeviceGeometry(boundDeviceID)
				}
			} else {
				devInfo = devices.ResolveDeviceGeometry(boundDeviceID)
			}

			// R5.3.3: Restore server -> client device_info message BEFORE config
			if devInfo != nil {
				deviceInfoMsg := DeviceInfoMessage{
					MessageType: "device_info",
					DeviceID:    boundDeviceID,
					DeviceInfo:  devInfo,
				}
				_ = clientConn.WriteJSON(deviceInfoMsg)
				log.Printf("[Signaling] Sent device_info to client %d for device %s: %+v", clientID, boundDeviceID, devInfo)
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

		case "start_preview":
			var req StartPreviewMessage
			if err := json.Unmarshal(data, &req); err != nil {
				continue
			}
			devID := req.DeviceID
			if devID == "" {
				devID = boundDeviceID
			}
			if devID == "" {
				continue
			}
			if !devices.CanAccessDevice(clientConn.UserRole, clientConn.AssignedDevices, devID) {
				log.Printf("[Signaling] Client %d unauthorized for start_preview on %s", clientID, devID)
				continue
			}

			// Generate or align session generation
			gen := h.NextDeviceGeneration(devID)
			clientConn.Generation = gen
			clientConn.IsWebRTC = false

			tracker := h.GetCoreTracker(devID)
			if tracker != nil {
				// Bidirectional handoff check: If device currently has active WebRTC, begin handoff WebRTC -> WS
				if tracker.WebRTCCount() > 0 {
					tracker.BeginHandoff("webrtc", "websocket", gen, 0, 0, clientID)
				}
				tracker.OnStartPreviewSubscriber(clientID, gen)
			}

			wasFirst := h.SubscribePreview(clientID, devID)
			if wasFirst {
				req.DeviceID = devID
				req.MessageType = "start_preview"
				req.Type = "start_preview"
				if err := h.RelayToAgent(devID, req); err != nil {
					log.Printf("[Signaling] Failed to relay start_preview to %s: %v, rolling back subscription", devID, err)
					h.UnsubscribePreview(clientID, devID)
				} else {
					log.Printf("[Signaling] Forwarding start_preview to %s: fps=%v, max_size=%v, bitrate=%v, stay_awake=%v",
						devID, req.FPS, req.MaxSize, req.Bitrate, req.StayAwake)
				}
			} else {
				log.Printf("[Signaling] Client %d subscribed to existing preview stream on %s", clientID, devID)
			}

		case "stop_preview":
			var req StopPreviewMessage
			if err := json.Unmarshal(data, &req); err != nil {
				continue
			}
			devID := req.DeviceID
			if devID == "" {
				devID = boundDeviceID
			}
			if devID == "" {
				continue
			}

			// Idempotent removal: only proceed if this client was actually subscribed
			removed, wasLast := h.RemovePreviewSubscriber(clientID, devID)
			if !removed {
				// Already unsubscribed, ignore duplicate stop
				continue
			}

			tracker := h.GetCoreTracker(devID)
			if tracker != nil {
				tracker.OnStopPreviewSubscriber(clientID, 1500*time.Millisecond, func() {
					if wasLast {
						req.DeviceID = devID
						req.MessageType = "stop_preview"
						req.Type = "stop_preview"
						_ = h.RelayToAgent(devID, req)
						log.Printf("[Signaling] Forwarding debounced stop_preview to %s", devID)
					}
				})
			} else if wasLast {
				req.DeviceID = devID
				req.MessageType = "stop_preview"
				req.Type = "stop_preview"
				_ = h.RelayToAgent(devID, req)
				log.Printf("[Signaling] Forwarding stop_preview to %s", devID)
			}

		case "stream_ready":
			var req struct {
				MessageType string `json:"message_type"`
				DeviceID    string `json:"device_id"`
				Mode        string `json:"mode"`
				Generation  uint64 `json:"generation"`
				AttemptID   uint32 `json:"attempt_id"`
			}
			if err := json.Unmarshal(data, &req); err == nil {
				devID := req.DeviceID
				if devID == "" {
					devID = boundDeviceID
				}
				if devID != "" {
					if tracker := h.GetCoreTracker(devID); tracker != nil {
						tracker.UpdateHandoffState("COMPLETE")
						tracker.MarkReady(fmt.Sprintf("stream_ready_ack_%s_gen_%d", req.Mode, req.Generation))
					}
					log.Printf("[Signaling] Client %d confirmed stream_ready: dev=%s mode=%s gen=%d attempt=%d",
						clientID, devID, req.Mode, req.Generation, req.AttemptID)
				}
			}

		case "stream_failed":
			var req struct {
				MessageType string `json:"message_type"`
				DeviceID    string `json:"device_id"`
				Mode        string `json:"mode"`
				Generation  uint64 `json:"generation"`
				AttemptID   uint32 `json:"attempt_id"`
				Reason      string `json:"reason"`
			}
			if err := json.Unmarshal(data, &req); err == nil {
				devID := req.DeviceID
				if devID == "" {
					devID = boundDeviceID
				}
				if devID != "" {
					if tracker := h.GetCoreTracker(devID); tracker != nil {
						tracker.UpdateHandoffState("ROLLBACK")
					}
					log.Printf("[Signaling] Client %d reported stream_failed: dev=%s mode=%s gen=%d attempt=%d reason=%s",
						clientID, devID, req.Mode, req.Generation, req.AttemptID, req.Reason)
				}
			}

		case "group_control_event":
			var env GroupControlEnvelope
			if err := json.Unmarshal(data, &env); err != nil {
				continue
			}
			targetDevs := env.TargetDeviceIDs
			if len(targetDevs) == 0 && boundDeviceID != "" {
				targetDevs = []string{boundDeviceID}
			}
			h.RelayGroupControl(clientConn.UserRole, clientConn.AssignedDevices, targetDevs, env.Event, clientConn.Username)

		case "command":
			var cmd CommandMessage
			if err := json.Unmarshal(data, &cmd); err != nil {
				continue
			}
			devID := cmd.DeviceID
			if devID == "" {
				devID = boundDeviceID
			}

			var seq interface{} = "none"
			var rawMap map[string]interface{}
			if err := json.Unmarshal(data, &rawMap); err == nil {
				if s, ok := rawMap["control_seq"]; ok {
					seq = s
				}
			}
			log.Printf("[CTRL] seq=%v event=command type=TOOLBAR relay client=%d dev=%s cmd=%q", seq, clientID, devID, cmd.Command)

			if devID != "" && devices.CanAccessDevice(clientConn.UserRole, clientConn.AssignedDevices, devID) {
				_ = h.RelayToAgent(devID, cmd)
			}

		case "inject_data":
			var inj InjectDataMessage
			if err := json.Unmarshal(data, &inj); err != nil {
				continue
			}
			targetDevs := inj.TargetDeviceIDs
			if len(targetDevs) == 0 && boundDeviceID != "" {
				targetDevs = []string{boundDeviceID}
			}
			for _, devID := range targetDevs {
				if devices.CanAccessDevice(clientConn.UserRole, clientConn.AssignedDevices, devID) {
					_ = h.RelayToAgent(devID, inj)
				}
			}

		case "quit_agent":
			var qa QuitAgentMessage
			if err := json.Unmarshal(data, &qa); err != nil {
				continue
			}
			devID := qa.DeviceID
			if devID == "" {
				devID = boundDeviceID
			}
			if devID != "" && devices.CanAccessDevice(clientConn.UserRole, clientConn.AssignedDevices, devID) {
				_ = h.RelayToAgent(devID, qa)
			}
		}
	}
}

// authenticateClient inspects request headers and query parameters for valid credentials.
// Corresponds to TRANSPORT_AUTH_MATRIX.json:
// 1. Authorization: Bearer <token>
// 2. ?token=<token>
// 3. ?share_token=<token>
func (h *Hub) authenticateClient(r *http.Request) (username string, role string, assignedDevices []string, ok bool) {
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
		if uname, err := h.authMgr.ValidateToken(token); err == nil {
			if profile, err := h.authMgr.GetUserProfile(uname); err == nil && profile != nil {
				return uname, profile.Role, profile.AssignedDevices, true
			}
			return uname, "admin", []string{"*"}, true
		}
	}

	// Source 3: Query param ?share_token=
	shareToken := r.URL.Query().Get("share_token")
	if shareToken != "" && h.sharesStore != nil {
		if share, exists := h.sharesStore.GetToken(shareToken); exists {
			// Validate share expiration
			if share.ExpiresAt.IsZero() || share.ExpiresAt.After(time.Now()) {
				// Share token grants guest access scoped strictly to assigned device
				return "guest", "guest", []string{share.DeviceID}, true
			}
		}
	}

	return "", "", nil, false
}

