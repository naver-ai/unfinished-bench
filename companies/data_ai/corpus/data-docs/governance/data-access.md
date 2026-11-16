# Requesting access to data

**Owner:** Data governance and open data  
**Last edited by:** Clara Bianchi (Head of Data Governance)

This page covers how staff get read access to a dataset or warehouse schema. Write access and table changes are covered separately in the data catalogue and the warehouse docs.

## How to request access

1. Open the data catalogue and find the dataset or schema you need. Each entry lists the dataset owner and the access group(s) that already exist.
2. Select **Request access** on the dataset page. You will be asked for:
   - the access group you want (or "new group" if none fits),
   - the reason (project, customer, or ongoing monitoring subscription),
   - how long you need it (default is 12 months; shorter is fine).
3. The request goes to the dataset owner for approval. The owner can approve, reject, or ask for more detail. If the owner does not respond within three working days, ping the data governance team in #data-governance.
4. Once approved, you will be added to the access group automatically and the group membership is applied to the warehouse or object store within the hour. You will get a notification in the data catalogue and a confirmation email.

## Access groups

- Access is granted through named groups, not individual grants. The group name should describe the use, for example `wh-read:flood-metrics:operations` or `imagery:tasking-orders:customer-success`.
- Groups live in the access control system and are referenced in the warehouse grants and the object store policies. Do not create ad-hoc grants outside a group.
- If you need a new group, request it via the same flow and mention "new group" in the reason. The dataset owner creates it with the data governance lead's review.
- Group memberships are visible to the dataset owner and to data governance. If you change teams or leave Brakwater, your manager or the IT service desk will remove you; you do not need to do anything.

## Contractors and temporary staff

- Contractor access is always time-limited. The request form requires an end date, and the access group is set to expire automatically.
- Extensions are possible: ask the dataset owner to extend the group before it lapses. If it lapses, you will need a new request.
- Contractor accounts are tied to the person, not shared. If a contractor needs access on behalf of a team, the team lead should request it and note the contractor's name in the reason.

## Quarterly review of groups

- Data governance reviews all access groups each quarter. The dataset owner gets a list of their groups and members and confirms whether each membership is still needed.
- If a member no longer needs access, the owner removes them during the review. If the owner does not respond, the group is flagged in #data-governance and access is paused after two reminders.
- The review also catches groups that have no active members; those are retired and the warehouse grants cleaned up.

## If it goes wrong

- You do not have access but were approved: check the data catalogue request status first. If it says approved but you still get permission errors, wait an hour and try again. If it still fails, post in #data-governance with the dataset name and the group.
- You were added to the wrong group or a group is too broad: tell the dataset owner or data governance as soon as you notice. They will adjust the membership and, if needed, tighten the group's scope.
- Access was removed but you still need it: re-request via the catalogue and explain why the previous request was not sufficient. Do not ask someone to grant access directly without a catalogue request.
- You see a group that looks wrong (people who left, or a scope that does not match the name): flag it in #data-governance rather than changing memberships yourself.
