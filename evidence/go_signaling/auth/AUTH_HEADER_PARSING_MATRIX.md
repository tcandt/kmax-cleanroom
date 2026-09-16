# Forensic Evidence: HTTP Authorization Header Parsing Matrix

**Target**: `webrtc-signaling` (Linux AMD64 / Windows AMD64)  
**Endpoint Tested**: `/api/me` (Protected Handler: Linux VA `0x73f100`, Windows VA `0x140348320`)  
**Token Used**: Freshly issued **VALID ORIGINAL TOKEN** from `/api/login`  
**Investigation Scope**: Disentangling Header Scheme Parser Casing vs Token Validity

---

## 1. Executive Summary & Ground Truth Finding

By probing the live original binary with a **confirmed valid token**, we determine the true contract of the HTTP header parser (`AUTH_TOKEN_LOOKUP`: Linux `main.lYKp_Iuf` @ `0x73b080`, Windows `main.mLWT3o` @ `0x140344260`):

> [!IMPORTANT]
> **Bearer Scheme Parsing is Case-Insensitive**:  
> The original binary accepts `Bearer`, `bearer`, `BEARER`, and `bEaReR` identically. All variations successfully authenticate the session and resolve the user identity.  
> Static disassembly confirms this behavior at Linux VA `0x73b140-0x73b185`: the header is split on whitespace, and the scheme segment (`parts[0]`) is converted to lowercase via `strings.ToLower` before comparison against `"bearer"`.

---

## 2. Dynamic Probe Results (Valid Token)

| Case ID | Injected Headers | Status | Body Preview | Authenticated? | Forensic / Architectural Rule |
|---|---|---|---|---|---|
| `BEARER_CANONICAL` | `{"Authorization": "Bearer e4653893271af635b73732e26984802435aa8ba50666c6148ac020b215af0650"}` | 200 | `{"ai_config":null,"assigned_devices` | **YES** (`admin`) | Bearer prefix accepted case-insensitively via strings.ToLower |
| `BEARER_LOWERCASE` | `{"Authorization": "bearer e4653893271af635b73732e26984802435aa8ba50666c6148ac020b215af0650"}` | 200 | `{"ai_config":null,"assigned_devices` | **YES** (`admin`) | Bearer prefix accepted case-insensitively via strings.ToLower |
| `BEARER_UPPERCASE` | `{"Authorization": "BEARER e4653893271af635b73732e26984802435aa8ba50666c6148ac020b215af0650"}` | 200 | `{"ai_config":null,"assigned_devices` | **YES** (`admin`) | Bearer prefix accepted case-insensitively via strings.ToLower |
| `BEARER_MIXED_CASE` | `{"Authorization": "bEaReR e4653893271af635b73732e26984802435aa8ba50666c6148ac020b215af0650"}` | 200 | `{"ai_config":null,"assigned_devices` | **YES** (`admin`) | Bearer prefix accepted case-insensitively via strings.ToLower |
| `WRONG_SCHEME_BASIC` | `{"Authorization": "Basic e4653893271af635b73732e26984802435aa8ba50666c6148ac020b215af0650"}` | 401 | `Unauthorized` | **NO** | Non-bearer or empty token rejected with 401 Unauthorized |
| `MISSING_HEADER` | `*(missing)*` | 401 | `Unauthorized` | **NO** | Non-bearer or empty token rejected with 401 Unauthorized |
| `EMPTY_HEADER` | `{"Authorization": ""}` | 401 | `Unauthorized` | **NO** | Non-bearer or empty token rejected with 401 Unauthorized |
| `EMPTY_BEARER` | `{"Authorization": "Bearer "}` | 401 | `Unauthorized` | **NO** | Non-bearer or empty token rejected with 401 Unauthorized |

---

## 3. Disassembly Ground Truth (`main.lYKp_Iuf` / `main.mLWT3o`)

```text
0x73b105: call net/http.(*Header).Get("Authorization")
0x73b10a: test rbx, rbx
0x73b135: call strings.Split / strings.Fields (delimiter ' ')
0x73b140: cmp rbx, 2               ; Expect exactly 2 parts: <scheme> <token>
0x73b155: call strings.ToLower      ; Convert parts[0] to lowercase
0x73b160: cmp rbx, 6               ; Check length == len("bearer") == 6
0x73b166: cmp dword ptr [rax], 0x72616562  ; "bear" in little-endian
0x73b16e: cmp word ptr [rax+4], 0x7265      ; "er" in little-endian
0x73b17b: mov rbx, [rdx + 0x18]    ; Extract parts[1] as session token!
0x73b185: ; If header missing or scheme != bearer -> fallback to req.URL.Query().Get("token")
```

---

## 4. Phase 2C.3 Contract Specifications

When Phase 2C.3 reconstructs the HTTP authentication middleware:
1. Header retrieval must parse `req.Header.Get("Authorization")`.
2. Whitespace separation into `parts`: if `len(parts) == 2` and `strings.EqualFold(parts[0], "bearer")` (or `strings.ToLower(parts[0]) == "bearer"`), use `parts[1]`.
3. Fallback to `req.URL.Query().Get("token")` if Authorization header is absent or does not contain a bearer scheme.
4. Non-bearer schemes (such as `Basic`) without query parameter fallback must return `401 Unauthorized`.
