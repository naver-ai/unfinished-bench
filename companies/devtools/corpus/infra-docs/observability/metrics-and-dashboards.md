# Metrics and dashboards

**Owner:** Site reliability  
**Last edited by:** Ava Fleming (SRE Manager)

## Context

We've grown from a handful of services to a few dozen, and the metrics stack has grown with us organically. Dashboards were being created ad hoc, often by whoever was on call, with naming that made sense to them at the time. This made it hard to find the right dashboard during an incident, and some services had no dashboards at all.

The SRE team ran a short review of how we use {{METRICS_DB}}, {{DASHBOARD_TOOL}}, and the metrics dashboards, and we've settled on some conventions. This doc captures those decisions so everyone can follow them.

## Metrics stack

We run {{METRICS_DB}} for metrics collection, with {{DASHBOARD_TOOL}} for dashboards and alerting. Metrics are retained for 15 months. The {{METRICS_DB}} servers are operated by Site reliability; if you need access to a server or want to add an exporter, ping #sre.

The metrics dashboards are at `metrics.gantline.dev`. The dashboards live in the `metrics` repository, which is owned by Site reliability.

## Dashboard naming

Each service gets one primary dashboard, named `{service}`. The service name must match the service catalogue entry in eng-docs/services/service-catalogue.md. If you can't find your service in the catalogue, that's the first thing to fix.

Secondary dashboards get a suffix: `{service} - {aspect}`. For example, `billing-service - queue depth` or `gnt - publish latency`. Keep the suffix short and descriptive; avoid acronyms unless they're in common use across the company.

A service dashboard should have:

- Request rate, error rate, and latency (RED) for each endpoint or job
- Resource usage (CPU, memory, disk) for each instance
- A link to the service's runbook in the on-call guide

## SLOs and error budgets

Each service with a user-facing SLA has an SLO defined in the service catalogue. The SLOs are stored as {{METRICS_DB}} recording rules in the `metrics` repository, next to the service's dashboard. The error budget is computed from the SLO and shown on the service dashboard.

For services without an explicit SLO, the default is 99.9% availability over a rolling 30-day window. If you think your service needs a different SLO, raise it with Site reliability.

## Alert rules

Alert rules live next to the service code, in the `alerts` directory of each service repository. This keeps alerts close to the people who understand the service. The rules are deployed by the CI pipeline for each service, and the SRE team reviews new alerts as part of the code review process.

When you add an alert rule, include a runbook link in the alert annotation. The runbook should say what to check first and who to page. Don't page someone without a runbook — it just leads to confusion.

## Asking for a new dashboard

If you need a dashboard that doesn't exist, open a ticket in the change tracker with the `dashboards` label. Include:

- The service name and what you're trying to understand
- The specific queries or panels you have in mind (a sketch is fine)
- Whether this is for an ongoing need or a one-off investigation

The SRE team reviews dashboard requests twice a week. If it's urgent, ping #sre and someone will take a look.

## Open questions

- Should we move dashboard configuration into each service repository, alongside the alert rules? That would give service teams more ownership, but it means the SRE team can't make quick fixes during an incident. To be discussed with the service teams at the next engineering sync.

## Loose ends

- The `metrics` repository still has a few old dashboards that don't follow the naming convention. We'll clean those up as we touch each service, but if you notice one that's actively misleading, flag it in #sre.
- A short guide on querying {{METRICS_DB}} for people who aren't familiar with PromQL is still to be written (tbc). Until then, the existing dashboards are a good starting point for copy-paste.
- Dashboard folder structure in {{DASHBOARD_TOOL}}: no convention yet (tbc) — right now it's a flat list, which is getting hard to browse.
