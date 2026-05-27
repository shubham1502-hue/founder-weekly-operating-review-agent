from __future__ import annotations

import html
import json
from pathlib import Path

from .analysis import money, percent


def write_outputs(analysis: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "weekly_operating_review.md").write_text(render_weekly_review(analysis), encoding="utf-8")
    (out_dir / "weekly_operating_review.html").write_text(render_weekly_review_html(analysis), encoding="utf-8")
    (out_dir / "investor_safe_update.md").write_text(render_investor_update(analysis), encoding="utf-8")
    (out_dir / "team_asks.md").write_text(render_team_asks(analysis), encoding="utf-8")
    (out_dir / "next_week_plan.md").write_text(
        render_next_week_plan(analysis), encoding="utf-8"
    )
    (out_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2), encoding="utf-8"
    )


def render_weekly_review(analysis: dict) -> str:
    latest = analysis["latest"]
    deltas = analysis["deltas"]
    lines = [
        f"# Weekly Operating Review: {latest['week']}",
        "",
        "## Headline",
        "",
        analysis["headline"],
        "",
        "## Metrics Snapshot",
        "",
        "| Metric | Latest | Change |",
        "|---|---:|---:|",
        f"| MRR | {money(latest['mrr'])} | {percent(deltas['mrr_growth'])} |",
        f"| Net New MRR | {money(latest['new_mrr'] + latest['expansion_mrr'] - latest['churn_mrr'])} | {percent(deltas['net_new_mrr_growth'])} |",
        f"| Activation Rate | {percent(latest['activation_rate'])} | {percent(deltas['activation_delta'])} pts |",
        f"| Pipeline Value | {money(latest['pipeline_value'])} | {percent(deltas['pipeline_growth'])} |",
        f"| Runway | {latest['runway_months']:.1f} months | n/a |",
        f"| Support Tickets Open | {latest['support_tickets_open']} | {percent(deltas['support_ticket_growth'])} |",
        f"| NPS | {latest['nps']:.0f} | n/a |",
        "",
        "## Risks",
        "",
    ]
    if analysis["risks"]:
        for risk in analysis["risks"]:
            lines.append(
                f"- **{risk['severity'].title()} - {risk['area'].title()}:** {risk['risk']} {risk['why_it_matters']}"
            )
    else:
        lines.append("- No material operating risk triggered this week.")

    lines.extend(["", "## Priorities", ""])
    lines.extend(
        f"{index}. {priority}"
        for index, priority in enumerate(analysis["priorities"], start=1)
    )
    lines.extend(["", "## Team Asks", ""])
    lines.extend(f"- **{ask['team']}:** {ask['ask']}" for ask in analysis["team_asks"])
    lines.extend(
        ["", "## Investor-Safe Summary", "", analysis["investor_safe_summary"], ""]
    )
    return "\n".join(lines)


def render_weekly_review_html(analysis: dict) -> str:
    latest = analysis["latest"]
    deltas = analysis["deltas"]
    risks = analysis["risks"] or [{
        "severity": "info",
        "area": "operations",
        "risk": "No material operating risk triggered this week.",
        "why_it_matters": "Keep monitoring the weekly trend.",
    }]

    def esc(value: object) -> str:
        return html.escape(str(value), quote=True)

    risk_items = "".join(
        f"<li><strong>{esc(risk['severity']).title()} - {esc(risk['area']).title()}:</strong> "
        f"{esc(risk['risk'])} {esc(risk['why_it_matters'])}</li>"
        for risk in risks
    )
    priority_items = "".join(f"<li>{esc(priority)}</li>" for priority in analysis["priorities"])
    ask_items = "".join(
        f"<li><strong>{esc(ask['team'])}:</strong> {esc(ask['ask'])}</li>"
        for ask in analysis["team_asks"]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Weekly Operating Review: {esc(latest['week'])}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.5; margin: 2rem auto; max-width: 900px; padding: 0 1rem; color: #172033; }}
    h1, h2 {{ line-height: 1.2; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d4d8e2; padding: 0.6rem; text-align: left; }}
    th {{ background: #f4f6fa; }}
    .headline {{ background: #fff7db; border-left: 4px solid #f2c94c; padding: 1rem; }}
  </style>
</head>
<body>
  <h1>Weekly Operating Review: {esc(latest['week'])}</h1>
  <h2>Headline</h2>
  <p class="headline">{esc(analysis['headline'])}</p>
  <h2>Metrics Snapshot</h2>
  <table>
    <thead><tr><th>Metric</th><th>Latest</th><th>Change</th></tr></thead>
    <tbody>
      <tr><td>MRR</td><td>{money(latest['mrr'])}</td><td>{percent(deltas['mrr_growth'])}</td></tr>
      <tr><td>Net New MRR</td><td>{money(latest['new_mrr'] + latest['expansion_mrr'] - latest['churn_mrr'])}</td><td>{percent(deltas['net_new_mrr_growth'])}</td></tr>
      <tr><td>Activation Rate</td><td>{percent(latest['activation_rate'])}</td><td>{percent(deltas['activation_delta'])} pts</td></tr>
      <tr><td>Pipeline Value</td><td>{money(latest['pipeline_value'])}</td><td>{percent(deltas['pipeline_growth'])}</td></tr>
      <tr><td>Runway</td><td>{latest['runway_months']:.1f} months</td><td>n/a</td></tr>
    </tbody>
  </table>
  <h2>Risks</h2>
  <ul>{risk_items}</ul>
  <h2>Priorities</h2>
  <ol>{priority_items}</ol>
  <h2>Team Asks</h2>
  <ul>{ask_items}</ul>
  <h2>Investor-Safe Summary</h2>
  <p>{esc(analysis['investor_safe_summary'])}</p>
</body>
</html>
"""


def render_investor_update(analysis: dict) -> str:
    latest = analysis["latest"]
    return "\n".join(
        [
            f"# Investor Update Draft: {latest['week']}",
            "",
            analysis["investor_safe_summary"],
            "",
            "## Current Focus",
            "",
            *[f"- {priority}" for priority in analysis["priorities"][:3]],
            "",
        ]
    )


def render_team_asks(analysis: dict) -> str:
    latest = analysis["latest"]
    lines = [f"# Team Asks: {latest['week']}", ""]
    lines.extend(f"- **{ask['team']}:** {ask['ask']}" for ask in analysis["team_asks"])
    lines.append("")
    return "\n".join(lines)


def render_next_week_plan(analysis: dict) -> str:
    latest = analysis["latest"]
    lines = [
        f"# Next Week Operating Plan: {latest['week']}",
        "",
        "## Focus",
        "",
    ]
    lines.extend(
        f"{index}. {priority}"
        for index, priority in enumerate(analysis["priorities"], start=1)
    )
    lines.extend(
        [
            "",
            "## Founder Checkpoints",
            "",
            "- Monday: confirm the one growth constraint and one product constraint.",
            "- Wednesday: review pipeline movement, support load, and activation blockers.",
            "- Friday: decide what moves into the next investor update.",
            "",
        ]
    )
    return "\n".join(lines)
