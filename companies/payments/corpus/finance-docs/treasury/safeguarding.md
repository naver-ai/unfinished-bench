# Safeguarding

**Owner:** Treasury & settlement  
**Last edited by:** Mara Costa (Treasury Analyst)

## Purpose

This document describes how Kilbarra safeguards merchant and e-money customer funds held in segregated accounts at partner banks, the daily safeguarding reconciliation, how a shortfall or excess affects the day's transfers, and the annual safeguarding audit. It applies to all treasury and settlement staff, and to anyone else who touches safeguarding account balances or the reconciliation tool.

## Scope

Covers safeguarding accounts across all partner banks serving EEA and UK merchants, and the US sponsor bank programme. It does not cover client money rules for the sponsor bank programme's own requirements — those are set out by the sponsor bank and applied through the treasury workstation.

## Safeguarding accounts

1. Safeguarded funds are held in dedicated accounts at partner banks. These accounts are opened in Kilbarra's name, are not used for operating cash, and are disclosed to each partner bank as safeguarding accounts.

1.1. The account set at each partner bank may include one or more settlement accounts plus a safeguarding holding account. All balances in these accounts count toward the safeguarding calculation.

1.2. The partner bank list is maintained by Treasury & settlement in the treasury workstation. Adding or removing a partner bank requires sign-off from Ivan Park and the CFO.

1.3. Interest earned on safeguarding accounts accrues to Kilbarra. Interest is swept on the last working day of each month.

## Daily safeguarding reconciliation

2. The safeguarding reconciliation runs each working day, before the bank file cut-off. The reconciliation tool pulls:

- balances from each partner bank safeguarding account;
- the aggregate e-money balance from the core ledger;
- outstanding settlement and payout amounts from the payments bus message store;
- chargebacks and other adjustments from the transaction monitoring system and the case tool.

2.1. The safeguarding position is calculated as:

   **Safeguarded funds held** (bank balances) **minus** (aggregate e-money balance plus outstanding settlement/payout obligations)

2.2. A positive result is an excess. A negative result is a shortfall.

2.3. If the reconciliation produces a shortfall, transfers from safeguarding accounts are paused for that day. The treasury workstation blocks payouts and settlement transfers, and the SRE team is paged through the paging tool so the issue is visible on the incidents channel in chat.

2.4. A shortfall is investigated immediately by the Treasury Analyst on duty. Common causes: a bank balance not yet posted, a payout file that settled late, or a ledger entry posted before bank movement. The analyst works through the reconciliation tool drill-down to the underlying entries and resolves with the partner bank or the payments platform team as needed.

2.5. An excess is not a problem by itself. The excess is retained in the safeguarding accounts and is not swept to the operating account. The daily run records the excess amount in the treasury workstation, and the cumulative excess is reviewed each month by Greta Moreau.

2.6. If a shortfall cannot be resolved by the end of the working day, Treasury & settlement notifies Ivan Park and Rafael Costa. A shortfall outstanding for more than two working days is escalated through the incidents channel.

## Transfers and the daily run

3. The daily safeguarding reconciliation is a precondition for the payout and settlement runs. Both are generated from the treasury workstation.

3.1. Payouts and settlement transfers are only released after the reconciliation tool confirms the safeguarding position is not negative.

3.2. If the reconciliation is not available by cut-off (for example, a partner bank feed is down), the treasury workstation prevents the payout run. The on-call treasury analyst coordinates with the partner bank and with the payments platform team. The missed run is executed the next working day, provided the safeguarding position is then positive.

3.3. When a shortfall is resolved, the analyst records the cause and resolution in the reconciliation tool. The note is visible to the whole Treasury & settlement team.

## Annual safeguarding audit

4. The safeguarding accounts and the daily reconciliation are audited each year as part of the annual safeguarding audit. The audit covers:

- the design and operating effectiveness of the daily reconciliation;
- the completeness of the bank account list in the treasury workstation;
- whether the core ledger e-money balance and the safeguarding bank balances actually match at a point in time;
- the treatment of interest sweeps;
- whether shortfalls or excesses were handled per this document.

4.1. The audit is run by an external firm engaged by the CFO. Treasury & settlement provides the auditor access to the reconciliation tool, the treasury workstation, and the relevant partner bank confirmations.

4.2. The auditor's report is shared with Ivan Park and Rafael Costa. Any findings are tracked in the tickets system as actions, with owners from Treasury & settlement.

4.3. If the auditor identifies a material shortfall that was not detected by the daily reconciliation, the reconciliation logic is reviewed and updated as needed. This is done together with the finance engineering team, and the change goes through the normal change management process.

## Related documents

- Eng-docs: accounting for safeguarding transactions is described in the event-sourced ledger ADR (eng-docs/adr/0004-event-sourced-ledger.md).
- Finance-docs: settlement and payouts (finance-docs/treasury/settlement-and-payouts.md), month-end close (finance-docs/close/month-end-close.md).
- Risk-docs: chargeback monitoring (risk-docs/risk/chargeback-monitoring.md).
