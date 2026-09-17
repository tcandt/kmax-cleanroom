// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_TEST
// Mapping Scope: WEBRTC_FILE_DATACHANNEL_TEST_SUITE
// Evidence:
//   DATACHANNEL_LABEL_EVIDENCE.json (confirmed_webrtc_channels.file-channel)
//   DATACHANNEL_FRAMING_MATRIX.json (channels.file-channel: HYBRID_METADATA_JSON_AND_BINARY_CHUNKS)
//   DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (file_channel_messages.start_upload)
//   STRINGS.json (log strings for FileChannel and disassembly xrefs)

package webrtc

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

// TestFileChannelMetadataParsing verifies start_upload JSON parsing and validation.
func TestFileChannelMetadataParsing(t *testing.T) {
	sink := NewMemoryFileSink()
	h := NewFileChannelHandler(sink, nil)

	// 1. Valid start_upload
	validJSON := `{"type":"start_upload","filename":"test.apk","size":1024,"sha256":"abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890","install":true}`
	if err := h.HandleMessage([]byte(validJSON), true); err != nil {
		t.Fatalf("expected valid start_upload to succeed, got: %v", err)
	}
	if h.GetState() != FileTransferStateMetadataAccepted {
		t.Fatalf("expected state METADATA_ACCEPTED, got: %s", h.GetState())
	}

	// 2. Reject duplicate start_upload before completion
	if err := h.HandleMessage([]byte(validJSON), true); err == nil {
		t.Fatalf("expected duplicate start_upload to fail")
	}
	if h.GetState() != FileTransferStateError {
		t.Fatalf("expected state ERROR after duplicate metadata, got: %s", h.GetState())
	}

	// 3. Reset and test missing/empty filename
	h2 := NewFileChannelHandler(NewMemoryFileSink(), nil)
	emptyName := `{"type":"start_upload","filename":"","size":100,"sha256":"abc","install":false}`
	if err := h2.HandleMessage([]byte(emptyName), true); err == nil {
		t.Fatalf("expected empty filename to fail")
	}

	// 4. Negative size
	h3 := NewFileChannelHandler(NewMemoryFileSink(), nil)
	negSize := `{"type":"start_upload","filename":"app.apk","size":-5,"sha256":"abc","install":false}`
	if err := h3.HandleMessage([]byte(negSize), true); err == nil {
		t.Fatalf("expected negative size to fail")
	}

	// 5. Wrong command type
	h4 := NewFileChannelHandler(NewMemoryFileSink(), nil)
	wrongType := `{"type":"stop_upload","filename":"app.apk","size":100,"sha256":"abc","install":false}`
	if err := h4.HandleMessage([]byte(wrongType), true); err == nil {
		t.Fatalf("expected non-start_upload command to fail")
	}

	// 6. Malformed JSON
	h5 := NewFileChannelHandler(NewMemoryFileSink(), nil)
	malformed := `{"type":"start_upload", filename: invalid}`
	if err := h5.HandleMessage([]byte(malformed), true); err == nil {
		t.Fatalf("expected malformed JSON to fail")
	}
}

