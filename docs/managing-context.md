---
title: Managing Context
nav_order: 9
---

# Managing Context

An agent only knows what its harness puts in front of it. This chapter is about supplying the right standing instructions, task-specific guidance, and project documentation without filling the context window with noise.

Most complaints that an agent "forgot" something or "ignored" an instruction are context problems, and most of them are fixable.

## What is the context window?

Every agent session has a finite context window: the messages, responses, file contents, instructions, and tool outputs that fit in working memory. When a conversation grows long, older content may be compressed or dropped to make room. The agent can then lose track of earlier instructions or decisions, or re-read files it already saw.

Managing context well means giving the agent the right information at the right time without filling the window with noise. The products expose similar concepts under different names:

| Mechanism | Claude Code | Codex |
|---|---|---|
| **Project instructions** | `CLAUDE.md` and `.claude/rules/` | Layered `AGENTS.md` files |
| **Personal instructions** | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| **Remembered session context** | Auto memory and session history | Session history and memories |
| **Task-specific guidance** | Skills and plugins | Skills and plugins |

Claude Code's `/context` shows what loaded and what it cost. Codex's `/status` summarizes the active session, while its layered `AGENTS.md` files remain the durable, inspectable source of project guidance.

### Starting with fresh context

When a conversation gets long or you switch tasks, start a new session or use the harness's context-reset command. In Claude Code, `/clear` drops the conversation and reloads the standing instructions. The important habit is product-independent: do not carry an old task's dead ends into a new one.

## Agent instructions

Coding agents read a file of standing instructions at the start of every session — build commands, coding conventions, architectural decisions, project-specific rules — so you don't have to repeat yourself.

There are two filenames for the same idea. Codex and many other agents read `AGENTS.md`; Claude Code reads `CLAUDE.md`.

**Create both, from the start.** Put the actual content in `AGENTS.md`, and make `CLAUDE.md` a single line:

```markdown
@AGENTS.md
```

That is the whole file. Claude Code expands the import at session start, so it loads exactly what every other agent loads, and you maintain one file rather than two that drift apart.

