# Month-end close

Owner: Finance  
Last edited by: Tom Whitlock

The month-end close runs on the working-day calendar published in `finance-docs/README.md`. The close calendar below is the target for a standard month; where a step slips, the team lead for that step tells Finance Operations before the end of the day so we can adjust downstream steps rather than discover the slip at hand-off.

## Close calendar

| Working day | Step | Owner | Notes |
|---|---|---|---|
| WD-3 | Preliminary stock valuation file from Supply chain & fulfilment | Theo Yilmaz | Sent via sharectl to `finance-month-end` share. Includes store stock, DC stock, and wholesale stock on hand. |
| WD-3 | Bank statement imports completed | Finance Operations | All store banking batches from `finance-docs/cash/store-banking.md` must be in the ledger by end of day. |
| WD-2 | Prepayments and accruals review | Bruno Ibarra | Draft journal entries in the ledger; check prior-month accruals that need reversal. |
| WD-2 | Wholesale AR ledger review | Credit control | Open invoices, credit notes, and any unallocated cash. See `finance-docs/wholesale/credit-terms.md`. |
| WD-1 | Stock valuation final file | Theo Yilmaz | Replaces the WD-3 file. Finance Operations loads it into the ledger and checks the movement against the WD-3 file. |
| WD-1 | Journal entry cut-off | Finance Operations | All manual journals must be entered in the ledger by end of day. |
| WD 1 | Close day | Finance Operations | Runs the month-end ledger close in the ledger. |
| WD+1 | Preliminary P&L and balance sheet | Finance Operations | Sent to Tom Whitlock and Oliver Brandt. |
| WD+1 | Stock valuation sign-off | Theo Yilmaz / Finance Operations | Theo confirms the final file matches the DC and store inventory system counts; Finance Operations confirms the ledger matches Theo's file. |
| WD+2 | Accruals and prepayments posted | Finance Operations | Includes the payroll accrual, bonus accrual where applicable, and the store utilities accrual. |
| WD+2 | Gift card liability check | Finance Operations | Movement in gift card liability from `finance-docs/gift-cards.md`; reconcile to the gift card platform report. |
| WD+2 | Chargeback provision review | Malik Dimitrov | Malik provides the chargeback pipeline figure; Finance Operations checks it against the provision. |
| WD+3 | Intercompany reconciliations | Finance Operations | Leeds (UK), Dublin (IE), and Columbus (US) entities. Confirm balances across the ledger entities. |
| WD+3 | VAT control account review | Finance Operations | See `finance-docs/tax/vat-notes.md` for the VAT postings and control account checks. |
| WD+4 | Draft management accounts | Finance Operations | Packs for Tom Whitlock and Oliver Brandt. |
| WD+4 | Sign-off by Financial Controller | Tom Whitlock | Tom reviews the draft pack, resolves open items with the relevant team, and signs off in the ledger. |
| WD+5 | Final management accounts published | Finance Operations | Published to the finance share in sharectl. Oliver Brandt receives the summary. |

## Journals

All journals go through the ledger with the `month-end` tag. The journal description must reference the source document or file name so we can trace back after the close.

- Standard accruals (utilities, professional fees, marketing accrual) are posted by Finance Operations without further approval.
- Reversals of prior-month accruals happen automatically in the ledger on the first day of the new month; Finance Operations checks the reversal list on WD+2.

Payroll-related accrual amounts follow the payroll calendar in `finance-docs/payroll/payroll-calendar.md`; the payroll team owns the figures that feed the accrual.

## Stock valuation hand-off

The supply chain team owns the stock count and valuation methodology. Finance's role is to load the file, check the totals against the general ledger stock account, and flag movements larger than 5% at department level. Theo's team publishes the valuation notes alongside the file; if the notes are missing, Finance Operations asks Theo before loading the file.

The stock valuation file includes:

- Store stock at cost (per the POS back office)
- Wakefield DC stock at cost
- Wholesale stock held at third-party warehouses
- In-transit stock between DC and stores

Items that are not in the file but appear in the ledger stock account are queried with Theo's team before the WD-1 load.

## Sign-off

Tom Whitlock signs off the close in the ledger on WD+4. Sign-off means the draft management accounts are complete and the remaining steps are presentation and publication. If Tom is out of the office, Oliver Brandt signs off in his place; Finance Operations checks the sign-off rota in the Finance channel.

## Common issues

- Bank statements from stores that miss the WD-3 import deadline: the stores team follows `finance-docs/cash/store-banking.md`; Finance Operations chases via #stores-ops and, if needed, the helpdesk.
- Wholesale credit notes raised after WD-2: credit control handles these per `finance-docs/wholesale/credit-terms.md`.
- Stock valuation file mismatches: Finance Operations and Theo's team reconcile on WD-1; if the mismatch is not resolved by end of day, the close calendar shifts by one working day and Tom is told.

## Table of controls

| Control | Check | Owner |
|---|---|---|
| Bank imports complete | the ledger shows all store banking batches for the month | Finance Operations |
| Stock valuation matches ledger | Final file total vs stock account balance | Finance Operations / Theo Yilmaz |
| Journals all tagged | No untagged postings in the month-end period | Finance Operations |
| Gift card liability reconciles | Platform report vs ledger control account | Finance Operations |
| Chargeback provision adequate | Pipeline figure vs provision | Malik Dimitrov |
| VAT control accounts clear | No unexplained balances | Finance Operations |
| Sign-off recorded | the ledger shows Tom's sign-off | Tom Whitlock |
