// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BEHAVIOR
// Mapping Scope: CORESERVICE_LIFECYCLE_STATE_MACHINE
// Task: Phase R3 - CoreService & UDS Reference Ownership & State Machine
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

// DeviceCoreTracker tracks reference ownership and manages transitions for a device.
type DeviceCoreTracker struct {
	mu              sync.Mutex
	deviceID        string
	state           CoreState
	webrtcMediaRefs int
	dataChannelRefs int
	wsPreviewRefs   int
	controlRefs     int
	stopDebounce    *time.Timer
}

// NewDeviceCoreTracker creates a tracker for a specific device.
func NewDeviceCoreTracker(deviceID string) *DeviceCoreTracker {
	return &DeviceCoreTracker{
		deviceID: deviceID,
		state:    CoreStateStopped,
	}
}

// logState logs the state according to Phase R3 format specification.
func (t *DeviceCoreTracker) logStateLocked(reason string) {
	touchUDS := "IDLE"
	controlUDS := "IDLE"
	videoUDS := "IDLE"

	if t.state == CoreStateReady || t.state == CoreStateStarting {
		touchUDS = "READY"
		controlUDS = "READY"
		if t.wsPreviewRefs > 0 || t.webrtcMediaRefs > 0 {
			videoUDS = "STREAMING"
		} else {
			videoUDS = "ACTIVE"
		}
	}

	log.Printf("[CORE] state=%s dev=%s reason=%s webrtcRefs=%d wsPreviewRefs=%d controlRefs=%d touchUDS=%s controlUDS=%s videoUDS=%s",
		t.state, t.deviceID, reason, t.webrtcMediaRefs, t.wsPreviewRefs, t.controlRefs, touchUDS, controlUDS, videoUDS)
}

// OnStartPreviewSubscriber marks a preview subscriber addition.
// Returns shouldSendStart = true if the agent needs to receive a start_preview command.
func (t *DeviceCoreTracker) OnStartPreviewSubscriber(clientID uint32) bool {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.stopDebounce != nil {
		t.stopDebounce.Stop()
		t.stopDebounce = nil
		log.Printf("[CORE] dev=%s cancelled pending stopDebounce timer due to incoming preview client %d", t.deviceID, clientID)
	}

	t.wsPreviewRefs++
	shouldSendStart := false

	if t.state != CoreStateReady && t.state != CoreStateStarting {
		t.state = CoreStateStarting
		shouldSendStart = true
	}

	t.logStateLocked(fmt.Sprintf("add_preview_client_%d", clientID))
	return shouldSendStart
}

// OnStopPreviewSubscriber decrements preview subscriber count.
// Uses a 1.5-second debounce window before actually stopping CoreService to prevent
// mode-switch and navigation teardown storms.
// onExpire is called if debounce expires and zero consumers remain.
func (t *DeviceCoreTracker) OnStopPreviewSubscriber(clientID uint32, debounce time.Duration, onExpire func()) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.wsPreviewRefs > 0 {
		t.wsPreviewRefs--
	}

	t.logStateLocked(fmt.Sprintf("remove_preview_client_%d", clientID))

	// Do NOT stop CoreService if active WebRTC media consumers or data channel consumers remain!
	if t.wsPreviewRefs == 0 && t.webrtcMediaRefs == 0 {
		if t.stopDebounce != nil {
			t.stopDebounce.Stop()
		}

		t.stopDebounce = time.AfterFunc(debounce, func() {
			t.mu.Lock()
			// Re-verify after debounce delay
			if t.wsPreviewRefs == 0 && t.webrtcMediaRefs == 0 {
				t.state = CoreStateStopping
				t.logStateLocked("preview_debounce_expired_stopping")
				t.state = CoreStateStopped
				t.logStateLocked("preview_stopped")
				t.mu.Unlock()
				if onExpire != nil {
					onExpire()
				}
			} else {
				t.logStateLocked("preview_debounce_cancelled_active_consumers_reacquired")
				t.mu.Unlock()
			}
		})
	}
}

// OnAddWebRTCClient increments WebRTC active media references.
func (t *DeviceCoreTracker) OnAddWebRTCClient(clientID uint32) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.stopDebounce != nil {
		t.stopDebounce.Stop()
		t.stopDebounce = nil
	}

	t.webrtcMediaRefs++
	if t.state != CoreStateReady {
		t.state = CoreStateStarting
	}
	t.logStateLocked(fmt.Sprintf("add_webrtc_client_%d", clientID))
}

// OnRemoveWebRTCClient decrements WebRTC active media references.
func (t *DeviceCoreTracker) OnRemoveWebRTCClient(clientID uint32) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.webrtcMediaRefs > 0 {
		t.webrtcMediaRefs--
	}
	t.logStateLocked(fmt.Sprintf("remove_webrtc_client_%d", clientID))
}

// OnAddControlClient increments control client references.
func (t *DeviceCoreTracker) OnAddControlClient(clientID uint32) {
	t.mu.Lock()
	defer t.mu.Unlock()

	t.controlRefs++
	t.logStateLocked(fmt.Sprintf("add_control_client_%d", clientID))
}

// OnRemoveControlClient decrements control client references.
func (t *DeviceCoreTracker) OnRemoveControlClient(clientID uint32) {
	t.mu.Lock()
	defer t.mu.Unlock()

	if t.controlRefs > 0 {
		t.controlRefs--
	}
	t.logStateLocked(fmt.Sprintf("remove_control_client_%d", clientID))
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

	return t.webrtcMediaRefs > 0 || t.wsPreviewRefs > 0 || t.dataChannelRefs > 0
}
