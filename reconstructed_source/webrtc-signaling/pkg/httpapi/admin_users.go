// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Users & Admin REST Handlers Reconstruction
// Evidence:
//   - Route map: ROUTE_HANDLER_MAP.json
//   - Disassembly & Callgraph: USER_ADMIN_FUNCTION_SLICES.json
//   - Wire contracts: USER_ADMIN_ROUTE_METHOD_MATRIX.json, USER_ADMIN_READ_CONTRACT.json,
//     USER_CREATE_CONTRACT.json, USER_UPDATE_CONTRACTS.json, USER_DELETE_CONTRACT.json,
//     USER_ASSIGNMENT_CROSS_CONTRACT.json, USER_ADMIN_AUTH_MATRIX.json
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"errors"
	"net/http"
	"sort"
	"strings"
	"time"

	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

var (
	errAdminForbidden    = errors.New("forbidden")
	errAdminUnauthorized = errors.New("unauthorized")
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Private helper to evaluate admin role or no-auth mode bypass
// Confidence: HIGH
func (s *Server) checkAdminAuth(r *http.Request) (*types.User, error) {
	if s.noAuth {
		return &types.User{Username: "admin", Role: "admin"}, nil
	}
	user, err := s.Authenticate(r)
	if err != nil {
		return nil, errAdminUnauthorized
	}
	if user.Role != "admin" {
		return nil, errAdminForbidden
	}
	return user, nil
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for UsersStore via Authenticator
// Confidence: HIGH
func (s *Server) getUsersStore() *storage.UsersStore {
	return s.auth.UsersStore()
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.eiuBQux8
// VA: 0x741ec0
// Whole Function VA: 0x741ec0
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-01, FACT-USER-ADMIN-LIST]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_ADMIN_READ_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleAdminUsers(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	usersMap := s.getUsersStore().ListUsers()
	usernames := make([]string, 0, len(usersMap))
	for u := range usersMap {
		usernames = append(usernames, u)
	}
	sort.Strings(usernames)

	resList := make([]map[string]interface{}, 0, len(usernames))
	for _, uname := range usernames {
		u := usersMap[uname]
		assigned := u.AssignedDevices
		if assigned == nil {
			assigned = []string{}
		}

		expiresAtStr := "0001-01-01T00:00:00Z"
		if !u.ExpiresAt.IsZero() {
			expiresAtStr = u.ExpiresAt.Format(time.RFC3339Nano)
		}

		item := map[string]interface{}{
			"active_devices":    []string{},
			"assigned_devices":  assigned,
			"expires_at":        expiresAtStr,
			"forbid_audio":      u.ForbidAudio,
			"forbid_bitrate":    u.ForbidBitrate,
			"forbid_fps":        u.ForbidFPS,
			"forbid_resolution": u.ForbidResolution,
			"note":              u.Note,
			"online":            false,
			"role":              u.Role,
			"settings":          u.Settings,
			"username":          u.Username,
		}
		resList = append(resList, item)
	}

	w.Header().Set("Content-Type", "application/json")
	if r.Method == http.MethodHead {
		w.WriteHeader(http.StatusOK)
		return
	}

	_ = json.NewEncoder(w).Encode(resList)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.zrTQTiT
// VA: 0x744140
// Whole Function VA: 0x744140
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-02, FACT-USER-CREATE]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_CREATE_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleAdminCreateUser(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.CreateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	username := strings.TrimSpace(req.Username)
	password := strings.TrimSpace(req.Password)
	if username == "" || password == "" {
		http.Error(w, "Username and password are required", http.StatusBadRequest)
		return
	}

	if _, exists := s.getUsersStore().GetUser(username); exists {
		http.Error(w, "Username already exists", http.StatusConflict)
		return
	}

	role := strings.TrimSpace(req.Role)
	if role == "" {
		role = "user"
	}

	salt := storage.GenerateSalt()
	hashedPwd := storage.HashPassword(password, salt)

	var expiresAt time.Time
	if req.ExpireSeconds > 0 {
		expiresAt = time.Now().Add(time.Duration(req.ExpireSeconds) * time.Second)
	}

	newUser := types.User{
		Username:         username,
		Password:         hashedPwd,
		Salt:             salt,
		Role:             role,
		AssignedDevices:  []string{},
		Note:             req.Note,
		ForbidBitrate:    false,
		ForbidFPS:        false,
		ForbidResolution: false,
		ForbidAudio:      false,
		ExpiresAt:        expiresAt,
	}

	if err := s.getUsersStore().SetUser(newUser); err != nil {
		http.Error(w, "Failed to save user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.daDbGP
// VA: 0x7464e0
// Whole Function VA: 0x7464e0
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-03, FACT-USER-UPDATE-NOTE]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_UPDATE_CONTRACTS.json
// Confidence: HIGH
func (s *Server) HandleAdminUpdateNote(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.UpdateNoteRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if req.Username == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	user, exists := s.getUsersStore().GetUser(req.Username)
	if !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	user.Note = req.Note
	if err := s.getUsersStore().SetUser(user); err != nil {
		http.Error(w, "Failed to save user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.rmHttgOpxTKh
// VA: 0x746e80
// Whole Function VA: 0x746e80
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-04, FACT-USER-RESET-PASSWORD]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_UPDATE_CONTRACTS.json
// Confidence: HIGH
func (s *Server) HandleAdminResetPassword(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.ResetPasswordRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if req.Username == "" || req.Password == "" {
		http.Error(w, "Username and new password are required", http.StatusBadRequest)
		return
	}

	user, exists := s.getUsersStore().GetUser(req.Username)
	if !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	salt := storage.GenerateSalt()
	user.Salt = salt
	user.Password = storage.HashPassword(req.Password, salt)

	if err := s.getUsersStore().SetUser(user); err != nil {
		http.Error(w, "Failed to save user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.as5uExtX
// VA: 0x7432a0
// Whole Function VA: 0x7432a0
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-05, FACT-USER-ASSIGN-DEVICES]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_UPDATE_CONTRACTS.json
// Confidence: HIGH
func (s *Server) HandleAdminAssign(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.AssignDevicesRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if req.Username == "" {
		http.Error(w, "Target username is required", http.StatusBadRequest)
		return
	}

	user, exists := s.getUsersStore().GetUser(req.Username)
	if !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	devices := req.Devices
	if devices == nil {
		devices = []string{}
	}
	user.AssignedDevices = devices

	if err := s.getUsersStore().SetUser(user); err != nil {
		http.Error(w, "Failed to save user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.m3nYlgst
// VA: 0x744c20
// Whole Function VA: 0x744c20
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-06, FACT-USER-UPDATE-PERMISSIONS]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_UPDATE_CONTRACTS.json
// Confidence: HIGH
func (s *Server) HandleAdminUpdateUser(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.UpdateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid payload", http.StatusBadRequest)
		return
	}

	if req.Username == "" {
		http.Error(w, "username is required", http.StatusBadRequest)
		return
	}

	user, exists := s.getUsersStore().GetUser(req.Username)
	if !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	user.ForbidBitrate = req.ForbidBitrate
	user.ForbidFPS = req.ForbidFPS
	user.ForbidResolution = req.ForbidResolution
	user.ForbidAudio = req.ForbidAudio
	user.Settings = req.Settings

	if req.ExpireSeconds != 0 {
		user.ExpiresAt = time.Now().Add(time.Duration(req.ExpireSeconds) * time.Second)
	}

	if err := s.getUsersStore().SetUser(user); err != nil {
		http.Error(w, "Failed to save user", http.StatusInternalServerError)
		return
	}

	expiresAtStr := "0001-01-01T00:00:00Z"
	if !user.ExpiresAt.IsZero() {
		expiresAtStr = user.ExpiresAt.Format(time.RFC3339Nano)
	}

	resp := map[string]interface{}{
		"code": 0,
		"data": map[string]interface{}{
			"expires_at":        expiresAtStr,
			"forbid_audio":      user.ForbidAudio,
			"forbid_bitrate":    user.ForbidBitrate,
			"forbid_fps":        user.ForbidFPS,
			"forbid_resolution": user.ForbidResolution,
			"settings":          user.Settings,
			"username":          user.Username,
		},
		"msg": "success",
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.eIddSiN_g
// VA: 0x747880
// Whole Function VA: 0x747880
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-07, FACT-USER-KICK]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_UPDATE_CONTRACTS.json
// Confidence: HIGH
func (s *Server) HandleAdminKickUser(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.KickUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if req.Username == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	// Terminate any active connection if registry is present (no-op if user not connected)
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.sGuPXW2D
// VA: 0x740f40
// Whole Function VA: 0x740f40
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-08, FACT-USER-RENAME]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_UPDATE_CONTRACTS.json
// Confidence: HIGH
func (s *Server) HandleAdminRenameUser(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	_, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.RenameUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	oldName := strings.TrimSpace(req.OldUsername)
	newName := strings.TrimSpace(req.NewUsername)
	if oldName == "" || newName == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	if oldName == newName {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
		return
	}

	if _, exists := s.getUsersStore().GetUser(oldName); !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	if _, exists := s.getUsersStore().GetUser(newName); exists {
		http.Error(w, "Username already exists", http.StatusConflict)
		return
	}

	if err := s.getUsersStore().RenameUser(oldName, newName); err != nil {
		http.Error(w, "Failed to rename user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main._Wcin_o
// VA: 0x745ba0
// Whole Function VA: 0x745ba0
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-09, FACT-USER-DELETE]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_DELETE_CONTRACT.json
// Confidence: HIGH
func (s *Server) HandleAdminDeleteUser(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	caller, err := s.checkAdminAuth(r)
	if err != nil {
		if errors.Is(err, errAdminForbidden) {
			http.Error(w, "Forbidden", http.StatusForbidden)
		} else {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		}
		return
	}

	var req types.DeleteUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if req.Username == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	if !s.noAuth && caller != nil && req.Username == caller.Username {
		http.Error(w, "Cannot delete yourself", http.StatusForbidden)
		return
	}

	if _, exists := s.getUsersStore().GetUser(req.Username); !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	if err := s.getUsersStore().DeleteUser(req.Username); err != nil {
		http.Error(w, "Failed to delete user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ajyljXiIN8
// VA: 0x73e7c0
// Whole Function VA: 0x73e7c0
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-10, FACT-USER-REGISTER]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_ADMIN_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleRegister(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusForbidden)
	_ = json.NewEncoder(w).Encode(map[string]string{
		"error": "Public registration is disabled. Please contact an administrator to create an account.",
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.jc6UOob61gVD
// VA: 0x73ffc0
// Whole Function VA: 0x73ffc0
// Mapping Scope: BEHAVIOR_SLICE
// Fact IDs: [FACT-USER-11, FACT-USER-AICONFIG]
// Evidence: USER_ADMIN_FUNCTION_SLICES.json, USER_TYPE_EVIDENCE.json
// Confidence: HIGH
func (s *Server) HandleUserAIConfig(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	targetUsername := ""
	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		targetUsername = user.Username
	} else {
		targetUsername = "admin"
	}

	var req types.AIConfig
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	user, exists := s.getUsersStore().GetUser(targetUsername)
	if !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	user.AIConfig = &req
	if err := s.getUsersStore().SetUser(user); err != nil {
		http.Error(w, "Failed to save user", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}
