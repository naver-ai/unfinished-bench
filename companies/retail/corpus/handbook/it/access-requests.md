# Getting access to systems

**Owner:** IT & service desk  
**Last edited by:** Mehmet Bianchi (Systems Administrator)

This page covers how to request access to Mossgrove systems, who approves what, and what happens when someone leaves.

---

## Requesting access

1. Open the service desk portal and choose **"Access request"** from the request catalogue. The form asks for:
   - your line manager's name and email
   - the system(s) you need (pick from the list — if a system isn't listed, choose "Other" and name it)
   - a short business reason (e.g. "covering AP payment runs while Zainab is on leave", "new starter in stores ops")
   - a start date and, for temporary access, an end date

2. Submit the form. The service desk (Nina or Chloe usually picks these up) will log it against your employee record and route it for approval.

3. Your line manager must approve the request first. For most systems that's all that's needed.

4. For the systems below, the named system owner also has to approve. The service desk will chase them if they don't respond within two working days.

| System | Approver |
|---|---|
| ledgerctl (finance) | Finance Operations team lead |
| sharectl | Data Engineering team lead |
| mailer | Marketing Operations |
| POS back office | Stores Operations team lead |
| CRM | CRM team lead |
| analytics warehouse | Data Engineering team lead |
| feature flag service | Platform & SRE team lead |

5. Once approvals are in, the service desk creates the account or updates your existing one. Standard systems (email, chat, intranet, expenses, HR) are usually done within one working day. Anything needing a security check or involving customer data can take up to five working days.

6. You'll get a confirmation in the tickets tool. If you don't hear anything after five working days, reply on the ticket rather than opening a new one.

---

## Temporary access

- Requests for temporary access (secondments, cover, project work) should be submitted the same way, with an end date on the form.
- The service desk sets the account to expire automatically on that date. If you need it extended, ask your line manager to reply on the original ticket before the expiry date.
- Short-term contractor or agency staff get temporary accounts with the same process; the engagement lead at Mossgrove is responsible for making sure the end date is right.

---

## Leavers

- When someone leaves, their line manager submits a **"Leaver"** ticket in the service desk portal. This triggers deactivation of their accounts across systems — usually within one working day of the ticket being raised.
- If someone is leaving on short notice, call the service desk rather than relying on the ticket. Anika or Mehmet can deactivate core systems immediately.
- For wholesale or stores staff who use the POS back office, the store manager or wholesale team lead should also confirm the leaver's till logins have been removed at their end.

---

## If it goes wrong

- You don't have access but the approvals are done and you've waited the expected time — reply on the ticket and mention Mehmet or Anika. They can see where it's stuck.
- You have access to something you shouldn't — tell the service desk or your line manager right away. Do not try to use it or test it.
- A leaver still has access after they've gone — treat this as an IT security incident and report it via the normal incident channel, then raise the leaver ticket if one hasn't been logged.

---

## Notes

- Access reviews happen each quarter — see the security docs for how those work. If you're a system owner, expect to be asked to confirm who still needs access.
- Don't share logins. Ever. If you need access for someone else, put in a request.
- For access to the GPU lab or model release pipelines, see the ML docs — those go through a different process.
