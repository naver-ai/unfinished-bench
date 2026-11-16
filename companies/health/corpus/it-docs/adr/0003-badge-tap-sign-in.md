# ADR 0003: Badge tap sign-in on clinical workstations

**Status:** Accepted  
**Owner:** Clinical applications (HIS)  
**Last edited by:** Fiona Moreau  

## Context

Clinical workstations across the three hospital campuses and the clinics currently require a username and password for every sign-in. This creates friction during shift changes, especially in high-traffic areas like the ED at South Bend and the nursing units at Kalamazoo. Staff have raised concerns about shared credentials being written down and left near workstations. The badge reader hardware is already present on most workstations — it was deployed for the medication dispensing cabinets and the secure supply rooms.

We need a sign-in method that uses the existing badge hardware, works with the EHR and the other clinical applications, and does not compromise the audit trail requirements from the compliance team.

## Options considered

1. **Full single sign-on with badge tap** — Staff tap their badge and the workstation unlocks and launches the EHR with their active session. This is what the vendor recommends.
2. **Badge tap to unlock, then manual password** — Tap the badge, then still type the password. Low value, staff would not use it.
3. **Keep username and password, add a fast-user-switching shortcut** — No new hardware dependency, but does not address the shared credential problem.

## Decision

Go with option 1: badge tap sign-in on all clinical workstations and on the clinic check-in desks. The workstation unlocks and opens the EHR to the user's default landing page. The patient portal and the provider portal are also available from the session launcher, but the EHR is the default.

The interface engine team confirmed the badge reader events can be written to the same audit feed we already use for the medication dispensing cabinets. Each sign-in event carries the workstation ID, the badge ID, and the timestamp.

Rollout is being handled by Clinical applications (HIS) working with the service desk. The badge reader drivers are already on the standard clinical workstation image, so no new workstation builds are needed.

## Consequences

- Staff must not share badges. The badge is the same one used for door access and the cafeteria, so sharing it has always been a policy violation — this makes that more visible.
- The credentialing system team will need a feed of badge IDs for temporary staff and locums. That is being set up through the usual access request process.
- The patient app team asked whether the same badge tap could work on the patient-facing check-in tablets. That is out of scope for this work — those tablets use the patient portal with a PIN.

## Rollout notes by campus

- **South Bend:** Start with the ED and the inpatient nursing units on the fourth and fifth floors. The clinic building next door will follow once the hospital floors are stable.
- **Valparaiso:** The hospital floors and the health plan offices on the same campus. The health plan offices are not clinical workstations, but the badge tap is being enabled there too so the sign-in experience is consistent.
- **Kalamazoo:** The hospital and the research institute. The institute's workstations are not part of this rollout — they use a different sign-in path for the EDC and the CTMS.
- **Cork:** The medical centre only. The research trials office in Cork is not included for the same reason as Kalamazoo.

## Loose ends

- The service desk is still deciding how to handle a lost badge that is also used for workstation sign-in. Right now the badge can be deactivated from the access control system, but the workstation sign-in feed is not tied to that deactivation. The security team is looking at it.
- The old sign-in screen from the previous vendor is still shown briefly on some workstations before the new one appears. It is cosmetic and does not affect the badge tap, but it looks untidy.
- A few of the clinic check-in desks in the South Bend area do not have the badge readers mounted yet. The service desk has a list and is scheduling the mounting visits.
