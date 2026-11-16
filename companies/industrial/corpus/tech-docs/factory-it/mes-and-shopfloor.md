# MES and shop-floor PCs

**Owner:** Factory IT  
**Last edited by:** Ivan Horvath (Factory IT Manager)

## Scope

This covers the MES terminals, line PCs and label printers on the production floors in Reutlingen, Telford and Greenville. The MES itself (application server, database, interface to the ERP) is covered in the MES runbook in the Factory IT share; this page is about the hardware and what to do when it misbehaves.

## Line PCs and terminals

1. All line PCs run the current MES client image. The image is built by Factory IT and deployed via the imaging server. Reimaging takes about 20 minutes per machine.
2. Terminals at the lines are thin clients connecting to the MES terminal server. The terminal server pool is run by IT infrastructure (Alba Fleming); if a thin client won't connect at all, check the network drop first (see step 6 below).
3. Each plant keeps a small stock of spare line PCs and thin clients:
   - Reutlingen: 4 spare thin clients, 2 spare line PCs (in the Factory IT cage, building 2)
   - Telford: 2 spare thin clients, 1 spare line PC (drives plant IT corner)
   - Greenville: 2 spare thin clients, 1 spare line PC (IT room by the shipping office)
4. Spares are imaged and ready to swap. Do not borrow a spare for office use — order a normal PC through the service desk instead.

## When a line terminal fails

1. Ask the operator what they see. Common issues: blank screen, "cannot reach server", or a label printer that stopped responding.
2. If the screen is blank, check the power LED on the thin client or PC. If it is off, check the outlet and the power strip. The strips are labelled per line.
3. If the device powers on but shows a network error, check the wall port. The port is labelled with the line number. Try the adjacent port if there is one — some lines have a spare drop.
4. If the device boots but the MES client errors, try logging off and back on. If that does not help, reboot the device.
5. If a reboot does not fix it, swap in a spare:
   - Disconnect the device, note which port it was plugged into.
   - Connect the spare, log on with the line's shared MES account (credentials are in the Factory IT password vault, item "MES line accounts").
   - Verify the line's label printer responds from the new device.
6. If the device works but the label printer does not, see the printer section below.
7. Log the failure in the service desk portal under category "Shop floor – terminal". Include the line number and what you replaced. Kalani Silva and Emeka Khan monitor these tickets; if a line is down for more than 30 minutes, message them in #reutlingen, #telford or #greenville as appropriate.

## Label printers on the lines

1. Label printers on the lines are networked. Each printer has a static IP that is listed on the small label stuck to the printer's side and in the MES device list (Factory IT share, "line devices").
2. If a printer is not printing, first check the MES client's printer setting — the client sometimes loses the printer mapping after a reboot. The setting is under "Line devices" in the client menu.
3. If the mapping is correct, check the printer's display for errors (paper jam, label roll empty, ribbon low).
4. If the printer shows no error but still does not print, power-cycle the printer (off, wait 10 seconds, on). The printer takes about a minute to come back on the network.
5. If it still does not print, try sending a test page from the printer's web interface (browse to the printer's IP). If that fails, replace the printer with the spare from the plant's stock and raise a ticket for the faulty unit.
6. Label rolls and ribbons are stocked in the plant stores. Reutlingen keeps them in the Building B stores; Telford in the drives line stores; Greenville in the warehouse stores. Order replacements through the normal purchasing channel — do not use the MES spares stock for that.

## If it goes wrong

- If more than one line is affected at the same time, suspect the terminal server or the network, not the individual devices. Call IT infrastructure first.
- If a line PC is physically damaged (liquid spill, impact), tag it and put it in the scrap/repair bin. Do not leave it on the line.
- If you cannot find a spare at the plant, check with the other plants via chat before ordering one — Telford and Greenville sometimes have different revisions of the thin client and the image may not fit.
- Never leave a line without a working terminal. If no spare is available and you cannot fix the device, escalate to Ivan Horvath directly — the line must not run without MES coverage.
