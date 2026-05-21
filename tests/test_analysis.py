from pathlib import Path
import tempfile
import unittest

from founder_weekly_review.analysis import analyze, merge_thresholds
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

    def test_custom_thresholds_override_defaults(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        default_result = analyze(metrics)
        custom_result = analyze(metrics, thresholds={"nps_medium_risk": 60})

        default_areas = {risk["area"] for risk in default_result["risks"]}
        custom_areas = {risk["area"] for risk in custom_result["risks"]}

        self.assertNotIn("customer sentiment", default_areas)
        self.assertIn("customer sentiment", custom_areas)

    def test_missing_threshold_values_fall_back_to_defaults(self):
        thresholds = merge_thresholds({"nps_medium_risk": 60})

        self.assertEqual(thresholds["nps_medium_risk"], 60)
        self.assertEqual(thresholds["runway_months_high_risk"], 6)

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
