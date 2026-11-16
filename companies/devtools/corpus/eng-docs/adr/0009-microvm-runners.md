# ADR 0009: Hosted runners on microVMs

**Status:** Accepted  
**Owner:** Hosted runners  
**Last edited by:** Grace Abara (Engineering Manager, Hosted runners)

## Context

Customer builds on Gantline Cloud run on our hosted runner fleet. Until now, each job ran as a container directly on a shared host, with {{DESKTOP_OS_3}} namespaces and cgroups providing isolation between jobs. This has worked well for throughput, but we've seen an increasing number of issues that trace back to shared-kernel isolation:

- Customer jobs that load kernel modules or run privileged operations inside their container can affect the host kernel in ways we can't fully predict.
- Side-channel noise between co-located jobs has caused intermittent, hard-to-reproduce failures that customers report as flaky builds.
- Some customers run workloads (custom toolchains, emulators, package managers with odd assumptions) that probe or depend on host-level state that leaks through the container boundary.

We also have a growing number of requests for jobs that need to run with more control over the environment — custom kernels, specific sysctls, or just a cleaner "machine-like" boundary than a container provides.

## Options considered

1. **Stay on containers, add stricter seccomp profiles and resource limits.** Rejected: this would break a meaningful number of existing customer builds that rely on syscalls we'd have to block, and it wouldn't address the kernel-module or host-state leakage concerns.
2. **Use a separate VM per customer org, with containers inside.** Rejected: too coarse-grained. Orgs with high concurrency would still share a kernel, and the cost of spinning up a VM per org on demand is too high for short jobs.
3. **Use a microVM per job.** Accepted. We already run microVMs for cloud workspaces (the editor backend uses the same runtime), so the infrastructure team has operational experience with the hypervisor and the image pipeline.

## Decision

Each hosted runner job gets its own microVM, booted from a base image that includes the runner agent, common build toolchains, and the gnt CLI. The microVM is provisioned on demand, the job runs inside it, and the microVM is torn down when the job finishes. No customer job shares a kernel with another customer job, and no customer job runs directly on the host kernel.

The runner fleet is sized so that cold-boot overhead (measured at roughly 2–4 seconds from job start to agent ready) is absorbed by the job scheduler: jobs that can tolerate a small delay are placed on hosts with available microVM capacity, and the queueing behaviour is the same as before for jobs that can't.

## Consequences

- **Boot time:** Jobs now pay a small fixed startup cost. For most builds this is negligible compared to dependency fetch and compile time. We've added a `runner.startup_time` metric to the hosted runner dashboards so we can track this per pool and per customer plan.
- **Caching:** The shared {{CONTAINER_TOOL}} layer cache that existed on the old container hosts is gone. We've replaced it with a per-org cache that lives on a network volume attached to the microVM at boot. Cache warm-up is handled by the runner agent before the build script runs. Early numbers show cache hit rates are comparable, but we're still tuning the eviction policy — see loose ends below.
- **Image updates:** Base images are rebuilt and published through the same pipeline as the cloud workspace images, so security patches and toolchain updates land on the same cadence. The image cache on the build farm is used for the microVM base images too — see `infra-docs/build-farm/image-cache.md` for how that's wired up.
- **Cost:** MicroVM overhead per job is higher than a container. The fleet is provisioned for the current CI load plus headroom for the workspace backend, and we're monitoring utilisation across both workloads.

## Loose ends

- Cache eviction: the per-org cache volume has a size cap, and we're still deciding whether eviction should be LRU or based on a recency/weight heuristic. Amir and Hamza are tracking this.
- {{DESKTOP_OS_2}} runners: the current microVM runtime is {{DESKTOP_OS_3}}-only. {{DESKTOP_OS_2}} hosted runners remain on containers for now; the plan is to revisit once the runtime supports {{DESKTOP_OS_2}} guests.
- Local testing: `gnt` has a `--runner=local` flag that runs the build script directly on the developer machine. The microVM behaviour is only exercised on the hosted fleet, so the local path can drift. We've added a CI job that runs a smoke build inside a microVM on every gnt release, but it's not the same as a full integration test.
- The old container-host runner pools are still running in parallel for the next few weeks while we drain them. No new jobs are scheduled there.
