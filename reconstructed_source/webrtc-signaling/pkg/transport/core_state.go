// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BEHAVIOR
// Mapping Scope: CORESERVICE_LIFECYCLE_STATE_MACHINE
// Task: Phase R5.4A - Atomic Mode Handoff & Consumer Session Ref Tracking
// Note: Behavioral reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package transport

import (
	"fmt"
	"log"
	"sync"
	"time"
)

// CoreState represents the lifecycle phase of CoreService / scrcpy-server on the device.
type CoreState string

const (
	CoreStateStopped  CoreState = "STOPPED"
	CoreStateStarting CoreState = "STARTING"
	CoreStateReady    CoreState = "READY"
	CoreStateStopping CoreState = "STOPPING"
)

// ConsumerRef tracks a single client's active session consumption on a device.
type ConsumerRef struct {
	ClientID   uint32
	DeviceID   string
	Generation uint64
	Mode       string // "webrtc" | "websocket" | "control"
}

// DeviceConsumers tracks active consumers by mode using client ID sets.
type DeviceConsumers struct {
	WebRTC  map[uint32]ConsumerRef
	WS      map[uint32]ConsumerRef
	Control map[uint32]ConsumerRef
}

// HandoffInfo tracks in-flight mode transition state.
type HandoffInfo struct {
	ID          string
	DeviceID    string
	FromMode    string
	ToMode      string
	Generation  uint64
	AttemptID   uint32
	OldClientID uint32
	NewClientID uint32
	State       string // "BEGIN", "HANDOFF_IN_PROGRESS", "NEW_STREAM_STARTING", "NEW_STREAM_READY", "COMPLETE", "ROLLBACK"
	StartTime   time.Time
}

// DeviceCoreTracker tracks reference ownership and manages transitions for a device.
type DeviceCoreTracker struct {
	mu             sync.Mutex
	deviceID       string
	state          CoreState
	consumers      DeviceConsumers
	stopDebounce   *time.Timer
	webrtcDebounce *time.Timer
	activeHandoff  *HandoffInfo
}

// NewDeviceCoreTracker creates a tracker for a specific device.
func NewDeviceCoreTracker(deviceID string) *DeviceCoreTracker {
	return &DeviceCoreTracker{
		deviceID: deviceID,
		state:    CoreStateStopped,
		consumers: DeviceConsumers{
			WebRTC:  make(map[uint32]ConsumerRef),
			WS:      make(map[uint32]ConsumerRef),
			Control: make(map[uint32]ConsumerRef),
		},
	}
}

// State returns the current CoreState under mutex lock.
func (t *DeviceCoreTracker) State() CoreState {
	t.mu.Lock()
	defer t.mu.Unlock()
	return t.state
}

// ScheduleWebRTCDisconnect registers a debounced client_disconnected dispatch.
func (t *DeviceCoreTracker) ScheduleWebRTCDisconnect(clientID uint32, debounce time.Duration, onExpire func()) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.webrtcDebounce != nil {
		t.webrtcDebounce.Stop()
	}

	t.webrtcDebounce = time.AfterFunc(debounce, func() {
		t.mu.Lock()
		t.webrtcDebounce = nil
		t.mu.Unlock()
		if onExpire != nil {
			onExpire()
		}
	})
	log.Printf("[CORE] dev=%s scheduled debounced client_disconnected for client %d (%v)", t.deviceID, clientID, debounce)
}

// CancelWebRTCDisconnect cancels any pending debounced client_disconnected timer.
func (t *DeviceCoreTracker) CancelWebRTCDisconnect() {
	t.mu.Lock()
	defer t.mu.Unlock()
	if t.webrtcDebounce != nil {
		t.webrtcDebounce.Stop()
		t.webrtcDebounce = nil
		log.Printf("[CORE] dev=%s cancelled pending webrtc disconnect debounce", t.deviceID)
	}
}

// logState logs the state according to Phase R3/R5.4A format specification.
func (t *DeviceCoreTracker) logStateLocked(reason string) {
	touchUDS := "IDLE"
	controlUDS := "IDLE"
	videoUDS := "IDLE"

	webrtcRefs := len(t.consumers.WebRTC)
	wsPreviewRefs := len(t.consumers.WS)
	controlRefs := len(t.consumers.Control)

	if t.state == CoreStateReady || t.state == CoreStateStarting {
		touchUDS = "READY"
		controlUDS = "READY"
		if wsPreviewRefs > 0 || webrtcRefs > 0 {
			videoUDS = "STREAMING"
		} else {
			videoUDS = "ACTIVE"
		}
	}

	log.Printf("[CORE] state=%s dev=%s reason=%s webrtcRefs=%d wsPreviewRefs=%d controlRefs=%d touchUDS=%s controlUDS=%s videoUDS=%s",
		t.state, t.deviceID, reason, webrtcRefs, wsPreviewRefs, controlRefs, touchUDS, controlUDS, videoUDS)
}

