# Answering auditor requests

Owner: Governance, risk & controls testing. Last edited by Nadia Petrov.

Evidence requests arrive through the `tickets` queue or direct from the requester's mailbox. Sources are SOC 2, PCI, Supervisory Authority inspections, and internal audit. All requests go into the evidence tracker (the GRC tab in `tickets`) — if someone pings you in `#general`, still log it there.

1. Open the ticket and check the tracker for the request ID. If there is no request ID, create one with the prefix `EVID-` and the ticket number.
2. Identify the owner: the GRC team (Nadia, Imani, Ben) answers controls evidence. If the request touches another team's system — the treasury workstation, the core ledger, the SIEM, the edge — reassign the ticket to that team's lead with a note that GRC is tracking.
3. Pull the evidence. For system-generated evidence, prefer exports from the system itself (e.g. the access review export from `access-reviews.md`, a saved SIEM query export) over screenshots. Name the file `EVID-<ID>-<description>-<YYYYMM>` where `<description>` is short, e.g. `EVID-1234-access-review-Q3.pdf`. Save it in the evidence tracker's drive folder under the request ID.
4. Upload the file to the request in `tickets`, add a one-line note on what it shows and which control it maps to (control numbering is in `control-testing.md`), and mark the request as "Evidence provided". Do not mark it "Closed" — the requester closes it.
5. Response target is three working days from receipt. If the request comes from a Supervisory Authority inspection team, target is two working days and Isaac is copied on the reply.
6. If the evidence is not yet available (e.g. a report run that happens monthly), reply with the date the report will be available and set the ticket reminder for that date.

**If it goes wrong**: if the evidence cannot be produced at all, escalate to Isaac Chowdhury before replying. If the file is too large for `tickets`, upload to the evidence tracker drive and paste the link instead. If the requester disagrees with what you provided, loop in Imani or Ben and do not send a second version until they have looked at it. If the request looks like it covers something outside our normal evidence set (e.g. a request for a specific merchant's data), pause and ask Isaac — do not assume it is a normal evidence pull.
