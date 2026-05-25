# Weekly metrics CSV schema

`examples/weekly_metrics.csv` is the default input for the weekly operating review. Each row represents one reporting week, and the CLI turns the trend across those rows into the generated memo, risk list, priorities, and next-week operating plan.

| Column | Required | Expected value |
| --- | --- | --- |
| `week` | Yes | Reporting week label, for example `2026-W04`. |
| `mrr` | Yes | Current monthly recurring revenue as a number. |
| `new_mrr` | Yes | New MRR added during the week as a number. |
| `expansion_mrr` | Yes | Expansion or upsell MRR added during the week as a number. |
| `churn_mrr` | Yes | MRR lost to churn during the week as a number. |
| `active_customers` | Yes | Count of active customers at week end. |
| `new_customers` | Yes | Count of customers added during the week. |
| `churned_customers` | Yes | Count of customers lost during the week. |
| `activation_rate` | Yes | Decimal activation rate, for example `0.62` for 62%. |
| `pipeline_value` | Yes | Current sales pipeline value as a number. |
| `cash_balance` | Yes | Current cash balance as a number. |
| `burn` | Yes | Weekly or monthly burn value used by the operating review. |
| `runway_months` | Yes | Remaining runway in months, for example `9.3`. |
| `support_tickets_open` | Yes | Count of unresolved support tickets. |
| `nps` | Yes | Net Promoter Score as a number. |
| `product_issues_open` | Yes | Count of unresolved product issues. |

Keep private company, customer, investor, or employee data out of public forks. Copy this schema into a private tracker before using real metrics.
