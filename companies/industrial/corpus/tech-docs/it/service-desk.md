# Service desk

**Owner:** Service desk  
**Last edited by:** Ava Osei (IT Support Technician)

## Queues and ownership

The service desk runs three queues in the service desk portal. Tickets are routed by category at submission; the desk re-routes anything misclassified during triage. The queues are:

| Queue | What lands here | Owner |
|---|---|---|
| **End-user support** | Laptop, mobile, printing, software access, password resets, VPN, meeting-room kit | Service desk (Reutlingen, Telford, Greenville) |
| **Plant IT** | Line terminals, MES shop-floor PCs, barcode scanners, label printers, test-rig PCs, calibration bench PCs | Service desk triage; escalated to Plant IT on-call outside desk hours |
| **Infrastructure** | Server, storage, network, backup, messaging, monitoring issues | Service desk triage; handed to Platform & SRE or Infrastructure teams |

## Priorities

Priority is set at intake and revisited during the ticket's life. When in doubt, ask the caller what is blocked — a single operator waiting on a line terminal is not the same as a whole station down.

| Priority | Definition | Examples | First response target |
|---|---|---|---|
| **P1** | Production or test-lab work is stopped; no workaround | Line terminal down on the Telford drives line; MES unavailable at a Reutlingen assembly cell; calibration bench cannot record | 15 minutes, 24/7 |
| **P2** | Significant impact but a workaround exists, or a single workstation offline | One operator's laptop dead but they can move to a shared desk; label printer offline with a spare available | 2 working hours |
| **P3** | Minor impact or cosmetic | Fonts missing in a document; second monitor not detected; printer queue stuck | 1 working day |
| **P4** | Request or question, no impact | Access request, software install request, "how do I…" | 3 working days |

P1 and P2 tickets stay open until the caller confirms the issue is resolved. P3 and P4 may be closed by the desk if no response is received after two follow-ups — note that in the ticket.

## Plant IT on-call

Outside desk hours, P1 plant issues go to the Plant IT on-call rota. The rota covers the Telford drives line, the Reutlingen main plant and test lab, and the Greenville plant. Call the on-call number from the service desk portal; do not page via chat for plant P1s.

On-call engineers carry a laptop and a plant radio. They can remote into MES shop-floor PCs and line terminals. If a terminal needs a physical replacement, the on-call engineer pulls a spare from the plant IT cabinet and swaps it — spares are labelled by site and line segment. Log the swap in the MES asset record and note the serial change in the ticket.

## Hand-offs

Infrastructure and factory IT are separate teams. Hand-offs happen through the ticket; never leave a ticket sitting in "waiting" without an owner.

| Hand-off | Trigger | How |
|---|---|---|
| **To Platform & SRE** | Server, storage, network, backup, monitoring, {{ALERT_ROUTER|lower}} issues | Desk diagnoses to component level, then reassigns with a clear summary of what was tried. P1s: also ping #it-help. |
| **To Factory IT** | MES application behaviour, shop-floor PC images, line-terminal config, test-lab capture issues | Desk handles hardware faults first. If the fault is in the MES client or capture software, reassign to Factory IT with the terminal ID and the exact error text. |
| **Back to desk** | Infrastructure or Factory IT need the caller to test a fix | They reassign to the desk with "please verify" — the desk contacts the caller and closes only on confirmation. |

Escalation path within the desk: Bruno Bakker and Nico Dahl handle first-line; Ava Osei is the technical escalation for plant and test-lab issues; Chiara Navarro owns the queue and the rota. Jens Oberle is the point for cross-team priority disputes, but that should be rare — sort it in the ticket first.
