---
title: Claude Code Concepts
nav_order: 4
---

# Claude Code Concepts

A brief orientation to Claude's interfaces and how Claude Code works.

## Ways to use Claude

Anthropic offers several ways to interact with Claude models:

| Interface | What it is |
|-----------|-----------|
| **Chat** ([claude.ai](https://claude.ai)) | Web-based conversation interface |
| **Code** | Agentic coding — Claude reads, writes, and runs code, with direct access to your filesystem and terminal |
| **Cowork** | Agentic non-coding tasks — document processing, image work, research, and other workflows for less technical users |
| **API / SDK** | Programmatic access for building Claude into your own applications |

Chat is what you get when you use Claude on the web, like other chatbots. Code and Cowork are agents that work on real files across multiple steps.

**In this lab we primarily use Claude Code.** It runs on several surfaces — the terminal, the VS Code and JetBrains extensions, the desktop app, and the web at [claude.ai/code](https://claude.ai/code) — all backed by the same engine. A repo's `CLAUDE.md`, settings, skills, and MCP servers work identically across them, so which one you use is a matter of preference. Most of us live in the terminal or the VS Code extension.

Cowork is the same underlying agent pointed at non-coding work, and it runs on the desktop app, web, and mobile. On the desktop it has access to local files much as Claude Code does. Skills are shared between the two: Cowork reads your personal skills in `~/.claude/skills/`, project skills in the repo, and skills from installed plugins, so a skill you write for one is available in the other on the same machine. In Cowork you manage them under **Customize → + → Skills**.

## How Claude Code interacts with your computer

When you launch Claude Code, you specify a **working directory** (the directory you run `claude` from). This is the project root where Claude focuses its work — reading files, writing code, and running commands.

Claude Code is not limited to this directory. It can read and write files elsewhere on your machine (subject to your [permission settings](managing-security.md)), but the working directory is the default context for all operations.

At startup, Claude Code loads **context** from several sources:

- **`CLAUDE.md` files** — Instructions checked into the repo (project-level) or in your home directory (user-level)
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

## Best practices for effective use

Getting good results from Claude Code is less about prompt engineering and more about workflow discipline.

**Plan before coding.** Ask Claude to develop a detailed plan before writing any code. Review and refine the plan together until you're confident in the approach. This avoids wasted effort and helps Claude make better decisions throughout implementation.

**Work in small, testable steps.** Break work into incremental tasks with clear, testable outcomes. After each task is completed and verified, ask Claude to commit (don't commit manually — Claude generates detailed commit messages that document the reasoning behind changes). Then clear the context with `/clear` before starting the next task. This keeps the conversation focused and prevents context from getting stale or cluttered.

**Use plan mode for anything you are not sure about.** `Shift+Tab` cycles to plan mode, where Claude explores and proposes but does not edit. You review the plan before any code is written. This is the cheapest place to catch a wrong approach.

**Know how to undo.** `/rewind` restores the conversation and the files to an earlier point in the session. Committing after each verified step, as above, is the more durable version of the same idea.

**Let Claude handle errors.** When code produces errors, don't copy and paste error messages into the chat. Instead, ask Claude to run the code itself — it will see the full error output, have the surrounding context, and can diagnose and fix the problem directly. This is faster and less error-prone than manually relaying fragments of stack traces.
