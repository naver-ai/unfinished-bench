# Month-end close

**Owner:** Finance operations  
**Last edited by:** Laszlo Brennan (Revenue Accountant)

## Purpose

This page is the operating calendar and task list for the monthly financial close. Finance operations runs the close; the financial controller reviews the close pack before the books are opened for the next period. Treasury, Payments platform, and Revenue Accounting all have hand-offs into the close, and their inputs are listed here in the order they are needed.

The close runs on working days relative to the last day of the reporting month (WD0). The calendar below is the default; if a working day falls on a bank holiday in Ireland, Lithuania, or the US, the close shifts by one working day and Finance operations announces the revised dates in `#finance-eng` and `#treasury-ops`.

## Close calendar

| WD | Task | Owner | Notes |
|----|------|-------|-------|
| WD-2 | Preliminary payout run list sent to treasury | Treasury & settlement | Treasury confirms large-payout exceptions to Finance operations |
| WD-1 | Cut-off for merchant fee adjustments | Revenue Accounting | Adjustments after this point go into the following month |
| WD-1 | Treasury posts final safeguarding balance snapshot | Treasury & settlement | Snapshot taken at the close of the WD-1 business day |
| WD0 | Core ledger cut-off at end of day UTC | Payments platform | No further entries accepted for the reporting month |
| WD+1 | Processing-fee revenue accrual posted | Revenue Accounting | From the fee lines in the core ledger, see below |
| WD+1 | Scheme fee and interchange accrual posted | Revenue Accounting | Card scheme statements may lag; accrual uses the prior month's actuals adjusted for volume |
| WD+2 | Safeguarding reconciliation hand-off from treasury | Treasury & settlement | See finance-docs/treasury/safeguarding.md for the reconciliation method |
| WD+2 | Intercompany entries posted with the US entity | Finance operations | Includes the sponsor bank programme balances |
| WD+3 | Close pack assembled | Finance operations | Pack is assembled in the shared Finance drive |
| WD+4 | Financial controller review | Financial controller | Queries are raised in the close pack document; Finance operations resolves by end of WD+4 |
| WD+5 | Close pack approved | Financial controller | Approval is recorded in the close pack document |
| WD+6 | Books opened for the new month | Finance operations | Core ledger re-opened; any late entries require a ticket to Finance operations |

## Processing-fee revenue

Processing-fee revenue is posted on WD+1 from the fee lines the core ledger records at settlement. Platform plan fees are booked in the ledger as they are charged, so they need no accrual.

The accrual is posted at the merchant plan level, not per transaction. Revenue Accounting reconciles the accrual to the settlement files from the acquirers during the month; differences above the materiality threshold agreed with the financial controller are flagged in the close pack.

## Scheme fee and interchange accruals

Scheme fee and interchange statements from the card schemes arrive after month-end, so the WD+1 accrual is an estimate. The accrual uses:

- the prior month's actual scheme fees and interchange, adjusted for the change in processed volume from the analytics warehouse, and
- any known rate changes notified by the schemes.

When the actual statements arrive, Revenue Accounting posts the true-up in the month the statement is received. The true-up is not held for the close.

## Safeguarding reconciliation hand-off

Treasury delivers the safeguarding reconciliation on WD+2. The hand-off confirms that the sum of merchant e-money balances in the core ledger matches the safeguarding accounts held with the partner banks. The hand-off includes:

- the aggregated balance per safeguarding account,
- the list of merchant balances over the threshold in finance-docs/treasury/safeguarding.md, and
- a note of any failed or pending payouts that affect the balance.

Finance operations reviews the hand-off and raises a ticket to treasury if any line does not tie back to the core ledger. The reconciliation is part of the close pack.

## Intercompany with the US entity

US merchants are served through the sponsor bank programme, and the US entity holds the sponsor bank relationship. On WD+2, Finance operations posts the intercompany entries for:

- fees earned by the US entity under the programme,
- costs recharged from the Dublin entity,
- the net settlement position between the two entities.

The intercompany balance is confirmed against the US entity's ledger by email before the close pack is assembled. Outstanding differences are listed in the close pack with an owner and an expected resolution date.

## Close pack review

The close pack is assembled on WD+3 and contains:

- the trial balance from the core ledger,
- the processing-fee revenue accrual and true-ups,
- the scheme fee and interchange accrual,
- the safeguarding reconciliation hand-off,
- the intercompany entries with the US entity,
- a variance note against the prior month for the main revenue and cost lines.

The financial controller reviews the pack on WD+4 and either approves it or raises queries in the document. Queries are resolved by Finance operations the same working day where possible; if a query needs input from another team, the close pack records the owner and the expected resolution date. The controller's approval on WD+5 closes the month; the books open on WD+6.

If the controller is unavailable on WD+4, the head of Finance operations reviews the pack in their place and notes it in the close pack document.
