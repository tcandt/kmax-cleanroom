// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Device Tags REST API (/api/tags)
// Evidence:
//   - Route registration: ROUTE_HANDLER_MAP.json (HandleFunc at call VA 0x76596c, handler main.main.func2 at VA 0x76d200)
//   - Handler & Callees: TAG_HTTP_FUNCTION_SLICES.json
//       * main.main.func2 (VA: 0x76d200, size: 704 bytes) -> CORS injection, method dispatch
//       * main.bFT5Enmzua (VA: 0x769d40, size: 1632 bytes) -> GET /api/tags handler
//       * main.k7fAFNISQp_m (VA: 0x76a4c0, size: 5056 bytes) -> POST /api/tags handler
//       * main.rCajRnfJZ (VA: 0x737da0, size: 608 bytes) -> saveDeviceTags persistence (direct os.WriteFile 0644)
//       * main.pVOasuBli (VA: 0x73d8a0, size: 1120 bytes) -> user device assignment check
//       * main.gevbuZQhJ (VA: 0x76ba00, size: 1216 bytes) -> response JSON builder
//   - Type Descriptors: TAG_TYPE_EVIDENCE.json (Tag 0x7e25a0, DeviceTagsConfig 0x7d6f80)
//   - Wire Matrices: TAG_ROUTE_METHOD_MATRIX.json, TAG_AUTH_MATRIX.json, TAG_OPERATION_CONTRACTS.json
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
// Purpose: Sets or updates the TagsStore instance on the Server
// Confidence: HIGH
func (s *Server) SetTagsStore(ts *storage.TagsStore) {
	s.tagsStore = ts
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for TagsStore with lazy fallback initialization
// Confidence: HIGH
func (s *Server) getTagsStore() *storage.TagsStore {
	if s.tagsStore == nil {
		s.tagsStore = storage.NewTagsStore("device_tags.json")
		_ = s.tagsStore.LoadOrCreate()
	}
	return s.tagsStore
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.main.func2
// VA: 0x76d200
// Size: 704 bytes
// Evidence: TAG_HTTP_FUNCTION_SLICES.json, ROUTE_HANDLER_MAP.json, TAG_ROUTE_METHOD_MATRIX.json
//   - Injects Access-Control-Allow-Origin: *
//   - Injects Access-Control-Allow-Headers: Content-Type, Authorization
//   - OPTIONS: writes 200 OK immediately
//   - POST: delegates to main.k7fAFNISQp_m (VA 0x76a4c0)
//   - All other verbs (GET, PUT, DELETE, PATCH, HEAD): delegates to main.bFT5Enmzua (VA 0x769d40)
// Confidence: HIGH
func (s *Server) HandleTags(w http.ResponseWriter, r *http.Request) {
	// CORS headers injected by main.main.func2
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method == http.MethodPost {
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		s.handlePostTags(w, r)
		return
	}

	// GET and fallback verbs (PUT, DELETE, PATCH, HEAD) handled by GET handler
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	s.handleGetTags(w, r)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.bFT5Enmzua
// VA: 0x769d40
// Size: 1632 bytes
// Evidence: TAG_HTTP_FUNCTION_SLICES.json, TAG_AUTH_MATRIX.json, TAG_OPERATION_CONTRACTS.json
//   - Authenticates caller via main.lYKp_Iuf (VA 0x73b080)
//   - Emits 401 Unauthorized\n on missing/invalid token
//   - Retrieves current tags and deviceTags mapping from state
//   - Emits HTTP 200 with Content-Type: application/json
// Confidence: HIGH
func (s *Server) handleGetTags(w http.ResponseWriter, r *http.Request) {
	if !s.noAuth {
		if _, err := s.Authenticate(r); err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
	}

	cfg := s.getTagsStore().GetConfig()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	if r.Method != http.MethodHead {
		_ = json.NewEncoder(w).Encode(cfg)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.k7fAFNISQp_m
// VA: 0x76a4c0
// Size: 5056 bytes
// Evidence: TAG_HTTP_FUNCTION_SLICES.json, TAG_AUTH_MATRIX.json, TAG_PERSISTENCE_CONTRACT.json, TAG_OPERATION_CONTRACTS.json
//   - Authenticates caller via main.lYKp_Iuf (VA 0x73b080)
//   - Emits 401 Unauthorized\n on missing/invalid token
//   - Unmarshals into *main.Svdju9 (tags + deviceTags)
//   - Emits 400 Invalid JSON\n on parse error or empty body
//   - Role check: role == "admin" (0x76ab58) replaces all state; non-admin scoped merge
//   - Device check via main.pVOasuBli (0x73d8a0) filters non-admin device mutations
//   - Invokes main.rCajRnfJZ (0x737da0) direct os.WriteFile (0644)
//   - Emits HTTP 200 {"status":"success"}\n
// Confidence: HIGH
func (s *Server) handlePostTags(w http.ResponseWriter, r *http.Request) {
	var user *types.User
	if !s.noAuth {
		var err error
		user, err = s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
	}

	var req types.DeviceTagsConfig
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&req); err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid JSON\n"))
		return
	}

	isAdmin := s.noAuth || (user != nil && user.Role == "admin")
	allowedDevices := make(map[string]bool)
	if !isAdmin && user != nil {
		for _, devID := range user.AssignedDevices {
			allowedDevices[devID] = true
		}
	}

	if err := s.getTagsStore().MutateTags(req, isAdmin, allowedDevices); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("{\"status\":\"success\"}\n"))
}
