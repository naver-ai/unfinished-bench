# Model serving

Serving runs in three environments: **staging**, **shadow**, and **production**. Staging is for integration checks against the API; shadow receives a copy of production traffic but responses are not returned to customers. Production is the only environment that serves customer requests.

All serving pods run on dedicated GPU node pools in the ML project. Node pools are split per environment so a staging rollout cannot compete with production for GPU capacity. Autoscaling is enabled on all pools, keyed on GPU utilization and request queue depth. If a pool is scaling too slowly, check the autoscaling events on the GPU pool dashboard before adding nodes by hand.

The two shadow slots are `shadow-a` and `shadow-b`. A candidate checkpoint can occupy one slot while the other stays free for the next candidate. Shadow runs for at least a full day of production traffic before we look at the comparison dashboards. When a candidate is promoted, the slot is cleared and the previous production checkpoint becomes the reference in the comparison view.

Dashboards for serving live in the BI dashboards under **ML → Serving**:

- **Latency by model and percentile** — p50/p95/p99, split by environment. Includes queue time before inference.
- **Error rate by model** — 4xx/5xx split, plus inference failures that return a fallback response.
- **Shadow comparison** — response agreement and latency delta between shadow slot and production.
- **GPU pool utilization** — per node pool, with autoscaling events overlaid.
- **Serving cost per model** — GPU hours from the billing export, joined with cost tags.

Customer models currently served:

| Model | Customers | Notes |
|---|---|---|
| flood-forecast-eu | Two North Sea port authorities, several water boards | Hourly inference for gauge sites; also exposed via analytics API |
| flood-forecast-us | Gulf Coast port authority | Same architecture, different regional weights |
| crop-health-temp | Agricultural co-ops in NL and DE | Daily inference on tasking orders |
| soil-moisture-eu | Insurer pilot | Weekly inference, low traffic |
| change-detect-v1 | Internal only | Used by the change detection team before rollout; not customer-facing |

Rollouts follow the process in `ml-docs/serving/rollout.md`. The serving on-call is covered by the ML platform SRE rotation; see the on-call guide for paging details. Model health checks run from the analytics API runbook.

Checkpoint storage is on the `serving-checkpoints` fileset. A monthly job prunes old serving copies; the current production checkpoint and the recent shadow candidates are kept.

Last edited by Daniel Arslan.
