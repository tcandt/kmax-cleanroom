// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Files, Tasks, Downloads, and Snapshots HTTP Handlers
// Evidence: FILES_TASKS_ROUTE_FAMILY.json, FILES_TASKS_METHOD_MATRIX.json, FILES_TASKS_AUTH_MATRIX.json
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"cloudphone-signaling/pkg/devices"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.swqKgLrjAZT9
// VA: 0x758c80
// Evidence: UPLOAD_OPERATION_CONTRACT.json, FILE_PATH_SECURITY_CONTRACT.json
// Purpose: Handles file upload and snapshot ingest
// Confidence: HIGH
func (s *Server) HandleUpload(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	q := r.URL.Query()
	typ := q.Get("type")
	devID := q.Get("device_id")

	// Snapshot ingest variant: POST /upload?type=snapshot&device_id=...
	if typ == "snapshot" {
		if devID == "" {
			http.Error(w, "Missing device_id", http.StatusBadRequest)
			return
		}
		if devID == "." || devID == "/" || devID == "\\" {
			http.Error(w, "Invalid device_id", http.StatusBadRequest)
			return
		}

		data, err := io.ReadAll(r.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		s.snapshotMgr.SaveSnapshot(devID, data)
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "Uploaded to memory for %s.jpg", devID)
		return
	}

	// Standard file upload variant: POST /upload?name=...
	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden: Only administrators can upload files", http.StatusForbidden)
			return
		}
	}

	name := q.Get("name")
	if name == "" {
		http.Error(w, "Missing file name", http.StatusBadRequest)
		return
	}

	clean := filepath.Clean(name)
	if clean == "." {
		http.Error(w, "Invalid file name", http.StatusBadRequest)
		return
	}
	base := filepath.Base(clean)
	if clean == ".." || base == ".." || base == "." {
		http.Error(w, "Invalid file path (path traversal detected)", http.StatusBadRequest)
		return
	}

	savedName, err := s.fileMgr.SaveUploadedFile(name, r.Body)
	if err != nil {
		if errors.Is(err, storage.ErrPathTraversal) {
			http.Error(w, "Invalid file path (path traversal detected)", http.StatusBadRequest)
			return
		}
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Uploaded to %s", savedName)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.qa3RvDW
// VA: 0x75a2c0
// Evidence: FILES_LIST_CONTRACT.json, FILES_TYPE_EVIDENCE.json
// Purpose: Handles file listing and deletion in the downloads directory
// Confidence: HIGH
func (s *Server) HandleFiles(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "GET, DELETE, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if !s.noAuth {
		_, err := s.Authenticate(r)
		if err != nil {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
	}

	switch r.Method {
	case http.MethodGet:
		items, err := s.fileMgr.ListFiles()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_ = json.NewEncoder(w).Encode(items)

	case http.MethodDelete:
		name := r.URL.Query().Get("name")
		if name == "" {
			http.Error(w, "Missing name parameter", http.StatusBadRequest)
			return
		}
		if err := s.fileMgr.DeleteFile(name); err != nil {
			if errors.Is(err, os.ErrNotExist) || errors.Is(err, storage.ErrMissingName) {
				http.Error(w, "File not found", http.StatusNotFound)
				return
			}
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"success"}`))

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.koVbnsD4T0d
// VA: 0x75afa0
// Evidence: TASKS_OPERATION_CONTRACT.json, TASK_TYPE_EVIDENCE.json
// Purpose: Creates a new batch task for target devices
// Confidence: HIGH
func (s *Server) HandleTasks(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		if user.Role != "admin" {
			http.Error(w, "Forbidden: admin only", http.StatusForbidden)
			return
		}
	}

	var req types.TaskCreateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if len(req.Targets) == 0 {
		http.Error(w, "Targets cannot be empty", http.StatusBadRequest)
		return
	}

	task, err := s.taskMgr.CreateTask(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"status":  "success",
		"task_id": task.TaskID,
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.p5P6cWj
// VA: 0x75ba00
// Evidence: TASK_DETAILS_CONTRACT.json, TASK_TYPE_EVIDENCE.json
// Purpose: Retrieves details of a specific batch task
// Confidence: HIGH
func (s *Server) HandleTaskDetails(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	if !s.noAuth {
		_, err := s.Authenticate(r)
		if err != nil {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
	}

	taskID := r.URL.Query().Get("task_id")
	if taskID == "" {
		http.Error(w, "Missing task_id parameter", http.StatusBadRequest)
		return
	}

	task, err := s.taskMgr.GetTask(taskID)
	if err != nil {
		http.Error(w, "Task not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(task)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.main.func5
// VA: 0x76da00
// Evidence: SNAPSHOTS_STATIC_CONTRACT.json
// Purpose: Serves device screen capture snapshot images from memory
// Confidence: HIGH
func (s *Server) HandleSnapshots(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	var role = "admin"
	var assigned []string = nil
	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		role = user.Role
		assigned = user.AssignedDevices
	}

	path := strings.TrimPrefix(r.URL.Path, "/snapshots/")
	if path == "" || strings.Contains(path, "/") {
		http.Error(w, "404 page not found", http.StatusNotFound)
		return
	}

	var devID string
	if strings.HasSuffix(path, ".jpg") {
		devID = strings.TrimSuffix(path, ".jpg")
	} else if !strings.Contains(path, ".") {
		devID = path
	} else {
		http.Error(w, "404 page not found", http.StatusNotFound)
		return
	}

	if !devices.CanAccessDevice(role, assigned, devID) {
		http.Error(w, "Forbidden", http.StatusForbidden)
		return
	}

	data, exists := s.snapshotMgr.GetSnapshot(devID)
	if !exists {
		http.Error(w, "404 page not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "image/jpeg")
	w.Header().Set("Cache-Control", "no-cache, no-store, must-revalidate")
	w.Header().Set("Content-Length", strconv.Itoa(len(data)))

	if r.Method == http.MethodHead {
		return
	}

	_, _ = w.Write(data)
}
