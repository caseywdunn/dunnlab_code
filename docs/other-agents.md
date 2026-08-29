---
title: Other Coding Agents
nav_order: 11
---

# Other Coding Agents

This manual is about Claude Code, but it is one of several capable tools and not an obvious permanent winner. The field moves fast enough that anything written here about relative quality will age badly, so this chapter is about the landscape and, more usefully, about how to keep your project working with more than one of them.

Running several is now normal rather than exotic. A common pattern is a terminal agent for large refactors, an in-editor agent for everyday flow, and sometimes a cloud agent for work you kick off and come back to. There is no reason your repository should have to pick one.

## The main ones

| Tool | What it is |
|------|-----------|
| **[OpenAI Codex](https://developers.openai.com/codex/)** | OpenAI's agent, spanning a CLI, an IDE extension, and a cloud service. The closest analogue to Claude Code. |
| **[GitHub Copilot](https://github.com/features/copilot)** | The most widely adopted by a wide margin, now well past autocomplete into agentic work and PR review. Deeply tied into GitHub. |
| **[Cursor](https://cursor.com/)** | An AI-native editor, a fork of VS Code. Strongest of the in-editor agents, and the usual comparison point for day-to-day flow. |
| **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** and **[Jules](https://jules.google/)** | Google's terminal agent and its asynchronous cloud agent. |
| **[Aider](https://aider.chat/)**, **[goose](https://block.github.io/goose/)**, **[OpenCode](https://github.com/sst/opencode)** | Open-source terminal agents. Model-agnostic, so you can point them at whichever provider you have access to. |
| **[Devin](https://devin.ai/)**, **[Windsurf](https://windsurf.com/)** | Cognition's asynchronous agent and the IDE it acquired. |

Two things follow from this list that matter more than any ranking.

**They are model-agnostic to varying degrees.** Several of these can run against Claude models, and Claude Code can run against Bedrock or Vertex. The tool and the model are separate choices.

**Most of what this manual teaches transfers.** The judgment in [Using AI in Research](using-ai.md) applies to any of them. So does the security thinking in [Managing Security](managing-security.md), though the specific controls differ. The context principles in [Managing Context](managing-context.md) — give the agent standing instructions, keep them short, scope detailed guidance to where it is relevant — are general even though the filenames are not.

## AGENTS.md

The one piece of genuine cross-tool standardisation so far is [`AGENTS.md`](https://agents.md/): a plain markdown file at your repository root holding the instructions an agent should read before working on your code. Build commands, test commands, conventions, things to avoid.

It emerged from work across OpenAI Codex, Amp, Google's Jules, Cursor, and Factory, and is now stewarded by the Agentic AI Foundation under the Linux Foundation. More than 60,000 open-source projects use one. It is read by Codex, Copilot, Cursor, Gemini CLI, Jules, Zed, Aider, Devin, goose, Windsurf, VS Code, and others.

The format is deliberately unopinionated: ordinary markdown, no required fields, and in a monorepo the nearest file up the tree wins.

## Serving both from one file

**Claude Code reads `CLAUDE.md`. It does not read `AGENTS.md`.** A repository with only an `AGENTS.md` gives Claude Code nothing — no warning, no error, it simply starts with no project instructions.

Maintaining two files that say the same thing is worse: they drift, and you will not notice which one an agent read. Instead, put the real content in `AGENTS.md` and make `CLAUDE.md` a one-line pointer to it:

```markdown
@AGENTS.md
```

That is the whole file. Claude Code expands the `@` import at session start, so it loads exactly what every other agent loads.

## Skills and MCP servers

Instructions are not the only thing you might want to carry between agents. Two other mechanisms matter, and they travel very differently.

### MCP servers travel well

The [Model Context Protocol](https://modelcontextprotocol.io/) is how an agent reaches external tools and data — a GitHub server, a database, an internal API. It began at Anthropic, is now maintained as an open standard under the Linux Foundation, and is implemented by essentially every major agent: Claude Code, Codex, Cursor, Copilot, Windsurf, Zed, and the main agent frameworks besides.

In practice a server you have configured for one agent works with another. What differs is where the configuration lives, not the server. This is the most portable part of your setup.

### Skills travel in their core, less so at the edges

[Agent Skills](https://agentskills.io/) is also an open format: a folder holding a `SKILL.md` with a name, a description, and instructions, optionally alongside scripts and reference files. It originated at Anthropic and has been adopted broadly — Codex, Cursor, Copilot, VS Code, Gemini CLI, goose, OpenCode, Amp, Factory, and JetBrains' Junie all read it.

The mechanism is the same everywhere, and it is what makes skills cheap: an agent loads only the name and description at startup, then pulls in the full instructions when a task matches. Many skills cost almost nothing until one is used.

What does not travel is the extensions. The spec defines six frontmatter fields — `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Claude Code accepts all six and adds its own, including `disable-model-invocation`, `when_to_use`, and `disallowed-tools`, along with body features like shell-command injection and `${CLAUDE_*}` variables. Another agent ignores what it does not recognise, so a skill leaning on those degrades rather than breaking — but it degrades quietly, which is worse.

For a skill you want to work everywhere, keep the frontmatter to the six spec fields and the body to plain markdown.

### Plugins do not travel

The packaging around skills — marketplaces, `plugin.json`, namespaced invocation — is Claude Code's own. [The DunnLab plugin](plugin.md) will not install into Codex or Cursor.

The skills inside it are ordinary `SKILL.md` files, though, so copying one into another agent's skills directory generally works. As it happens all seven of ours use only the six spec fields, so they should load anywhere that reads the format.

### Changing the model underneath

None of this depends on which model you run. Claude Code against Amazon Bedrock, Google Cloud, or Microsoft Foundry is the same client with the same skills, MCP servers, and settings — only the inference endpoint changes. Model choice does affect some features, auto mode among them, but not the portability of your configuration.
