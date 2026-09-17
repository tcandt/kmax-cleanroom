// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Mapping Scope: WEBRTC_FILE_DATACHANNEL_RECONSTRUCTION
// Evidence:
//   DATACHANNEL_LABEL_EVIDENCE.json (confirmed_webrtc_channels.file-channel: INBOUND_CLIENT_CREATED, ordered=true)
//   DATACHANNEL_FRAMING_MATRIX.json (channels.file-channel: HYBRID_METADATA_JSON_AND_BINARY_CHUNKS)
//   DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (file_channel_messages.start_upload: filename, size, sha256, install)
//   STRINGS.json (log strings for FileChannel and disassembly xrefs)
//   useWebRTC.js:1361-1385 (sendFileChannelCmd, sendFileChannelChunk)
// Disassembly:
//   AMD64 0x9e2f40 (OnDataChannel callback dispatch 0x9e2f20)
//   ARM64 0x53f234 (OnDataChannel callback dispatch 0x53f210)
//   AMD64 0x9e9ab1 (start_upload format string log)
// Note: Behavioral and protocol reconstruction; does NOT claim literal original Go source recovery.
// Confidence: HIGH

package webrtc

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"github.com/pion/webrtc/v3"
)

// DefaultDestinationDir is the confirmed destination staging path in original binary disassembly.
// Classification: STATIC_CONFIRMED.
const DefaultDestinationDir = "/data/local/tmp"

// CmdStartUpload is the discriminator for file upload initiation.
// Classification: STATIC_CONFIRMED.
const CmdStartUpload = "start_upload"

// FileTransferState represents the explicit lifecycle states of the file upload session.
// Classification: IMPLEMENTATION_CHOICE.
type FileTransferState string

const (
	FileTransferStateIdle             FileTransferState = "IDLE"
	FileTransferStateMetadataAccepted FileTransferState = "METADATA_ACCEPTED"
	FileTransferStateReceiving        FileTransferState = "RECEIVING"
	FileTransferStateComplete         FileTransferState = "COMPLETE"
	FileTransferStateError            FileTransferState = "ERROR"
)

// FileMetadata represents the JSON start_upload frame.
// Classification: STATIC_CONFIRMED (disassembly AMD64 0x9e9ab1, useWebRTC.js:1366).
type FileMetadata struct {
	Type     string `json:"type"`
	Filename string `json:"filename"`
	Size     int64  `json:"size"`
	SHA256   string `json:"sha256"`
	Install  bool   `json:"install"`
}

// FileSink abstracts the destination storage for clean-room testing and sandboxing.
// Classification: IMPLEMENTATION_CHOICE.
type FileSink interface {
	Begin(metadata FileMetadata) error
	WriteChunk(chunk []byte) error
	Complete() error
	Abort() error
}

// PostUploadActionHandler defines an event callback triggered when an upload completes
// with metadata.Install == true.
// Classification: IMPLEMENTATION_CHOICE.
type PostUploadActionHandler func(metadata FileMetadata, targetPath string)

// SanitizeFilename hardens against directory traversal (../), absolute root paths,
// Windows drive letters, UNC shares, and NUL bytes.
// Classification: IMPLEMENTATION_CHOICE.
func SanitizeFilename(filename string) (string, error) {
	// Strip NUL bytes
	if strings.ContainsRune(filename, 0) {
		return "", errors.New("filename contains NUL character")
	}

	// Normalize backslashes to slashes
	cleaned := strings.ReplaceAll(filename, "\\", "/")

	// Strip Windows drive letters (e.g., C:/...)
	if len(cleaned) >= 2 && cleaned[1] == ':' && ((cleaned[0] >= 'a' && cleaned[0] <= 'z') || (cleaned[0] >= 'A' && cleaned[0] <= 'Z')) {
		cleaned = cleaned[2:]
	}

	// Take only the base component
	base := filepath.Base(filepath.Clean(cleaned))
	if base == "." || base == "/" || base == "\\" || base == ".." || base == "" {
		return "", errors.New("invalid or empty filename after sanitization")
	}

	// Double check no path separators remain
	if strings.ContainsAny(base, "/\\:") {
		return "", errors.New("filename contains path separators")
	}

	return base, nil
}

