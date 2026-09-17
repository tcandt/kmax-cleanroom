// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: CENTRAL_TRANSPORT_HUB_AND_ROUTING
// Evidence: TRANSPORT_CONCURRENCY_CONTRACT.json, DEVICE_AGENT_CLIENT_ASSOCIATION_CONTRACT.json,
//   TRANSPORT_IMPLEMENTATION_CONTRACT.json
// Binary Symbols: main.u8Z_Xk, main.lv6Xh7
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

import (
	"net/http"
	"sync"
	"sync/atomic"

	"github.com/gorilla/websocket"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/devices"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// DeviceConn encapsulates a registered device WebSocket connection.
type DeviceConn struct {
	DeviceID string
	Conn     *websocket.Conn
	WriteMu  sync.Mutex
	Closed   sync.Once
}

// WriteJSON sends a JSON frame with serialized write protection.
func (dc *DeviceConn) WriteJSON(v interface{}) error {
	dc.WriteMu.Lock()
	defer dc.WriteMu.Unlock()
	return dc.Conn.WriteJSON(v)
}

// Close safely closes the WebSocket connection.
func (dc *DeviceConn) Close() error {
	var err error
	dc.Closed.Do(func() {
		err = dc.Conn.Close()
	})
	return err
}

// AgentConn encapsulates a registered agent WebSocket connection.
type AgentConn struct {
	DeviceID string
	Conn     *websocket.Conn
	WriteMu  sync.Mutex
	Closed   sync.Once
}

// WriteJSON sends a JSON frame with serialized write protection.
func (ac *AgentConn) WriteJSON(v interface{}) error {
	ac.WriteMu.Lock()
	defer ac.WriteMu.Unlock()
	return ac.Conn.WriteJSON(v)
}

// Close safely closes the WebSocket connection.
func (ac *AgentConn) Close() error {
	var err error
	ac.Closed.Do(func() {
		err = ac.Conn.Close()
	})
	return err
}

// ClientConn encapsulates an authenticated client WebSocket connection.
type ClientConn struct {
	ClientID        uint32
	DeviceID        string
	Conn            *websocket.Conn
	UserRole        string
	AssignedDevices []string
	WriteMu         sync.Mutex
	Closed          sync.Once
}

// WriteJSON sends a JSON frame with serialized write protection.
func (cc *ClientConn) WriteJSON(v interface{}) error {
	cc.WriteMu.Lock()
	defer cc.WriteMu.Unlock()
	return cc.Conn.WriteJSON(v)
}

// Close safely closes the WebSocket connection.
func (cc *ClientConn) Close() error {
	var err error
	cc.Closed.Do(func() {
		err = cc.Conn.Close()
	})
	return err
}

// Hub manages active WebSocket connections, signaling routing, and device/client mappings.
type Hub struct {
	deviceReg   *devices.Registry
	authMgr     *auth.Authenticator
	sharesStore *storage.SharesStore

	iceServersMu sync.RWMutex
	iceServers   []types.ICEServer

	upgrader websocket.Upgrader

	// Active device WebSocket connections
	devicesMu sync.RWMutex
	devices   map[string]*DeviceConn

	// Active agent WebSocket connections (1 active agent per device)
	agentsMu sync.RWMutex
	agents   map[string]*AgentConn

	// Active client WebSocket connections (0 to N clients per device)
	clientsMu     sync.RWMutex
	clients       map[uint32]*ClientConn
	deviceClients map[string]map[uint32]*ClientConn

	// Monotonically increasing atomic client ID generator (IMPLEMENTATION_CHOICE)
	nextClientID uint32
}

// NewHub instantiates a clean-room transport Hub.
func NewHub(deviceReg *devices.Registry, authMgr *auth.Authenticator, sharesStore *storage.SharesStore, iceServers []types.ICEServer) *Hub {
	if iceServers == nil {
		iceServers = []types.ICEServer{
			{URLs: []string{"stun:stun.l.google.com:19302"}},
		}
	}

	return &Hub{
		deviceReg:   deviceReg,
		authMgr:     authMgr,
		sharesStore: sharesStore,
		iceServers:  iceServers,
		upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
			CheckOrigin: func(r *http.Request) bool {
				return true
			},
			EnableCompression: false,
		},
		devices:       make(map[string]*DeviceConn),
		agents:        make(map[string]*AgentConn),
		clients:       make(map[uint32]*ClientConn),
		deviceClients: make(map[string]map[uint32]*ClientConn),
		nextClientID:  0,
	}
}

// SetICEServers updates the ICE server configuration pushed to connecting peers.
func (h *Hub) SetICEServers(servers []types.ICEServer) {
	h.iceServersMu.Lock()
	defer h.iceServersMu.Unlock()
	h.iceServers = servers
}

// SetSharesStore updates the SharesStore used for share token validation.
func (h *Hub) SetSharesStore(ss *storage.SharesStore) {
	h.sharesStore = ss
}


// GetICEServers returns a copy of current ICE servers.
func (h *Hub) GetICEServers() []types.ICEServer {
	h.iceServersMu.RLock()
	defer h.iceServersMu.RUnlock()
	copied := make([]types.ICEServer, len(h.iceServers))
	copy(copied, h.iceServers)
	return copied
}

