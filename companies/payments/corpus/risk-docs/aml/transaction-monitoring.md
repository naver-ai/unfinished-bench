# Transaction monitoring

**Owner:** Financial crime  
**Last edited by:** Jasmine Rao (Financial Crime Manager)

This document covers the alert types in the transaction monitoring system, how to work an alert in the case tool, when to escalate to the MLRO, suspicious transaction reports (STRs), and tipping-off.

## Alert types

The transaction monitoring system raises alerts in the following categories:

1. **Velocity alerts** – unusual frequency of transactions (e.g., rapid spending across multiple merchant accounts or e-money wallets).
2. **Structuring alerts** – patterns that suggest deliberately splitting amounts to stay below reporting thresholds.
3. **Geographic alerts** – activity from high-risk jurisdictions or sudden changes in expected geography for a merchant or payee.
4. **Counterparty alerts** – transactions involving known high-risk or sanctioned counterparties (name matches from screening).
5. **Amount anomalies** – transactions significantly outside a merchant’s historical pattern, either single large payments or an unusual total over a rolling window.
6. **Round-trip alerts** – funds moving out and back in quickly, often through the same or related accounts.

## Working an alert in the case tool

1. Open the case tool and filter the work queue for your name under **Financial crime > Transaction monitoring > My queue**.
2. Claim an alert by selecting **Assign to me**. Do not work an alert that is already assigned to someone else unless asked by the Financial Crime Manager.
3. Review the alert summary: the merchant, the transactions flagged, the rule that fired, and the time window.
4. Open the merchant record in the back office and check:
   - risk rating and any open flags
   - expected activity profile (from onboarding and reviews)
   - whether the alert overlaps with an existing open case
5. Pull the underlying transactions from the core ledger or the reconciliation tool as needed. Save the relevant ones to the case under **Evidence**.
6. Record your initial assessment in the case notes: what you checked, what you found, and whether the activity is consistent with the merchant’s known profile.
7. If the activity is explained (e.g., a one-off large invoice or a planned payout), mark the alert as **Closed – no further action** and state the reason in the notes.
8. If the activity is not explained or you have concerns, mark the alert as **Pending review** and escalate to Jasmine Rao (or the duty Financial Crime Manager if Jasmine is away). Do not close it.

## Escalation to the MLRO

Escalate to the MLRO through the case tool using **Escalate > MLRO review**. Include:

- a summary of the activity and why it is suspicious
- the merchant ID and any related accounts
- the transactions you have attached as evidence
- any previous alerts or cases on the same merchant

The MLRO decides whether a suspicious transaction report is needed. You will be notified in the case tool when the decision is made.

## Suspicious transaction reports (STRs)

STRs go to the Financial Intelligence Unit through its online reporting system and are filed by the MLRO's office. When the MLRO asks for an STR, the analyst prepares it in the case tool:

1. Open the case and select **Prepare STR**.
2. Pre-fill the merchant details from the case (use the **Copy from case** button).
3. Complete the narrative fields, describing the activity in plain terms and why it is suspicious. Do not include speculation.
4. Attach the supporting evidence from the case (saved as PDF under **Evidence**).
5. Hand the draft to the MLRO's office in the case tool. The STR reference appears on the case once it has been filed.

Keep the case open until the MLRO confirms it can be closed.

## Tipping-off

Do not tell the merchant, or anyone outside the financial crime team and the MLRO, that a suspicious transaction report has been made or is being considered. This includes:

- conversations in the chat – do not name the merchant in #general or #random
- responses to merchant queries – deflect without confirming or denying any reporting activity
- any written communication to the merchant, including merchant notices and dashboard messages

If you believe a merchant may have become aware of an STR, tell Jasmine Rao immediately and do not discuss it further with anyone else.

## If it goes wrong

- **You claimed the wrong alert** – release it in the case tool (**Release claim**) and add a note saying it was claimed in error.
- **The case tool is down** – keep a local note of the merchant ID and alert number, and tell the financial crime team on #risk-controls. Work the alert once the case tool is available.
- **You cannot find the underlying transactions** – check whether the activity is in the core ledger or the reconciliation tool first; if still missing, ask on #payments-platform before closing anything.
- **You closed an alert that should have been escalated** – reopen it immediately, mark it as **Pending review**, and tell Jasmine Rao. Do not edit the original closure note; add a new note explaining the correction.
