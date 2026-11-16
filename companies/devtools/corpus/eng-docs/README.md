# eng-docs

Owner: Product engineering · Last edited by Ingrid Holm

Engineering documentation index. Keep this current when adding pages.

## Contents

- **On-call** — `oncall/`: incident process, on-call guide
- **Practices** — `practices/`: code review, testing, RFC process
- **Services** — `services/`: service catalogue, environment definitions
- **Release** — `release/`: release train, builds and runtimes, publishing, versioning
- **Security** — `security/`: secrets management
- **ADRs** — `adr/`: architecture decision records (currently microVM runners, regional data)
- **API** — `api/`: public API overview
- **CLI** — `cli/`: gnt architecture
- **Editor / mobile / search / identity** — one page each for current architecture and key decisions

## Adding a page

- Create the file under the relevant area folder, add a one-line description in the right section above, and link it in the service catalogue if it describes a service.
- RFCs live in their own repo (`rfcs`), not in this tree — point to them from here if useful.

## Notes

- Pages under `practices/` are expected to be short and updated in place, not versioned.
- `release/` pages cover both hosted and self-hosted runners; check which one you are documenting before editing.
