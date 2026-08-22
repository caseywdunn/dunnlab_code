# Contributing

[![checks (dev)](https://github.com/caseywdunn/dunnlab_code/actions/workflows/checks.yml/badge.svg?branch=dev)](https://github.com/caseywdunn/dunnlab_code/actions/workflows/checks.yml?query=branch%3Adev)

That badge is `dev`, the integration branch — the state of what is queued for the next release. The badge in `README.md` tracks `main`, which is what the lab actually has installed.

How to add or modify skills, commands, hooks, and documentation in this repo.

## Adding a new skill

1. Create a directory: `skills/<skill-name>/`
2. Create `skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`) and instructions
3. Keep the `description` to one concise sentence — it's always in context
4. Reference `dunnlab-defaults` for shared conventions rather than duplicating them
5. Test locally: `claude --plugin-dir /path/to/dunnlab_code`, then invoke it as `/dunnlab-code:<skill-name>`
6. Update `README.md` and `dev_docs/plugin-architecture.md` to list the new skill
7. Run `claude plugin validate . --strict` before opening a PR

## Adding a new command

1. Create `commands/<command-name>.md` with frontmatter (`name`, `description`) and instructions
2. Test locally with `/command-name`
3. Update `README.md` to list the new command

## Adding a hook

1. Create a script in `hooks/` (e.g., `pre-commit-check.sh`)
2. Register it in `hooks/hooks.json` at the repo root — plugin hooks live there, not in `.claude/settings.json`
3. Document it in `hooks/README.md`
4. Test by triggering the relevant event

## Modifying existing skills

- Edit the `SKILL.md` file directly, then run `/reload-plugins` to pick it up. Personal and project skills are detected live, but **plugin skills are not** — this repo's skills need the reload.
- If changing a skill's scope or purpose, update its `description` frontmatter.
- If the change affects how other skills reference it, check cross-references.

## Updating the GitHub Pages site

- Pages live in `docs/` and use Jekyll with the just-the-docs remote theme.
- Each page has YAML frontmatter with `title` and `nav_order`.
- See `dev_docs/github-pages.md` for configuration details.
- Preview locally: `cd docs && bundle install && bundle exec jekyll serve` (requires Ruby; optional)

## Updating the example settings.json

- The HPC settings file is at `assets/settings.json`.
- It uses JSON comment arrays (`_comment_*` keys) since JSON doesn't support comments.
- When updating permission rules, follow the deny > ask > allow priority order.
- Test permission changes by copying to a project's `.claude/settings.json` and verifying behavior.

## Branching model

Three kinds of branch, and the rule is simple: **`main` is always releasable, and nothing lands on it that has not passed.**

| Branch | Purpose | Who merges into it |
|--------|---------|--------------------|
| `main` | Always releasable. What users install and what the docs site serves. | `dev`, at a release |
| `dev` | Integration. Work accumulates here between releases. | feature branches |
| `feature/<short-name>` | One change, one branch. Short-lived. | — |

```
feature/fix-scratch-purge ─┐
feature/add-rules-section ─┼─→ dev ─→ main (release, tagged)
feature/devcontainer-test ─┘
```

Never commit directly to `main`. Never commit directly to `dev` for anything
larger than a typo — branch, then open a PR into `dev`.

Name feature branches for the change, not the person: `feature/bouchet-partitions`,
not `feature/casey-wip`.

### Working on a feature

```bash
git checkout dev && git pull
git checkout -b feature/my-change

# ... work ...

./scripts/check.sh                  # must pass
./scripts/test-devcontainer.sh      # only if you touched dunnlab-devcontainer

git push -u origin feature/my-change
```

Open the PR against **`dev`**, not `main`. CI runs the structural checks on
the PR; they must be green before merge.

### Keeping a branch current

Rebase onto `dev` rather than merging `dev` into your branch, so the history
stays linear and a release diff is readable:

```bash
git fetch origin && git rebase origin/dev
```

If you have already pushed, that needs `git push --force-with-lease`. Use
`--force-with-lease`, never plain `--force` — it refuses if someone else has
pushed to your branch in the meantime.

## Releasing

Merging `dev` into `main` **is** the release. Two things happen the moment it
lands, so treat the merge as the publication event rather than a housekeeping
step:

- **The docs site rebuilds.** GitHub Pages serves from `main`, so every docs
  change on `dev` is invisible to readers until this merge.
- **The plugin becomes available to the lab** — but only if you bumped the
  version. See below.

### The version bump is not optional

Claude Code decides whether to update a cached plugin by comparing the
`version` field. **If you change a skill and don't bump the version, nobody
receives the change** — their cached copy stays put and nothing reports an
error. This is the single most common way a plugin release silently fails.

The version lives in two files and they must agree:

- `.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → `plugins[0].version`

`./scripts/check.sh` fails if they drift, and `claude plugin tag` refuses to
tag if they disagree.

What to bump:

| Change | Bump |
|--------|------|
| Removing or renaming a skill or command, or anything that loosens the permission templates | **major** — `/dunnlab-code:<name>` invocations and settings people have copied will break |
| A new skill, a new command, or substantive new guidance in an existing one | **minor** |
| Corrections, copy edits, link fixes, HPC number updates | **patch** |
| Changes only under `docs/` | none needed — Pages does not read the version — but bumping is never wrong |

### Release steps

From an up-to-date `dev`:

```bash
# 1. Bump the version in BOTH manifests, and add a CHANGELOG entry.
#    Commit that on dev.

# 2. Everything passes.
./scripts/check.sh
./scripts/test-devcontainer.sh     # if the devcontainer skill changed

# 3. Sanity-check the plugin as a user would receive it.
claude --plugin-dir .
#   /dunnlab-code:dunnlab-check    → lists every skill
#   /context                       → skill listing cost looks sane

# 4. Merge to main. Use a merge commit, not a squash, so dev's history
#    survives and the release diff is reviewable.
git checkout main && git pull
git merge --no-ff dev -m "Release 0.4.0"

# 5. Tag. This validates that the two manifests agree before it writes anything.
claude plugin tag . --dry-run      # check what it would do
claude plugin tag . --push         # creates dunnlab-code--v0.4.0 and pushes it

# 6. Push main, then fast-forward dev so the two do not diverge.
git push origin main
git checkout dev && git merge --ff-only main && git push origin dev
```

The `main` badge in `README.md` should go green shortly after the merge. It
reads the workflow's latest run on `main`, so it stays grey ("no status") until
a release has actually run CI there — that is expected on a branch that has
never seen the workflow, not a failure.

### Tell people

**Auto-update is off by default for third-party marketplaces**, which includes
ours. Nobody gets a new version by sitting still. After a release, tell the lab
to run:

```
/plugin update dunnlab-code@dunnlab
```

Anyone loading the repo with `--plugin-dir` just needs `git pull`.

### If a release goes wrong

Do not delete a published tag or force-push `main` — people may already have
installed it. Fix forward: branch from `main`, fix, bump the patch version, and
release again. A bad version that is superseded in an hour is a much smaller
problem than a version number that means two different things.

## Pull request process

1. Create a branch from `main`
2. Make changes and test locally
3. Open a PR with a description of what changed and why
4. After the merge, check the repo's Actions tab — the `pages-build-deployment` run tells you whether the site built
