# Brand voice and visual style

**Owner:** Brand and communications  
**Last edited by:** Amara Das (Content Editor)

## Tone

- Write plainly. Short sentences, everyday words, no marketing exaggeration.
- Describe what a product or feature does, not how impressive it is. Let the data speak.
- Avoid superlatives like "unmatched," "best-in-class," "revolutionary." If we can't verify it, don't claim it.
- Use active voice. "The analytics API returns flood extents within an hour of capture" not "Flood extents are made available…"
- Be direct about limitations. If a model has a known gap at high latitudes or in dense cloud, say so.
- For customer-facing materials, address the reader as "you." Internal docs can use "we."
- Do not use exclamation marks in customer-facing text. One per page maximum in internal communications.
- Spell out acronyms on first use in any document that leaves the company.
- For US audiences, use US spelling and terms ("modeling," "center"). For EU audiences, UK spelling ("modelling," "centre"). Rotterdam office writes UK English by default.

## Product names

- "Brakwater" is the company name. "Brakwater Geo" appears only in legal documents.
- Product lines: "Flood Monitor," "Crop Monitor," "Soil Monitor," "Analytics API," "Tasking Portal." Capitalise as written.
- The Analytics API is called "the Analytics API" or "our API" — never "Brakwater API."
- The ground sensor network is "the sensor network" in prose, "Ground Sensor Network" in technical docs.
- Do not invent product names or call features "solutions." A product is what we sell; a feature is one capability of a product.
- Version numbers appear only in release notes and API docs, not in marketing copy.

## Map styling and colour ramps

- Basemaps are neutral grey-blue. No satellite imagery as basemap behind vector overlays unless the image itself is the deliverable.
- Flood extents: use the "Brakwater Blue" ramp — sequential blues from #E3F0F7 (low) to #0B3D5C (high). Never use red or orange for water.
- Crop health: green-yellow-red diverging ramp, green = healthy, yellow = stressed, red = critical. Use colourblind-safe palette from the design system.
- Soil moisture: brown-to-blue ramp, dry to wet. Include the scale legend on every map.
- Confidence layers: use opacity, not colour, to show confidence. Full opacity = high confidence.
- All maps need: scale bar, north arrow (unless orientation is obvious), date of imagery, and the coordinate reference system if relevant.
- Do not use rainbow ramps or any ramp that implies a value ordering where none exists.

## Captions and imagery credits

- Every image gets a caption. Captions state what the reader is looking at, where, and when.
- Format: "Flood extent along the Maas near Rotterdam, captured [date]. Source: Brakwater satellite imagery."
- For third-party imagery, credit the provider: "Contains modified {{EO_DATA_PROGRAMME}} data."
- Ground sensor photos credit the sensor network team: "Photo: Brakwater sensor network."
- If an image is illustrative, say "Illustrative" at the start of the caption.
- Alt text is mandatory for any image in digital materials. Describe the content, not the aesthetics.
- Do not crop or recolour a partner's imagery without their written agreement.

## Units

- Metric units are the default: metres, kilometres, hectares, cubic metres per second.
- US agriculture customers get acres, feet, and inches in any customer-facing material produced for the US market.
- Mixing units in one document is a mistake. Pick one system and stick to it.
- Water levels: report in metres above a referenced datum, and name the datum if it is not local mean sea level.
- Soil moisture: report as volumetric water content (percentage) or as a classification (dry/moderate/wet), never as an unnamed index.
- Dates in customer materials use the local format: DD Month YYYY for EU, Month DD, YYYY for US.

## Review and updates

- This document is reviewed each quarter by Brand and communications. Proposed changes go through Amara or Mirela.
- Questions about a specific asset go to #marketing.
- Outdated guidance in this file takes precedence over instinct. If the rule does not fit, raise it in the channel rather than improvising.
