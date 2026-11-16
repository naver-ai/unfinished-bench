# Setting up a new supplier

**Owner:** Procurement  
**Last edited by:** Ibrahim Richter (Vendor Manager)

---

## Supplier request form

- The requesting team submits the supplier request form in the tickets system with the supplier's legal name, trading name (if different), registered address, VAT / tax ID, and a short description of the goods or services.
- Attach a copy of the supplier's latest financial statements if the expected annual spend is above the threshold in the tickets form.
- If the supplier is already in the ledger, skip the request form and raise a change request against the existing supplier record instead.
- For subcontractors or resellers, name the underlying vendor in the request so we can check for conflicts of interest.

## Company and bank checks

- Procurement runs a credit check on the supplier's registered entity in its country of incorporation. For suppliers based outside the Netherlands or the US, allow extra time for the check.
- The supplier must provide bank details on company letterhead or via a secure bank confirmation. We do not accept bank details sent by email attachment.
- Confirm the bank account's currency matches the agreed invoicing currency. If the supplier invoices in a currency we do not normally pay, flag this in the request so the AP team can set up the currency in the expenses tool.
- For suppliers that will handle customer data (imagery, sensor readings, or anything derived from those), send the security questionnaire before any contract work starts. The questionnaire is reviewed by the security team; see `handbook/security/data-classification.md` for what counts as customer data.
- If the supplier's answers to the questionnaire raise any flags, Procurement coordinates with the security team and the requesting team before proceeding. Resubmission is common; allow for a second round.

## Data processing agreement

- A data processing agreement is required when the supplier will process personal data on our behalf. This includes things like HR records, customer contact details in the CRM, or field app user accounts.
- The DPA template is available from Legal and compliance. Do not use the supplier's own DPA unless legal has reviewed it.
- For suppliers that only provide hardware or connectivity for the ground sensor network, a DPA is usually not needed. When in doubt, ask the data governance team via the data catalogue or the #data-governance channel.

## Contract request to legal

- Once the checks are complete, raise a contract request in the tickets system with the completed supplier form, the questionnaire (if applicable), and the DPA status.
- Legal reviews the contract terms and returns a track-changes version or a summary of points. The requesting team is responsible for resolving commercial points with the supplier; legal handles liability, termination, and data protection clauses.
- Signing follows `handbook/legal/contracts-and-signing.md`.
- For tasking orders or imagery supply agreements, include the delivery terms from the imagery catalogue so the operations team can plan ingest capacity.

## Adding the supplier to the ledger

- After the contract is signed, AP creates the supplier record in the ledger. The supplier's bank details are entered from the confirmed bank documentation only.
- Tag the supplier record with the cost centre of the requesting team and, if the spend is project-specific, the project code from the analytics API usage tracking.
- The requesting team can then raise purchase orders against the supplier in the tickets system.
- Tell the supplier to send invoices with the purchase order number and the supplier ledger number. Invoices without these are returned by AP.
- If the supplier is used for recurring services (monitoring subscriptions, connectivity for sensor sites), set the renewal reminder in the CRM so the account owner is prompted before the term ends.
