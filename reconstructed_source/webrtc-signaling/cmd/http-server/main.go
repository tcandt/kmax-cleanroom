// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: Reconstructed HTTP server binary for Phase 2C.3 differential testing
// Confidence: HIGH

package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"path/filepath"

	"cloudphone-signaling/pkg/auth"
	"cloudphone-signaling/pkg/httpapi"
	"cloudphone-signaling/pkg/license"
	"cloudphone-signaling/pkg/session"
	"cloudphone-signaling/pkg/storage"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_FUNCTION
// Mapping Scope: GENERATED_BUILD_FUNCTION
// Original Function Mapping: NONE
// Purpose: Main entrypoint for launching reconstructed HTTP server in differential testing
// Source Behavior: Initializes storage, session, auth, license, and httpapi.Server; binds to port
// Confidence: HIGH
func main() {
	port := flag.Int("port", 29991, "Port to listen on")
	dataDir := flag.String("data", "./data", "Data directory containing users.json")
	noAuth := flag.Bool("noAuth", false, "Disable authentication requirements")
	flag.BoolVar(noAuth, "no-auth", false, "Disable authentication requirements (alias)")
	iceServersFlag := flag.String("ice_servers", "", "Comma-separated list of STUN/TURN servers")
	stunServerFlag := flag.String("stun_server", "stun:stun.l.google.com:19302", "Deprecated STUN server fallback")
	_ = flag.Bool("tls", false, "Enable TLS (accepted for CLI parity)")
	_ = flag.String("assets", "./assets", "Assets directory (accepted for CLI parity)")
	debug := flag.Bool("debug", false, "Enable debug mode")
	flag.Parse()

	usersPath := filepath.Join(*dataDir, "users.json")
	usersStore := storage.NewUsersStore(usersPath)
	if err := usersStore.LoadOrCreate(); err != nil {
		log.Fatalf("Failed to initialize users store: %v", err)
	}

	tagsPath := filepath.Join(*dataDir, "device_tags.json")
	tagsStore := storage.NewTagsStore(tagsPath)
	if err := tagsStore.LoadOrCreate(); err != nil {
		log.Printf("Failed to initialize tags store: %v", err)
	}

	sharesPath := filepath.Join(*dataDir, "shares.json")
	sharesStore := storage.NewSharesStore(sharesPath)
	if err := sharesStore.Load(); err != nil {
		log.Printf("Failed to initialize shares store: %v", err)
	}

	shortcutsPath := filepath.Join(*dataDir, "shortcuts.json")
	shortcutsStore := storage.NewShortcutsStore(shortcutsPath)
	if err := shortcutsStore.LoadOrCreate(); err != nil {
		log.Printf("Failed to initialize shortcuts store: %v", err)
	}

	sm := session.NewSessionManager(session.RealClock{})
	authenticator := auth.NewAuthenticator(usersStore, sm, *noAuth)
	server := httpapi.NewServer(authenticator, *noAuth)
	server.SetTagsStore(tagsStore)
	server.SetSharesStore(sharesStore)
	server.SetShortcutsStore(shortcutsStore)
	server.SetICEServers(httpapi.ParseICEServers(*iceServersFlag, *stunServerFlag))
	server.SetListeningPort(fmt.Sprintf("%d", *port))
	server.SetDebug(*debug)

	licenseMgr := license.NewManager(*dataDir)
	server.SetLicenseManager(licenseMgr)

	fileMgr := storage.NewFileManager(filepath.Join(*dataDir, "downloads"))
	if err := fileMgr.EnsureDirectories(); err != nil {
		log.Printf("Failed to initialize downloads directory: %v", err)
	}
	server.SetFileManager(fileMgr)
	taskMgr := storage.NewTaskManager()
	server.SetTaskManager(taskMgr)
	snapshotMgr := storage.NewSnapshotManager()
	server.SetSnapshotManager(snapshotMgr)

	addr := fmt.Sprintf("127.0.0.1:%d", *port)
	log.Printf("[HTTP] Reconstructed server listening on %s", addr)
	if err := http.ListenAndServe(addr, server); err != nil {
		log.Fatalf("HTTP server failed: %v", err)
	}
}
