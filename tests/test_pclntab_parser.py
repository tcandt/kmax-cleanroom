import os
import sys
import unittest
from pathlib import Path

# Add repo root to sys.path portably
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root, parse_elf_sections, parse_pclntab

ROOT = get_repo_root()
SIGNALING_LINUX = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
AGENT_ARM64 = ROOT / "cloudphone-v0.3.6 (1)" / "android" / "cloudphone-agent"

class TestPclntabParserInvariants(unittest.TestCase):
    def test_path_portability(self):
        self.assertTrue(ROOT.exists(), f"Repo root does not exist: {ROOT}")
        self.assertTrue(SIGNALING_LINUX.exists(), f"Signaling binary missing: {SIGNALING_LINUX}")
        self.assertTrue(AGENT_ARM64.exists(), f"Agent binary missing: {AGENT_ARM64}")

    def test_signaling_linux_invariants(self):
        with open(SIGNALING_LINUX, "rb") as f:
            data = f.read()
        secs = parse_elf_sections(data)
        self.assertIn(".gopclntab", secs)
        self.assertIn(".text", secs)
        self.assertIn(".rodata", secs)

        pcln_data = data[secs[".gopclntab"]["offset"] : secs[".gopclntab"]["offset"] + secs[".gopclntab"]["size"]]
        res = parse_pclntab(pcln_data)

        # Invariant 1: ptrSize is 4 or 8
        self.assertIn(res["ptrSize"], (4, 8))
        self.assertEqual(res["ptrSize"], 8)

        # Invariant 2: Total entries parsed equals header nfunc
        self.assertEqual(res["nfunc"], 7571)
        self.assertEqual(res["entries_parsed"], 7571)

        # Invariant 3: entryoff is strictly monotonically ascending
        self.assertTrue(res["monotonic_ascending"])

        # Invariant 4: No overlapping function ranges & function end > function start
        self.assertTrue(res["non_overlapping"])
        self.assertTrue(res["size_valid"])

        # Invariant 5: Sentinel entry exists and is valid
        self.assertTrue(res["sentinel_valid"])

        # Invariant 6: Zero out-of-range funcoff or nameoff
        self.assertEqual(res["out_of_range_funcoff"], 0)
        self.assertEqual(res["out_of_range_nameoff"], 0)
        self.assertEqual(res["invalid_names"], 0)

        # Invariant 7: Preserved standard library and runtime symbols exist
        names = [f["name"] for f in res["functions"]]
        self.assertTrue(any(n.startswith("runtime.") for n in names))
        self.assertTrue(any(n.startswith("reflect.") for n in names))
        self.assertTrue(any(n.startswith("sync.") for n in names))
        self.assertTrue(any(n.startswith("syscall.") for n in names))
        self.assertTrue(any("internal/abi" in n for n in names))

    def test_agent_arm64_invariants(self):
        with open(AGENT_ARM64, "rb") as f:
            data = f.read()
        secs = parse_elf_sections(data)
        self.assertIn(".gopclntab", secs)
        self.assertIn(".text", secs)
        self.assertIn(".rodata", secs)

        pcln_data = data[secs[".gopclntab"]["offset"] : secs[".gopclntab"]["offset"] + secs[".gopclntab"]["size"]]
        res = parse_pclntab(pcln_data)

        # Invariant 1: ptrSize is 4 or 8
        self.assertIn(res["ptrSize"], (4, 8))
        self.assertEqual(res["ptrSize"], 8)

        # Invariant 2: Total entries parsed equals header nfunc
        self.assertEqual(res["nfunc"], 15398)
        self.assertEqual(res["entries_parsed"], 15398)

        # Invariant 3: entryoff is strictly monotonically ascending
        self.assertTrue(res["monotonic_ascending"])

        # Invariant 4: No overlapping function ranges & function end > function start
        self.assertTrue(res["non_overlapping"])
        self.assertTrue(res["size_valid"])

        # Invariant 5: Sentinel entry exists and is valid
        self.assertTrue(res["sentinel_valid"])

        # Invariant 6: Zero out-of-range funcoff or nameoff
        self.assertEqual(res["out_of_range_funcoff"], 0)
        self.assertEqual(res["out_of_range_nameoff"], 0)
        self.assertEqual(res["invalid_names"], 0)

        # Invariant 7: Preserved symbols
        names = [f["name"] for f in res["functions"]]
        self.assertTrue(any("internal/abi" in n for n in names))
        self.assertTrue(any("runtime." in n for n in names))

if __name__ == "__main__":
    unittest.main()
