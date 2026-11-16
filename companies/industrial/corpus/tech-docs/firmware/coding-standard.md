# Firmware coding standard

**Owner:** Control firmware  
**Last edited by:** Kasia Kato (Firmware QA Lead)

Applies to all firmware in the `firmware/` monorepo: motion controllers (MC series), servo drives and direct-drive units (DU series), and test-rig firmware. The plant in Telford and the Greenville plant build to this standard; firmware is developed in Reutlingen.

## MISRA subset

- We follow MISRA C:2012 with the following deviations, recorded in the deviations list in the monorepo:
  - Directive 4.6 (typedefs for basic types): allowed for register maps and hardware access structs.
  - Rule 10.4 (usual arithmetic conversions): allowed in the motion kernel where the types are controlled by the same module.
  - Rule 11.4 (pointer to integer conversions): allowed only inside the HAL layer, with a comment referencing the datasheet.
  - Rule 13.5 (right-hand operand of `&&`/`||` must not contain persistent side effects): allowed for the watchdog kick inside the main loop.
- No other deviations without an approved waiver from the Firmware Tech Lead. Waivers are raised as tickets and referenced in the commit message with `Refs: #`.
- C++ modules (the DU-series commissioning tool) follow the same MISRA rules where they map to C++; the remaining rules are listed in the commissioning tool's own readme. New C++ code is only allowed in the commissioning tool — the motion kernel and all drivers remain C.

## Static analysis in CI

- Every merge request runs `cppcheck` with the `--misra=2012-5.7` profile, plus the project config in `tools/static-analysis/cppcheck.cfg`.
- Clang-tidy runs with the `.clang-tidy` file at the repo root. Warnings are errors on the main build; the `-firmware-tests` build allows a fixed list of warnings for test-only code, maintained by Firmware QA.
- The MISRA checker (a script wrapping `cppcheck`'s MISRA output) runs on the full tree and on the delta of the merge request. Both must pass.
- New findings on unchanged code must be raised as a ticket and linked in the merge request description. The ticket must be referenced in the commit message with `Refs: #`.
- The firmware build and analysis pipeline runs on the Reutlingen build agents. The Greenville and Telford sites do not run firmware CI; they consume signed builds from the Reutlingen pipeline.

## Review checklist

Every merge request must be reviewed by at least one person who is not the author. The reviewer checks:

- [ ] MISRA deviations have a waiver or are in the allowed list, with a comment in the code.
- [ ] No leftover to-do markers or commented-out code in the diff (a one-line reference to a ticket number is fine).
- [ ] Register access uses the HAL accessors, not raw pointer dereferences, unless the file is inside `hal/` and the access has a datasheet reference.
- [ ] Interrupt handlers are short and only set flags or enqueue; no blocking calls.
- [ ] The motion kernel files (`kernel/`) have no dynamic allocation and no recursion.
- [ ] New driver files follow the naming conventions below.
- [ ] Unit tests cover new behaviour on the host build; hardware-specific behaviour has a target test listed in the merge request.
- [ ] The change builds in the `-firmware-tests` configuration before the merge request is opened.
- [ ] If the change touches the build system or signing scripts, the Firmware Tech Lead (currently Zoe) is a reviewer.

## Unit tests

- Host tests run in CI on every merge request. They build with the `-firmware-tests` target and run on the build agent.
- Target tests run on hardware for all MC and DU firmware changes. The test matrix is:
  - MC204 and MC308 controllers on the Reutlingen test bench.
  - DU210 and DU450 drives, with the Telford drives line running the DU210 tests on every second working day.
  - Greenville runs the same target tests on their bench before releasing a Site Acceptance Test build; the results are entered in the lab calendar.
- Target tests are started from the bench PCs in the test lab. The bench logs the board serial, firmware hash and the test result.
- If a target test fails, the merge request is blocked until the failure is resolved or explicitly waived by Owen Price with a comment in the merge request.
- Test code is in `test/` next to the module it tests. Naming: `test_<module>_<behaviour>.c`.

## Naming conventions

- Drivers: `drv_<device>_<function>.c`, e.g. `drv_encoder_heidenhain.c`, `drv_tx_amplifier.c`. Headers are `drv_<device>.h`.
- HAL layer: `hal_<peripheral>.c`, e.g. `hal_spi.c`, `hal_timer.c`. These are the only files allowed to include vendor register maps directly.
- Motion kernel: files are in `kernel/` and are named by function, e.g. `trajectory_gen.c`, `pid_loop.c`, `commutation.c`. No `drv_`-style prefix — the kernel is not a driver.
- Functions in the kernel return `int32_t` status codes where 0 is success. Drivers return the same convention for init and config functions; interrupt handlers are `void`.
- Constants for hardware registers are `UPPER_SNAKE_CASE` and are defined in the HAL header for that peripheral, not in the driver.
- Static functions are `static` and named with a leading underscore, e.g. `_compute_feedforward`.
- Public functions in the kernel are prefixed `mc_` (motion controller) or `du_` (drive unit), matching the product line.

## Build and signing

- The build produces a signed binary for each target. Signing runs in the CI pipeline on the Reutlingen agents; the signing key never leaves the build infrastructure.
- The build and signing steps are documented in `tech-docs/firmware/build-and-signing.md`. The firmware monorepo layout is described in ADR 0009.
