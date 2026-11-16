# Backups

**Owner:** IT Infrastructure & Operations  
**Last edited by:** Lucia Kowalski (Systems Administrator)

## What we cover

The backup service covers the core systems that hold institutional data:

- **Databases** — the student record system, the finance system, the HR and payroll system, the research grants system, the supporter CRM, the library system, and the VLE.
- **File stores** — the shared drives on Hollins Hill and City campus, the Student Services file store, the academy's school information system data, and the Malaysia campus property lease files.
- **Email** — the university mailboxes and shared mailboxes.
- **The room booking system** and the **timetabling system** configuration data.

## Retention

- Deleted files and overwritten database records are recoverable for **30 days** from the point of deletion or change.
- Email is held for **30 days** after deletion from the mailbox (including the deleted-items folder).
- Full database backups are kept for **60 days**; after that they are rotated out.
- The student record system has an additional nightly export that is kept for **90 days** to support statutory reporting.

## Restore tests

- We run a **quarterly restore test** on a rotating selection of systems. The exercise is logged in the IT change tracker and the results are noted in the infrastructure on-call handover.
- The current cycle covers the student record system, the finance system, and the VLE. The supporter CRM and the library system are scheduled for the next cycle.
- If a restore test fails, the system in question is re-tested within **5 working days** and any fix is tracked as a priority ticket in the service desk portal.

## How to ask for a restore

- Log a ticket in the IT service desk portal under **"Backup / Restore"**.
- Include the system, the file or database object, and the point in time you need restored (we can go back up to 30 days).
- For the student record system or the finance system, mark the ticket as **"priority"** — these are treated as business-critical.
- For files on the shared drives, you can also raise it through the estates helpdesk if that is how you normally log things, but the IT service desk portal is quicker.
- Restore requests are normally completed within **2 working days** for standard file restores and **5 working days** for database or mailbox restores.

## Loose ends

- The Kuala Lumpur campus shared drive is still backed up to the local server room; the replication to Hollins Hill is due to be completed but the timeline has slipped. The lease data is covered by the local backup for now.
- The old backup tool used for the student record system (the one that produced the `.bkf` files) is still referenced in a couple of the runbooks; the current tool is the one that is actually in use.
- The academy's school information system is backed up through the same service, but texts sent to families are not included — those are held by the messaging provider and can be requested separately through the Kestrel Vale office.
- For anything not listed here, or if you are unsure whether a system is covered, ask in #it-services and someone will point you at the right place.
