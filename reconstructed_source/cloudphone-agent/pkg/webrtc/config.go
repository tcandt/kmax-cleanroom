// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_MEDIA_ENGINE_AND_CODEC_REGISTRATION
// Evidence: WEBRTC_CODEC_CAPABILITY_MATRIX.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Disassembly: main.main (0x9bc7a1 AMD64, 0x51e7f0 ARM64 for H264; 0x9bc816 AMD64, 0x51e850 ARM64 for Opus)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"github.com/pion/webrtc/v3"
)

// NewEvidenceBoundMediaEngine initializes a Pion MediaEngine strictly populated with
// the confirmed codecs from WEBRTC_CODEC_CAPABILITY_MATRIX.json:
// 1. video/H264 at 90000 Hz with nack, pli, fir feedback
// 2. audio/opus at 48000 Hz, 2 channels, with fmtp minptime=10
// Excludes unselected codecs (VP8, VP9, AV1, PCMU, PCMA, G722) per frozen evidence.
// Classification: RECONSTRUCTED_FROM_BINARY.
func NewEvidenceBoundMediaEngine() (*webrtc.MediaEngine, error) {
	m := &webrtc.MediaEngine{}

	// 1. Confirmed Video Codec: H.264 / 90000
	h264Capability := webrtc.RTPCodecCapability{
		MimeType:    webrtc.MimeTypeH264,
		ClockRate:   90000,
		Channels:    1,
		SDPFmtpLine: "",
		RTCPFeedback: []webrtc.RTCPFeedback{
			{Type: "nack"},
			{Type: "pli"},
			{Type: "fir"},
		},
	}
	if err := m.RegisterCodec(webrtc.RTPCodecParameters{
		RTPCodecCapability: h264Capability,
		PayloadType:        96,
	}, webrtc.RTPCodecTypeVideo); err != nil {
		return nil, err
	}

	// 2. Confirmed Audio Codec: Opus / 48000 / 2ch / minptime=10
	opusCapability := webrtc.RTPCodecCapability{
		MimeType:     webrtc.MimeTypeOpus,
		ClockRate:    48000,
		Channels:     2,
		SDPFmtpLine:  "minptime=10",
		RTCPFeedback: nil,
	}
	if err := m.RegisterCodec(webrtc.RTPCodecParameters{
		RTPCodecCapability: opusCapability,
		PayloadType:        111,
	}, webrtc.RTPCodecTypeAudio); err != nil {
		return nil, err
	}

	return m, nil
}

// NewAPIWithEvidenceBoundEngine constructs a Pion webrtc.API using the evidence-bound media engine.
// Classification: GENERATED_ADAPTER.
func NewAPIWithEvidenceBoundEngine() (*webrtc.API, error) {
	mediaEngine, err := NewEvidenceBoundMediaEngine()
	if err != nil {
		return nil, err
	}

	settingEngine := webrtc.SettingEngine{}
	// DetachDataChannels or standard multiplexing can be configured if needed
	return webrtc.NewAPI(
		webrtc.WithMediaEngine(mediaEngine),
		webrtc.WithSettingEngine(settingEngine),
	), nil
}

// BuildRTCConfiguration creates a webrtc.Configuration from a list of ICE servers.
// Classification: GENERATED_ADAPTER.
func BuildRTCConfiguration(iceServers []webrtc.ICEServer) webrtc.Configuration {
	if len(iceServers) == 0 {
		// Standard default STUN fallback if none provided by signaling config
		iceServers = []webrtc.ICEServer{
			{
				URLs: []string{"stun:stun.l.google.com:19302"},
			},
		}
	}
	return webrtc.Configuration{
		ICEServers: iceServers,
	}
}
