# Study IDs and pseudonymisation

**Owner:** Research data management  
**Last edited by:** Marco Ferrari (Clinical Data Coordinator)

## How study IDs are assigned

1. When a new study is set up in the CTMS, the study coordinator creates the participant ID list. The ID format is `<study short code>-<site>-<3-digit sequence>`, e.g., `MEL-02-KAL-014` for the Kalamazoo site or `MEL-02-CRK-003` for Cork.
2. The study coordinator generates the ID list in the CTMS using **Create Participant IDs** under the study's Participant tab. The system assigns the sequence numbers automatically and will not reuse a number even if a participant is screen-failed or withdrawn.
3. Assign the next ID in sequence at the point of consent, not before. If consent is taken at a clinic visit, the coordinator on site assigns the ID. For trials run out of the Cork office, the Cork coordinator pulls the next ID from the same CTMS list.
4. The participant's name, date of birth, and contact details are recorded against the study ID in the eIRB study record and in the CTMS. These are the only two places where the linkage key lives.

## The linkage key

5. Access to the linkage key (the list that maps study ID to direct identifiers) is restricted to the study coordinator, the Study Data Manager (Esme Latimer's team), and the Principal Investigator. The eIRB system enforces this by role: the **Study Coordinator** role and the **Research Data Management** role are the only roles that can open the Participant Identifiers screen.
6. The CTMS also holds the key but the screen is hidden for anyone with the **Data Entry** role. If you need to see it and you don't have a role that permits it, ask the study coordinator or Esme's team. Do not ask anyone in IT to grant you the role directly — that goes through the access request process in `handbook/it/access-requests.md`.
7. The linkage key is never exported. If a monitor or an external body asks for it, point them to the monitoring visits process in `research-docs/trials/monitoring-visits.md`.

## Direct identifiers out of analysis datasets

8. Analysis datasets are built in the data warehouse from the EDC. The EDC extracts use only the study ID; the EDC does not hold name or date of birth.
9. When we pull data from the CTMS into the warehouse for a study report, the extract job strips name, date of birth, and contact fields automatically. If you are building a dataset manually (e.g., for an ad-hoc query), remove those fields yourself and check the output before saving anything to a shared location.
10. Free-text fields in the EDC sometimes contain names or dates entered by data entry staff. The EDC has a flag on each text field called **Contains PHI** that the data entry person sets at entry time. When you build an analysis dataset, filter out any field where that flag is set.
11. If you find a direct identifier in a dataset that should not be there, remove it and tell the study coordinator so they can update the entry guidance for that study.

## Dates

12. For analysis datasets, full dates of birth are replaced with year and month only (`YYYY-MM`). This is done in the warehouse view `research.demographics_shifted` — use that view rather than the raw table.
13. Event dates (visit dates, procedure dates, adverse event onset dates) are shifted by a random offset per participant, between −30 and +30 days. The offset is assigned once per participant and stored in the warehouse table `research.date_offsets`. The same offset applies to all events for that participant so the intervals between events stay correct.
14. If you need an unshifted date (e.g., for a monitoring visit or a serious adverse event report), pull it from the EDC directly, not from the warehouse. Do not export unshifted dates into any shared dataset.

## If it goes wrong

- You assigned an ID to the wrong person: contact the study coordinator immediately. The CTMS allows the ID to be reassigned to the correct participant only before any data has been entered against it. If data already exists, the ID is retired and the participant gets a new one; tell Esme's team so they can update any datasets that already contain the retired ID.
- You exported a dataset and find a name or DOB in it: do not email the file to anyone else, do not copy it to a shared drive. Delete the local copy, rebuild the export without the identifier, and tell the Study Data Manager. They will check whether the file went anywhere it should not have.
- The date shift looks wrong (e.g., a visit date falls before the consent date): check the offset in `research.date_offsets` for that participant. If the offset was applied twice, the warehouse job logs the error in `research.date_shift_errors`. Ask data engineering to reset the offset for that participant.
- Someone without the right role asks you to open the linkage key: tell them to request access through the eIRB role request form. Do not share your own access.
