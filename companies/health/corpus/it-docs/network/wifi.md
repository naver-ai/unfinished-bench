# Wi-Fi Networks

**Owner:** Network engineering & remote access  
**Last edited by:** Ivan Walsh

Needs updating after the Valparaiso refresh — ping #network-ops if something here looks wrong.

## Campus networks

| Campus | Staff SSID | Clinical device SSID | Guest SSID | Notes |
|---|---|---|---|---|
| South Bend (HQ/hospital) | Kellsbrook-Staff | Kellsbrook-Devices | Kellsbrook-Guest | Devices SSID is broadcast; staff and guest are hidden |
| Valparaiso (hospital/health plan) | Kellsbrook-Staff | Kellsbrook-Devices | Kellsbrook-Guest | Guest SSID only on floors 1–2; hospital wing uses South Bend's RADIUS |
| Kalamazoo (hospital/research institute) | Kellsbrook-Staff | Kellsbrook-Devices | Kellsbrook-Guest | Research institute wing has no guest coverage — use the hospital wing |
| Cork (medical centre/IT ops) | Kellsbrook-Cork-Staff | Kellsbrook-Cork-Devices | Kellsbrook-Cork-Guest | Separate SSIDs; no roaming with US campuses |

## Which devices go where

- **Kellsbrook-Devices** is for clinical equipment only: infusion pumps, physiological monitors, unit phones, medication dispensing cabinets, and the label printers on the lab floors. Do not connect staff laptops or personal phones to this SSID.
- **Kellsbrook-Staff** is for company-issued laptops, phones and tablets. Personal devices should use the guest network — the staff network requires the device certificate from the VPN client profile.
- **Kellsbrook-Guest** is for visitors and personal devices. It is internet-only and does not reach internal systems. The patient app and patient portal are reachable from guest Wi-Fi.

## Certificates

Staff devices get the Wi-Fi certificate automatically when they enrol for the VPN client. Clinical devices that need certificates (the medication cabinets and the newer infusion pumps) are provisioned by the device vendor during installation — see the clinical workstations page for the badge tap process, which uses the same certificate store.

If a device drops off the clinical device network, first check that its certificate hasn't expired. Certificates for clinical devices are valid for 12 months; staff device certificates are valid for 24 months. Re-issue requests go through tickets with the device's asset tag.

## Requesting coverage changes

Coverage additions or SSID changes go through the change management process. For a new building or a floor remodel, submit the request at least two weeks before the go-live date so network engineering can do a site survey. Temporary coverage for events (health fairs, screening clinics) is handled by the same process but with a shorter lead time — the Kalamazoo research institute sometimes needs ad-hoc coverage for trial recruitment days.

There is no coverage in the Cork IT operations room beyond the standard office SSID — the server racks are wired only.
