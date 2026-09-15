// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: stateful test harness communicating over stdio to enable long-lived in-memory session testing
// Confidence: N/A

package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
)

type Request struct {
	Op       string `json:"op"`
	Username string `json:"username,omitempty"`
	Password string `json:"password,omitempty"`
	Token    string `json:"token,omitempty"`
	Seconds  int64  `json:"seconds,omitempty"`
}

type Response struct {
	OK      bool        `json:"ok"`
	Error   string      `json:"error,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Token   string      `json:"token,omitempty"`
	User    string      `json:"user,omitempty"`
	Role    string      `json:"role,omitempty"`
	Devices []string    `json:"assigned_devices,omitempty"`
	Count   int         `json:"count,omitempty"`
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: main loop of stateful auth test interface
// Confidence: N/A
func main() {
	dataDir := flag.String("data", "./data", "Data directory containing users.json")
	useMockClock := flag.Bool("mockClock", false, "Use controllable mock clock for TTL testing")
	noAuth := flag.Bool("no-auth", false, "Enable no-auth bypass mode")
	flag.Parse()

	// Initialize persistence
	usersPath := filepath.Join(*dataDir, "users.json")
	usersStore := storage.NewUsersStore(usersPath)
	if err := usersStore.LoadOrCreate(); err != nil {
		fmt.Fprintf(os.Stderr, "Failed to load users: %v\n", err)
		os.Exit(1)
	}

	var clock session.Clock = session.RealClock{}
	var mockClock *session.MockClock
	if *useMockClock {
		mockClock = session.NewMockClock(time.Now())
		clock = mockClock
	}

	sessionMgr := session.NewSessionManager(clock)
	authenticator := auth.NewAuthenticator(usersStore, sessionMgr, *noAuth)

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Bytes()
		if len(line) == 0 {
			continue
		}

		var req Request
		if err := json.Unmarshal(line, &req); err != nil {
			sendResp(Response{OK: false, Error: fmt.Sprintf("invalid JSON: %v", err)})
			continue
		}

		handleOp(req, authenticator, sessionMgr, mockClock)
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: dispatches JSON requests to in-memory authenticator and session manager
// Confidence: N/A
func handleOp(req Request, a *auth.Authenticator, sm *session.SessionManager, mc *session.MockClock) {
	switch req.Op {
	case "login":
		res, err := a.AuthenticateCredentials(req.Username, req.Password)
		if err != nil {
			sendResp(Response{OK: false, Error: err.Error()})
			return
		}
		sendResp(Response{
			OK:      true,
			Token:   res.Token,
			User:    res.Username,
			Role:    res.Role,
			Devices: res.AssignedDevices,
		})

	case "verify_token":
		user, err := a.ValidateToken(req.Token)
		if err != nil {
			sendResp(Response{OK: false, Error: err.Error()})
			return
		}
		sendResp(Response{OK: true, User: user})

	case "logout":
		a.Logout(req.Token)
		sendResp(Response{OK: true, Data: map[string]string{"status": "success"}})

	case "get_profile":
		user, err := a.ValidateToken(req.Token)
		if err != nil {
			sendResp(Response{OK: false, Error: err.Error()})
			return
		}
		profile, err := a.GetUserProfile(user)
		if err != nil {
			sendResp(Response{OK: false, Error: err.Error()})
			return
		}
		sendResp(Response{OK: true, Data: profile})

	case "count_user_sessions":
		c := sm.CountUserSessions(req.Username)
		sendResp(Response{OK: true, Count: c})

	case "revoke_user_sessions":
		c := sm.RevokeUserSessions(req.Username)
		sendResp(Response{OK: true, Count: c})

	case "advance_clock":
		if mc == nil {
			sendResp(Response{OK: false, Error: "mockClock not enabled"})
			return
		}
		mc.Add(time.Duration(req.Seconds) * time.Second)
		sendResp(Response{OK: true, Data: map[string]string{"now": mc.Now().Format(time.RFC3339)}})

	case "ping":
		sendResp(Response{OK: true, Data: "pong"})

	default:
		sendResp(Response{OK: false, Error: fmt.Sprintf("unknown op: %s", req.Op)})
	}
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_TEST_INTERFACE
// Original Function Mapping: NONE
// Source Behavior: serializes Response to JSON line on standard output
// Confidence: N/A
func sendResp(resp Response) {
	b, _ := json.Marshal(resp)
	fmt.Println(string(b))
}
