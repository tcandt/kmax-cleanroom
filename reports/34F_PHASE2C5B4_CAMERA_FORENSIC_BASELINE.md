# Cleanroom Forensic Engineering Report 34F
## Phase 2C.5B4F — Camera Forensic Precision & Contract Freeze Closure

- **Phase**: Phase 2C.5B4F (Forensic Precision Pass, Contract Narrowing, and Baseline Freeze)
- **Base Commit**: `2a039510d7e5ae4ef3f067769b40660c705989ff`
- **Closure Date**: 2026-09-18
- **Mode**: FORENSIC ONLY (No production Go source in `pkg/` modified; no business logic implemented)
- **Contract Status**: FROZEN FORENSIC BASELINE
- **Spec Artifact**: `evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json`
- **Spec SHA-256**: `1a177531761d51ee280be5d9dce5bd8442c42f19f66ca5acde66b38dd4c48ff9`
- **Contract Artifact**: `evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json`
- **Contract SHA-256**: `818abe7db2cc38df3563a0f6cf45ec047cf0c0a93338c994e60a327fc0d471ce`
- **Reproducer Tool**: `tools/forensics/reproduce_camera_forensics.py`

---

### 1. Executive Summary & Forensic Verdict

Phase 2C.5B4F successfully executes a rigorous forensic precision closure to address the 6 critical corrections raised on Phase 2C.5B4 before freezing the contract:

1. **4-Byte Length Prefix Byte Order**: Resolved conclusively to **Little-Endian uint32** (`binary.LittleEndian.PutUint32` / `binary.LittleEndian.Uint32`). Disassembly proves direct 32-bit register store instructions (`str w3, [x0]` on AArch64 and `movl %edx, (%rax)` on x86_64) without byte-reversal instructions (`rev` or `bswap`) on natively little-endian targets.
2. **Camera HAL/Bridge Inbound Read Framing**: Fully recovered the exact inbound event parser. The Agent reads HAL events using identical framing: a 4-byte Little-Endian uint32 length prefix via `io.ReadFull`, followed by an exact `length`-byte ASCII event payload via `io.ReadFull`. Events are NOT newline-delimited, NOT raw tokens, and NOT JSON-wrapped envelopes.
3. **Planar YUV420P / I420 Exact Stride & Subsampling**: Disassembly at ARM64 `0x51c250`-`0x51c780` proves concrete type `*image.YCbCr` is validated with `SubsampleRatio == 2` (`YCbCrSubsampleRatio420`). Output buffer is allocated to exact size $(W \times H \times 3) / 2$. A fast path performs 3 contiguous `memmove` operations for Y ($W \times H$), Cb ($(W/2) \times (H/2)$), and Cr ($(W/2) \times (H/2)$) when `YStride == W` and `CStride == W/2`. Stride fallback copies row-by-row with stride offsets $y \times \text{Stride}$, and non-4:2:0 images fall back to standard Rec.601 RGB-to-YUV conversion.
4. **Channel Capacity & Drop Semantics**: `cameraFrameChan` buffer capacity is proved to be **exactly 1** (`runtime.makechan64` with size 1 at `0x51ea3c`). Non-blocking send at `0x51a388` calls `runtime.selectnbsend`. Fact wording is strictly frozen as `"current frame is not enqueued when non-blocking send cannot proceed"`, with latency minimization classified as `[Inference]`.
5. **Snapshot Cache Ordering**: In `OnMessage`, `s.latestCameraJpeg` is updated under `latestCameraJpegMu` BEFORE `runtime.selectnbsend`. Therefore, a frame dropped from the streaming channel due to full capacity still updates the snapshot cache; `VIRTUAL_DEVICE_CAPTURE_IMAGE` always receives the newest frame.
6. **Physical vs Virtual Camera Separation**: Positively proved that `CameraCapture.java` belongs strictly to the physical camera capture pipeline (`android.hardware.camera2` $\to$ `@uds_sys_v_`). No call or data flow links it to virtual camera injection (`camera-channel` $\to$ Agent JPEG decode $\to$ planar YUV420P $\to$ Camera HAL TCP bridge).
7. **Semantic Lifecycle Classification**: The 7-state lifecycle model is classified as `RECONSTRUCTED_SEMANTIC_MODEL` (not literal binary enum names).
8. **Provenance Hygiene**: All forensic scripts are housed exclusively in repo-local `tools/forensics/camera/` and `tools/forensics/`. Toolchain metadata is recorded with cryptographic hashes.

