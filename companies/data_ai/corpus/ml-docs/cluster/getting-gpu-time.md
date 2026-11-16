# Getting GPU time

_Owner: ML platform (training cluster and serving)_  
_Last edited by: Bo Vasquez_

**How do I book a reservation for a pretraining run?**

Open a ticket in tickets against the ML platform component and include the number of GPUs, the model size, and the expected duration. The ML platform team reviews requests twice a week and confirms reservations on a first-come, first-served basis, with priority for runs that have a release date committed to a customer. Once confirmed, the reservation is created in the cluster scheduler and you will get the reservation ID to use when submitting the job.

**Why is my job sitting pending?**

Usually one of three things: the reservation you requested is not active yet, the reservation is active but there are not enough free GPUs in the pool because a pre-emption window is open, or the job spec does not match the reservation (wrong GPU type, wrong queue). Check the reservation status in the scheduler CLI with `reservation show`, and look at the job events for a reason string. If the reason says `reservation-not-active`, the job will start automatically when the window opens. If it says `capacity`, wait for the current pre-emption cycle to finish.

**How does pre-emption by reservations work?**

Reservations can pre-empt jobs that are running outside a reservation. When a reservation window opens, the scheduler drains the required GPUs by sending a pre-emption signal to the affected jobs. Jobs that are part of a reservation are never pre-empted by another reservation. Jobs submitted without a reservation are pre-emptible at any time. The scheduler gives a five-minute grace period between the signal and the actual reclaim, so the trainer can checkpoint and exit cleanly.

**What does the trainer do when pre-empted?**

The training harness listens for the pre-emption signal, saves a checkpoint to its run directory on scratch, and exits with a specific exit code. The job is then resubmitted automatically by the scheduler when the reservation window that caused the pre-emption closes, and it resumes from the latest checkpoint. If the checkpoint save fails, the run restarts from the last good checkpoint. Check the run log for `preempted` markers to see how often this happens.

**Is there a way to avoid pre-emption?**

Yes — submit the job under a reservation. That is the only way to get a guaranteed window. If you do not need a full reservation, you can use the `best-effort` flag when submitting, which tells the scheduler to run the job in any free capacity but also to prefer keeping it alive over pre-emptible jobs. It is not a guarantee, but it helps in practice.

**How is per-project quota set each quarter?**

At the start of each quarter, the ML platform team reviews GPU usage from the previous quarter in the scheduler accounting, and the queue wait times. Quota is then set per project based on the average number of GPUs actually used and the number of active reservations. Projects that have not used their quota for two consecutive quarters have it reduced. If you need more than your project quota, open a ticket and the ML platform team will review it with the project lead.

**I used to use `gpu-reserve` to book a slot. Is that still a thing?**

No, that tool was replaced by the reservation system in the scheduler. `gpu-reserve` is no longer installed on the login nodes. Use the scheduler CLI or the ticket flow described above.

**Who do I talk to about quota for a new project?**

Talk to Bo Vasquez; large allocations also go past Hugo Brandsma. For a new project, include an estimate of the number of runs you expect and the typical GPU hours per run.

**What happens if a reservation overlaps with another reservation?**

The scheduler will reject the second reservation request when it is submitted. If you need to extend a reservation, open a ticket and the ML platform team will check whether the extension can be fitted in without displacing another reservation. Overlapping reservations are never allowed.
