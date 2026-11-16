# tech-docs

Index of engineering and IT platform documentation. Owner: IT infrastructure. Last edited by Olivier Young.

## Areas

- **ADR** — decisions and rationale for platform changes, `adr/`
- **Factory IT** — MES and shop-floor PCs, `factory-it/mes-and-shopfloor.md`
- **Firmware** — build pipeline, signing, coding standards, `firmware/`
- **Identity** — joiners/movers/leavers, seasonal intake directory, `identity/`
- **IT operations** — backups, network, service desk, `it/`
- **Messaging** — mail, calendars, mail archive, `messaging/`
- **Orders DB** — schema overview, migration runbook, `orders-db/`
- **Platform** — monitoring and alerting, `platform/monitoring-and-alerts.md`
- **SCM** — source control, Git mirror, `scm/`
- **Storage** — file shares, NFS retirement, `storage/`

## Adding a page

- Place it under the matching area folder.
- Add a one-line pointer above.
- If the change is architectural, write an ADR instead of a page.
- Update this index in the same commit.

## Notes

- Capture server docs moved to ops-docs/test-lab/ — the old link in `factory-it/` still points there.
- Telford drives line docs live under ops-docs/plants/, not here.
- For questions on ADRs, ask the firmware or platform team leads first.
