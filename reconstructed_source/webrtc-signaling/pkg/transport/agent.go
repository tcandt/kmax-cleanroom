// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: ROUTE_HANDLER_AND_STATE_MACHINE
// Endpoint: /register_agent
// Binary Symbol: main.jdUaLc5NMO5 (VA: 0x754b40)
// Evidence: REGISTER_AGENT_STATE_MACHINE.json, TRANSPORT_METHOD_UPGRADE_MATRIX.json,
//   TRANSPORT_AUTH_MATRIX.json, TRANSPORT_HEARTBEAT_CONTRACT.json,
//   TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

// HandleRegisterAgent handles the WebSocket upgrade and agent lifecycle for /register_agent.
// Public endpoint (no pre-upgrade auth, per TRANSPORT_AUTH_MATRIX.json).
func (h *Hub) HandleRegisterAgent(w http.ResponseWriter, r *http.Request) {
	// Gorilla WebSocket handles RFC 6455 upgrade verification and error status (400 Bad Request)
	ws, err := h.upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}

	agentConn := &AgentConn{
		Conn: ws,
	}

	var boundDeviceID string

	// Ensure cleanup executes once on close/EOF/error
	defer func() {
		h.CleanupAgent(boundDeviceID, agentConn)
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

		// Refresh read deadline on every incoming frame
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
		case "agent_register":
			var reg AgentRegisterMessage
			if err := json.Unmarshal(data, &reg); err != nil {
				continue
			}
			if reg.DeviceID == "" {
				continue
			}

			boundDeviceID = reg.DeviceID
			agentConn.DeviceID = boundDeviceID

			// Update device registry entry if present
			if h.deviceReg != nil {
				h.deviceReg.RegisterDevice(boundDeviceID, nil, reg.IsWebRTC)
			}

			// Register in Hub (replaces previous agent connection if duplicate)
			h.RegisterAgentConn(boundDeviceID, agentConn)

			// Reply with agent_register_ok
			ack := AgentRegisterOkMessage{
				MessageType: "agent_register_ok",
				Status:      "ok",
			}
			_ = agentConn.WriteJSON(ack)

			// Broadcast updated device status
			h.BroadcastDeviceListUpdate()

		case "heartbeat":
			// Update last_seen timestamp in device registry if device is registered
			if boundDeviceID != "" && h.deviceReg != nil {
				if dev, exists := h.deviceReg.GetDevice(boundDeviceID); exists {
					dev.Mu.Lock()
					dev.LastSeen = time.Now()
					dev.Mu.Unlock()
				}
			}

		case "forward":
			var fwd ForwardEnvelope
			if err := json.Unmarshal(data, &fwd); err != nil {
				continue
			}
			_ = h.RelayAgentToClient(boundDeviceID, fwd.ClientID, fwd.Payload)
		}
	}

}
