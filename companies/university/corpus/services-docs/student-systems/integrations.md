# Student record system integrations

**Owner:** Student Systems  
**Last edited by:** Bianca Russo (Student Systems Analyst)  
**Review cycle:** every two terms, or when a sync fails twice in a working week

## Overview

The student record system ({{STUDENT_RECORD_SYSTEM|code}}) is the source of truth for student data. This note covers the main integrations that consume its data, who looks after each one, and what to check when something stops. It does not cover the research grants system, the HR and payroll system, or the supporter CRM — those have their own integration notes.

## Interfaces

### VLE roster sync

- **Frequency:** every couple of hours, starting just after midnight for Hollins Hill and City, and just after midnight Malaysia time for Kuala Lumpur.
- **Owner:** Student Systems (Ben Barros).
- **What it does:** pushes module enrolments and staff assignments to the VLE. The VLE pulls from the feed, so the sync is one-way.
- **If it fails:** check the roster file in the shared drive first, then the VLE side. The most common cause is a module code change that hasn't been reflected in the VLE's course map. Ben usually spots this within a day, but if the sync has not run for three consecutive cycles, raise a ticket on the IT service desk portal and tag #it-help.

### Timetabling

- **Frequency:** a batch that runs each night.
- **Owner:** Timetabling team (they sit in Registry but the feed is maintained by Student Systems — Imani Yamamoto).
- **What it does:** sends module registrations and room requirements to the timetabling system for the next academic year. The timetabling system returns clash reports, which come back to Student Systems for review.
- **If it fails:** the batch writes a log to the {{STUDENT_RECORD_SYSTEM|code}} file area. The timetabling team will usually notice first because their morning feed is empty. Imani coordinates the rerun; do not rerun the batch yourself without checking the log — duplicate feeds cause double-bookings.

### Library system

- **Frequency:** daily, just after midnight.
- **Owner:** Library systems team, with Student Systems support (Mara Gallagher).
- **What it does:** sends new and withdrawn student records so library accounts are created or closed. Also sends module enrolments for reading list permissions.
- **If it fails:** library staff will see accounts not appearing at the City campus desk. The feed is a simple file drop; check the file is being written and that the library system's pickup folder has space. There was a period when the pickup folder filled up and the sync looked like it was running when it was not.

### Student casework system

- **Frequency:** near-real-time, every quarter of an hour.
- **Owner:** Student Systems (Bianca Russo) and Student Services (the casework team leads).
- **What it does:** sends a read-only view of the student record — programme, mode of study, current module registrations, and any flags that Student Services have asked us to surface. The casework system does not write back to {{STUDENT_RECORD_SYSTEM|code}}.
- **If it fails:** caseworkers will see stale data in open cases. The integration uses an API that was set up by the vendor; if the token has expired, the service account password may also need rotating. Check the service account's last logon before asking the vendor — it is usually that.

### Accommodation booking system

- **Frequency:** twice a day, mid-morning and mid-afternoon UK time.
- **Owner:** Student Accommodation and Student Systems (Mara Gallagher).
- **What it does:** sends offer-holders and continuing students who have accepted a room offer so the accommodation team can see who is eligible for a contract. The booking system sends back occupancy data, which we hold but do not currently use.
- **If it fails:** the accommodation team will raise a ticket. The feed is a CSV export that the accommodation system imports; check the export file for a student who has no programme record — that usually breaks the whole file.

## General notes

- All feeds use the student's {{STUDENT_RECORD_SYSTEM|code}} ID as the key. Do not change the key format without telling the receiving team first.
- When a student is withdrawn, the feeds update automatically within the next scheduled run. There is no manual trigger.
- If a sync has failed for more than one working day, tell Mara before the end of that day. She will decide whether to pause the feed while it is investigated.
- The interface definitions live in the Student Systems shared area, not in this document. Ask the team if you need a copy.

## Loose ends

- The library system feed still uses the old file transfer method that the vendor said they would retire. It works, but we should push them to move to the same mechanism as the casework system.
- The accommodation booking system's occupancy data is not being used anywhere. There was a plan to feed it into the room booking system, but that has not been scoped.
- The VLE roster sync does not include students on the Kuala Lumpur campus if their module is taught in the UK. This has been on the list for a while; the Kuala Lumpur campus registry manager is aware.
