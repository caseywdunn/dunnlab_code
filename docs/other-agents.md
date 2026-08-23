---
title: Other Coding Agents
nav_order: 9
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

If you have guidance that only makes sense for Claude Code — a skill to invoke, a permission mode to prefer — add it below the import rather than in `AGENTS.md`:

```markdown
@AGENTS.md

## Claude Code

Use plan mode for anything under `analysis/`.
Invoke the `dunnlab-bioinformatics` skill before touching sequence data.
```

This way there is one source of truth, every agent reads it, and the Claude-specific additions live somewhere they will not confuse another tool.

Everything [Managing Context](managing-context.md) says about keeping instructions short, and about moving detailed guidance into path-scoped rules, applies to the `AGENTS.md` at the other end of that import.
