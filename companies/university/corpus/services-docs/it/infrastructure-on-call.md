# Infrastructure on-call

**Owner:** IT Infrastructure & Operations  
**Last edited by:** Lucia Kowalski, Systems Administrator

## Purpose

This page covers the on-call rota for IT Infrastructure & Operations, how paging works, and what to do when you get paged. It is not a full runbook for every service — for deep troubleshooting, see the relevant service notes in the IT change tracker and the backups page.

## Rota

- The rota lives in the IT service desk portal under **On-call > Rota**. One person is on call at a time, covering evenings and non-working days.
- The rota runs from the first working day of each month to the last working day of the month. Swaps are allowed if both people update the rota and the IT service desk portal is notified.
- If you are on call, you carry the on-call phone. It is a separate handset, not a personal device.
- If you cannot pick up the phone within 15 minutes, the paging system escalates to the next person on the rota. That person then owns the incident until the original on-call confirms they are available.

## Paging

- Pages come through the IT service desk portal and the on-call phone. You get a page for:
  - a **Priority 1** incident (service down or major impact)
  - a **Priority 2** incident that has not had an update for 2 hours
  - automated alerts from the network, virtual server, backup or identity monitoring
- Most automated alerts are noise. Check the dashboard before calling anyone.

## When you are paged

1. **Acknowledge the page** in the IT service desk portal. Open the ticket, set yourself as the assignee, and add a note saying you are responding.
2. **Check the dashboard** — the infrastructure status page on the IT service desk portal shows current alerts for the Hollins Hill core, City campus, Kuala Lumpur campus, and Kestrel Vale Academy links.
3. **Decide if it is real.** If a single alert is from one device and the dashboard shows no wider impact, note that in the ticket and close the alert. If more than one device or service is affected, treat it as an incident.
4. **If it is real, act.** The sections below cover the four most common areas.
5. **If you cannot fix it within 30 minutes**, page the service owner (see escalation below).
6. **Update the ticket** with what you found, what you tried, and what you changed. The next person on call needs to be able to pick this up.

## Network

- The core switches at Hollins Hill are `core-hh-01` and `core-hh-02`. City campus has `core-city-01`. Kuala Lumpur connects back via the university's VPN concentrator.
- **If a site link is down:** check the site-to-site VPN status first. If the VPN is down, try restarting the tunnel from the network management console. If that does not work, check the physical link status on the edge router for that site.
- **If a building segment is down:** check the switch status in the network management console. Look for a port that has gone into an error state. If a port is flapping, disable it and note the port number in the ticket. Estates may need to be involved if it is a physical cabling issue — raise a maintenance request via the estates helpdesk.
- **If the wireless network is down:** check the controller first. Wireless access points will drop off the controller if the wired link to them is down. Check a sample of access points in the affected area before assuming the controller is at fault.

## Identity

- The identity service is the main sign-in for staff and students. If it is down, people cannot get into most systems.
- **Check the service status page** on the IT service desk portal first. If the identity service is showing as down, check the server that hosts it.
- The identity service runs on two virtual servers, `idm-01` and `idm-02`. If one is down, the other should carry the load. Check both are reachable.
- If both are down, try restarting the service on `idm-01` first. If it comes up, check that `idm-02` synchronises before bringing it back into load.
- **If passwords are not working:** do not reset passwords unless you have verified the person is who they say they are. Refer them to the IT service desk during working hours. If the issue is widespread, check whether the identity service is in a degraded state rather than fully down.

## Virtual servers

- Virtual servers run on the hypervisor cluster at Hollins Hill. There is a second cluster at City campus for disaster recovery.
- **If a virtual server is down:** check the hypervisor console first. Is the server powered off, or is it showing as running but not responding?
- If it is powered off, try starting it. If it is running but not responding, try a graceful shutdown from the console, then start it again.
- **If the whole cluster is slow:** check the storage. The cluster uses a shared storage array. If the array is showing high latency, that will affect every virtual server on it. Do not restart virtual servers to fix this — it does not help and makes the load worse.
- **If a virtual server will not start:** check it is not trying to start on a host that is already at capacity. Move it to another host if needed.

## Backups

- Backup jobs run on a schedule from the backup server, `bkup-01`. The backup status page on the IT service desk portal shows the last run for each job.
- **If a backup job fails:** check the error message first. Most failures are because the source virtual server was offline at the scheduled time, or the backup target ran out of space.
- If the source was offline, re-run the job manually from the backup console. Do not wait for the next scheduled run — the backup may be needed sooner.
- If the target is out of space, check what is taking up space — large backups for retired servers are the usual culprit — and note what you found in the ticket.
- **If a restore is needed:** do not attempt it without confirming with the requester that the server name, date and path are correct. A restore to the wrong location can overwrite data.

## Escalation

- If you cannot resolve an incident within 30 minutes, or if you are not comfortable with the area, page the service owner:
  - **Network:** Mateo Bianchi
  - **Identity:** Reza Harper
  - **Virtual servers:** Lucia Kowalski
  - **Backups:** Victor Palmer
- If the service owner does not respond within 15 minutes, page Victor Palmer directly.
- If the incident is affecting teaching or exams, also notify the relevant team via chat. Exams officers are in #exams-officers, and the Registry team is in #registry.

## Handover notes

- Always leave a note in the ticket when you finish your shift. Include:
  - what the issue was
  - what you did
  - whether it is resolved or still open
  - anything the next person should check or try
- If you made a change that affects a service, add a change note in the IT change tracker as well. A ticket note is not enough.
- If the incident is still open at the end of your shift, do not close it. The next person on call picks it up from the ticket.

## If it goes wrong

- If you restart a service and it does not come back, say so in the ticket immediately. Do not keep trying the same thing.
- If you think you have made something worse, page the service owner straight away. It is better to get help early than to spend an hour making things worse.
- If a server is down and you are not sure which team owns it, check the IT service desk portal for the asset record. It lists the service owner.
- If the issue is at the Kuala Lumpur campus, remember the time difference. The site link is monitored from the UK, and Hafiz Rahim (IT Manager, Malaysia Campus) can arrange physical checks if needed.

## Contact

- On-call rota: IT service desk portal, **On-call > Rota**
- Infrastructure status: IT service desk portal, **Infrastructure > Status**
- Backups: see `services-docs/it/backups.md` for the backup schedule and retention periods
- The on-call phone is kept in the IT Infrastructure office on the ground floor of the Hollins Hill campus, in the cabinet by the door.
