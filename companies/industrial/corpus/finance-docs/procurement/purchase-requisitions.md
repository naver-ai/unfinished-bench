# Purchase requisitions

**Owner:** Group purchasing  
**Last edited by:** Dara Doyle (Commodity Manager, Castings)

Questions people actually ask about raising a requisition in the ERP.

---

**How do I raise a requisition?**

Go to the ERP → Purchasing → Requisitions → New. Fill in the item (search the item master first), quantity, need-by date and the cost centre or project. The workflow routes it to the budget holder for approval, then to purchasing. If you get stuck on the approval chain, ask Lotte Mulder.

**When should I use a catalogue item versus free text?**

Always use a catalogue item if one exists. The item master covers all MC and DU series components, TX transducers, standard fasteners, bearings, packaging materials and MRO consumables stocked at Reutlingen, Telford or Greenville. Free text is for one-off items not yet in the master — but expect to be asked why there is no item, and allow extra time for purchasing to validate the supplier and price.

**Which suppliers should I pick?**

Use the preferred supplier list in the ERP. A quick summary:

- **Castings:** Dara Doyle manages the castings frame; if it's a new casting, involve Dara before you raise anything.
- **Electronics:** standard PCB and component suppliers via the electronics commodity team (check the item master for the default vendor).
- **Bearings:** two preferred bearing distributors, one EU-based, one US-based. The ERP will usually default to the right one based on the ship-to plant.
- **Packaging:** Telford and Greenville have local packaging suppliers set up in the system; use those unless the packaging spec says otherwise.
- **MRO:** site-specific MRO suppliers are configured per plant — don't cross-order MRO between sites, it messes up the delivery and the cost centre.

**What lead time should I plan for?**

Standard catalogue parts: two to three weeks. Bearings and electronics: four to six weeks. Castings: eight to twelve weeks from order, plus machining if the casting needs secondary work. If you need tooling (moulds, fixtures, special gauges), plan for twelve to sixteen weeks — tooling quotes usually take a week or two on their own. For anything on a critical path, put the need-by date in the requisition and name the project or order in the header notes.

**What does purchasing need from me to get a quote?**

For a free-text requisition, include:

- A clear description or, better, a link to the drawing or spec in the PLM.
- Quantity and unit of measure.
- The plant it will be delivered to.
- The required delivery date (working day, not a vague "soon").
- Any supplier the requester knows already supplies the part — that speeds things up, but purchasing still runs the commercial check.

For castings specifically, include the pattern or tooling reference if one exists, and whether the drawing revision is current in the PLM.

**Can I contact the supplier directly?**

Only if purchasing has asked you to join the call or meeting. All commercial contact goes through the buyer. Technical questions can go through the plant's engineering contacts, but keep purchasing in the loop.

**What happens after I submit?**

The requisition goes to the budget holder for approval. Once approved, it lands in the purchasing work queue. A buyer will either create a purchase order from it or come back with questions. If the requisition sits longer than three working days without being touched, ping Ingrid Holm or the purchasing coordinator for your site.

**Do I need to attach anything else?**

Only if the item is a capital asset or requires an engineering change. Capital items need the capex approval reference in the header. If the part needs a drawing revision bump, get the change approved in the PLM first — purchasing cannot order to an unapproved revision.

**What about urgent requests?**

Mark the requisition as high priority with the reason in the notes, and tell the buyer directly via chat (#purchasing) — a requisition with a clear reason usually gets picked up the same day.

---

For questions on PO release timing or supplier master changes, see `finance-docs/procurement/po-release.md` and the supplier master data page under finance-docs/ap.
