# Shift handover

**Owner:** Reutlingen plant · **Last edited by:** Mikael Jaramillo (Manufacturing Engineer)

Applies to the assembly lines in Reutlingen (MC series final assembly, DU series build and TX subassembly). The handover board in the MES is the single source for shift-to-shift status — the stand-up at the line is a summary, not a replacement.

## Before the outgoing shift lead leaves

- [ ] Update the handover board in the MES for every line that ran: output against plan (units, not hours), current WIP, and which stations are ahead or behind.
- [ ] Record stoppages of 15 minutes or more on the line log: reason code, duration, and the CMMS work order number if a machine or fixture was involved.
- [ ] Open quality issues on the line: NCR numbers, affected serial numbers or batches, and whether the line is blocked or running with a containment in place. Do not close an NCR from the handover board — that stays with the quality team.
- [ ] Note any safety observations or near misses on the line in the EHS reporting tool, and flag them on the board so the incoming shift sees them first.
- [ ] If a station is running with a temporary workaround (e.g. a substitute tool or a manual step while a fixture is in repair), say so explicitly — do not leave it to the incoming lead to spot.
- [ ] Check that the MES shows no open "line stopped" state on any line you are handing over. If a line is stopped, the reason must be on the board.

## At the stand-up

Keep it short — 10 to 15 minutes at the line, standing. The incoming shift lead runs it.

1. Outgoing lead walks the board: output vs plan, where the line stands, what is blocked.
2. Incoming lead confirms they have the context for any open NCRs and stoppages — if not, ask now, not later.
3. One point each from the outgoing team on anything the incoming team needs to know (tooling, material shortages, a customer-requested build order).
4. If a line is stopped, agree on the next check-in before the incoming lead walks away.

## During the shift

- The incoming shift lead owns the board from the moment the stand-up ends. Update it as the line moves — do not batch updates for the end of the shift.
- If a stoppage or quality issue changes the plan for the day, update the board within the hour, not at handover.
- If a line cannot be covered (e.g. a callout), the shift lead escalates to Salma Rahman before the end of the shift — do not leave it for the handover.

## Reminders

- The board is in the MES, not on paper. Paper notes from the stand-up are fine but must be transferred to the MES before the outgoing lead leaves.
- Handover is between shift leads; the board is the record. If the incoming lead disagrees with something on the board, resolve it at the stand-up and correct the board together.
- Maintenance requests go through the CMMS — a note on the handover board is not a work order.
