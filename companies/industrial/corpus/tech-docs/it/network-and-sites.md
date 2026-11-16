# Network and sites

Needs a tidy-up after the last round of rack changes — ping #sre if something here looks wrong.

Owner: IT infrastructure · Last edited by Olivier Young

## Site networks

| Site | LAN / WAN uplink | Plant network segment | Notes |
|---|---|---|---|
| Reutlingen (HQ) | 10.20.0.0/16, 2× 10 Gbit/s uplinks | 10.30.0.0/16 (OT) | Main plant and test lab on separate VLANs; OT segment is air-gapped from office LAN except for the MES gateway hosts |
| Telford (UK) | 10.40.0.0/16, 1× 10 Gbit/s uplink | 10.50.0.0/16 (OT) | Drives line and distribution centre share the OT segment; the line PLCs are on their own VLAN within it |
| Greenville (US) | 10.60.0.0/16, 1× 1 Gbit/s uplink (upgrade planned) | 10.70.0.0/16 (OT) | Americas service office and US plant on the same site; OT segment covers the test stands and the calibration benches |

The OT segments at all three plants are managed by the plant engineering teams in daily operation; IT infrastructure owns the routing, the firewalls and the remote-access jump hosts. Firmware updates to drives and controllers on the OT network go through the MES gateway hosts — never connect a laptop directly to an OT switch port.

## WAN links

All three sites are connected over the site-to-site VPN with the hub in Reutlingen. Telford and Greenville have a direct link between them for the shared ERP and PLM replication traffic — this was added when the drives plant started building to Reutlingen designs directly from the PLM.

| Link | Bandwidth | Use |
|---|---|---|
| Reutlingen ↔ Telford | 10 Gbit/s | ERP, PLM, MES replication, voice |
| Reutlingen ↔ Greenville | 1 Gbit/s | ERP, PLM, mail, file shares (pool-b replication) |
| Telford ↔ Greenville | 1 Gbit/s | PLM replication, MES reporting |

The MES at each plant writes to its local instance and replicates to Reutlingen every few minutes. If a WAN link is down, the MES keeps running locally; only cross-plant order visibility is affected.

## Guest Wi-Fi

Guest SSID is `Kessendorf-Guest` at all sites. Access is self-service via the portal, valid for one working day, and the terms page is shown on first connect. Staff should use the corporate SSID, not the guest network. The guest network is on a separate VLAN with no route into the office LAN or the OT segments.

## Changes and requests

Network changes (VLANs, firewall rules, WAN routing, Wi-Fi SSIDs) go through the tickets system with the `network` tag. Incident-related changes are handled through the standard escalation path — see the service desk handbook for how to raise those. The #sre channel is the right place for questions about link status or monitoring.

For plant OT network changes, coordinate with the plant engineering team first — the IT infrastructure team will not touch OT switches without their sign-off on the ticket. Guest Wi-Fi password resets and SSID questions are handled by the service desk directly.
