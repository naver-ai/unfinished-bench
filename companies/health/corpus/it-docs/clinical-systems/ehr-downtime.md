# EHR downtime procedures

**Owner:** Clinical applications (HIS)  
**Last edited by:** Yasmin Osei, Clinical Systems Analyst  
**Applies to:** The three hospitals and the US clinics (South Bend, Valparaiso, Kalamazoo). The Cork medical centre runs its own practice system and has its own downtime steps.

---

## When this procedure applies

The EHR is the clinical record for all patient-facing sites. Downtime means the EHR (or the parts of it needed for clinical care) is not available for charting, orders, or results review.

Two kinds of downtime:

- **Planned** — announced in advance, usually for maintenance. These go through the change management process and are communicated by Clinical applications (HIS) at least two working days ahead via chat and email to site leadership, nursing leadership, and clinic managers.
- **Unplanned** — the EHR is unavailable without prior notice. Clinical applications (HIS) declares unplanned downtime after confirming the outage with the infrastructure team.

## Who calls a downtime

- **Planned:** The change owner in Clinical applications (HIS) declares the downtime window. Aiko Young or their designee approves the communication.
- **Unplanned:** The on-call member of Clinical applications (HIS) confirms the outage with infrastructure and declares the downtime. If the outage affects only one site or one department, the clinical systems analyst may declare a downtime for that scope only.

Once declared, the downtime is announced in **#it-help** and the relevant site channel (**#southbend-campus**, **#valpo-office**, **#kalamazoo-campus**). The message includes the scope, the expected duration if known, and the time of the next update.

## Downtime reporting workstations

Every nursing unit and clinic front desk has at least one designated downtime reporting workstation. These are the white-labelled workstations with a paper sign taped to the monitor: **"DOWNTIME WORKSTATION — do not move or unplug."**

These workstations run a local instance of the downtime forms. They do not need the EHR to be up. If the downtime workstation itself is not working, use the paper forms from the downtime binders (see below) and call the service desk.

## Paper forms

Each unit and clinic keeps a **downtime binder** at the nurses' station or front desk. The binder contains:

- Paper encounter forms (visit, visit type, reason for visit)
- Paper order sheets
- Paper medication administration record (MAR)
- Paper lab requisitions
- Paper results log
- Downtime log sheet (one per patient)

During downtime, clinical staff chart on paper as they normally would in the EHR. Do not wait until the EHR is back to write things down. Write legibly, use the patient's name and date of birth on every page, and use the patient's MRN if known.

## During the downtime

1. The downtime announcement goes out in **#it-help** and the site channel. Unit clerks and clinic front desks confirm they have the downtime binder.
2. Continue to register patients using the downtime registration forms in the binder. Do not turn away patients who arrive without an appointment.
3. For orders, write the order on the paper order sheet and hand it to the appropriate department (lab, pharmacy, radiology). The receiving department enters the order into the lab information system or pharmacy system directly if those systems are up.
4. For medications, use the paper MAR. The pharmacy can still dispense from the paper order.
5. For results, use the paper results log. The lab information system and pharmacy system are separate from the EHR and may still be up. Results will be entered into the EHR after recovery.
6. For the Health Plan member-facing teams: the member portal and claims adjudication system are separate from the EHR. Member services and claims-ops continue as normal. The EHR downtime does not affect claims or member lookups in the member system.
7. The clinical systems analyst on call posts a status update to **#it-help** every hour, even if there is no change.

## Back-entry after recovery

When the EHR is back up, do the following:

1. The downtime announcement is rescinded in **#it-help** and the site channel. This is the official signal to begin back-entry.
2. Each unit or clinic designates a back-entry lead (usually the charge nurse or clinic manager). The lead coordinates who enters what.
3. Enter all paper encounters into the EHR as **downtime encounters**. Do not backdate the entry time; use the actual time of entry. The original visit time goes in the encounter notes.
4. Orders written on paper are entered by the ordering provider or by the clinical staff who received the paper order, following the usual order entry process. The paper order sheet is scanned into **chartarc** and attached to the patient's chart using the "downtime order" document type.
5. Medication administration from the paper MAR is entered into the EHR's medication administration record by the nurse who administered the medication, or by the charge nurse if the nurse is off shift.
6. Lab and radiology results that were reported on paper are entered into the EHR by the receiving department (lab, radiology). The paper results log goes to the HIM team for scanning into chartarc.
7. Each unit/clinic completes back-entry within two working days of the EHR coming back up. The back-entry lead confirms completion in the site channel.

## If it goes wrong

- **The downtime workstation is not working:** Use paper forms from the binder. Call the service desk and mention the downtime. The service desk has a stock of downtime workstations that can be swapped in.
- **Back-entry is behind schedule:** The back-entry lead should say so in the site channel. Clinical applications (HIS) can pull a report of open downtime encounters to help track what is left. Do not let back-entry pile up past two working days without escalation.
- **The EHR comes back but the interface engine is not processing:** The interface engine (HL7 feeds) may take time to catch up. Lab and pharmacy results may appear delayed. Do not re-enter results manually unless the interface has been confirmed as fully restored. Check **#it-help** for the all-clear from the interface team (Paloma Mishra or Fatima Fujita).
- **A patient is in the building and their chart is not available:** Use the paper chart from the unit or clinic. The clinical workstations and badge tap sign-in still work for workstation access, but chart access depends on the EHR being up. If the patient needs care and the chart is unavailable, treat using the paper record and note the limitation in the post-recovery entry.
- **The outage lasts longer than one shift:** The clinical systems analyst on call coordinates with nursing leadership and clinic managers to ensure each incoming shift knows the downtime is still active. The downtime binder stays in use until the EHR is confirmed back up.
- **Something is not covered here:** Ask in **#it-help** or **#his-platform**. Do not improvise in a way that creates a gap in the clinical record.