// OnStartPreviewSubscriber marks a preview subscriber addition with session generation.
// Returns shouldSendStart = true if the agent needs to receive a start_preview command.
func (t *DeviceCoreTracker) OnStartPreviewSubscriber(clientID uint32, generation uint64) bool {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.stopDebounce != nil {
		t.stopDebounce.Stop()
		t.stopDebounce = nil
		log.Printf("[CORE] dev=%s cancelled pending stopDebounce timer due to incoming preview client %d", t.deviceID, clientID)
	}
	if t.webrtcDebounce != nil {
		t.webrtcDebounce.Stop()
		t.webrtcDebounce = nil
		log.Printf("[CORE] dev=%s cancelled pending webrtcDebounce due to incoming preview client %d", t.deviceID, clientID)
	}

	wasEmpty := len(t.consumers.WS) == 0
	t.consumers.WS[clientID] = ConsumerRef{
		ClientID:   clientID,
		DeviceID:   t.deviceID,
		Generation: generation,
		Mode:       "websocket",
	}

	shouldSendStart := false
	if wasEmpty && t.state != CoreStateReady && t.state != CoreStateStarting {
		t.state = CoreStateStarting
		shouldSendStart = true
	}

	t.logStateLocked(fmt.Sprintf("add_preview_client_%d_gen_%d", clientID, generation))
	return shouldSendStart
}

// OnStopPreviewSubscriber decrements preview subscriber count.
// Uses a debounce window before actually stopping CoreService to prevent
// mode-switch and navigation teardown storms.
// onExpire is called if debounce expires and zero consumers remain and no handoff is active.
func (t *DeviceCoreTracker) OnStopPreviewSubscriber(clientID uint32, debounce time.Duration, onExpire func()) {
	t.mu.Lock()
	defer t.mu.Unlock()

	delete(t.consumers.WS, clientID)
	t.logStateLocked(fmt.Sprintf("remove_preview_client_%d", clientID))

	// Do NOT stop CoreService if active WebRTC consumers, active handoff, or remaining WS consumers exist!
	if len(t.consumers.WS) == 0 && len(t.consumers.WebRTC) == 0 && (t.activeHandoff == nil || t.activeHandoff.State == "COMPLETE" || t.activeHandoff.State == "ROLLBACK") {
		if t.stopDebounce != nil {
			t.stopDebounce.Stop()
		}

		t.stopDebounce = time.AfterFunc(debounce, func() {
			t.mu.Lock()
			// Re-verify after debounce delay with leak-proof check
			if len(t.consumers.WS) == 0 && len(t.consumers.WebRTC) == 0 && (t.activeHandoff == nil || t.activeHandoff.State == "COMPLETE" || t.activeHandoff.State == "ROLLBACK") {
				t.state = CoreStateStopping
				t.logStateLocked("preview_debounce_expired_stopping")
				t.state = CoreStateStopped
				t.logStateLocked("preview_stopped")
				t.mu.Unlock()
				if onExpire != nil {
					onExpire()
				}
			} else {
				t.logStateLocked("preview_debounce_cancelled_active_consumers_or_handoff_reacquired")
				t.mu.Unlock()
			}
		})
	}
}

// OnAddWebRTCClient registers a WebRTC client consumer reference.
func (t *DeviceCoreTracker) OnAddWebRTCClient(clientID uint32, generation uint64) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.stopDebounce != nil {
		t.stopDebounce.Stop()
		t.stopDebounce = nil
	}
	if t.webrtcDebounce != nil {
		t.webrtcDebounce.Stop()
		t.webrtcDebounce = nil
		log.Printf("[CORE] dev=%s cancelled pending webrtcDebounce due to incoming webrtc client %d", t.deviceID, clientID)
	}

	t.consumers.WebRTC[clientID] = ConsumerRef{
		ClientID:   clientID,
		DeviceID:   t.deviceID,
		Generation: generation,
		Mode:       "webrtc",
	}

	if t.state != CoreStateReady {
		t.state = CoreStateStarting
	}
	t.logStateLocked(fmt.Sprintf("add_webrtc_client_%d_gen_%d", clientID, generation))
}

// OnRemoveWebRTCClient removes a WebRTC client consumer reference.
func (t *DeviceCoreTracker) OnRemoveWebRTCClient(clientID uint32) {
	t.mu.Lock()
	defer t.mu.Unlock()

	delete(t.consumers.WebRTC, clientID)
	t.logStateLocked(fmt.Sprintf("remove_webrtc_client_%d", clientID))
}

