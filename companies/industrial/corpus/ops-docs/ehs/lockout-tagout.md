# Lockout / tagout

**Owner:** Health, safety & environment  
**Last edited by:** Malik Nakamura (HSE Advisor)

---

## Purpose

This covers isolation of energy sources before maintenance, cleaning or setup work on machines, test benches and rigs. It applies at all three sites — Reutlingen, Telford and Greenville — and to field service work on customer equipment where the customer's own procedure is not stricter.

## Personal locks and tags

1. Every person who works on a machine or test bench carries their own lock and tag. Locks are available from the HSE office or the site store; tags are pre-printed with your name and employee number.
2. Your lock goes on **every** isolation point that affects the work. One person, one lock, one key. The key stays with you until you remove your own lock.
3. Tags must state: your name, the date, and a short description of the work. Fill them in before you start, not after.
4. If you lose your key, do not cut the lock. Contact HSE (Reutlingen: ext. 3411, Telford: ext. 5820, Greenville: ext. 7743) or your shift lead. The lock will be removed by a second person after the machine is verified safe and only after the shift lead confirms no one else is working under it.

## Isolation steps

1. Identify all energy sources for the machine or bench — electrical, pneumatic, hydraulic, gravitational, stored spring, residual heat. The machine documentation in the PLM lists the isolation points for each model; for test benches, the lab overview in `ops-docs/test-lab/lab-overview.md` covers the bench-specific points.
2. Shut down the machine using its normal stop sequence.
3. Open the main isolator(s) and, where fitted, the lockable circuit breaker. For TX series transducer rigs, also isolate the excitation supply at the bench panel — the MES screen will show "BENCH NOT READY" once the supply drops.
4. Lock each isolation point with your personal lock. Where several people work on the same machine, each person adds their own lock to a group hasp — see below.
5. Depressurise pneumatic and hydraulic systems. Bleed the line at the lowest point; check the pressure gauge reads zero and stays at zero.
6. For servo drives and DU-series direct drives, wait for the DC bus to discharge. The drive display shows the bus voltage; do not proceed until it reads below 50 V. The discharge time is on the drive label.
7. Release any suspended loads or counterbalance them. Lower vertical axes to the rest position where one exists.
8. Verify zero energy — try the start button and the emergency stop reset. The machine must not start. Where the machine has a residual voltage indicator, it must show zero.
9. Only then begin work.

## Group lockout

- One person acts as the lockout custodian for the job. That person places a group hasp on each isolation point and every member of the crew puts their personal lock on the hasp.
- The custodian keeps the only key to the hasp and records the lockout in the CMMS work order (field: "Isolation ref."). The work order number goes on the tag.
- To remove a group lockout: the custodian checks that all crew members have removed their personal locks, walks the machine once, and only then removes the hasp. If someone has left site without removing their lock, follow the lost-key procedure above.

## Shift handover

- If the machine stays locked out beyond the shift, the outgoing custodian and the incoming custodian hand over **lock and key** at the machine, not by message. Both sign the handover entry in the CMMS work order.
- The incoming custodian checks the isolation points themselves — do not trust the written word alone. See `ops-docs/plants/shift-handover.md` for the general handover rules.
- Tags stay on the isolation points for the duration of the work. They are removed only when the last person finishes.

## If it goes wrong

- If a machine starts while someone is working on it, stop the machine immediately, make the area safe, and report it as a near miss through the EHS reporting tool — see `ops-docs/ehs/incident-reporting.md`. Do not restart work until HSE has reviewed the isolation.
- If you find a lock or tag that has been tampered with, or an isolation point that was not locked but should have been, stop work, tell the shift lead, and raise an EHS report. Do not re-energise until the cause is understood.
- If the energy verification fails — the machine tries to start, or a gauge shows pressure after bleeding — isolate again from step 3 and contact the test lab (for benches) or maintenance (for production machines) before continuing.

Questions on this procedure go to the HSE team — Dalia Alvarez, Ilse Patel or Malik Nakamura — or to the site HSE rep on the shift.
