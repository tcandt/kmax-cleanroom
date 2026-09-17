// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: ROUTE_HANDLER_AND_STATE_MACHINE
// Endpoint: /register_device
// Binary Symbol: main.rQffYkwYhw (VA: 0x74e4a0)
// Evidence: REGISTER_DEVICE_STATE_MACHINE.json, TRANSPORT_METHOD_UPGRADE_MATRIX.json,
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

// HandleRegisterDevice handles the WebSocket upgrade and device lifecycle for /register_device.
// Public endpoint (no pre-upgrade auth, per TRANSPORT_AUTH_MATRIX.json).
func (h *Hub) HandleRegisterDevice(w http.ResponseWriter, r *http.Request) {
	// Gorilla WebSocket handles RFC 6455 upgrade verification and error status (400 Bad Request)
	ws, err := h.upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}

	devConn := &DeviceConn{
		Conn: ws,
	}

	var boundDeviceID string

	// Ensure cleanup executes once on close/EOF/error
	defer func() {
		h.CleanupDevice(boundDeviceID, devConn)
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

		// Refresh read deadline on every valid incoming frame
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
		case "register":
			var reg RegisterMessage
			if err := json.Unmarshal(data, &reg); err != nil {
				continue
			}
			if reg.DeviceID == "" {
				continue
			}

			boundDeviceID = reg.DeviceID
			devConn.DeviceID = boundDeviceID

			// Update device registry (online = true)
			if h.deviceReg != nil {
				h.deviceReg.RegisterDevice(boundDeviceID, reg.DeviceInfo, false)
			}

			// Register in Hub (replaces previous connection if duplicate)
			h.RegisterDeviceConn(boundDeviceID, devConn)

			// Reply with config containing ICE servers
			cfg := ConfigMessage{
				MessageType: "config",
				DeviceID:    boundDeviceID,
				ICEServers:  h.GetICEServers(),
			}
			_ = devConn.WriteJSON(cfg)

			// Broadcast device list update to all connected clients
			h.BroadcastDeviceListUpdate()

		case "forward":
			var fwd ForwardEnvelope
			if err := json.Unmarshal(data, &fwd); err != nil {
				continue
			}
			_ = h.RelayAgentToClient(boundDeviceID, fwd.ClientID, fwd.Payload)

		case "unregister":
			return
		}
	}

}
