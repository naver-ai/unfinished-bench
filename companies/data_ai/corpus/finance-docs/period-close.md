# Period close

Owner: Accounting, AP and payroll · Last edited by: Jin Kowalski · Applies to: Brakwater Geo B.V. and Brakwater Geo US Inc.

## Calendar

The financial year runs from January and is divided into thirteen four-week periods. The first three quarters each have three periods; Q4 has four periods. Each period closes on the last working day of the period (WD0). The close runs from WD-2 to WD+4.

| Working day | Activity | Owner |
|---|---|---|
| WD-2 | Cloud billing export pulled from the warehouse; accrual draft prepared | Accounting, AP and payroll |
| WD-2 | Imagery provider invoices expected; anything missing is flagged to Ana's team | Accounting, AP and payroll |
| WD-1 | Accrual entries posted; intercompany recharges drafted | Accounting, AP and payroll |
| WD-1 | Subscription revenue recognition run for the period | Accounting, AP and payroll |
| WD0 | Period closes; last day for adjusting entries | Accounting, AP and payroll |
| WD+1 | Intercompany entries posted; balances agreed between B.V. and US entity | Accounting, AP and payroll |
| WD+2 | Reporting pack issued to Finance | Accounting, AP and payroll |
| WD+3 | Review with Tom Keane; open items resolved | Finance |
| WD+4 | Final reporting pack published; period marked closed in the BI dashboards | Accounting, AP and payroll |

## Journals and accruals

All journals go through the accounting system with a period reference. Use the standard journal template from the finance-docs folder. Attach supporting detail to each entry — for accruals that means the underlying calculation or the invoice line items.

Accruals are posted in the following areas:

| Accrual | Basis | Notes |
|---|---|---|
| Cloud bill | Billing export (warehouse `finops` schema) | Accrue from the export even if the invoice has not arrived. Split across B.V. and US entity per the tag split in the export. |
| Imagery provider invoices | Purchase orders and delivery notes | Some providers invoice late. Accrue the expected amount per the PO when the imagery has been delivered but the invoice is missing. Flag to Imagery acquisition and processing at WD-2. |
| Sensor network site costs | Lease and service agreements | Accrue per the agreement schedule; reconcile quarterly. |
| Professional fees | Engagement letters | Accrue when the service has been delivered but the invoice is pending. |

## Revenue recognition

Subscription revenue is recognised evenly over the subscription term. The revenue recognition run happens at WD-1 and covers all active subscriptions in the billing system. The run picks up new subscriptions, renewals and cancellations effective in the period.

Imagery tasking orders are recognised when the imagery is delivered to the customer. If delivery crosses a period boundary, recognise the portion delivered up to WD0 and accrue the remainder. The tasking portal shows delivery status per order; use that as the source for the split.

Analytics API usage is recognised based on metered usage from the customer API console. The metre is pulled at WD-1 and posted as usage-based revenue.

## Intercompany

Intercompany entries are posted between the B.V. and the US entity for:

- Cloud costs incurred centrally and recharged to the US entity per the cost tag split
- Imagery procurement done by the B.V. on behalf of the US entity
- Shared service charges (Rotterdam-based teams supporting US customers) — allocated per the quarterly allocation note from Finance
- Any cash movements between the entities

Draft entries at WD-1, post at WD+1. Balances must agree between the two ledgers by WD+2. Use the intercompany clearing account in both ledgers; do not net balances across categories.

## Reporting pack

The reporting pack is assembled from the BI dashboards plus the period close working file. It includes:

- Profit and loss by entity and consolidated
- Revenue by line of business (monitoring subscriptions, imagery tasking, analytics API)
- Cloud cost by cost centre and by project tag
- Accruals detail and movement versus prior period
- Intercompany balance confirmation
- Headcount and payroll summary from the HR system

The pack is published to the finance folder in the document repository. The BI dashboards are marked with the period close status so other teams can see whether the numbers are final.

## Practical notes

- The close calendar is fixed per period; if a working day falls on a holiday in either Rotterdam or Denver, the close shifts with the local holiday and the other office follows the same calendar.
- The accounting system locks the prior period at WD+4. No entries are accepted after the lock.
- Payroll runs on its own calendar (see the payroll calendar and cut-offs doc) and does not move with the period close.
- Any questions on the close go to the Accounting, AP and payroll team in #finance.

## Change log

| When | What changed | Who |
|---|---|---|
| — | Initial version | Accounting, AP and payroll |
| — | Added sensor network site costs accrual line after the sensor network rollout expanded | Jin Kowalski |
| — | Clarified that the cloud bill accrual follows the billing export tag split | Jin Kowalski |