---

### 2. Toolchain Provenance Metadata

External tools used during the forensic extraction are documented as formal toolchain dependencies:

| Attribute | Value |
|---|---|
| **Disassembler Executable** | `llvm-objdump.exe` |
| **Version** | `22.1.8` (Optimized build, LLVM-MinGW UCRT x86_64) |
| **SHA-256** | `2225c03acd46d4dd9aee94ae2f431e42d305b9145a885462c1e5d1998983d64d` |
| **Origin / Install Method** | WinGet package `MartinStorsjo.LLVM-MinGW.UCRT` (`20260616-ucrt-x86_64`) |
| **Target Architectures** | `aarch64` (little endian), `x86-64` (little endian) |
| **Extraction Scripts** | `tools/forensics/camera/dump_camera_strings.py`<br>`tools/forensics/camera/extract_camera_disassembly.py`<br>`tools/forensics/camera/derive_camera_protocol.py` |
| **Canonical Reproducer** | `tools/forensics/reproduce_camera_forensics.py` |
| **Canonical Output Directory**| `D:\KMAX-CLEANROOM` |

---

### 3. Physical-Camera vs Virtual-Camera Boundary

Forensic cross-referencing across the Android helper Java sources and the Go Agent binary establishes strict architectural decoupling:

```
[ PHYSICAL CAMERA CAPTURE PIPELINE ]
Physical Camera Sensor (Hardware)
   │
   ▼
CameraCapture.java (android.hardware.camera2)
   │
   ▼
SurfaceCapture (OpenGL EGL / MediaCodec)
   │
   ▼
UNIX Domain Socket (@uds_sys_v_)
   │
   ▼
Agent Video Ingestion -> WebRTC Media Track (display_0) -> Remote Viewer


[ VIRTUAL CAMERA INJECTION PIPELINE ]
Browser Client (navigator.mediaDevices.getUserMedia -> canvas.toBlob)
   │
   ▼ ArrayBuffer (image/jpeg)
WebRTC DataChannel ("camera-channel", ordered=true)
   │
   ▼ OnMessage
Agent s.latestCameraJpeg (Mutex) & s.cameraFrameChan (cap=1, selectnbsend)
   │
   ▼
image/jpeg.Decode -> Planar I420 YUV (W*H*3/2 bytes)
   │
   ▼ 4-byte LE length prefix
TCP Bridge (127.0.0.1:9001 / Camera HAL)
   │
   ▼
Android Apps (WeChat, WhatsApp, Zoom, Camera App)
```

**Positive Boundary Conclusion (`CROSS_COMPONENT_CONFIRMED`)**:
> "CameraCapture.java is positively bound to the physical-camera capture pipeline. No recovered call/data-flow evidence places CameraCapture.java on the virtual-camera injection path; the recovered injection path is camera-channel -> Agent JPEG decode -> camera TCP bridge."

---

### 4. Channel Ownership and Gating

- **Channel Name**: `"camera-channel"` (`STATIC_CONFIRMED`, offset `0x6a93ba` in ARM64 `.rodata`).
- **Creator / Ownership**: Outbound, Agent-created (`STATIC_CONFIRMED`, `CreateDataChannel` called before SDP offer creation).
- **Ordered Flag**: `true` (`STATIC_CONFIRMED`, byte pointer `&ordered` where `ordered = 1` passed to `CreateDataChannel` at ARM64 `0x53e740` and AMD64 `0x9e216d`).
- **Camera Support Gate (`STATIC_CONFIRMED`)**:
  - Probed at startup via `net.DialTimeout("tcp", cameraAddr, timeout)` (ARM64 `0x51ee5c`).
  - If dial succeeds: `cameraSupport = true`, logged as `[Agent] Camera HAL is available at %s (camera support enabled)` (`0x6e22c4`).
  - If dial fails and `-force-camera` is unset: `cameraSupport = false`, logged as `[Agent] Camera HAL is not available at %s (camera support disabled). Use -force-camera to override.` (`0x6e9132`).
  - If dial fails and `-force-camera` is set: `cameraSupport = true`, logged as `[Agent] Camera HAL is not available, but camera support is FORCED enabled via -force-camera` (`0x6e8858`).
  - Offer signaling: SDP offer payload includes boolean `"camera_support": true/false`.
  - Channel creation condition: `camera-channel` is created if and only if `cameraSupport == true`.

