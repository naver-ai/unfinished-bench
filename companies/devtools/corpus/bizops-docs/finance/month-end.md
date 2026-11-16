# Month-end close

**Owner:** Accounting & payroll  
**Last edited by:** Arjun Meyer (Accountant)  
**Applies to:** Gantline Software, Lda. (Portugal) and Gantline Inc. (US)

## Purpose

This document describes the monthly close calendar for the accounting team, from the working days before month end through final sign-off. It covers revenue recognition, accruals, the reconciliation of billing-service exports against the ledger, and the approval steps required before the books are locked.

The close calendar is expressed in working days relative to the last working day of the calendar month. Working days exclude Gantline holidays observed in both Lisbon and Portland.

## Close calendar

| WD | Activity | Owner | Notes |
|----|----------|-------|-------|
| WD-2 | Freeze seat changes in the Gantline Cloud admin console for the closing month | Customer Success | Seat counts for the closing month are final after this point. Any seat change requested after WD-2 is booked in the following month. |
| WD-1 | Extract billing-service exports for the closing month | Accounting & payroll | Run the standard export from the billing-service admin surfaces. Save the raw export to the finance folder in the data warehouse. |
| WD+1 | Post revenue for annual plans | Accounting & payroll | See revenue recognition below. |
| WD+1 | Post accruals | Accounting & payroll | See accruals below. |
| WD+2 | Reconcile billing-service exports against the ledger | Accounting & payroll | See reconciliation below. |
| WD+3 | Resolve reconciling items | Accounting & payroll | Any open items after WD+3 are escalated to the Finance Manager. |
| WD+4 | Draft close summary and variance notes | Accounting & payroll | |
| WD+5 | Final sign-off | Finance Manager | The books are locked after sign-off. |

The close calendar is also available as an iCal subscription in the finance channel. If a working day falls on a Gantline holiday in only one office, the calendar still applies — the team in the other office covers the steps that day.

## Revenue recognition for annual plans

Annual plans are invoiced upfront and recognised evenly over the contract term. For each annual plan invoice in the closing month:

1. Confirm the contract start date in the CRM matches the billing-service subscription start date.
2. Recognise the portion of the invoice attributable to the closing month.
3. Defer the remainder, which appears in the ledger as deferred revenue.

Monthly plans are recognised in full in the month the service is provided, which is the month the subscription is active.

If a customer upgrades mid-term, the additional seat revenue is recognised from the upgrade effective date, not from the invoice date. Downgrades are recognised as a reduction from the effective date of the downgrade.

## Accruals

Accruals are posted for expenses incurred in the closing month that have not yet been invoiced. The standard accrual categories are:

| Category | Basis | Example |
|----------|-------|---------|
| Cloud infrastructure | Usage reports from the cloud providers for the closing month | Compute, storage, network egress |
| Build farm | Metered usage from the build farm hosts | Registry image volumes, build host storage |
| Vendor licences | Contract value prorated to the closing month | SSO provider, helpdesk, email platform |
| Professional services | Time or milestone confirmed by the requesting team | External consultants, legal advice |
| Employee expenses | Expenses submitted through the expenses tool for the closing month | Travel, meals, equipment |

Accrual entries are posted with a description that includes the vendor or provider name and the month the expense relates to. Reversals are posted in the following month.

If a vendor invoice arrives after the close but relates to the closing month, it is posted against the accrual. If the invoice amount differs from the accrual by more than 10% per line, the difference is flagged in the close summary.

## Reconciling billing-service exports with the ledger

The billing-service export for the closing month is the source of record for customer revenue. The export contains:

- Invoice number and issue date
- Customer org name and ID
- Plan name and seat count
- Line amounts (gross, discount, tax)
- Payment status (paid, pending, failed)

Reconcile the export against the ledger as follows:

1. Confirm the total of invoices in the export equals the total of posted revenue plus deferred revenue for the closing month.
2. Confirm the total of paid invoices matches the bank deposits recorded in the ledger.
3. Confirm the total of failed payments matches the balance in the dunning queue in the billing-service admin console.
4. Confirm that no invoice in the export appears twice in the ledger and no ledger line is missing from the export.

Reconciling items are logged in the finance channel with the invoice number, the difference, and the likely cause. Common causes are VAT corrections, duplicate invoice lines, and plan changes applied after the seat freeze.

## Sign-off

The Finance Manager reviews the close summary, the variance notes, and the open reconciling items. The close is signed off when:

- All revenue and accrual entries are posted.
- The billing-service export reconciles to the ledger with no unresolved items.
- Deferred revenue balances match the CRM contract start dates.
- The close summary is posted in the finance channel.

After sign-off, the books are locked. Any adjustments requested after the lock require the Finance Manager's approval and are posted in the following month.

## Related documents

- `bizops-docs/people-ops/payroll.md` — payroll calendar and cut-offs
- `bizops-docs/billing/invoicing.md` — invoice formats and delivery
- `bizops-docs/billing/dunning.md` — failed payment handling
- `bizops-docs/billing/credits.md` — account credit process

Questions about the close calendar should go to the Accounting & payroll team in the finance channel.
