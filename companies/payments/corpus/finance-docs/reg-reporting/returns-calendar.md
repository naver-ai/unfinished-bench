# Regulatory returns calendar

**Owner:** Regulatory reporting  
**Last edited by:** Hana Sato (Regulatory Reporting Analyst)  

This page lists the recurring regulatory and supervisory returns Kilbarra prepares and submits. Working-day offsets are counted from the relevant period end, excluding Irish public holidays. Where a due date falls on a non-working day, the return is submitted on the next working day.

| Return | Period | Due (working days from period end) | Data owner | Preparer | Notes |
|---|---|---|---|---|---|
| Supervisory Authority EMI quarterly return (Q-EMI) | Quarterly (Mar, Jun, Sep, Dec) | WD+20 | Treasury & settlement | Regulatory reporting | Covers safeguarding, e-money issuance, payment volumes. Filed via filingctl. |
| Safeguarding audit report | Annual (financial year end) | WD+15 after audit opinion issued | Treasury & settlement | Regulatory reporting | Submitted to the Supervisory Authority and board. Audit firm prepares opinion; Regulatory reporting assembles package. |
| AML/CFT annual return | Annual (calendar year end) | WD+30 | Compliance | Regulatory reporting | Prepared from transaction monitoring system data and KYB onboarding tool records. |
| Payment statistics return (PSR) | Quarterly | WD+15 | Payments platform | Regulatory reporting | Volume and value by payment instrument. Pull from the core ledger and payments bus message store. |
| Balance of payments statistical return | Quarterly | WD+25 | Finance | Regulatory reporting | For the Supervisory Authority statistics division. Uses treasury workstation and core ledger data. |
| Sponsor bank monthly activity report | Monthly | WD+5 | Treasury & settlement | Regulatory reporting | US merchant activity through the sponsor bank programme. Submitted via the sponsor bank portal. |
| Sponsor bank quarterly attestation | Quarterly | WD+10 | Compliance | Regulatory reporting | Confirms US programme compliance. |

## Working notes

- The Q-EMI return is the heaviest lift each quarter. Data comes from the core ledger and treasury workstation; Regulatory reporting reconciles it against the safeguarding account before submission.
- The AML annual return feeds from extracts produced by the transaction monitoring system. Aleksander Das owns the underlying dataset on behalf of Compliance.
- Statistical returns use the same source figures as the Q-EMI where possible — see `finance-docs/reg-reporting/data-lineage.md` for how the figures map.
- The safeguarding audit report is the only return on this calendar with a date tied to the audit opinion rather than a fixed working-day offset. The audit firm usually issues the opinion in the weeks after the financial year end; the WD+15 clock starts when the opinion is issued, not at the year end.
- All filings go through filingctl unless the return itself is submitted through an external portal (the sponsor bank reports are the exception).
- If a deadline is missed, the incident process in `eng-docs/incidents/incident-process.md` applies, and the Regulatory Reporting Manager (Aoife Brennan) should be pulled in immediately. The Supervisory Authority has a published late-filing procedure; we do not rely on it.

## Preparation schedule

Preparation for each quarter-end return starts on the first working day after the period end. The preparer listed above assembles the figures and goes through them with the data owner.

- WD+1 to WD+5: data extraction and initial reconciliation
- WD+6 to WD+10: review with data owner, resolution of differences
- WD+11 to due date: final checks and submission via filingctl

For the annual returns, the same cadence applies but preparation begins two weeks before the period end so that the audit firm (for safeguarding) and Compliance (for AML) have their inputs ready on time.
