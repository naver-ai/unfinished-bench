# CI pipelines

Owner: Release engineering & CI · Last edited by Kofi Osei

All CI workloads run on Gantline hosted runners. Pipeline definitions live in the repo under `.gnt/pipelines/` and are written as YAML. The `gnt` CLI resolves and runs them; there is no separate CI server to configure.

## Pipeline structure

A pipeline has three stages. Every stage must pass before the pipeline is green.

1. **build** — compiles the service, runs `gnt build` with the lockfile and runtime pinned in `buildcfg`. The build stage uploads its artifacts to the artifact store (`artifactctl` lists and manages them).
2. **test** — runs unit tests, integration tests, and the code search index check. Test shards are split across runners; the shard count is set in the pipeline file.
3. **package** — assembles the deployable image, pushes it to the registry, and records the image digest in the artifact store.

Stages run in order. A failure in any stage stops the pipeline; later stages are not started.

## Caching

- Dependencies are cached per repo and per lockfile hash. The cache key is printed at the top of the build stage log.
- If a cache entry is stale (for example after a lockfile change), delete it from the pipeline's cache tab in the web UI and re-run. Do not edit the cache directly on the build hosts.
- The build farm's image cache is shared across pipelines; see `infra-docs/build-farm/image-cache.md` if a build step pulls slowly.

## Checks on main

Pipelines on the main branch run an extra set of checks after the package stage:

- **Vulnerability scan** — the scanner runs against the packaged image. Failures are reported in the pipeline log and via the metrics dashboards.
- **Release readiness** — verifies the version in `versioning.md` matches the changelog and that the changelog has an entry for the current release train. See `eng-docs/release/versioning.md`.
- **API compatibility** — for services that publish to the public API, this checks that the OpenAPI document is unchanged or the change is marked as breaking in the changelog.

These checks do not block merges; they block the release train. A red check on main is a release blocker and should be triaged the same day.

## Debugging a red pipeline

1. Open the pipeline from the commit status or the CI tab. The failing stage is highlighted; click it to see the log.
2. The log is streamed from the runner. If the log is truncated, use **Download full log** in the stage's action menu.
3. Re-run the failed stage from the stage's action menu. A re-run uses the same commit and cache. If the stage passes on re-run, note it in the pipeline's comment thread.
4. If the failure is intermittent, check the runner pool status in `infra-docs/ci/runner-pools.md` and the build farm overview. Runner health is also visible in `#buildfarm`.
5. For test failures, copy the failing test's output into the PR thread. Do not re-run the whole pipeline repeatedly to "shake out" a flake; file a ticket for the flaky test instead.

## If it goes wrong

- A pipeline that is stuck in "queued" for more than a few minutes usually means the runner pool is saturated. Check `#buildfarm` before paging.
- A build failure that is not reproducible locally is often a cache problem. Clear the cache and re-run.
- If the artifact store rejects an upload, the store may be in maintenance. Check the status page and `#releases`.
- Do not edit pipeline logs or artifacts after the fact. If a pipeline result is wrong, re-run it and keep the original log.

Pipeline logs are kept for 90 days in the artifact store. After that they are expired automatically; export what you need before then.
