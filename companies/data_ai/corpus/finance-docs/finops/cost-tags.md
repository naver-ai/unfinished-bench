# Cloud cost tagging

**Owner:** FinOps (cloud cost)  
**Last edited by:** Rahul Muller  

## Required tags

- `team` — the team that owns the resource (use the team names from the org overview, e.g. `eo-models`, `sensor-network`, `data-platform`).
- `project` — the project or initiative the resource belongs to (e.g. `floodwatch-nl`, `crop-insight-pilot`).
- `env` — `prod`, `staging`, `dev`, or `test`. If a resource is shared across environments, tag it as `shared` and note it in the resource description.
- `customer` — required for any resource that processes data for a specific customer (water board, port, co-op, insurer). Use the customer short code from the CRM. If a resource serves multiple customers, use `multi-customer` and list the customers in the description field.

## Untagged resources

- A report of untagged resources is posted to #finops twice a week. It lists the resource, the project it appears to belong to, and the owning team if we can infer it.
- If a resource appears in the report for two consecutive postings and still has no tags, the owning team gets a ping in #finops and the resource is flagged as `data-shared` for cost allocation purposes.
- Untagged spend lands in the `data-shared` cost centre. The monthly cost report shows this as a line, and teams are expected to keep it near zero.

## Fixing tags in bulk

- For compute and storage resources, use the bulk tagging page in the cloud console to apply tags to multiple resources at once. You can filter by project prefix or by the `data-shared` flag.
- For resources created by {{IAC_TOOL}}, update the tags in the {{IAC_TOOL}} definitions and apply. Do not hand-edit resources that {{IAC_TOOL}} manages — the next apply will revert it. See `platform-docs/cloud/iac-workflow.md`.
- If you spot a resource that clearly belongs to another team, tag it with the correct team and drop a note in #finops so we can reconcile the cost centre.
- For anything that looks like it was created outside the normal workflows (e.g. a one-off notebook cluster), ask the team in the relevant channel before tagging — it may be a trial that should be shut down instead.