---

### 5. Control Direction & Framing

- **Agent $\to$ Browser Control (`STATIC_CONFIRMED`)**:
  - Start command: JSON text frame `{"action":"start"}` dispatched when HAL sends `VIRTUAL_DEVICE_START_CAMERA_SESSION`.
  - Stop command: JSON text frame `{"action":"stop"}` dispatched when HAL sends `VIRTUAL_DEVICE_STOP_CAMERA_SESSION`.
  - Wire method: `webrtc.DataChannel.SendText(jsonString)` (ARM64 `0x51c980`).
- **Browser $\to$ Agent Frame Stream (`STATIC_CONFIRMED`)**:
  - Inbound frames: Raw binary JPEG ArrayBuffer payloads.
  - Wire method: `webrtc.DataChannel.OnMessage(func(msg webrtc.DataChannelMessage))` where `msg.Data` contains raw JPEG bytes.

---

### 6. Browser / Reference Encoding Classification

- **Original Agent Evidence (`STATIC_CONFIRMED`)**:
  - Decoder: Standard Go `image/jpeg.Decode` (ARM64 `0x51c27c`).
  - Type expectation: Expects `*image.YCbCr` struct.
- **Reference Frontend Implementation (`REFERENCE_ONLY`)**:
  - Canvas resolution: `640x480`.
  - Capture frame rate: 30 FPS timer (`1000 / 30 ms`).
  - Encoding MIME type: `image/jpeg`.
  - JPEG quality parameter: `0.6`.
  - Transport: `cameraChannel.send(arrayBuffer)`.
  - **Parity Principle**: Browser encoder parameters (resolution 640x480, FPS 30, quality 0.6) are reference-only lane D implementation details; Agent binary decodes arbitrary JPEG dimensions.

---

### 7. YUV420 / Planar I420 Layout Precision

Disassembly of ARM64 `0x51c250`-`0x51c780` establishes exact plane layout and fallback behaviors:

| Parameter | Forensic Value | Classification |
|---|---|---|
| **Decoded Type** | `*image.YCbCr` | `STATIC_CONFIRMED` |
| **Subsampling Ratio** | `YCbCrSubsampleRatio420 == 2` (checked at offset `0x58`) | `STATIC_CONFIRMED` |
| **Total Buffer Size** | `(width * height * 3) / 2` bytes | `STATIC_CONFIRMED` |
| **Y Plane** | Offset `0`, length `width * height` bytes | `STATIC_CONFIRMED` |
| **Cb (U) Plane** | Offset `width * height`, length `(width/2) * (height/2)` bytes | `STATIC_CONFIRMED` |
| **Cr (V) Plane** | Offset `width * height + (width/2)*(height/2)`, length `(width/2) * (height/2)` bytes | `STATIC_CONFIRMED` |
| **Plane Order** | Contiguous Planar I420: `Y` $\to$ `Cb (U)` $\to$ `Cr (V)` | `STATIC_CONFIRMED` |
| **Contiguous Fast Path** | Checked if `YStride == width` and `CStride == width / 2`. If true, copies 3 planes via single `runtime.memmove` per plane. | `STATIC_CONFIRMED` |
| **Stride Fallback** | If strides differ, iterates row-by-row copying row slices from offset $y \times \text{Stride}$. | `STATIC_CONFIRMED` |
| **Generic Fallback** | If `SubsampleRatio != 2` or not `*image.YCbCr`, converts pixel-by-pixel via `img.At(x, y)` $\to$ `color.RGBA()` $\to$ standard Rec.601 YUV. | `STATIC_CONFIRMED` |

