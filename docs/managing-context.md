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
| **Project instructions** | `AGENTS.md`, through a one-line `CLAUDE.md` import; `.claude/rules/` | Layered `AGENTS.md` files |
| **Personal instructions** | `~/.claude/CLAUDE.md`, which can import a personal `AGENTS.md` | `~/.codex/AGENTS.md` |
| **Remembered session context** | Auto memory and session history | Session history and memories |
| **Task-specific guidance** | Skills and plugins | Skills and plugins |

Claude Code's `/context` shows what loaded and what it cost. Codex's `/status` summarizes the active session, while its layered `AGENTS.md` files remain the durable, inspectable source of project guidance.

### Starting with fresh context

When a conversation gets long or you switch tasks, start a new session or use the harness's context-reset command. In Claude Code, `/clear` drops the conversation and reloads the standing instructions. The important habit is product-independent: do not carry an old task's dead ends into a new one.

### Resuming sessions

The opposite need also arises: returning to a conversation after closing the terminal or losing a connection. Both agents save local sessions and can resume them:

```bash
claude -c        # continue the most recent Claude Code session
claude -r        # choose a Claude Code session to resume
codex resume     # choose a Codex session to resume
```

A resumed session carries its full history, including whatever cluttered it. Resume to continue the same task; start fresh for a new one.

## Agent instructions

Coding agents read a file of standing instructions at the start of every session: build and test commands, coding conventions, architectural decisions, and project-specific rules. You write them once instead of repeating them in every conversation.

