# Reporting a security incident

**Owner:** Security  
**Last edited by:** Daniela Ferraz

## What counts as a security incident

- A lost or stolen laptop, phone, or hardware key (including a device you left in a cab or at a gate)
- A phishing message you clicked, or one you spotted and want to flag
- A credential you think leaked — a token in a public gist, a password in a commit, an API key in a log you happened to read
- Access you didn't expect — a permission on an account you never requested, a session that stayed alive after you revoked it, a runner that answered from an IP it shouldn't have

If you are unsure whether something counts, report it anyway. The Security team would rather close a false alarm than miss a real one.

## How to report

1. Go to the `#security` channel in chat and post what you saw. Include the system or service involved, the time window you noticed it, and anything you touched since then. Do not paste credentials or secrets into chat.
2. If the channel is quiet or you want a tracked ticket, open one in the helpdesk using the "Security incident" category. That goes to the same queue — chat is just faster for a first alert.
3. If you cannot reach chat or the helpdesk, page the Security on-call via the paging tool. The on-call rotation is in the paging tool's schedule.

## What happens next

1. Security acknowledges your report in the ticket or channel — usually within a couple of hours during the working day.
2. The responder triages: they may ask you to confirm details, check logs, or sit tight while they look. Answer promptly; the faster you reply, the faster they can act.
3. You will get a short summary of what they found and whether they took any action. If the incident turns out to be a false alarm, they will say so plainly.

## If it goes wrong

- Do not investigate on your own. Do not "just take a quick look" at the account, the log, or the machine involved. Your access and your view of the system are not the same as the Security team's, and poking around can destroy evidence or extend the blast radius. If you already looked, say so in your report — that is fine, just be upfront about it.
- If the leaked credential is one you own, rotate it as `eng-docs/security/secrets.md` says. Leave other people's accounts and credentials alone unless Security asks you to act. If you changed a password before reporting, mention that too.
- If the incident involves a customer-visible service, do not post about it in `#general` or `#incidents` until Security has said it is safe to. They will coordinate the external-facing message with the support and customer-success teams.
