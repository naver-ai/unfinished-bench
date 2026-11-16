# Community forum

**Owner:** Developer relations
**Last edited by:** Rukmini Sethi (Developer Relations Lead)

## Purpose

The community forum is the public place for Gantline users to ask questions about gnt and Gantline Cloud, share workflows, and help each other. This document covers how the Developer relations team moderates the forum, how quickly we respond, and how we route posts to the right place.

## Scope

Applies to all forum spaces: the gnt category, the Gantline Cloud category, and the general discussion area. It does not cover the docs site feedback form or chat channels.

## Moderation

1. Moderators are the Developer relations team plus nominated volunteers from Engineering. The current moderator list lives in the forum’s team page.
1.1. Moderators review the moderation queue at least once per working day, Lisbon time.
1.2. Posts that are spam, abuse, or clearly off-topic for the forum are removed without notice. The author gets a short private message explaining why.
1.3. Posts that are borderline (for example, a support question better suited to the helpdesk, or a feature request that belongs in the issue tracker) are moved rather than deleted. The author is told where the post went.
1.4. If a post names a specific customer org or mentions a paid plan’s details in a way that could identify the customer, the post is edited to remove identifying information before it stays visible.

## Response targets

2. Unanswered questions in the gnt category and the Gantline Cloud category should get a first response within two working days.
2.1. The Developer relations team checks the forum twice a day, mid-morning and mid-afternoon Lisbon time, and again at the end of the Lisbon working day.
2.2. If a question is unanswered after one working day, a member of the Developer relations team posts a brief reply — even if it just says we are looking into it and gives a rough timeline.
2.3. Questions that need Engineering input are tagged with the relevant component (for example `cli`, `editor`, `search`) and a Developer relations engineer pings the owning team in `#engineering` or the team’s channel.
2.4. If a question has been open for five working days with no useful answer, the Developer relations lead raises it in the weekly devrel planning chat.

## Moving bug reports to the issue tracker

3. Posts that describe a reproducible bug in gnt or Gantline Cloud are moved to the issue tracker.
3.1. A Developer relations engineer files the issue in the right repository (the gnt repo for CLI bugs, the cloud repo for platform bugs) and links back to the forum thread.
3.2. The forum post is closed with a comment pointing to the issue number.
3.3. If the report is missing steps to reproduce, the reporter is asked for them before the issue is filed. Reports without reproduction steps are left open in the forum until the reporter provides them.
3.4. Security-sensitive reports are not handled on the forum. The post is removed and the reporter is pointed to the security reporting process in `handbook/security/reporting-an-incident.md`.

## Pointing paying customers to support

4. If a post makes clear the author is on a paid plan (they mention their org name, a seat count, or an invoice), the reply should suggest they open a ticket with the helpdesk for anything that involves their account, billing, or a service outage.
4.1. Do not troubleshoot account-specific issues on the forum. Ask them to open a ticket and note the ticket number if they share it.
4.2. If a post is from someone who works at a company we know is a customer (their email domain matches an org in the admin console), the same rule applies: open a ticket, do not debug on the forum.
4.3. If the poster is clearly on the free plan, handle their question on the forum normally. The helpdesk is still available to them, but the forum is the primary channel.

## Code of conduct

5. The forum’s code of conduct is the same as the one used for the gnt project’s issue tracker and pull requests.
5.1. Violations are reported to the Developer relations team via the forum’s report button or by messaging `#devrel`.
5.2. The Developer relations lead reviews reports within two working days and decides on the response: a warning, a temporary ban, or a permanent ban.
5.3. Bans are logged in the forum’s moderator notes with the reason and the date. The log is reviewed each quarter by the Developer relations team.
5.4. Appeals go to the Developer relations lead. The lead’s decision is final unless the appeal involves a Gantline employee, in which case the People team is consulted.
