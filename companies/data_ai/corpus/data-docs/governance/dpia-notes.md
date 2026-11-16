# DPIA notes

Owner: Legal and compliance  
Last edited by: Liesbeth Kramer

## When a DPIA is needed

We run a DPIA when we start processing personal data that is likely to result in a high risk to individuals. In practice that means:

- New use of high-resolution imagery that can identify homes, gardens, boats, vehicles or people (not just bare land / agricultural parcels)
- New use of sensor data that tracks movement of people or vehicles over time
- Recording or transcribing calls or chats that contain personal data
- Combining datasets that weren't combined before and could lead to re-identification
- Large-scale profiling of individuals (even if the output is aggregated)

If you're unsure whether your project needs a DPIA, ask Mina Novak (DPO) before you start building. The team does not need a formal request template — a message to Mina with a short description of the data flow is enough to get a decision.

## Recent DPIAs

### High-resolution imagery over residential areas

Completed, with the imagery-ops and eo-models teams. The DPIA covered our 30 cm and finer imagery products over residential zones in the Netherlands and the US. We concluded that the risk is acceptable where we:

- Redact imagery at request of the DPO where a specific address is the subject of a customer request
- Keep the imagery catalogue access logs for a rolling period of 13 months
- Do not apply facial recognition or licence-plate reading models to any imagery

Loose end: the DPIA references the old catalogue tool (the pre-STAC catalogue) in section 4.2. The section should point to the current imagery catalogue but hasn't been updated. Mina knows.

### Support call recorder

Completed, with the support systems team. We record support calls through the phone system in the helpdesk. The DPIA concluded:

- Recordings are kept with the case record for its queue (see platform-docs/support-systems/case-records.md)
- Call recordings are only accessible to the support systems team and to Karim Rossi's quality reviewers
- Customers are told the call is recorded when they join the queue
- We do not use call recordings for model training or analytics

Loose end: the DPIA still lists a support systems reviewer who has since left. The next review should name Eero Schmidt instead.

### Field app location tracking

Completed, with the sensor network team. The field app records the location of sensor technicians during site visits so we can map sensor positions accurately. The DPIA concluded:

- Location is only collected while the field app is open and a visit is active
- Location history is stored in the sensor network database, not in the field app itself
- Access to location history is restricted to the sensor network team and to the support team when troubleshooting a sensor reading
- Location history older than 24 months is purged automatically

Loose end: Ben Bose raised a question about whether the app should also collect location in the background for safety reasons (technicians working alone in remote areas). That question was parked and has not been resolved. If we decide to enable background collection, we need to revisit the DPIA.

## Contact

Mina Novak is the Data Protection Officer. She reviews and signs off all DPIAs. If Mina is unavailable, contact Liesbeth Kramer in Legal.

## Review cycle

DPIAs are reviewed when the processing changes, and at least every 24 months. The review is usually a short check of whether the processing still matches what the DPIA describes. The Legal team tracks review dates in the legal matter tracker.
