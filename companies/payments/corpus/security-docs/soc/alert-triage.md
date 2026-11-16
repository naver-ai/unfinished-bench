# SOC alert triage

**Owner:** Security operations (SOC)  
**Last edited by:** Esther Hayashi (SOC Manager)

## Scope

This runbook covers triage of alerts in the SIEM alert queue, from initial acknowledgement through disposition or escalation. It applies to all SOC analysts on shift across Vilnius and Dublin. The queue is shared; there is no separate queue per site.

## The alert queue

1. Open the SIEM workbench and go to **Alerts → Open**. The default view is sorted by severity, then by oldest first.
2. Every alert must be claimed within **30 minutes** of appearing in the queue. Claim by assigning yourself as the owner in the alert details pane.
3. If the queue has more than 10 unclaimed alerts, or any alert older than 4 hours, notify the SOC channel in `chat` and ask for a second reviewer to help clear it.

## Triage steps

Apply the following in order. Stop at the first step that resolves the alert.

1. **Read the alert metadata.** Check the rule name, the source log type, the asset or account involved, and the time range. If the alert references a merchant or partner, check whether it matches an entity we know from the KYB onboarding tool or the CRM.
2. **Check for known causes.** Look for an existing open incident in `tickets` with similar indicators. Search `#security` and `#soc-platform` for recent discussion of the same rule firing. If a known benign trigger exists (deployments, scheduled jobs, maintenance windows), note it and close as **False positive – known cause**.
3. **Open the underlying events.** Use the alert's event list to view the raw log lines. Confirm the alert rule's condition actually matches the events, and that the events are not from a test source or a replayed feed.
4. **Scope the impact.** Determine what entity is affected: a merchant account, a partner integration, an internal user, or infrastructure. For merchant or partner activity, check the back office for the account state and recent activity.
5. **Decide the disposition:**
   - **False positive** – the alert condition matched but there is no real security concern. Add a short note explaining why.
   - **Benign** – the activity is real but expected (for example, an internal tool scanning a range, a finance operation running a scheduled export). Note the legitimate context.
   - **Suspicious** – real activity with no clear legitimate explanation. Proceed to the escalation steps below.
   - **Confirmed** – activity that clearly matches a known threat pattern or policy violation. Treat as suspicious and escalate immediately.

## Severities and escalation

- **Low** – informational or policy noise. Triage within the shift. Close with a note.
- **Medium** – possible misuse or misconfiguration. Investigate within 2 working hours. If you cannot conclude, discuss with a second analyst before closing.
- **High** – likely compromise, data exfiltration, or abuse of a merchant or partner account. Escalate immediately.
- **Critical** – active compromise or confirmed large-scale exposure. Page the security incident lead right away.

For **High** or **Critical** alerts, page the Security Incident Lead using the paging tool. If the lead is unavailable, page the SOC Manager. Do not wait for shift handover to escalate.

## Closing notes

- Every alert must have a closing note that states the disposition, the basis for the decision, and any follow-up action. Closing without a note is not possible in the tool.
- Follow-up actions (for example, updating a rule, adding an allow condition, requesting a log source change) are tracked in `tickets` and linked to the alert. If a rule fires repeatedly with the same false-positive pattern, file a request for the detection engineers (Beatriz Fonseca) to tune it.
- Alerts tied to an open incident stay linked to that incident and are closed when the incident is closed, unless the incident lead says otherwise.

## Shift handover between Vilnius and Dublin

Handover happens twice a day at the shift change between the Vilnius and Dublin SOC teams. The handover note goes in the `#soc-platform` channel and must cover:

- Open alerts older than one shift, with the current disposition and what remains.
- Any alert that is still under investigation, including what has been tried and what the next analyst should look at.
- Incidents in progress that the SOC is feeding into.
- Rules that are firing more than usual or any log source that is behaving differently.

The incoming analyst should review the handover note and check the queue for anything not mentioned. A handover is not complete until the incoming analyst has confirmed the queue is clear of unclaimed alerts.

## If it goes wrong

- If you claim an alert by accident, unassign and add a note so the next analyst knows it is untouched.
- If you close an alert and then find evidence it was real, reopen it (the tool allows this) and escalate. Tell the SOC lead on shift so they can check whether the same indicators appear elsewhere.
- If the SIEM itself is slow or the queue is not updating, check the SIEM health dashboard and ask the #soc-platform channel for help. Do not assume alerts are not firing because the queue looks empty.
- If you page the incident lead and they do not respond within 10 minutes, page them again and also contact the SOC Manager. The paging tool shows whether the page was acknowledged; an unacknowledged page is treated as a missed page.
