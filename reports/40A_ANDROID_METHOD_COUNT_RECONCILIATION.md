# Report 40A: Android Helper Method Count Reconciliation & DEX Ground Truth

## 1. Executive Summary

During early forensic extraction (Phase 0), artifact manifests recorded **1,625 methods** for `libsys_core.so` (the disguised Android APK helper `com.android.helper`, version `3.3.4-2af7ccc1`). In Phase 1A direct decompilation, **1,061 class-defined methods** across **154 defined classes** were cataloged and decompiled.

This report documents the deterministic binary and mathematical decomposition of this count relationship. The difference of **564 method references** is an inherent architectural property of the Dalvik Executable (DEX) file format:
- **1,625** is the cardinality of the DEX header `method_ids` table (the total population of indexed method identifiers).
- **1,061** is the total population of concrete direct and virtual methods declared inside the 154 application class definitions (`class_data_item`).
- **564** is the exact population of non-defined method reference entries:
  - **279** standard Java runtime library methods (`java.*`)
  - **269** Android OS framework API methods (`android.*`)
  - **7** internal-class-owner non-defined method references (methods invoked via helper subclasses but declared in superclasses)
  - **9** DEX synthetic array-owner `clone()` method references on helper enum arrays (`[Lcom/android/helper/...;`)

There is zero missing code and zero population loss: $1,625 = 1,061 + (279 + 269 + 7 + 9) = 1,061 + 564$. 100.00% of defined methods (1,061 of 1,061) decompiled cleanly.

---

## 2. DEX Binary Header Ground Truth

Direct inspection of `classes.dex` inside `cloudphone-v0.3.6 (1)/android/libsys_core.so` (SHA-256: `9557601adbcba9352e854b73bda82806ceb5ab3e9bb62ba41b07223b37803301`) via deterministic parser `tools/audit/audit_method_count.py` yields the following header layout:

| Header Field | Byte Offset | Size / Count | Description |
|---|---|---|---|
| `magic` | `0x00 - 0x07` | `dex\n035\0` | Standard Android DEX version 035 magic |
| `string_ids_size` | `0x38 - 0x3B` | **2,661** | Total indexed UTF-8 string constants |
| `type_ids_size` | `0x40 - 0x43` | **419** | Total indexed type descriptors |
| `proto_ids_size` | `0x48 - 0x4B` | **625** | Total method prototypes (return + parameter types) |
| `field_ids_size` | `0x50 - 0x53` | **721** | Total field identifiers |
| `method_ids_size` | `0x58 - 0x5B` | **1,625** | **Total method reference index table entries** |
| `class_defs_size` | `0x60 - 0x63` | **154** | **Total defined application classes** |

The `method_ids` table in the DEX format (DALVIK-SPEC §4.3) stores `method_id_item` entries consisting of `(class_idx, proto_idx, name_idx)`. Every Dalvik invocation instruction (`invoke-virtual`, `invoke-direct`, `invoke-static`, `invoke-interface`, `invoke-super`) takes a 16-bit reference into this table. Consequently, all external and inherited APIs called by the application must be assigned a slot in this 1,625-entry table.

---

## 3. Mathematical Population Reconciliation

$$\text{DEX } method\_ids \ (1,625) = \text{Internal Class-Defined Methods} \ (1,061) + \text{Non-Defined Method References} \ (564)$$

```text
+-----------------------------------------------------------------------------------------------------------------+
|                                           DEX method_ids Table (1,625)                                          |
+---------------------------------------------------------+-------------------------------------------------------+
|        Internal Declared Methods across 154 classes     |         Non-Defined Method References (564)           |
|                         (1,061)                         |                                                       |
|  - Direct application methods: 940                      |  - java.* (Java platform library):              279   |
|  - Synthetic / lambda methods: 121                      |  - android.* (Android framework library):       269   |
|  - Total class-defined:       1,061 (100% decompiled)   |  - internal-class-owner (inherited superclass):   7   |
|                                                         |  - DEX synthetic array-owner clone():             9   |
+---------------------------------------------------------+-------------------------------------------------------+
```

