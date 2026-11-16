# ADR 0009: Move firmware to a monorepo

**Status:** Accepted  
**Owner:** Developer platform & build tooling  
**Last edited by:** Ethan Lee (Build Tooling Engineer)

## Context

Firmware for the MC controller series, DU drive units and the TX transducer range currently lives in three separate repositories, one per product family (`controller-fw`, `du-drive`, `tx-fw`). Each repo contains its own copy of the hardware abstraction layer, the fieldbus stack and the calibration routines. The duplication has led to at least two incidents where a fix applied to the MC branch of the HAL was not ported to the DU or TX variants, and the fieldbus stack has diverged enough that a unified debugger tool no longer works against all three.

The build agents in the test lab and the signing pipeline are configured per repository. Each repo has its own CI configuration, and the firmware team spends about half a day per week syncing changes across the three repos by hand. The PLM references firmware deliverables by product family, so the repository layout change needs to be reflected there as well.

## Options considered

1. **Keep separate repos, add a shared library package.** Rejected because the packaging overhead for the embedded toolchain is significant, and the team would still need to coordinate releases across repos.
2. **Monorepo with per-product directories and a shared `common/` tree.** Chosen. The existing codebase already has a common HAL that is copy-pasted, so moving it into a real shared directory is a low-risk refactor.
3. **Single repo, single build for all products.** Rejected because the TX transducers have a different toolchain (no RTOS) and forcing a unified build would complicate their CI.

## Decision

Create a monorepo `kessendorf-firmware` containing:

- `mc/` – motion controller firmware
- `du/` – drive unit firmware
- `tx/` – torque transducer firmware
- `common/` – shared HAL, fieldbus stack, calibration routines, linker scripts

The build pipeline will use a new top-level build script (`build.py`, replacing the old `mkdist.sh` wrapper) that dispatches to the per-product build systems. The signing step stays unchanged: the signing server still receives the same artifact format.

## Consequences

- All three product teams now commit to the same repo. Merge conflicts across product trees should be rare, but the `common/` tree will need a designated reviewer from each team.
- Build agents will need a one-time reconfiguration to check out the monorepo instead of the individual repos. Lab scripts reference the old repo paths; those references will be updated as part of the migration.
- Git history is preserved per product directory. The old repositories will be archived (read-only) after the first stable release from the monorepo.
- The MES references firmware version strings by product family; those version strings are unchanged.

## Loose ends

- The DU team wants to move their bootloader into `common/` as well; this is deferred until the first release cycle is complete.
- Ethan is coordinating with the test lab on the build agent migration window.
- The firmware coding standard document should be updated to reference the new directory layout.
- The `mirrorctl` configuration for the internal Git mirror needs a new entry for the monorepo.
