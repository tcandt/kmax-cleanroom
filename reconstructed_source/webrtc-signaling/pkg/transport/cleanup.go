// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BEHAVIOR
// Mapping Scope: DISCONNECT_CLEANUP_AND_IDEMPOTENCY
// Evidence: TRANSPORT_DISCONNECT_CLEANUP_CONTRACT.json, TRANSPORT_CONCURRENCY_CONTRACT.json,
//   TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Binary Symbols: main.lv6Xh7 (VA: 0x74da60)
// Mechanism: sync.Once is selected as an IMPLEMENTATION_CHOICE to ensure strict idempotency.
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

// CleanupDevice performs deterministic and idempotent teardown of a device connection.
// Safely closes the socket, removes registration from the hub, marks device offline in registry,
// and broadcasts device_list_update.
func (h *Hub) CleanupDevice(deviceID string, dc *DeviceConn) {
	if dc == nil {
		return
	}

	_ = dc.Close()

	if deviceID != "" {
		if h.UnregisterDeviceConn(deviceID, dc) {
			if h.deviceReg != nil {
				h.deviceReg.DisconnectDevice(deviceID)
			}
			h.BroadcastDeviceListUpdate()
		}
	}
}

// CleanupAgent performs deterministic and idempotent teardown of an agent connection.
// Safely closes the socket, removes agent binding from the hub, and broadcasts device_list_update.
func (h *Hub) CleanupAgent(deviceID string, ac *AgentConn) {
	if ac == nil {
		return
	}

	_ = ac.Close()

	if deviceID != "" {
		if h.UnregisterAgentConn(deviceID, ac) {
			h.BroadcastDeviceListUpdate()
		}
	}
}

// CleanupClient performs deterministic and idempotent teardown of a client connection.
// Safely closes the socket, removes client from routing maps, decrements client count on device,
// and broadcasts device_list_update.
func (h *Hub) CleanupClient(deviceID string, cc *ClientConn) {
	if cc == nil {
		return
	}

	_ = cc.Close()

	if h.UnregisterClientConn(cc) {
		if deviceID != "" && h.deviceReg != nil {
			if dev, exists := h.deviceReg.GetDevice(deviceID); exists {
				dev.Mu.Lock()
				if dev.ClientCount > 0 {
					dev.ClientCount--
				}
				newClients := make([]interface{}, 0, len(dev.Clients))
				for _, c := range dev.Clients {
					if cid, ok := c.(uint32); ok && cid == cc.ClientID {
						continue
					}
					newClients = append(newClients, c)
				}
				dev.Clients = newClients
				dev.Mu.Unlock()
			}

			// Notify agent of client disconnection matching original binary behavior
			if ag, ok := h.GetAgentConn(deviceID); ok && ag != nil {
				_ = ag.WriteJSON(map[string]interface{}{
					"message_type": "client_disconnected",
					"device_id":    deviceID,
					"client_id":    cc.ClientID,
				})
			}

			h.BroadcastDeviceListUpdate()
		}
	}
}
