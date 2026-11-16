# Helpdesk administration

**Owner:** Support systems  
**Last edited by:** Kalani Sokolov  

## Context

The helpdesk is the front door for all customer support traffic — inbound email, the web form on the customer portal, and phone calls routed through the support desk line. We centralised administration under Support systems after the move away from the old per-product mailboxes.

## Queues

Each product line has its own queue:

- **Imagery tasking** — orders placed through the tasking portal, delivery questions, tasking status
- **Monitoring subscriptions** — flood/water and crop/soil subscription customers
- **Analytics API** — API access, quota questions, integration support
- **Billing** — invoices, payment terms, contract questions (handled with FP&A via the finance queue in the CRM)

Queue assignment happens automatically based on the product the customer is associated with in the CRM. Manual reassignment is allowed for any agent but should be rare — if a ticket lands in the wrong queue regularly, tell Support systems rather than working around it.

## Sign-in

SSO is enforced for all agents. The helpdesk trusts our identity provider, so no separate passwords exist for the helpdesk itself. Access is granted through the usual access request process (see `handbook/it/access-requests.md`). New joiners in Support get agent access as part of onboarding; read-only access can be granted to people outside Support on request.

## Macros

Macros live in the helpdesk and are grouped by queue. The common ones (greetings, out-of-office, request for more detail) are maintained by Support systems. Queue-specific macros are maintained by the queue's lead — for imagery tasking that's Imagery operations, for monitoring subscriptions it's the support lead for that product.

Macro names start with the queue name, e.g. `tasking – order received`, `subscriptions – sensor offline`. If you need a new macro, ask in #support and the queue lead can add it.

## CRM sync

The helpdesk syncs bidirectionally with the CRM. Customer details, contract numbers and subscription status come from the CRM into the helpdesk; ticket history and resolution notes go back to the CRM. The sync runs every few minutes and is monitored by Support systems.

One quirk: contact name changes in the CRM can take a while to appear on open tickets. If a customer has changed their name and it matters for the ticket, update it manually.

## Phone line

The support desk phone number routes through the phone system to the helpdesk. Calls land in a dedicated phone queue and are answered by whoever is on phone duty that day. Phone duty is rota'd within the support team per office — Rotterdam covers the morning window, Denver covers the afternoon. The phone line integration creates a ticket automatically when a call is missed, so nothing falls through.

## Permissions

Queue settings (routing rules, macro lists, auto-responses) can be changed by Support systems only. Agents can change their own personal settings and can create personal macros. Anything that affects how tickets are routed or how the queues behave goes through Support systems — the team uses the change tracker for this.

## Known quirks

- The web form sometimes drops attachments over a certain size. Customers get an error message telling them to email instead, but occasionally the ticket still comes through without the attachment. Check the ticket notes if a customer says they attached something.
- The phone integration has a known issue where the caller ID shows as "unknown" for numbers not in the CRM. The ticket still gets created, but the customer may need to confirm their details.
- The old support mailbox (support@) still receives mail and forwards to the helpdesk. This was supposed to be retired but the forwarding rule is still in place — don't remove it, a few long-standing customers still use it.
- Macro variables in the `tasking` queue sometimes render oddly when the order reference contains certain characters. Support systems is aware; workaround is to paste the reference manually.

## Loose ends

- The phone duty rota is still managed in a spreadsheet shared by the support team. Moving it to the roster tool has been discussed but not scheduled.
- The CRM sync was recently upgraded to handle custom fields for monitoring subscriptions. There are a few legacy tickets where those fields are blank — this is expected, not a fault.
