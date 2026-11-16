# ADR 0011: Retire nfs-a and move to pool-b

**Status:** Accepted  
**Owner:** Storage & file services  
**Last edited by:** Rahul Iyer (Storage Engineer)

## Context

`nfs-a` is the older of our two filers at Telford. It exports volumes for a long list of internal services: the orders service and its database, the ERP file store, CI caches, the wiki, reporting and analytics, department shares and home directories, and the backup vaults. The hardware is out of vendor support and has been running on extended maintenance; the vendor will not renew again, and the shelves come out one at a time as capacity allows.

`pool-b` has been in production for new shares for a while. It has redundancy on both controllers and sits under the normal backup policy, which nfs-a only partly did — several nfs-a volumes were only ever snapshotted locally.

## Options considered

1. **Extend support with a third-party maintainer.** Rejected: spare parts for the shelves are already hard to get, and it only moves the problem.
2. **One big copy and a single cutover.** Rejected: too many services with different owners and change windows, and one failed service would hold up all the others.
3. **Service by service, in waves.** Chosen.

## Decision

Move every service off nfs-a to pool-b in waves. Each wave groups a few services whose owners can cut over in the same window. For each service:

- Storage & file services copies the volumes to pool-b, then runs a delta copy just before the cutover.
- The service owner moves the clients to the pool-b paths under their own change ticket and checks the service afterwards.
- The nfs-a volumes stay in place for a short grace period after the cutover so the owner can compare or copy back; after that they count as reclaimable.

The wave plan and the cutover tickets are tracked in the storage queue in the ticket system. Each wave has an owner in Storage & file services.

## Consequences

- Some older scripts and mount points reference `nfs-a` by hostname. We keep a DNS alias for a transition period and remove it after the last wave.
- Services that write heavily (databases, CI caches) need a short freeze for the final delta; their owners pick the window.
- Department shares and home directories go last, with comms to staff through the intranet.
- Shelves are pulled one by one as the used capacity on the remaining shelves allows.

## Loose ends

- The calibration database has one export path pointing at nfs-a; the quality team will confirm the new path once their share has moved.
- Wave dates live in the tickets, not here — this page is the decision, not the plan.
- Progress updates go in #storage as each wave completes.
