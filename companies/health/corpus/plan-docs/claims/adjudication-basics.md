# How a claim moves through adjudication

**Owner:** Claims  
**Last edited by:** Chiara Sorensen (Claims Operations Lead)

---

This document walks through the life of a claim from the moment it arrives at Kellsbrook Health Plan until it reaches an adjudication decision. It is meant as an overview for people new to Claims and as a reference for anyone who needs to explain the process to another team.

## Intake

Most of our claims arrive as electronic 837 files through the clearinghouse. The clearinghouse does a basic format check before we see the file, but we still run our own validation when it lands in the claims adjudication system. If the file fails structural validation, it goes to a rejection queue and the clearinghouse is notified so the submitter can correct and resend.

Paper claims come through the mailroom at the Valparaiso office. The mailroom scans every envelope and routes the images to the claims document ingest pipeline, which runs OCR and attaches the images to the claim record in the adjudication system. Paper claims with a legible CMS-1500 or UB-04 form are entered by the intake team; if the form is not legible or the OCR confidence is low, the claim waits in the scanning queue for manual review.

The filing clock starts on the date the claim reaches us, not the date on the provider's form. For the specifics of timely filing, see the timely filing and corrections document.

## Front-end edits

Once a claim is in the system, it runs through front-end edits. These are the most basic checks:

- Member is on the file for the date of service
- Subscriber ID and group number are present and match
- Provider is in our network or has a valid out-of-network profile
- Place of service and type of bill are valid for the line items
- Date of service is not in the future
- Diagnosis codes are valid for the date of service

Claims that fail a front-end edit are rejected back to the submitter with an explanation, or pended if the issue looks like something we can resolve from the record we already have. For example, an invalid subscriber ID on an otherwise clean electronic claim might pend so an examiner can check whether the member recently changed ID numbers.

## Eligibility and benefits

If the claim clears the front-end edits, it moves to eligibility and benefits. The adjudication system checks the member's eligibility for the date of service, including whether the member was active in the product line billed (employer group, individual plan, or {{MANAGED_PLAN_PROGRAM}}). It also verifies:

- Copay, coinsurance, and deductible amounts that apply
- Remaining deductible and out-of-pocket accumulators
- Whether the service is a covered benefit under the member's plan
- Coordination of benefits status

If the member has other coverage on file, the claim may pend for a coordination of benefits questionnaire. The COB questionnaire goes to the member asking about their other coverage; we hold the claim until the questionnaire comes back or the response window closes. If the member does not respond, we process the claim as primary and note the other coverage on the record.

## Pricing

After eligibility and benefits, the claim is priced. In-network claims are priced against the fee schedule for the provider's contract. The fee schedule is loaded in the adjudication system by contract, and the system applies the correct rate based on the service code, place of service, and the provider's specialty.

Out-of-network claims are priced against the out-of-network schedule, which is a percentage-based reduction from billed charges. The system applies the member's out-of-network benefit level and the balance-billing rules for the member's state (Indiana, Michigan, or Ohio for the small number of members who live across the border and have an out-of-state primary).

If a service code is not in the fee schedule, the claim pends for manual pricing. The examiner checks whether the code maps to a similar service, whether it was part of a packaged rate, or whether it needs to go to the pricing team for a one-off determination.

## Coding edits

Once priced, the claim runs through coding edits. These check:

- Procedure codes are valid for the diagnosis codes on the claim
- Modifiers are appropriate for the service
- Units are within expected ranges for the service
- National Correct Coding Initiative (NCCI) edits are applied
- Medically unlikely edits (MUEs) are applied

A claim that fails a coding edit is pended with the specific edit reason. Most of these are resolved when the provider sends corrected information or when an examiner reviews the record and sees that the edit is not applicable (for example, a bilateral procedure billed with the correct modifier but the edit did not recognize it).

## Pend reasons

Claims can pend for many reasons. The most common ones we see:

- Missing information, such as an attachment, a referral number, or a prior authorization reference
- COB questionnaire outstanding
- Coding edit questions
- Pricing questions
- Eligibility questions that need a manual look at the member record
- Provider credentialing questions (for example, a new provider who is not yet in the credentialing system)

Pended claims sit in the work queues until an examiner picks them up. We do not automatically deny a claim just because it pended; the examiner reviews the record, reaches out to the provider or member if needed, and either resolves the pend or moves the claim to a denial with a clear reason.

## Examiner work queues

Examiners work out of several queues in the claims adjudication system. The queues are organized by pend reason and by product line, so a {{MANAGED_PLAN_PROGRAM}} claim with a coding edit goes to a different queue than a commercial group claim with the same edit. The Claims Operations Lead (Chiara) and the senior examiners monitor queue sizes and reassign work as needed.

When an examiner opens a claim, they see the full claim record, any attached documents from the ingest pipeline, and the pend reason. They work the claim from there. If the examiner needs to speak with the provider, they use the provider portal notes or place a call. If they need to speak with the member, they use the member contact log in the adjudication system.

Examiners are expected to resolve pends in the order the claims arrived, unless a claim has a clinical urgency flag or the member has an active appeal. The examiner quality audit process samples work from every examiner on a rolling basis; the quality audit document has the details.

## Approval

When all edits are passed and any pends are resolved, the claim is approved. The adjudication system calculates the payment amount, applies the member's benefits, and posts the claim to the payment queue. The claim leaves the examiner's queue and moves to the payment run process, which is covered in a separate document.

A claim can also be denied, in which case the system generates a denial explanation that is sent to the provider and the member (where required). Denied claims stay on the examiner's worklist until the denial letter is issued, so the examiner can confirm the reason is correct before it goes out.

## After adjudication

Once adjudicated, the claim record is final unless a correction, void, or appeal comes in. The timely filing and corrections document covers corrected and voided claims, and the appeals and grievances document covers member appeals. Providers can submit reconsideration requests through the provider portal; those come back to the Claims team as a new work item with the original claim linked.

If you are not sure where a claim is in the process, the claim record in the adjudication system shows a status history with timestamps for each step. You can also check the claims payment queue for anything that has been approved and is waiting on the payment run. For questions about a specific claim, ask in #claims-ops or bring it to the weekly Claims team huddle.
