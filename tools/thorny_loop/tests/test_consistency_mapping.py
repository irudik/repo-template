"""Tests for manuscript/output consistency helpers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.thorny_loop.consistency import detect_consistency_risk, scan_manuscript_for_outputs


class ConsistencyMappingTest(unittest.TestCase):
    """Detect manuscript references to generated outputs."""

    def test_scan_manuscript_maps_output_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            latex_dir = repo_root / "latex"
            latex_dir.mkdir(parents=True, exist_ok=True)
            (latex_dir / "manuscript.tex").write_text("\\input{revenue_estimate.txt}\n")

            references = scan_manuscript_for_outputs(repo_root)

            self.assertIn("output/numbers/revenue_estimate.txt", references)

    def test_detect_consistency_risk_for_code_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            latex_dir = repo_root / "latex"
            latex_dir.mkdir(parents=True, exist_ok=True)
            (latex_dir / "manuscript.tex").write_text("\\input{revenue_estimate.txt}\nA result in prose.\n")

            finding = detect_consistency_risk(
                repo_root,
                ["code/simulation/main.jl"],
                "Fix why manuscript numbers disagree",
            )

            self.assertTrue(finding.risky)
            self.assertIn("output/numbers/revenue_estimate.txt", finding.referenced_outputs)


if __name__ == "__main__":
    unittest.main()