// MemoryFileSink is an in-memory test double avoiding host filesystem modification.
// Classification: IMPLEMENTATION_CHOICE.
type MemoryFileSink struct {
	mu        sync.Mutex
	Metadata  FileMetadata
	Buffer    bytes.Buffer
	Completed bool
	Aborted   bool
}

// NewMemoryFileSink creates an in-memory FileSink.
func NewMemoryFileSink() *MemoryFileSink {
	return &MemoryFileSink{}
}

func (s *MemoryFileSink) Begin(metadata FileMetadata) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.Metadata = metadata
	s.Buffer.Reset()
	s.Completed = false
	s.Aborted = false
	return nil
}

func (s *MemoryFileSink) WriteChunk(chunk []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.Aborted {
		return errors.New("write to aborted sink")
	}
	_, err := s.Buffer.Write(chunk)
	return err
}

func (s *MemoryFileSink) Complete() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.Completed = true
	return nil
}

func (s *MemoryFileSink) Abort() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.Aborted = true
	return nil
}

func (s *MemoryFileSink) GetBytes() []byte {
	s.mu.Lock()
	defer s.mu.Unlock()
	copied := make([]byte, s.Buffer.Len())
	copy(copied, s.Buffer.Bytes())
	return copied
}

func (s *MemoryFileSink) IsCompleted() bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.Completed
}

func (s *MemoryFileSink) IsAborted() bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.Aborted
}

// LocalFileSink writes to a sandbox directory with strict path sanitization.
// Classification: IMPLEMENTATION_CHOICE.
type LocalFileSink struct {
	mu          sync.Mutex
	BaseDir     string
	currentFile *os.File
	targetPath  string
	metadata    FileMetadata
}

// NewLocalFileSink creates a FileSink targeting baseDir.
func NewLocalFileSink(baseDir string) (*LocalFileSink, error) {
	if baseDir == "" {
		baseDir = DefaultDestinationDir
	}
	return &LocalFileSink{
		BaseDir: baseDir,
	}, nil
}

func (s *LocalFileSink) Begin(metadata FileMetadata) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	safeName, err := SanitizeFilename(metadata.Filename)
	if err != nil {
		return fmt.Errorf("invalid filename: %w", err)
	}

	target := filepath.Join(s.BaseDir, safeName)
	f, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
	if err != nil {
		log.Printf("[FileChannel] Failed to create upload file %s: %v", target, err)
		return fmt.Errorf("failed to create upload file: %w", err)
	}

	s.currentFile = f
	s.targetPath = target
	s.metadata = metadata
	return nil
}

func (s *LocalFileSink) WriteChunk(chunk []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.currentFile == nil {
		return errors.New("no active file for write")
	}

	_, err := s.currentFile.Write(chunk)
	if err != nil {
		log.Printf("[FileChannel] Error writing to file: %v", err)
		return err
	}
	return nil
}

func (s *LocalFileSink) Complete() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.currentFile != nil {
		_ = s.currentFile.Sync()
		_ = s.currentFile.Close()
		s.currentFile = nil
	}
	return nil
}

func (s *LocalFileSink) Abort() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.currentFile != nil {
		_ = s.currentFile.Close()
		s.currentFile = nil
		if s.targetPath != "" {
			_ = os.Remove(s.targetPath)
		}
	}
	return nil
}

func (s *LocalFileSink) TargetPath() string {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.targetPath
}

// FileChannelHandler manages file-channel message state transitions, checksumming, and sink dispatch.
// Classification: RECONSTRUCTED_FROM_BINARY.
type FileChannelHandler struct {
	mu            sync.Mutex
	sink          FileSink
	postAction    PostUploadActionHandler
	state         FileTransferState
	metadata      FileMetadata
	receivedBytes int64
	hasher        io.Writer
	hashSummer    interface{ Sum([]byte) []byte }
}

