// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Scope: Unit tests for FileManager, TaskManager, SnapshotManager
// Confidence: HIGH

package storage

import (
	"bytes"
	"os"
	"path/filepath"
	"regexp"
	"testing"

	"cloudphone-signaling/pkg/types"
)

func TestFileManagerLifecycle(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "fm_test_*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	downloadsDir := filepath.Join(tempDir, "downloads")
	fm := NewFileManager(downloadsDir)

	if err := fm.EnsureDirectories(); err != nil {
		t.Fatalf("EnsureDirectories failed: %v", err)
	}

	// 1. Initially empty
	items, err := fm.ListFiles()
	if err != nil {
		t.Fatalf("ListFiles failed: %v", err)
	}
	if len(items) != 0 {
		t.Fatalf("Expected 0 items, got %d", len(items))
	}

	// 2. Upload file
	content := []byte("hello world binary payload")
	savedName, err := fm.SaveUploadedFile("test_file.bin", bytes.NewReader(content))
	if err != nil {
		t.Fatalf("SaveUploadedFile failed: %v", err)
	}
	if savedName != "test_file.bin" {
		t.Fatalf("Expected saved name test_file.bin, got %s", savedName)
	}

	// 3. List contains file
	items, err = fm.ListFiles()
	if err != nil {
		t.Fatalf("ListFiles failed: %v", err)
	}
	if len(items) != 1 || items[0].Name != "test_file.bin" || items[0].Size != int64(len(content)) {
		t.Fatalf("Unexpected items after upload: %+v", items)
	}
	if items[0].URL != "/downloads/test_file.bin" {
		t.Fatalf("Unexpected item URL: %s", items[0].URL)
	}

	// 4. Path traversal rejections on dots
	if _, err := fm.SaveUploadedFile(".", bytes.NewReader([]byte("x"))); err != ErrPathTraversal {
		t.Fatalf("Expected ErrPathTraversal on '.', got %v", err)
	}
	if _, err := fm.SaveUploadedFile("..", bytes.NewReader([]byte("x"))); err != ErrPathTraversal {
		t.Fatalf("Expected ErrPathTraversal on '..', got %v", err)
	}

	// Sanitization of relative segments: saves to base filename
	sanitizedName, err := fm.SaveUploadedFile("../sanitized.txt", bytes.NewReader([]byte("x")))
	if err != nil || sanitizedName != "sanitized.txt" {
		t.Fatalf("Expected sanitized filename 'sanitized.txt', got %s, err=%v", sanitizedName, err)
	}
	if err := fm.DeleteFile("sanitized.txt"); err != nil {
		t.Fatalf("Failed to delete sanitized.txt: %v", err)
	}

	// 5. Delete initial file
	if err := fm.DeleteFile("test_file.bin"); err != nil {
		t.Fatalf("DeleteFile failed: %v", err)
	}
	items, err = fm.ListFiles()
	if err != nil {
		t.Fatalf("ListFiles failed: %v", err)
	}
	if len(items) != 0 {
		t.Fatalf("Expected 0 items after delete, got %d", len(items))
	}
}

func TestTaskManagerLifecycle(t *testing.T) {
	tm := NewTaskManager()

	// 1. Empty targets rejected
	_, err := tm.CreateTask(types.TaskCreateRequest{
		Type:    "install",
		Targets: []string{},
	})
	if err != ErrEmptyTargets {
		t.Fatalf("Expected ErrEmptyTargets, got %v", err)
	}

	// 2. Create batch task with offline targets
	req := types.TaskCreateRequest{
		Type:     "shell",
		Targets:  []string{"dev-001", "dev-002"},
		Payload:  "getprop",
		DestPath: "/sdcard",
	}
	task, err := tm.CreateTask(req)
	if err != nil {
		t.Fatalf("CreateTask failed: %v", err)
	}

	// Validate Task ID format: task_YYYYMMDDhhmmss_<hex16>
	re := regexp.MustCompile(`^task_\d{14}_[0-9a-f]{16}$`)
	if !re.MatchString(task.TaskID) {
		t.Fatalf("TaskID does not match expected format: %s", task.TaskID)
	}

	if len(task.Devices) != 2 {
		t.Fatalf("Expected 2 devices in task status map, got %d", len(task.Devices))
	}

	for _, devID := range req.Targets {
		st, exists := task.Devices[devID]
		if !exists {
			t.Fatalf("Device %s not found in task devices", devID)
		}
		if st.Status != "failed" || st.Result != "Device offline" || st.Progress != 0 {
			t.Fatalf("Unexpected device status: %+v", st)
		}
	}

	// 3. Lookup task
	found, err := tm.GetTask(task.TaskID)
	if err != nil {
		t.Fatalf("GetTask failed: %v", err)
	}
	if found.TaskID != task.TaskID || found.Type != "shell" {
		t.Fatalf("Mismatched task details: %+v", found)
	}

	// 4. Nonexistent task
	_, err = tm.GetTask("task_nonexistent")
	if err != ErrTaskNotFound {
		t.Fatalf("Expected ErrTaskNotFound, got %v", err)
	}
}

func TestSnapshotManagerLifecycle(t *testing.T) {
	sm := NewSnapshotManager()

	// 1. Lookup nonexistent
	if _, exists := sm.GetSnapshot("dev-1"); exists {
		t.Fatalf("Expected nonexistent snapshot to return false")
	}

	// 2. Save snapshot
	data := []byte{0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46}
	sm.SaveSnapshot("dev-1", data)

	retrieved, exists := sm.GetSnapshot("dev-1")
	if !exists {
		t.Fatalf("Expected saved snapshot to exist")
	}
	if !bytes.Equal(retrieved, data) {
		t.Fatalf("Retrieved data did not match saved data")
	}

	// 3. Overwrite
	newData := []byte{0xFF, 0xD8, 0xFF, 0xE0, 0x99}
	sm.SaveSnapshot("dev-1", newData)
	retrieved, _ = sm.GetSnapshot("dev-1")
	if !bytes.Equal(retrieved, newData) {
		t.Fatalf("Overwritten data did not match")
	}
}
