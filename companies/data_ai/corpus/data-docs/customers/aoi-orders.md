# AOI orders

**Owner:** Customer success and delivery  
**Last edited by:** Sabine Mishra

## How does a customer place an AOI order?

Customers order via the tasking portal or through their account manager. For recurring monitoring subscriptions, the AOI is fixed at contract signature and any change goes through the CRM as an order amendment. One-off deliveries are entered in the CRM by the Solutions Engineer supporting the customer.

## What happens at intake?

The Solutions Engineer checks the AOI against the imagery catalogue for archive coverage first. If the customer needs fresh capture, the order goes to Imagery acquisition and processing via the tasking portal. Archive-only orders skip tasking entirely.

## Archive coverage vs new tasking — how do we decide?

Three questions: does the AOI fall inside our archive footprint, is the most recent cloud-free pass within the customer's required recency window, and does the resolution meet the use case (flood monitoring, crop health, etc.)? If archive fails any of those, we quote new tasking. Dara Hartmann can advise on whether a satellite pass is likely to succeed for a given AOI before we commit.

## Cloud cover thresholds?

Archive search defaults to 20% cloud cover over the AOI. If the customer's application is flood extent mapping, we can relax that to 30% and let the model handle shadows, but QA will flag any scene where the cloudy area intersects the area of interest. New tasking is accepted up to 30% predicted cloud; if the delivered scene misses that, we retask at no cost once per order.

## What is the turnaround?

Archive deliveries: three working days from order confirmation. New tasking: five working days from the first successful pass, not from order date. If the satellite doesn't get a usable pass within the tasking window, we tell the customer and offer either an extended window or a partial archive delivery. Processing happens in the shared batch pool; large AOIs may take an extra working day.

## How does QA work?

Imagery operations runs an automated QC pass — georeferencing against the catalogue, cloud check, radiometric range. Anything flagged goes to the imagery operations team for a manual look. The customer sees the delivery only after QA has signed off. If QA fails a scene, the order is not marked delivered and the customer is notified through the CRM.

## What status do customers see?

The web app shows: *Order received*, *Feasibility check*, *Tasking scheduled* (if applicable), *Processing*, *QA*, *Delivered*. The status updates automatically from the tasking portal and the warehouse. If an order is stuck in *Feasibility check* for more than two working days, the support team pings the delivery team directly — that shouldn't happen.

## Can a customer change the AOI after ordering?

Small adjustments (a few kilometres) can be done at no cost before processing starts. Anything larger — or if the change pushes the order into a different resolution tier — is a new order. The customer success manager handles the commercial side of that.

## Who do we contact for questions?

Delivery questions go to the customer success and delivery team in the #support channel. Imagery-specific questions (pass predictions, sensor quirks) go to Dara in #imagery-ops. Billing questions go through the normal finance process — the CRM order references the quote, so the FP&A team can pull the numbers from there.
