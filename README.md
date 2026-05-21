# Founder Weekly Operating Review Agent

Generate a founder-ready weekly operating review from startup metrics and company context.

<!-- FOUNDER_OS_STANDARD_README -->

## Start here

| Reader | Open first | Why | CTA |
| --- | --- | --- | --- |
| Founder | `docs/sample_weekly_operating_review.md` | Inspect the committed weekly review before running anything. | Use the structure for the next operating review. |
| Non-technical operator | `examples/weekly_metrics.csv` | See the input shape for a weekly review. | Copy the columns into a private tracker. |
| Technical operator | `README.md#quick-start` | Run the local command and generate the demo output. | Compare `outputs/demo/weekly_operating_review.md` with the sample. |
| Hiring manager | `docs/sample_weekly_operating_review.md` | See how metrics, risks, asks, and next actions become cadence. | Review the memo for decision clarity. |

## Use this instead of adjacent repos when

| If the operating problem is... | Use this repo | Use the adjacent repo instead when... |
| --- | --- | --- |
| The founder needs one weekly packet across metrics, risks, asks, and next actions | Yes | Use source modules first if the underlying workflow is not yet structured. |
| Revenue, onboarding, retention, product, hiring, or AI signals need one cadence | Yes | Use the relevant source repo when the problem is diagnosing that function. |
| Investor or board narrative is the primary output | Not first | Use `board-pack-investor-update-agent` when the operating packet needs investor-ready narrative. |

## Non-technical starting point

