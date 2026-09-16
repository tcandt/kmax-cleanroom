// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Target Binary: webrtc-signaling (Linux AMD64 SHA256: 6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3)
// Scope: Files Management & Local Storage
// Evidence: FILES_LIST_CONTRACT.json, FILE_PATH_SECURITY_CONTRACT.json, UPLOAD_OPERATION_CONTRACT.json
// Confidence: HIGH

package storage

import (
	"errors"
	"io"
	"os"
	"path/filepath"
	"sort"

	"cloudphone-signaling/pkg/types"
)

var (
	ErrPathTraversal = errors.New("Invalid file path (path traversal detected)")
	ErrMissingName   = errors.New("Missing name parameter")
)

// FileManager manages files in the downloads directory.
type FileManager struct {
	downloadsDir string
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Constructs a new FileManager bound to the specified downloads directory
// Source Behavior: Manages file storage and retrieval in downloads directory
// Confidence: HIGH
func NewFileManager(downloadsDir string) *FileManager {
	return &FileManager{
		downloadsDir: downloadsDir,
	}
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.main
// VA: 0x765c88
// Evidence: FILESYSTEM_ROOT_CONTRACT.json
// Purpose: Eagerly ensures that the downloads directory exists at startup
// Confidence: HIGH
func (fm *FileManager) EnsureDirectories() error {
	return os.MkdirAll(fm.downloadsDir, 0755)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.qa3RvDW
// VA: 0x75a2c0
// Evidence: FILES_LIST_CONTRACT.json, FILES_TYPE_EVIDENCE.json
// Purpose: Lists non-directory files from data/downloads sorted lexicographically
// Confidence: HIGH
func (fm *FileManager) ListFiles() ([]types.FileItem, error) {
	entries, err := os.ReadDir(fm.downloadsDir)
	if err != nil {
		if os.IsNotExist(err) {
			return []types.FileItem{}, nil
		}
		return nil, err
	}

	var items []types.FileItem
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		info, err := entry.Info()
		if err != nil {
			continue
		}
		items = append(items, types.FileItem{
			Name:      entry.Name(),
			Size:      info.Size(),
			UpdatedAt: info.ModTime().Format("2006-01-02T15:04:05.999999999-07:00"),
			URL:       "/downloads/" + entry.Name(),
		})
	}

	if items == nil {
		return []types.FileItem{}, nil
	}

	sort.Slice(items, func(i, j int) bool {
		return items[i].Name < items[j].Name
	})

	return items, nil
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.qa3RvDW
// VA: 0x75a8c5
// Evidence: FILES_LIST_CONTRACT.json, FILE_PATH_SECURITY_CONTRACT.json
// Purpose: Deletes a named file from data/downloads ensuring path containment
// Confidence: HIGH
func (fm *FileManager) DeleteFile(name string) error {
	if name == "" {
		return ErrMissingName
	}
	cleanBase := filepath.Base(filepath.Clean(name))
	if cleanBase == "." || cleanBase == ".." || cleanBase != name {
		return os.ErrNotExist
	}
	target := filepath.Join(fm.downloadsDir, cleanBase)
	info, err := os.Stat(target)
	if err != nil {
		return os.ErrNotExist
	}
	if info.IsDir() {
		return os.ErrNotExist
	}
	return os.Remove(target)
}

// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Binary Symbol: main.swqKgLrjAZT9
// VA: 0x758c80
// Evidence: UPLOAD_OPERATION_CONTRACT.json, FILE_PATH_SECURITY_CONTRACT.json
// Purpose: Saves an uploaded stream directly to data/downloads/<filename>
// Confidence: HIGH
func (fm *FileManager) SaveUploadedFile(name string, r io.Reader) (string, error) {
	if name == "" {
		return "", errors.New("Missing file name")
	}
	clean := filepath.Clean(name)
	base := filepath.Base(clean)
	if base == "." || base == ".." {
		return "", ErrPathTraversal
	}

	target := filepath.Join(fm.downloadsDir, base)
	out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0666)
	if err != nil {
		return "", err
	}
	defer out.Close()

	if _, err := io.Copy(out, r); err != nil {
		return "", err
	}
	return base, nil
}

// CLEANROOM-PROVENANCE:
// Classification: GENERATED_ADAPTER
// Mapping Scope: GENERATED_ADAPTER
// Original Function Mapping: NONE
// Purpose: Exposes the downloads directory path for static file server mounting
// Source Behavior: Returns filesystem path for http.FileServer
// Confidence: HIGH
func (fm *FileManager) DownloadsDir() string {
	return fm.downloadsDir
}
