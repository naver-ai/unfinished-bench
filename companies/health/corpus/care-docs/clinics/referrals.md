# Outgoing referrals

> Needs updating after the move — ping #clinic-ops if something here looks wrong.

Owner: Clinics (primary and specialty care) · Last edited by Marisol Molina

## Placing a referral in the EHR

1. Open the patient chart in the EHR and go to **Orders** → **Referrals**.
2. Select **New Referral**.
3. Choose the referral type:
   - **Specialist** — for clinic or hospital-based specialty visits
   - **Imaging** — for radiology, MRI, CT, ultrasound
   - **Therapy** — for PT, OT, speech
   - **Behavioral health** — for psychiatry or counseling
4. Search for the receiving provider or practice. In-network specialists appear first in the search results with a blue **IN** badge. Use those unless the patient has already seen an out-of-network specialist and the visit is a follow-up.
5. Set the **reason for referral** using the patient's own words where possible, plus the relevant diagnosis code. Do not leave this blank — the receiving office calls us when it is blank.
6. Attach any required documents (recent notes, lab results, imaging reports) using the **Attach from chart** button. This pulls from the patient's record directly; do not upload scanned copies unless the original is in chartarc.
7. Click **Submit**.

## Prior authorization hand-off

1. After the referral is submitted, check if the destination service requires prior authorization. This shows in the EHR as a **PA required** flag on the referral.
2. If the flag is present, create a prior authorization request in the prior authorization queue **before** telling the patient to book an appointment.
3. Attach the referral record and any supporting clinical notes. The UM team works the queue in order; routine requests are usually decided within two working days.
4. Once the response comes back, update the referral status in the EHR to **Approved** or **Denied**. If denied, the ordering clinician is notified through the EHR worklist — do not relay the denial yourself.
5. For patients covered by Kellsbrook Health Plan, the prior authorization queue is the same one used by the plan's UM team. For other payers, follow the payer's own portal or phone process and note the authorization number in the referral record.

## Tracking referrals that haven't been scheduled

1. Open the **Referral Worklist** from the EHR home screen.
2. Filter by **Status = Sent, Not Scheduled**.
3. Review the list weekly. For each referral older than 10 working days:
   - Call the receiving office to confirm they received it and ask about scheduling availability.
   - If the patient has not heard from the office, call the patient and offer to resend the referral or help book the appointment.
   - If the patient declines the referral or finds a different specialist, mark the referral **Closed — Patient declined** or **Closed — Other provider**.
4. If a referral comes back as **Returned** (the receiving office rejects it), check the reason. Common reasons: missing documentation, wrong provider, or service not covered. Fix the issue and resubmit within two working days.
5. Referrals to Cork-based specialists (for our Cork medical centre patients) follow the same process but the worklist shows them under the Cork site. The receiving office there uses the same EHR, so nothing different is needed.

## If it goes wrong

- **Referral was submitted to the wrong provider** — void the referral and create a new one. Do not edit the receiving provider on a submitted referral; the receiving office may already have pulled it into their schedule.
- **Duplicate referrals** — if the same patient has two open referrals for the same service, close the older one with status **Duplicate** and keep the newer one.
- **Referral lost or not received by the office** — resend through the EHR using **Resend** on the referral record, then call the office to confirm. If it still does not arrive, contact #his-platform with the referral number.
- **Patient calls saying the specialist won't see them** — check whether the referral has a **PA required** flag that was never actioned. If so, escalate to the prior authorization queue right away and update the patient on the expected timeline.
