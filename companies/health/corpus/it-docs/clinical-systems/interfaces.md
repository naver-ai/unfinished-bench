# Interface engine and HL7 feeds

**Owner:** Clinical applications (HIS)  
**Last edited by:** Fatima Fujita

## Scope

The interface engine handles HL7 v2.x traffic between the EHR, lab information system, pharmacy system, scheduling and registration system, and the claims adjudication system. This covers the main production feeds and the monitoring queues.

## Main feeds

| Feed | Source → Destination | Notes |
|------|---------------------|-------|
| ADT (A01–A08, A40) | Scheduling and registration → EHR, claims adjudication system | Patient admits, discharges, transfers, registrations. Also feeds the patient portal demographics. |
| ADT (A28–A31) | EHR → claims adjudication system | New/changed patient demographics for members. |
| Orders (ORM) | EHR → lab information system, pharmacy system | Inpatient and outpatient orders. |
| Results (ORU) | Lab information system → EHR | Auto-posting of results. |
| Charges (DFT) | EHR → billing system | Encounter charges. Review the charge capture queue in the EHR before expecting these to flow. |

The Cork medical centre runs its own practice system; its only feed here is the care summary for employer-group members treated both in Cork and at a US site. The European trials office works in the EDC and does not use HL7 feeds.

## Monitoring queues

- **Interface engine dashboard**: watch for messages stuck in the retry queue longer than 15 minutes. The dashboard is the first place to look when a clinician says "the result didn't post" or registration says "the patient isn't showing up."
- **Failed message queue**: messages that failed validation. Most common causes are bad patient IDs, missing attending physician, or invalid visit numbers.
- **Reconciliation report**: runs twice a day. Compares message counts between source and destination systems. A mismatch here means a feed is silently dropping messages — check this before escalating.

## Resending messages

- If a message is stuck in the retry queue and the destination system is back up, you can resend from the interface engine console. Select the message and choose **Resend**.
- If the message failed validation, fix the underlying data in the source system first. Do not resend a failed message without correcting it — it will just fail again.
- For a full replay of a feed (e.g., after a destination system restore), contact the interface team via the `#his-platform` channel. Do not replay an entire feed on your own; it can duplicate messages downstream.

## Vendor contacts

- **EHR vendor**: their support line is in the tickets system under the vendor contacts list. For interface engine issues, open a ticket with priority P2 and tag the HIS team.
- **Lab information system vendor**: they have a dedicated interface support mailbox. If results are not posting, check the ORU feed first, then contact them with the message IDs from the failed queue.
- **Pharmacy system vendor**: for order feed issues, call their interface desk directly. Their number is in the vendor contacts list in tickets.
- **Claims adjudication system**: this is internal. If ADT messages are not reaching the claims adjudication system, it's usually a mapping issue — escalate to Yasmin on the HIS team before calling anyone.

## Notes

- The interface engine is on the same VLAN as the VPN gateway; if the engine is unreachable, check whether the network team is doing maintenance in `#network-ops`.
- HL7 acknowledgements are turned on for all production feeds. If you see lots of AR (application reject) messages, check the destination system's interface log — it usually means a table lookup is failing.
- The old interface engine console (the web app that was replaced a while back) is still accessible on some workstations in the Kalamazoo data centre. Do not use it; it is not connected to the current message queues.
- For the Valparaiso health plan offices, the claims adjudication system is hosted in the South Bend data centre; latency on ADT messages is normal and does not need action.
- The `#his-platform` channel is the right place for interface questions. The `#infrastructure` channel is for engine hosting issues, not message content.
- Aiko has the credentials for the vendor support portals. The HIS team shared mailbox also has them, but the password was rotated recently — check the password manager rather than asking around.
