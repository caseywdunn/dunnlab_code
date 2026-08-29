---
title: Claude Code Concepts
nav_order: 5
---

# Claude Code Concepts

How Claude Code actually works: which interface does what, what it can reach on your machine, and how it is extended.

The three chapters after this one build directly on it. [Managing Security](managing-security.md) is about constraining what Claude can do, [Managing Context](managing-context.md) about giving it the right information, and [Working Effectively](working-effectively.md) about how to frame the work. All three assume the vocabulary introduced here.

## How Claude Code interacts with your computer

When you launch Claude Code, you specify a **working directory** (the directory you run `claude` from). This is the project root where Claude focuses its work — reading files, writing code, and running commands.

Claude Code is not limited to this directory. It can read and write files elsewhere on your machine (subject to your [permission settings](managing-security.md)), but the working directory is the default context for all operations.

At startup, Claude Code loads **context** from several sources:

- **Standing instructions** — A file of project conventions checked into the repo, plus your own personal preferences. [Managing Context](managing-context.md#agent-instructions) covers the format
- **Rules** (`.claude/rules/`) — Topic-specific instructions, optionally scoped to file paths so they load only when relevant
- **Auto memory** — Notes Claude has kept for itself from previous sessions in this repository
- **Plugins** — Bundles of skills, commands, and hooks (like this Dunn Lab plugin)
- **MCP servers** — External tool integrations configured in settings

Run `/context` at any time to see exactly what loaded and what it cost. See [Managing Context](managing-context.md) for how to shape it.

## Extensibility: tools, skills, commands, hooks, and MCP

Claude Code's capabilities can be extended in several ways. These differ in how they are triggered and what they do:

| Mechanism | Trigger | Purpose |
|-----------|---------|---------|
| **Tools** | Automatic — Claude decides when to use them | Built-in capabilities (read/write files, run bash, search code, etc.) |
| **Skills** | Automatic (context-based) or explicit (`/skill-name`) | Sets of instructions that guide Claude's behavior for specific tasks |
| **Hooks** | Automatic — fired by events (e.g., before a tool runs) | Shell scripts that run in response to Claude Code lifecycle events |
| **Subagents** | Claude delegates, or you invoke one | Separate context windows for work that would otherwise crowd the main conversation |
| **MCP servers** | Automatic — Claude decides when to call them | External integrations that give Claude access to additional tools and data sources |

Custom slash commands used to be a separate mechanism. They have been merged into skills: a file at `.claude/commands/foo.md` and a skill at `.claude/skills/foo/SKILL.md` both give you `/foo` and behave the same way. Existing command files keep working, but write new ones as skills.

For details on each, see the [Claude Code documentation](https://code.claude.com/docs/en/overview).

## Other ways to use Claude

Claude Code is one of several ways Anthropic offers to work with Claude models:

| Interface | What it is |
|-----------|-----------|
| **Chat** ([claude.ai](https://claude.ai)) | Web-based conversation interface |
| **Code** | Agentic coding — Claude reads, writes, and runs code, with direct access to your filesystem and terminal |
| **Cowork** | Agentic non-coding tasks — document processing, image work, research, and other workflows for less technical users |
| **API / SDK** | Programmatic access for building Claude into your own applications |

Chat is what you get when you use Claude on the web, like other chatbots. Code and Cowork are agents that work on real files across multiple steps.

Cowork is the same underlying agent pointed at non-coding work, and it runs on the desktop app, web, and mobile. On the desktop it has access to local files much as Claude Code does. Skills are shared between the two: Cowork reads your personal skills in `~/.claude/skills/`, project skills in the repo, and skills from installed plugins, so a skill you write for one is available in the other on the same machine. In Cowork you manage them under **Customize → + → Skills**.

The API and SDK are useful for automating many tasks at once, and for large batch runs.