If you are a founder and want the no-code version first, start with the matching kit in:
[Founder OS Adoption Kit](https://github.com/shubham1502-hue/founder-os-adoption-kit)

This repo is the deeper module. The adoption kit gives you the simple template, sample input, founder prompt, and sample output.

Start with the [Weekly Review Kit](https://github.com/shubham1502-hue/founder-os-adoption-kit/tree/main/starter-kits/weekly-review-kit).

## The founder problem

Weekly reviews become slow when metrics, risks, product issues, GTM movement, and team asks are assembled manually. Founders need one operating packet that shows what changed, what matters, and what decisions need attention.

## What this repo does

- reads weekly metrics and company context
- identifies changes, risks, priorities, and asks
- generates a CEO-ready weekly review memo
- creates an investor-safe narrative when needed

## What a founder gets in 10 minutes

- weekly operating review memo
- risk and priority list
- next-week execution plan
- investor-safe update language

## Before and after

Before:

- manual weekly reporting
- unclear decision points
- scattered metrics
- no reusable cadence

After:

- one weekly operating packet
- clear risks and priorities
- repeatable cadence
- founder-ready narrative

## Who this is for

- early-stage founders
- Founder's Office teams
- BizOps operators
- startup generalists
- board and investor reporting owners

## Quick start

- Run `python -m pip install -e .`.
- Run `PYTHONPATH=src python3 -m founder_weekly_review --metrics examples/weekly_metrics.csv --context examples/company_context.md --out outputs/demo`.
- Optional: override risk thresholds with `--config examples/thresholds.json`. Missing values fall back to defaults.
- Open `docs/sample_weekly_operating_review.md` first to inspect the committed demo. After running the command, open `outputs/demo/weekly_operating_review.md` locally.

## How to fork and use this for your company

1. Click Fork.
2. Rename the repo if needed.
3. Replace `examples/weekly_metrics.csv` with your weekly metrics.
4. Replace `examples/company_context.md` with company context.
5. Run the weekly review command.
6. Move decisions into Linear, Asana, ClickUp, Notion, or your internal ops tracker.

### Non-technical path

- Replace one CSV: `examples/weekly_metrics.csv`.
- Edit one context file: `examples/company_context.md`.
- Run one command.
- Read one committed demo first: `docs/sample_weekly_operating_review.md`.

## Input format

- weekly metrics CSV with growth, retention, activation, pipeline, runway, support, product, and operating notes where relevant
- company context describing stage, strategy, team, and constraints

The default sample data and examples are synthetic, anonymized, or template-only unless the repo explicitly documents a public source. Keep private customer, prospect, employee, investor, borrower, merchant, payment, or company data out of public forks.

## Output files

- `docs/sample_weekly_operating_review.md`: committed sample weekly review for quick inspection
- `outputs/demo/weekly_operating_review.md`: founder weekly review memo generated locally from the CLI

## Example founder workflow

- Monday: update metrics.
- Tuesday: run the weekly review.
- Wednesday: review risks and owners.
- Thursday: close decisions.
- Friday: roll decisions into next week and investor-safe notes.

## Customization guide

Customize these before using the repo for a real company:

- metric columns
- risk thresholds
- company context
- review sections
- decision owners

## Standalone or integrated

Standalone:
Use this repo by itself if you only need a weekly founder operating review from metrics, risks, asks, and company context. Fork it, replace the sample input, run the workflow or copy the templates, and use the main output in your next founder review.

Integrated:
Use this repo with the Founder OS ecosystem if you want to connect it to adjacent operating workflows.

- Use as the weekly review layer.
- Pull inputs from [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine), [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os), [founder-retention-expansion-os](https://github.com/shubham1502-hue/founder-retention-expansion-os), [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os), [founder-hiring-talent-pipeline-os](https://github.com/shubham1502-hue/founder-hiring-talent-pipeline-os), and [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent).
- Pull product decisions and customer signal themes from [founder-product-feedback-roadmap-os](https://github.com/shubham1502-hue/founder-product-feedback-roadmap-os).
- Use it even if you have no other repo.

## Lifecycle handoff

Before:

- [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine) for GTM and funnel risks.
- [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os) for onboarding and activation risks.
- [founder-retention-expansion-os](https://github.com/shubham1502-hue/founder-retention-expansion-os) for customer health, renewal risk, expansion opportunities, churn drivers, and proof opportunities.
- [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) for AI leverage priorities.
- [founder-hiring-talent-pipeline-os](https://github.com/shubham1502-hue/founder-hiring-talent-pipeline-os) for role priorities, candidate decisions, trial projects, reference checks, offer risks, and hiring bottlenecks.
- Weekly metrics from your internal tracker.

This repo produces:

- CEO-ready weekly operating review
- Risks and decisions
- Team asks
- Next-week plan

After:

- [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) for investor or board narrative.
- Founder and leadership decisions for the next operating cycle.

## Onboarding input

[Founder Customer Onboarding OS](https://github.com/shubham1502-hue/founder-customer-onboarding-os) can feed the weekly operating review with onboarding health, activation risk, founder attention accounts, SLA issues, owner gaps, and next actions.

## Retention and expansion input

[Founder Retention Expansion OS](https://github.com/shubham1502-hue/founder-retention-expansion-os) can feed the weekly operating review with customer health, renewal risk, expansion opportunities, churn drivers, proof opportunities, and founder attention accounts.

## Product roadmap input

[Founder Product Feedback Roadmap OS](https://github.com/shubham1502-hue/founder-product-feedback-roadmap-os) can feed the weekly operating review with roadmap decisions, repeated customer themes, product gaps, non-product fixes, discovery needs, owner actions, and product risks.

## Hiring pipeline input

[Founder Hiring Talent Pipeline OS](https://github.com/shubham1502-hue/founder-hiring-talent-pipeline-os) can feed the weekly operating review with role priorities, candidate decisions, trial projects, reference checks, offer risks, and hiring bottlenecks.

## Where this fits in the Founder OS

Use this as the weekly cadence layer. It can absorb signals from `founder-os-revenue-engine`, `founder-customer-onboarding-os`, `founder-retention-expansion-os`, `startup-metrics-playbook`, `founder-ai-workflow-roi-os`, `founder-hiring-talent-pipeline-os`, and `board-pack-investor-update-agent`.

## Why this matters

This is not a dashboard. It is the weekly operating review that turns metrics into decisions and next actions.

## Roadmap

- Google Sheets import
- Notion export
- Slack decision alerts
- board pack handoff
- AI-assisted narrative review

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) if present. Practical improvements are welcome when they make the workflow easier to fork, run, or adapt.

## License

MIT License. See [LICENSE](LICENSE).

## Built by

Built by Shubham Singh, a founder-facing operator focused on RevOps, GTM systems, startup metrics, AI workflows, and operating systems for early-stage teams.

## Use this in your company

Fork it, replace the sample inputs with your company context, and run the workflow. Start with the main output listed in the Quick Start section. Keep private data out of public forks.

## If you are a Founder's Office candidate

Use this repo to understand how a founder-facing operator turns messy inputs into decisions, cadence, and execution artifacts. Fork it, adapt it to a real company example, and write a short case note explaining what changed.

---

## Detailed implementation notes

The founder-facing guide above is the fastest path. The original repo-specific notes are preserved below for deeper implementation context.

## Problem This Solves

Founders lose time turning scattered weekly metrics into a clear operating narrative. The problem is not knowing the numbers; it is deciding what changed, what is risky, what needs action, and what can be safely shared with investors.

## How It Helps

- Converts a weekly metrics CSV and company context into a CEO-ready operating review.
- Produces risks, priorities, team asks, an investor-safe update, and a next-week execution plan.
- Gives founders and founder's office operators a forkable cadence for weekly business reviews before they have a full BizOps, RevOps, or FP&A function.

## When To Fork This

- Fork this if your weekly review is still built manually from spreadsheets, Slack notes, and founder memory.
- Fork it when leadership needs one operating packet that connects growth, churn, activation, pipeline, runway, support load, and product issues.
- Replace the sample metrics, thresholds, and output format with your company's operating cadence.

## Use This In Your Company

This repo is designed to be forked into an internal company workflow. Fork it, replace the sample inputs with your company context, and keep only the parts that match your operating cadence. No permission request or sales call is needed before using it; the repo is the handoff. Check the license if you plan to redistribute your version.

- Use it as a weekly operating review generator for founders and Founder Office teams.
- Keep the output set: CEO review, investor-safe update, risks, team asks, next-week plan, and JSON analysis.
- Replace only the weekly metrics CSV and company context to start.

## Minimum Edits To Make It Yours

Change these first:

| Edit | Where | Why |
|---|---|---|
| Replace weekly metrics. | `examples/weekly_metrics.csv` | This is the core input for risks, priorities, wins, blockers, and follow-ups. |
| Rewrite company context. | `examples/company_context.md` | Makes the review read like your business, not a generic demo. |
| Tune risk and priority logic. | `src/founder_weekly_review/analysis.py` | Adjusts what the system escalates to the founder. |
| Review the generated operating review. | output Markdown/report | Keeps judgment with the founder or operator before sharing. |

You can leave the reporting format, CLI, and sample output structure alone on the first fork. Run it with your metrics once before changing the analysis code.

## What It Produces

```text
weekly_operating_review.md  CEO-ready weekly review
investor_safe_update.md   External-safe investor narrative
team_asks.md         Clear asks by function
next_week_plan.md      Focus areas and execution plan
analysis.json        Structured metric deltas, risks, and priorities
```

## AI leverage input

[Founder AI Workflow ROI OS](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) can feed the weekly operating review with automation priorities, AI pilots, owner assignments, risk flags, and estimated savings.

## Quickstart

```bash
git clone https://github.com/shubham1502-hue/founder-weekly-operating-review-agent.git
cd founder-weekly-operating-review-agent

python3 -m founder_weekly_review \
 --metrics examples/weekly_metrics.csv \
 --context examples/company_context.md \
 --out outputs/demo
```

Then open the local generated outputs:

- `outputs/demo/weekly_operating_review.md`
- `outputs/demo/investor_safe_update.md`
- `outputs/demo/team_asks.md`
- `outputs/demo/next_week_plan.md`
- `outputs/demo/analysis.json`

## Demo Output Preview

See [docs/sample_weekly_operating_review.md](docs/sample_weekly_operating_review.md) for a generated example.

## Project Structure

```text
founder-weekly-operating-review-agent/
|-- examples/
|  |-- company_context.md
|  `-- weekly_metrics.csv
|-- src/founder_weekly_review/
|  |-- analysis.py
|  |-- cli.py
|  |-- metrics.py
|  `-- reporting.py
|-- tests/
|  `-- test_analysis.py
`-- README.md
```

## Metrics Expected

The sample CSV includes:

- MRR, new MRR, expansion MRR, churn MRR
- Active customers, new customers, churned customers
- Activation rate
- Pipeline value
- Cash balance, burn, runway
- Open support tickets
- NPS
- Open product issues

## Why This Matters

This repo is built for the founder's office job to be done: absorb messy operating signal, identify what deserves leadership attention, and convert it into a weekly cadence that makes decisions faster.

## License

MIT
