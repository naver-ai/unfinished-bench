# Where the return figures come from

**Owner:** Regulatory reporting  
**Last edited by:** Fatima Pham (Senior Regulatory Reporting Analyst)  
**Status:** Draft — two sections unfinished, one open question for the next working group

---

## Purpose

This note maps each schedule line in the supervisory returns to the warehouse views and ledger accounts we draw from, records known breaks between the two, and lists the checks we run before a return is drafted. It is meant for the regulatory reporting team and for Finance Engineering when they touch the relevant views.

## Context

We have two sources of truth for return figures: the core ledger (what actually settled) and the analytics warehouse (what the reporting views serve). For most lines they agree. For some they do not, and we need to know which one wins and why. This note captures the decisions from the working group that met ahead of the current reporting cycle.

## Schedule line mapping

| Schedule line | Warehouse view | Ledger accounts | Notes |
|---|---|---|---|
| E-money outstanding | `warehouse.e_money_balances_daily` | Core ledger balance sheet accounts 4100–4199 | View is as-of end of day; ledger is point-in-time. Use ledger for the return date, view for trend comparison. |
| Payment transactions volume | `warehouse.payment_txns_daily` | Ledger revenue accounts 7100–7199 | Volume line comes from the view only; ledger accounts only capture fee revenue, not gross volume. |
| Payouts sent | `warehouse.payouts_daily` | Ledger settlement accounts 5200–5299 | Known break: payouts initiated but failed before submission appear in the view but not in the ledger. We exclude them from the return. |
| Merchant balances | `warehouse.merchant_balances_daily` | Ledger merchant liability accounts 3000–3099 | Matches, except for merchants in the process of closing — see open question below. |
| Card acquiring volume | `warehouse.acquiring_volume_daily` | No direct ledger account | Acquirer reports volume separately; never take this from the ledger. |
| Partner platform balances | `warehouse.partner_balances_daily` | Ledger partner liability accounts 3100–3199 | Matches at month end. Intra-month the view lags by up to two working days because of the warehouse sync schedule. |

## Known breaks

1. **Failed payouts** — described above. The reconciliation tool flags these; we exclude them from the return and add a note in the submission file.
2. **Merchant closures** — when a merchant closes, their balance moves to a suspense account before final payout. The warehouse view keeps showing the balance under the merchant until the next full refresh. If a return date falls in that window, use the ledger.
3. **Partner platform balances** — the view is good enough for the quarterly return, but for the annual return we use the ledger because the view's two-day lag can cross a quarter end.
4. **Still open: intra-month e-money outstanding** — we have not yet decided whether the daily view or the ledger snapshot is authoritative for the mid-month return. Hana is checking whether the warehouse sync team can give us a point-in-time flag.

## Checks before drafting

- Run `filingctl` preflight: it compares the warehouse view totals against the ledger for every mapped line and reports differences above €1,000.
- Reconcile the e-money outstanding line against the safeguarding report from Treasury (Ivan Park's team) — the two must match to the cent.
- Check that the `warehouse.e_money_balances_daily` view has data through the return date; Oliver's team publishes it by mid-morning Ireland time on the first working day after the period end.
- Pull the acquiring volume from the acquirer's own report and compare to `warehouse.acquiring_volume_daily` — differences above 0.1% go back to Finance Engineering before we draft.
- Confirm with Treasury that no payouts are stuck in the `pending` state on the return date (Tariq Rahman usually has this visibility).
- **Still open: partner platform balances at quarter end** — we need to agree with Oliver's team whether the view refresh on the quarter-end date is guaranteed or whether we should always use the ledger for that line.

## Open question

For merchant closures, should we standardise on the ledger balance as at the return date, or should we use the last balance the merchant had before the closure was initiated? The difference matters for the E-money outstanding line and affects how the return compares to the safeguarding position. Zoe is pulling examples from the last two quarters to bring to the next working group.

## Related documents

- `finance-docs/treasury/safeguarding.md`
- `finance-docs/reg-reporting/returns-calendar.md`
- `finance-docs/reg-reporting/submission.md`
- `eng-docs/data/warehouse.md`
