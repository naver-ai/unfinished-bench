# The HR system

Owner: People operations. Last edited by Ebony Muller.

## What lives in the HR system

The HR system is the source of truth for:

- **Person records** — name, contact details, start date, contract type, probation end date, location (Lisbon or Portland), office, cost centre, department.
- **Job data** — job title, band, manager, direct reports, and any secondary reporting lines (e.g. a Portland engineer who matrix-reports into Developer productivity).
- **Leave** — all annual, sick, parental, and unpaid leave, plus the leave balances that flow into payroll.
- **Org chart** — derived from the manager field on each person record. If the org chart looks wrong, the underlying manager field is what needs fixing.

The system also holds the historical record of job changes, transfers, and compensation changes. We do not keep a separate spreadsheet of "old job titles" — that lives in the audit trail here.

## Who updates what

- **People ops** updates job changes, compensation, transfers, leave of absence, and probation outcomes. This is done on the back of the change form (see below) or the joiners/movers/leavers process.
- **Managers** update their team's leave requests through the employee self-service view. They also approve leave, so the balance stays in sync.
- **Employees** update their own contact details, emergency contacts, and bank details (bank details go through the HR system and flow into payroll).
- **IT** reads the system for onboarding and offboarding triggers (account creation, laptop assignment, access removal), but they do not write to it.
- **Payroll** reads the system for the monthly payroll run. If a change is needed to a person's records, it goes through People ops, not through Accounting & payroll directly.

## Requesting a change

If a manager needs a change to their team (new hire, transfer, title change, comp change, leave adjustment), they open a request in the change and request tracker. The request must come from the manager on the person record, or from a People Partner. People ops pick up the request and apply the change in the HR system within two working days.

For off-cycle comp changes, attach the approved comp memo to the request. For transfers between departments, the receiving manager's request is what we follow, but we confirm with the losing manager before moving the person in the system.

## Reports for managers

People ops runs these on request, usually monthly or when a manager asks:

- **Headcount by team** — active headcount, open requisitions are not tracked here.
- **Leave balances** — current accrual and used-to-date for a team, broken out by leave type.
- **Team movement** — joiners, movers and leavers for a team over a chosen window.

Managers can also pull these themselves through the dashboard, but it is fine to ask us — we have a couple of saved report templates that cover the common variants.

## Loose ends

- The org chart export to the intranet has been flaky since the directory service moved. Export still works manually; the scheduled sync is what is broken.
- Some old records from before the current band structure have legacy job titles that do not map cleanly to the current band structure. We are leaving those as-is until the employee's next job change.
- The "location" field is not always kept in sync for people who work hybrid between the two offices. We are treating home address as the default location unless the manager tells us otherwise.
