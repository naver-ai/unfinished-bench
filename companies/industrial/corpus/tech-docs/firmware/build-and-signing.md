# Firmware builds and signing

**Owner:** Release engineering  
**Last edited by:** Mia Brennan (Release Coordinator)  
**Applies to:** MC series, DU series, TX series embedded firmware and the encoder firmware line

---

## Build pipeline

1. Firmware lives in the monorepo (`tech-docs/adr/0009-firmware-monorepo.md`). Each merge to `main` triggers a CI build on the build agents in Reutlingen.
2. CI runs the static checks from `tech-docs/firmware/coding-standard.md`, then compiles per-target. Targets are named by product family and hardware revision, e.g. `mc3-rev-b`, `du2-rev-a`, `tx1-rev-c`.
3. Builds that pass are published to the artefact store under `firmware/<family>/<version>/`. Artefacts are kept for the supported lifetime of the release.
4. Each artefact gets a SHA-256 checksum and a manifest listing the source commit, toolchain version and build agent. The manifest is written into the artefact store alongside the image.

## Signing

5. Only Release engineering can trigger a signed build. Signing happens on the signing service, which holds the production key. The key never leaves that service.
6. To sign a build, open a ticket in `tickets` with the artefact path and the target release number. The Release Coordinator (currently Mia Brennan) reviews the manifest, confirms the source commit is tagged, and queues the signing job.
7. The signing service applies the production signature and writes the signed image back to the artefact store as `<image>.signed`. The unsigned image is kept in the same folder for reference.
8. Firmware update packages for the field (`.kup` files) are assembled from signed images. They are not considered releasable until the signature check passes in the update tool.
9. Images for the test lab benches go through the same signing step.

## Build numbers and version strings

10. Version strings are `<major>.<minor>.<patch>-<build>`. The build number is taken from the CI pipeline counter, not from the source commit hash.
11. A release candidate is `<version>-rc<N>`. RC builds are signed with the same key and are field-installable; if an RC goes out to a customer, it must be tracked in the artefact store like a normal release.
12. Hotfixes bump the patch number and get a new build number. Do not reuse a build number even if the source is identical.

## Rebuilding an older release

13. To rebuild an older release, find the release tag in the monorepo (tags are named `rel-<family>-<version>`). Check out the tag, then run the CI pipeline manually with the `release` parameter set to the tag name.
14. CI will rebuild from the tag and produce a new artefact with a new build number. The version string stays the same, but the build number differs from the original. Note this in the artefact manifest.
15. Old toolchain versions are pinned in the monorepo, so a rebuild from a tag from several cycles back should still compile. If the pinned toolchain is no longer available on the build agents, contact Platform (Quentin Ibarra's team) to have it restored.

## If it goes wrong

- **Build fails after a merge:** check the CI log for the failing target. If the failure is in the shared HAL, it usually affects all targets — fix at source, do not bypass the target.
- **Signature mismatch on a `.kup`:** do not ship it. Re-run the signing job from the same artefact; if it still mismatches, the artefact is corrupt and must be rebuilt from the tag.
- **Signing service unreachable:** signed builds wait. Do not attempt to sign with a development key or a self-hosted key. Contact Release engineering and let the queue build up.
- **Wrong version in a manifest:** do not edit the manifest by hand. Re-run the build with the correct version parameter and use the new artefact.

For questions about the monorepo layout, see `tech-docs/adr/0009-firmware-monorepo.md`. For source control workflows, see `tech-docs/scm/source-control.md`.
