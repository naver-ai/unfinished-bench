# About Brakwater

Brakwater Geo B.V. started as a small flood-mapping consultancy for Dutch water boards, working out of a shared office in the Rotterdam port area. The early work was mostly manual: field visits, survey data, and a lot of hand-drawn risk maps for local drainage authorities. Over time we built our own ground sensor network to get water level readings directly from ditches, canals and storm basins, which made the flood models considerably more useful than relying on public measurement stations alone.

From there we moved into satellite imagery, first as a way to fill gaps between sensor readings, then as a product in its own right. We now operate our own analytics platform that combines imagery from multiple providers with our ground network, and we train our own earth observation models on the imagery archive. The company has grown to about 310 staff, with offices in Rotterdam (headquarters) and Denver, which we opened to serve US agricultural co-ops and crop insurers.

## What we sell

Our main products are:

- **Monitoring subscriptions** – recurring delivery of flood risk, water level, crop health and soil moisture insights for a defined area of interest. Most subscribers are water boards, port authorities, agricultural co-ops and insurers. Subscriptions include access to the customer API console and the data catalogue, and can be configured with alerts for threshold breaches.
- **Imagery tasking orders** – one-off or standing orders for satellite imagery over a specific area, placed through the tasking portal. Customers typically use these for event response (e.g. a storm surge or a flooding incident) or for seasonal monitoring where they need higher revisit frequency than our standard archive covers.
- **Analytics API** – programmatic access to our derived products: water level estimates, flood extent, crop stage, soil moisture indices and similar. The API is used both by customers directly and by partners who build their own applications on top of our data.

## Customers

On the water side, our customers are mostly Dutch and German water boards, a few port authorities in northwest Europe, and some flood-prone municipalities. On the agriculture side, we work with large agricultural co-ops in the US Midwest and Plains, plus a number of crop insurers who use our soil moisture and crop stage data to adjust loss adjustment processes. We also have a smaller set of consulting firms and research institutions that buy imagery tasking orders and use the analytics API for specific projects.

## Departments

The company is organised into a number of teams, each owning a specific part of the platform:

- **Executive team** – sets company direction, owns the budget and major partnerships.
- **Product management** – owns the roadmap for the analytics API, the tasking portal and the monitoring subscriptions.
- **Web app and API** – builds and maintains the customer-facing applications: the tasking portal, the customer API console, and the internal tools that support them.
- **ML platform** – runs the GPU training cluster and the model serving infrastructure. This team also looks after the modelhub, where trained checkpoints are registered.
- **Applied ML and EO models** – develop the earth observation models themselves, including labelling, training and offline evaluation.
- **Data engineering and data platform** – own the imagery ingest pipelines, the analytics warehouse, and the data catalogue. They also run the workflow scheduler for batch pipelines.
- **Ground sensor network** – designs, deploys and maintains the physical sensor network, including the field app used by technicians during site visits.
- **Imagery operations** – handles tasking orders, works with satellite providers, and manages the imagery archive.
- **Customer support** – runs the helpdesk and handles escalations; the helpdesk itself is administered by the support systems team. Support coverage across offices is described in commercial-docs/support/coverage.md.
- **FinOps** – manages cloud costs, budgets and commitments. They publish the monthly cloud cost report.
- **Customer success and delivery** – owns onboarding and ongoing relationships with subscribers and API customers.

## Offices and working across them

Rotterdam is the larger office and houses most of the engineering, data and imagery teams, plus the executive team and finance. Denver is primarily customer-facing for the US agricultural market, with sales, customer success and a small engineering presence that works closely with Rotterdam on API and data platform topics. Most cross-office collaboration happens over chat and the usual video calls; the working-across-offices page in the handbook has practical guidance on overlap hours and communication norms.

## A note on how we work

We are a data company and we try to act like one: most decisions are documented in the relevant team's docs, changes to shared infrastructure go through the change process in the tickets system, and we run an internal status page so everyone can see what is going on with the platform. If you are new, the onboarding checklist in the handbook is a good place to start, and the org-overview page explains who does what in more detail.
