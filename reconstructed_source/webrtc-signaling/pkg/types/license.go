// CLEANROOM-PROVENANCE:
// Classification: DIRECT_TYPE_RECOVERY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: License Request DTO & Entitlement Status DTO (0x7bd580, 0x7bf940, 0x7c0340)
// Evidence: LICENSE_TYPE_EVIDENCE.json, LICENSE_STATUS_CONTRACT.json, LICENSE_ACTIVATION_REJECTION_CONTRACT.json
// Confidence: HIGH

package types

// ActivationRequest represents the incoming JSON payload for /api/activate.
// Recovered directly from ELF type descriptor at 0x7bd580:
// struct { GJjLo4tZRb string "json:\"license\"" }
type ActivationRequest struct {
	License string `json:"license"`
}

// LicenseStatusResponse represents the 13-field response for /api/license_status and /debug/license.
// Recovered directly from runtime map construction in main.J_5lH4w6CU (0x735400).
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

// ActivationSuccessResponse represents the wire response upon successful activation.
// Recovered from main.jcraNgV8Jg (0x74bd11: "success", 0x74bd57: "激活码更新成功").
type ActivationSuccessResponse struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

// ActivationErrorResponse represents the wire response upon validation error.
// Recovered from main.jcraNgV8Jg (0x74be4f: "error", 0x42ab3e: "授权码格式错误").
type ActivationErrorResponse struct {
	Error string `json:"error"`
}
