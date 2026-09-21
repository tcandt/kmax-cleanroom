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
	"fmt"
	"log"
	"net/http"
	"sync"
	"sync/atomic"
	"time"

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

// WriteMessage sends a raw WebSocket frame with serialized write protection.
func (dc *DeviceConn) WriteMessage(messageType int, data []byte) error {
	dc.WriteMu.Lock()
	defer dc.WriteMu.Unlock()
	return dc.Conn.WriteMessage(messageType, data)
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

// WriteMessage sends a raw WebSocket frame with serialized write protection.
func (ac *AgentConn) WriteMessage(messageType int, data []byte) error {
	ac.WriteMu.Lock()
	defer ac.WriteMu.Unlock()
	return ac.Conn.WriteMessage(messageType, data)
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
	Username        string
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

// WriteMessage sends a raw WebSocket frame with serialized write protection.
func (cc *ClientConn) WriteMessage(messageType int, data []byte) error {
	cc.WriteMu.Lock()
	defer cc.WriteMu.Unlock()
	return cc.Conn.WriteMessage(messageType, data)
}

// WritePing sends an RFC 6455 Ping frame with serialized write protection.
func (cc *ClientConn) WritePing() error {
	cc.WriteMu.Lock()
	defer cc.WriteMu.Unlock()
	return cc.Conn.WriteControl(websocket.PingMessage, []byte{}, time.Now().Add(5*time.Second))
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

	// Active preview subscribers (deviceID -> clientID -> ClientConn)
	// Decoupled from WebRTC deviceClients to prevent lifecycle conflation.
	previewSubscribersMu sync.RWMutex
	previewSubscribers   map[string]map[uint32]*ClientConn

	// CoreService State Machine & Reference Trackers (Phase R3)
	coreTrackersMu sync.RWMutex
	coreTrackers   map[string]*DeviceCoreTracker

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
		devices:            make(map[string]*DeviceConn),
		agents:             make(map[string]*AgentConn),
		clients:            make(map[uint32]*ClientConn),
		deviceClients:      make(map[string]map[uint32]*ClientConn),
		previewSubscribers: make(map[string]map[uint32]*ClientConn),
		coreTrackers:       make(map[string]*DeviceCoreTracker),
		nextClientID:       0,
	}
}

// GetCoreTracker retrieves or creates the DeviceCoreTracker for a device.
func (h *Hub) GetCoreTracker(deviceID string) *DeviceCoreTracker {
	if deviceID == "" {
		return nil
	}
	h.coreTrackersMu.Lock()
	defer h.coreTrackersMu.Unlock()
	tr, ok := h.coreTrackers[deviceID]
	if !ok {
		tr = NewDeviceCoreTracker(deviceID)
		h.coreTrackers[deviceID] = tr
	}
	return tr
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

// SubscribePreview registers a client connection as a subscriber for device preview stream.
// Returns wasFirst = true if this is the first subscriber for the device.
func (h *Hub) SubscribePreview(clientID uint32, deviceID string) bool {
	h.previewSubscribersMu.Lock()
	defer h.previewSubscribersMu.Unlock()

	h.clientsMu.RLock()
	cc, ok := h.clients[clientID]
	h.clientsMu.RUnlock()
	if !ok || cc == nil {
		return false
	}

	subs, exists := h.previewSubscribers[deviceID]
	wasFirst := false
	if !exists {
		subs = make(map[uint32]*ClientConn)
		h.previewSubscribers[deviceID] = subs
		wasFirst = true
	} else if len(subs) == 0 {
		wasFirst = true
	}
	subs[clientID] = cc
	return wasFirst
}

// UnsubscribePreview removes a client from a device's preview subscribers.
// Returns wasLast = true if subscriber count reached zero.
func (h *Hub) UnsubscribePreview(clientID uint32, deviceID string) bool {
	h.previewSubscribersMu.Lock()
	defer h.previewSubscribersMu.Unlock()

	subs, exists := h.previewSubscribers[deviceID]
	if !exists {
		return false
	}
	delete(subs, clientID)
	if len(subs) == 0 {
		delete(h.previewSubscribers, deviceID)
		return true
	}
	return false
}

// UnsubscribeClientFromAllPreviews removes a client from all preview subscriptions upon disconnect.
// Returns the list of device IDs whose subscriber count dropped to zero.
func (h *Hub) UnsubscribeClientFromAllPreviews(clientID uint32) []string {
	h.previewSubscribersMu.Lock()
	defer h.previewSubscribersMu.Unlock()

	var emptyDevices []string
	for devID, subs := range h.previewSubscribers {
		if _, ok := subs[clientID]; ok {
			delete(subs, clientID)
			if len(subs) == 0 {
				delete(h.previewSubscribers, devID)
				emptyDevices = append(emptyDevices, devID)
			}
		}
	}
	return emptyDevices
}

// RelayBinaryPreviewToSubscribers routes PREV binary frames to authorized subscribers.
// Strictly verifies header format and matches boundDeviceID.
func (h *Hub) RelayBinaryPreviewToSubscribers(boundDeviceID string, data []byte) error {
	frameDeviceID, err := ParsePreviewDeviceID(data)
	if err != nil {
		return err
	}
	if boundDeviceID == "" || frameDeviceID != boundDeviceID {
		return ErrPreviewDeviceMismatch
	}

	h.previewSubscribersMu.RLock()
	subs, exists := h.previewSubscribers[boundDeviceID]
	if !exists || len(subs) == 0 {
		h.previewSubscribersMu.RUnlock()
		return nil
	}
	targets := make([]*ClientConn, 0, len(subs))
	for _, cc := range subs {
		targets = append(targets, cc)
	}
	h.previewSubscribersMu.RUnlock()

	for _, cc := range targets {
		if devices.CanAccessDevice(cc.UserRole, cc.AssignedDevices, boundDeviceID) {
			_ = cc.WriteMessage(websocket.BinaryMessage, data)
		}
	}
	return nil
}

// RelayToAgent forwards a message directly to the registered agent of a target device.
func (h *Hub) RelayToAgent(deviceID string, msg interface{}) error {
	h.agentsMu.RLock()
	ac, exists := h.agents[deviceID]
	h.agentsMu.RUnlock()
	if !exists || ac == nil {
		return fmt.Errorf("agent for device %s not connected", deviceID)
	}
	return ac.WriteJSON(msg)
}

// RelayGroupControl broadcasts or dispatches group control events to target devices.
func (h *Hub) RelayGroupControl(userRole string, assignedDevices []string, targetDevices []string, event map[string]interface{}, username string) {
	for _, devID := range targetDevices {
		if !devices.CanAccessDevice(userRole, assignedDevices, devID) {
			log.Printf("[GroupControl] User %q does not have permission for device %s, dropping event", username, devID)
			continue
		}
		h.agentsMu.RLock()
		ac, exists := h.agents[devID]
		h.agentsMu.RUnlock()
		if !exists || ac == nil {
			log.Printf("[GroupControl] Device %s agent is offline, cannot forward event (user: %q)", devID, username)
			continue
		}
		// Canonicalize event payload for agent compatibility:
		// - If type is "scroll", alias to "inject_scroll"
		// - Alias scrollH/scrollV to scroll_h/scroll_v
		normEvent := make(map[string]interface{}, len(event)+4)
		for k, v := range event {
			normEvent[k] = v
		}
		if evType, ok := normEvent["type"].(string); ok && evType == "scroll" {
			normEvent["type"] = "inject_scroll"
		}
		if sh, ok := normEvent["scrollH"]; ok && normEvent["scroll_h"] == nil {
			normEvent["scroll_h"] = sh
		}
		if sv, ok := normEvent["scrollV"]; ok && normEvent["scroll_v"] == nil {
			normEvent["scroll_v"] = sv
		}

		seq, hasSeq := normEvent["control_seq"]
		if !hasSeq {
			seq, hasSeq = normEvent["seq"]
			if !hasSeq {
				seq = "none"
			}
		}
		t2 := time.Now().UnixMilli()
		var lagT2T1 string
		if clientTs, ok := normEvent["client_ts_ms"].(float64); ok && clientTs > 0 {
			lagT2T1 = fmt.Sprintf(" lag_t2_t1=%dms", t2-int64(clientTs))
		}
		log.Printf("[CTRL] seq=%v event=%v type=RELAY relay user=%q dev=%s t2=%d%s", seq, normEvent["type"], username, devID, t2, lagT2T1)

		envelope := map[string]interface{}{
			"message_type": "group_control_event",
			"event":        normEvent,
		}
		if err := ac.WriteJSON(envelope); err != nil {
			log.Printf("[GroupControl] Error forwarding event to device %s: %v", devID, err)
		} else {
			log.Printf("[GroupControl] Forwarded group_control_event (%v) to device %s: %+v", normEvent["type"], devID, normEvent)
		}
	}
}

// BroadcastSnapshotUpdate pushes base64 snapshot updates to authorized client sessions.
func (h *Hub) BroadcastSnapshotUpdate(deviceID string, data string) {
	h.clientsMu.RLock()
	clientList := make([]*ClientConn, 0, len(h.clients))
	for _, client := range h.clients {
		clientList = append(clientList, client)
	}
	h.clientsMu.RUnlock()

	msg := SnapshotUpdateMessage{
		MessageType: "snapshot_update",
		DeviceID:    deviceID,
		Data:        data,
	}
	for _, client := range clientList {
		if devices.CanAccessDevice(client.UserRole, client.AssignedDevices, deviceID) {
			_ = client.WriteJSON(msg)
		}
	}
}
