# Plugin Architecture

This repo is a Claude Code plugin, defined by `.claude-plugin/plugin.json`. When it is loaded — installed from the marketplace, or passed with `--plugin-dir` — Claude Code discovers the `skills/`, `commands/`, and `hooks/` directories automatically.

There is no `claude plugin add` subcommand. <!-- check-ignore --> The ways to load a plugin are `claude plugin install <name>@<marketplace>`, `claude --plugin-dir <path>`, `claude --plugin-url <url>`, and `claude plugin init` for a skills-directory plugin. See the [plugins reference](https://code.claude.com/docs/en/plugins-reference).

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

- **dunnlab-defaults** — Language, code style, dependency management, testing, and version-control conventions.
- **dunnlab-workflow-design** — Computational workflow design from exploration onward: readable data flow, shared implementation, execution provenance, valid reuse, and reproduction instructions.
- **dunnlab-bioinformatics** — Biological methods, preferred tools and usage details, sequence identifiers, and domain-specific checks.
- **dunnlab-lifecycle** — Scientific planning, exploration, selection, validation, and publication handoff; distillation retains the working implementation and closes evidence gaps.
- **dunnlab-new-project** — Minimal repository, environment, and documentation scaffolding, followed by a handoff to the relevant work.
- **dunnlab-hpc** — YCRC cluster reference: Bouchet, McCleary, and Misha partitions, storage, SLURM, and Snakemake integration.
- **dunnlab-devcontainer** — Add an isolated Claude Code development container; workflow design handles preservation of the scientific runtime.
- **dunnlab-codereview** — Targeted code review and verification using the relevant skill's standards.
- **dunnlab-biblio** — Verified manuscript, data, and software citations, claim support, and BibTeX conventions.

### Design principles

- **Description budget**: Skill descriptions share a listing budget of **1% of the model's context window** by default (`skillListingBudgetFraction`). When the listing overflows, Claude Code shortens descriptions starting with the skills you invoke least — names always survive, descriptions may not. Each entry's `description` plus `when_to_use` is separately capped at 1,536 characters. Keep descriptions to one concise sentence with the key use case first, and check the cost with `/doctor`.
- **Body size**: The full skill body loads on invocation and stays in context for the rest of the session. Longer skills consume more context. Aim for completeness without redundancy.
- **Cross-references**: Skills can reference each other by name (e.g., "apply conventions from the `dunnlab-defaults` skill"). They don't need to duplicate shared content.

### Ownership and composition

Each convention has one authoritative skill. A companion references that owner
instead of restating or overriding its policy. Workflow design applies during
exploration as well as distillation; lifecycle determines the evidence needed for
the selected scientific scope. Bioinformatics supplies methods and tool details,
and HPC supplies the execution platform. Scaffolding ends when the repository is
ready for the requested work.

The development path grows evidence around a shared implementation: establish the
question and design safeguards, explore with recoverable runs, select and complete
the retained scope, assess claims and reproduction, then prepare the applicable
publication or release handoff. Code review supplies engineering evidence;
bibliography supplies verified citations. Neither alone establishes scientific
readiness. Publication handoff is conditional lifecycle guidance, not a fifth phase
or a requirement for every notebook. A development container helps build and run
the project; its existence does not establish preservation of the scientific runtime.

Keep substantial conditional details in references: Snakemake organization,
execution provenance, reader documentation, and biological tool recipes. Preserve
existing skill names when narrowing scope so installed invocations remain useful.
A reference to a companion is a routing instruction, not a requirement to load
all companions for every task.

Use these scenarios when evaluating changes to skill boundaries:

| Request | Applicable guidance | Expected boundary |
|---|---|---|
| Explore a small dataset in a notebook | Defaults; workflow design for the analysis path; lifecycle when organizing research | Rerunnable work and decision evidence; no mandatory notebook rewrite or full release process |
| Design a multi-species sequence pipeline | Workflow design + bioinformatics; HPC if Yale execution is needed | General graph/provenance rules and domain choices compose without duplicate pipelines |
| Retain selected exploratory analyses for a report | Lifecycle + workflow design + relevant domain skill | Select configurations and shared code, preserve history, close verification gaps |
| Resume a scaffolded project to implement its plan | Relevant workflow/domain or software guidance | New-project checks unfinished setup only; it does not own the build loop |
| Review a workflow change or propose a design | Review/design skills as relevant | Assess requested artifacts without launching a lifecycle or expensive computation |
| Rename workflow rules or update documentation | Workflow design; targeted review | Verify scope and dependencies; reuse still-valid scientific execution evidence |
| Prepare a manuscript or dataset release for handoff | Lifecycle publication reference + workflow design + bibliography as relevant | Match the final artifact to evidence, preserve a citable version and access route, identify pending deposits without repeating valid computation |

For substantial skill changes, exercise representative scenarios with an
independent agent using small isolated artifacts. Inspect the resulting behavior,
not just whether the skill repeats its own wording. Record any unavailable runtime
checks rather than treating a document review as an end-to-end execution test.

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
