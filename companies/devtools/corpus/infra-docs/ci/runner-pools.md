# Internal runner pools

Owner: Release engineering & CI. Last edited by Isaac Lopez.

This covers the runner pools used by Gantline's own pipelines (gnt builds, service CI, release builds, editor and mobile builds). For customer-facing runner docs, see the Cloud product docs.

## Pool layout

- `{{DESKTOP_OS_3|lower}}-large`: default for most service builds. Autoscales between 10 and 40 instances.
- `{{DESKTOP_OS_3|lower}}-small`: used for lint, formatting, and quick checks. Autoscales between 5 and 20.
- `arm64`: for cross-architecture gnt builds and tests. Autoscales between 2 and 8.
- `{{DESKTOP_OS_1|lower}}-editor`: {{DESKTOP_OS_1}} runners for the desktop editor. Fixed pool of 6, no autoscaling.
- `{{DESKTOP_OS_1|lower}}-{{MOBILE_OS_1|lower}}`: {{MOBILE_OS_1}} builds and signing. Fixed pool of 4, no autoscaling.

All {{DESKTOP_OS_3}} pools run on microVMs (see ADR 0009). {{DESKTOP_OS_1}} pools are physical hosts in Portland.

## Autoscaling

Autoscaling is driven by queue depth in the CI system. Scale-up is immediate; scale-down has a 15-minute cooldown after the queue drains. If a pool is consistently saturated, bump the max and file a ticket to review the fleet cost.

## Runner images

Base images:

- {{DESKTOP_OS_3}}: `gnt-{{LINUX_DISTRO_1|lower}}-2404` and `gnt-{{LINUX_DISTRO_1|lower}}-2204`
- arm64: `gnt-{{LINUX_DISTRO_1|lower}}-2404-arm64`
- {{DESKTOP_OS_1}}: `gnt-{{DESKTOP_OS_1|lower}}-14` (editor) and `gnt-{{DESKTOP_OS_1|lower}}-15` ({{MOBILE_OS_1}})

Images are rebuilt on a weekly cadence by a scheduled pipeline in the `runner-images` repo. If a dependency needs a newer runtime before the weekly rebuild, open a ticket on the build farm board and mention it in #buildfarm.

Rebuilt images are pushed to the internal registry and then rolled out to pools in stages: `{{DESKTOP_OS_3|lower}}-small` first, then `{{DESKTOP_OS_3|lower}}-large`, then `arm64`. {{DESKTOP_OS_1}} images are installed directly on the physical hosts by a script in the same repo.

## Reporting a broken runner

If a runner is misbehaving (failing setup, hanging jobs, bad image):

1. Check the pool health dashboard first — it may be a known issue.
2. File a ticket with the pool name, job ID, and what you saw. Tag it `buildfarm`.
3. Ping #buildfarm with the ticket link. For urgent issues, page the build farm on-call via the paging tool.

Do not manually drain or remove runners from a pool unless you are on the build farm on-call rotation. The autoscaler will replace unhealthy instances on its own within a few minutes.

## Notes

- If a pool is idle for more than a week, the cost dashboards will show it. Review before renewing capacity.
- Old references to the `ci-runner` service in runbooks refer to the current runner agent. Update any copy you spot.