// TestFileChannelTransferFlow verifies single-chunk and multi-chunk file transfer with exact byte parity.
func TestFileChannelTransferFlow(t *testing.T) {
	testCases := []struct {
		name       string
		totalSize  int
		chunkSizes []int
	}{
		{"single_chunk_small", 64, []int{64}},
		{"multi_chunk_exact", 1024, []int{256, 256, 256, 256}},
		{"multi_chunk_irregular", 1500, []int{512, 512, 476}},
		{"multi_chunk_large", 65536, []int{16384, 16384, 16384, 16384}},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			payload := make([]byte, tc.totalSize)
			_, _ = rand.Read(payload)

			hExpected := sha256.Sum256(payload)
			shaHex := hex.EncodeToString(hExpected[:])

			sink := NewMemoryFileSink()
			var postActionCalled bool
			h := NewFileChannelHandler(sink, func(meta FileMetadata, path string) error {
				postActionCalled = true
				return nil
			})

			metaJSON := fmt.Sprintf(`{"type":"start_upload","filename":"%s.bin","size":%d,"sha256":"%s","install":true}`,
				tc.name, tc.totalSize, shaHex)

			if err := h.HandleMessage([]byte(metaJSON), true); err != nil {
				t.Fatalf("failed to send metadata: %v", err)
			}

			offset := 0
			for i, chunkSize := range tc.chunkSizes {
				chunk := payload[offset : offset+chunkSize]
				offset += chunkSize

				if err := h.HandleMessage(chunk, false); err != nil {
					t.Fatalf("chunk %d failed: %v", i, err)
				}
			}

			if h.GetState() != FileTransferStateComplete {
				t.Fatalf("expected state COMPLETE, got: %s", h.GetState())
			}

			if !sink.IsCompleted() {
				t.Fatalf("expected sink.Completed to be true")
			}

			reconstructed := sink.GetBytes()
			if !bytes.Equal(reconstructed, payload) {
				t.Fatalf("payload mismatch! Expected %d bytes, got %d bytes", len(payload), len(reconstructed))
			}

			if !postActionCalled {
				t.Fatalf("expected postUploadAction to be invoked for install=true")
			}
		})
	}
}

// TestFileChannelZeroByteUpload verifies zero-byte upload completes immediately.
func TestFileChannelZeroByteUpload(t *testing.T) {
	sink := NewMemoryFileSink()
	var postActionCalled bool
	h := NewFileChannelHandler(sink, func(meta FileMetadata, path string) error {
		postActionCalled = true
		return nil
	})

	emptyHash := sha256.Sum256([]byte{})
	emptyHex := hex.EncodeToString(emptyHash[:])

	metaJSON := fmt.Sprintf(`{"type":"start_upload","filename":"empty.txt","size":0,"sha256":"%s","install":true}`, emptyHex)
	if err := h.HandleMessage([]byte(metaJSON), true); err != nil {
		t.Fatalf("failed zero-byte upload metadata: %v", err)
	}

	if h.GetState() != FileTransferStateComplete {
		t.Fatalf("expected state COMPLETE for zero-byte upload, got: %s", h.GetState())
	}

	if !sink.IsCompleted() {
		t.Fatalf("expected sink to be completed")
	}

	if len(sink.GetBytes()) != 0 {
		t.Fatalf("expected 0 bytes in sink, got: %d", len(sink.GetBytes()))
	}

	if !postActionCalled {
		t.Fatalf("expected postAction to be called")
	}
}

// TestFileChannelChecksumMismatch verifies integrity check failure aborts the transfer.
func TestFileChannelChecksumMismatch(t *testing.T) {
	payload := []byte("corrupted payload content")
	correctHash := sha256.Sum256(payload)
	badHex := strings.Repeat("0", 64)
	if badHex == hex.EncodeToString(correctHash[:]) {
		badHex = strings.Repeat("1", 64)
	}

	sink := NewMemoryFileSink()
	var postActionCalled bool
	h := NewFileChannelHandler(sink, func(meta FileMetadata, path string) error {
		postActionCalled = true
		return nil
	})

	metaJSON := fmt.Sprintf(`{"type":"start_upload","filename":"corrupt.bin","size":%d,"sha256":"%s","install":true}`,
		len(payload), badHex)

	if err := h.HandleMessage([]byte(metaJSON), true); err != nil {
		t.Fatalf("failed metadata: %v", err)
	}

	err := h.HandleMessage(payload, false)
	if err == nil {
		t.Fatalf("expected checksum mismatch error, got nil")
	}

	if !strings.Contains(err.Error(), "hash mismatch") && !strings.Contains(err.Error(), "checksum mismatch") {
		t.Fatalf("expected hash mismatch error message, got: %v", err)
	}

	if h.GetState() != FileTransferStateError {
		t.Fatalf("expected state ERROR, got: %s", h.GetState())
	}

	if !sink.IsAborted() {
		t.Fatalf("expected sink to be aborted on checksum mismatch")
	}

	if postActionCalled {
		t.Fatalf("postAction must not be called on checksum mismatch")
	}
}

