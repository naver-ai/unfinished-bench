# Provider EFT and remittance

**Owner:** Provider services  
**Last edited by:** Daisuke Khan (Provider Network Specialist)

This covers EFT enrollment through the provider portal, bank letter verification, 835 remittance files, paper checks via the print vendor, and remittance questions from providers.

## EFT enrollment

1. Provider signs in to the provider portal and goes to **Payments → EFT enrollment**.
2. Provider enters the bank routing number, account number, and account type (checking or savings), then uploads a voided check or bank letter.
3. Provider submits the enrollment. The portal creates a task in the credentialing system under Provider services.
4. Provider services reviews the task. If the uploaded document is a voided check, no further verification is needed. If it is a bank letter, the letter must be dated within the last 90 days and show the provider's legal business name and the full account number.
5. If the bank letter is missing any of those, send the task back through the portal with a note telling the provider what to correct. Do not accept a screenshot of online banking.
6. When the bank details check out, mark the task complete in the credentialing system. The provider's EFT profile becomes active in the claims adjudication system on the next working day.

## 835 remittance files

- EFT-enrolled providers receive an 835 file with each payment run. The file is posted to the provider portal under **Payments → Remittance**.
- Providers who use a clearinghouse can have the 835 delivered there instead. That is set in the provider portal under **Payments → Remittance delivery**, and the clearinghouse routing ID is validated by Provider services before the change takes effect.
- The 835 is generated from the claims adjudication system after the payment run completes. If a provider says they have not received a file, check the payment run in claimsctl first, then check whether the provider's EFT profile is still active.

## Paper checks

- Providers who are not EFT-enrolled receive paper checks. The check and remittance advice are sent through the print vendor on the same day the payment run completes.
- The print vendor sends a confirmation file back, which is loaded into the claims adjudication system. Use that confirmation to answer "was it printed" questions.
- If the confirmation file is missing, contact the print vendor through tickets with the payment run ID.

## Answering remittance questions

- Most questions are about a specific claim's payment amount, adjustment reason codes, or why a claim paid to a different provider. Pull the claim in the claims adjudication system and read the adjustment codes before answering.
- For questions about a payment run that has not settled, check claimsctl for the run status before telling the provider anything.
- If the question is about a claim that is still in adjudication, say so and give the expected working day based on the adjudication queue. Do not guess.

## If it goes wrong

- **EFT payment rejected by the bank:** the claims adjudication system flags the payment. Verify the account details with the provider, have them re-submit a voided check or bank letter, and the rejected payment is reissued on the next payment run.
- **Provider says the 835 did not arrive:** confirm the file was generated and posted, then check the delivery method on file. If it is portal delivery, the file is there. If it is clearinghouse delivery, confirm the routing ID with the clearinghouse before re-sending.
- **Wrong payment amount:** do not adjust anything on a phone call. Have the provider submit a written remittance inquiry through the provider portal. Provider services reviews it against the adjudication record and responds through the portal.
- **Check lost in the mail:** the provider can request a stop payment and reissue through the provider portal. Stop payments go through the claims adjudication system and the reissue is sent on the next print run.
