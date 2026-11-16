# Cloud accounts and projects

Owner: Cloud platform  
Last edited by: Kasia Nowak

This page lists the cloud accounts we run and what lives in each. If you need access to an account, see [Getting access to systems](/handbook/it/access-requests.md). For tagging requirements, see [Cloud cost tagging](/finance-docs/finops/cost-tags.md).

| Account | Purpose | Owning team | Region |
|---|---|---|---|
| imagery-prod | Satellite ingest, processing pipelines, imagery catalogue | Imagery acquisition and processing | eu-west-1 |
| analytics-prod | Scheduled data jobs, warehouse transforms, BI extracts | Data engineering | eu-west-1 |
| web-prod | Web app, analytics API, customer API console | Web app and API | eu-west-1 |
| ml-training | GPU training cluster | ML platform | eu-west-1 |
| ml-research | Experimentation and small training runs | Earth observation models | eu-west-1 |
| data-shared | Shared platform services, untagged resources | Cloud platform | eu-west-1 |
| dev | Development and integration testing | All teams | eu-west-1 |

## Notes

- **imagery-prod** also hosts the tasking portal and the field app backend. Imagery ingest pipelines are described in [Imagery ingest](/data-docs/pipelines/imagery-ingest.md).
- **analytics-prod** runs the workflow scheduler and the scheduled data jobs that feed the warehouse and the BI extracts.
- **web-prod** serves both the customer-facing web app and the analytics API. Runbooks live in [Analytics API runbook](/platform-docs/apps/analytics-api-runbook.md).
- **ml-training** is the GPU cluster documented in [GPU training cluster](/ml-docs/cluster/overview.md). Research work that needs GPUs should go through [Getting GPU time](/ml-docs/cluster/getting-gpu-time.md) rather than ml-research.
- **data-shared** is where we keep shared services like the data catalogue, the notebook server, and supporting infrastructure that doesn't belong to a single product line. Resources here are expected to be tagged with the owning team where one exists.
- **dev** is a single account shared by all teams. Prefer using separate projects or prefixes within dev over creating new accounts.

## Account access and ownership

Each account has a primary owning team listed above. The Cloud platform team administers all accounts. If you need something in an account you don't own, ask the owning team first — they will usually be able to help without a Cloud platform ticket.

Region choices are fixed per account; we do not run multi-region today. If you believe a workload needs a different region, raise it with the Cloud platform team before building anything.

Cost tracking follows the account boundaries above. See [Cost reporting](/finance-docs/finops/cost-reporting.md) for how we allocate spend across accounts and teams.
