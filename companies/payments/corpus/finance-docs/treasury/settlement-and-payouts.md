# Settlement and payouts

**Owner:** Treasury & settlement  
**Last edited by:** Tariq Gonzaga (Treasury Analyst)  
**Applies to:** Treasury & settlement, Settlement Operations  

This covers the daily settlement and merchant payout cycle: scheme settlement received, payout runs built and sent to partner banks, confirmations, returns, and the month-end calendar.

## Daily cycle overview

The settlement cycle runs every banking day, including days when Ireland or the US observe holidays but the schemes settle. If a scheme is closed, its settlement simply does not arrive and the affected payouts move to the next run.

### 1. Scheme settlement received

1. Scheme settlement files arrive in the treasury workstation from {{CARD_SCHEME_1}}, {{CARD_SCHEME_2}} and {{PAYMENT_SCHEME_1|code}} schemes. The workstation polls their SFTP endpoints on a schedule; there is no manual fetch.
2. The treasury workstation reconciles each file against the core ledger's expected settlement entries. Discrepancies appear in the reconciliation tool under **Settlement > Scheme exceptions**.
3. Confirm all schemes have settled for the day. The settlement dashboard shows each scheme's status: **Expected**, **Received**, **Short**, **Missing**.
4. If a scheme is marked **Short** or **Missing** after the cut-off, follow the scheme exception steps below.

### 2. Payout run build

1. Open the treasury workstation and go to **Payouts > Build run**.
2. Select the currency and the payout date. The workstation defaults to the next banking day for the merchant's settlement currency.
3. The build pulls eligible merchant balances from the core ledger. A merchant is eligible when:
   - the balance is above the minimum payout threshold for their plan,
   - the merchant has no active payout hold on their account,
   - the merchant's settlement bank details are valid and verified.
4. Review the run summary. The workstation shows the number of payouts, total value, and any merchants excluded with reasons.
5. Click **Build run**. The run is staged and visible in **Payouts > Staged runs**.

### 3. Approve and send bank files

1. The run must be approved by a second person in Treasury & settlement. Go to **Payouts > Staged runs**, open the run, and click **Approve and generate files**.
2. The workstation generates bank files per partner bank and currency and hands them to the bank connectivity service.
3. The bank connectivity service transmits each file to the partner bank's SFTP endpoint. Transmission status is visible in the treasury workstation under **Transfers > Outbound**.
4. Confirm each file shows **Sent** and note the transmission reference. The bank file cut-offs are:

| Currency | Cut-off (Dublin time) |
|---|---|
| EUR | Mid-afternoon, for same-day {{PAYMENT_SCHEME_1|code}} credit |
| GBP | Early afternoon, for same-day sterling payments |
| USD | Late afternoon, through the sponsor bank |

Files not sent by the cut-off are held and included in the next day's run. A run may be sent late only if the partner bank confirms they will accept it — contact the bank's service desk directly and log the confirmation reference in the run notes.

### 4. Confirmation files

1. Partner banks return confirmation files through the bank connectivity service. The treasury workstation imports these automatically.
2. Go to **Payouts > Confirmations** to review. Each payout shows **Confirmed**, **Returned**, or **Pending**.
3. Confirmations are expected within one banking day of sending. If a confirmation is still **Pending** after two banking days, check the file transmission in the treasury workstation and raise a ticket with the partner bank if needed.
4. The core ledger is updated with the confirmation status. Confirmed payouts are marked settled; returned payouts are reversed back to the merchant balance automatically.

### 5. Returned payouts and re-sends

1. When a bank returns a payout, the treasury workstation reverses the entry and the merchant sees the funds back in their balance. The return reason is stored on the payout record.
2. Review returned payouts in **Payouts > Returns**. Common reasons: invalid IBAN or account number, account closed, name mismatch.
3. Notify the merchant through custnotify when a payout is returned. The notice template is **Payout returned** and includes the return reason as provided by the bank.
4. If the merchant provides corrected bank details, the next payout run picks them up automatically. There is no manual re-send.
5. If a payout was returned in error by the bank, contact the bank's service desk and ask them to accept the file again. Once they confirm, rebuild the payout from the returned record using **Payouts > Returns > Rebuild**.

## Month-end payout calendar

The last banking day of the month is treated as a normal settlement day, but there are two additional steps:

1. **Final run of the month** — the run for the last banking day must be built and sent by the normal cut-offs. Do not hold payouts to the next month unless the merchant has asked us to and it is recorded on their account.
2. **Month-end reconciliation** — after the last confirmation arrives, run the month-end payout report from the reconciliation tool and check it against the core ledger. The report is filed under **Treasury > Month-end** in the shared drive.

Payouts scheduled for a non-banking day are moved to the preceding banking day automatically by the workstation. The month-end calendar in the treasury workstation shows which payouts fall in which month.

## If it goes wrong

- **Scheme settlement missing:** Check the scheme's operational status page. If the scheme reports no issue, escalate to the scheme's service desk with the expected settlement reference from the workstation. Log the case in tickets under **Treasury > Settlement**.
- **Bank file fails to send:** the treasury workstation shows the error. Retry the transfer from **Transfers > Outbound**. If it fails again, check the file with the partner bank's file format guide — a formatting error will be rejected. Fix the file only if the error is in our generation; otherwise raise a ticket.
- **Confirmation not received:** First check the bank's status page, then raise a ticket with the bank. Do not re-send the payout file unless the bank confirms the original was not received.
- **Run built incorrectly:** If a run has not been sent, it can be deleted from **Payouts > Staged runs** and rebuilt. If it has been sent, contact Treasury & settlement management before taking any further action.

## Related documents

- finance-docs/treasury/safeguarding.md
- merchant-docs/billing/invoices-and-fees.md
