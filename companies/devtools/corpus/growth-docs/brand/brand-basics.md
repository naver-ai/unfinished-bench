# Brand basics

**Owner:** Design  
**Last edited by:** Dmitri Delgado

## Name and spelling

- [ ] The company name is **Gantline Software, Lda.** in Portugal and **Gantline Inc.** for US customers. Use "Gantline" in prose.
- [ ] The CLI is always **`gnt`** — lowercase, code font, never "GNT" or "Gantline CLI" unless it's the first mention in a doc.
- [ ] The hosted platform is **Gantline Cloud** — capital G, capital C, never "Gantline cloud" or "the Cloud".
- [ ] Use "Gantline Cloud admin console" for the admin UI; "admin console" is fine after first mention.
- [ ] Refer to our offices as **Lisbon** and **Portland** — no "HQ" unless talking to an outside audience.

## Logo

- [ ] Use the logo files from the brand folder Design shares — those are the only ones approved.
- [ ] Clear space: keep at least the height of the "G" on all sides.
- [ ] Minimum width: 24 px on screen, 12 mm in print.
- [ ] On dark backgrounds use the white version; on light backgrounds use the dark version. No other color variants.
- [ ] Don't stretch, rotate, add effects, or put the logo on a photo without asking Design.
- [ ] The favicon and app icons use the mark only — don't swap in the full lockup.

## Colours

- [ ] Primary: **Gantline Indigo** `#3B35E0`. Use for links, buttons, and primary actions.
- [ ] Secondary: **Slate** `#1E293B` for headings and body text on light backgrounds.
- [ ] Backgrounds: **Cloud White** `#F8FAFC` for docs and marketing pages; **Ink** `#0F172A` for dark mode and terminal themes.
- [ ] Accent: **Signal Green** `#16A34A` only for "running", "passed", "available" statuses. Don't use it decoratively.
- [ ] Error/danger stays **`#DC2626`** — don't invent a new red.
- [ ] Colour contrast must meet WCAG AA for text. When in doubt, ask Design.

## Terminal-style screenshots

- [ ] Use the **Gantline Dark** terminal theme (Ink background, Cloud White text, Signal Green prompt) for `gnt` output.
- [ ] Pick a readable mono font — the one in Design's terminal theme file is preferred.
- [ ] Show real commands and output. Don't fake success states or hide errors that would naturally appear.
- [ ] Keep the window chrome minimal — no window buttons or title bars unless the context needs them.
- [ ] Crop to the relevant output; don't include the whole scrollback.

## Tone for developer audiences

- [ ] Write like an engineer talking to an engineer: direct, specific, no marketing fluff.
- [ ] Use "you" — "you can run `gnt build`" — not "the user" or "developers".
- [ ] Show commands and flags in code font; use full flag names (`--target`) in docs, short flags are fine in examples.
- [ ] Don't claim speed or reliability numbers unless they're from our metrics dashboards — link to the dashboard instead.
- [ ] When referencing open source, link to the repo or the docs site, not to a search.
- [ ] If a feature is in beta or behind a flag, say so. Don't imply general availability.
- [ ] For anything destined for a blog or external post, also read growth-docs/content/style-guide.md before writing.
