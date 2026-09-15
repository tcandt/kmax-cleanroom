# WebRTC Signaling: Recovered Environment Variables

| Variable Name | Default Value | Functional Description | Evidence Origin |
|---|---|---|---|
| `PORT` | `8443` | Listening port for HTTPS/WSS service | Docker Compose & `.rodata` |
| `HOST` | `0.0.0.0` | Network binding interface IP | Docker Compose & `.rodata` |
| `ASSETS` | `/app/assets` | Directory path containing web frontend build | Docker Compose & `.rodata` |
| `DATA_DIR` | `/app/data` | Directory for persistent storage (SQLite/shares.json) | Docker Compose & `.rodata` |
| `USE_TLS` | `true` | Enable TLS/HTTPS/WSS encryption | Docker Compose & `.rodata` |
| `TLS_CERT` | `/app/certs/server.crt` | Path to TLS certificate PEM | Docker Compose & `.rodata` |
| `TLS_KEY` | `/app/certs/server.key` | Path to TLS private key | Docker Compose & `.rodata` |
| `ICE_SERVERS` | `turn:...` | STUN/TURN configuration delivered to WebRTC clients | Docker Compose & `.rodata` |
| `DEFAULT_SETTINGS` | `{maxBitrate:4,...}` | Global fallback parameters for virtual machines | Docker Compose & `.rodata` |