// NewFileChannelHandler initializes a new FileChannelHandler.
// Classification: GENERATED_ADAPTER.
func NewFileChannelHandler(sink FileSink, postAction PostUploadActionHandler) *FileChannelHandler {
	return &FileChannelHandler{
		sink:       sink,
		postAction: postAction,
		state:      FileTransferStateIdle,
	}
}

// GetState returns the current transfer lifecycle state.
func (h *FileChannelHandler) GetState() FileTransferState {
	h.mu.Lock()
	defer h.mu.Unlock()
	return h.state
}

// GetReceivedBytes returns the total bytes accumulated so far.
func (h *FileChannelHandler) GetReceivedBytes() int64 {
	h.mu.Lock()
	defer h.mu.Unlock()
	return h.receivedBytes
}

// HandleMessage handles an incoming DataChannel message (JSON text or binary chunk).
// Classification: RECONSTRUCTED_FROM_BINARY.
func (h *FileChannelHandler) HandleMessage(data []byte, isString bool) (err error) {
	defer func() {
		if r := recover(); r != nil {
			log.Printf("[FileChannel] OnMessage PANIC recovered: %v", r)
			err = fmt.Errorf("recovered panic: %v", r)
		}
	}()

	h.mu.Lock()
	defer h.mu.Unlock()

	// 1. Text Framing: start_upload metadata JSON
	if isString || (h.state == FileTransferStateIdle && len(data) > 0 && data[0] == '{') {
		var meta FileMetadata
		if parseErr := json.Unmarshal(data, &meta); parseErr != nil {
			log.Printf("[FileChannel] Failed to parse control msg: %v", parseErr)
			return fmt.Errorf("failed to parse control msg: %w", parseErr)
		}

		if meta.Type != CmdStartUpload {
			log.Printf("[FileChannel] Unexpected command: %s", meta.Type)
			return fmt.Errorf("unexpected command type: %s", meta.Type)
		}

		if meta.Filename == "" {
			return errors.New("empty filename in start_upload")
		}
		if meta.Size < 0 {
			return errors.New("negative size in start_upload")
		}

		// Disallow duplicate metadata unless previous transfer completed
		if h.state != FileTransferStateIdle && h.state != FileTransferStateComplete {
			if h.sink != nil {
				_ = h.sink.Abort()
			}
			h.state = FileTransferStateError
			return errors.New("duplicate start_upload before previous transfer completion")
		}

		log.Printf("[FileChannel] Start uploading to %s (size=%d, sha256=%s, install=%v)",
			meta.Filename, meta.Size, meta.SHA256, meta.Install)

		if h.sink != nil {
			if beginErr := h.sink.Begin(meta); beginErr != nil {
				h.state = FileTransferStateError
				return fmt.Errorf("sink begin failed: %w", beginErr)
			}
		}

		h.metadata = meta
		h.receivedBytes = 0
		hasher := sha256.New()
		h.hasher = hasher
		h.hashSummer = hasher

		// Handle zero-byte file immediately
		if meta.Size == 0 {
			computedHash := hex.EncodeToString(hasher.Sum(nil))
			if meta.SHA256 != "" && !strings.EqualFold(computedHash, meta.SHA256) {
				if h.sink != nil {
					_ = h.sink.Abort()
				}
				h.state = FileTransferStateError
				log.Printf("[FileChannel] Upload integrity check FAILED: hash mismatch on empty file")
				return errors.New("upload integrity check failed: hash mismatch")
			}
			if h.sink != nil {
				if compErr := h.sink.Complete(); compErr != nil {
					h.state = FileTransferStateError
					return compErr
				}
			}
			h.state = FileTransferStateComplete
			log.Printf("[FileChannel] SHA-256 integrity check passed: %s", computedHash)
			log.Printf("[FileChannel] Upload finished: %s (%d bytes)", meta.Filename, 0)
			if meta.Install && h.postAction != nil {
				h.postAction(meta, meta.Filename)
			}
			return nil
		}

		h.state = FileTransferStateMetadataAccepted
		return nil
	}

	// 2. Binary Framing: streaming raw chunk
	if h.state != FileTransferStateMetadataAccepted && h.state != FileTransferStateReceiving {
		if h.sink != nil {
			_ = h.sink.Abort()
		}
		h.state = FileTransferStateError
		return errors.New("binary chunk received without accepted metadata")
	}

	h.state = FileTransferStateReceiving
	chunkLen := int64(len(data))

	// Check size overflow
	if h.receivedBytes+chunkLen > h.metadata.Size {
		if h.sink != nil {
			_ = h.sink.Abort()
		}
		h.state = FileTransferStateError
		return fmt.Errorf("received bytes (%d) exceeds declared size (%d)", h.receivedBytes+chunkLen, h.metadata.Size)
	}

	// Update streaming SHA-256
	if h.hasher != nil {
		if _, writeErr := h.hasher.Write(data); writeErr != nil {
			if h.sink != nil {
				_ = h.sink.Abort()
			}
			h.state = FileTransferStateError
			return writeErr
		}
	}

	// Dispatch to FileSink
	if h.sink != nil {
		if sinkErr := h.sink.WriteChunk(data); sinkErr != nil {
			_ = h.sink.Abort()
			h.state = FileTransferStateError
			return fmt.Errorf("sink write chunk failed: %w", sinkErr)
		}
	}

	h.receivedBytes += chunkLen

	// Check for completion
	if h.receivedBytes == h.metadata.Size {
		var computedHash string
		if h.hashSummer != nil {
			computedHash = hex.EncodeToString(h.hashSummer.Sum(nil))
		}

		if h.metadata.SHA256 != "" && !strings.EqualFold(computedHash, h.metadata.SHA256) {
			if h.sink != nil {
				_ = h.sink.Abort()
			}
			h.state = FileTransferStateError
			log.Printf("[FileChannel] Upload integrity check FAILED: expected %s, got %s", h.metadata.SHA256, computedHash)
			return fmt.Errorf("checksum mismatch: expected %s, got %s", h.metadata.SHA256, computedHash)
		}

		if h.sink != nil {
			if compErr := h.sink.Complete(); compErr != nil {
				h.state = FileTransferStateError
				return compErr
			}
		}

		h.state = FileTransferStateComplete
		log.Printf("[FileChannel] SHA-256 integrity check passed: %s", computedHash)
		log.Printf("[FileChannel] Upload finished: %s (%d bytes)", h.metadata.Filename, h.receivedBytes)

		// Post-upload boundary (installer execution strictly deferred)
		if h.metadata.Install && h.postAction != nil {
			h.postAction(h.metadata, h.metadata.Filename)
		}
	}

	return nil
}

