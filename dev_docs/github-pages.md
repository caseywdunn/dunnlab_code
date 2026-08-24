# GitHub Pages Site

The `docs/` directory contains the GitHub Pages site for this project, providing user-facing documentation for lab members on installing, using, and contributing to the plugin.

**Important**: `docs/` is for the Jekyll site served to users. It is **not** the `dev_docs/` directory (which is developer reference for working on this repo).

## Configuration

- **Theme**: `just-the-docs` via `jekyll-remote-theme`
- **Config**: `docs/_config.yml`
- **URL**: `https://dunnlab.org/dunnlab_code`
- **Plugin**: `jekyll-remote-theme` (required for GitHub Pages with remote themes)

## Page structure

Each page is a markdown file with YAML frontmatter:

```yaml
---
title: Page Title
nav_order: 3
---
```

`nav_order` controls sidebar ordering (lower numbers appear first).

### Current pages

The chapters are ordered by how widely they apply, narrowing as they go. Keep new pages in the tier they belong to rather than appending them at the end.

| File | nav_order | Tier | Content |
|------|-----------|------|---------|
| `index.md` | 1 | — | Landing page; states the tier structure and where to start |
| `using-ai.md` | 2 | anyone | Responsibility, reviewing generated code, data handling, disclosure, journal and funder policy |
| `quick-reference.md` | 3 | anyone | One-page cheatsheet: setup, working rhythm, permission modes, sessions, tmux |
| `getting-started.md` | 4 | anyone | Recommended stack, installing and verifying Claude Code |
| `claude-intro.md` | 5 | anyone | How Claude Code works: interfaces, working directory, extensibility, effective use |
| `managing-security.md` | 6 | anyone | Permissions, sandboxing, isolation |
| `managing-context.md` | 7 | anyone | Context window, CLAUDE.md, rules, auto memory, skills, plugins |
| `plugin.md` | 8 | anyone | The plugin as an artifact: skills, commands, assets, install and update |
| `example-workflows.md` | 9 | anyone | Step-by-step walkthrough of a project |
| `other-agents.md` | 10 | anyone | The wider agent landscape, AGENTS.md, and serving several agents from one file |
| `yale.md` | 11 | Yale | YCRC clusters and running Claude Code on shared hardware |
| `lab-practices.md` | 12 | Dunn Lab | The reasoning behind our conventions, and data management |

Quick Reference deliberately duplicates commands that appear in later chapters. Keep it to commands and one-line descriptions — the explanation belongs in the chapter it links to, so the two cannot drift far.

Keep this table in sync with the frontmatter. `./scripts/check.sh` verifies that `nav_order` values are contiguous and unique and that every page is linked from `index.md`, but **it does not check this table** — that is on you.

When adding a page, ask which tier it belongs to. Anything institution-specific belongs at 8 or later; anything lab-specific at 9 or later. A page that would need to be deleted before sharing the manual with another group is in the wrong tier.

## Adding a new page

1. Create a markdown file in `docs/` with frontmatter (`title`, `nav_order`)
2. Choose a `nav_order` that places it logically in the sidebar, and renumber the pages after it so the sequence stays contiguous
3. Link to it from `docs/index.md` in the table of contents, and add a row to the table above
4. Push to `main` — GitHub Pages builds and deploys automatically

## Local preview

```bash
./scripts/preview-docs.sh          # serve at http://localhost:4000/dunnlab_code/
./scripts/preview-docs.sh build    # build only, then exit
```

This runs Jekyll in Docker, so no Ruby is needed on the host. The first run installs gems and takes a few minutes; they are cached in a named volume, so later runs start quickly.

GitHub Pages builds this site with its **legacy** builder, which uses the `github-pages` gem — the same gem `docs/Gemfile` pins. So a local build is close to what actually gets published, remote theme included.

If you would rather use a local Ruby:

```bash
cd docs
bundle install    # first time only
bundle exec jekyll serve
```

### Preview before a release

The deployed site is built from `main`, so nothing on `dev` is visible until the release merge. To look at the real HTML first, either run the script above on `dev`, or download the `docs-site` artifact from the `site` CI job on any pull request and open `index.html` locally.

That CI job also *builds* the site on every push and PR, which is the only thing that catches a broken `_config.yml` or a Liquid error in a page — `check.sh` validates frontmatter and links but never renders anything.

Local preview is optional. The site is built and deployed by GitHub Pages' built-in Jekyll build on every push to `main` — there is no workflow file in `.github/`, and the build shows up in the repo's Actions tab as `pages-build-deployment`. If a page renders wrong after a push, check there first.

## Linking conventions

- Internal links use relative markdown paths: `[Getting Started](getting-started.md)`
- External links to the repo use the full GitHub URL
- The `aux_links` in `_config.yml` adds a "GitHub Repo" link to the site header
