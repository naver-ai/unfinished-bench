# Docs site

**Owner:** Developer relations  
**Last edited by:** Rhea Patel (Developer Relations Engineer)

The public docs live at docs.gantline.dev and are built from the `docs` repository. This page covers how the site is built, how versioning works, and who to talk to when you need something changed.

## Repo layout

The docs repo has one branch per supported gnt minor release (`v1.42`, `v1.43`, etc.) plus a `main` branch that tracks the upcoming release. The `main` branch is the default and is what most contributors work against.

Each branch has:

- `content/` — markdown source files, organised by topic
- `static/` — images and other assets
- `config.toml` — site configuration (nav order, redirects, etc.)

The version selector on the site is driven by which branches exist in the repo. When we cut a new gnt release, release engineering tags it and we create a matching branch in the docs repo.

## Building locally

```sh
git clone git@gantline.dev:docs/docs.git
cd docs
{{JS_PACKAGE_REGISTRY}} install
{{JS_PACKAGE_REGISTRY}} run dev
```

That starts a local preview on `localhost:3000`. The dev server does hot reload, so you can edit markdown and see changes immediately.

## Preview builds on PRs

Every pull request against the docs repo gets a preview build. The build farm runs a job that:

1. Checks out the PR branch
2. Builds the site with the same toolchain as production
3. Publishes the result to a per-PR URL, e.g. `preview-<pr-number>.docs.gantline.dev`

The preview URL is posted as a comment on the PR by the build bot. You need to be on the VPN to view preview builds.

To trigger a rebuild of the preview (for example if you pushed new commits), push an empty commit:

```sh
git commit --allow-empty -m "rebuild preview"
```

## Versioning

When a new gnt release is published, the docs site needs a new version branch. The process is:

1. Wait for the release announcement in #releases
2. Create the branch: `git branch v<major>.<minor> main`
3. Push it: `git push origin v<major>.<minor>`
4. Update the `config.toml` on `main` to mark the new version as the current one

If you're not sure whether a release is imminent, check the release train doc in eng-docs or ask in #devrel.

## Who looks after docs changes

Any employee can open a PR against the docs repo. The Developer relations team reviews docs changes, and the review queue is tracked in the docs repo project board.

If your change is a straightforward fix (typo, broken link, updated command output), tag `@devrel` on the PR and it'll usually be merged within a working day or two.

Substantive changes to the structure of the docs (new section, renaming a page, changing the nav) should be discussed in #devrel first. The team has opinions about information architecture and it's easier to agree before you write 2,000 words.

## If it goes wrong

- **The site is down** — check the status page first, then look at the `docs-site` dashboard. If the build pipeline failed, check the logs in the artifact store. If the site itself is unreachable, page the on-call via the usual process.
- **A preview build didn't appear** — the build bot comments on the PR when it finishes. If there's no comment after a few minutes, check that the CI pipeline actually ran. Sometimes the PR was opened by someone outside the org and the pipeline needs a maintainer to approve it.
- **The version selector shows a wrong version** — someone probably created or deleted a branch without updating `config.toml`. Fix the config on `main` and merge.
- **A page is missing from the nav** — the nav is defined in `config.toml`. Check the `weight` values on the pages in question; if a page isn't listed there at all, it won't show up.

For anything else, ask in #devrel or grab Rhea or Jin in chat.
