# Versioning and changelogs

Owner: Release engineering & CI. Last edited by Isaac Lopez.

## gnt and SDKs

- Semver for `gnt` and all SDK packages. `MAJOR.MINOR.PATCH`:
  - MAJOR: breaking CLI or API surface changes, removal of a command or flag, change to default behavior that affects output
  - MINOR: new commands, flags, or compatible features; deprecations land here and stay for at least two MINORs
  - PATCH: bug fixes, internal refactors, doc-only changes
- Pre-1.0: MAJOR is 0, MINOR can include breaking changes with a note in the changelog. Only the Python SDK is still pre-1.0; `gnt` and the TypeScript SDK are on 1.x.
- Since we ship from the release train, version bumps happen on the train branch. The train bump is MINOR by default; PATCH for hotfixes.
- The `gnt` version and the `gnt` CLI's reported version must match the tag. `gnt --version` output includes the short commit hash on dev builds.

## API

- The public API is dated: `YYYYMMDD.1`, incrementing the last segment per breaking change on the same day.
- Non-breaking API additions bump the minor segment of the current dated version.
- The API version appears in the `Gantline-Version` response header and in the docs sidebar.
- Deprecated API fields stay for at least 90 days from the deprecation notice.

## Changelogs

- Every package keeps a changelog file in the repo root, generated from pull request labels by the release tooling.
- Labels: `change:major`, `change:minor`, `change:patch`, `change:skip`. Missing labels default to `change:patch`.
- Changelog entries are written by the owning team in the PR description, not by release engineering. We only move them between sections.
- Format per entry: `- {type}: {summary} ({PR #})`. Types: `Added`, `Changed`, `Deprecated`, `Fixed`, `Removed`, `Security`.
- The "Unreleased" section accumulates entries; the release build cuts it into the version heading.

## Release notes

- Release notes are collected weekly from the daily trains, drafted by the owning team for their area, then edited by devrel before publishing. Devrel owns tone and length; we own accuracy.
- Notes go on the docs site under `/releases/`, one page per week. The blog gets a shorter post only when there's a headline feature.
- Hotfixes get a short note appended to the current train page, not a separate post.

## Tooling notes

- The old `changelog-gen` script in the release repo is still around but the train pipeline uses the labels path. Don't run it by hand.
- Changelog label questions go to #releases; Kofi set up the label rules if something looks off.
- The release notes template lives in the docs site repo; the publishing flow points to it.
