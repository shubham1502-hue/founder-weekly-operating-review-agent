from __future__ import annotations

from dataclasses import asdict

from .metrics import WeeklyMetrics

DEFAULT_THRESHOLDS = {
    "runway_months": 6,
    "churn_rate": 0.06,
    "activation_drop": 0.03,
    "support_growth": 0.15,
    "nps": 30,
}


def pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous


def pp_change(current: float, previous: float) -> float:
    return current - previous


def money(value: float) -> str:
    return f"${value:,.0f}"


def percent(value: float) -> str:
    return f"{value:.1%}"


def analyze(metrics: list[WeeklyMetrics], context: str = "", thresholds=None) -> dict:

    if len(metrics) < 2:
        raise ValueError("At least two weeks of metrics are required.")
    final_thresholds = DEFAULT_THRESHOLDS.copy()
    if thresholds:
        final_thresholds.update(thresholds)
    previous = metrics[-2]
    latest = metrics[-1]
    mrr_growth = pct_change(latest.mrr, previous.mrr)
    net_new_growth = pct_change(latest.net_new_mrr, previous.net_new_mrr)
    activation_delta = pp_change(latest.activation_rate, previous.activation_rate)
    pipeline_growth = pct_change(latest.pipeline_value, previous.pipeline_value)
    support_growth = pct_change(
        latest.support_tickets_open, previous.support_tickets_open
    )
    product_issue_change = latest.product_issues_open - previous.product_issues_open
    churn_rate = latest.churn_mrr / max(previous.mrr, 1)
    burn_multiple = latest.burn / max(latest.net_new_mrr, 1)
    pipeline_to_burn = latest.pipeline_value / max(latest.burn, 1)

    deltas = {
        "mrr_growth": mrr_growth,
        "net_new_mrr_growth": net_new_growth,
        "activation_delta": activation_delta,
        "pipeline_growth": pipeline_growth,
        "support_ticket_growth": support_growth,
        "product_issue_change": product_issue_change,
        "churn_rate": churn_rate,
        "burn_multiple": burn_multiple,
        "pipeline_to_monthly_burn": pipeline_to_burn,
    }

    risks = build_risks(latest, previous, deltas, final_thresholds)
    priorities = build_priorities(latest, deltas, risks)
    team_asks = build_team_asks(latest, deltas, risks)

    return {
        "context": context.strip(),
        "latest": asdict(latest),
        "previous": asdict(previous),
        "deltas": deltas,
        "headline": build_headline(latest, deltas, risks, final_thresholds),
        "risks": risks,
        "priorities": priorities,
        "team_asks": team_asks,
        "investor_safe_summary": build_investor_summary(latest, deltas, risks),
    }


def build_headline(
    latest: WeeklyMetrics, deltas: dict[str, float], risks: list[dict], thresholds
) -> str:
    if latest.runway_months < thresholds["runway_months"]:
        return (
            f"{latest.week}: growth is continuing, but runway is now the operating constraint. "
            f"MRR grew {percent(deltas['mrr_growth'])} while runway fell to {latest.runway_months:.1f} months."
        )
    if risks:
        return (
            f"{latest.week}: MRR grew {percent(deltas['mrr_growth'])}, "
            f"but {len(risks)} operating risks need leadership attention."
        )
    return f"{latest.week}: metrics are directionally healthy and execution should stay focused."


def build_risks(
    latest: WeeklyMetrics, previous: WeeklyMetrics, deltas: dict[str, float], thresholds
) -> list[dict]:
    # Use thresholds passed from CLI or defaults
    # Each risk comparison uses thresholds to determine if it should be triggered
    risks: list[dict] = []
    if latest.runway_months < thresholds["runway_months"]:
        risks.append(
            {
                "severity": "high",
                "area": "cash",
                "risk": f"Runway is {latest.runway_months:.1f} months.",
                "why_it_matters": "The company needs tighter prioritization before fundraising pressure increases.",
            }
        )
    if deltas["churn_rate"] > thresholds["churn_rate"]:
        risks.append(
            {
                "severity": "medium",
                "area": "retention",
                "risk": f"Churn MRR is {money(latest.churn_mrr)}, or {percent(deltas['churn_rate'])} of previous MRR.",
                "why_it_matters": "Growth quality is weaker if new revenue is offset by preventable churn.",
            }
        )
    if deltas["activation_delta"] < (-1) * thresholds["activation_drop"]:
        risks.append(
            {
                "severity": "medium",
                "area": "activation",
                "risk": f"Activation moved from {percent(previous.activation_rate)} to {percent(latest.activation_rate)}.",
                "why_it_matters": "Lower activation will reduce downstream conversion and customer expansion.",
            }
        )
    if deltas["support_ticket_growth"] > thresholds["support_growth"]:
        risks.append(
            {
                "severity": "medium",
                "area": "support",
                "risk": f"Open support tickets rose {percent(deltas['support_ticket_growth'])}.",
                "why_it_matters": "Support load can slow onboarding and reduce founder-led GTM quality.",
            }
        )
    if latest.nps < thresholds["nps"]:
        risks.append(
            {
                "severity": "medium",
                "area": "customer sentiment",
                "risk": f"NPS is {latest.nps:.0f}.",
                "why_it_matters": "Low customer sentiment can show up later as churn, expansion drag, and weaker referrals.",
            }
        )
    return risks


def build_priorities(
    latest: WeeklyMetrics, deltas: dict[str, float], risks: list[dict]
) -> list[str]:
    priorities: list[str] = []
    risk_areas = {risk["area"] for risk in risks}

    if "cash" in risk_areas:
        priorities.append(
            "Cut or delay non-critical spend and define the next fundraising-readiness milestone."
        )
    if "retention" in risk_areas:
        priorities.append(
            "Run a churn review on the latest lost accounts and create a save playbook for at-risk customers."
        )
    if "activation" in risk_areas or latest.product_issues_open > 30:
        priorities.append(
            "Make activation recovery the product focus: fix onboarding blockers and reduce open product issues."
        )
    if deltas["pipeline_growth"] > 0.1:
        priorities.append(
            "Convert pipeline quality into booked meetings and identify which segment is producing qualified demand."
        )
    if not priorities:
        priorities.append(
            "Keep the weekly operating focus on compounding the current growth motion."
        )

    return priorities[:4]


def build_team_asks(
    latest: WeeklyMetrics, deltas: dict[str, float], risks: list[dict]
) -> list[dict]:
    asks = [
        {
            "team": "GTM",
            "ask": "Review the top 10 pipeline accounts and identify the highest-conviction next action for each.",
        },
        {
            "team": "Product",
            "ask": "Triage activation blockers and close the issues most likely to affect new customer onboarding.",
        },
        {
            "team": "Founder/Finance",
            "ask": "Reforecast runway using current burn and decide which spend is mandatory for next week's plan.",
        },
    ]
    if latest.support_tickets_open > 120:
        asks.append(
            {
                "team": "Support/Ops",
                "ask": "Segment open tickets by root cause and escalate the top two recurring issues to product.",
            }
        )
    return asks


def build_investor_summary(
    latest: WeeklyMetrics, deltas: dict[str, float], risks: list[dict]
) -> str:
    risk_text = (
        "Runway and operating load remain the main areas under active management."
        if risks
        else "No major operating risk changed materially this week."
    )
    return (
        f"MRR reached {money(latest.mrr)}, up {percent(deltas['mrr_growth'])} week over week. "
        f"Pipeline grew {percent(deltas['pipeline_growth'])} to {money(latest.pipeline_value)}. "
        f"{risk_text} The team is focused on activation quality, pipeline conversion, and runway discipline."
    )
