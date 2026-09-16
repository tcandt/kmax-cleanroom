// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: In-Memory Task Queue & Snapshot Memory Store
// Evidence: TASK_TYPE_EVIDENCE.json, TASKS_OPERATION_CONTRACT.json, SNAPSHOTS_STATIC_CONTRACT.json
// Confidence: HIGH

package storage

import (
	"crypto/rand"
	"errors"
	"fmt"
	"sync"
	"time"

	"cloudphone-signaling/pkg/types"
)

var (
	ErrEmptyTargets = errors.New("Targets cannot be empty")
	ErrTaskNotFound = errors.New("Task not found")
)

// TaskManager manages asynchronous tasks in memory.
type TaskManager struct {
	mu    sync.RWMutex
	tasks map[string]*types.Task
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Constructs a new in-memory TaskManager
// Source Behavior: Initializes thread-safe in-memory task map
// Confidence: HIGH
func NewTaskManager() *TaskManager {
	return &TaskManager{
		tasks: make(map[string]*types.Task),
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.koVbnsD4T0d
// VA: 0x75afa0
// Evidence: TASKS_OPERATION_CONTRACT.json, TASK_ID_CONTRACT.json
// Purpose: Creates a new batch task, validates targets, and assigns immediate offline failure
// Confidence: HIGH
func (tm *TaskManager) CreateTask(req types.TaskCreateRequest) (*types.Task, error) {
	if len(req.Targets) == 0 {
		return nil, ErrEmptyTargets
	}

	// Generate task ID: task_YYYYMMDDhhmmss_<random_hex16> (layout 0x825bda, format 0x82229b)
	now := time.Now()
	randBytes := make([]byte, 8)
	if _, err := rand.Read(randBytes); err != nil {
		return nil, err
	}
	taskID := fmt.Sprintf("task_%s_%x", now.Format("20060102150405"), randBytes)

	nowFormatted := now.Format("2006-01-02T15:04:05-07:00")
	devMap := make(map[string]*types.DeviceTaskStatus)
	for _, target := range req.Targets {
		devMap[target] = &types.DeviceTaskStatus{
			DeviceID:  target,
			Status:    "failed",
			Progress:  0,
			Result:    "Device offline",
			UpdatedAt: nowFormatted,
		}
	}

	task := &types.Task{
		TaskID:    taskID,
		Type:      req.Type,
		Payload:   req.Payload,
		DestPath:  req.DestPath,
		CreatedAt: nowFormatted,
		Devices:   devMap,
	}

	tm.mu.Lock()
	tm.tasks[taskID] = task
	tm.mu.Unlock()

	return task, nil
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Adapter method delegating task creation to CreateTask
// Source Behavior: Calls CreateTask and returns task ID string
// Confidence: HIGH
func (tm *TaskManager) CreateBatchTask(req *types.TaskCreateRequest) (string, error) {
	if req == nil {
		return "", ErrEmptyTargets
	}
	t, err := tm.CreateTask(*req)
	if err != nil {
		return "", err
	}
	return t.TaskID, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.bhMId7t5J
// VA: 0x763ec0
// Evidence: TASK_DETAILS_CONTRACT.json
// Purpose: Looks up an in-memory task by task ID
// Confidence: HIGH
func (tm *TaskManager) GetTask(taskID string) (*types.Task, error) {
	tm.mu.RLock()
	defer tm.mu.RUnlock()

	t, exists := tm.tasks[taskID]
	if !exists {
		return nil, ErrTaskNotFound
	}
	return t, nil
}

// SnapshotManager manages screen capture snapshots in memory.
type SnapshotManager struct {
	mu        sync.RWMutex
	snapshots map[string][]byte
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Constructs a new in-memory SnapshotManager
// Source Behavior: Initializes thread-safe in-memory snapshot cache
// Confidence: HIGH
func NewSnapshotManager() *SnapshotManager {
	return &SnapshotManager{
		snapshots: make(map[string][]byte),
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.swqKgLrjAZT9
// VA: 0x759048
// Evidence: UPLOAD_OPERATION_CONTRACT.json, SNAPSHOTS_STATIC_CONTRACT.json
// Purpose: Stores raw snapshot image bytes in memory keyed by device ID
// Confidence: HIGH
func (sm *SnapshotManager) SaveSnapshot(deviceID string, data []byte) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	sm.snapshots[deviceID] = data
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.main.func5
// VA: 0x76da00
// Evidence: SNAPSHOTS_STATIC_CONTRACT.json
// Purpose: Retrieves in-memory snapshot image bytes by device ID
// Confidence: HIGH
func (sm *SnapshotManager) GetSnapshot(deviceID string) ([]byte, bool) {
	sm.mu.RLock()
	defer sm.mu.RUnlock()

	data, exists := sm.snapshots[deviceID]
	return data, exists
}
