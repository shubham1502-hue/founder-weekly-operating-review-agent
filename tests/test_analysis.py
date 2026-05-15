from pathlib import Path
import tempfile
import unittest

from founder_weekly_review.analysis import analyze
from founder_weekly_review.metrics import load_metrics
from founder_weekly_review.reporting import write_outputs


ROOT = Path(__file__).resolve().parents[1]


class WeeklyReviewTests(unittest.TestCase):
    def test_load_metrics_and_build_analysis(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics, context="Test context")

        self.assertEqual(result["latest"]["week"], "2026-W06")
        self.assertGreater(result["deltas"]["mrr_growth"], 0)
        self.assertGreaterEqual(len(result["risks"]), 1)
        self.assertGreaterEqual(len(result["priorities"]), 1)

    def test_writes_expected_outputs(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics)

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            write_outputs(result, out_dir)

            weekly_review = out_dir / "weekly_operating_review.md"
            investor_update = out_dir / "investor_safe_update.md"

            self.assertTrue(weekly_review.exists())
            self.assertTrue(investor_update.exists())
            self.assertTrue((out_dir / "team_asks.md").exists())
            self.assertTrue((out_dir / "next_week_plan.md").exists())
            self.assertTrue((out_dir / "analysis.json").exists())

            review_text = weekly_review.read_text()
            investor_text = investor_update.read_text()

            # Founder-facing weekly review sections
            self.assertIn("Executive Summary", review_text)
            self.assertIn("Metrics Snapshot", review_text)
            self.assertIn("Risks", review_text)
            self.assertIn("Priorities", review_text)
            self.assertIn("Team Asks", review_text)

            # Investor-safe update content
            self.assertTrue(
                "Investor-Safe Summary" in investor_text
                or "Investor Update" in investor_text
            )


if __name__ == "__main__":
    unittest.main()
