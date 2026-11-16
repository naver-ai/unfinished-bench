# Maintenance requests

**Owner:** Reutlingen plant  
**Last edited by:** Mikael Jaramillo (Manufacturing Engineer)

This covers raising a work order in the CMMS, priorities, planned maintenance slots, spare parts from stores, and contractor access. Applies to the Reutlingen plant only; Telford and Greenville have their own arrangements.

## Raising a work order

1. Log in to the CMMS (intranet → Maintenance → CMMS, or direct link from the plant dashboard).
2. Select **New Work Order**.
3. Fill in:
   - **Asset** — search by asset tag or name. If the asset isn't listed, use the machine's parent asset and mention the exact location in the description.
   - **Reported by** — defaults to your name; change only if you raise it for someone else.
   - **Location** — building, bay, and machine number if known.
   - **Description** — what's wrong, what you were doing when it happened, and any error codes shown.
4. Set the **priority** (see below).
5. Add a photo if you have one — attach it to the work order, don't send it in chat.
6. Save. The work order gets a WO number starting with `25` (plant code for Reutlingen).

The maintenance team picks up work orders from the CMMS queue. If a machine is down and blocking production, also call the maintenance hotline (extension 4110) — don't rely on the work order alone.

## Priorities

| Priority | Meaning | Examples |
|---|---|---|
| P1 – Emergency | Machine down, production stopped, or safety risk | Drive fault on an active line, compressed air failure, guard damaged |
| P2 – Urgent | Fault that will stop production soon or already degrades output | Unusual vibration, coolant leak, recurring alarms |
| P3 – Normal | Fault that doesn't affect production now | Minor oil weep, worn handle, rattling panel |
| P4 – Planned | Known work, no fault | Lubrication, inspection, calibration pre-checks |

P1 work orders page the on-call maintenance engineer. Only raise P1 if the machine is actually down or there is a direct safety hazard. If in doubt, use P2 and call the hotline.

## Planned maintenance slots

Maintenance slots are booked in the CMMS calendar. Production planning (Marco Blanco's team) coordinates with the shift leads before slots are published.

- **Weekly slot:** second shift on the first working day of the week, machines in the assembly area.
- **Monthly slot:** the full shutdown window on the first working day after the monthly MRP run.
- **Quarterly deep maintenance:** one full day, booked per area, at least two working days in advance.

If you need a machine out of service for maintenance, request the slot via the CMMS calendar at least two working days ahead. For anything longer than a day, talk to production planning first — they may need to move orders.

## Spare parts in the stores

- Stores (Reutlingen warehouse, section C) stock common filters, belts, sensors and fuses for MC and DU series equipment.
- Check stock in the CMMS before raising a work order that needs parts. If the part isn't in stores, the maintenance planner creates a purchase request via the ERP.
- **Kitting:** for planned maintenance, you can request a parts kit when booking the slot. Pick up the kit from stores on the morning of the work.
- If you take a part from stores for a temporary fix, log it against the work order — otherwise the stock count drifts and the next person won't find it.

## Contractors working on site

Contractors (e.g. for crane inspection, HVAC, or specialist welding) need a maintenance work order too. The maintenance planner raises the WO and the contractor gets a visitor badge linked to the WO number.

- Contractors must sign in at the gate and be escorted to the work area by a Kessendorf employee (maintenance or the requesting engineer).
- Permits: hot work, confined space and work at height require a permit from the EHS team. The maintenance planner requests it when the WO is raised.
- The contractor's work must be recorded against the WO, including what was done and any parts fitted. Close the WO when the work is verified.

## If it goes wrong

- **Wrong asset or location:** contact the maintenance planner (via the CMMS, not chat) and they will reassign it. Don't edit the WO yourself unless you raised it.
- **Duplicate work orders:** leave the older one open with a note pointing to the newer WO number.
- **P1 that turns out not to be P1:** the maintenance lead re-prioritises it. No one gets in trouble for over-reporting a genuine stoppage.
- **Parts not available:** the WO stays open, priority stays, and the planner updates the expected date. Chasing the planner once per shift is fine; calling multiple times doesn't speed it up.
- **Contractor without a permit:** stop the work, tell the maintenance planner. The planner sorts it with EHS before work resumes.
