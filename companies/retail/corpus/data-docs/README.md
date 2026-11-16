# data-docs

Index for the data documentation space. Owner: Data engineering. Last edited by Leila Doyle.

## What’s here

- `catalogue.md` — data catalogue, short version. Covers warehouse tables, key fields, and which team owns what.
- `dpia-notes.md` — DPIA working notes. Read before starting anything new that touches personal data.
- `sharing.md` — notes on sharing data outside Mossgrove. Check this before sending anything to a partner.

## Who to ask

- Data access requests: start with the Data engineering team on #data-eng.
- Warehouse access and permissions: Joy Mbeki handles the access review cycle.
- Catalogue updates: add a row or flag a change in the doc, then ping Leila or Greta in #data-eng.
- Legacy pipeline questions: Ada Aoki still knows the old `datasync` jobs better than anyone, even though the scheduled moves now run as warehouse export jobs.

## Notes

- The catalogue is maintained manually for now. It lags the warehouse by a few weeks sometimes.
- If a table isn’t in the catalogue, check the warehouse `information_schema` before assuming it’s gone.
- The US e-commerce tables live in the same warehouse but are prefixed `us_`. Columbus owns those, so check with them before changing anything.

See `eng-docs/data/warehouse.md` for the warehouse layout and connection details.