// AllocateClientID generates a unique uint32 client identifier (IMPLEMENTATION_CHOICE: atomic counter).
func (h *Hub) AllocateClientID() uint32 {
	return atomic.AddUint32(&h.nextClientID, 1)
}

// BroadcastDeviceListUpdate sends device summary updates to all currently active client sessions.
// Corresponds to symbol main.lv6Xh7 and oracle case TR-E2E-CLI-CONNECT.
func (h *Hub) BroadcastDeviceListUpdate() {
	if h.deviceReg == nil {
		return
	}

	h.clientsMu.RLock()
	clientList := make([]*ClientConn, 0, len(h.clients))
	for _, client := range h.clients {
		clientList = append(clientList, client)
	}
	h.clientsMu.RUnlock()

	for _, client := range clientList {
		dtos := h.deviceReg.GetDevices(client.UserRole, client.AssignedDevices)
		msg := DeviceListUpdateMessage{
			MessageType: "device_list_update",
			Devices:     dtos,
		}
		_ = client.WriteJSON(msg)
	}
}

// RegisterDeviceConn binds a device connection to its device_id in the hub.
func (h *Hub) RegisterDeviceConn(deviceID string, dc *DeviceConn) *DeviceConn {
	h.devicesMu.Lock()
	old, exists := h.devices[deviceID]
	h.devices[deviceID] = dc
	h.devicesMu.Unlock()

	if exists && old != nil && old != dc {
		_ = old.Close()
	}
	return old
}

// UnregisterDeviceConn unbinds a device connection if matching current instance.
func (h *Hub) UnregisterDeviceConn(deviceID string, dc *DeviceConn) bool {
	h.devicesMu.Lock()
	curr, exists := h.devices[deviceID]
	if exists && curr == dc {
		delete(h.devices, deviceID)
		h.devicesMu.Unlock()
		return true
	}
	h.devicesMu.Unlock()
	return false
}

// RegisterAgentConn binds an agent connection to its device_id in the hub.
func (h *Hub) RegisterAgentConn(deviceID string, ac *AgentConn) *AgentConn {
	h.agentsMu.Lock()
	old, exists := h.agents[deviceID]
	h.agents[deviceID] = ac
	h.agentsMu.Unlock()

	if exists && old != nil && old != ac {
		_ = old.Close()
	}
	return old
}

// UnregisterAgentConn unbinds an agent connection if matching current instance.
func (h *Hub) UnregisterAgentConn(deviceID string, ac *AgentConn) bool {
	h.agentsMu.Lock()
	curr, exists := h.agents[deviceID]
	if exists && curr == ac {
		delete(h.agents, deviceID)
		h.agentsMu.Unlock()
		return true
	}
	h.agentsMu.Unlock()
	return false
}

// GetAgentConn retrieves the active agent connection for a given device_id.
func (h *Hub) GetAgentConn(deviceID string) (*AgentConn, bool) {
	h.agentsMu.RLock()
	defer h.agentsMu.RUnlock()
	ac, exists := h.agents[deviceID]
	return ac, exists
}

// RegisterClientConn adds a client connection to the hub routing tables.
func (h *Hub) RegisterClientConn(cc *ClientConn) {
	h.clientsMu.Lock()
	defer h.clientsMu.Unlock()

	h.clients[cc.ClientID] = cc
	if cc.DeviceID != "" {
		dm, exists := h.deviceClients[cc.DeviceID]
		if !exists {
			dm = make(map[uint32]*ClientConn)
			h.deviceClients[cc.DeviceID] = dm
		}
		dm[cc.ClientID] = cc
	}
}

// BindClientToDevice associates an unbound client connection to a specific device.
func (h *Hub) BindClientToDevice(cc *ClientConn, deviceID string) {
	h.clientsMu.Lock()
	defer h.clientsMu.Unlock()

	// If previously bound to another device, remove from old map
	if cc.DeviceID != "" && cc.DeviceID != deviceID {
		if oldDm, exists := h.deviceClients[cc.DeviceID]; exists {
			delete(oldDm, cc.ClientID)
			if len(oldDm) == 0 {
				delete(h.deviceClients, cc.DeviceID)
			}
		}
	}

	cc.DeviceID = deviceID
	dm, exists := h.deviceClients[deviceID]
	if !exists {
		dm = make(map[uint32]*ClientConn)
		h.deviceClients[deviceID] = dm
	}
	dm[cc.ClientID] = cc
}

// UnregisterClientConn removes a client connection from hub routing tables.
func (h *Hub) UnregisterClientConn(cc *ClientConn) bool {
	h.clientsMu.Lock()
	defer h.clientsMu.Unlock()

	curr, exists := h.clients[cc.ClientID]
	if exists && curr == cc {
		delete(h.clients, cc.ClientID)
		if cc.DeviceID != "" {
			if dm, ok := h.deviceClients[cc.DeviceID]; ok {
				delete(dm, cc.ClientID)
				if len(dm) == 0 {
					delete(h.deviceClients, cc.DeviceID)
				}
			}
		}
		return true
	}
	return false
}

// GetClientConn retrieves a client connection by its client_id.
func (h *Hub) GetClientConn(clientID uint32) (*ClientConn, bool) {
	h.clientsMu.RLock()
	defer h.clientsMu.RUnlock()
	cc, exists := h.clients[clientID]
	return cc, exists
}