---

### 8. Camera HAL / Bridge TCP Endpoint Classification

- **Classification**:
  - **DEFAULT Endpoint**: `127.0.0.1:9001` (from `.rodata:0x6a92e8`).
  - **CONFIGURABLE Option (CLI Flag)**: `-camera-addr` (from `.rodata:0x6a5738`).
  - **CONFIGURABLE Option (Env Var)**: `CP_AGENT_CAMERA_ADDR` (from `.rodata:0x6af343`).
  - **OVERRIDE Option (CLI Flag)**: `-force-camera` (from `.rodata:0x6d88a6`, `0x6d917b`).
  - **ACTUAL Runtime Endpoint**: Dialed dynamically on startup; if dial fails without `-force-camera`, camera support is disabled.
- **Terminology**: Designated as **"default Camera HAL/bridge endpoint"**.

---

### 9. HAL Read/Write Framing & Byte Order

#### 9.1 Wire Length Framing Byte Order (`STATIC_CONFIRMED`)
Both ARM64 and AMD64 architectures use native 32-bit register store instructions into a 4-byte buffer without byte swapping:
- ARM64 (`0x51c0a8`): `str w3, [x0]`
- AMD64 (`0x9b9845`): `movl %edx, (%rax)`
- Machine byte order: Target binaries are `elf64-littleaarch64` and `elf64-x86-64` (Little-Endian).
- **Wire Representation**: **Little-Endian uint32** (`binary.LittleEndian.PutUint32(buf[:4], uint32(len))`).

#### 9.2 Wire Framing Test Vectors (`STATIC_CONFIRMED`)

| Description | Payload Length $N$ | Expected Prefix Bytes (Little-Endian) | Wire Prefix Hex |
|---|---|---|---|
| Empty Payload | 0 | `[0x00, 0x00, 0x00, 0x00]` | `00000000` |
| Small YUV Frame (2x2) | 6 | `[0x06, 0x00, 0x00, 0x00]` | `06000000` |
| `VIRTUAL_DEVICE_CAPTURE_IMAGE` | 28 | `[0x1c, 0x00, 0x00, 0x00]` | `1c000000` |
| `VIRTUAL_DEVICE_STOP_CAMERA_SESSION` | 34 | `[0x22, 0x00, 0x00, 0x00]` | `22000000` |
| `VIRTUAL_DEVICE_START_CAMERA_SESSION` | 35 | `[0x23, 0x00, 0x00, 0x00]` | `23000000` |
| Handshake JSON (`{"width":640,...}`) | 44 | `[0x2c, 0x00, 0x00, 0x00]` | `2c000000` |
| Standard 640x480 YUV420P Frame | 460800 | `[0x00, 0x08, 0x07, 0x00]` | `00080700` |

#### 9.3 HAL Inbound Read Framing (`STATIC_CONFIRMED`)
Disassembly at ARM64 `0x51aa8c`-`0x51abf8` establishes the exact inbound read loop:
1. `makeslice(byte, 4, 4)` allocates 4-byte header buffer.
2. `io.ReadFull(conn, lenBuf[:4])` reads 4 bytes.
3. `ldr w2, [x3]` loads 32-bit unsigned integer length in Little-Endian.
4. `makeslice(byte, length, length)` allocates payload buffer of exact length.
5. `io.ReadFull(conn, payloadBuf)` reads exact payload.
6. Payload is converted to string and compared via `runtime.memequal` (`0x15440`).

---

### 10. HAL Event Semantics & Inbound Dispatch

The three inbound HAL events are handled as follows:

