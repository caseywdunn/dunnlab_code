---
title: DunnLab Plugin
nav_order: 8
---

# The DunnLab Plugin

The conventions in this manual are also packaged as a Claude Code plugin, so Claude applies them while you work instead of you having to remember them and restate them in every session.

That is the point of the thing. A convention in a document is one somebody has to read and recall; a convention in a skill is one that gets applied. This chapter documents what is in the plugin and how to run it.

You do not need the plugin to use anything else in this manual, and the skills are readable as plain markdown whether or not you install it. If you are at another institution, the parts that assume Yale are `dunnlab-hpc` and the cluster settings example; everything else stands on its own.

## What a plugin contains

| Component | What it is | How it fires |
|-----------|-----------|--------------|
| **Skills** | Instruction sets Claude loads into context when relevant | Automatically when the task matches, or explicitly with `/dunnlab-code:<name>` |
| **Commands** | Slash commands that trigger a specific behavior | You type them |
| **Hooks** | Shell scripts bound to lifecycle events | On the event. None are defined here yet |
| **Assets** | Files distributed alongside, for you to copy | You copy them |

Plugin skills are namespaced, so the full name is `/dunnlab-code:dunnlab-defaults`. The bare `/dunnlab-defaults` also works unless something else has claimed that name.

## The skills

Each is a single markdown file you can read at `skills/<name>/SKILL.md` in [the repository](https://github.com/caseywdunn/dunnlab_code/tree/main/skills). Reading them is the authoritative answer to "what does this actually do" — this table is a map, not a substitute.

| Skill | What it settles |
|-------|-----------------|
| **`dunnlab-defaults`** | The foundational one. Preferred languages and their best practices, dependency and environment management, file naming, project structure, workflow orchestration, testing, and version control. The others build on it. |
| **`dunnlab-new-project`** | A staged workflow for starting a project: define scope, initialize the repo and permissions, write planning documents before any code, then build in reviewable increments. Tracks its own progress in `.claude/new-project-progress.yaml`, so it survives `/clear` and resumes in a later session. |
| **`dunnlab-bioinformatics`** | Sequence analysis conventions: input validation, gene name sanitization, globally unique cross-species gene IDs, paralog resolution, contamination screening, and a default tool for each job. Builds on `dunnlab-defaults`. |
| **`dunnlab-hpc`** | YCRC cluster reference — partitions, storage quotas, SLURM batch templates, GPU inventory, Snakemake integration. Yale-specific; see [Computing at Yale](yale.md). |
| **`dunnlab-devcontainer`** | Scaffolds an isolated container to work in: a standard configuration built on the official Claude Code dev container feature, or a hardened one that adds a default-deny egress firewall. |
| **`dunnlab-codereview`** | The review checklist and process, including how to give feedback that distinguishes blocking issues from nits. |
| **`dunnlab-biblio`** | BibTeX conventions for manuscripts: entry keys, full author lists, title capitalization, and a strict rule against ever guessing a bibliographic field. |

Skills are loaded on demand, so the body of one costs you nothing until it is used. What is always in context is the one-line description of each, which is how Claude decides whether a skill applies — see [Managing Context](managing-context.md#skills) for the budget that governs this.

## Commands

| Command | What it does |
|---------|--------------|
| `/dunnlab-code:dunnlab-check` | Confirms the plugin is loaded and lists the skills it provides |

## Assets

Files in [`assets/`](https://github.com/caseywdunn/dunnlab_code/tree/main/assets) are not loaded by Claude. They are there for you to copy.

- **`settings.json`** — A restrictive Claude Code configuration built for the Bouchet cluster, with a cluster quick reference in its comments. See [Computing at Yale](yale.md#use-restrictive-permissions).
- **`tmux/`** — A shared tmux configuration and cheat sheet for working over SSH, including clipboard support that works without X11 forwarding.

## Installing and keeping it current

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

Then confirm it loaded:

```
/dunnlab-code:dunnlab-check
```

**Updates do not arrive on their own.** Auto-update is off by default for third-party marketplaces like this one, so nothing changes under you — and nothing improves either. To pick up a new version:

```
/plugin update dunnlab-code@dunnlab
```

You can turn auto-update on for this marketplace under `/plugin` → **Marketplaces** if you would rather not think about it.

To switch it off without uninstalling:

```
/plugin disable dunnlab-code@dunnlab
/plugin enable dunnlab-code@dunnlab
```

### Working from a local copy

To run the plugin from a working copy — useful when changing it:

```bash
git clone https://github.com/caseywdunn/dunnlab_code.git
claude --plugin-dir ./dunnlab_code
```

This loads it for that session alongside anything already installed. Edits take effect in the next session, or immediately after `/reload-plugins`. Plugin skills are not picked up live the way personal and project skills are, so that reload is necessary.

## Changing a skill

Skills are markdown. Editing one is editing a text file, and that is deliberate — the barrier to fixing a convention should be low enough that people actually do it.

If a convention is wrong, or you have settled a question the skills do not cover, change it rather than working around it. [`dev_docs/contributing.md`](https://github.com/caseywdunn/dunnlab_code/blob/main/dev_docs/contributing.md) covers the branching model, the checks that run on every change, and the release process. Note that a change only reaches anyone if the version is bumped — the release ritual there explains why.

For building skills of your own, [Managing Context](managing-context.md#adding-skills) covers the format and the tooling for evaluating whether one actually helps.
