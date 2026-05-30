import unittest
from unittest.mock import patch

from founder_weekly_review.cli import main

CSV_PAYLOAD = """week,mrr,new_mrr,expansion_mrr,churn_mrr,active_customers,new_customers,churned_customers,activation_rate,pipeline_value,cash_balance,burn,runway_months,support_tickets_open,nps,product_issues_open
2026-W01,100,10,5,1,10,2,0,0.5,1000,5000,100,10,3,40,2
2026-W02,120,12,6,2,12,3,1,0.6,1200,4900,100,9,4,42,3
"""


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return CSV_PAYLOAD.encode("utf-8")


class GoogleSheetImportTests(unittest.TestCase):
    def test_cli_downloads_published_sheet_csv(self):
        with patch("founder_weekly_review.metrics.urlopen", return_value=FakeResponse()) as urlopen:
            with self.subTest("run"):
                with unittest.mock.patch("founder_weekly_review.cli.write_outputs") as write_outputs:
                    result = main(["--google-sheet-csv-url", "https://docs.google.com/spreadsheets/d/example/export?format=csv"])

        self.assertEqual(result, 0)
        urlopen.assert_called_once()
        analysis = write_outputs.call_args.args[0]
        self.assertEqual(analysis["latest"]["week"], "2026-W02")


if __name__ == "__main__":
    unittest.main()
