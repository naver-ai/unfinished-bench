# Who does what

This page gives a quick map of teams at Kilbarra. For the full org chart, reporting lines and current team membership, check the HR system — that is the source of truth. This page is a rough guide for finding the right channel or team when you are new or when you are reaching across departments.

## Engineering

| Team | Owns | Channel |
|---|---|---|
| Merchant payments | Merchant API, hosted checkout, the payments gateway and 3DS | #payments-dev |
| Payments platform | Payments bus, core ledger and ledger API, settlement and payout services | #payments-platform |
| API platform & edge | API gateway and the edge | #platform |
| Integrations & partners | Partner integrations, webhooks, solutions engineering | #partner-integrations |
| Merchant apps (dashboard & mobile) | Merchant dashboard, mobile app, payment links, the back office | #dev-platform |
| Data products | Scheme and bank file ingestion, warehouse sync | #data-lake |
| Data platform | Data lake, pipelines, analytics warehouse | #data-lake |
| Infrastructure | Cloud accounts, databases, networks, backups | #platform |
| Developer platform | CI/CD, deployctl, environments, the release train | #dev-platform |
| SRE | Monitoring, SLOs, on-call, incident response | #sre |
| Security | SIEM, SOC, PKI, secrets, appsec | #security |

Engineering also runs the internal change process through the tickets system; see `eng-docs/platform/change-management.md` for how changes are approved and scheduled.

## Finance & Treasury

| Team | Owns | Channel |
|---|---|---|
| Treasury & settlement | Safeguarding, settlement runs, payouts, treasury workstation, bank files | #treasury-ops |
| Finance operations | Month-end close, revenue accounting, the reconciliation tool | #finance-eng |
| Finance engineering | batch-reconciler and the finance data jobs | #finance-eng |
| Payroll & payables | Payroll, supplier payments | #finance-eng |
| Regulatory reporting | Supervisory returns, returns calendar, data lineage | #reg-reporting |
| Merchant billing | Merchant invoices, plan fees, plan-change billing | #billing |

Finance publishes its own docs under `finance-docs/`, including the returns calendar and the safeguarding policy.

## Risk & Compliance

| Team | Owns | Channel |
|---|---|---|
| Financial crime | Merchant due diligence (KYB), transaction monitoring, the case tool | #compliance |
| Risk controls | Merchant risk ratings, chargeback monitoring | #risk-controls |
| Compliance | Complaints, outsourcing register, regulatory change log | #compliance |
| GRC | Control testing, PCI DSS and SOC 2 evidence, access reviews | #compliance |
| Privacy & data governance | Data subject requests, DPIAs, records of processing | #data-governance |

## People, Legal & Office

| Team | Owns | Channel |
|---|---|---|
| People team | Hiring, onboarding, payroll, leave, performance, expenses | #general |
| Legal | Contracts, records retention, who can sign, press and social media | #general |
| Office & IT | Devices, sign-in, access requests, offices in Dublin, Vilnius and Austin | #it-help |

## Sales & Merchant Success

| Team | Owns | Channel |
|---|---|---|
| Merchant success | Quarterly reviews, merchant segments, account management | #merchant-success |
| Merchant support | Helpdesk, support handbook, escalations | #merchant-support |
| Merchant operations desk | Onboarding operations, collections, the disputes desk | #merchant-support |
| Incident & merchant communications | Merchant notices, writing to merchants | #customer-comms |
| Sales | New merchant deals, plan selection | #partnerships |
| Partnerships & RevOps | Partner programme, the CRM, partner data feeds | #partnerships |

## Find the right channel

If you are not sure where something belongs, start in the team channel listed above and ask. The chat directory in the HR system has the full list of channels with descriptions. For operational topics — an active incident, a change window, a partner feed issue — the relevant team channel is still the right first stop; the on-call rota is in the paging tool and the on-call guide under `eng-docs/oncall/`.

Last edited by Milan Balogun, People team.
