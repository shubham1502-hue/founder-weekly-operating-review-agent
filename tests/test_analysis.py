import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from founder_weekly_review.analysis import analyze  # noqa: E402
from founder_weekly_review.metrics import load_metrics  # noqa: E402
from founder_weekly_review.reporting import render_weekly_review, write_outputs  # noqa: E402


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
            self.assertTrue((out_dir / "weekly_operating_review.html").exists())
            self.assertTrue((out_dir / "investor_safe_update.md").exists())
            self.assertTrue((out_dir / "team_asks.md").exists())
            self.assertTrue((out_dir / "next_week_plan.md").exists())
            self.assertTrue((out_dir / "analysis.json").exists())

    # Custom threshold test: ensures JSON config affects risks
    # Threshold values are read dynamically from examples/thresholds.json
    # This verifies that risks are correctly triggered or suppressed
    def test_custom_thresholds_loaded_from_json(self):
        # Load metrics
        metrics = load_metrics(ROOT / "examples/weekly_metrics.csv")

        # Load thresholds from JSON (like CLI)
        threshold_file = ROOT / "examples/thresholds.json"
        import json

        with threshold_file.open("r", encoding="utf-8") as f:
            thresholds = json.load(f)

        # Run analysis with thresholds
        result = analyze(metrics, thresholds=thresholds)

        # Extract risk areas
        risk_areas = [r["area"] for r in result["risks"]]

        # Check each metric threshold
        if thresholds["runway_months"] > metrics[-1].runway_months:
            self.assertIn("cash", risk_areas)
        else:
            self.assertNotIn("cash", risk_areas)

        if thresholds["churn_rate"] < metrics[-1].churn_mrr / max(metrics[-2].mrr, 1):
            self.assertIn("retention", risk_areas)
        else:
            self.assertNotIn("retention", risk_areas)
        activation_delta = metrics[-1].activation_rate - metrics[-2].activation_rate
        if activation_delta < -thresholds["activation_drop"]:
            self.assertIn("activation", risk_areas)
        else:
            self.assertNotIn("activation", risk_areas)


        if thresholds["support_growth"] < (
            metrics[-1].support_tickets_open - metrics[-2].support_tickets_open
        ) / max(metrics[-2].support_tickets_open, 1):
            self.assertIn("support", risk_areas)
        else:
            self.assertNotIn("support", risk_areas)

        if thresholds["nps"] > metrics[-1].nps:
            self.assertIn("customer sentiment", risk_areas)
        else:
            self.assertNotIn("customer sentiment", risk_areas)


    def test_activation_threshold_triggers_and_not(self):
        from founder_weekly_review.metrics import WeeklyMetrics

        base = dict(
            mrr=50000.0,
            new_mrr=5000.0,
            expansion_mrr=1000.0,
            churn_mrr=0.0,
            active_customers=100,
            new_customers=10,
            churned_customers=0,
            pipeline_value=200000.0,
            cash_balance=500000.0,
            burn=50000.0,
            runway_months=12.0,
            support_tickets_open=50,
            nps=50.0,
            product_issues_open=5,
        )
        previous = WeeklyMetrics(week="2026-W01", activation_rate=0.60, **base)

        # Drop of 0.10 exceeds threshold of 0.05 → activation risk triggered
        latest_big_drop = WeeklyMetrics(week="2026-W02", activation_rate=0.50, **base)
        result = analyze([previous, latest_big_drop], thresholds={"activation_drop": 0.05})
        self.assertIn("activation", [r["area"] for r in result["risks"]])

        # Drop of 0.02 stays within threshold of 0.05 → activation risk not triggered
        latest_small_drop = WeeklyMetrics(week="2026-W02", activation_rate=0.58, **base)
        result2 = analyze([previous, latest_small_drop], thresholds={"activation_drop": 0.05})
        self.assertNotIn("activation", [r["area"] for r in result2["risks"]])


if __name__ == "__main__":
    unittest.main()
