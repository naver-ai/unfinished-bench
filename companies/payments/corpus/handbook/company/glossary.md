# Payments glossary

Owner: Merchant support · Last edited by Lena Fischer (Support Lead)

New joiners in support, onboarding, and the Dublin/Vilnius/Austin offices keep tripping over the same payment terms. This glossary is the short version — if a term still doesn't make sense after reading this, ask in #merchant-success or #payments-platform.

## The basics

| Term | What it means at Kilbarra |
|---|---|
| Acquirer | The entity that processes card payments on behalf of a merchant. For EU merchants that's Kilbarra (we hold an e-money licence). For US merchants, our sponsor bank is the acquirer of record and Kilbarra provides the platform and processing. |
| Card scheme | {{CARD_SCHEME_1}}, {{CARD_SCHEME_2}}, and (for some EU merchants) the smaller schemes. The scheme sets the rules and fees for the card products we process. |
| Interchange | The fee the cardholder's bank charges the merchant's bank (us, or our sponsor bank) for each card transaction. Set by the scheme, not by Kilbarra. We pass it through to the merchant on their invoice. |
| MID | Merchant identification number. A merchant can have more than one MID (one per card scheme, per entity, or per settlement configuration). MIDs are visible in the back office under the merchant's profile. |
| MCC | Merchant category code. A four-digit code that describes what a merchant sells. MCCs affect card scheme fees, risk review, and whether a transaction needs 3DS. |

## Authorisation and capture

| Term | What it means |
|---|---|
| Authorisation | When the cardholder's bank checks the card and reserves the funds. This is the "is the card good?" step. An auth can be approved but the money is not moved yet. |
| Capture | When the merchant actually charges the card. Capture can happen at the same time as auth (most online payments) or later (hotels, car rental, pre-orders). |
| Settlement | The movement of funds from the card schemes to Kilbarra (or our sponsor bank for US merchants). Settlement is how we get the money to pay out to the merchant. |
| Payout | The transfer from the merchant's Kilbarra e-money balance to their external bank account. Payouts run on a schedule — see the payout run notes in the treasury workstation. |

## Money movement

| Term | What it means |
|---|---|
| E-money | Electronic money: the digital equivalent of cash. When a merchant receives funds from a card payment, we credit their e-money balance. It's not a bank deposit — it's an e-money liability on our books. |
| Safeguarding | The legal requirement to keep merchant funds separate from Kilbarra's own money. Safeguarded funds sit in dedicated accounts and are reconciled daily. Details in `finance-docs/treasury/safeguarding.md`. |
| Rolling reserve | A percentage of a merchant's daily volume held back for a set period (typically 5–10% for 90–180 days). It covers chargebacks and refunds if the merchant's balance does not. Shown on the merchant's profile in the back office. |
| Chargeback | A cardholder disputes a transaction through their bank. The funds are taken back from the merchant, plus a scheme fee. Chargebacks are handled by risk and support — see `risk-docs/risk/chargeback-monitoring.md`. |

## Compliance and risk

| Term | What it means |
|---|---|
| KYB | Know your business. Our onboarding checks on the merchant's legal entity, directors, and beneficial owners, run through the KYB onboarding tool. Not the same as KYC (which is about the merchant's customers). |
| 3DS | Three-Domain Secure. The cardholder authentication step (the redirect to their bank's page, or an in-app prompt). Required for most EU card-not-present transactions and for some US ones depending on the scheme and MCC. |

## Reading the merchant invoice

The invoice line items reference most of the terms above. The fee types are: interchange (passed through at cost), scheme fees (passed through at cost), our processing fee (per transaction or per volume depending on the plan), and any monthly or annual account fees. Chargebacks appear as a separate line per dispute. `merchant-docs/billing/invoices-and-fees.md` has worked examples.

## Where things happen

- Card auths and captures flow through the payments bus; the message store is in `eng-docs/payments-bus/message-store.md`.
- Payout runs are executed by Treasury Operations from the treasury workstation and settle via the core ledger.
- Merchant limits (including rolling reserve percentages) are shown on the merchant's profile in the back office; questions about them go to #risk-controls.
- If a merchant asks about a term not listed here, point them at the merchant dashboard's help centre and raise a ticket if it's about their account specifically.
