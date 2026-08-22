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
| `getting-started.md` | 3 | anyone | Recommended stack, installing and verifying Claude Code |
| `claude-intro.md` | 4 | anyone | How Claude Code works: interfaces, working directory, extensibility, effective use |
| `managing-security.md` | 5 | anyone | Permissions, sandboxing, containers |
| `managing-context.md` | 6 | anyone | Context window, CLAUDE.md, rules, auto memory, skills, plugins |
| `plugin.md` | 7 | anyone | The plugin as an artifact: skills, commands, assets, install and update |
| `example-workflows.md` | 8 | anyone | Step-by-step walkthrough of a project |
| `yale.md` | 9 | Yale | YCRC clusters and running Claude Code on shared hardware |
| `lab-practices.md` | 10 | Dunn Lab | The reasoning behind our conventions, and data management |

Keep this table in sync with the frontmatter. `./scripts/check.sh` verifies that `nav_order` values are contiguous and unique and that every page is linked from `index.md`, but **it does not check this table** — that is on you.

When adding a page, ask which tier it belongs to. Anything institution-specific belongs at 8 or later; anything lab-specific at 9 or later. A page that would need to be deleted before sharing the manual with another group is in the wrong tier.

## Adding a new page

1. Create a markdown file in `docs/` with frontmatter (`title`, `nav_order`)
2. Choose a `nav_order` that places it logically in the sidebar, and renumber the pages after it so the sequence stays contiguous
3. Link to it from `docs/index.md` in the table of contents, and add a row to the table above
4. Push to `main` — GitHub Pages builds and deploys automatically

## Local preview

Requires Ruby. `docs/Gemfile` pins the `github-pages` gem set so a local build matches what GitHub deploys.

```bash
cd docs
bundle install    # first time only
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000/dunnlab_code/`.

Local preview is optional. The site is built and deployed by GitHub Pages' built-in Jekyll build on every push to `main` — there is no workflow file in `.github/`, and the build shows up in the repo's Actions tab as `pages-build-deployment`. If a page renders wrong after a push, check there first.

## Linking conventions

- Internal links use relative markdown paths: `[Getting Started](getting-started.md)`
- External links to the repo use the full GitHub URL
- The `aux_links` in `_config.yml` adds a "GitHub Repo" link to the site header