{: .note }
The two-file convention makes neither harness primary: `AGENTS.md` is the shared source of truth and `CLAUDE.md` is the compatibility import Claude Code requires. [Coding Agents](other-agents.md#serving-both-from-one-file) explains the implementation.

The product-specific details below use Claude Code's filenames because its import is the extra compatibility layer. The general rules—keep instructions short, version them, and point to deeper documentation—apply equally to Codex's `AGENTS.md` hierarchy.

### Where to put them

| Location | Scope |
|----------|-------|
| Managed policy (e.g. `/etc/claude-code/CLAUDE.md`) | Organization-wide; cannot be excluded |
| `~/.claude/CLAUDE.md` | Personal preferences, applied to all projects |
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project-level, committed to git |
| `./CLAUDE.local.md` | Personal, project-specific; add to `.gitignore` |

Claude also discovers CLAUDE.md files in parent directories (loaded at startup) and subdirectories (loaded on demand when you work in those directories). Everything discovered is concatenated rather than overriding, ordered from the filesystem root down, so the file closest to where you launched Claude is read last.

A CLAUDE.md can pull in other files with `@path/to/file` syntax. Imports are expanded at launch, so this helps organization but does not save context — the imported text is loaded either way. To reference a path without importing it, wrap it in backticks.

### Keep it short

CLAUDE.md content is loaded into the context window at session start. Longer files consume more of your context budget and reduce Claude's adherence to instructions. The [official guidance](https://code.claude.com/docs/en/memory) targets under 200 lines, and a stricter house limit is worth considering — this lab holds to 100. If you need more detail, put it in a [rule](#rules) or point Claude to where it can find the information rather than including it inline:

```markdown
## Architecture
See `docs/architecture.md` for the full system design.

## API conventions
See `src/api/README.md` for endpoint patterns and error handling.
```

This way Claude loads the detailed context only when it's relevant to the current task.

### What to include

- Build, test, and lint commands
- Language and framework conventions
- Naming conventions and file organization
- Pointers to files with additional context (as shown above)
- Common workflows and gotchas

Use `/context` to see which CLAUDE.md files actually loaded in the current session — `/memory` lists the locations and lets you open them, but `/context` is what shows you what Claude received.

In a large monorepo, `claudeMdExcludes` in your settings skips ancestor CLAUDE.md files from other teams.

For full documentation, see the [official CLAUDE.md reference](https://code.claude.com/docs/en/memory).

## Rules

When project guidance outgrows a 100-line CLAUDE.md, the answer is usually `.claude/rules/` rather than a longer CLAUDE.md. Rules are markdown files, one topic each, discovered recursively:

```
.claude/
├── CLAUDE.md
└── rules/
    ├── snakemake.md
    ├── plotting.md
    └── hpc.md
```

A rule with no frontmatter loads at launch, at the same priority as `.claude/CLAUDE.md`. **A rule with a `paths:` field loads only when Claude touches a matching file** — which is what makes this worth doing:

```markdown
---
paths:
  - "scripts/**/*.py"
---

# Analysis scripts

- Every script takes `--input` and `--output`; never hardcode paths.
- Write intermediate files to `data/processed/`, never back into `data/raw/`.
- Log to `logs/{script_name}.log` rather than printing to stdout.
```

That guidance costs nothing until Claude opens a file under `scripts/`. Detailed conventions can live in the repo without being paid for in every session.

Personal rules go in `~/.claude/rules/` and apply to every project on your machine. The directory supports symlinks, so a shared set of rules can be linked into several repos.

## Auto memory

Separately from anything you write, Claude keeps its own notes across sessions — your working preferences, corrections you have given it, and project context it cannot derive from the code. These live in `~/.claude/projects/<project>/memory/`, with a `MEMORY.md` index whose first 200 lines (or 25 KB) load at the start of every session; the topic files are read on demand.

It is on by default. Browse and edit what it has saved with `/memory`, which also has the toggle. To turn it off for one project:

```json
{
  "autoMemoryEnabled": false
}
```

Or set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` for all of them.

**Auto memory is machine-local and is not in version control.** It is not a substitute for CLAUDE.md, rules, or `dev_docs/` for anything a collaborator — or you on a different machine — needs to know. Treat it as convenience, not documentation.

## Skills

Skills are markdown files that extend Claude with reusable, task-specific instructions. Unlike CLAUDE.md (which is always loaded), skill content is injected into context only when the skill is invoked — either by you or by Claude when it determines a skill is relevant.

### How they work

Each skill has a short **description** that is always present in context (so Claude knows what's available) and a full **instruction body** that loads only on use. This keeps context lean until you actually need the skill.

### Invoking skills

- Type `/skill-name` to invoke a skill directly
- Claude can also invoke skills automatically when it determines one is relevant to your request (unless the skill opts out with `disable-model-invocation: true`)

### Viewing loaded context

Use `/context` to see the size of the skill listing, and `/doctor` for an estimate of which skills contribute most to it.

Skill descriptions share a listing budget of **1% of the model's context window** by default. When the listing overflows that budget, Claude Code does not drop skills — every skill name stays available. It **shortens descriptions**, starting with the skills you invoke least, which can strip the keywords Claude needs to match a request to the right skill. Each entry's `description` is separately capped at 1,536 characters.

If you have enough skills to hit this, raise the budget with `skillListingBudgetFraction` (e.g. `0.02` for 2%), or trim the descriptions themselves, putting the key use case first.

### Adding skills

Skills live in a directory containing a `SKILL.md` file with YAML frontmatter:

```
my-skill/
├── SKILL.md          # Required: frontmatter + instructions
└── reference.md      # Optional: supporting files
```

The `SKILL.md` frontmatter defines metadata:

```yaml
---
description: One-line summary of what this skill does, and when to use it
---

# Instructions

Your skill instructions here...
```

`description` is the only field that really matters — it is what Claude reads to decide whether the skill applies. For a personal or project skill the directory name becomes the command, so `name` is optional; in a plugin skill it sets the last segment of the namespaced command. Add `disable-model-invocation: true` for skills you want to trigger yourself and never have Claude start on its own.

Skills can be added at three levels:

| Location | Scope |
|----------|-------|
| `~/.claude/skills/<name>/SKILL.md` | Personal, all projects |
| `.claude/skills/<name>/SKILL.md` | Project, committed to git |
| `<plugin>/skills/<name>/SKILL.md` | Distributed via plugin |

### Updating skills

Edit the `SKILL.md` file directly. Personal and project skills are picked up automatically, with no restart. **Skills that come from a plugin are not** — run `/reload-plugins` after editing one.

Note also that once a skill has been invoked, its content stays in context for the rest of the session. Claude does not re-read the file on later turns, so write guidance that should hold throughout a task as standing instructions rather than one-time steps.

For full documentation, see the [official skills reference](https://code.claude.com/docs/en/skills).

### Creating and evaluating skills

The **skill-creator** plugin, from the official Anthropic marketplace, provides a structured workflow for building skills and measuring whether they actually help:

```bash
claude plugin install skill-creator@claude-plugins-official
```

It operates in four modes — **Create**, **Eval**, **Improve**, and **Benchmark** — backed by separate agents that run a skill against eval prompts, grade the outputs against expectations, compare two versions blind, and suggest changes. Invoke it and describe what you want:

```
/skill-creator Evaluate the skill at skills/my-skill/SKILL.md
```

The core idea, whatever the interface details: each test prompt is run **twice**, once with your skill and once without. Comparing the two is the only way to know whether the skill is doing anything.

#### What a benchmark tells you

The benchmark highlights three things:

- **Discriminating checks** — pass with the skill and fail without it. These are the ones that measure what the skill adds. A project scaffolding skill might reliably produce `CLAUDE.md` and `dev_docs/overview.md` while the baseline never does.
- **Non-discriminating checks** — pass in both conditions. They validate correctness but don't justify the skill's existence. If *every* check is non-discriminating, the skill is not earning its context cost.
- **Cost** — skills increase token usage and runtime. Weigh that against what they add.

Once the content is settled, the same tooling can tune the `description` for triggering accuracy: generate should-trigger and should-not-trigger queries, then refine until it fires on the right ones and stays quiet on the rest.

## Plugins

Plugins are packages that bundle skills, commands, and hooks for distribution. While you can add skills individually to a project, plugins let you install a curated set from a **marketplace** — a catalog of plugins hosted on GitHub or another git provider.

### Marketplaces

A marketplace is a git repository containing a `.claude-plugin/marketplace.json` file that lists available plugins. There are two kinds:

- **Official Anthropic marketplace** (`claude-plugins-official`) — available automatically, browsable via `/plugin`
- **Third-party marketplaces** — any GitHub repo (or other git host) with a `marketplace.json`, added manually

To add a third-party marketplace:

```bash
/plugin marketplace add owner/repo
```

This works with GitHub, GitLab, Bitbucket, or any git URL. You can also add a local path for development.

### Hosting your own marketplace on GitHub

Any GitHub repository can serve as a marketplace. The minimum structure is:

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── my-plugin/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── my-skill/
                └── SKILL.md
```

The `marketplace.json` lists each plugin with a name and source:

```json
{
  "name": "my-marketplace",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What this plugin does",
      "version": "1.0.0"
    }
  ]
}
```

Plugin sources can be relative paths (for monorepos), GitHub repos, git URLs, or npm packages. See the [official marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces) for the full `marketplace.json` schema and source types.

Run `claude plugin validate <path>` before publishing; add `--strict` to treat warnings as errors.

### Installing plugins

1. Run `/plugin` to open the plugin manager
2. Browse the marketplace and select a plugin to install
3. Claude Code copies the plugin to a local cache at `~/.claude/plugins/cache/`

You can also install via the CLI:

```bash
claude plugin install plugin-name@marketplace-name
```

For team projects, you can pre-configure marketplaces and plugins in `.claude/settings.json` so they're available to all contributors.

### Auto-updates

Auto-update behavior depends on the marketplace type:

| Marketplace | Auto-update default |
| -------- | -------- |
| Official Anthropic | Enabled |
| Third-party | Disabled |

When auto-update is enabled, Claude Code checks for new versions at startup and updates installed plugins automatically. If updates are found, you'll be prompted to run `/reload-plugins` to apply them.

The `version` field in a plugin's `plugin.json` determines whether an update is needed — if code changes but the version isn't bumped, the cached copy won't update.

You can toggle auto-update per marketplace via `/plugin` → Marketplaces, or control it globally with environment variables:

| Method | Effect |
| -------- | -------- |
| `/plugin` → Marketplaces → toggle | Enable or disable auto-update per marketplace |
| `export DISABLE_AUTOUPDATER=true` | Disable all auto-updates (including Claude Code itself) |
| Both `DISABLE_AUTOUPDATER=true` and `FORCE_AUTOUPDATE_PLUGINS=true` | Disable CLI updates but keep plugin updates |

To manually update a specific plugin:

```bash
claude plugin update plugin-name@marketplace-name
```

### Context impact

Plugin skill descriptions count toward the same skill-listing budget as everything else. Use `/context` for the total and `/doctor` to see which plugins contribute most. The `/plugin` **Discover** tab also shows a context-cost estimate before you install, and the **Installed** tab flags plugins you haven't used in a while — both are worth checking periodically, since an unused plugin still costs you context every turn.

For full documentation, see the [official plugins reference](https://code.claude.com/docs/en/plugins-reference).