// Attach binds the FileChannelHandler to a Pion DataChannel OnMessage callback.
// Classification: GENERATED_ADAPTER.
func (h *FileChannelHandler) Attach(dc *webrtc.DataChannel) {
	if dc == nil {
		return
	}
	dc.OnMessage(func(msg webrtc.DataChannelMessage) {
		_ = h.HandleMessage(msg.Data, msg.IsString)
	})
}

// RegisterFileChannel binds the FileChannelHandler to incoming file-channel instances on a PeerSession.
// Classification: GENERATED_ADAPTER.
func RegisterFileChannel(session *PeerSession, handler *FileChannelHandler) {
	if session == nil || session.PC == nil || handler == nil {
		return
	}

	session.PC.OnDataChannel(func(remoteDC *webrtc.DataChannel) {
		label := remoteDC.Label()
		attachInertLifecycleHooks(remoteDC)

		if label == ChannelFile {
			handler.Attach(remoteDC)
		}

		if session.Channels != nil {
			session.Channels.mu.Lock()
			switch label {
			case ChannelFile:
				session.Channels.FileChannel = remoteDC
			case ChannelAICommand:
				session.Channels.AICommandChannel = remoteDC
			case ChannelADB:
				session.Channels.ADBChannel = remoteDC
			}
			session.Channels.mu.Unlock()
		}
	})
}
