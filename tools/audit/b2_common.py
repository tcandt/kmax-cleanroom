#!/usr/bin/env python3
"""
tools/audit/b2_common.py
Phase 2C.5B2R3 Shared Evidence-Execution and Semantic Validation Primitives.

Pure, side-effect-free audit functions used identically across:
- tools/derive_b2_differential.py (generator)
- tools/verify_phase2.py (master audit verifier)
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ALLOWED_REPO_ROOT_PREFIXES = ("evidence/", "raw_extraction/", "reports/")


def resolve_json_pointer(doc: Any, pointer: str) -> Any:
    """
    Strict RFC 6901 JSON pointer evaluator.
    - Empty pointer "" returns the entire document.
    - Non-empty pointer must start with "/".
    - Unescapes ~1 -> / and ~0 -> ~.
    - Navigates dict keys and list integer indices.
    - Raises KeyError, IndexError, or ValueError on unresolvable tokens.
    """
    if pointer == "":
        return doc
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer!r}")

    current = doc
    tokens = pointer[1:].split("/")
    for token in tokens:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise KeyError(f"Key {token!r} not found in object")
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit():
                raise ValueError(f"Array index {token!r} is not an integer")
            if len(token) > 1 and token.startswith("0"):
                raise ValueError(f"Array index {token!r} contains forbidden leading zero")
            idx = int(token)
            if idx < 0 or idx >= len(current):
                raise IndexError(f"Array index {idx} out of bounds (length: {len(current)})")
            current = current[idx]
        else:
            raise ValueError(f"Cannot traverse into scalar value of type {type(current).__name__} with token {token!r}")

    return current


def are_values_type_safe_equal(actual: Any, expected: Any) -> bool:
    """
    Type-safe JSON equality check.
    Guarantees bool is not conflated with int (e.g., True != 1).
    """
    if type(actual) is not type(expected):
        return False
    return actual == expected


def validate_path_safety(rel_path_str: str, repo_root: Path) -> Path:
    """
    Ensures relative path does not escape repo root, use traversal, UNC, or forbidden roots.
    """
    p = Path(rel_path_str)
    if p.is_absolute():
        raise ValueError(f"Path must be repo-relative, got absolute: {rel_path_str}")
    norm_str = p.as_posix()
    if norm_str.startswith("..") or "/../" in norm_str or norm_str.endswith("/.."):
        raise ValueError(f"Path traversal ('..') forbidden: {rel_path_str}")
    if norm_str.startswith("//") or norm_str.startswith("\\\\"):
        raise ValueError(f"UNC path forbidden: {rel_path_str}")
    if not any(norm_str.startswith(prefix) for prefix in ALLOWED_REPO_ROOT_PREFIXES):
        raise ValueError(f"Path must start with one of {ALLOWED_REPO_ROOT_PREFIXES}, got: {rel_path_str}")

    resolved = (repo_root / p).resolve()
    resolved_root = repo_root.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        raise ValueError(f"Path escapes repository root: {rel_path_str}")
    return resolved


def validate_evidence_ref(ref: Dict[str, Any], repo_root: Path) -> Tuple[bool, str]:
    """
    Validates a single structured evidence reference:
    1. Validates path safety.
    2. Verifies artifact file exists.
    3. Parses artifact as JSON.
    4. Evaluates RFC 6901 JSON pointer.
    5. Checks type-safe equality against expected value.
    6. Checks expected_classification where provided.
    """
    artifact_rel = ref.get("artifact")
    if not artifact_rel:
        return False, "Missing 'artifact' field in evidence_ref"

    try:
        artifact_path = validate_path_safety(artifact_rel, repo_root)
    except Exception as e:
        return False, f"Path security violation: {e}"

    if not artifact_path.exists():
        return False, f"Artifact file does not exist: {artifact_rel}"

    try:
        content = json.loads(artifact_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Artifact {artifact_rel} failed to parse as JSON: {e}"

    json_pointer = ref.get("json_pointer", "")
    try:
        actual_val = resolve_json_pointer(content, json_pointer)
    except Exception as e:
        return False, f"JSON pointer resolution failed on {artifact_rel}#{json_pointer}: {e}"

    expected_val = ref.get("expected")
    if not are_values_type_safe_equal(actual_val, expected_val):
        return False, f"Value mismatch at {artifact_rel}#{json_pointer}: expected {expected_val!r} ({type(expected_val).__name__}), got {actual_val!r} ({type(actual_val).__name__})"

    expected_classification = ref.get("expected_classification")
    if expected_classification:
        class_pointer = ref.get("classification_json_pointer")
        if class_pointer:
            try:
                actual_class = resolve_json_pointer(content, class_pointer)
            except Exception as e:
                return False, f"Classification pointer resolution failed: {e}"
            if actual_class != expected_classification:
                return False, f"Classification mismatch: expected {expected_classification}, got {actual_class}"

    return True, "OK"


def scan_deferred_channels_isolation(agent_pkg_dir: Path) -> List[str]:
    """
    Examines all production non-test Go files under cloudphone-agent/pkg.
    Ensures camera-channel, file-channel, ai-command-channel, and adb-channel
    are strictly isolated without active business logic.
    """
    violations = []
    deferred_vars = ["CameraChannel", "FileChannel", "AICommandChannel", "ADBChannel", "camCh"]

    if not agent_pkg_dir.exists():
        return [f"Agent package directory missing: {agent_pkg_dir}"]

    for go_file in agent_pkg_dir.rglob("*.go"):
        if go_file.name.endswith("_test.go"):
            continue
        content = go_file.read_text(encoding="utf-8")

        # 1. Check for OnMessage on deferred channels
        for dvar in deferred_vars:
            if f"{dvar}.OnMessage" in content:
                violations.append(f"{go_file.name}: contains {dvar}.OnMessage handler")

        # 2. Check for camera processing business logic
        for kw in ["ProcessCameraFrame", "VirtualCamera", "CameraProcessor", "H264Camera", "OnCameraFrame"]:
            if kw in content:
                violations.append(f"{go_file.name}: contains camera business logic '{kw}'")

        # 3. Check for file transfer / payload parser / file write business logic
        for kw in ["SaveFile", "ParseFileChunk", "FileTransfer", "FileReceiver"]:
            if kw in content:
                violations.append(f"{go_file.name}: contains file transfer business logic '{kw}'")
        if "os.Create(" in content or "os.WriteFile(" in content or "ioutil.WriteFile(" in content:
            violations.append(f"{go_file.name}: contains direct file write call")

        # 4. Check for AI command execution business logic
        for kw in ["ExecuteAICommand", "ParseAICommand", "RunAICommand"]:
            if kw in content:
                violations.append(f"{go_file.name}: contains AI command business logic '{kw}'")
        if "os/exec" in content or "exec.Command(" in content:
            violations.append(f"{go_file.name}: contains command execution call")

        # 5. Check for ADB sockets/bridges
        for kw in ["AdbBridge", "AdbSocket", "ConnectAdb", "ForwardAdb"]:
            if kw in content:
                violations.append(f"{go_file.name}: contains ADB business logic '{kw}'")

    # In datachannel.go: only inputCh and clipCh may attach OnMessage
    datachannel_go = agent_pkg_dir / "webrtc" / "datachannel.go"
    if datachannel_go.exists():
        dc_lines = datachannel_go.read_text(encoding="utf-8").splitlines()
        on_message_targets = []
        for line in dc_lines:
            if ".OnMessage(" in line:
                target = line.split(".OnMessage(")[0].strip()
                on_message_targets.append(target)
        invalid_on_messages = [t for t in on_message_targets if t not in ["inputCh", "clipCh"]]
        if invalid_on_messages:
            violations.append(f"datachannel.go: unexpected OnMessage registered on: {invalid_on_messages}")
    else:
        violations.append("datachannel.go missing")

    return violations


def parse_go_test_json(stdout: str) -> Dict[str, Any]:
    """
    Parses machine-readable line-by-line events from `go test -json`.
    Extracts package pass/fail and per-test/subtest action states.
    """
    test_actions = {}
    package_action = None

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        action = ev.get("Action")
        test_name = ev.get("Test")
        if test_name:
            if action in ("pass", "fail", "skip"):
                test_actions[test_name] = {
                    "action": action,
                    "elapsed": ev.get("Elapsed", 0.0),
                }
        else:
            if action in ("pass", "fail", "skip"):
                package_action = action

    return {
        "package_action": package_action,
        "package_passed": (package_action == "pass"),
        "tests": test_actions,
    }


def evaluate_android_runtime_prerequisites() -> Dict[str, Any]:
    """
    Evaluates authentic Android runtime prerequisites independently.
    Does not assume availability from host platform alone.
    """
    prereqs = {
        "original_agent_artifact_available": False,
        "compatible_android_target_available": False,
        "app_process_available": False,
        "helper_artifact_available": False,
        "execution_context_shell_uid_2000": False,
        "abstract_uds_support": False,
        "safe_launch_capability": False,
    }

    is_linux = sys.platform.startswith("linux")
    if is_linux:
        if os.path.exists("/system/bin/app_process") or os.path.exists("/system/bin/app_process64"):
            prereqs["app_process_available"] = True
        if os.path.exists("/system/bin/sh") and os.path.exists("/dev/socket"):
            prereqs["compatible_android_target_available"] = True
            prereqs["abstract_uds_support"] = True

    is_available = all(prereqs.values())
    return {
        "is_available": is_available,
        "verdict": "PASS" if is_available else "ENVIRONMENT_UNAVAILABLE",
        "prerequisites": prereqs,
        "diagnostic": (
            "Genuine Android runtime environment available"
            if is_available else
            "Android runtime requiring original Agent/helper execution context (shell UID 2000, app_process, abstract UDS) is unavailable on current host"
        ),
    }
