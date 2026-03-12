---
title: Managing Context
nav_order: 6
---

# Managing Context

## What is the context window?

Every conversation with Claude has a finite context window — the total amount of text (your messages, Claude's responses, file contents, tool outputs) that fits in working memory. When a conversation grows long, older content is compressed or dropped to make room. This means Claude can forget earlier instructions, lose track of decisions, or re-read files it already saw.

Managing context well means giving Claude the right information at the right time without filling the window with noise. Two mechanisms help with this: CLAUDE.md files provide persistent project instructions, and skills inject task-specific guidance on demand.

### The `/clear` command

When a conversation gets long or you're switching tasks, use `/clear` to reset the context window. This drops the conversation history and re-loads your CLAUDE.md files fresh. It's the simplest way to reclaim context space.

## CLAUDE.md

CLAUDE.md files are markdown files that Claude reads at the start of every session. They provide standing instructions — build commands, coding conventions, architectural decisions, project-specific rules — so you don't have to repeat yourself.

### Where to put them

| Location | Scope |
|----------|-------|
| `~/.claude/CLAUDE.md` | Personal preferences, applied to all projects |
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project-level, committed to git |

Claude also discovers CLAUDE.md files in parent directories (loaded at startup) and subdirectories (loaded on demand when you work in those directories).

### Keep it short

CLAUDE.md content is loaded into the context window at session start. Longer files consume more of your context budget and reduce Claude's adherence to instructions. **Keep each CLAUDE.md under 100 lines.** If you need more detail, point Claude to where it can find the information rather than including it inline:

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

Use `/memory` to see which CLAUDE.md files are loaded in your current session.

For full documentation, see the [official CLAUDE.md reference](https://docs.anthropic.com/en/docs/claude-code/memory).

## Skills

Skills are markdown files that extend Claude with reusable, task-specific instructions. Unlike CLAUDE.md (which is always loaded), skill content is injected into context only when the skill is invoked — either by you or by Claude when it determines a skill is relevant.

### How they work

Each skill has a short **description** that is always present in context (so Claude knows what's available) and a full **instruction body** that loads only on use. This keeps context lean until you actually need the skill.

### Invoking skills

- Type `/skill-name` to invoke a skill directly
- Claude can also invoke skills automatically when it determines one is relevant to your request (unless the skill opts out with `disable-model-invocation: true`)

### Viewing loaded context

Use `/context` to see which skills are loaded and whether any have been excluded due to context budget limits. Skill descriptions share a budget of roughly 2% of the context window — if you have many skills, some may be dropped.

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
name: my-skill
description: One-line summary of what this skill does
---

# Instructions

Your skill instructions here...
```

Skills can be added at three levels:

| Location | Scope |
|----------|-------|
| `~/.claude/skills/<name>/SKILL.md` | Personal, all projects |
| `.claude/skills/<name>/SKILL.md` | Project, committed to git |
| `<plugin>/skills/<name>/SKILL.md` | Distributed via plugin |

### Updating skills

Edit the `SKILL.md` file directly. Claude Code detects changes automatically — no restart needed.

For full documentation, see the [official skills reference](https://docs.anthropic.com/en/docs/claude-code/skills).

### Creating and evaluating skills

The **skill-creator** skill (available from the Anthropic official plugin marketplace) provides a structured workflow for building new skills and measuring their effectiveness. Install it via `/plugin` or use it if it's already available in your environment.

#### The development loop

1. **Define intent** — clarify what the skill should do, when it should trigger, and what output it produces
2. **Draft the SKILL.md** — write frontmatter and instructions following the patterns in [Adding skills](#adding-skills)
3. **Run test cases** — the skill-creator generates realistic test prompts and runs them both *with* and *without* your skill, using isolated subagents
4. **Review and grade** — an eval viewer opens in your browser showing side-by-side outputs and quantitative benchmarks
5. **Iterate** — revise the skill based on feedback, re-run, and compare against previous iterations

#### Running an evaluation

To evaluate an existing skill, invoke the skill-creator and ask it to evaluate your skill by path:

```
/skill-creator Evaluate the skill at skills/my-skill/SKILL.md
```

The skill-creator will:

- **Generate test prompts** — 2–3 realistic user requests that should trigger your skill. You review and approve these before they run.
- **Run with-skill and baseline comparisons** — each test prompt is executed twice: once following your skill's instructions, once without any skill. Both runs happen in isolated worktrees so no files are modified in your working directory.
- **Grade against assertions** — objective checks (file exists, content matches pattern) are evaluated programmatically. Results are saved as `grading.json` per run.
- **Aggregate a benchmark** — pass rates, token usage, and timing are compared between with-skill and baseline runs, with analyst observations about which assertions discriminate (measure skill value) vs. which pass regardless.
- **Open an eval viewer** — a browser-based tool with an "Outputs" tab for browsing files produced by each run and a "Benchmark" tab showing quantitative results.

#### What the benchmark tells you

The benchmark highlights three things:

- **Discriminating assertions** — checks that pass with the skill but fail without it. These measure what value the skill actually adds. For example, a project scaffolding skill might always produce `CLAUDE.md` and `documentation/overview.md` while the baseline never does.
- **Non-discriminating assertions** — checks that pass in both conditions. These validate correctness but don't justify the skill's existence. If all your assertions are non-discriminating, the skill may not be adding value.
- **Cost tradeoff** — skills typically increase token usage and execution time. The benchmark quantifies this so you can decide whether the added structure is worth the cost.

#### Description optimization

After the skill content is finalized, the skill-creator can also optimize the `description` field for better triggering accuracy. It generates a set of should-trigger and should-not-trigger test queries, then iteratively refines the description to maximize correct triggering while minimizing false positives.

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

Plugin sources can be relative paths (for monorepos), GitHub repos, git URLs, or npm packages. See the [official marketplace documentation](https://docs.anthropic.com/en/docs/claude-code/plugins) for the full `marketplace.json` schema and source types.

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

Plugin skill descriptions count toward the same ~2% context budget as other skills. Use `/context` to see which plugin skills are loaded and their token cost.

For full documentation, see the [official plugins reference](https://docs.anthropic.com/en/docs/claude-code/plugins).
