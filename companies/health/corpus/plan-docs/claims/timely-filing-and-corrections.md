# Timely filing, corrected and voided claims

**Owner:** Claims  
**Last edited by:** Chiara Sorensen (Claims Operations Lead)

**What does "timely filing" mean in days?**

- Employer group and individual plans: 180 days from date of service
- {{MANAGED_PLAN_PROGRAM}}: 365 days from date of service (except where {{HEALTH_PROGRAM_REGULATOR|code}} rules say otherwise for specific claim types)

**When does the clock start?**

Date of service for most claims. For inpatient stays, it is the discharge date. For professional claims with a span of dates, it is the last date on the claim.

**What if the claim was submitted on time but the clearinghouse rejected it?**

We look at the clearinghouse rejection date and the original submission timestamp in the interface engine logs. If the original submission was within the filing limit and the corrected resubmission goes out within 30 days of the rejection, we treat it as timely. The resubmission needs to come back through the normal clearinghouse path — not by fax or through the provider portal.

**What about the clearinghouse outage we had a while back?**

For claims that failed during an outage, we extended the filing limit by the number of full days the outage lasted. The outage dates were posted in #claims-ops and on the adjudication system's sign-in banner. If a provider says they submitted during the outage and we have no record of it, ask for their clearinghouse confirmation page or submission report. Lin and Dara have been handling those lookups.

**What is a corrected claim (frequency code 7)?**

A corrected claim replaces the original in its entirety. We do not merge information from the original and the correction. The corrected claim must contain the complete, accurate billing information — all lines, all charges, all modifiers. The provider should not send a corrected claim just to add a missing attachment; attachments go through the usual documentation request process.

**What do examiners check on a corrected claim?**

- That it was submitted within the filing limit (or within 12 months of the original paid or denied claim, whichever is later)
- That the original claim exists in the adjudication system and matches on member ID, date of service, and provider NPI
- That the correction is actually a change, not a duplicate resubmission of the same information
- That the "original claim number" field is populated. If it is blank, we cannot link it and it will pend.

**What is a void (frequency code 8)?**

A void cancels the original claim. It is used when the claim should never have been billed — wrong patient, wrong service date, or the service did not happen. A void is not a way to correct a small error; that is what a corrected claim is for.

**What happens after a void is processed?**

The original claim is reversed in the adjudication system and in the data warehouse. If the original was already paid, the payment is recovered through the normal overpayment process. The provider will see the void on the next remittance advice.

**Can a void be submitted after the filing limit?**

Voids are not subject to timely filing limits. If the provider needs to void a claim, we process it regardless of how old the original is.

**Who reviews corrected and voided claims?**

All claims examiner levels can process them. Senior examiners handle corrected claims where the original was already paid or where the adjustment crosses a benefit year. If a corrected claim changes the member's cost share, it goes to the member services queue for a possible refund or additional billing.

**What documentation do we keep?**

The original claim image, the corrected or voided claim image, and the adjudication history showing the linkage between them. Paper claims are scanned in the mailroom, so all the images come through the claims ingest pipeline.

**Questions?**

Ask in #claims-ops or tag Chiara. For {{MANAGED_PLAN_PROGRAM}} filing limit questions, check the plan products page in plan-docs/overview/plan-products.md.
