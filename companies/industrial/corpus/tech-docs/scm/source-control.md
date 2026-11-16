# Source control

**Owner:** Developer platform & build tooling  
**Last edited by:** Imani Medina

## Host and layout

All source lives on the company Git host, with `git.kessendorf.com` as the upstream. The host is managed by Developer platform; access is via the existing SSO. Build agents and plant CI fetch from the internal Git mirror rather than from the upstream; the mirror and mirrorctl are covered in `tech-docs/scm/git-mirror.md`.

The firmware monorepo (`firmware/`) was adopted per ADR 0009 and is the only repo new firmware work is created in. The older per-product repositories (`controller-fw`, `du-drive`, `tx-fw`) are read-only for most staff; only the firmware team has push rights, and only for hotfixes on released branches that have not yet been migrated. No new long-lived branches should be created in those repos.

Non-firmware code (build tooling, lab scripts) lives in separate repositories under `platform/` and `tools/`. Those are not part of the monorepo.

## Branch naming

- `main` is the integration branch for the monorepo and for all platform/tools repos.
- Release branches: `release/<product>/<major>.<minor>` (for example `release/mc3/2.4`).
- Feature branches: `<initials>/<short-description>`, e.g. `im/tx-fw-calib-offset`.
- Hotfix branches: `hotfix/<product>/<ticket-ref>`.

The ticket reference in a hotfix branch name should match the ticket ID in the commit message. We have not enforced this in CI, but reviewers are asked to flag mismatches.

## Merge requests and review

All changes to `main` and to release branches go through a merge request. Direct pushes to `main` are blocked on the host; the block is enforced server-side, not just by client hooks.

- A merge request needs at least one approval from someone other than the author. For firmware changes that touch motion-control paths (anything under `firmware/control/`), one of the approvals must come from the control firmware team.
- The author is responsible for picking reviewers; if the author is unsure, they should ask in #firmware or #build-tooling.
- Builds must pass before merge. The merge pipeline runs the same build and signing steps described in `tech-docs/firmware/build-and-signing.md`.
- A merge request that is approved but not merged within a few working days will be mentioned in the team channel; stale branches should be closed out rather than left hanging.

## Deploy keys for build agents

Build agents that need to fetch from the host use deploy keys, not personal accounts. Keys are issued per agent and stored in the host's deploy-key settings. The team keeps a list of which agents have keys in the internal wiki (not in this repo).

- Keys are scoped to a single repository and to read-only access, except for the release agent, which has write access to `main` only for the firmware monorepo. That exception is deliberate and was agreed when the release pipeline was set up.
- If an agent is decommissioned, its key must be removed by the person who decommissions it. If the key is lost or suspected of being exposed, remove it immediately and issue a replacement.

## Loose ends

- The remaining per-product repos are still referenced by some build scripts outside the monorepo. Ethan Lee is tracking those references and the plan is to retire the repos once the last reference is migrated. No date has been set.
- We have not yet enabled signed commits for all repos; currently only the firmware monorepo requires them. The rest of the platform repos are expected to follow in the next quarter.
- The deploy-key inventory in the wiki is only updated manually; if you notice an agent that no longer exists, flag it in #build-tooling.
