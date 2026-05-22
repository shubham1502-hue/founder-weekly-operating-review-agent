from pathlib import Path
import tempfile
import unittest

from founder_weekly_review.analysis import analyze
from founder_weekly_review.metrics import load_metrics
from founder_weekly_review.reporting import render_weekly_review, write_outputs


ROOT = Path(__file__).resolve().parents[1]


class WeeklyReviewTests(unittest.TestCase):
    def test_load_metrics_and_build_analysis(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics, context="Test context")

        self.assertEqual(result["latest"]["week"], "2026-W06")
        self.assertGreater(result["deltas"]["mrr_growth"], 0)
        self.assertGreaterEqual(len(result["risks"]), 1)
        self.assertGreaterEqual(len(result["priorities"]), 1)


    def test_weekly_review_includes_key_founder_sections(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics)

        rendered = render_weekly_review(result)

        self.assertIn("## Headline", rendered)
        self.assertIn("## Metrics Snapshot", rendered)
        self.assertIn("## Risks", rendered)
        self.assertIn("## Priorities", rendered)
        self.assertIn("## Team Asks", rendered)
        self.assertIn("## Investor-Safe Summary", rendered)

    def test_writes_expected_outputs(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics)

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            write_outputs(result, out_dir)
            self.assertTrue((out_dir / "weekly_operating_review.md").exists())
            self.assertTrue((out_dir / "investor_safe_update.md").exists())
            self.assertTrue((out_dir / "team_asks.md").exists())
            self.assertTrue((out_dir / "next_week_plan.md").exists())
            self.assertTrue((out_dir / "analysis.json").exists())


if __name__ == "__main__":
    unittest.main()
