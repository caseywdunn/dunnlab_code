# DunnLab Code — Claude Code Plugin

A shared Claude Code plugin providing skills, commands, and hooks for the Dunn Lab.
Distributed as a plugin via `.claude-plugin/plugin.json`.

## Repo structure

| Directory        | Purpose |
|-----------------|---------|
| `skills/`       | Claude Code skills (each in `<name>/SKILL.md`) |
| `commands/`     | Slash commands (`<name>.md`) |
| `hooks/`        | Event-driven automation (placeholder for now) |
| `docs/`         | GitHub Pages site (Jekyll, just-the-docs theme) — **not** Claude Code documentation |
| `assets/`       | Shared resources (e.g., example `settings.json` for HPC) |
| `documentation/`| Developer docs for this repo — load into context as needed |

## Testing changes locally

```bash
claude --plugin-dir /path/to/dunnlab_code
/dunnlab-check
```

## Key conventions

- Skills use YAML frontmatter with `name` and `description` fields
- Skill descriptions must be concise — they consume ~2% of context budget
- The `docs/` directory is for the GitHub Pages site (user-facing), not for Claude Code context
- The `documentation/` directory is for developer reference when working on this repo
- When writing docs, link to [official Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) rather than repeating it

## Documentation

Detailed guides for working on this repo (load as needed):

- `documentation/plugin-architecture.md` — How skills, commands, and hooks are structured
- `documentation/contributing.md` — How to add or modify skills, commands, hooks, and Pages content
- `documentation/github-pages.md` — How the `docs/` Jekyll site is configured and deployed