// TestFileChannelSizeMismatch verifies short uploads and oversized chunks are caught.
func TestFileChannelSizeMismatch(t *testing.T) {
	// 1. Oversized chunk triggers overflow error
	sink1 := NewMemoryFileSink()
	h1 := NewFileChannelHandler(sink1, nil)
	meta1 := `{"type":"start_upload","filename":"overflow.bin","size":100,"sha256":"","install":false}`
	if err := h1.HandleMessage([]byte(meta1), true); err != nil {
		t.Fatalf("metadata failed: %v", err)
	}

	overflowChunk := make([]byte, 101)
	err := h1.HandleMessage(overflowChunk, false)
	if err == nil {
		t.Fatalf("expected overflow error")
	}
	if h1.GetState() != FileTransferStateError {
		t.Fatalf("expected state ERROR on overflow")
	}
	if !sink1.IsAborted() {
		t.Fatalf("expected sink aborted on overflow")
	}

	// 2. Short upload leaves state in RECEIVING (incomplete)
	sink2 := NewMemoryFileSink()
	h2 := NewFileChannelHandler(sink2, nil)
	meta2 := `{"type":"start_upload","filename":"short.bin","size":100,"sha256":"","install":false}`
	if err := h2.HandleMessage([]byte(meta2), true); err != nil {
		t.Fatalf("metadata failed: %v", err)
	}

	shortChunk := make([]byte, 50)
	if err := h2.HandleMessage(shortChunk, false); err != nil {
		t.Fatalf("short chunk failed: %v", err)
	}

	if h2.GetState() != FileTransferStateReceiving {
		t.Fatalf("expected state RECEIVING for partial upload, got: %s", h2.GetState())
	}
	if h2.GetReceivedBytes() != 50 {
		t.Fatalf("expected 50 received bytes, got: %d", h2.GetReceivedBytes())
	}
	if sink2.IsCompleted() {
		t.Fatalf("sink must not be completed for partial upload")
	}
}

// TestFileChannelStateViolations verifies illegal message sequences fail closed.
func TestFileChannelStateViolations(t *testing.T) {
	// Binary chunk before metadata
	sink := NewMemoryFileSink()
	h := NewFileChannelHandler(sink, nil)

	err := h.HandleMessage([]byte("orphan binary chunk"), false)
	if err == nil {
		t.Fatalf("expected error for binary chunk before metadata")
	}
	if h.GetState() != FileTransferStateError {
		t.Fatalf("expected state ERROR, got: %s", h.GetState())
	}
}

// TestFileChannelStrictFraming verifies strict distinction between text metadata and binary data frames.
func TestFileChannelStrictFraming(t *testing.T) {
	sink := NewMemoryFileSink()
	h := NewFileChannelHandler(sink, nil)

	// 1. Binary frame attempting to transmit start_upload JSON in IDLE state must be rejected
	binaryMeta := []byte(`{"type":"start_upload","filename":"test.bin","size":10,"sha256":""}`)
	err := h.HandleMessage(binaryMeta, false) // isString == false
	if err == nil {
		t.Fatalf("expected error when sending JSON metadata as binary frame")
	}
	if h.GetState() != FileTransferStateError {
		t.Fatalf("expected state ERROR when binary frame received in IDLE, got: %s", h.GetState())
	}

	// 2. Text frame containing metadata accepted in IDLE state
	h2 := NewFileChannelHandler(NewMemoryFileSink(), nil)
	textMeta := `{"type":"start_upload","filename":"test.bin","size":10,"sha256":""}`
	if err := h2.HandleMessage([]byte(textMeta), true); err != nil {
		t.Fatalf("unexpected error on text metadata: %v", err)
	}
	if h2.GetState() != FileTransferStateMetadataAccepted {
		t.Fatalf("expected METADATA_ACCEPTED, got: %s", h2.GetState())
	}

	// 3. Text frame sent during RECEIVING state must be rejected (must be binary)
	err = h2.HandleMessage([]byte("illegal text chunk"), true) // isString == true
	if err == nil {
		t.Fatalf("expected error when sending text frame during chunk transfer")
	}
	if h2.GetState() != FileTransferStateError {
		t.Fatalf("expected state ERROR after text chunk violation, got: %s", h2.GetState())
	}
}

