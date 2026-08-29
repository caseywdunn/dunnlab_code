# DunnLab Code

[![checks](https://github.com/caseywdunn/dunnlab_code/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/caseywdunn/dunnlab_code/actions/workflows/checks.yml?query=branch%3Amain)
[![plugin](https://img.shields.io/badge/dynamic/json?url=https%3A//raw.githubusercontent.com/caseywdunn/dunnlab_code/main/.claude-plugin/plugin.json&query=%24.version&label=plugin&color=blue)](CHANGELOG.md)

This repo has two purposes:

- Documenting our best practices, onboarding, and instruction on using AI in our research.
- Shared skills, hooks, and commands for the Dunn Lab. The focus is on Claude Code.

**[View the full documentation site](https://dunnlab.org/dunnlab_code/)**

This repository was written by Casey Dunn with Claude, Anthropic's AI assistant, from the first commit onward. The [full statement](https://dunnlab.org/dunnlab_code/#ai-use) says what was delegated and to which models; the commit history is the detailed record.

## Installation

Register the repo as a marketplace, then install the plugin:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

This pulls the plugin from GitHub and caches it locally. It works anywhere Claude Code runs, including inside dev containers.

The [Getting Started](https://dunnlab.org/dunnlab_code/getting-started.html) guide walks through the full setup, including the other plugins we recommend.

### Loading a local copy instead

To load the plugin from a working copy without installing it — useful while developing it:

```bash
git clone https://github.com/caseywdunn/dunnlab_code ~/repos/dunnlab_code
claude --plugin-dir ~/repos/dunnlab_code
```

This loads the plugin for that session alongside anything already installed; it does not replace them. The flag is repeatable (`--plugin-dir ~/pluginA --plugin-dir ~/pluginB`). If a `--plugin-dir` plugin shares a name with an installed one, the local copy wins for that session. Because it reads from the directory, edits take effect in the next session with no update step.

There is no `--plugin-dir` option for the Claude VS Code extension, but you can run `claude --plugin-dir` in the VS Code terminal.

## Using skills and commands

Once the plugin is installed, everything is available automatically — there are no extra activation steps.

- **Skills** load based on context. The `dunnlab-defaults` skill, for example, activates when you start a new analysis script or set up a project. You can also invoke any skill explicitly.
- **Hooks** run automatically in response to events (none are defined yet).

Plugin skills are namespaced by the plugin, so the full name is `/dunnlab-code:<skill>`. The bare `/<skill>` form also works as long as nothing else has claimed that name.

To confirm the plugin is loaded and see what it provides:

```
/dunnlab-code:dunnlab-check
```

To disable the plugin without uninstalling it:

```
/plugin disable dunnlab-code@dunnlab
/plugin enable dunnlab-code@dunnlab
```

## Updating the plugin

If you installed from the marketplace:

```
/plugin update dunnlab-code@dunnlab
```

Claude Code can also update marketplaces and their plugins in the background after startup, but **auto-update is off by default for third-party marketplaces like this one**. Turn it on per marketplace under `/plugin` → **Marketplaces**, or run the update command above when you want the latest.

If you are loading a local copy with `--plugin-dir`, just `git pull`. Changes are picked up on the next session.

## What's included

| Directory    | Contents |
|-------------|----------|
| `skills/`   | Reusable Claude Code skills for lab workflows |
| `commands/` | Slash commands |
| `hooks/`    | Event-driven automation hooks (none yet) |
| `assets/`   | Shared resources: example HPC `settings.json`, tmux config |
| `docs/`     | GitHub Pages site with setup guides and lab practices |
| `dev_docs/` | Developer reference for working on this repo |

### Skills

- **dunnlab-defaults** — Lab-wide coding conventions: preferred languages, formatting, testing, project structure, and version control practices. The foundational skill the others build on.
- **dunnlab-new-project** — Step-by-step workflow for scaffolding a new project from scratch, with progress that survives `/clear`.
- **dunnlab-hpc** — YCRC cluster reference: Bouchet, McCleary, and Misha partitions, storage, SLURM, and Snakemake integration.
- **dunnlab-bioinformatics** — Sequence analysis conventions: data hygiene, input validation, gene ID handling, and default tools.
- **dunnlab-devcontainer** — Add a `.devcontainer/` configuration for reproducible, isolated Claude Code environments.
- **dunnlab-codereview** — Code review checklist and process.
- **dunnlab-biblio** — BibTeX conventions for manuscripts: entry keys, author lists, title capitalization.

### Commands

- **/dunnlab-check** — Verifies the plugin is loaded and lists available skills.

Full documentation, including onboarding instructions and lab conventions, is on the [Pages site](https://dunnlab.org/dunnlab_code/).
