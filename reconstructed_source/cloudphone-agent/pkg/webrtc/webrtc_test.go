// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_UNIT_TESTS
// Evidence: WEBRTC_CODEC_CAPABILITY_MATRIX.json, MEDIA_TRACK_CONSTRUCTION_EVIDENCE.json,
//   DATACHANNEL_LABEL_EVIDENCE.json, WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/pion/webrtc/v3"
)

// TestEvidenceBoundMediaEngine verifies that ONLY evidence-confirmed codecs are registered.
// Unconfirmed codecs (VP8, VP9, AV1, PCMU, PCMA, G722) must NOT appear in the generated SDP.
func TestEvidenceBoundMediaEngine(t *testing.T) {
	session, err := NewPeerSession(99, "dev-test-codecs", nil)
	if err != nil {
		t.Fatalf("failed to create session: %v", err)
	}
	defer session.Close()

	offerPayload, err := session.CreateOffer()
	if err != nil {
		t.Fatalf("failed to create offer: %v", err)
	}

	sdp := offerPayload.SDP

	// 1. Confirmed codecs must be present
	if !strings.Contains(sdp, "H264/90000") {
		t.Errorf("expected H264/90000 in SDP, but not found:\n%s", sdp)
	}
	if !strings.Contains(sdp, "opus/48000/2") {
		t.Errorf("expected opus/48000/2 in SDP, but not found:\n%s", sdp)
	}
	if !strings.Contains(sdp, "minptime=10") {
		t.Errorf("expected minptime=10 in SDP, but not found:\n%s", sdp)
	}

	// 2. Unconfirmed codecs must NOT be present
	unconfirmed := []string{"VP8", "VP9", "AV1", "PCMU", "PCMA", "G722"}
	for _, codec := range unconfirmed {
		if strings.Contains(strings.ToUpper(sdp), codec) {
			t.Errorf("unconfirmed codec %s unexpectedly present in SDP", codec)
		}
	}
}

// TestMediaTrackProperties verifies track IDs, stream IDs, and sample writing interfaces.
func TestMediaTrackProperties(t *testing.T) {
	tracks, err := NewConfirmedMediaTracks()
	if err != nil {
		t.Fatalf("failed to create confirmed media tracks: %v", err)
	}

	if tracks.VideoTrack.ID() != VideoTrackID {
		t.Errorf("expected video track ID %s, got %s", VideoTrackID, tracks.VideoTrack.ID())
	}
	if tracks.VideoTrack.StreamID() != VideoStreamID {
		t.Errorf("expected video stream ID %s, got %s", VideoStreamID, tracks.VideoTrack.StreamID())
	}

	if tracks.AudioTrack.ID() != AudioTrackID {
		t.Errorf("expected audio track ID %s, got %s", AudioTrackID, tracks.AudioTrack.ID())
	}
	if tracks.AudioTrack.StreamID() != AudioStreamID {
		t.Errorf("expected audio stream ID %s, got %s", AudioStreamID, tracks.AudioTrack.StreamID())
	}

	// Verify sample writing interface compatibility
	var vSource VideoSampleSource = tracks
	var aSource AudioSampleSource = tracks
	if vSource == nil || aSource == nil {
		t.Errorf("tracks do not satisfy sample source interfaces")
	}
}

