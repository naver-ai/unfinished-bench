# Telford drives line

**Owner:** Telford plant  
**Last edited by:** Hamza Graham (Production Supervisor)

## Scope

Covers the DU-series drives line: SMT, conformal coating, burn-in, end-of-line test. MC-series controllers are built on the same line in small batches — see the planning board for the current split.

## Line flow

1. **SMT** — two pick-and-place lines, one for DU power stages, one shared with controller boards. Solder paste inspection is inline on both. AOI after reflow catches most issues; the odd escapee shows up at end-of-line test.
2. **Conformal coating** — selective coating robot, two stations. The second station is normally the constraint if we're running mixed batches, because changeover between DU and MC board profiles takes about 20 minutes.
3. **Burn-in** — six racks, each holds 24 drives. Standard burn-in is 4 hours at 40°C with a resistive load profile. Racks 1–4 are the older ones with the manual load selectors; racks 5–6 have the newer automatic load profiling and are quieter. Rack 4 has a known intermittent temperature sensor on channel 7 — the reading drifts but it doesn't affect the cycle, just log it on the whiteboard if you see it.
4. **End-of-line test** — two test stations running the full electrical test (insulation, torque loop, encoder alignment, commutation check). Omar Eklund owns the test fixtures and the calibration schedule for the torque arms. The third station is currently used as a rework/test bay and is not in the normal flow.

## Bottlenecks

- **SMT changeover** — the shared line for controller boards means we batch DU boards to minimise switching. If the MC schedule slips, the drives line feels it. Talk to Planning if the two weeks look tight.
- **Burn-in rack capacity** — Racks 1–4 fill up first because operators prefer them (the newer racks' load profiles need the settings confirmed in the MES before starting). If we're behind, the newer racks are fine — the MES flow is the same, just confirm the profile matches the work order.
- **End-of-line test** — normally fine, but encoder alignment on the larger DU-80 frames takes longer than the smaller frames and isn't always reflected in the standard time. Worth checking the queue if the mix shifts.

## Who to call

| Station | First contact |
|---|---|
| SMT | Hamza Graham |
| Conformal coating | Nasser Lund |
| Burn-in | Nasser Lund |
| End-of-line test | Omar Eklund |
| MES issues | IT service desk (incident to the factory-it queue) |
| Fixture calibration | Omar Eklund, or the test lab via the lab calendar |

## Notes

- Reworked boards go through the same burn-in cycle as new ones — no shortcuts. If burn-in is full, queue them with the supervisor, don't leave them by the test stations.
- The MES work order must be closed before the pallet leaves the line. If the MES terminal is down, note the serials on the paper traveller and close the work order when the terminal is back — the shift handover should flag this.
- The old test program list on the shared drive (the `telford-test` folder) is still current for the DU-40 and DU-60 frames; the DU-80 programs are on the test station PCs only. Newer program versions go through the firmware change process, see the firmware build notes.
