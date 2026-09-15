// CLEANROOM-PROVENANCE:
// Classification: GENERATED_BUILD_STRUCTURE
// Mapping Scope: PACKAGE_LEVEL
// Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Purpose: HTTP response encoding and CORS preflight helpers
// Confidence: HIGH

package httpapi

import (
	"encoding/json"
	"net/http"
)

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Applies CORS headers matching binary oracle behavior
// Source Behavior: Sets Access-Control-Allow-Origin (*), Access-Control-Allow-Methods, and Access-Control-Allow-Headers
// Confidence: HIGH
func SetCORS(w http.ResponseWriter, methods string) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", methods)
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Writes JSON payload with Content-Type and trailing newline
// Source Behavior: json.NewEncoder(w).Encode(data) appending trailing \n
// Confidence: HIGH
func WriteJSON(w http.ResponseWriter, status int, data interface{}) error {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	return json.NewEncoder(w).Encode(data)
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Writes HTTP error response with standard Go http.Error formatting
// Source Behavior: http.Error sets text/plain; charset=utf-8 and appends \n
// Confidence: HIGH
func WriteError(w http.ResponseWriter, status int, msg string) {
	http.Error(w, msg, status)
}
