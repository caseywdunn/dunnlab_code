# DunnLab Code — Claude Code Plugin

A shared Claude Code plugin providing skills, commands, and hooks for the Dunn Lab.
Distributed as a plugin via `.claude-plugin/plugin.json`.

## Repo structure

| Directory        | Purpose |
|-----------------|---------|
| `skills/`       | Claude Code skills (each in `<name>/SKILL.md`) |
| `commands/`     | Slash commands (`<name>.md`) |
| `hooks/`        | Event-driven automation (placeholder; plugin hooks go in `hooks/hooks.json`) |
| `docs/`         | GitHub Pages site (Jekyll, just-the-docs theme) — **not** Claude Code documentation |
| `assets/`       | Shared resources: example HPC `settings.json`, tmux config and cheat sheet |
| `dev_docs/`     | Developer docs for this repo — load into context as needed |
| `workshops/`    | Slide decks and workshop material |

## Testing changes locally

```bash
claude --plugin-dir /path/to/dunnlab_code
# then, in-session:
/dunnlab-code:dunnlab-check
```

Run `claude plugin validate . --strict` before opening a PR. After editing a skill, `/reload-plugins` — plugin skills are not detected live.

## Key conventions

- Skills use YAML frontmatter; `description` is what matters, and in a plugin skill `name` sets the last segment of the namespaced command (`/dunnlab-code:<name>`)
- Skill descriptions must be concise — they share a listing budget of ~1% of the context window, and overflow gets descriptions truncated (check with `/doctor`)
- The `docs/` directory is for the GitHub Pages site (user-facing), not for Claude Code context
- The `dev_docs/` directory is for developer reference when working on this repo
- When writing docs, link to the [official Claude Code documentation](https://code.claude.com/docs/en/overview) rather than repeating it

## Documentation

Detailed guides for working on this repo (load as needed):

- `dev_docs/plugin-architecture.md` — How skills, commands, and hooks are structured
- `dev_docs/contributing.md` — How to add or modify skills, commands, hooks, and Pages content
- `dev_docs/github-pages.md` — How the `docs/` Jekyll site is configured and deployed
