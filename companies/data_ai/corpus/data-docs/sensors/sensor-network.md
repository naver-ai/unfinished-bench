# Ground sensor network

Owner: Ground sensor network  
Last edited by: Reza Tanaka

## Scope

Covers river gauges, rain gauges and soil moisture probes deployed across our monitoring sites, plus the telemetry path from field to warehouse. Sensor fleet and site registry live with the Sensor Network team; anything about the field app itself is in the field app docs.

## Telemetry path

Sensors report over the cellular modem on each site's logger. Readings are pushed to the ingest endpoint every 15 minutes for river and rain gauges, hourly for soil moisture. Ingest validates the reading against the site's instrument type and range, then writes to the raw sensor table in the warehouse. If the warehouse write fails, the ingest retries for up to 30 minutes before dropping the reading into a dead-letter bucket.

## Site registry

The site registry is the source of truth for all deployed instruments. It lives in the Sensor Network team's project area and is backed up nightly. Each site record contains:

- Site id
- Location (coordinates, plus a named reference to the nearest water body or field parcel)
- Instrument type and serial
- Status (active, maintenance, closed)
- Collection set (current, reserve, candidate or closed — reset each year from the network plan)
- Source (our own instrument, or the partner who operates it)
- Installed date and last calibration visit

Sites are added through the change tracker; the Sensor Network team reviews requests from customer onboarding and from Geo operations. Site retirement requires the site owner to confirm no active subscription depends on the readings — check the customer API console for active queries against the site before retiring.

## Calibration visits

Calibration is due per the instrument datasheet, typically twice a year for river gauges, quarterly for rain gauges. Calibration visits are scheduled through the field app and the visit result (adjustment applied, sensor replaced, or no action) is recorded there. The field app writes the calibration event back to the site registry so the warehouse can join readings to the calibration history.

Nina Sato coordinates field routes across the Netherlands and can help with visit planning for the US sites.

## Battery swaps

Loggers run on a solar panel plus battery. Battery level is reported with each reading; the alert threshold is 20%. Battery swaps are planned through the field app and logged against the site. Swaps are batched with calibration visits where possible to reduce field time. A small stock of batteries is held at the Rotterdam office and at the Denver office for the US sites.

## Readings in the warehouse

Raw readings land in `raw.sensor_readings` with the site id, measured value, and received timestamp. The warehouse dbt layer builds the cleaned `sensor.sensor_readings` table, applying calibration offsets and flagging values outside the instrument's plausible range. A separate table `sensor.site_status` is maintained for operational status (active, maintenance, closed) and should be joined to readings when a site is used in analytics.

The BI dashboards for flood and soil monitoring read from the cleaned tables. Any change to the cleaning logic goes through the usual dbt review cycle in the warehouse repo.

## Loose ends

- The ingest endpoint's dead-letter bucket needs a periodic review; nothing currently monitors it for growth.
- A few older sites still report through the legacy collector that was replaced for new deployments. Those sites are on the list for a logger swap, but the schedule depends on field capacity.
- The site registry has a handful of closed sites that still show as maintenance — the team is working through the backlog to confirm their status with the relevant account owners.
- Soil moisture probe depth is not consistently recorded for all sites; should be added to the registry before the next planting season reporting.
