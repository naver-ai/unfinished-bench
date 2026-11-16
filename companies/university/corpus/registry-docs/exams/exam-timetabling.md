# Exam timetabling

**Owner:** Examinations & Assessment  
**Last edited by:** Ivan Petrov (Registry Officer (Examinations & Results))

This note covers how the exam timetable is built for each assessment period, how clashes are checked, how rooms are allocated, and how the timetable gets published.

## Building the timetable

1. At the start of each assessment period planning cycle, the Examinations & Assessment team pulls the list of modules with exams from the timetabling system. The student record system supplies expected cohort sizes per module from current enrolments.

2. Exams are scheduled in two windows per academic year: the January assessment period and the May–June assessment period. A small number of resit exams run in the August period.

3. Open the timetabling system and select **Assessment Period** → **Create New Session**. Name the session using the period and year, e.g. `January Assessments`.

4. Use the **Auto-schedule** function with these parameters:
   - Exam duration from the module's approved assessment plan
   - Two sittings per day: one in the mid-morning and one in the early afternoon
   - No exam to start in the late afternoon
   - At least one clear day between exams for the same student

5. The system will produce a first draft. Review it in the **Clash Check** view. The system flags any student with two exams in the same sitting, or exams on consecutive sittings without a break.

## Clash checks

1. Run the clash report from the timetabling system: **Reports** → **Clash Report**.
2. Export to the student record system and cross-check against the **Examination Entries** list. The student record system is the authoritative source for who is actually entered for each exam.
3. Where a clash is identified, resolve it by:
   - Moving one exam to a different sitting where room capacity allows
   - For students with a clashing pair that cannot be moved, arrange an **overlapping exam** with separate invigilation in the same hall
   - A clash that affects more than five students should be escalated to Alice Aoki before any individual arrangements are made
4. Re-run the clash report after any change. The exam timetable is not considered final until a clean clash report has been produced.

## Room allocation

1. The timetabling system pulls available rooms from the room booking system. Exam rooms are limited to spaces on the Hollins Hill campus, plus the City campus hall for larger sittings.
2. Room capacity is set in the room booking system and includes the reduced seating for exam layouts. Do not override these figures.
3. The Kuala Lumpur campus runs its own timetable from the same system, using rooms in the KL building. Aldercombe Estates Services Ltd needs at least three working days' notice if additional rooms are required at either UK campus.
4. For each sitting, allocate rooms in the timetabling system using **Room Assign** → **Auto Allocate**. Check the resulting seating numbers against expected attendance. Where attendance is within 10% of capacity, keep the allocation but flag it in the session notes.

## Alternative arrangements

1. Disability support plans are held in the student casework system. The Examinations & Assessment team receives a summary report from Student Services ahead of each assessment period.
2. Enter the required adjustments into the timetabling system under **Candidate Adjustments**:
   - Extra time: add to the exam duration in the system. The system extends the end time automatically.
   - Rest breaks: add a rest break flag. Invigilators are briefed separately on how these work.
   - Separate room: the system allocates the student to a smaller room with its own invigilator. The Student Hub team books these rooms through the room booking system.
3. The timetabling system applies adjustments when generating the individual candidate timetable.
4. If a student requests an adjustment after the timetable has been published, they should contact the Student Hub. Marcus Bell's team will pass the request to Examinations & Assessment. We will only change the timetable where the student record system shows an approved support plan.

## Publishing

1. Once the timetable is confirmed, generate the PDFs from the timetabling system: **Publish** → **Candidate Timetables**.
2. Upload each student's personal timetable to the student record system. Students see their timetable on the student portal once it is marked **Published** in the system.
3. Also publish the master timetable on the Registry pages of the university website. The Comms team should be notified so they can link to it from the student news feed.
4. The timetable goes live five working days before the first exam of the period. Students are told the publication date at the start of the assessment period via the VLE announcements.

## If it goes wrong

- **Clash report fails to run:** Check that the timetabling system and the student record system are both showing the same assessment period. The integration between the two runs on a scheduled basis; if the report is stale, re-sync from the student record system before re-running.
- **Room double-booked:** The room booking system may show a room as available while the lettings system holds it for an external booking. Contact the Estates team via the estates helpdesk to release the room. Do not swap rooms without updating the timetabling system first.
- **A student missing from the clash report:** Check that their module enrolment is current in the student record system. If the enrolment is correct but the exam entry is missing, contact the relevant faculty office to confirm the entry, then add it manually in the timetabling system.
- **Published timetable needs a change:** Any change after publication must be approved by Alice Aoki and the Academic Registrar's office. The student record system will send a notification to affected students. Keep a note of the change in the session file in Registry's shared folder.
