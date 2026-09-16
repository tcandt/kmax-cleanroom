// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Scope: HTTP API tests for files, tasks, downloads, and snapshots
// Confidence: HIGH

package httpapi

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

func setupFilesTasksServer(t *testing.T) (*Server, string, string, string, func()) {
	tmpDir, err := os.MkdirTemp("", "httpapi_ft_test_*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}

	usersFilePath := filepath.Join(tmpDir, "users.json")
	usersStore := storage.NewUsersStore(usersFilePath)
	_ = usersStore.LoadOrCreate()
	salt := "test_salt_12345"

	_ = usersStore.SetUser(types.User{
		Username:        "admin",
		Password:        storage.HashPassword("admin123", salt),
		Salt:            salt,
		Role:            "admin",
		AssignedDevices: []string{"*"},
	})
	_ = usersStore.SetUser(types.User{
		Username:        "norm_assigned",
		Password:        storage.HashPassword("pass123", salt),
		Salt:            salt,
		Role:            "user",
		AssignedDevices: []string{"dev-001"},
	})
	_ = usersStore.SetUser(types.User{
		Username:        "norm_unassigned",
		Password:        storage.HashPassword("pass123", salt),
		Salt:            salt,
		Role:            "user",
		AssignedDevices: []string{},
	})

	sm := session.NewSessionManager(session.RealClock{})
	authenticator := auth.NewAuthenticator(usersStore, sm, false)
	server := NewServer(authenticator, false)

	// Configure downloads dir in tmpDir
	downloadsDir := filepath.Join(tmpDir, "downloads")
	fileMgr := storage.NewFileManager(downloadsDir)
	_ = fileMgr.EnsureDirectories()
	server.SetFileManager(fileMgr)

	adminAuth, err := authenticator.AuthenticateCredentials("admin", "admin123")
	if err != nil {
		t.Fatalf("Admin login failed: %v", err)
	}
	userAssignedAuth, err := authenticator.AuthenticateCredentials("norm_assigned", "pass123")
	if err != nil {
		t.Fatalf("Assigned user login failed: %v", err)
	}
	userUnassignedAuth, err := authenticator.AuthenticateCredentials("norm_unassigned", "pass123")
	if err != nil {
		t.Fatalf("Unassigned user login failed: %v", err)
	}

	cleanup := func() {
		_ = os.RemoveAll(tmpDir)
	}

	return server, adminAuth.Token, userAssignedAuth.Token, userUnassignedAuth.Token, cleanup
}

func TestHandleUpload_DualProtocols(t *testing.T) {
	srv, adminToken, userToken, _, cleanup := setupFilesTasksServer(t)
	defer cleanup()

	// 1. Snapshot ingest: unauthenticated
	snapBody := []byte{0xFF, 0xD8, 0xFF, 0xE0, 0x01, 0x02}
	reqSnap := httptest.NewRequest(http.MethodPost, "/upload?type=snapshot&device_id=dev-001", bytes.NewReader(snapBody))
	wSnap := httptest.NewRecorder()
	srv.ServeHTTP(wSnap, reqSnap)

	if wSnap.Code != http.StatusOK {
		t.Fatalf("Expected 200 on snapshot ingest, got %d: %s", wSnap.Code, wSnap.Body.String())
	}
	if wSnap.Body.String() != "Uploaded to memory for dev-001.jpg" {
		t.Fatalf("Unexpected snapshot upload body: %q", wSnap.Body.String())
	}

	// 2. Standard upload: unauthorized without token
	reqNoAuth := httptest.NewRequest(http.MethodPost, "/upload?name=test.txt", bytes.NewReader([]byte("data")))
	wNoAuth := httptest.NewRecorder()
	srv.ServeHTTP(wNoAuth, reqNoAuth)
	if wNoAuth.Code != http.StatusUnauthorized {
		t.Fatalf("Expected 401 on standard upload without token, got %d", wNoAuth.Code)
	}

	// 3. Standard upload: forbidden for normal user
	reqUser := httptest.NewRequest(http.MethodPost, "/upload?name=test.txt", bytes.NewReader([]byte("data")))
	reqUser.Header.Set("Authorization", "Bearer "+userToken)
	wUser := httptest.NewRecorder()
	srv.ServeHTTP(wUser, reqUser)
	if wUser.Code != http.StatusForbidden {
		t.Fatalf("Expected 403 on standard upload for normal user, got %d", wUser.Code)
	}

	// 4. Standard upload: success for admin
	fileContent := []byte("hello cleanroom static file")
	reqAdmin := httptest.NewRequest(http.MethodPost, "/upload?name=test.txt", bytes.NewReader(fileContent))
	reqAdmin.Header.Set("Authorization", "Bearer "+adminToken)
	wAdmin := httptest.NewRecorder()
	srv.ServeHTTP(wAdmin, reqAdmin)
	if wAdmin.Code != http.StatusOK {
		t.Fatalf("Expected 200 on standard upload for admin, got %d: %s", wAdmin.Code, wAdmin.Body.String())
	}
	if wAdmin.Body.String() != "Uploaded to test.txt" {
		t.Fatalf("Unexpected upload response: %q", wAdmin.Body.String())
	}

	// 5. Verify static download
	reqDl := httptest.NewRequest(http.MethodGet, "/downloads/test.txt", nil)
	wDl := httptest.NewRecorder()
	srv.ServeHTTP(wDl, reqDl)
	if wDl.Code != http.StatusOK {
		t.Fatalf("Expected 200 on /downloads/test.txt, got %d", wDl.Code)
	}
	if !bytes.Equal(wDl.Body.Bytes(), fileContent) {
		t.Fatalf("Downloaded content did not match uploaded content")
	}
}

func TestHandleFiles_ListAndDelete(t *testing.T) {
	srv, adminToken, userToken, _, cleanup := setupFilesTasksServer(t)
	defer cleanup()

	// 1. Initial list -> []
	reqList := httptest.NewRequest(http.MethodGet, "/api/files", nil)
	reqList.Header.Set("Authorization", "Bearer "+userToken)
	wList := httptest.NewRecorder()
	srv.ServeHTTP(wList, reqList)
	if wList.Code != http.StatusOK {
		t.Fatalf("Expected 200 on list files, got %d", wList.Code)
	}
	if wList.Body.String() != "[]\n" {
		t.Fatalf("Expected empty array '[]\\n', got %q", wList.Body.String())
	}

	// 2. Upload file as admin
	reqUp := httptest.NewRequest(http.MethodPost, "/upload?name=f1.txt", bytes.NewReader([]byte("content1")))
	reqUp.Header.Set("Authorization", "Bearer "+adminToken)
	wUp := httptest.NewRecorder()
	srv.ServeHTTP(wUp, reqUp)
	if wUp.Code != http.StatusOK {
		t.Fatalf("Upload failed: %d", wUp.Code)
	}

	// 3. List contains f1.txt
	reqList2 := httptest.NewRequest(http.MethodGet, "/api/files", nil)
	reqList2.Header.Set("Authorization", "Bearer "+userToken)
	wList2 := httptest.NewRecorder()
	srv.ServeHTTP(wList2, reqList2)
	var items []types.FileItem
	if err := json.Unmarshal(wList2.Body.Bytes(), &items); err != nil {
		t.Fatalf("Failed to unmarshal file list: %v", err)
	}
	if len(items) != 1 || items[0].Name != "f1.txt" {
		t.Fatalf("Unexpected items in list: %+v", items)
	}

	// 4. Delete f1.txt
	reqDel := httptest.NewRequest(http.MethodDelete, "/api/files?name=f1.txt", nil)
	reqDel.Header.Set("Authorization", "Bearer "+adminToken)
	wDel := httptest.NewRecorder()
	srv.ServeHTTP(wDel, reqDel)
	if wDel.Code != http.StatusOK {
		t.Fatalf("Delete failed: %d", wDel.Code)
	}
	if wDel.Body.String() != `{"status":"success"}` {
		t.Fatalf("Unexpected delete response: %q", wDel.Body.String())
	}
}

func TestHandleTasks_CreateAndDetails(t *testing.T) {
	srv, adminToken, userToken, _, cleanup := setupFilesTasksServer(t)
	defer cleanup()

	// 1. Normal user forbidden to create task
	body := []byte(`{"type":"install","targets":["dev-001"],"payload":"app.apk"}`)
	reqUser := httptest.NewRequest(http.MethodPost, "/api/tasks", bytes.NewReader(body))
	reqUser.Header.Set("Authorization", "Bearer "+userToken)
	wUser := httptest.NewRecorder()
	srv.ServeHTTP(wUser, reqUser)
	if wUser.Code != http.StatusForbidden {
		t.Fatalf("Expected 403 on task create for normal user, got %d", wUser.Code)
	}
	if wUser.Body.String() != "Forbidden: admin only\n" {
		t.Fatalf("Expected 'Forbidden: admin only\\n', got %q", wUser.Body.String())
	}

	// 2. Empty targets rejected
	emptyBody := []byte(`{"type":"install","targets":[]}`)
	reqEmpty := httptest.NewRequest(http.MethodPost, "/api/tasks", bytes.NewReader(emptyBody))
	reqEmpty.Header.Set("Authorization", "Bearer "+adminToken)
	wEmpty := httptest.NewRecorder()
	srv.ServeHTTP(wEmpty, reqEmpty)
	if wEmpty.Code != http.StatusBadRequest {
		t.Fatalf("Expected 400 on empty targets, got %d", wEmpty.Code)
	}

	// 3. Admin creates task successfully
	reqAdmin := httptest.NewRequest(http.MethodPost, "/api/tasks", bytes.NewReader(body))
	reqAdmin.Header.Set("Authorization", "Bearer "+adminToken)
	wAdmin := httptest.NewRecorder()
	srv.ServeHTTP(wAdmin, reqAdmin)
	if wAdmin.Code != http.StatusOK {
		t.Fatalf("Expected 200 on task create for admin, got %d: %s", wAdmin.Code, wAdmin.Body.String())
	}

	var res map[string]interface{}
	if err := json.Unmarshal(wAdmin.Body.Bytes(), &res); err != nil {
		t.Fatalf("Failed to parse task creation response: %v", err)
	}
	taskID, ok := res["task_id"].(string)
	if !ok || taskID == "" {
		t.Fatalf("Missing task_id in response: %+v", res)
	}

	// 4. Retrieve task details (both admin and normal user allowed)
	reqDetails := httptest.NewRequest(http.MethodGet, fmt.Sprintf("/api/tasks/details?task_id=%s", taskID), nil)
	reqDetails.Header.Set("Authorization", "Bearer "+userToken)
	wDetails := httptest.NewRecorder()
	srv.ServeHTTP(wDetails, reqDetails)
	if wDetails.Code != http.StatusOK {
		t.Fatalf("Expected 200 on task details for normal user, got %d", wDetails.Code)
	}

	var task types.Task
	if err := json.Unmarshal(wDetails.Body.Bytes(), &task); err != nil {
		t.Fatalf("Failed to unmarshal task details: %v", err)
	}
	if task.TaskID != taskID || task.Type != "install" {
		t.Fatalf("Unexpected task details: %+v", task)
	}
	if devStatus, exists := task.Devices["dev-001"]; !exists || devStatus.Status != "failed" || devStatus.Result != "Device offline" {
		t.Fatalf("Unexpected offline device status: %+v", devStatus)
	}
}

func TestHandleSnapshots_RBACAndFormat(t *testing.T) {
	srv, adminToken, userAssignedToken, userUnassignedToken, cleanup := setupFilesTasksServer(t)
	defer cleanup()

	// Save snapshot directly into snapshotMgr
	imgBytes := []byte{0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46}
	srv.snapshotMgr.SaveSnapshot("dev-001", imgBytes)

	// 1. Unassigned user forbidden
	reqUn := httptest.NewRequest(http.MethodGet, "/snapshots/dev-001.jpg", nil)
	reqUn.Header.Set("Authorization", "Bearer "+userUnassignedToken)
	wUn := httptest.NewRecorder()
	srv.ServeHTTP(wUn, reqUn)
	if wUn.Code != http.StatusForbidden {
		t.Fatalf("Expected 403 for unassigned user, got %d", wUn.Code)
	}

	// 2. Assigned user allowed
	reqAss := httptest.NewRequest(http.MethodGet, "/snapshots/dev-001.jpg", nil)
	reqAss.Header.Set("Authorization", "Bearer "+userAssignedToken)
	wAss := httptest.NewRecorder()
	srv.ServeHTTP(wAss, reqAss)
	if wAss.Code != http.StatusOK {
		t.Fatalf("Expected 200 for assigned user, got %d", wAss.Code)
	}
	if wAss.Header().Get("Content-Type") != "image/jpeg" {
		t.Fatalf("Expected image/jpeg Content-Type, got %s", wAss.Header().Get("Content-Type"))
	}
	if !bytes.Equal(wAss.Body.Bytes(), imgBytes) {
		t.Fatalf("Snapshot image bytes did not match")
	}

	// 3. Extensionless URL matches
	reqNoExt := httptest.NewRequest(http.MethodGet, "/snapshots/dev-001", nil)
	reqNoExt.Header.Set("Authorization", "Bearer "+adminToken)
	wNoExt := httptest.NewRecorder()
	srv.ServeHTTP(wNoExt, reqNoExt)
	if wNoExt.Code != http.StatusOK {
		t.Fatalf("Expected 200 for extensionless URL, got %d", wNoExt.Code)
	}

	// 4. Invalid extension (.png) returns 404
	reqPng := httptest.NewRequest(http.MethodGet, "/snapshots/dev-001.png", nil)
	reqPng.Header.Set("Authorization", "Bearer "+adminToken)
	wPng := httptest.NewRecorder()
	srv.ServeHTTP(wPng, reqPng)
	if wPng.Code != http.StatusNotFound {
		t.Fatalf("Expected 404 for .png URL, got %d", wPng.Code)
	}
}
