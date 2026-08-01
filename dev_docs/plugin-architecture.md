# Plugin Architecture

This repo is a Claude Code plugin, defined by `.claude-plugin/plugin.json`. When registered (via `claude plugin add` or `--plugin-dir`), Claude Code discovers the `skills/`, `commands/`, and `hooks/` directories automatically.

## Skills

Skills are reusable instruction sets that Claude loads into context when relevant.

### File structure

```
skills/<skill-name>/SKILL.md
```

Each `SKILL.md` has YAML frontmatter and a markdown body:

```yaml
---
name: skill-name
description: >
  One-line summary. This text is always in context so Claude knows
  when to invoke the skill. Keep it short.
---

# Skill Title

Full instructions here — loaded only when the skill is invoked.
```

### Current skills

- **dunnlab-defaults** — Coding conventions, preferred languages, project structure, testing, and version control practices. This is the foundational skill that other skills reference.
- **dunnlab-new-project** — Step-by-step workflow for scaffolding new projects. References dunnlab-defaults for conventions.
- **dunnlab-review** — Code review checklist and feedback process.

### Design principles

- **Description budget**: All skill descriptions share ~2% of the context window. Keep descriptions to one concise sentence.
- **Body size**: The full skill body loads on invocation. Longer skills consume more context. Aim for completeness without redundancy.
- **Cross-references**: Skills can reference each other by name (e.g., "apply conventions from the `dunnlab-defaults` skill"). They don't need to duplicate shared content.

## Commands

Slash commands are markdown files in `commands/` that trigger specific Claude behaviors.

### File structure

```
commands/<command-name>.md
```

Frontmatter requires `name` and `description`:

```yaml
---
name: command-name
description: What this command does
---

Instructions for Claude when this command is invoked...
```

### Current commands

- **/dunnlab-check** — Verifies the plugin is loaded and lists available skills.

## Hooks

Hooks are event-driven scripts that run in response to Claude Code events (e.g., pre-commit, post-file-create). They are registered in `.claude/settings.json` under the `hooks` key.

No lab-specific hooks have been implemented yet. See `hooks/README.md` for the placeholder structure.

## Assets

The `assets/` directory contains shared resources distributed with the plugin:

- **settings.json** — Example Claude Code settings for the Yale YCRC Bouchet HPC cluster. Includes permission rules, cluster quick reference, SLURM templates, and conda workflow guidance. Users can copy or adapt this for their own `~/.claude/settings.json`.
- **tmux/** — A shared tmux setup for working over SSH on cluster login nodes. `tmux.conf` (copy to `~/.tmux.conf`) fixes mouse scrolling and enables system-clipboard copy over SSH via OSC 52; `tmux.md` is the matching cheat sheet.
