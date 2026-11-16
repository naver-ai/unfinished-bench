# Reporting a security incident

**Owner:** Cloud security · **Last edited by:** Bianca Patel

If you think something is a security incident, report it. You don't need to be sure. The Cloud security team would rather triage ten false alarms than miss one real incident.

## What counts

- Lost or stolen laptop, phone, or hardware token — including if it was in a bag that went missing
- Someone accessing a system, office, or data who shouldn't have
- A phishing email you clicked, or credentials you entered on a page that wasn't the real sign-in
- A key, token, or password that may have been exposed (for example, pasted into a public repo or chat)
- Malware or unexpected pop-ups on a Brakwater device
- Data that left Brakwater that shouldn't have (check the data classification guide if unsure)

## How to report

1. **Immediately** — if you can't sign in, or the issue involves the password manager or your MFA device, call the IT service desk. Otherwise, post in **#security** with a short description: what happened, when, and what you did after. Do not include secrets or personal data in the message.
2. **If you're not sure** whether it's an incident, post in #security anyway. The on-call security engineer will respond with next steps.
3. **For anything involving a lost device** — ask the IT service desk to trigger a remote wipe if the device holds Brakwater data. Do this before posting if you can.
4. **Keep the original evidence** — don't delete the phishing email, don't clear browser history, don't reboot the machine. Screenshots are fine, but leave the originals in place.
5. **If you're on the batch cluster or pipeline on-call** and see something that looks like an incident while dealing with an unrelated page — report it in #security, then continue with the original issue. Don't wait.

## What happens next

- The security on-call acknowledges in #security and opens a case in the IT service desk. You'll get the case number in the channel.
- A security engineer may ask you a few questions in a thread. Answer what you can; it's fine to say you don't know.
- If the incident involves a customer system or data, Customer success and delivery will be looped in. You don't need to contact the customer yourself.
- For lost or stolen devices: the security engineer will confirm the wipe status, and you'll get instructions for getting a replacement from the IT service desk.
- You'll get a summary when the case closes, usually within a few working days.

## If it goes wrong

- If you can't reach #security (no network, locked out, etc.), call the IT service desk. They have a direct line to the security on-call.
- If the incident is happening live — for example, you're watching someone access a system — don't confront them. Step away from the screen, close the door if you can, and report it.
- Don't sign out of the password manager or change passwords before reporting, unless the IT service desk tells you to. Account recovery is easier when the original state is intact.

## Don't investigate yourself

Do not try to figure out what the attacker did, check logs, or test whether a credential still works. Do not post details of what you think happened in #random or other channels. Report and stop. The Cloud security team handles containment and analysis.
