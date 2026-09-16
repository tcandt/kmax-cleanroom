// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Binary Type Descriptor VA: 0x7bd580 (struct size: 16 bytes)
// Field Descriptor Array VA: 0x7bd5c0 (1 field: GJjLo4tZRb string json:"license")
// Scope: License Activation Request DTO
// Evidence: LICENSE_TYPE_EVIDENCE.json, LICENSE_ACTIVATION_REJECTION_CONTRACT.json
// Confidence: HIGH

package types

// ActivationRequest represents the incoming JSON payload for /api/activate.
// Recovered directly from ELF type descriptor at 0x7bd580:
// struct { GJjLo4tZRb string "json:\"license\"" }
type ActivationRequest struct {
	License string `json:"license"`
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BEHAVIOR
// Mapping Scope: WIRE_SCHEMA
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Original Construction: Runtime map[string]interface{} constructed in main.J_5lH4w6CU at VA 0x735400
// Scope: 13-key entitlement status response model matching original wire representation
// Evidence: LICENSE_STATUS_CONTRACT.json, LICENSE_ROUTE_METHOD_MATRIX.json
// Confidence: HIGH

// LicenseStatusResponse represents the 13-field wire model for /api/license_status and /debug/license.
// In the original binary, this is constructed as a map[string]interface{} in main.J_5lH4w6CU (0x735400).
// Fields are ordered alphabetically to match Go's map serialization on the wire.
type LicenseStatusResponse struct {
	Activated           bool   `json:"activated"`
	CurrentDevices      int    `json:"current_devices"`
	Customer            string `json:"customer"`
	DaysRemaining       int    `json:"days_remaining"`
	ErrorMsg            string `json:"error_msg"`
	ExpiresAt           string `json:"expires_at"`
	LicenseExpired      bool   `json:"license_expired"`
	LicenseSource       string `json:"license_source"`
	MachineID           string `json:"machine_id"`
	MaxDevices          int    `json:"max_devices"`
	PostPromoMaxDevices int    `json:"post_promo_max_devices"`
	Promo               bool   `json:"promo"`
	Status              string `json:"status"`
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_WIRE_MODEL
// Mapping Scope: GENERATED_WIRE_MODEL
// Original Function Mapping: main.jcraNgV8Jg (0x74b6c0)
// Scope: Convenience wire model for successful activation response map
// Evidence: LICENSE_ROUTE_FAMILY.json
// Confidence: HIGH

// ActivationSuccessResponse represents the wire response upon successful activation.
// Original binary constructs a runtime map with keys "status" and "message".
type ActivationSuccessResponse struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_WIRE_MODEL
// Mapping Scope: GENERATED_WIRE_MODEL
// Original Function Mapping: main.jcraNgV8Jg (0x74b6c0)
// Scope: Convenience wire model for error activation response map
// Evidence: LICENSE_ACTIVATION_REJECTION_CONTRACT.json
// Confidence: HIGH

// ActivationErrorResponse represents the wire response upon validation error.
// Original binary constructs a runtime map with key "error".
type ActivationErrorResponse struct {
	Error string `json:"error"`
}
