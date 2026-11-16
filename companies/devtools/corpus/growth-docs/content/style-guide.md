# Style guide

Owner: Content · Last edited by Sabine Rao

Writing style for the product blog, docs site, changelog, and any customer-facing copy we ship. If a rule here conflicts with what you see in a draft, the rule wins — file a PR if you think it's wrong.

## Plain English

- Write for a developer who is skimming. Short sentences. One idea per sentence.
- Prefer the active voice: "gnt builds the project" not "the project is built by gnt".
- Use "you" for the reader. Use "we" only when Gantline is acting.
- Avoid jargon unless the term is the actual name of a feature (`microVM`, `workspace`, `runner`).
- Spell out acronyms on first use in a document. Exceptions: API, CI, CLI, SSH, HTTPS — everyone in our audience knows these.
- No marketing superlatives. If a feature is faster, say how much faster and on what.
- Humour is fine in the changelog, in small doses. Not in docs or the blog.

## Code blocks and commands

- Every command in docs must run as-is. Nothing left for the reader to fill in by guessing.
- Use `$` for shell prompts in the docs site. In the blog and changelog, omit the prompt unless the line is ambiguous.
- Show output only when it matters. Trim output to the relevant lines and say so: `…` on its own line.
- Flag commands that need elevated permissions or a non-default region.
- When showing edits to existing files, prefer a diff block over "before/after" prose.
- Keep code blocks short enough that a reader can copy the whole block without scrolling on a laptop.

## Numbers

- Use numerals for versions, ports, counts and measurements: `gnt v1.43`, `port 8080`, `12 runners`.
- Spell out numbers below ten in prose: "three regions", "nine services". Exceptions: versions, percentages, and anything the reader might compare.
- Ranges use an en dash: `4–8 GB`. A span of versions uses `..`: `v1.41..v1.43`.
- Currency: `$`, then the figure, no decimals for whole amounts. USD is the default; state other currencies explicitly.
- Times and dates in customer-facing copy follow the reader's locale. In internal drafts, write the date in full — do not rely on a bare numeral like `03/04`.

## Headings

- Sentence case: "Build times after the move" not "Build Times After The Move".
- Keep headings under about six words. If you need more, split the section.
- In docs, one `h1` per page, then `h2` for sections and `h3` for subsections. No deeper nesting.
- In the changelog, each entry gets an `h2` with the version and a short summary. The title should carry the main point, not "Fixes".

## Naming product features

- Use the product name as it appears in the UI and the docs site. If a name changed, update the old reference — do not keep both.
- Capitalise product features (`Hosted runners`, `Code search`, `Cloud workspaces`). Lowercase generic terms (`runner`, `workspace`, `search`).
- Don't coin a new name for a feature that already has one. If you believe a name is wrong, raise it with the owning team before writing.
- Refer to gnt as `gnt` in running text, not "the gnt CLI" on every mention. Use the full form once at first mention.
- Gantline Cloud is the platform. Gantline Inc. is the US entity. Do not interchange them in customer-facing copy.

## Inclusive language

- Use "they" as a singular pronoun. Do not use "he or she".
- Avoid "crash", "kill", "master/slave", "whitelist/blacklist", "sanity check". Use the alternatives already in our docs: "stop", "terminate", "primary/replica", "allowlist/denylist", "confidence check".
- When writing about people, lead with the person, not the condition or role: "a developer who is blind" not "a blind developer".
- Use "email", not "e-mail". Use "login" as a noun, "log in" as a verb.
- Avoid "simply", "just", "obviously" — they read as condescending and add nothing.

## Tone for the changelog

- One entry per change, written as a user-visible outcome: "You can now filter the run list by branch".
- Bug fixes say what was broken and what the fix does. If the fix changes behaviour, say so.
- Do not promise timelines or "coming soon" in a changelog entry. If a release is partial, say what is not included yet.
