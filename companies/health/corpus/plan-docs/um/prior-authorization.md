# Prior authorization

**Owner:** Utilization management  
**Last edited by:** Leah Dubois, Case Manager, RN

## What needs prior authorization

Prior authorization (PA) is required for the service categories listed in the benefits summary for each Kellsbrook Health Plan product. The full list is maintained in the claims adjudication system's benefit configuration, and the provider portal shows which CPT/HCPCS codes require PA for a given member's plan. As a general rule, anything that is not a routine office visit, preventive service, or emergency stabilization should be checked.

{{MANAGED_PLAN_PROGRAM}} products have their own PA list that overrides the commercial list where they differ. The Cork medical centre does not bill through Kellsbrook Health Plan, so PA does not apply to services delivered there — it applies only to US plan members receiving care from network or out-of-network providers.

## How requests arrive

1. **Provider portal submissions** — Most requests come in through the provider portal. The portal validates that the provider is in the credentialing system and that the member is active at the time of submission.
2. **Fax** — Providers who are not set up on the portal can fax the PA request form to the utilization management fax line. The fax lands in the document archive and is routed to the prior authorization queue by the interface engine. Faxed requests are worked in the same queue as portal submissions.
3. **Internal requests** — Occasionally a Kellsbrook clinic or hospital department submits a PA on behalf of a patient (for example, when a referral requires it). These come through the provider portal using the clinic's own credentials.

## Working the queue

The prior authorization queue is in the claims adjudication system, under the Utilization management worklist.

1. Open the request and confirm:
   - the service and diagnosis codes match what the provider submitted
   - the rendering provider is in the credentialing system (or the request is for a facility-based service where the facility is contracted)
   - the member's benefit plan covers the service
2. Check whether the service matches the clinical criteria published in the utilization management policy library. The criteria are also available inside the claims adjudication system as an integrated reference.
3. If the request meets criteria, approve it. The system sends the approval to the provider portal and records the authorization number.
4. If the request does not clearly meet criteria, route it to the medical director review worklist with a brief note about what is missing.

## Turnaround targets

- **Standard requests:** decision within 3 working days of receipt.
- **Expedited requests:** decision within 1 working day. Expedited applies when the treating provider indicates the standard timeline could seriously jeopardize the member's life or health.
- **Post-service requests:** reviewed under the same criteria but flagged for the provider's attention on timely filing.

If we do not have enough information to make a decision, we send an information request to the provider and the clock pauses until the information arrives.

## Peer-to-peer review

When a request is denied, the requesting provider can ask for a peer-to-peer review. The provider calls the utilization management line and is connected to a physician reviewer. The reviewer can overturn the denial if the additional clinical information supports it. Peer-to-peer requests are tracked in the prior authorization queue; if the provider does not request one, the denial stands and the member can appeal through the appeals and grievances process.

## Linking authorizations to claims

When a claim comes through adjudication, the system matches it to the authorization using the member, the rendering provider, and the service code. The authorization number does not need to appear on the claim for the match to work, but it helps when the service code was billed with modifiers. If a claim does not match an authorization, it denies with a "prior authorization required" reason code and the provider can submit a corrected claim once the authorization is on file.

## If it goes wrong

- **Wrong member selected at submission** — The request was submitted for a different member in the same family. Contact the provider to confirm the intended member, then move the request to the correct member record.
- **Duplicate requests** — Providers sometimes submit both a portal request and a fax. Keep the earliest submission and close the duplicate with a note.
- **Criteria reference not loading** — If the clinical criteria reference fails to open in the claims adjudication system, use the utilization management policy library directly and note the policy version in the request.
- **Authorization approved but claim denied** — Usually a code mismatch (modifier, place of service). Check the authorization's approved code list before contacting the provider.
- **Provider says they never got the decision** — Verify the decision was posted, then resend through the provider portal. For faxed decisions, the fax log is in the document archive.
- **A request sits in the queue past the target** — Escalate to the utilization management supervisor. The queue is reviewed each morning and again mid-afternoon, so this should be rare.
