# Code search overview

Owner: Search & indexing. Last edited by Mehmet Yilmaz.

## How code search works

The search-indexer service consumes push events from git-gateway and builds shards per repository. Shards are written to object storage and registered in the search-query service's index registry. search-query serves all read traffic; it talks to the registry to find the right shard set for a given org and repository, then loads shards into memory.

Shard builds are incremental. When a push comes in, the indexer fetches the changed refs, computes the diff against the last indexed commit, and applies a delta update. Full reindexes happen when the delta chain is too long or when we change the index schema.

## Freshness

The indexer emits a freshness metric per repository (time since last successful index). The search dashboard tracks p95 freshness across all orgs. We page when a top-tier org's repository goes more than 30 minutes without indexing a push. The alert is configured in the paging tool; the runbook points at the indexer logs and the git-gateway event queue.

## Reindexing a large org

For orgs with more than 5,000 repositories, a full reindex can take several hours. We run these as background jobs, throttled so they don't starve incremental indexing. The indexer has a per-org concurrency limit; bumping it requires a ticket to the Search team.

The search-query service holds shards in memory. When a large reindex completes, the new shard set is swapped in atomically. Old shards are released once no queries reference them.

## Synonyms and ranking

The synonyms file lives in the search-indexer repo and is deployed with the service. It maps common misspellings and abbreviations to canonical terms. Changes to synonyms go through the usual review process and are applied on the next shard build — we don't rewrite existing shards.

The ranking profile is a separate file, also in the search-indexer repo. It controls term weighting, recency boost, and the default tie-break ordering. We've had a few rounds of tuning based on the search metrics dashboards; the current profile is the result of the last tuning pass.

## Loose ends

- The indexer still references an old bucket path from before the shard storage moved to the new layout. It works, but it's on the list to clean up.
- Ruth wrote the original freshness alert and still gets pinged about it directly; it should go through the Search on-call route like everything else.
- The synonyms doc that used to live in the search docs site has been folded into the main docs site, but a couple of internal links still point at the old location.
