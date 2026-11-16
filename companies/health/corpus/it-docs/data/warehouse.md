# Enterprise data warehouse

Owner: Data & analytics engineering  
Last edited by Anders Tran

## What lives here

The warehouse is the main reporting and analysis platform for Kellsbrook Health, covering:

- **Encounters** — hospital, clinic and urgent care visits from the EHR via the interface engine. Includes ED, inpatient, outpatient and professional encounters. Kalamazoo and South Bend feeds land separately, then get merged. Valpo hospital is on the same feed as South Bend.
- **Claims** — adjudicated and paid claim lines, plus enrollment from the Health Plan member system. The claims tables are refreshed from the claims adjudication system nightly along with the payment run output. Denials and adjustments are in the `claims_adjust` schema.
- **Quality** — quality measures we report, pulled from the EHR and the safety event reporting system. This is the source for the quarterly board pack and the value-based contract reporting.
- **Finance** — general ledger detail, charges from revenue cycle, and cost accounting feeds from the hospital systems. Payroll actuals land monthly from the HR system.

## Loads

- Nightly batch starts at the data centre in South Bend, finishes before the first shift arrives. Cork runs a shorter refresh mid-morning their time for the practice and trials office.
- The claims load is the long pole. If it misses the window, the whole batch shifts and we tell Jasmine before the South Bend offices open.
- The pharmacy system feed is still landing through the old SFTP drop on the Kalamazoo box. It's scheduled to move to the interface engine but hasn't happened yet.

## Access requests

- Request access through tickets, type "Warehouse access". Data & analytics engineering reviews and provisions within a couple of days.
- Read-only by default. Write access to the `analytics_work` schema only, and only if the request is from a member of the data team or someone Jasmine approves.
- PKI or VPN required from off-campus. The VPN profiles in it-docs/network/remote-access-vpn.md are fine for the warehouse.

## Report catalogue

- The catalogue lives in the data warehouse itself, `report_catalog` schema. If you can't find a report there, it probably doesn't exist.
- The patient survey dashboards and the complaints dashboard are maintained by the analytics team — data lands from the survey vendor files and the complaints queue.
- Research analysis datasets live in the `research` schema and are built by Research data management. Ask them before building study extracts here.

## Heavy queries

- Please don't run full scans on `fact_claim_line` outside the reporting window. It's the biggest table in the warehouse and it makes the nightly load back up.
- The cost of a heavy query shows up in the warehouse console. If you're going to run something that touches more than a couple of billion rows, tell Tariq first so he can schedule it.
- The old {{DATA_WAREHOUSE}} box is still switched on for archive reads only. If you need something from before the migration, it's on that box and the connection is read-only from the warehouse. Don't load anything new into it.

## Notes

- The warehouse is NOT the system of record for any source system. EHR, the claims adjudication system, the HR system, all of them are authoritative.
- If a load fails for three nights in a row, the data team gets paged. If you see gaps in a table and no one has mentioned it, check the load log before assuming the data is right.
- Cork staff can see the warehouse through the VPN, but the practice management system data is not in the warehouse yet.
