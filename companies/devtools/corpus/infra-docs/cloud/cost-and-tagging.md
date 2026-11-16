# Cloud cost tagging

Owner: Site reliability. Last edited by Ava Fleming.

## Required tags

Every cloud resource must carry all three tags:

- `team` — the team that owns the resource. Use the team names from the org overview; if you are not sure which team owns something, ask in #engineering before creating it.
- `service` — the service or workload the resource supports. Match the service name in the service catalogue where one exists; otherwise use a short, descriptive name and add it to the catalogue in the same change.
- `env` — one of `prod`, `staging`, `dev`, or `tools`. The `tools` env is for CI runners, build hosts, and similar shared infrastructure, not for application workloads.

Tag resources at creation time. Untagged resources are treated as a defect, not a cleanup task.

## Untagged resources report

The metrics dashboards include a daily report of resources missing any of the required tags, grouped by cloud account and region.

- Site reliability reviews the report on the first working day of the week.
- If a resource has been untagged for more than two working days, the owning team is pinged in #sre.
- Long-lived untagged resources are flagged in the monthly cost review. Repeated occurrences are raised with the team's manager.

## Monthly cost review

Finance and Site reliability meet once a month to review cloud spend.

- Site reliability prepares a short summary of spend by team and by service, using the cloud providers' cost reports.
- Teams with notable increases (more than 10% month over month) are expected to have a representative at the review or to send a comment in advance.
- Any resource that has been untagged for more than a month is called out by name.

## Reserved capacity

Purchases of reserved instances or savings plans are handled by Site reliability, not by individual teams.

- Requests go through the change tracker with the `cloud-costs` label.
- Purchases are made only for workloads that have been running steadily for at least two months and are expected to continue at the same or higher usage.
- The reserved capacity register (in the cloud accounts and regions doc) is updated within two working days of a purchase.
