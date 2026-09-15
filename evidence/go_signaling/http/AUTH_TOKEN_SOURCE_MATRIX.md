# Forensic Evidence: HTTP Authentication Token Source & Precedence Matrix

**Target**: `webrtc-signaling` (Linux AMD64 / Windows AMD64)  
**Endpoint Tested**: `/api/me`  
**Precedence Verdict**: `HEADER_FIRST_STRICT: Header is evaluated first. If Bearer scheme is present, header token is selected exclusively (invalid bearer fails without falling back to query).`  

---

## 1. Ground Truth Finding & Evidence Table

| Case ID | Authorization Header | Query Token Type | Header Identity | Query Identity | Status | Authenticated User | Selected Source | Classification |
|---|---|---|---|---|---|---|---|---|
| `CASE_01_HEADER_BEARER_VALID_NO_QUERY` | `Bearer 509ea96650a883aa55e3d73be2632a34dc6f93a98d2d0bfddf154bad4b463899` | `NONE` | `admin` | `NONE` | 200 | `admin` | `HEADER` | `AUTHENTICATED_VIA_HEADER` |
| `CASE_02_NO_HEADER_QUERY_VALID` | *(none)* | `VALID_ORIGINAL_TOKEN` | `NONE` | `admin` | 200 | `admin` | `QUERY` | `AUTHENTICATED_VIA_QUERY` |
| `CASE_03_HEADER_VALID_QUERY_INVALID` | `Bearer 509ea96650a883aa55e3d73be2632a34dc6f93a98d2d0bfddf154bad4b463899` | `INVALID_TOKEN` | `admin` | `INVALID` | 200 | `admin` | `HEADER` | `AUTHENTICATED_VIA_HEADER` |
| `CASE_04_HEADER_INVALID_QUERY_VALID` | `Bearer 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef` | `VALID_ORIGINAL_TOKEN` | `INVALID` | `admin` | 401 | *(rejected)* | `NONE` | `REJECTED_UNAUTHORIZED` |
| `CASE_05_HEADER_BASIC_VALID_QUERY_VALID` | `Basic 509ea96650a883aa55e3d73be2632a34dc6f93a98d2d0bfddf154bad4b463899` | `VALID_ORIGINAL_TOKEN` | `admin (Basic scheme)` | `admin` | 401 | *(rejected)* | `NONE` | `REJECTED_UNAUTHORIZED` |
| `CASE_06_HEADER_MALFORMED_QUERY_VALID` | `MalformedNoSpaceOrUnknownHeaderToken` | `VALID_ORIGINAL_TOKEN` | `MALFORMED` | `admin` | 401 | *(rejected)* | `NONE` | `REJECTED_UNAUTHORIZED` |
| `CASE_07_HEADER_EMPTY_BEARER_QUERY_VALID` | `Bearer ` | `VALID_ORIGINAL_TOKEN` | `EMPTY_BEARER` | `admin` | 401 | *(rejected)* | `NONE` | `REJECTED_UNAUTHORIZED` |
| `CASE_08_NO_HEADER_QUERY_INVALID` | *(none)* | `INVALID_TOKEN` | `NONE` | `INVALID` | 401 | *(rejected)* | `NONE` | `REJECTED_UNAUTHORIZED` |
| `CASE_09_NO_HEADER_QUERY_EMPTY` | *(none)* | `EMPTY_TOKEN` | `NONE` | `EMPTY` | 401 | *(rejected)* | `NONE` | `REJECTED_UNAUTHORIZED` |
| `CASE_10_HEADER_VALID_USER_A_QUERY_VALID_USER_B` | `Bearer 509ea96650a883aa55e3d73be2632a34dc6f93a98d2d0bfddf154bad4b463899` | `VALID_DIFFERENT_USER_TOKEN` | `admin` | `test_user` | 200 | `admin` | `HEADER` | `AUTHENTICATED_VIA_HEADER` |

## 2. Disassembly Corroboration

Disassembly of `AUTH_TOKEN_LOOKUP` (Linux `main.lYKp_Iuf` @ `0x73b080`, Windows `main.mLWT3o` @ `0x140344260`) shows:
1. `r.Header.Get("Authorization")` is retrieved.
2. If header is present and splits into 2 parts with `strings.ToLower(parts[0]) == "bearer"`:
   - `parts[1]` is unconditionally extracted as the token.
   - The function returns this token immediately. If invalid, the downstream authenticator rejects it (no query fallback).
3. If header is absent, empty, does NOT split into 2 parts, or `parts[0] != "bearer"`:
   - Execution falls through to `r.URL.Query().Get("token")`.
4. Probed Case 4 (Bearer <invalid> + query <valid>) yielded status `401`.
5. Probed Case 5 (Basic <valid> + query <valid>) yielded status `401` with user `None` (fell back to query!).
6. Probed Case 6 (Malformed + query <valid>) yielded status `401` with user `None` (fell back to query!).
7. Probed Case 7 (Bearer empty + query <valid>) yielded status `401` with user `None`.
8. Probed Case 10 (Header Admin + Query User) authenticated `admin` (header took precedence).
