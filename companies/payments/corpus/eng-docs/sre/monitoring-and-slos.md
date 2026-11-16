# Monitoring and SLOs

**Owner:** Site reliability  
**Last edited by:** Ben Whitaker (SRE Lead)

## Service Level Objectives

| SLO | Target | Measurement window | Notes |
|---|---|---|---|
| Authorisation success rate | ≥ 99.95% | 30 days | Successful auth responses (approved or declined) over total auth requests at the gateway, excluding edge WAF blocks. |
| API p99 latency | ≤ 400 ms | 30 days | Merchant dashboard and merchant API calls, measured from the edge to response. Partner API calls are tracked on their own dashboard. |
| Payout files on time | ≥ 99.9% | 30 days | Payout files submitted to the treasury workstation before the bank file cut-off. |

## Dashboards

The main SRE dashboards live in the analytics warehouse and are linked from the `#sre` channel topic:

- **Gateway overview** — auth volume, success rate, p99/p95 latency, error codes by endpoint.
- **Payout pipeline** — file generation times, submission status, retries, cut-off headroom.
- **Payments bus health** — message store depth, consumer lag, DLQ counts per segment.
- **Edge and WAF** — request rates, blocked traffic, TLS handshake failures, certificate expiry.

## Alert Routing

Alerts flow from the monitoring stack into {{ALERT_ROUTER|lower}}, which routes by severity and team:

| Severity | Route | Response |
|---|---|---|
| Page | Paging tool via {{ALERT_ROUTER|lower}} | Immediate, 24/7 duty rotation per the on-call guide |
| Ticket | tickets (priority 2) | Next working day |
| Log | tickets (priority 3) | Triaged weekly |

Routing rules are managed in the `monitoring` repo. Changes go through the normal change management process in the platform handbook.

## Monthly Noisy-Alert Clean-up

On the first working day of each month, the SRE team reviews alert firing history from the previous month. Any alert that fired more than 50 times without a corresponding page or ticket is flagged for review. The team then either:

- Adjusts thresholds or severity in the alert definition,
- Adds a suppression window where the alert is known to be noisy during batch jobs,
- Removes the alert entirely if it has not caught a real issue in two consecutive reviews.

Findings are logged in the monthly review ticket and shared in `#sre`. The paging tool maintains a history of all pages for audit purposes; the review confirms every page had a documented response in the incident tracker.

## Ownership

SRE owns the SLO definitions and the dashboards. Changes to SLO targets require sign-off from the SRE Lead and the VP Engineering. The dashboards themselves are maintained by the SRE team; the data pipelines feeding them are covered in the data lake on-call runbook.
