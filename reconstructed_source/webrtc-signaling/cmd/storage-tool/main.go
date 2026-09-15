// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_FILE
// Project: KMAX / CloudPhone Clean-Room Source Recovery
// Purpose: CLI utility for differential testing of storage subsystem against original binary.
// Evidence: Minimal bootstrap wrapper exposing storage lifecycle.
// Confidence: HIGH

package main

import (
	"flag"
	"fmt"
	"os"

	"cloudphone-signaling/pkg/storage"
	"cloudphone-signaling/pkg/types"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_FUNCTION
// Original Function Mapping: NONE
// Purpose: CLI entrypoint for differential testing and automated storage verification
// Confidence: N/A
func main() {
	dataDir := flag.String("data", "./data", "Path to data directory")
	action := flag.String("action", "init", "Action to perform: init, create-share, save-user, inspect")
	flag.Parse()

	sm, err := storage.NewStorageManager(*dataDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Storage initialization error: %v\n", err)
		os.Exit(1)
	}

	switch *action {
	case "init":
		if err := sm.InitBootstrap(); err != nil {
			fmt.Fprintf(os.Stderr, "Bootstrap error: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("BOOTSTRAP_COMPLETE")

	case "create-share":
		if err := sm.SharesStore.Load(); err != nil {
			fmt.Fprintf(os.Stderr, "Shares load error: %v\n", err)
			os.Exit(1)
		}
		tok := types.ShareToken{
			TokenID:     "diff-test-token-01",
			DeviceID:    "device-001",
			Creator:     "admin",
			AccessMode:  "readonly",
			Description: "Differential testing share token",
		}
		if err := sm.SharesStore.SetToken(tok); err != nil {
			fmt.Fprintf(os.Stderr, "SetToken error: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("CREATE_SHARE_COMPLETE")

	case "save-user":
		if err := sm.UsersStore.LoadOrCreate(); err != nil {
			fmt.Fprintf(os.Stderr, "Users load error: %v\n", err)
			os.Exit(1)
		}
		u, exists := sm.UsersStore.GetUser("admin")
		if !exists {
			fmt.Fprintf(os.Stderr, "Admin user not found\n")
			os.Exit(1)
		}
		u.Note = "Updated note by differential test"
		if err := sm.UsersStore.SetUser(u); err != nil {
			fmt.Fprintf(os.Stderr, "SetUser error: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("SAVE_USER_COMPLETE")

	default:
		fmt.Fprintf(os.Stderr, "Unknown action: %s\n", *action)
		os.Exit(1)
	}
}
