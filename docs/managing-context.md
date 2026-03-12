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
