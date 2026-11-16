# Test lab overview

The Kessendorf test lab in Reutlingen is the central validation facility for motion controllers, servo drives, direct-drive units, torque transducers and laser encoders. We also support the Telford and Greenville plants with acceptance testing and fault reproduction when their own rigs are not suitable. The lab reports into Engineering, with Rafael Hayashi as Test Lab Lead.

## Benches and their use

**Vibration shaker.** The electrodynamic shaker in the main hall is used for sine and random vibration tests on complete drive units and on instrumented torque transducer assemblies. Typical work is resonance sweeps on DU series rotors, and endurance runs for laser encoder heads that will be mounted on high-speed spindles. Miriam Takahashi owns the vibration schedule and the fixture library. If a fixture is not in the library, ask her before booking — we have had fixtures built that duplicate one already in the cabinet.

**Thermal chambers.** Two chambers are available: a small one for encoder heads and electronics subassemblies, and a walk-in for complete cabinets and drive racks. The walk-in is the one most often requested by firmware for temperature cycling of MC series controllers. Hiroshi Arslan maintains the chamber calibration records and the temperature profiles. The chambers can run unattended only when Hiroshi or Miriam have set up the run and confirmed the profile in the capture server.

**Acoustic room.** The semi-anechoic room is used for NVH measurements on direct drives and on complete test rigs, mainly for noise mapping and for verifying that tonal complaints from customers are addressed. Irene Larsen is the lead for acoustic work, and she carries out most of the measurements herself. The room doubles as a quiet space for listening tests on encoder count stability — book it via the lab calendar and state what you are using it for, because the two uses have different setup times.

**Pressure rig.** The pressure rig is used for static and dynamic pressure testing of transducer housings and seals, mostly for TX series products destined for hydraulic applications. It is operated by Carlos Wagner, who also handles the rig's safety checks at the start of each working day. The rig is not available for customer-owned parts unless the customer has signed the test agreement — Carlos will ask.

**Drive dynamometers.** Three dynamometer cells are in the building: two for DU series direct drives up to 120 Nm, one for servo drive systems with gearboxes. They are used for load testing, efficiency mapping and long-duration soak runs. Lara Park runs the dynamometers and keeps the test logs. The big cell is the one with a pit — if you are booking it, note that access to the pit is restricted to Lara and to maintenance staff with a valid permit.

## Who runs the lab

The lab is staffed by the Test Lab team: Rafael, Hiroshi, Miriam, Irene, Carlos and Lara. Engineering teams book time on the benches themselves, but the lab team performs the actual setup and runs for shaker, chamber and acoustic work. For dynamometer work, engineers may operate the cells under Lara's supervision after a short induction. Test lab owns the equipment and the calibration schedules; Engineering owns the test specifications.

## Run naming

Every run gets an id when the capture starts: a bench prefix and a running number — `VIB-` for the shaker, `TH-` for the thermal chambers, `AC-` for the acoustic room, `PR-` for the pressure rig and `DYN1-` to `DYN3-` for the dynamometer cells (for example `VIB-2231`). The number comes from the capture server, so do not make up your own. Quick checks that are not formal runs are noted in the lab notebook against the booking instead. The run id appears on the capture, in the lab notebook and in the test report. If you run the same setup twice, the second run gets a new id.

## Booking

All bench time goes through the lab calendar, which is visible to Engineering and to the Test Lab team. Book at least one working day ahead for shaker, chamber and acoustic work; dynamometer cells can sometimes be taken the same day if Lara is free. The calendar shows the setup time as part of the booking, so a two-hour shaker run with a one-hour setup is a three-hour slot. If a booking is cancelled, remove it from the calendar the same day so the slot can be reused. The lab calendar is the only place where bench time is agreed — chat messages and hallway conversations do not count.

For long-duration runs (more than eight hours), book the run and the follow-up inspection as two contiguous slots. The inspection is the time the lab team uses to review the capture before the bench is released for the next booking.
