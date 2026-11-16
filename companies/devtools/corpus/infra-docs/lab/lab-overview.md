# The lab

The lab runs a set of hypervisors that exist so we can test Gantline in environments that look like what our customers run. The machines there are not part of the production fleet. We use them for upgrade tests of self-managed installs (including releases that are not ready for prime time), performance runs against a recent build, customer demos that need a live environment, and general team VMs for people who need a box that is not their laptop.

The hypervisors are managed by Lab & hypervisors. If you need a VM, you do not need to talk to anyone — open the lab portal with your Gantline SSO and create one. The portal will pick a hypervisor for you, apply the default image, and give you SSH access. Most VMs are on the standard image, which tracks the current stable release line and includes the `gnt` CLI and the usual build tools. If you need a different base image, the portal has a list of maintained images. If what you need is not there, ask in #lab-infra and someone can build it.

GPU hosts are a separate pool. They are not part of the default portal flow. If your work needs a GPU, open a ticket in the helpdesk with the lab team as the assignee and say what you are running. The GPU hosts are shared, so we will work out a lease length that fits.

For a special setup — a multi-node topology, a specific network shape, or a custom image — the portal will not get you there directly. The usual path is to create a VM, then ask in #lab-infra for the extra pieces. The lab team is small, so for anything bigger than one box, give us a couple of working days of lead time. For customer demos, loop in the Customer Success team early; they know what the demo needs to look like and they can tell us the deadline.

The lab is not the place for long-running services. If you need something up for more than a few weeks, the build farm or a cloud workspace is probably a better fit. The portal shows the lease end date on every VM and sends a reminder before it ends; you can extend a lease from the portal if you still need the box. How lease kinds work and how the team clears out ended leases is in `infra-docs/lab/vm-leases.md`.

If you are not sure whether the lab is the right place for what you are doing, ask in #lab-infra before spinning anything up. The team would rather answer a quick question than clean up after a VM that grew into a small deployment.
