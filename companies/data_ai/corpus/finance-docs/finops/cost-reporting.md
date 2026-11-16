# The monthly cloud cost report

Owner: FinOps (cloud cost) · Last edited by Rahul Muller

The monthly cloud cost report is issued on the second working day of each month for the prior month, with a preliminary version on the first working day. It is published to the BI dashboards and announced in #finops. The numbers come from the billing export that lands in the warehouse and is refreshed every few hours, so unless a month is still open the report reflects everything invoiced or metered up to the end of the prior month.

## What the report shows

| Sheet | Contents |
| --- | --- |
| Spend by account and team | Cloud spend broken down by cloud account and by the team that owns the workload, using the tags from `finance-docs/finops/cost-tags.md`. |
| Unit costs | Cost per satellite image processed, per sensor reading ingested, per API call served, per training GPU-hour. See `finance-docs/finops/unit-costs.md` for how these are calculated. |
| Month-on-month movement | Absolute and percentage change per account and per team, with the three largest movers called out in a short note. |
| Showback detail | Line-level showback for each team: which accounts, projects and cost centres they are charged to, so teams can reconcile against their own records. |

## Where the numbers come from

The billing export for all cloud providers is pulled into the warehouse on a schedule that runs every few hours. The report reads from the warehouse tables in the `finops` schema, which are maintained by the data platform team. If a table is missing data for a day, the report shows the gap in a footnote rather than estimating it.

## Who gets it

- **Finance** (Tom Keane and Petra Keller) for the period close pack.
- **All team leads** for their team's showback lines.
- **FinOps** for the commitment and budget review that happens the same week.
- **The cloud platform team** for capacity planning conversations.

The report is not sent as an attachment. Teams are expected to read it from the BI dashboards. A short summary with the headline numbers is posted in #finops and #finance.

## How teams read the showback lines

Each team sees their own spend by account and project, using the same tags as the budgets. Read the showback lines against the team's budget:

| Column | What it means |
| --- | --- |
| Account | The cloud account the spend landed in. |
| Project | The project tag on the resources. |
| Team | The team responsible for the workload, from the tag. |
| Spend | Total for the month, in EUR. |
| Budget | The team's share of the finance-period budget, pro-rated to the calendar month. |
| Burn | Spend divided by budget, as a percentage. |

If a team's burn is above 100%, the report's note explains which account and project drove it. Teams do not need to raise a ticket to ask for the breakdown — the detail is in the dashboard under the same name.

The report also shows the cost per unit for the main products: monitoring subscriptions, imagery tasking orders and the analytics API. These are computed from the same warehouse tables and are used by pricing discussions in commercial-docs/sales/pricing-and-packaging.md.
