# Open source at Gantline

Owner: Legal · Last edited by Samir Kaplan (Product Counsel)

This page covers how we license and contribute to open source. If you have a question that isn't answered here, ask in #contracts-help.

## The gnt CLI

`gnt` is published under the Apache-2.0 license. All source code lives in public repositories under the `gantline` organization on the code host we use for public projects. The license text and NOTICE file are in the repository root — do not alter them without Legal review.

The gnt codebase includes a few vendored components that carry their own licenses (BSD, MIT, ISC). These are fine to keep; the NOTICE file lists them.

## Contributor licence agreement

Outside contributors to `gnt` must sign a contributor licence agreement (CLA) before we accept their pull requests. The CLA is managed through the same bot used by the `gnt` repository — it checks every pull request for a signed CLA on file and blocks merge until one is present. The CLA text is the standard Apache-style individual CLA, with Gantline Inc. named as the beneficiary for US contributors and Gantline Software, Lda. for everyone else. Legal maintains the templates; if a contributor asks to negotiate terms, point them to Samir.

Company employees do not sign the CLA. Our employment agreements and contractor agreements already assign IP to Gantline, so the CLA check is configured to skip accounts linked to a Gantline email domain.

## Contributing to other projects

We encourage contributing fixes and small improvements to open-source projects we depend on. This counts as work time, and you do not need approval for contributions that meet all of the following:

| Condition | What it means |
|---|---|
| Scope | A bug fix, documentation fix, or small feature — roughly a day of work or less |
| Project | A project we already use in Gantline Cloud or in `gnt` (check the dependency manifests) |
| License | The project is under a permissive license (MIT, BSD, Apache-2.0) or a weak copyleft license (LGPL, MPL, EPL) |
| Ownership | You are contributing your own work, not code written by someone else at Gantline |

Anything else — new projects, contributions we don't directly depend on, larger features, or projects under strong copyleft licenses (GPL, AGPL) — needs a quick check with Legal first. Send a note to #contracts-help with the project, the license, and what you plan to contribute. This is a same-day review, not a process.

If you maintain a personal project that overlaps with Gantline's business, keep it separate from your Gantline accounts and machines.

## Using open-source code inside Gantline Cloud

Most permissive licenses are fine to use in Gantline Cloud without asking. The table below is the general guidance:

| License family | Examples | Inside Gantline Cloud? |
|---|---|---|
| Permissive | MIT, BSD-2/3-Clause, ISC, Apache-2.0, Zlib | Yes — no review needed |
| Weak copyleft | LGPL-2.1/3.0, MPL-2.0, EPL-2.0 | Yes for libraries, with attribution preserved. Talk to Legal before linking into a distributed binary in ways that trigger LGPL obligations |
| Strong copyleft | GPL-2.0/3.0, AGPL-3.0, SSPL | No — talk to Legal before using in any Gantline Cloud service or tooling |
| Source-available / non-OSI | Elastic License, BUSL, Commons Clause | No — talk to Legal first |
| Unlicensed / unknown | No license file, "all rights reserved", withdrawn licenses | No — treat as unavailable |

When you add a dependency, check its license before you open the pull request. The `gnt` dependency scanner flags unknown or strong-copyleft licenses in CI for `gnt` itself; for Gantline Cloud services, the same check runs in the build pipeline for the main service repos. If the scanner flags something, resolve it with Legal before merging.

Some projects dual-license: one license for open source, a separate commercial license. If you are evaluating a project that offers a commercial license as an alternative, you do not need to involve Legal just to read the terms — but if you think we would need the commercial license, loop in Samir before you commit to it.

## Questions

- CLA or licensing questions: #contracts-help
- Adding a dependency with a license you are unsure about: #contracts-help
- Everything else: ask in #contracts-help and we will point you at the right place.
