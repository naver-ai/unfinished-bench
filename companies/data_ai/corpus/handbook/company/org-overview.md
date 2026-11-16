# Who does what

A quick map of Brakwater's departments and what they own. For the full org chart and reporting lines, see the HR system — names and team membership live there, not here.

## Departments

| Team | Owns | Main channel |
| --- | --- | --- |
| Executive | Company strategy, M&A, external relations | #announcements |
| People | Hiring, onboarding, payroll, performance, office life | #ask-people |
| Finance | Planning, FP&A, billing, procurement, payroll processing | #finance |
| FinOps | Cloud budgets, cost reporting, reservations | #finops |
| Marketing | Campaigns, events, sales collateral, product marketing | #marketing |
| Brand and communications | Brand, press, social media | #marketing |
| Sales | Subscriptions, tasking orders, partner deals, tenders | #sales |
| Customer Success | Onboarding, renewals, health checks | #support |
| Support | Customer helpdesk, SLAs, escalation | #support |
| Product | Roadmap, UX, pricing input | #apps |
| Data Engineering | Ingestion pipelines, the workflow scheduler, dbt | #data-eng |
| Analytics warehouse | The warehouse, loads, schemas | #data-platform |
| Data Governance | Catalogue, open data, access, DPIA | #data-governance |
| BI and reporting | BI dashboards, scheduled reports | #bi |
| Pricing and commercial analytics | Price lists, commercial analysis, API rate-limit exceptions | #bi |
| Imagery Ops | Satellite tasking, ingest, archive, COGs | #imagery-ops |
| Sensor Network | Ground sensors, field visits, telemetry | #sensor-network |
| ML Platform | Training cluster, model serving, rollout | #ml-platform |
| EO Models | Foundation model, change detection, crop/water models | #eo-models |
| Applied ML | Customer-facing analytics, API model endpoints | #applied-ml |
| Platform | Cloud accounts, {{IAC_TOOL}}, security, on-call | #cloud-platform |
| IT | Laptops, accounts, access requests, service desk | #it-help |
| Cloud security | Incident response, vulnerability management, secrets | #security |
| Legal and compliance | Contracts, privacy and DPIAs, compliance | #data-governance |
| Model governance | Model release reviews, model risk | #model-governance |
| Support systems | Helpdesk administration, phone line, CRM sync | #support |

## Notes

- **Rotterdam HQ** holds most of Engineering, ML, Imagery Ops and Data. **Denver** holds Sales, Customer Success, Marketing and the change detection team. See `handbook/people/working-across-offices.md` for how we collaborate.
- **Tasking orders** go through the tasking portal; customer API access through the customer API console. Both are owned by Product with Imagery Ops supporting delivery.
- **Batch compute** is one shared pool, run by the Batch compute team; data teams run jobs on it daily and `batchctl` shows what is running. See `platform-docs/batch/batch-pool.md`.
- **Model serving** is run by ML Platform; the team that trained a model owns its checkpoints in the modelhub.
- **Support coverage** across offices is in `commercial-docs/support/coverage.md`.
- **Cost tagging** for cloud spend is in `finance-docs/finops/cost-tags.md`; the monthly report comes from FinOps.

For anything not listed here, ask in the team channel or check the handbook index.
