// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Device Shares REST API (/api/share/*)
// Evidence:
//   - Route registrations in ROUTE_HANDLER_MAP.json:
//       * /api/share/create (call VA 0x765b50, handler main.cYYycnP3 at VA 0x75c240)
//       * /api/share/list (call VA 0x765b68, handler main._0VLCRLL at VA 0x75d9a0)
//       * /api/share/revoke (call VA 0x765b80, handler main.nFuQn_o at VA 0x75e5a0)
//       * /api/share/extend (call VA 0x765b98, handler main.d1oM4aHeERk4 at VA 0x75ee20)
//       * /api/share/update (call VA 0x765bb0, handler main.nMFGdqfO at VA 0x75fb20)
//       * /api/share/info (call VA 0x765bc8, handler main.busbgD at VA 0x760480)
//       * /api/share/redeem_card (call VA 0x765be0, handler main.iSjKlH94xCO at VA 0x761a20)
//   - Persistence & Helper Callees:
//       * main.fomL4ATwVV1 (VA 0x739900) -> saveShares (atomic .tmp + os.Rename, mode 0600)
//       * main.cLTBoWx9C0 (VA 0x739440) -> generateCardCode (CP-%s-%s base32)
//       * main.dYBSRoVh.func1 (VA 0x73a120) -> shareCleanupWorker
//   - Type Descriptors: SHARE_TYPE_EVIDENCE.json (ShareToken at 0x80f700, 192 bytes, 18 fields)
//   - Matrices: SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH

package httpapi

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: sets or updates the SharesStore instance on the Server
// Confidence: HIGH
func (s *Server) SetSharesStore(ss *storage.SharesStore) {
	s.sharesStore = ss
	if s.transportHub != nil {
		s.transportHub.SetSharesStore(ss)
	}
}


// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Source Behavior: accessor for SharesStore with lazy fallback initialization
// Confidence: HIGH
func (s *Server) getSharesStore() *storage.SharesStore {
	if s.sharesStore == nil {
		s.sharesStore = storage.NewSharesStore("shares.json")
		_ = s.sharesStore.Load()
	}
	return s.sharesStore
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.cLTBoWx9C0
// VA: 0x739440
// Evidence: SHARE_TYPE_EVIDENCE.json, SHARE_HTTP_FUNCTION_SLICES.json
// Confidence: HIGH
func generateCardCode() string {
	const alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
	b := make([]byte, 8)
	_, _ = rand.Read(b)
	var chars [8]byte
	for i := 0; i < 8; i++ {
		chars[i] = alphabet[b[i]&0x1f]
	}
	return fmt.Sprintf("CP-%s-%s", string(chars[:4]), string(chars[4:]))
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: BEHAVIOR_SLICE
// Binary Symbol: main.cYYycnP3
// VA: 0x75c7e0
// Evidence: inlined 16-byte random read, lowercase hex encoding, and st_ prefix concatenation (0x75c7e0-0x75c867)
// Confidence: HIGH
func generateShareToken() string {
	b := make([]byte, 16)
	_, _ = rand.Read(b)
	return "st_" + hex.EncodeToString(b)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.cYYycnP3
// VA: 0x75c240
// Evidence: SHARE_CREATE_CONTRACT.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareCreate(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Method Not Allowed\n"))
		return
	}

	creator := "admin"
	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
		if user.Role != "admin" {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden: admin only\n"))
			return
		}
		creator = user.Username
	}

	var req types.CreateShareRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid payload\n"))
		return
	}

	if strings.TrimSpace(req.DeviceID) == "" {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("device_id is required\n"))
		return
	}

	store := s.getSharesStore()

	// Check if active share already exists on device
	if existing, exists := store.GetTokenByDeviceID(req.DeviceID); exists {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusConflict)
		errMsg := fmt.Sprintf("该设备已存在活跃分享（卡密 %s），请先撤销或对其延时", existing.CardCode)
		_ = json.NewEncoder(w).Encode(map[string]interface{}{
			"code": 409,
			"msg":  errMsg,
		})
		return
	}

	tokenID := generateShareToken()
	cardCode := generateCardCode()
	now := time.Now()

	var expiresAt time.Time
	if req.ExpireSeconds > 0 {
		expiresAt = now.Add(time.Duration(req.ExpireSeconds) * time.Second)
	}

	var pwdHash string
	requirePwd := false
	if req.Password != "" {
		requirePwd = true
		h := sha256.Sum256([]byte(req.Password))
		pwdHash = hex.EncodeToString(h[:])
	}

	accessMode := req.AccessMode
	if accessMode == "" {
		accessMode = "full"
	}

	tok := types.ShareToken{
		TokenID:          tokenID,
		CardCode:         cardCode,
		DeviceID:         req.DeviceID,
		Creator:          creator,
		CreatedAt:        now,
		ExpiresAt:        expiresAt,
		AccessMode:       accessMode,
		RequirePassword:  requirePwd,
		PasswordHash:     pwdHash,
		AllowClipboard:   req.AllowClipboard,
		AllowFileTx:      req.AllowFileTx,
		ForbidBitrate:    req.ForbidBitrate,
		ForbidFPS:        req.ForbidFPS,
		ForbidResolution: req.ForbidResolution,
		ForbidAudio:      req.ForbidAudio,
		GuestSettings:    req.GuestSettings,
		Description:      req.Description,
		UseCount:         0,
	}

	_ = store.SetToken(tok)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"code": 0,
		"data": types.CreateShareResponseData{
			AccessMode: tok.AccessMode,
			CardCode:   tok.CardCode,
			DeviceID:   tok.DeviceID,
			ExpiresAt:  tok.ExpiresAt,
			ShareURL:   "/share?token=" + tok.TokenID,
			Token:      tok.TokenID,
		},
		"msg": "success",
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main._0VLCRLL
// VA: 0x75d9a0
// Evidence: SHARE_LIST_CONTRACT.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareList(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
		if user.Role != "admin" {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden: admin only\n"))
			return
		}
	}

	filterDev := r.URL.Query().Get("device_id")
	tokens := s.getSharesStore().ListTokens()

	items := make([]types.ShareListItem, 0)
	for _, tok := range tokens {
		if filterDev != "" && tok.DeviceID != filterDev {
			continue
		}
		items = append(items, types.ShareListItem{
			ShareToken:        tok,
			ActiveConnections: 0,
		})
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if r.Method != http.MethodHead {
		_ = json.NewEncoder(w).Encode(map[string]interface{}{
			"code": 0,
			"data": items,
		})
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.nFuQn_o
// VA: 0x75e5a0
// Evidence: SHARE_MUTATION_CONTRACTS.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareRevoke(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
		if user.Role != "admin" {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden: admin only\n"))
			return
		}
	}

	var req types.RevokeShareRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid payload\n"))
		return
	}

	if req.Token == "" {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Share token not found\n"))
		return
	}

	store := s.getSharesStore()
	if _, exists := store.GetToken(req.Token); !exists {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Share token not found\n"))
		return
	}

	_ = store.DeleteToken(req.Token)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"code": 0,
		"msg":  "Share revoked successfully",
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.d1oM4aHeERk4
// VA: 0x75ee20
// Evidence: SHARE_MUTATION_CONTRACTS.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareExtend(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Method Not Allowed\n"))
		return
	}

	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
		if user.Role != "admin" {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden: admin only\n"))
			return
		}
	}

	var req types.ExtendShareRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid payload\n"))
		return
	}

	if req.Token == "" || req.ExtendSeconds <= 0 {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("token and positive extend_seconds are required\n"))
		return
	}

	tok, exists := s.getSharesStore().GetToken(req.Token)
	if !exists {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Share token not found\n"))
		return
	}

	if tok.ExpiresAt.IsZero() {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_ = json.NewEncoder(w).Encode(map[string]interface{}{
			"code": 400,
			"msg":  "永久有效的分享无需延时",
		})
		return
	}

	updated, _ := s.getSharesStore().ExtendToken(req.Token, req.ExtendSeconds)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"code": 0,
		"data": map[string]interface{}{
			"expires_at": updated.ExpiresAt,
		},
		"msg": "success",
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.nMFGdqfO
// VA: 0x75fb20
// Evidence: SHARE_MUTATION_CONTRACTS.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareUpdate(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method != http.MethodPost {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Method Not Allowed\n"))
		return
	}

	if !s.noAuth {
		user, err := s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
		if user.Role != "admin" {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden: admin only\n"))
			return
		}
	}

	var req types.UpdateShareRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid payload\n"))
		return
	}

	if req.Token == "" {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("token is required\n"))
		return
	}

	updated, err := s.getSharesStore().UpdateToken(req.Token, req)
	if err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Share token not found\n"))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"code": 0,
		"data": updated,
		"msg":  "success",
	})
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.busbgD
// VA: 0x760480
// Evidence: SHARE_INFO_CONTRACT.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareInfo(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	token := r.URL.Query().Get("token")
	if token == "" {
		token = r.URL.Query().Get("stoken")
	}

	if token == "" {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Token required\n"))
		return
	}

	tok, exists := s.getSharesStore().GetToken(token)
	if !exists {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Share link expired or invalid\n"))
		return
	}

	now := time.Now()
	if !tok.ExpiresAt.IsZero() && now.After(tok.ExpiresAt) {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Share link expired or invalid\n"))
		return
	}

	if tok.RequirePassword {
		reqPwd := r.URL.Query().Get("password")
		h := sha256.Sum256([]byte(reqPwd))
		hashStr := hex.EncodeToString(h[:])
		if reqPwd == "" || hashStr != tok.PasswordHash {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			_ = json.NewEncoder(w).Encode(map[string]interface{}{
				"code": 401,
				"data": map[string]interface{}{
					"require_password": true,
				},
				"msg": "该分享需要访问密码",
			})
			return
		}
	}

	var remSec int64 = -1
	if !tok.ExpiresAt.IsZero() {
		remSec = int64(tok.ExpiresAt.Sub(now).Seconds())
		if remSec < 0 {
			remSec = 0
		}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if r.Method != http.MethodHead {
		_ = json.NewEncoder(w).Encode(map[string]interface{}{
			"code": 0,
			"data": types.ShareInfoResponseData{
				AccessMode:       tok.AccessMode,
				AllowClipboard:   tok.AllowClipboard,
				AllowFileTx:      tok.AllowFileTx,
				CardCode:         tok.CardCode,
				Description:      tok.Description,
				DeviceID:         tok.DeviceID,
				DeviceName:       tok.DeviceID,
				ExpiresAt:        tok.ExpiresAt,
				ForbidAudio:      tok.ForbidAudio,
				ForbidBitrate:    tok.ForbidBitrate,
				ForbidFPS:        tok.ForbidFPS,
				ForbidResolution: tok.ForbidResolution,
				GuestSettings:    tok.GuestSettings,
				Online:           false,
				RemainingSeconds: remSec,
				RequirePassword:  tok.RequirePassword,
				Token:            tok.TokenID,
			},
		})
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.iSjKlH94xCO
// VA: 0x761a20
// Evidence: SHARE_REDEEM_CARD_CONTRACT.json, SHARE_ROUTE_METHOD_MATRIX.json, SHARE_AUTH_MATRIX.json
// Confidence: HIGH
func (s *Server) HandleShareRedeemCard(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	var req types.RedeemCardRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Invalid payload\n"))
		return
	}

	if req.CardCode == "" {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("card_code is required\n"))
		return
	}

	tok, exists := s.getSharesStore().GetTokenByCardCode(req.CardCode)
	if !exists {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_ = json.NewEncoder(w).Encode(map[string]interface{}{
			"code": 404,
			"msg":  "卡密不存在或已失效",
		})
		return
	}

	now := time.Now()
	var remSec int64 = -1
	if !tok.ExpiresAt.IsZero() {
		remSec = int64(tok.ExpiresAt.Sub(now).Seconds())
		if remSec < 0 {
			remSec = 0
		}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"code": 0,
		"data": types.ShareInfoResponseData{
			AccessMode:       tok.AccessMode,
			AllowClipboard:   tok.AllowClipboard,
			AllowFileTx:      tok.AllowFileTx,
			CardCode:         tok.CardCode,
			Description:      tok.Description,
			DeviceID:         tok.DeviceID,
			DeviceName:       tok.DeviceID,
			ExpiresAt:        tok.ExpiresAt,
			ForbidAudio:      tok.ForbidAudio,
			ForbidBitrate:    tok.ForbidBitrate,
			ForbidFPS:        tok.ForbidFPS,
			ForbidResolution: tok.ForbidResolution,
			GuestSettings:    tok.GuestSettings,
			Online:           false,
			RemainingSeconds: remSec,
			RequirePassword:  tok.RequirePassword,
			Token:            tok.TokenID,
		},
		"msg": "success",
	})
}
