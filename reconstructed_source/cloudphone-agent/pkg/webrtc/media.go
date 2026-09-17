// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_MEDIA_TRACK_CONSTRUCTION_AND_SAMPLE_WRITING
// Evidence: MEDIA_TRACK_CONSTRUCTION_EVIDENCE.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Disassembly:
//   Constructor: webrtc.NewTrackLocalStaticSample (0x968320 AMD64, 0x4d3a80 ARM64)
//   Creation Site: main.main (0x9bc7a8 for display_0, 0x9bc824 for audio_0)
//   Sample Writer: WriteSample (0x968cc0 AMD64, 0x4d4210 ARM64)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"fmt"
	"time"

	"github.com/pion/webrtc/v3"
	"github.com/pion/webrtc/v3/pkg/media"
)

// Confirmed media track identifiers from MEDIA_TRACK_CONSTRUCTION_EVIDENCE.json
const (
	VideoTrackID  = "display_0"
	VideoStreamID = "display_0"

	AudioTrackID  = "audio_0"
	AudioStreamID = "audio_0"
)

// VideoSampleSource defines the interface for injecting H.264 video frames into the WebRTC pipeline.
// Classification: GENERATED_ADAPTER.
type VideoSampleSource interface {
	WriteVideoSample(sample media.Sample) error
}

// AudioSampleSource defines the interface for injecting Opus audio frames into the WebRTC pipeline.
// Classification: GENERATED_ADAPTER.
type AudioSampleSource interface {
	WriteAudioSample(sample media.Sample) error
}

// MediaTracks bundles the local video and audio tracks associated with a PeerConnection.
// Classification: RECONSTRUCTED_FROM_BINARY.
type MediaTracks struct {
	VideoTrack *webrtc.TrackLocalStaticSample
	AudioTrack *webrtc.TrackLocalStaticSample
}

// NewConfirmedMediaTracks constructs the exact video (display_0) and audio (audio_0) tracks
// using webrtc.NewTrackLocalStaticSample matching original agent assembly.
// Classification: RECONSTRUCTED_FROM_BINARY.
func NewConfirmedMediaTracks() (*MediaTracks, error) {
	// 1. Confirmed Video Track: display_0 (video/H264)
	videoTrack, err := webrtc.NewTrackLocalStaticSample(
		webrtc.RTPCodecCapability{
			MimeType:  webrtc.MimeTypeH264,
			ClockRate: 90000,
		},
		VideoTrackID,
		VideoStreamID,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create video track %s: %w", VideoTrackID, err)
	}

	// 2. Confirmed Audio Track: audio_0 (audio/opus)
	audioTrack, err := webrtc.NewTrackLocalStaticSample(
		webrtc.RTPCodecCapability{
			MimeType:    webrtc.MimeTypeOpus,
			ClockRate:   48000,
			Channels:    2,
			SDPFmtpLine: "minptime=10",
		},
		AudioTrackID,
		AudioStreamID,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create audio track %s: %w", AudioTrackID, err)
	}

	return &MediaTracks{
		VideoTrack: videoTrack,
		AudioTrack: audioTrack,
	}, nil
}

// WriteVideoSample writes a media.Sample (H.264 NALUs) to the local video track.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (mt *MediaTracks) WriteVideoSample(sample media.Sample) error {
	if mt == nil || mt.VideoTrack == nil {
		return fmt.Errorf("video track is not initialized")
	}
	return mt.VideoTrack.WriteSample(sample)
}

// WriteAudioSample writes a media.Sample (Opus frames) to the local audio track.
// Classification: RECONSTRUCTED_FROM_BINARY.
func (mt *MediaTracks) WriteAudioSample(sample media.Sample) error {
	if mt == nil || mt.AudioTrack == nil {
		return fmt.Errorf("audio track is not initialized")
	}
	return mt.AudioTrack.WriteSample(sample)
}

// CreateSyntheticH264Sample produces a minimal valid synthetic Annex-B H.264 sample (IDR slice)
// for deterministic testing of the media pipeline without requiring Android hardware encoders.
// Classification: GENERATED_ADAPTER.
func CreateSyntheticH264Sample() media.Sample {
	// Minimal Annex B H.264 frame (SPS, PPS, IDR slice)
	syntheticNALU := []byte{
		0x00, 0x00, 0x00, 0x01, 0x67, 0x42, 0x00, 0x0a, 0xf8, 0x41, 0xa2, // SPS
		0x00, 0x00, 0x00, 0x01, 0x68, 0xce, 0x38, 0x80,                   // PPS
		0x00, 0x00, 0x00, 0x01, 0x65, 0x88, 0x84, 0x00, 0x10,             // IDR
	}
	return media.Sample{
		Data:      syntheticNALU,
		Duration:  33 * time.Millisecond,
		Timestamp: time.Now(),
	}
}

// CreateSyntheticOpusSample produces a minimal valid synthetic Opus frame (silence frame)
// for deterministic testing of the audio pipeline.
// Classification: GENERATED_ADAPTER.
func CreateSyntheticOpusSample() media.Sample {
	// Opus silence frame (0xf8, 0xff, 0xfe)
	syntheticOpus := []byte{0xf8, 0xff, 0xfe}
	return media.Sample{
		Data:      syntheticOpus,
		Duration:  20 * time.Millisecond,
		Timestamp: time.Now(),
	}
}
