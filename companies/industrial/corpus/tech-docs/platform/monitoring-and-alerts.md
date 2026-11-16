# Monitoring and alerts

**Owner:** Platform & SRE · **Last edited by:** Marisol Reyes

This page covers how {{ALERT_ROUTER|lower}} routes alerts for our platform and factory IT, which channels receive what, and how thresholds get chosen for disk and storage volumes. For dashboards, see the {{DASHBOARD_TOOL}} instance linked from the intranet Platform & SRE page. For alert response runbooks, check the `runbooks/` folder in the platform repo.

## Alert routes

{{ALERT_ROUTER}} routes on alert labels (`severity`, `site`, `service`). Alerts without a `site` label default to Reutlingen. All `critical` alerts also notify the on-call engineer via the paging integration; `warning` alerts do not page.

| Route | Match | Channel |
|---|---|---|
| Platform critical | `severity="critical"`, `service="platform"` | #sre (paging), #reutlingen if `site="reutlingen"`, #telford if `site="telford"`, #greenville if `site="greenville"` |
| Platform warnings | `severity="warning"`, `service="platform"` | #sre |
| Storage | `service="storage"` | #storage (all severities) |
| Factory IT | `service="factory-it"` | #it-help, plus #telford for the drives line, #reutlingen for the main plant |
| Database | `service="orders-db"` | #database |
| Messaging | `service="messaging"` | #messaging-ops |
| Test lab | `service="test-lab"` | #test-lab |

Alerts that match no route go to #sre. The Platform & SRE team reviews unmatched alert traffic each month and adjusts routes rather than adding catch-all rules. If you think an alert belongs in a different channel, raise it in #sre or open a ticket.

## Silences

Silences are for planned maintenance only. Create them from the {{ALERT_ROUTER|lower}} UI using the same label matchers as the alert, and always set an end time — a silence without an end time is treated as a fault and gets removed by the team. For maintenance windows longer than a working day, split the silence into per-day segments so the alert comes back at the end of each shift. The on-call engineer gets notified when a silence expires.

Do not silence an alert because it is noisy; fix the threshold or the alert definition instead. Noisy alerts get discussed in the weekly Platform & SRE review.

## Thresholds for disks and storage volumes

Thresholds are set per volume group, not globally. The default split is `warning` at 80% and `critical` at 90%, but the team adjusts these based on the growth rate and the time needed to remediate:

- **Growth rate:** measure utilisation over at least two full weeks of normal operation. If a volume grows faster than 5% per week, set `warning` at 75% and `critical` at 85% so there is time to add space or move data.
- **Remediation time:** volumes that need a change request or a maintenance window to extend (for example, the MES database files) get a lower `critical` threshold than volumes that can be extended on the fly.
- **Burst behaviour:** volumes that see predictable end-of-month or quarter-end spikes (finance extracts, consolidation) use the base thresholds but the team checks them before the spike window.

| Volume group | Example | Warning | Critical |
|---|---|---|---|
| Orders DB data | `orders-db` primary | 80% | 92% |
| Orders DB logs | `orders-db` transaction log | 70% | 85% |
| File shares (pool-b) | home shares, project shares | 82% | 92% |
| MES shop-floor | plant PC image store | 75% | 88% |
| Test lab captures | `capctl` capture volume | 80% | 90% |
| Build server | firmware build artifacts | 78% | 88% |
| Git mirror | mirror volumes | 80% | 90% |

Threshold changes go through the normal change process and get noted in the {{ALERT_ROUTER|lower}} route comments so the next person knows why a value differs from the default. The {{DASHBOARD_TOOL}} storage dashboard shows utilisation history per volume group; use it when proposing a change.

For questions about a specific alert or threshold, ask in #sre. For access to the {{ALERT_ROUTER|lower}} UI, see `handbook/it/access-requests.md`.
