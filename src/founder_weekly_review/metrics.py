from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen


@dataclass(frozen=True)
class WeeklyMetrics:
    week: str
    mrr: float
    new_mrr: float
    expansion_mrr: float
    churn_mrr: float
    active_customers: int
    new_customers: int
    churned_customers: int
    activation_rate: float
    pipeline_value: float
    cash_balance: float
    burn: float
    runway_months: float
    support_tickets_open: int
    nps: float
    product_issues_open: int

    @property
    def net_new_mrr(self) -> float:
        return self.new_mrr + self.expansion_mrr - self.churn_mrr

    @property
    def gross_new_mrr(self) -> float:
        return self.new_mrr + self.expansion_mrr


def _float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _int(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def load_metrics(path: Path) -> list[WeeklyMetrics]:
    with path.open(newline="", encoding="utf-8") as handle:
        return parse_metrics_csv(handle)


def load_metrics_from_url(url: str) -> list[WeeklyMetrics]:
    with urlopen(url, timeout=20) as response:
        payload = response.read().decode("utf-8-sig")
    return parse_metrics_csv(io.StringIO(payload))


def parse_metrics_csv(handle) -> list[WeeklyMetrics]:
    rows = list(csv.DictReader(handle))

    if len(rows) < 2:
        raise ValueError("At least two weeks of metrics are required.")

    required = set(WeeklyMetrics.__dataclass_fields__)
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    metrics = [
        WeeklyMetrics(
            week=row["week"],
            mrr=_float(row, "mrr"),
            new_mrr=_float(row, "new_mrr"),
            expansion_mrr=_float(row, "expansion_mrr"),
            churn_mrr=_float(row, "churn_mrr"),
            active_customers=_int(row, "active_customers"),
            new_customers=_int(row, "new_customers"),
            churned_customers=_int(row, "churned_customers"),
            activation_rate=_float(row, "activation_rate"),
            pipeline_value=_float(row, "pipeline_value"),
            cash_balance=_float(row, "cash_balance"),
            burn=_float(row, "burn"),
            runway_months=_float(row, "runway_months"),
            support_tickets_open=_int(row, "support_tickets_open"),
            nps=_float(row, "nps"),
            product_issues_open=_int(row, "product_issues_open"),
        )
        for row in rows
    ]
    return metrics
