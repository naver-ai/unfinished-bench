# Control testing

**Owner:** Governance, risk & controls testing  
**Last edited by:** Ben Abara (Controls Testing Analyst)

The control library lives in the GRC tracker, with each control tagged by line of defence, owning team, and the system or process it applies to. First-line controls are owned by the business teams that run the process; second-line controls are owned by GRC and test the first line's operation. The library is reviewed continuously; any control that no longer matches the process it covers is flagged in the tracker and either updated or retired at the next quarterly review.

## Testing calendar

Testing runs on a quarterly cycle, aligned to the financial year. The calendar below shows the minimum cadence; GRC may pull additional controls into a quarter if a risk rating changes or an incident points at a gap.

| Quarter | First-line testing focus | Second-line testing focus |
| --- | --- | --- |
| Q1 | Merchant onboarding and KYB checks, safeguarding reconciliation, transaction monitoring alert closure | Control library refresh, sample testing on Q4 first-line results |
| Q2 | Payouts and settlement, chargeback handling, supplier payments | Deep-dive on a high-risk process (rotates each year), evidence review for auditor requests |
| Q3 | Fee and invoice posting, complaints handling, reconciliation breaks | Cross-team testing with Risk & compliance, sample testing on H1 first-line results |
| Q4 | Regulatory returns preparation, access review completion, incident response actions | Year-end control effectiveness summary for the risk committee |

First-line teams record their testing results in the GRC tracker as they complete them. Second-line testing is scheduled by GRC at the start of each quarter and published in the tracker; teams are notified through the tracker and a note in #risk-controls.

## Sampling

Samples are drawn from the population in the system of record, not from what the control owner provides. For most controls we use a fixed sample of ten items per quarter, with the selection spread across the quarter's activity where that is practical. For controls that run less often (for example, quarterly access reviews), the sample covers the whole population. If a control processes high volumes — like transaction monitoring alerts — we use a larger sample and note the confidence level in the results.

## Recording results and issues

Each test record captures the control ID, the period covered, the sample size, the number of items that passed, and the tester's name. Issues are recorded with a severity rating:

- **High** — the control did not operate, or failed on the majority of the sample. The owning team has until the end of the next working day to respond.
- **Medium** — the control operated but with exceptions on several items. The owning team has five working days to respond.
- **Low** — isolated exceptions or observations that do not indicate a systemic gap. The owning team acknowledges and addresses at the next control review.

Issues are tracked to closure in the GRC tracker. A control with an open high or medium issue is reported as "not effective" in the quarterly summary until the issue is closed and a re-test passes.

## Reporting to the risk committee

The quarterly control summary is prepared by GRC and shared with the Chief Risk Officer ahead of the risk committee meeting. It covers: the number of controls tested, the pass rate by line of defence, all high issues and their status, and any controls that were not tested because of a change in the process. The summary is also stored in the GRC tracker for audit evidence; see `security-docs/compliance/audit-evidence.md` for how auditor requests are handled.
