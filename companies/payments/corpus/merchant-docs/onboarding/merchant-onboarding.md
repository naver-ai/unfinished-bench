# Merchant onboarding

**Owner:** Merchant operations desk  
**Last edited by:** Simone Richter (Collections Desk Analyst)

This page covers the path from signed application to live: KYB hand-off, MID and account set-up, the merchant test environment, go-live checks, and the first payout.

## Before you start

You need a fully signed application in the KYB onboarding tool, with the merchant's legal entity details, directors and beneficial owners captured. If anything is missing, return it to the sponsor in sales via the onboarding tool rather than starting set-up.

## 1. KYB hand-off

1. In the KYB onboarding tool, set the application status to `Ready for review`. This notifies the financial crime team.
2. The financial crime team runs KYB and risk checks. They will either approve the application or send it back with comments.
3. Once approved, the application appears in the back office under **Merchant applications** with status `Approved`.
4. Assign yourself as the onboarding owner in the back office.

## 2. MID and account set-up

1. Open the application in the back office and select **Create merchant account**.
2. Enter the legal entity name exactly as it appears on the KYB record. The tax identifier field is mandatory for EU entities and optional for US ones.
3. Select the merchant's risk rating (assigned by financial crime — do not change it).
4. Choose the settlement currency. For US merchants, this will be USD and the merchant is onboarded under the sponsor bank programme. For all others, EUR or GBP.
5. Click **Create**. The back office generates:
   - Merchant account ID (starts with `M-`)
   - One or more MIDs (starts with `MID-`)
   - API credentials (client ID and secret) — visible only at creation time
6. Record the MID and account ID in the application record.
7. If the merchant needs a platform account (for software partners embedding payments), create it under **Platform accounts** in the back office and link it to the merchant account. See `merchant-docs/partners/partner-programme.md`.

## 3. Configure the merchant account

1. In the back office, open the new account and go to **Settings**.
2. Set the settlement schedule. Default is daily, but weekly or monthly is available on request.
3. Configure payout currency conversion if the merchant's settlement currency differs from their bank account currency.
4. Set the statement descriptor (this appears on cardholders' statements). The default is the merchant's trading name; some acquirers require a specific format, so check the application notes.
5. Add the merchant's settlement bank account under **Payout details**. IBAN for EU, account and routing number for US.
6. If the merchant needs payment links or invoicing, enable those features under **Products**. Payment links on the merchant's own domain need that domain set up first — see `eng-docs/platform/dns-and-domains.md`.

## 4. Fees and plan

1. Apply the agreed pricing plan from the signed application. This is done under **Billing** → **Plan**.
2. If the plan includes volume-based fees, set the volume tiers now.
3. The first invoice will be generated on the next billing run. See `merchant-docs/billing/invoices-and-fees.md` if the merchant asks about timing.

## 5. Merchant test environment

1. Every merchant gets access to the test environment. There is no separate onboarding step — the merchant's API credentials work against both `api.kilbarrapay.com` (live) and `api.kilbarrapay.dev` (test) once the account is created.
2. Test cards are listed in the merchant dashboard under **Developers** → **Test cards**. Do not share test card numbers over chat; point the merchant to the dashboard.
3. The merchant should run through at least one successful payment and one failed payment (e.g. using a declined test card) before go-live.
4. Webhooks can be tested using the test endpoint. See `eng-docs/merchant-api/webhooks.md` for the list of events and the signing mechanism.

## 6. Go-live checks

Run through this checklist before telling the merchant they are live:

- [ ] KYB approval is present in the onboarding tool
- [ ] Merchant account is active in the back office (status `Live`, not `Pending`)
- [ ] MIDs are provisioned and visible under **Accounts** → **MIDs**
- [ ] Settlement bank account is verified (the back office shows `Verified`; if `Pending`, chase treasury ops)
- [ ] Pricing plan is applied
- [ ] Webhook endpoint is configured (if the merchant uses webhooks)
- [ ] Test transaction was completed in the test environment
- [ ] Merchant has confirmed they have received their API credentials (check the onboarding tool for the confirmation tick)

Once all checks pass, send the go-live confirmation through custnotify. The merchant is live immediately — there is no separate activation step.

## 7. First payout

1. The first payout runs on the merchant's settlement schedule. For daily settlement, this is the first working day after the first successful transaction.
2. If the first payout fails (e.g. bank details rejected), the merchant operations desk is notified via the reconciliation tool. The failure reason appears in the back office under **Payouts** → **Failed**.
3. Common causes and fixes:
   - **Incorrect IBAN/account number** — ask the merchant to re-enter details in the dashboard, then re-run the payout from the back office.
   - **Bank account not verified** — chase treasury ops via `#treasury-ops`.
   - **Payout below minimum** — some acquirers impose a minimum payout amount. If the merchant's first payout is below this, it will be held until the threshold is met. Mention this to the merchant in the go-live confirmation so they are not surprised.
4. If a payout fails twice, escalate to Reza Teixeira (Merchant operations desk) rather than retrying a third time.

## If it goes wrong

- **KYB is rejected.** Financial crime will add a comment with the reason. Return the application to sales via the onboarding tool with the comment attached. Do not create an account while KYB is rejected.
- **MID creation fails.** The back office returns an error with a reference code. Check `#it-help` for known issues, then raise a ticket with the code if nothing is there.
- **Merchant cannot log in to the dashboard.** Check the account status in the back office. If the account is `Pending` or `Suspended`, that is the cause. Otherwise, raise it with IT & workplace in `#it-help`.
- **Test environment is down.** Check the status page first, then post in `#sre` if the status page shows no issue.
- **Merchant reports they cannot see payouts.** Verify the payout schedule in the back office, then check the reconciliation tool for the payout status. If the payout shows `Processing` for more than two working days, escalate to treasury ops.

If you are unsure whether a step is complete, ask in `#merchant-success` rather than guessing. The onboarding tool tracks most of this, so check it first.
