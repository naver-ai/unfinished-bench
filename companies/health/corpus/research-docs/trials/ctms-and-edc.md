# CTMS and EDC basics

**Owner:** Research data management  
**Last edited by:** Anton Ozturk (Research Data Manager)

## What lives where

- **CTMS** — study setup, site activation status, visit tracking, monitoring visit reports, delegation logs, training records, regulatory documents, enrollment metrics.
- **EDC** — the actual participant data: case report form (CRF) responses, lab values, adverse events, concomitant medications, visit assessments.

Keep the two in sync but don't duplicate. If it's a data point collected from a participant, it goes in the EDC. If it's about how the study is running, it goes in the CTMS.

## Study build and access

- Study build requests go through Research data management. Lead time is two working weeks for a standard Phase II/III build, longer if the protocol needs custom CRFs.
- EDC access is role-based. Principal investigators get full view; coordinators get entry and review; monitors get read-only plus query capability. Research data management approves all access changes.
- CTMS access follows the same approval path. The Cork trials office staff get the same roles as their US counterparts.
- Access requests go through the normal tickets system. Tag the study record with the study ID so the build team can find it.

## Data entry timelines

- **Entry:** within two working days of the visit completing. If the visit is done by a locum or covering clinician, the person who did the visit enters the data; don't wait for the next regular clinic day.
- **Source document review:** within five working days of entry. The clinical data coordinator assigned to the study does this in the EDC, not on paper.
- **Query resolution:** queries should be answered within three working days of being raised. If a query sits unanswered for five working days, it escalates to the Study Data Manager.
- For studies run out of the Cork site, the same timelines apply. Maeve's team at the front desk books visits with the data entry deadline in mind, so flag scheduling conflicts early.

## Query workflow

- Queries are raised in the EDC by the data management team or by monitors during monitoring visits. All queries stay in the EDC — no email answers.
- When answering a query, correct the source data first, then answer the query. If the source data is already correct, explain why the query is not applicable.
- Don't close a query and make the data change in the same edit. Make the edit, save, then answer the query.
- If a query requires a source document that's in chartarc, pull it there and attach the reference to the query response.

## Database lock

- Lock requests come from the sponsor or the study lead. Research data management coordinates the lock checklist.
- Before lock: all queries closed, all visits entered, all discrepancies resolved. If a query is still open at lock time, the study is not locked.
- Once locked, the EDC prevents all data changes. A post-lock correction needs an unlock request to Research data management and is tracked in the CTMS.

## Notes

- The eIRB approval letter and the signed protocol get filed in the CTMS before the first data entry. If they're missing, the build team won't open the EDC.
- For studies with a lab component, lab values flow from the lab information system through the interface engine into the EDC. Don't rekey lab values manually; if the feed is down, tell Research data management before the visit window closes.
- When a protocol amendment changes the CRFs, the EDC rebuild is a separate piece of work — don't assume the EDC is updated just because the amendment has gone through.
