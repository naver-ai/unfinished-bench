# Monitoring visits

**Owner:** Clinical trials office  
**Last edited by:** Petra Delgado, Clinical Research Coordinator

## Monitoring plan

Each study gets a monitoring plan written by the Clinical trials office before the first site is activated. The plan sets the monitoring frequency (usually every 4–6 weeks for higher-risk studies, quarterly for lower-risk), the percentage of source data to verify, and whether visits are on-site or remote. The plan lives in the CTMS under the study record; the coordinating centre and the sponsor both have read access.

For studies where Kellsbrook is the sponsor, the trial master file in the CTMS holds the signed monitoring plan. For sponsor-initiated studies, the sponsor's CRO usually provides the plan; we keep a copy in the study folder and confirm it matches what we actually do.

## On-site visits

1. Log the visit in the CTMS at least five working days ahead (or as the monitoring plan allows). Add the visit dates and the scope (for example, "interim monitoring, first 20 enrolled participants").
2. Book a room near the research institute's clinical trials office in Kalamazoo, or at the Cork medical centre when monitoring the European site. The institute's front desk handles room bookings; the clinical trials office has two quiet rooms on the second floor.
3. Before the visit, pull the participant list from the EDC and cross-check it against the enrolment log in the CTMS. Note any participants whose visit windows have slipped — the site coordinator should have noted those in the CTMS.
4. On the day, start with the pre-visit meeting: the site coordinator (Fabio for Cork, otherwise the assigned coordinator) walks through enrolment, serious adverse events, and any protocol deviations logged since the last visit.
5. Perform source data verification (SDV). For each selected participant, compare the EDC entries against the source documents — the EHR, the participant's research chart, lab reports from the lab information system, and any paper diaries. Mark each verified field in the EDC as "SDV done" with the date and your initials.
6. Check the investigational product accountability log (for studies with an IP component) against what is physically in the secure storage. The clinical pharmacologist, Mei Lin, can help if quantities do not reconcile.
7. Review the informed consent forms for the selected participants — confirm each has the correct version, the ethics committee stamp, and the participant's signature date is before the first study procedure.
8. Hold the close-out meeting with the site team. Summarise what was found, what needs correcting, and the deadlines. Enter any findings in the CTMS as action items.
9. Write the follow-up letter (see below) and upload it to the study record in the CTMS.

## Remote visits

Remote monitoring uses the VPN client and gateway to reach the EDC and the CTMS. The interface engine feeds the EDC from the EHR, so most source data is visible remotely; anything that exists only on paper (consent forms, paper diaries, IP logs) still requires an on-site visit or a scan uploaded to the study record.

For a remote visit:

1. Request access to the EDC for the study if you do not already have it — the CTMS grants this automatically when you are assigned as monitor on the study.
2. Start the visit in the CTMS as "remote" and note the participants you will review.
3. Run the EDC's discrepancy report for the study; review each open query and close or re-issue them as needed.
4. Verify SDV remotely for the selected participants, using the same comparison against the EHR via the interface engine's data.
5. Schedule a video call with the site coordinator for the opening and closing meetings. Use the company chat to coordinate; if the coordinator is at the Cork site, mind the time difference and book in the late morning Irish time.

## Follow-up letters

After every visit (on-site or remote), write a follow-up letter in the CTMS and route it for review. The letter lists:

- The date and scope of the visit
- Action items, each with an owner, a due date, and a priority (critical, major, minor)
- For each action item, the finding, the correction needed, and where in the EDC or CTMS it should be documented

Send the letter to the site coordinator and copy the Clinical trials office. The letter is part of the study record and must be filed in the CTMS before the next visit is logged.

## Tracking action items to closure

Action items from monitoring visits are tracked in the CTMS. Each item stays open until the site coordinator marks it resolved and the monitor confirms the resolution.

1. Open the CTMS, go to the study record, and select "Action items".
2. Filter by status (open, in progress, closed) and by the visit date range.
3. For each open item, review the site coordinator's notes and any attached documents (for example, a corrected consent form or a new lab report).
4. If the resolution is acceptable, close the item and add a short note. If not, add a comment and leave it open; the system sends a reminder to the site coordinator every three working days.
5. For critical items, confirm the correction in the EDC before closing the item — do not rely on the coordinator's note alone.

The Clinical trials office reviews open action items at the monthly study team meeting. If an item has been open past its due date and the coordinator has not responded to two reminders, escalate to Ben Bauer, the Director of the Clinical Trials Office.

## If it goes wrong

- If you cannot reach the EDC or the CTMS during a remote visit, check the VPN connection first, then the IT service desk ticket queue. The on-call guide in it-docs lists the paging system number for urgent issues.
- If a participant's source data does not match the EDC and the discrepancy cannot be resolved in the same visit, log it as a critical finding and leave the EDC query open. Do not close the participant's record until the site resolves it.
- If the site coordinator is unavailable at the agreed visit time, reschedule the visit in the CTMS and notify the Clinical trials office. Do not proceed with the visit without the coordinator present.
- If you find missing consent forms or expired consent during SDV, stop the visit and inform the Clinical trials office immediately. The study may need to pause enrolment until the issue is resolved.
