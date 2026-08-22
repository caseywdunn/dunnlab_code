# Plugin Architecture

This repo is a Claude Code plugin, defined by `.claude-plugin/plugin.json`. When it is loaded — installed from the marketplace, or passed with `--plugin-dir` — Claude Code discovers the `skills/`, `commands/`, and `hooks/` directories automatically.

There is no `claude plugin add` subcommand. The ways to load a plugin are `claude plugin install <name>@<marketplace>`, `claude --plugin-dir <path>`, `claude --plugin-url <url>`, and `claude plugin init` for a skills-directory plugin. See the [plugins reference](https://code.claude.com/docs/en/plugins-reference).

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

Frontmatter `name` is optional for personal and project skills, where the directory name determines the command. In a *plugin* skill it sets the last segment of the command, so `skills/dunnlab-hpc/SKILL.md` with `name: dunnlab-hpc` is invoked as `/dunnlab-code:dunnlab-hpc`.

### Current skills

- **dunnlab-defaults** — Coding conventions, preferred languages, project structure, testing, and version control practices. The foundational skill the others reference.
- **dunnlab-new-project** — Step-by-step workflow for scaffolding new projects. References dunnlab-defaults for conventions.
- **dunnlab-hpc** — YCRC cluster reference: partitions, storage, SLURM, Snakemake integration.
- **dunnlab-bioinformatics** — Sequence analysis conventions. Builds on dunnlab-defaults and dunnlab-new-project.
- **dunnlab-devcontainer** — Scaffolds a `.devcontainer/` configuration.
- **dunnlab-codereview** — Code review checklist and feedback process.
- **dunnlab-biblio** — BibTeX conventions for manuscripts.

### Design principles

- **Description budget**: Skill descriptions share a listing budget of **1% of the model's context window** by default (`skillListingBudgetFraction`). When the listing overflows, Claude Code shortens descriptions starting with the skills you invoke least — names always survive, descriptions may not. Each entry's `description` plus `when_to_use` is separately capped at 1,536 characters. Keep descriptions to one concise sentence with the key use case first, and check the cost with `/doctor`.
- **Body size**: The full skill body loads on invocation and stays in context for the rest of the session. Longer skills consume more context. Aim for completeness without redundancy.
- **Cross-references**: Skills can reference each other by name (e.g., "apply conventions from the `dunnlab-defaults` skill"). They don't need to duplicate shared content.

## Commands

Slash commands are markdown files in `commands/` that trigger specific Claude behaviors.

**`commands/` is a legacy layout.** Custom commands have been merged into skills: a file at `commands/foo.md` and a skill at `skills/foo/SKILL.md` both produce `/dunnlab-code:foo` and behave the same way. Existing command files keep working, but new work should go in `skills/`, which additionally supports supporting files and `disable-model-invocation`. A command file ignores the `name` and `paths` frontmatter fields.

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

Hooks are event-driven scripts that run in response to Claude Code lifecycle events (`PreToolUse`, `PostToolUse`, `SessionStart`, and others).

**Plugin hooks are registered in `hooks/hooks.json` at the plugin root, not in `.claude/settings.json`.** The JSON format is the same as the `hooks` object in a settings file, so a hook can be moved between the two, but a plugin ships its own file. See the [hooks reference](https://code.claude.com/docs/en/hooks).

No lab-specific hooks have been implemented yet. See `hooks/README.md` for the placeholder structure.

## Assets

The `assets/` directory contains shared resources distributed with the plugin:

- **settings.json** — Example Claude Code settings for the Yale YCRC Bouchet HPC cluster. Includes permission rules, cluster quick reference, SLURM templates, and conda workflow guidance. Users can copy or adapt this for their own `~/.claude/settings.json`.
- **tmux/** — A shared tmux setup for working over SSH on cluster login nodes. `tmux.conf` (copy to `~/.tmux.conf`) fixes mouse scrolling and enables system-clipboard copy over SSH via OSC 52; `tmux.md` is the matching cheat sheet.
