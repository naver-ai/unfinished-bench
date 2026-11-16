# Gauge and instrument calibration

**Owner:** Quality  
**Last edited by:** Reza Hartmann (Calibration Technician)

All gauges, torque transducers, laser encoders and reference instruments used for product verification or in the calibration lab must be tracked in the calibration database. The database holds the instrument ID, location, calibration interval, next-due date and the certificate number of the last calibration.

## Calibration intervals

| Instrument type | Interval | Calibration location |
|---|---|---|
| TX series torque transducers (working standards) | 12 months | Reutlingen calibration lab (accredited) |
| TX series torque transducers (production floor) | 12 months | Reutlingen calibration lab |
| Laser encoders (reference units) | 24 months | Reutlingen calibration lab |
| Handheld torque wrenches | 6 months | Reutlingen calibration lab |
| Dial indicators and micrometers | 12 months | Reutlingen calibration lab or external service |
| DU series test rigs (integral sensors) | 24 months | Reutlingen calibration lab |
| MC series test fixtures | 24 months | Reutlingen calibration lab |
| Multimeters and electrical references | 12 months | External accredited lab (arranged via Reutlingen) |

Instruments at Telford or Greenville that are due for calibration are returned to Reutlingen via the normal internal logistics route, unless an external lab is already listed for that instrument type in the calibration database. The UK and US plants keep a small stock of calibrated spares so production is not held up while instruments are away.

## Labels and the calibration database

Every instrument has a calibration label showing the instrument ID, the calibration due date and the initials of the technician who last calibrated it. Labels are colour-coded by quarter. A missing or damaged label counts as a nonconformance — log it in the QMS and put the instrument out of use until the calibration database entry is confirmed.

The calibration database is the source of truth. It generates the monthly list of instruments due in the next 60 days, which the calibration team works through. The list is reviewed in the Quality team meeting each month.

## Out-of-tolerance and damaged instruments

If an instrument is dropped, shows signs of damage, or is found out of tolerance during use:

1. Remove it from service immediately and attach a red "Do not use" tag.
2. Raise a nonconformance in the QMS (refer to `ops-docs/quality/nonconformance.md`).
3. The calibration lab at Reutlingen will recalibrate it and issue a certificate.
4. If the instrument was found out of tolerance, the Quality team reviews any product that was measured with it since the last calibration. The review and its outcome are recorded in the 8D.
5. If the instrument cannot be recalibrated, it is scrapped via the normal disposal route and the calibration database is updated.

## Reutlingen calibration lab

The Reutlingen lab is accredited for torque and length measurements. Calibration certificates issued from the lab carry the accreditation mark. Requests for lab capacity go through the lab calendar; the calibration technician team coordinates the schedule. External calibration services are used only for instrument types the lab is not accredited for.

Instruments built into the test lab benches are listed per bench in `ops-docs/test-lab/lab-overview.md`; their calibration is tracked in the calibration database like everything else.
