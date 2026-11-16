# Pitching an engineering post

Engineers at Gantline often have the best material for the blog — a tricky bug in the build farm, a design decision behind a new `gnt` flag, or how we shaved seconds off hosted CI cold starts. The Developer relations team (usually Sara or Rhea) can help you shape that into a post, but the pitch starts with you. This page explains how to bring us an idea we can say yes to quickly.

## The pitch

Send a short message in #devrel or email the devrel team. A good pitch is three or four sentences: what you want to write about, why it matters to other engineers, and roughly how long you think it will take to write. If you have a link to a relevant issue, PR, or internal design doc, include it. We get a lot of pitches that are really just "we shipped X" — that's fine, but tell us what was interesting about building X. If nothing was interesting, it's probably not a post.

We read pitches in the order they arrive and try to respond within a couple of working days. If we think the topic is better suited for the community forum or the docs site, we'll say so and point you at the right place. We maintain a content calendar so we can also tell you when a post would slot in — sometimes we hold a good pitch for a few weeks to line it up with a release.

## Outline and first draft

Once we've accepted a pitch, we'll ask for a short outline — bullet points are fine. This is mainly so we can catch structural issues early. We're looking for a clear narrative arc: what problem you were solving, what you tried, what worked, and what you'd do differently. Pretty much every good engineering post follows that shape.

For the first draft, start it as a draft in the blog CMS (devrel can set one up for you) so we can comment on it directly. Don't worry about prose quality at this stage — get the technical content right and we'll help with the writing. If you're not sure where to start, look at a couple of recent posts on the engineering blog; Sara can point you at ones that came from engineers in your area. We generally expect a first draft within a couple of weeks of the outline being agreed, but life happens — just tell us if it's going to slip.

## Performance numbers

If your post includes performance claims — "this change made builds 30% faster" — we need to be able to back them up. Include the exact commands you ran, the machine or runner pool you used, and the workload. For anything involving our hosted runners, state which instance type and region. We don't publish performance numbers that can't be reproduced by a reader with a Gantline Cloud account and a public repo.

A few practical notes. Run the same measurement at least three times and report the spread, not just the best number. Don't compare against numbers from a different era of the codebase — if you're comparing against a version from two release trains ago, say so explicitly. And if your numbers came from a personal laptop rather than a build host, that's fine but say it; readers care about the environment.

We keep a small set of scripts that devrel uses to verify numbers before publication. Ask Rhea for access if you want to run your measurements through them. It saves a round of review comments later.

## Diagrams

A diagram can make a post much clearer, but it has to be maintainable. For architecture diagrams, draw them in Mermaid and keep the source with the post. We've had too many posts with images that nobody could regenerate when the system changed. If you need help with Mermaid, the docs site has examples, or ask in #devrel.

For screenshots — for example, of the editor or the CLI — keep them tight and crop out anything that isn't relevant. Don't include screenshots of internal dashboards or admin consoles; the reader can't see those and it just raises questions. The style guide has more detail on image formatting.

## Getting code samples right

The most common reason a post gets sent back for another round is a code sample that doesn't match what's actually in `gnt` or the API. Before you submit a draft, run every code snippet you included. For `gnt` commands, use the current release, not a development build. For API examples, hit the real endpoint with a throwaway token — the public API overview in `eng-docs` has the current auth flow.

If a code sample requires a specific version of `gnt` or a specific API version, note that in a comment at the top of the sample. We've published posts that silently assumed a feature that was only in the nightly build, and the comments were not kind. Also, keep samples short — readers will copy them, so they should be runnable in a fresh checkout without needing internal infrastructure. Anything that requires access to our internal runners or the lab won't work for a reader, so either adapt it to something public or cut it.

When you're done, paste the code into a clean workspace and run it start to finish. If the sample is for a language we support in the SDKs, test it against the published SDK, not a local checkout. Sara does a final pass on all code samples before publication, but the earlier you catch problems, the faster the review goes.

## After you submit

The devrel team reviews the draft for technical accuracy and style, then it goes through the normal publishing process — you'll get comments on the draft and we'll iterate until it's ready. Most posts take two or three rounds. Once it's live, we'll post it in #general and you get to bask in the glory. Thank you for writing it.