// TestDataChannelLabels verifies the outbound DataChannels and their properties under both cameraSupport true and false.
func TestDataChannelLabels(t *testing.T) {
	api, err := NewAPIWithEvidenceBoundEngine()
	if err != nil {
		t.Fatalf("failed to create API: %v", err)
	}

	// 1. cameraSupport = true
	{
		pc, err := api.NewPeerConnection(BuildRTCConfiguration(nil))
		if err != nil {
			t.Fatalf("failed to create PC: %v", err)
		}
		defer pc.Close()

		dc := NewDataChannels()
		if err := dc.SetupOutboundChannels(pc, true); err != nil {
			t.Fatalf("failed to setup outbound channels: %v", err)
		}

		if dc.InputChannel == nil || dc.InputChannel.Label() != ChannelInput {
			t.Errorf("expected %s to be created", ChannelInput)
		}
		if dc.ClipboardChannel == nil || dc.ClipboardChannel.Label() != ChannelClipboard {
			t.Errorf("expected %s to be created", ChannelClipboard)
		}
		if dc.CameraChannel == nil || dc.CameraChannel.Label() != ChannelCamera {
			t.Errorf("expected %s to be created when cameraSupport=true", ChannelCamera)
		}

		if !dc.InputChannel.Ordered() || !dc.ClipboardChannel.Ordered() || !dc.CameraChannel.Ordered() {
			t.Errorf("all outbound channels must have ordered=true")
		}
	}

	// 2. cameraSupport = false
	{
		pc, err := api.NewPeerConnection(BuildRTCConfiguration(nil))
		if err != nil {
			t.Fatalf("failed to create PC: %v", err)
		}
		defer pc.Close()

		dc := NewDataChannels()
		if err := dc.SetupOutboundChannels(pc, false); err != nil {
			t.Fatalf("failed to setup outbound channels: %v", err)
		}

		if dc.InputChannel == nil || dc.InputChannel.Label() != ChannelInput {
			t.Errorf("expected %s to be created", ChannelInput)
		}
		if dc.ClipboardChannel == nil || dc.ClipboardChannel.Label() != ChannelClipboard {
			t.Errorf("expected %s to be created", ChannelClipboard)
		}
		if dc.CameraChannel != nil {
			t.Errorf("camera-channel MUST NOT be created when cameraSupport=false")
		}
	}
}

// TestPeerSessionOfferCreation validates offer SDP generation, local description, and camera support flag for both true and false.
func TestPeerSessionOfferCreation(t *testing.T) {
	// 1. CameraSupport = true
	{
		session, err := NewPeerSessionWithOptions(PeerSessionOptions{
			ClientID:      101,
			DeviceID:      "dev-test-1",
			CameraSupport: true,
			CameraConfig:  DefaultCameraConfig(),
		})
		if err != nil {
			t.Fatalf("failed to create peer session: %v", err)
		}
		defer session.Close()

		if session.GetState() != SessionStateConnecting {
			t.Errorf("expected state %v, got %v", SessionStateConnecting, session.GetState())
		}

		offerPayload, err := session.CreateOffer()
		if err != nil {
			t.Fatalf("failed to create offer: %v", err)
		}

		if offerPayload.Type != "offer" {
			t.Errorf("expected type offer, got %s", offerPayload.Type)
		}
		if offerPayload.CameraSupport == nil || *offerPayload.CameraSupport != true {
			t.Errorf("expected camera_support=true in offer payload")
		}
		if session.Channels.CameraChannel == nil {
			t.Errorf("expected camera-channel to be created when CameraSupport=true")
		}
		if !strings.Contains(offerPayload.SDP, "m=video") {
			t.Errorf("offer SDP missing m=video section")
		}
		if !strings.Contains(offerPayload.SDP, "m=audio") {
			t.Errorf("offer SDP missing m=audio section")
		}
		if !strings.Contains(offerPayload.SDP, "display_0") {
			t.Errorf("offer SDP missing display_0 track identifier")
		}
		if !strings.Contains(offerPayload.SDP, "audio_0") {
			t.Errorf("offer SDP missing audio_0 track identifier")
		}
		if session.GetState() != SessionStateHaveLocalOffer {
			t.Errorf("expected state %v, got %v", SessionStateHaveLocalOffer, session.GetState())
		}
	}

	// 2. CameraSupport = false
	{
		session, err := NewPeerSessionWithOptions(PeerSessionOptions{
			ClientID:      102,
			DeviceID:      "dev-test-1-nocam",
			CameraSupport: false,
			CameraConfig:  DefaultCameraConfig(),
		})
		if err != nil {
			t.Fatalf("failed to create peer session: %v", err)
		}
		defer session.Close()

		offerPayload, err := session.CreateOffer()
		if err != nil {
			t.Fatalf("failed to create offer: %v", err)
		}

		if offerPayload.CameraSupport == nil || *offerPayload.CameraSupport != false {
			t.Errorf("expected camera_support=false in offer payload")
		}
		if session.Channels.CameraChannel != nil {
			t.Errorf("camera-channel MUST NOT be created when CameraSupport=false")
		}
	}
}

