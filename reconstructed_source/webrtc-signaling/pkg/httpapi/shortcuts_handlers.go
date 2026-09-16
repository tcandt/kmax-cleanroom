// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Shortcuts REST API (/api/shortcuts)
// Evidence:
//   - Route registration: ROUTE_HANDLER_MAP.json (HandleFunc at call VA 0x765984, handler main.main.func3 at VA 0x76d4c0)
//   - Wrapper & Handler: SHORTCUT_HTTP_FUNCTION_SLICES.json
//       * main.main.func3 (VA: 0x76d4c0, size: 672 bytes) -> CORS injection, OPTIONS 200, non-OPTIONS dispatch
//       * main.yHBQWSpi (VA: 0x76c640, size: 1856 bytes) -> auth check, GET/POST routing, JSON handling, 405 error
//       * main.iXiPYH2zBLTK (VA: 0x76bf20, size: 640 bytes) -> loadShortcuts
//       * main.jk9A26 (VA: 0x76c2c0, size: 608 bytes) -> saveShortcuts (direct os.WriteFile 0644)
//   - Type Descriptors: SHORTCUT_TYPE_EVIDENCE.json (Shortcut 0x7d70c0, map 0x7bfc40)
//   - Wire Matrices: SHORTCUT_ROUTE_METHOD_MATRIX.json, SHORTCUT_AUTH_MATRIX.json, SHORTCUT_OPERATION_CONTRACTS.json
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"net/http"

	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets or updates the ShortcutsStore instance on the Server
// Confidence: HIGH
func (s *Server) SetShortcutsStore(ss *storage.ShortcutsStore) {
	s.shortcutsStore = ss
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for ShortcutsStore with lazy fallback initialization
// Confidence: HIGH
func (s *Server) getShortcutsStore() *storage.ShortcutsStore {
	if s.shortcutsStore == nil {
		s.shortcutsStore = storage.NewShortcutsStore("shortcuts.json")
		_ = s.shortcutsStore.LoadOrCreate()
	}
	return s.shortcutsStore
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.main.func3
// VA: 0x76d4c0
// Size: 672 bytes
// Evidence: SHORTCUT_HTTP_FUNCTION_SLICES.json, ROUTE_HANDLER_MAP.json, SHORTCUT_ROUTE_METHOD_MATRIX.json
//   - Injects Access-Control-Allow-Origin: *
//   - Injects Access-Control-Allow-Methods: GET, POST, OPTIONS
//   - Injects Access-Control-Allow-Headers: Content-Type, Authorization
//   - OPTIONS: returns 200 OK immediately with empty body
//   - Non-OPTIONS: delegates to main.yHBQWSpi (VA 0x76c640)
// Confidence: HIGH
func (s *Server) HandleShortcuts(w http.ResponseWriter, r *http.Request) {
	// CORS headers injected by main.main.func3
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	s.handleShortcutsBusiness(w, r)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.yHBQWSpi
// VA: 0x76c640
// Size: 1856 bytes
// Evidence: SHORTCUT_HTTP_FUNCTION_SLICES.json, SHORTCUT_AUTH_MATRIX.json, SHORTCUT_OPERATION_CONTRACTS.json
//   - Authenticates caller via main.lYKp_Iuf (VA 0x73b080)
//   - Emits 401 Unauthorized\n on missing/invalid token
//   - In -no-auth mode, bypasses authentication and uses key "admin"
//   - GET: retrieves []Shortcut for caller username, emits HTTP 200 application/json
//   - POST: decodes []Shortcut, emits 400 Invalid JSON\n on decode failure
//   - POST: persists to shortcuts.json via main.jk9A26, emits 200 {"status":"success"}\n
//   - Disallowed verbs (PUT, PATCH, DELETE, HEAD): emits 405 Method not allowed\n
// Confidence: HIGH
func (s *Server) handleShortcutsBusiness(w http.ResponseWriter, r *http.Request) {
	username := "admin"
	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
		username = user.Username
	}

	switch r.Method {
	case http.MethodGet:
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		list := s.getShortcutsStore().Get(username)
		_ = json.NewEncoder(w).Encode(list)

	case http.MethodPost:
		var list []types.Shortcut
		dec := json.NewDecoder(r.Body)
		if err := dec.Decode(&list); err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Invalid JSON\n"))
			return
		}

		if err := s.getShortcutsStore().Set(username, list); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("{\"status\":\"success\"}\n"))

	default:
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Method not allowed\n"))
	}
}
