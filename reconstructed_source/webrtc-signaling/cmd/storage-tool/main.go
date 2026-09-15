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
)

func main() {
	dataDir := flag.String("data", "./data", "Path to data directory")
	flag.Parse()

	sm, err := storage.NewStorageManager(*dataDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Storage initialization error: %v\n", err)
		os.Exit(1)
	}

	if err := sm.InitBootstrap(); err != nil {
		fmt.Fprintf(os.Stderr, "Bootstrap error: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("BOOTSTRAP_COMPLETE")
}