**Write them in `AGENTS.md`**, a plain Markdown file at the root of the repository. Codex and many other agents read [`AGENTS.md`](https://agents.md/) directly. Claude Code reads a file called `CLAUDE.md` instead, so give it a `CLAUDE.md` containing a single line that imports `AGENTS.md`:

```markdown
@AGENTS.md
```

That is the whole file. Claude Code expands the import at session start, so it loads exactly what every other agent loads. Create both files from the start. Two files maintained by hand drift apart, and a reader cannot tell which is current; one file with an import gives every agent the same version-controlled instructions.

### Where to put them

- **The project root:** `AGENTS.md`, committed to Git, with the `CLAUDE.md` import beside it.
- **Subdirectories:** an `AGENTS.md` in a subdirectory adds instructions for work in that part of the project. Codex layers these automatically, with the file closest to the working directory taking precedence. Claude Code needs a one-line `CLAUDE.md` import beside each one.
- **Your home directory,** for personal preferences that apply to every project: `~/.codex/AGENTS.md` for Codex, and for Claude Code a `~/.claude/CLAUDE.md` that imports the same file with `@~/.codex/AGENTS.md`.

Each harness has further options, such as organization-wide policy files; see the documentation for [Claude Code](https://code.claude.com/docs/en/memory) and [Codex](https://developers.openai.com/codex/guides/agents-md).

### Keep it short

Everything in `AGENTS.md` is loaded into the context window at the start of every session. A longer file costs more of that budget and is followed less reliably. Anthropic's [guidance](https://code.claude.com/docs/en/memory) suggests staying under 200 lines, and shorter is better. When you need more detail, point to where it lives rather than including it:

```markdown
## Architecture
See `docs/architecture.md` for the full system design.

## API conventions
See `src/api/README.md` for endpoint patterns and error handling.
```

The agent then reads the detailed document only when it is relevant to the task.

### What to include

- Build, test, and lint commands
- Language and framework conventions
- Naming conventions and file organization
- Pointers to files with additional context (as shown above)
- Common workflows and gotchas
- How to attribute AI in commits, for agents that do not do it by themselves: for example, *end every commit message with a `Co-Authored-By:` trailer naming the exact model and version you are running as*

To see what actually loaded in a session, use `/context` in Claude Code or `/status` in Codex.

## Rules

When project guidance outgrows a short `AGENTS.md`, Claude Code offers `.claude/rules/`: Markdown files, one topic each, discovered recursively. Codex has no equivalent; there, use `AGENTS.md` files in subdirectories, or linked documents.

```
.claude/
└── rules/
    ├── snakemake.md
    ├── plotting.md
    └── hpc.md
```

A rule with no frontmatter loads at launch, like the project instructions. **A rule with a `paths:` field loads only when Claude touches a matching file** — which is what makes this worth doing:

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

**Auto memory is machine-local and is not in version control.** It is not a substitute for `AGENTS.md`, rules, or `dev_docs/` for anything a collaborator — or you on a different machine — needs to know. Treat it as convenience, not documentation.

## Skills

Skills are markdown files that extend Claude with reusable, task-specific instructions. Unlike `AGENTS.md` (which is always loaded), skill content is injected into context only when the skill is invoked — either by you or by Claude when it determines a skill is relevant.

### How they work

Each skill has a short **description** that is always present in context (so Claude knows what's available) and a full **instruction body** that loads only on use. This keeps context lean until you actually need the skill.

### Invoking skills

- Type `/skill-name` to invoke a skill directly
- Claude can also invoke skills automatically when it determines one is relevant to your request (unless the skill opts out with `disable-model-invocation: true`)

### Viewing loaded context

Use `/context` to see the size of the skill listing, and `/doctor` for an estimate of which skills contribute most to it.

Skill descriptions share a listing budget of **1% of the model's context window** by default. When the listing overflows that budget, Claude Code does not drop skills — every skill name stays available. It **shortens descriptions**, starting with the skills you invoke least, which can strip the keywords Claude needs to match a request to the right skill. Each entry's `description` is separately capped at 1,536 characters.

If you have enough skills to hit this, raise the budget with `skillListingBudgetFraction` (e.g. `0.02` for 2%), or trim the descriptions themselves, putting the key use case first.

### Bundled skills

Claude Code ships with a set of **bundled skills** that are available in every session with nothing to install. Several are worth knowing about:

| Skill | What it does |
|-------|-------------|
| `/code-review` | Reviews the current diff, a branch, or a PR for correctness bugs and cleanups |
| `/simplify` | Reviews changed code for reuse, quality, and efficiency, then applies the fixes |
| `/security-review` | Security review of pending changes |
| `/claude-api` | Reference for the Claude API and Anthropic SDKs — model IDs, pricing, tool use, caching |
| `/run`, `/verify` | Launch your project and confirm a change works against the running app, not just the tests |
| `/doctor` | Setup checkup, including what your skills and plugins are costing you in context |
| `/loop` | Repeat a prompt on an interval |

Type `/` to see everything available in the current session.

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

- **Discriminating checks** — pass with the skill and fail without it. These are the ones that measure what the skill adds. A project scaffolding skill might reliably produce `AGENTS.md` and `dev_docs/overview.md` while the baseline never does.
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

Anyone can publish a marketplace; the [official marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces) covers how. [The DunnLab Plugin](plugin.md) is an example.

### Installing plugins

1. Run `/plugin` to open the plugin manager
2. Browse the marketplace and select a plugin to install
3. Claude Code copies the plugin to a local cache at `~/.claude/plugins/cache/`

You can also install via the CLI:

```bash
claude plugin install plugin-name@marketplace-name
```

For team projects, you can pre-configure marketplaces and plugins in `.claude/settings.json` so they're available to all contributors.

### Updates

Plugins from the official Anthropic marketplace update automatically. **Third-party marketplaces do not, by default**, so a plugin from one stays at the version you installed until you update it:

```bash
claude plugin update plugin-name@marketplace-name
```

You can turn on auto-update per marketplace under `/plugin` → **Marketplaces**. The [plugin documentation](https://code.claude.com/docs/en/discover-plugins) covers the other update settings.

### Plugins worth knowing about

These come from Anthropic's official marketplace:

```bash
claude plugin install <plugin-name>@claude-plugins-official
```

| Plugin | What it does |
|--------|-------------|
| **skill-creator** | Structured workflow for building skills, running evals against them, and tuning descriptions. Worth having if you plan to write skills of your own — see [Creating and evaluating skills](#creating-and-evaluating-skills). |
| **pyright-lsp** | Gives Claude a language server for Python: type errors reported immediately after each edit, plus jump-to-definition and find-references. Requires `pyright-langserver` on your PATH. There are equivalents for [most languages](https://code.claude.com/docs/en/discover-plugins#code-intelligence), including `rust-analyzer-lsp`. |
| **security-guidance** | Reviews each change Claude makes for common vulnerabilities and fixes what it finds in the same session. |

Browse everything available by running `/plugin` and opening the **Discover** tab.

### Context impact

Plugin skill descriptions count toward the same skill-listing budget as everything else. Use `/context` for the total and `/doctor` to see which plugins contribute most. The `/plugin` **Discover** tab also shows a context-cost estimate before you install, and the **Installed** tab flags plugins you haven't used in a while — both are worth checking periodically, since an unused plugin still costs you context every turn.

For full documentation, see the [official plugins reference](https://code.claude.com/docs/en/plugins-reference).
