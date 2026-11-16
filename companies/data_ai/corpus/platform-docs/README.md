# platform-docs

Index for platform, security, batch and support-systems documentation. Owned by the Cloud platform team.

## Contents

- **Cloud**: accounts-and-projects.md, environments.md, backups-and-restore.md, iac-workflow.md
- **Security**: egress.md, secrets.md, service-accounts.md, vulnerability-management.md
- **Batch**: batch-pool.md, submitting-jobs.md (see ADR 0009 for background)
- **Support systems**: case-records.md, helpdesk-admin.md
- **On-call**: oncall-guide.md, incident-process.md
- **Apps**: analytics-api-runbook.md
- **ADRs**: in `adr/` — currently 0004 (COG/STAC) and 0009 (batch cluster). New ADRs follow the same format and live alongside the existing ones.

## Adding a page

Create the file under the relevant folder, add it to the list above, and mention it in `#cloud-platform` or `#batch-cluster` as appropriate. Keep pages focused — if a topic spans platform and support systems, put it in the folder of the team that owns it day-to-day.

## Notes

- Runbooks for the GPU training cluster and model serving live in `ml-docs`; warehouse and pipeline runbooks live in `data-docs`.
- Pages in `support-systems/` are owned by the Support systems team.