| Event Name | Length | VA | Inbound Action | Outbound Consequence |
|---|---|---|---|---|
| `VIRTUAL_DEVICE_START_CAMERA_SESSION` | 35 | `0x6ceac7` | Sets streaming active flag (`0x460`) | Dispatches `{"action":"start"}` to browser over `camera-channel` |
| `VIRTUAL_DEVICE_STOP_CAMERA_SESSION` | 34 | `0x6cdb19` | Clears streaming active flag (`0x460`) | Dispatches `{"action":"stop"}` to browser over `camera-channel` |
| `VIRTUAL_DEVICE_CAPTURE_IMAGE` | 28 | `0x6c7482` | Acquires `latestCameraJpegMu` (`0x498`), reads `latestCameraJpeg` (`0x470`), unlocks | Sends 4-byte LE length prefix + cached JPEG snapshot to HAL TCP socket |

---

### 11. Backpressure, Capacity & Snapshot Ordering

- **Channel Capacity (`STATIC_CONFIRMED`)**:
  - `s.cameraFrameChan` is allocated at ARM64 `0x51ea3c` passing capacity `1` to `runtime.makechan64`.
  - Capacity is **EXACTLY 1**.
- **Enqueue Semantics (`STATIC_CONFIRMED`)**:
  - Calls `runtime.selectnbsend(s.cameraFrameChan, msg.Data)` at `0x51a388`.
  - Static fact: `"current frame is not enqueued when non-blocking send cannot proceed"`.
  - Rationale: `[Inference]` (non-blocking drop policy prevents buffer lag and minimizes streaming latency).
- **Snapshot Cache Ordering (`STATIC_CONFIRMED`)**:
  - In `OnMessage`, `s.latestCameraJpeg` is updated under `latestCameraJpegMu` BEFORE `selectnbsend`.
  - Consequence: Even when `cameraFrameChan` is saturated and the frame is dropped from the video stream, the snapshot cache retains the newest frame. `VIRTUAL_DEVICE_CAPTURE_IMAGE` is always guaranteed the most recent received frame.

---

### 12. Lifecycle Model Classification

- **Internal State Model (`RECONSTRUCTED_SEMANTIC_MODEL`)**:
  - `STATE_UNINITIALIZED`: Initial session state.
  - `STATE_CONNECTING_HAL`: DataChannel opened, dialing HAL TCP socket.
  - `STATE_HAL_HANDSHAKE`: TCP connected, transmitting 4-byte LE length-prefixed JSON handshake.
  - `STATE_IDLE_WAIT_HAL`: Handshake completed, waiting for `VIRTUAL_DEVICE_START_CAMERA_SESSION`.
  - `STATE_ACTIVE_STREAMING`: Virtual camera active, browser streaming frames, Agent forwarding YUV to HAL.
  - `STATE_PAUSED`: Virtual camera temporarily paused by `VIRTUAL_DEVICE_STOP_CAMERA_SESSION`.
  - `STATE_CLOSED`: DataChannel or TCP socket closed, resources released.
- **Classification Note**: These 7 state names represent clean-room semantic state machine architecture, not literal recovered binary enum names.

---

### 13. Protocol Specification & Contract Audit (13 Requirements)

Every requirement in `CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json` has been audited and mapped to strict evidence classes:

