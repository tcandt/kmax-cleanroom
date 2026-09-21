// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Server Configuration REST Route Family (/api/server/addresses, /api/default_settings, /api/ice_servers, /api/version)
// Evidence:
//   - Route registrations: ROUTE_HANDLER_MAP.json
//       * /api/server/addresses (call VA 0x765bf8, handler main.vz0hZo0q1IzM @ 0x7632a0)
//       * /api/default_settings (call VA 0x765ce8, handler main.j0yBBXR1Hjl @ 0x768980)
//       * /api/ice_servers      (call VA 0x765d00, handler main.vREP2EE2 @ 0x768500)
//       * /api/version          (call VA 0x765d18, handler main.ys0CAJV5f5k @ 0x769840)
//   - Contracts & Type Descriptors:
//       * SERVER_ADDRESSES_CONTRACT.json, DEFAULT_SETTINGS_CONTRACT.json
//       * ICE_SERVER_CONTRACT.json, ICE_SERVER_TYPE_EVIDENCE.json
//       * VERSION_CONTRACT.json, DEFAULT_SETTINGS_TYPE_EVIDENCE.json
// Confidence: HIGH

package httpapi

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"strings"

	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets or updates the configured ICE servers on Server
// Confidence: HIGH
func (s *Server) SetICEServers(servers []types.ICEServer) {
	s.iceServersMu.Lock()
	defer s.iceServersMu.Unlock()
	s.iceServers = servers
	if s.transportHub != nil {
		s.transportHub.SetICEServers(servers)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for the configured ICE servers
// Confidence: HIGH
func (s *Server) GetICEServers() []types.ICEServer {
	s.iceServersMu.RLock()
	defer s.iceServersMu.RUnlock()
	return s.iceServers
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets the in-memory default settings on Server
// Confidence: HIGH
func (s *Server) SetDefaultSettings(settings map[string]interface{}) {
	s.defaultSettingsMu.Lock()
	defer s.defaultSettingsMu.Unlock()
	s.defaultSettings = settings
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Accessor for the in-memory default settings
// Confidence: HIGH
func (s *Server) GetDefaultSettings() map[string]interface{} {
	s.defaultSettingsMu.RLock()
	defer s.defaultSettingsMu.RUnlock()
	return s.defaultSettings
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets the version information returned by /api/version
// Confidence: HIGH
func (s *Server) SetVersionInfo(v types.VersionInfo) {
	s.versionInfo = v
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Sets the daemon listening port string for address resolution
// Confidence: HIGH
func (s *Server) SetListeningPort(port string) {
	s.listeningPort = port
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.vz0hZo0q1IzM
// VA: 0x7632a0
// Size: 3072 bytes
// Evidence: SERVER_ADDRESSES_CONTRACT.json, SERVER_CONFIG_ROUTE_METHOD_MATRIX.json, SERVER_CONFIG_AUTH_MATRIX.json
//   - Injects Access-Control-Allow-Origin: *
//   - Injects Access-Control-Allow-Methods: GET, OPTIONS
//   - Injects Access-Control-Allow-Headers: Content-Type, Authorization
//   - OPTIONS: returns 200 OK immediately with empty body
//   - Authenticates caller via main.lYKp_Iuf (VA 0x73b080)
//   - Resolves r.Host and iterates net.InterfaceAddrs() excluding loopbacks
//   - Returns 200 {"code":0,"data":{"addresses":[...],"current":"..."}}\n
// Confidence: HIGH
func (s *Server) HandleServerAddresses(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if !s.noAuth {
		if _, err := s.Authenticate(r); err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
	}

	current := r.Host
	port := s.listeningPort
	if port == "" {
		port = "80"
	}

	_, portPart, err := net.SplitHostPort(r.Host)
	if err == nil && portPart != "" {
		port = portPart
	}

	addresses := []string{current}
	seen := map[string]bool{current: true}

	if addrs, err := net.InterfaceAddrs(); err == nil {
		for _, addr := range addrs {
			if ipNet, ok := addr.(*net.IPNet); ok {
				ip := ipNet.IP
				if ip.IsLoopback() || ip.IsLinkLocalUnicast() || ip.IsLinkLocalMulticast() {
					continue
				}
				var formatted string
				if ip.To4() != nil {
					formatted = fmt.Sprintf("%s:%s", ip.String(), port)
				} else if ip.To16() != nil {
					formatted = fmt.Sprintf("[%s]:%s", ip.String(), port)
				}
				if formatted != "" && !seen[formatted] {
					seen[formatted] = true
					addresses = append(addresses, formatted)
				}
			}
		}
	}

	resp := types.ServerAddressesResponse{
		Code: 0,
		Data: types.ServerAddressesData{
			Addresses: addresses,
			Current:   current,
		},
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.j0yBBXR1Hjl
// VA: 0x768980
// Size: 3648 bytes
// Evidence: DEFAULT_SETTINGS_CONTRACT.json, DEFAULT_SETTINGS_TYPE_EVIDENCE.json, SERVER_CONFIG_AUTH_MATRIX.json
//   - Injects Access-Control-Allow-Origin: *
//   - Injects Access-Control-Allow-Methods: GET, POST, OPTIONS
//   - Injects Access-Control-Allow-Headers: Content-Type, Authorization
//   - OPTIONS: returns 200 OK immediately with empty body
//   - Authenticates caller via main.lYKp_Iuf (VA 0x73b080)
//   - GET: emits in-memory default_settings map (initial {})
//   - POST: requires admin role via 0x73ae20, emits 403 Forbidden: admin only\n for non-admin
//   - POST: decodes map[string]interface{}, emits 400 Invalid JSON\n on empty body or decode error
//   - POST null: sets map to nil, responds 200 {"status":"success"}
//   - Disallowed verbs (PUT, PATCH, DELETE, HEAD): emits 405 Method not allowed\n
// Confidence: HIGH
func (s *Server) HandleDefaultSettings(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	var user *types.User
	if !s.noAuth {
		var err error
		user, err = s.Authenticate(r)
		if err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
	}

	switch r.Method {
	case http.MethodGet:
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		s.defaultSettingsMu.RLock()
		settings := s.defaultSettings
		s.defaultSettingsMu.RUnlock()

		raw, err := json.Marshal(settings)
		if err != nil {
			w.Write([]byte("{}"))
		} else {
			w.Write(raw)
		}

	case http.MethodPost:
		if !s.noAuth && (user == nil || user.Role != "admin") {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden: admin only\n"))
			return
		}

		bodyBytes, err := io.ReadAll(r.Body)
		if err != nil || len(bytes.TrimSpace(bodyBytes)) == 0 {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Invalid JSON\n"))
			return
		}

		trimmed := bytes.TrimSpace(bodyBytes)
		if string(trimmed) == "null" {
			s.defaultSettingsMu.Lock()
			s.defaultSettings = nil
			s.defaultSettingsMu.Unlock()

			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			w.Write([]byte("{\"status\":\"success\"}"))
			return
		}

		var m map[string]interface{}
		if err := json.Unmarshal(bodyBytes, &m); err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Invalid JSON\n"))
			return
		}

		s.defaultSettingsMu.Lock()
		s.defaultSettings = m
		s.defaultSettingsMu.Unlock()

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("{\"status\":\"success\"}"))

	default:
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte("Method not allowed\n"))
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.vREP2EE2
// VA: 0x768500
// Size: 1152 bytes
// Evidence: ICE_SERVER_CONTRACT.json, ICE_SERVER_TYPE_EVIDENCE.json, SERVER_CONFIG_ROUTE_METHOD_MATRIX.json
//   - Injects Access-Control-Allow-Origin: *
//   - Injects Access-Control-Allow-Methods: GET, OPTIONS
//   - Injects Access-Control-Allow-Headers: Content-Type, Authorization
//   - OPTIONS: returns 200 OK immediately with empty body
//   - Authenticates caller via main.lYKp_Iuf (VA 0x73b080)
//   - Encodes configured []types.ICEServer slice as JSON array with trailing newline
//   - Permissive verb acceptance across GET, POST, PUT, DELETE, etc.
// Confidence: HIGH
func (s *Server) HandleICEServers(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	if !s.noAuth {
		if _, err := s.Authenticate(r); err != nil {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.Header().Set("X-Content-Type-Options", "nosniff")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("Unauthorized\n"))
			return
		}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	s.iceServersMu.RLock()
	servers := s.iceServers
	s.iceServersMu.RUnlock()

	if servers == nil {
		servers = []types.ICEServer{}
	}
	_ = json.NewEncoder(w).Encode(servers)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.ys0CAJV5f5k
// VA: 0x769840
// Size: 1248 bytes
// Evidence: VERSION_CONTRACT.json, SERVER_CONFIG_ROUTE_METHOD_MATRIX.json, SERVER_CONFIG_AUTH_MATRIX.json
//   - Injects Access-Control-Allow-Origin: *
//   - Injects Access-Control-Allow-Methods: GET, OPTIONS
//   - Injects Access-Control-Allow-Headers: Content-Type, Authorization
//   - OPTIONS: returns 200 OK immediately with empty body
//   - PUBLIC: no authentication check performed
//   - Returns 200 {"build_time":"...","git_commit":"...","version":"..."}\n
//   - Permissive verb acceptance across GET, POST, PUT, DELETE, etc.
// Confidence: HIGH
func (s *Server) HandleVersion(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(s.versionInfo)
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Parses -ice_servers and -stun_server CLI flags into []types.ICEServer
// Source Behavior: Matches binary CLI precedence rules: -ice_servers > -stun_server > compiled default
// Confidence: HIGH
func ParseICEServers(iceFlag string, stunFlag string) []types.ICEServer {
	iceFlag = strings.TrimSpace(iceFlag)
	if iceFlag != "" {
		parts := strings.Split(iceFlag, ",")
		var servers []types.ICEServer
		for _, raw := range parts {
			p := strings.TrimSpace(raw)
			if p == "" {
				continue
			}
			lower := strings.ToLower(p)
			if strings.HasPrefix(lower, "turn:") {
				colonIdx := strings.Index(p, ":")
				scheme := p[:colonIdx+1]
				rest := p[colonIdx+1:]
				if atIdx := strings.Index(rest, "@"); atIdx != -1 {
					userinfo := rest[:atIdx]
					hostport := rest[atIdx+1:]
					var username, credential string
					if credIdx := strings.Index(userinfo, ":"); credIdx != -1 {
						username = userinfo[:credIdx]
						credential = userinfo[credIdx+1:]
					} else {
						username = userinfo
					}
					servers = append(servers, types.ICEServer{
						URLs:       []string{scheme + hostport},
						Username:   username,
						Credential: credential,
					})
					continue
				}
			}
			servers = append(servers, types.ICEServer{
				URLs: []string{p},
			})
		}
		if len(servers) > 0 {
			return servers
		}
	}

	stunFlag = strings.TrimSpace(stunFlag)
	if stunFlag != "" {
		return []types.ICEServer{
			{URLs: []string{stunFlag}},
		}
	}

	return []types.ICEServer{
		{URLs: []string{"stun:stun.l.google.com:19302"}},
	}
}