// TestPeerSessionIdempotentClose validates concurrent close safety.
func TestPeerSessionIdempotentClose(t *testing.T) {
	session, err := NewPeerSession(102, "dev-test-2", nil)
	if err != nil {
		t.Fatalf("failed to create peer session: %v", err)
	}

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			_ = session.Close()
		}()
	}
	wg.Wait()

	if session.GetState() != SessionStateClosed {
		t.Errorf("expected closed state, got %v", session.GetState())
	}

	// Late operations should return ErrSessionClosed
	if _, err := session.CreateOffer(); err != ErrSessionClosed {
		t.Errorf("expected ErrSessionClosed, got %v", err)
	}
	if err := session.HandleRemoteAnswer("v=0..."); err != ErrSessionClosed {
		t.Errorf("expected ErrSessionClosed, got %v", err)
	}
	if err := session.AddRemoteCandidate(webrtc.ICECandidateInit{Candidate: "cand"}); err != ErrSessionClosed {
		t.Errorf("expected ErrSessionClosed, got %v", err)
	}
}

// TestSessionStateTransitions validates observable lifecycle transitions.
func TestSessionStateTransitions(t *testing.T) {
	session, err := NewPeerSession(103, "dev-test-3", nil)
	if err != nil {
		t.Fatalf("failed to create peer session: %v", err)
	}
	defer session.Close()

	var states []SessionState
	var mu sync.Mutex
	session.OnSessionStateChange(func(s SessionState) {
		mu.Lock()
		states = append(states, s)
		mu.Unlock()
	})

	_, err = session.CreateOffer()
	if err != nil {
		t.Fatalf("failed to create offer: %v", err)
	}

	// Verify state stringer
	if SessionStateHaveLocalOffer.String() != "HaveLocalOffer" {
		t.Errorf("unexpected string representation: %s", SessionStateHaveLocalOffer.String())
	}

	_ = session.Close()
	time.Sleep(20 * time.Millisecond)

	mu.Lock()
	defer mu.Unlock()
	// Should have recorded Closed state
	hasClosed := false
	for _, s := range states {
		if s == SessionStateClosed {
			hasClosed = true
		}
	}
	if !hasClosed {
		t.Errorf("expected to observe SessionStateClosed in transitions")
	}
}

// TestConcurrencyEdgeCases tests the mandatory concurrency edge cases:
// 1. Simultaneous ICE callbacks
// 2. Duplicate Close()
// 3. Late ICE candidate after cleanup
// 4. Remote answer arriving after teardown
func TestConcurrencyEdgeCases(t *testing.T) {
	session, err := NewPeerSession(104, "dev-test-conc", nil)
	if err != nil {
		t.Fatalf("failed to create session: %v", err)
	}

	_, err = session.CreateOffer()
	if err != nil {
		t.Fatalf("failed to create offer: %v", err)
	}

	// 1. Simultaneous ICE callbacks from multiple goroutines
	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			mid := "0"
			mline := uint16(0)
			_ = session.AddRemoteCandidate(webrtc.ICECandidateInit{
				Candidate:     "candidate:dummy",
				SDPMid:        &mid,
				SDPMLineIndex: &mline,
			})
		}(i)
	}
	wg.Wait()

	// 2. Teardown session
	if err := session.Close(); err != nil {
		t.Errorf("expected clean close: %v", err)
	}

	// Duplicate Close() must be idempotent and race-free
	for i := 0; i < 5; i++ {
		_ = session.Close()
	}

	// 3. Late ICE candidate after cleanup must return ErrSessionClosed without panic
	lateCandErr := session.AddRemoteCandidate(webrtc.ICECandidateInit{Candidate: "late-cand"})
	if lateCandErr != ErrSessionClosed {
		t.Errorf("expected ErrSessionClosed for late candidate, got: %v", lateCandErr)
	}

	// 4. Remote answer arriving after teardown must return ErrSessionClosed without panic
	lateAnsErr := session.HandleRemoteAnswer("v=0\r\no=- 0 0 IN IP4 127.0.0.1\r\n")
	if lateAnsErr != ErrSessionClosed {
		t.Errorf("expected ErrSessionClosed for late answer, got: %v", lateAnsErr)
	}
}

