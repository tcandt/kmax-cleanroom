// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Task Data Models & Files Wire Schema
// Evidence: TASK_TYPE_EVIDENCE.json, FILES_TYPE_EVIDENCE.json
// Confidence: HIGH

package types

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_WIRE_MODEL
// Mapping Scope: WIRE_SCHEMA
// Evidence: FILES_TYPE_EVIDENCE.json, FILES_LIST_CONTRACT.json
// Purpose: Represents an individual file entry in /api/files JSON array
// Confidence: HIGH
type FileItem struct {
	Name      string `json:"name"`
	Size      int64  `json:"size"`
	UpdatedAt string `json:"updated_at"`
	URL       string `json:"url"`
}

// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Mapping Scope: DIRECT_TYPE_RECOVERY
// Descriptor VA: 0x7ea980
// Evidence: TASK_TYPE_EVIDENCE.json
// Size: 72 bytes
// Fields: type (0), targets (16), payload (40), dest_path (56)
// Confidence: HIGH
type TaskCreateRequest struct {
	Type     string   `json:"type"`
	Targets  []string `json:"targets"`
	Payload  string   `json:"payload"`
	DestPath string   `json:"dest_path"`
}

// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Mapping Scope: DIRECT_TYPE_RECOVERY
// Descriptor VA: 0x7fb3c0
// Binary Symbol: main.Jh0XQJ
// Evidence: TASK_TYPE_EVIDENCE.json, TASK_DETAILS_CONTRACT.json
// Size: 88 bytes
// Fields: task_id (0), type (16), payload (32), dest_path (48), created_at (64), devices (80)
// Confidence: HIGH
type Task struct {
	TaskID    string                       `json:"task_id"`
	Type      string                       `json:"type"`
	Payload   string                       `json:"payload"`
	DestPath  string                       `json:"dest_path,omitempty"`
	CreatedAt string                       `json:"created_at"`
	Devices   map[string]*DeviceTaskStatus `json:"devices"`
}

// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Mapping Scope: DIRECT_TYPE_RECOVERY
// Descriptor VA: 0x7f4be0
// Binary Symbol: main.ZFJczDtV4TR
// Evidence: TASK_TYPE_EVIDENCE.json, TASKS_OPERATION_CONTRACT.json
// Size: 72 bytes
// Fields: device_id (0), status (16), progress (32), result (40), updated_at (56)
// Confidence: HIGH
type DeviceTaskStatus struct {
	DeviceID  string `json:"device_id"`
	Status    string `json:"status"`
	Progress  int    `json:"progress"`
	Result    string `json:"result"`
	UpdatedAt string `json:"updated_at"`
}
