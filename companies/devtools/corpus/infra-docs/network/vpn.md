# VPN

> Needs updating after the Portland office refresh — ping #netops if something here looks wrong.

The staff VPN client is the {{VPN_SOFTWARE}}-based `gnt vpn` command (installed via the `gnt` toolchain). It covers access to internal hosts that aren't exposed on the public internet: the admin console's private endpoints, the helpdesk's internal mirror, the metrics dashboards' internal views, the build farm's orchestration API, and the lab hypervisors' management interfaces. Most other systems (chat, email, the CRM, the data warehouse, the password manager, the feature flag service) are reachable without the VPN.

Connecting from the Portland office or the Lisbon office is not needed — office networks are already on the internal backbone. From home or on the road:

1. Run `gnt vpn up` from a terminal. The client picks the nearest regional entry point automatically.
2. If you're on a laptop that has both the corp profile and a personal profile, make sure you're on the corp profile first (`gnt auth status`). The VPN will refuse to start otherwise.
3. When you're done, run `gnt vpn down`. The client idles out after 8 hours as a safety net, but you'll get a reminder in chat before that.

For cloud workspaces, the VPN is already enabled inside the workspace image — you don't need to start it manually. The mobile apps never use the VPN; they talk to the public API directly.

### If it goes wrong

- **"No usable IP range"** — you're on a network that blocks UDP. Try `gnt vpn up --tcp-fallback`.
- **Hotel or conference Wi-Fi** — many of these block the UDP port the VPN uses. The `--tcp-fallback` flag usually works. If the connection comes up but pages hang, try switching to the other regional entry point with `gnt vpn up --region=us --tcp-fallback`.
- **DNS looks wrong after disconnecting** — run `gnt vpn down --flush-dns`.
- **Nothing helps** — grab the output of `gnt vpn diagnostics` and post it in #netops. Avoid pasting full output if it contains hostnames you don't recognise; the team will ask for specifics if they need them.

Owner: Network engineering. Last edited by Freya Lindgren.