// TestPathSanitizationDefensive tests directory traversal prevention.
func TestPathSanitizationDefensive(t *testing.T) {
	tests := []struct {
		input       string
		expected    string
		shouldError bool
	}{
		{"app.apk", "app.apk", false},
		{"simple_test_123.bin", "simple_test_123.bin", false},
		{"../etc/passwd", "passwd", false},
		{"../../../../system/bin/sh", "sh", false},
		{"C:\\Windows\\System32\\cmd.exe", "cmd.exe", false},
		{"D:/malicious/path/evil.apk", "evil.apk", false},
		{"\\\\server\\share\\evil.apk", "evil.apk", false},
		{"foo/bar/baz.apk", "baz.apk", false},
		{"foo\\bar\\baz.apk", "baz.apk", false},
		{"", "", true},
		{".", "", true},
		{"..", "", true},
		{"/", "", true},
		{"\\", "", true},
		{"test\x00evil.apk", "", true},
	}

	for _, tt := range tests {
		safeName, err := SanitizeFilename(tt.input)
		if tt.shouldError {
			if err == nil {
				t.Errorf("SanitizeFilename(%q) expected error, got: %q", tt.input, safeName)
			}
		} else {
			if err != nil {
				t.Errorf("SanitizeFilename(%q) unexpected error: %v", tt.input, err)
			}
			if safeName != tt.expected {
				t.Errorf("SanitizeFilename(%q) expected %q, got: %q", tt.input, tt.expected, safeName)
			}
			if strings.ContainsAny(safeName, "/\\:") {
				t.Errorf("SanitizeFilename(%q) returned name with separators: %q", tt.input, safeName)
			}
		}
	}
}

// TestLocalFileSinkTemporarySandbox verifies LocalFileSink writes only inside isolated sandbox.
func TestLocalFileSinkTemporarySandbox(t *testing.T) {
	tempDir := t.TempDir()
	sink := NewLocalFileSink(tempDir)

	meta := FileMetadata{
		Type:     CmdStartUpload,
		Filename: "sandboxed_test.bin",
		Size:     12,
		Install:  false,
	}

	if err := sink.Begin(meta); err != nil {
		t.Fatalf("sink.Begin failed: %v", err)
	}

	chunk := []byte("sandbox data")
	if err := sink.WriteChunk(chunk); err != nil {
		t.Fatalf("sink.WriteChunk failed: %v", err)
	}

	if err := sink.Complete(); err != nil {
		t.Fatalf("sink.Complete failed: %v", err)
	}

	writtenPath := filepath.Join(tempDir, "sandboxed_test.bin")
	content, err := os.ReadFile(writtenPath)
	if err != nil {
		t.Fatalf("failed to read sandbox written file: %v", err)
	}

	if !bytes.Equal(content, chunk) {
		t.Fatalf("written file content mismatch")
	}

	// Test Target method
	if sink.Target() != writtenPath {
		t.Fatalf("expected Target() %q, got %q", writtenPath, sink.Target())
	}

	// Test Abort removes active file
	sink2 := NewLocalFileSink(tempDir)
	meta2 := FileMetadata{
		Type:     CmdStartUpload,
		Filename: "aborted_test.bin",
		Size:     100,
	}
	_ = sink2.Begin(meta2)
	_ = sink2.WriteChunk([]byte("abort me"))
	_ = sink2.Abort()

	abortedPath := filepath.Join(tempDir, "aborted_test.bin")
	if _, err := os.Stat(abortedPath); !os.IsNotExist(err) {
		t.Fatalf("expected aborted file to be removed, but stat succeeded")
	}
}