// HasWebRTCClient checks if a specific clientID is an active WebRTC consumer.
func (t *DeviceCoreTracker) HasWebRTCClient(clientID uint32) bool {
	t.mu.Lock()
	defer t.mu.Unlock()
	_, exists := t.consumers.WebRTC[clientID]
	return exists
}

// OnAddControlClient registers a control client reference.
func (t *DeviceCoreTracker) OnAddControlClient(clientID uint32, generation uint64) {
	t.mu.Lock()
	defer t.mu.Unlock()

	t.consumers.Control[clientID] = ConsumerRef{
		ClientID:   clientID,
		DeviceID:   t.deviceID,
		Generation: generation,
		Mode:       "control",
	}
	t.logStateLocked(fmt.Sprintf("add_control_client_%d_gen_%d", clientID, generation))
}

// OnRemoveControlClient removes a control client reference.
func (t *DeviceCoreTracker) OnRemoveControlClient(clientID uint32) {
	t.mu.Lock()
	defer t.mu.Unlock()

	delete(t.consumers.Control, clientID)
	t.logStateLocked(fmt.Sprintf("remove_control_client_%d", clientID))
}

// BeginHandoff initiates an atomic bidirectional mode transition.
func (t *DeviceCoreTracker) BeginHandoff(fromMode, toMode string, generation uint64, attemptID uint32, oldClientID, newClientID uint32) *HandoffInfo {
	t.mu.Lock()
	defer t.mu.Unlock()

	handoffID := fmt.Sprintf("h-%s-%d-%d", t.deviceID, generation, time.Now().UnixMilli())
	info := &HandoffInfo{
		ID:          handoffID,
		DeviceID:    t.deviceID,
		FromMode:    fromMode,
		ToMode:      toMode,
		Generation:  generation,
		AttemptID:   attemptID,
		OldClientID: oldClientID,
		NewClientID: newClientID,
		State:       "HANDOFF_IN_PROGRESS",
		StartTime:   time.Now(),
	}
	t.activeHandoff = info
	log.Printf("[HANDOFF] id=%s device=%s from=%s to=%s gen=%d attempt=%d oldClient=%d newClient=%d state=BEGIN",
		info.ID, t.deviceID, fromMode, toMode, generation, attemptID, oldClientID, newClientID)
	log.Printf("[HANDOFF] id=%s device=%s state=HANDOFF_IN_PROGRESS", info.ID, t.deviceID)
	return info
}

// UpdateHandoffState transitions the handoff state machine.
func (t *DeviceCoreTracker) UpdateHandoffState(newState string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.activeHandoff == nil {
		return
	}
	t.activeHandoff.State = newState
	log.Printf("[HANDOFF] id=%s device=%s state=%s", t.activeHandoff.ID, t.deviceID, newState)
	if newState == "COMPLETE" || newState == "ROLLBACK" {
		t.activeHandoff = nil
	}
}

// HasActiveHandoff checks if a handoff is currently in progress.
func (t *DeviceCoreTracker) HasActiveHandoff() bool {
	t.mu.Lock()
	defer t.mu.Unlock()
	return t.activeHandoff != nil && t.activeHandoff.State != "COMPLETE" && t.activeHandoff.State != "ROLLBACK"
}

// HasNewerLiveConsumer checks if any active consumer has a generation strictly greater than the specified generation.
func (t *DeviceCoreTracker) HasNewerLiveConsumer(generation uint64) bool {
	t.mu.Lock()
	defer t.mu.Unlock()

	for _, ref := range t.consumers.WebRTC {
		if ref.Generation > generation {
			return true
		}
	}
	for _, ref := range t.consumers.WS {
		if ref.Generation > generation {
			return true
		}
	}
	return false
}

// WebRTCCount returns the count of registered WebRTC consumers.
func (t *DeviceCoreTracker) WebRTCCount() int {
	t.mu.Lock()
	defer t.mu.Unlock()
	return len(t.consumers.WebRTC)
}

// WSCount returns the count of registered WS preview consumers.
func (t *DeviceCoreTracker) WSCount() int {
	t.mu.Lock()
	defer t.mu.Unlock()
	return len(t.consumers.WS)
}

// MarkReady marks the CoreService as fully operational.
func (t *DeviceCoreTracker) MarkReady(reason string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	t.state = CoreStateReady
	t.logStateLocked(reason)
}

// HasActiveConsumers checks if any consumer is holding a reference.
func (t *DeviceCoreTracker) HasActiveConsumers() bool {
	t.mu.Lock()
	defer t.mu.Unlock()

	return len(t.consumers.WebRTC) > 0 || len(t.consumers.WS) > 0 || len(t.consumers.Control) > 0
}