| Req ID | Requirement Description | Evidence Class | Scope Audit Status |
|---|---|---|---|
| **CAM-B4-01** | Outbound Camera-Channel Creation & Ordered Flag | `STATIC_CONFIRMED` | Strictly confirmed by disassembly (`ordered=1`) |
| **CAM-B4-02** | Camera HAL/Bridge Probe & Offer Flag Parity | `STATIC_CONFIRMED` | Confirmed via `net.DialTimeout` and log strings |
| **CAM-B4-03** | DataChannel Lifecycle Binding (OnOpen/Message/Close) | `STATIC_CONFIRMED` | Confirmed via closure registrations at `0x51a030`-`0x51a0c0` |
| **CAM-B4-04** | HAL/Bridge TCP Connection & Handshake Framing | `STATIC_CONFIRMED` | Confirmed 4-byte LE length + JSON `{width,height,frame_rate}` |
| **CAM-B4-05** | HAL Inbound Event Read Framing & Dispatch | `STATIC_CONFIRMED` | Confirmed 4-byte LE length prefix + ASCII event payload |
| **CAM-B4-06** | Outbound Start/Stop Command Dispatch | `STATIC_CONFIRMED` | Confirmed JSON text `{"action":"start"/"stop"}` |
| **CAM-B4-07** | Inbound Binary JPEG & Snapshot Cache Ordering | `STATIC_CONFIRMED` | Confirmed lock update before non-blocking enqueue |
| **CAM-B4-08** | Channel Buffer Capacity = 1 & Non-Blocking Enqueue | `STATIC_CONFIRMED` | Confirmed `makechan64(cap=1)` and `selectnbsend` |
| **CAM-B4-09** | JPEG Decode to Planar I420 with Stride Handling | `STATIC_CONFIRMED` | Confirmed `YCbCrSubsampleRatio420`, contiguous & stride fallback |
| **CAM-B4-10** | Little-Endian Length-Prefixed YUV Transmission | `STATIC_CONFIRMED` | Confirmed native 32-bit LE register store (`str w3`) |
| **CAM-B4-11** | Virtual Camera JPEG Snapshot Extraction | `STATIC_CONFIRMED` | Confirmed 4-byte LE length + cached JPEG under mutex |
| **CAM-B4-12** | Physical vs Virtual Camera Boundary Decoupling | `CROSS_COMPONENT_CONFIRMED` | Confirmed separation of `CameraCapture.java` from injection |
| **CAM-B4-13** | Strict Isolation of Deferred Channels (AI/ADB) | `STATIC_CONFIRMED` | Preserved inert lifecycle references only |

---

### 14. Known UNKNOWN Items & Implementation Choices

The following items are identified as unobservable from binary evidence and classified accordingly:

1. **Camera Peer Process Identity (`UNKNOWN`)**: Whether the peer listening on `127.0.0.1:9001` is an Android C++ HAL service, a v4l2loopback injector daemon, or a QEMU pipe bridge cannot be determined from Agent binary alone; designated neutrally as **"Camera HAL/bridge endpoint"**.
2. **Maximum JPEG Frame Dimensions (`IMPLEMENTATION_CHOICE`)**: The binary does not enforce an explicit upper bound check before `jpeg.Decode()`; the clean-room implementation enforces a safe maximum of 10 MB and $4096 \times 4096$ resolution.
3. **Dial Timeout Duration (`IMPLEMENTATION_CHOICE`)**: Exact timeout passed to `net.DialTimeout` on startup probe is reconstructed as 1000ms.

---

### 15. Reproducer Output & Cryptographic SHA-256 Hashes

The canonical reproducer `tools/forensics/reproduce_camera_forensics.py` was executed with 100% success:

```
=== Step 1: Executing dump_camera_strings.py ===
  All 26 string assertions verified.
=== Step 2: Executing extract_camera_disassembly.py ===
  Disassembly manifest extracted.
=== Step 3: Executing derive_camera_protocol.py ===
=== Step 4: Generating CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json ===
  Regenerated evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json
=== Step 5: Generating CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json ===
  Regenerated evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json
=== Step 6: Verifying Artifact Invariants and Hashes ===

------------------------------------------------------------
PHASE 2C.5B4F FORENSIC PRECISION PASS COMPLETE
  CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json:         1a177531761d51ee280be5d9dce5bd8442c42f19f66ca5acde66b38dd4c48ff9
  CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json: 818abe7db2cc38df3563a0f6cf45ec047cf0c0a93338c994e60a327fc0d471ce
------------------------------------------------------------
```

- **Spec SHA-256**: `1a177531761d51ee280be5d9dce5bd8442c42f19f66ca5acde66b38dd4c48ff9`
- **Contract SHA-256**: `818abe7db2cc38df3563a0f6cf45ec047cf0c0a93338c994e60a327fc0d471ce`

---

### 16. Verdict & STOP Condition

Phase 2C.5B4F is complete. All 6 user corrections have been fully satisfied, verified, and sealed with cryptographic hashes. In strict compliance with instructions:
- **NO production Go source** has been modified.
- **NO camera-channel business logic** has been implemented.
- **NO deferred channels** (AI/ADB) have been touched.
- **Execution HALTS** here for user review and explicit approval of the frozen contract before beginning Phase 2C.5B4 reconstruction.
