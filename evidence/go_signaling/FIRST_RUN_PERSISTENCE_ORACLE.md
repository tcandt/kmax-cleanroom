# Forensic Report: First-Run Persistence Oracle

**Status**: DYNAMIC LIFECYCLE OBSERVATION (PASS)

## 1. Observed Lifecycle State Transitions

| Item Name | Type | Before Startup | After Startup | After Shutdown | Lifecycle Note |
|---|---|---|---|---|---|
| `device_tags.json` | `file` | ABSENT | EXISTS (36 B) | EXISTS (36 B) | Created on boot |
| `downloads` | `directory` | ABSENT | EXISTS (0 B) | EXISTS (0 B) | Created on boot |
| `snapshots` | `directory` | ABSENT | EXISTS (0 B) | EXISTS (0 B) | Created on boot |
| `users.json` | `file` | ABSENT | EXISTS (411 B) | EXISTS (411 B) | Created on boot |

## 2. Key Lifecycle Findings

- **`users.json`**: Eagerly created at first startup with default administrator credentials (`admin`/`admin123`).
- **`device_tags.json`**: Eagerly created at first startup with empty structure `{"tags":[], "deviceTags":{}}`.
- **`downloads/` & `snapshots/`**: Directories eagerly created on startup.
- **`shares.json`**: **NOT created at boot**. It is initialized lazily when shares are created or saved.
- **Shutdown Persistence**: All initialized files and directories persist across shutdown without corruption.
