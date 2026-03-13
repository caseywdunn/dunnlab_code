# GitHub Pages Site

The `docs/` directory contains the GitHub Pages site for this project, providing user-facing documentation for lab members on installing, using, and contributing to the plugin.

**Important**: `docs/` is for the Jekyll site served to users. It is **not** the `documentation/` directory (which is developer reference for working on this repo).

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

| File | nav_order | Content |
|------|-----------|---------|
| `index.md` | 1 | Home page with table of contents |
| `getting-started.md` | 2 | Installation and setup walkthrough |
| `lab-practices.md` | 3 | Conventions for AI-assisted work |
| `data-analysis.md` | 4 | Using Claude Code for data analysis (placeholder) |
| `managing-security.md` | 5 | Permission system and settings.json guide |
| `managing-context.md` | 6 | Context window, CLAUDE.md, and skills |

## Adding a new page

1. Create a markdown file in `docs/` with frontmatter (`title`, `nav_order`)
2. Choose a `nav_order` that places it logically in the sidebar
3. Link to it from `docs/index.md` in the table of contents
4. Push to `main` — GitHub Actions builds and deploys automatically

## Local preview

```bash
cd docs
bundle install    # first time only
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000/dunnlab_code/`.

## Linking conventions

- Internal links use relative markdown paths: `[Getting Started](getting-started.md)`
- External links to the repo use the full GitHub URL
- The `aux_links` in `_config.yml` adds a "GitHub Repo" link to the site header
