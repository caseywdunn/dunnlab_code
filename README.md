# DunnLab Code

[![checks](https://github.com/caseywdunn/dunnlab_code/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/caseywdunn/dunnlab_code/actions/workflows/checks.yml?query=branch%3Amain)
[![plugin](https://img.shields.io/badge/dynamic/json?url=https%3A//raw.githubusercontent.com/caseywdunn/dunnlab_code/main/.claude-plugin/plugin.json&query=%24.version&label=plugin&color=blue)](CHANGELOG.md)

This repo has two purposes:

- Documenting our best practices, onboarding, and instruction on using AI in our research.
- Shared skills, hooks, and commands for the Dunn Lab. The focus is on Claude Code.

**[View the full documentation site](https://dunnlab.org/dunnlab_code/)**

This repository was written by Casey Dunn with Claude, Anthropic's AI assistant, from the first commit onward. The [full statement](https://dunnlab.org/dunnlab_code/#ai-use) says what was delegated and to which models; the commit history is the detailed record.

## Plugin installation

### Claude Code

Install from the GitHub repository by registering it as a marketplace:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

To update an installation from GitHub, refresh the marketplace and then update the plugin:

```bash
claude plugin marketplace update dunnlab
claude plugin update dunnlab-code@dunnlab
```

Restart Claude Code to use the updated plugin. Auto-update is off by default for third-party marketplaces; you can enable it under `/plugin` → **Marketplaces**.

### Codex

Install from the same GitHub repository:

```bash
codex plugin marketplace add caseywdunn/dunnlab_code
codex plugin add dunnlab-code@dunnlab
```

To update an installation from GitHub, refresh the marketplace snapshot and install the current plugin version:

```bash
codex plugin marketplace upgrade dunnlab
codex plugin add dunnlab-code@dunnlab
```

Start a new Codex session to use the updated plugin. Codex loads the shared `skills/` directory; the Claude-specific slash command and plugin controls below apply only to Claude Code. See the [official Codex plugin documentation](https://developers.openai.com/plugins/build/plugins) for marketplace details.

The [Getting Started](https://dunnlab.org/dunnlab_code/getting-started.html) guide walks through the full setup, including the other plugins we recommend.

For local development installs, updates, and removal in either tool, see [Contributing](dev_docs/contributing.md#working-with-a-local-plugin).

## Using skills and commands in Claude Code

Once the plugin is installed, everything is available automatically — there are no extra activation steps.

- **Skills** load based on context. The `dunnlab-coding-defaults` skill, for example, activates when you write or review code or make a commit. You can also invoke any skill explicitly.
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

- **dunnlab-coding-defaults** — Language, code style, dependency management, testing, and version-control conventions.
- **dunnlab-workflow-design** — Computational workflow design from exploration onward: readable data flow, shared implementation, execution provenance, valid reuse, and reproduction instructions.
- **dunnlab-bioinformatics** — Biological methods, preferred tools and usage details, sequence identifiers, and domain-specific checks.
- **dunnlab-release-cycle** — Development and release process for projects with several contributors or outside users: dev and issue branches, a plan with gates, changelog, and releases.
- **dunnlab-research-lifecycle** — Scientific planning, exploration, selection, validation, and publication handoff; distillation retains the working implementation and closes evidence gaps.
- **dunnlab-new-project** — Minimal repository, environment, and documentation scaffolding, followed by a handoff to the relevant work.
- **dunnlab-specimens** — Specimen and sample metadata with provenance: vouchers, field and tube IDs, collecting data, taxonomy, crosswalks among YPM/LUX, GBIF, iNaturalist, SRA, and ENA, and tools to fetch, build, validate, and export.
- **dunnlab-hpc** — YCRC cluster reference: Bouchet, McCleary, and Misha partitions, storage, SLURM, Snakemake integration, and running coding agents on Bouchet's agent partition.
- **dunnlab-codereview** — Targeted code review and verification using the relevant skill's standards.
- **dunnlab-manuscript** — Manuscript prose style, manuscript repositories with Quarto source, results staged by the analysis repository and synced in, PDF and Word builds, and co-author edits.
- **dunnlab-biblio** — Verified manuscript, data, and software citations, claim support, and BibTeX conventions.

### Commands

- **/dunnlab-check** — Verifies the plugin is loaded and lists available skills.

Full documentation, including onboarding instructions and lab conventions, is on the [Pages site](https://dunnlab.org/dunnlab_code/).
