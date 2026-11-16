# Passwords and sign-in

Owner: Cloud security. Last edited by Sara Olsen.

## Password manager

- Every account that supports it uses the password manager with generated passwords. No shared passwords, no personal vaults for company accounts.
- The password manager is the only place company credentials are stored. If you keep a credential outside it (spreadsheet, sticky note, personal vault), that's an acceptable-use issue — tell Cloud security and we'll help you move it.
- If you suspect a stored credential has leaked, rotate it from the password manager and open a ticket in the IT service desk.

## MFA

- MFA is required on every service that supports it, and it must be a hardware key. No TOTP apps, no SMS. Rotterdam and Denver both have a small stock of keys — ask the IT service desk if you need one.
- Keys are registered for your corporate account and the customer API console. If you also use a key for personal accounts, keep it on a separate key — don't mix.
- The hardware key is tied to you. Don't lend it, don't leave it in a shared drawer, and don't attach it to a keyring that leaves the office without you.
- If you lose your key: disable it yourself in the IT service desk portal if you can, then request a replacement. Cloud security can revoke it on your behalf if you're locked out. A replacement key arrives via the office mail drop; plan for a couple of working days.
- If you get an MFA push you didn't trigger, decline it and report it in #security or through the incident process. Don't just ignore it — repeated unexpected pushes on the same account mean the credential may already be compromised, and we'll want to rotate it.
- If a push comes from a system you no longer use or an account you don't recognise, treat it the same way: decline, report, rotate.
