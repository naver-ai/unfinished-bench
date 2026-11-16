# Build farm overview

**Owner:** Build infrastructure  
**Last edited by:** Aleksander Novak

## Purpose

The build farm is the pool of hosts that run our internal BuildKit builders and host the registry image volumes. Both our own `gnt` development builds and the hosted platform's CI workloads land here. This doc covers the pieces the Build infrastructure team owns end to end.

## BuildKit builders

We run BuildKit in rootless mode on the big build hosts. The builder instances are provisioned through the same config that drives the hosted runners, so changes to builder settings go through the normal review process first. Marisol maintains the buildkitd config and the startup scripts.

Each build host runs two builders: one for internal workloads (the `gnt build`/`gnt test` jobs from our own repos) and one for hosted platform CI. The hosted builders are grouped into pools; see `infra-docs/ci/runner-pools.md` for the pool layout.

## Registry

`registry.gantline.dev` is the internal registry. The hosted platform clusters pull images from it, and our own release builds push to it. The registry itself runs on the build farm hosts; the image volumes live on the same hosts and are managed with cachectl.

Base images (the ones used by `gnt`'s build templates and by the hosted platform's default images) are maintained by Build infrastructure. Adrian owns the image build definitions. The images are rebuilt on a fixed cadence and on demand when a dependency needs a bump. The image cache on the build hosts is documented in `infra-docs/build-farm/image-cache.md`.

## Build logs

Build logs for internal builds go to the same log store as the hosted platform's CI logs and are kept for 90 days, like pipeline logs.

## Queue alerts

We page on two conditions:

- Build queue depth above the threshold for more than a few minutes (checked on a rolling window).
- Registry pull latency above the threshold, measured from the hosted platform clusters.

Both alerts route through the paging tool to the on-call rotation for Build infrastructure. The dashboards for queue depth and pull latency are linked from the metrics dashboards page under the build farm section.

## Loose ends

- The old `buildctl` wrapper script is still referenced in a couple of internal runbooks; it has been replaced by `gnt` commands and will be removed once the runbooks are updated.
- Ethan used to maintain the builder host images before moving to the lab team; Adrian took over the image definitions and the rebuild schedule.
- The link to the builder config examples in the `eng-docs` repo has moved; the current location is the `buildkit-config` repo, under `examples/`.
