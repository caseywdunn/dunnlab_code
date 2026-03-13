---
title: Claude Code Concepts
nav_order: 3
---

# Claude Code Concepts

A brief orientation to Claude's interfaces and how Claude Code works.

## Ways to use Claude

Anthropic offers several ways to interact with Claude models:

| Interface | What it is |
|-----------|-----------|
| **Chat** ([claude.ai](https://claude.ai)) | Web-based conversation interface |
| **Cowork** | Claude works alongside you in your IDE (VS Code, JetBrains) as a pair programmer |
| **Code** | CLI-based agentic coding — Claude reads, writes, and runs code in your terminal |
| **API / SDK** | Programmatic access for building Claude into your own applications |

In this lab we primarily use **Claude Code**. It gives Claude direct access to your filesystem and terminal, making it effective for data analysis, scripting, and project development.

## How Claude Code interacts with your computer

When you launch Claude Code, you specify a **working directory** (the directory you run `claude` from). This is the project root where Claude focuses its work — reading files, writing code, and running commands.

Claude Code is not limited to this directory. It can read and write files elsewhere on your machine (subject to your [permission settings](managing-security.md)), but the working directory is the default context for all operations.

At startup, Claude Code loads **context** from several sources:

- **`CLAUDE.md` files** — Instructions checked into the repo (project-level) or in your home directory (user-level)
- **Plugins** — Bundles of skills, commands, and hooks (like this Dunn Lab plugin)
- **MCP servers** — External tool integrations configured in settings

See [Managing Context](managing-context.md) for more on how to shape what Claude knows.

## Extensibility: tools, skills, commands, hooks, and MCP

Claude Code's capabilities can be extended in several ways. These differ in how they are triggered and what they do:

| Mechanism | Trigger | Purpose |
|-----------|---------|---------|
| **Tools** | Automatic — Claude decides when to use them | Built-in capabilities (read/write files, run bash, search code, etc.) |
| **Skills** | Automatic (context-based) or explicit (`/skill-name`) | Sets of instructions that guide Claude's behavior for specific tasks |
| **Commands** | Explicit — user types a slash command | Predefined prompts that trigger specific Claude actions |
| **Hooks** | Automatic — fired by events (e.g., before a tool runs) | Shell scripts that run in response to Claude Code lifecycle events |
| **MCP servers** | Automatic — Claude decides when to call them | External integrations that give Claude access to additional tools and data sources |

For details on each, see the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code).

## Best practices for effective use

Getting good results from Claude Code is less about prompt engineering and more about workflow discipline.

**Plan before coding.** Ask Claude to develop a detailed plan before writing any code. Review and refine the plan together until you're confident in the approach. This avoids wasted effort and helps Claude make better decisions throughout implementation.

**Work in small, testable steps.** Break work into incremental tasks with clear, testable outcomes. After each task is completed and verified, ask Claude to commit (don't commit manually — Claude generates detailed commit messages that document the reasoning behind changes). Then clear the context with `/clear` before starting the next task. This keeps the conversation focused and prevents context from getting stale or cluttered.

**Let Claude handle errors.** When code produces errors, don't copy and paste error messages into the chat. Instead, ask Claude to run the code itself — it will see the full error output, have the surrounding context, and can diagnose and fix the problem directly. This is faster and less error-prone than manually relaying fragments of stack traces.
