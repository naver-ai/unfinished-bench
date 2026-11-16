# Quality measures we report

Owner: Quality & patient safety  
Last edited by: Leon Singh

This page lists the measure sets we report externally, where the numbers come from, and which team owns the submission. If you are looking for internal quality-improvement work that is not tied to a reporting program, that lives with the operating teams and is not tracked here.

## {{HEALTH_PROGRAM_REGULATOR|code}} inpatient measures

Reporting for the three hospitals (South Bend, Valparaiso, Kalamazoo) runs through the EHR and the data warehouse. Extraction queries are maintained by Data & analytics engineering; the measure definitions live in the quality team's own files. Joy Balogun owns sign-off before anything is transmitted. The clinical teams are responsible for documenting the elements that feed the measures — if a measure drops, the first question is usually whether the documentation was complete at discharge.

| Measure area | Source | Owner |
| --- | --- | --- |
| Readmissions (all-payer, 30-day) | Data warehouse from EHR and claims feeds | Jasmine Schmidt's team prepares; Joy Balogun submits |
| Mortality | EHR discharge data | Quality & patient safety |
| Hospital-acquired conditions (HAC) | Safety event reporting system + EHR | Leon Singh |
| ED throughput | Scheduling and registration system | Operations, with Quality & patient safety review |
| Sepsis care | EHR flowsheet data | Nursing leaders, with Quality & patient safety |

## HEDIS

The health plan's HEDIS measures are calculated from claims adjudication system data plus the member portal and the EHR for supplemental data (for example, blood pressure readings from a clinic visit that did not generate a claim). The data warehouse pulls from all of those. Kellsbrook Health Plan members are the denominator population; we do not include the Cork medical centre in HEDIS.

The annual HEDIS season runs from the start of the measurement year through the close-out period. Data & analytics engineering extracts the rates, and the health plan's quality staff review them before submission. If you have a question about a specific measure, start with the Data & analytics team — they keep the measure logic and the known data gaps.

| Measure area | Source | Owner |
| --- | --- | --- |
| Childhood immunizations | EHR + state registry feeds via the interface engine | Quality & patient safety with Pediatrics |
| Diabetes care (HbA1c, eye exam) | EHR + claims | Health plan quality staff |
| Breast cancer screening | Claims + EHR | Health plan quality staff |
| CAHPS | Survey vendor files | Patient experience team with health plan quality staff |
| Medication adherence | Pharmacy system + claims | Health plan quality staff |

## Other reporting

- **State reporting** — Indiana and Michigan each have their own inpatient and ambulatory reporting. These are handled by the same extraction process as the {{HEALTH_PROGRAM_REGULATOR|code}} measures, with state-specific suppression rules applied by the data warehouse. The Valparaiso and South Bend campuses report to Indiana; Kalamazoo reports to Michigan.
- **{{HEALTH_PROGRAM_REGULATOR|code}} Star Ratings** ({{MANAGED_PLAN_PROGRAM}}) — pulled from the same HEDIS sources plus the appeals and grievances system. The health plan quality staff own the submission.
- **Patient experience** — HCAHPS for the hospitals and CG-CAHPS for clinics. The survey vendor samples from our discharge and visit files and runs the mailings; the patient experience team owns the results.

## Where the numbers come from

Most measures are extracted from the data warehouse, which receives daily feeds from the EHR, the claims adjudication system, the pharmacy system, and the lab information system. The warehouse is the source for every submission on this page. If a number does not reconcile between the warehouse and the source system, the Data & analytics team investigates — do not adjust a submission to make it match a source system total without involving them.

For chart review measures (readmission validation, HAC), the reviewers pull charts in the EHR; older scanned charts come from the chart archive.

## Who to contact

- Joy Balogun — final sign-off on {{HEALTH_PROGRAM_REGULATOR|code}} and state submissions
- Leon Singh — HAC and safety-event related measures
- Jasmine Schmidt — extraction logic, warehouse questions, HEDIS technical work
- Health plan quality staff (through the health plan office in Valparaiso) — HEDIS submission and Star Ratings
- Patient experience team — CAHPS-related reporting

If you are not sure which program a measure belongs to, ask in #nursing-leaders or #data-eng rather than guessing. The quality team keeps the current measure list and the submission calendar in the shared drive.