---

## 4. Rigorous Decomposition of the 564 Non-Defined References

### A. Java Platform Standard Library Methods (279)
Invoked across collection handling, threading, I/O, and string formatting (e.g. `java.lang.String`, `java.util.Map`, `java.io.InputStream`, `java.lang.Thread`).

### B. Android OS Framework Methods (269)
Invoked across IPC, display control, surface buffers, and input injection (e.g. `android.view.SurfaceControl`, `android.os.IBinder`, `android.os.Parcel`, `android.view.MotionEvent`, `android.hardware.display.IDisplayManager`).

### C. Internal-Class-Owner Non-Defined Method References (7)
Methods referenced with an internal `Lcom/android/helper/...` owner type in the DEX instruction pool, but actually resolved and defined in base classes:
1. `FakeContext.getPackageManager`: Resolved as inherited from `android.content.Context`.
2. `DesktopConnection$SocketWrapper.close`: Resolved as inherited from `java.io.Closeable` / `java.lang.AutoCloseable`.
3. `Orientation.ordinal`: Resolved as inherited from `java.lang.Enum`.
4. `Ln$Level.ordinal`: Resolved as inherited from `java.lang.Enum`.
5. `CameraCapture.invalidate`: Resolved as inherited from internal abstract superclass `com.android.helper.video.SurfaceCapture`.
6. `NewDisplayCapture.invalidate`: Resolved as inherited from internal abstract superclass `com.android.helper.video.SurfaceCapture`.
7. `ScreenCapture.invalidate`: Resolved as inherited from internal abstract superclass `com.android.helper.video.SurfaceCapture`.

### D. DEX Synthetic Array-Owner Method References (9)
Compiler-synthesized array `clone()` method references on enum and helper value arrays:
- `[Lcom/android/helper/audio/AudioCodec;.clone()`
- `[Lcom/android/helper/audio/AudioSource;.clone()`
- `[Lcom/android/helper/device/Orientation$Lock;.clone()`
- `[Lcom/android/helper/device/Orientation;.clone()`
- `[Lcom/android/helper/util/Codec$Type;.clone()`
- `[Lcom/android/helper/util/Ln$Level;.clone()`
- `[Lcom/android/helper/video/CameraFacing;.clone()`
- `[Lcom/android/helper/video/VideoCodec;.clone()`
- `[Lcom/android/helper/video/VideoSource;.clone()`

Sum of non-defined reference categories: $279 + 269 + 7 + 9 = 564$.
Total DEX method IDs: $1,061 + 564 = 1,625$.

---

## 5. Tooling Truthfulness & Archival Classification

- **JADX v1.5.6**: Recovered 1,061/1,061 declared methods into readable Java source under `raw_extraction/android/jadx/`.
- **Apktool v3.0.3**: Extracted resources, binary manifest, and metadata under `raw_extraction/android/apktool/`.
- **Baksmali v2.5.2**: Output preserved under `raw_extraction/android/smali/`. Classified as `HISTORICAL_ARCHIVAL_OUTPUT_PRESENT` (archival evidence, not claimed as an independently re-run verification tool in Phase 3AR).
- **Automated Verification**: `tools/audit/audit_method_count.py --check` passes with zero unclassified references.

### Precision Language Rule
- We do **not** claim "100% literal original source text recovery" (local parameter names and original comments stripped by D8/R8 during helper compilation are naturally absent).
- We **do** claim **100.00% decompilation completeness for the recovered class/method population** (all 1,061 declared methods decompiled into valid Java syntax with full control-flow recovery).

---

## 6. Closure Verdict

- **Phase 0 Metric (1,625)**: Correctly identifies DEX `method_ids` table size.
- **Phase 1A Metric (1,061)**: Correctly identifies declared class method definitions.
- **Delta (564)**: Fully decomposed into 279 Java platform, 269 Android framework, 7 inherited methods, and 9 array clone references.
- **Status**: **RECONCILED, DETERMINISTICALLY PROVEN, AND FORMALLY CLOSED**.