// TestPostUploadActionBoundary verifies install flag boundary semantics and unambiguous target path.
func TestPostUploadActionBoundary(t *testing.T) {
	data := []byte("apk binary simulation")
	hSum := sha256.Sum256(data)
	hHex := hex.EncodeToString(hSum[:])

	// Case 1: MemoryFileSink with install=true invokes postAction with memory target
	var installTarget string
	h1 := NewFileChannelHandler(NewMemoryFileSink(), func(meta FileMetadata, target string) error {
		installTarget = target
		return nil
	})
	meta1 := fmt.Sprintf(`{"type":"start_upload","filename":"test.apk","size":%d,"sha256":"%s","install":true}`, len(data), hHex)
	_ = h1.HandleMessage([]byte(meta1), true)
	_ = h1.HandleMessage(data, false)

	if installTarget != "memory://test.apk" {
		t.Fatalf("expected postAction target 'memory://test.apk', got: %q", installTarget)
	}

	// Case 2: LocalFileSink with install=true invokes postAction with actual sandbox target path
	tempDir := t.TempDir()
	localSink := NewLocalFileSink(tempDir)
	var localTarget string
	hLocal := NewFileChannelHandler(localSink, func(meta FileMetadata, target string) error {
		localTarget = target
		return nil
	})
	_ = hLocal.HandleMessage([]byte(meta1), true)
	_ = hLocal.HandleMessage(data, false)

	expectedLocalPath := filepath.Join(tempDir, "test.apk")
	if localTarget != expectedLocalPath {
		t.Fatalf("expected postAction local target %q, got: %q", expectedLocalPath, localTarget)
	}

	// Case 3: install=false does NOT invoke postAction
	var installTarget2 string
	h2 := NewFileChannelHandler(NewMemoryFileSink(), func(meta FileMetadata, target string) error {
		installTarget2 = target
		return nil
	})
	meta2 := fmt.Sprintf(`{"type":"start_upload","filename":"test.apk","size":%d,"sha256":"%s","install":false}`, len(data), hHex)
	_ = h2.HandleMessage([]byte(meta2), true)
	_ = h2.HandleMessage(data, false)

	if installTarget2 != "" {
		t.Fatalf("postAction should not be called when install=false, got: %q", installTarget2)
	}
}

// TestFileChannelRobustnessAndFuzz guarantees zero panic under fuzzed/malformed inputs.
func TestFileChannelRobustnessAndFuzz(t *testing.T) {
	sink := NewMemoryFileSink()
	h := NewFileChannelHandler(sink, nil)

	fuzzInputs := [][]byte{
		nil,
		{},
		[]byte(""),
		[]byte("{"),
		[]byte("}"),
		[]byte(`{"type": null}`),
		[]byte(`{"type": 123}`),
		[]byte(`{"type": "start_upload", "size": "not_an_int"}`),
		bytes.Repeat([]byte("A"), 100000),
		{0x00, 0xFF, 0xFE, 0xFD},
	}

	for i, input := range fuzzInputs {
		t.Run(fmt.Sprintf("fuzz_%d", i), func(t *testing.T) {
			defer func() {
				if r := recover(); r != nil {
					t.Fatalf("panic on fuzz input %d: %v", i, r)
				}
			}()
			_ = h.HandleMessage(input, true)
			_ = h.HandleMessage(input, false)
		})
	}
}

// TestFileChannelConcurrentSafety runs concurrent calls without races.
func TestFileChannelConcurrentSafety(t *testing.T) {
	sink := NewMemoryFileSink()
	h := NewFileChannelHandler(sink, nil)

	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			_ = h.GetState()
			_ = h.GetReceivedBytes()
			_ = h.HandleMessage([]byte(fmt.Sprintf(`{"type":"invalid_%d"}`, idx)), true)
		}(i)
	}
	wg.Wait()
}
