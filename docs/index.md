---
title: Home
nav_order: 1
---

# Dunn Lab Code

[This repository](https://github.com/caseywdunn/dunnlab_code) is a resource for scientists using AI in their research. It is really three things. First, it is a manual about using AI assistance in computational research. You are reading the manual now. Second, it has an optional Claude Code plugin that implements some of the conventions described here as skills. Third, it has assorted other resources such as example configuration files. The plugin is product-specific; the manual is not.

The manual uses Claude Code and Codex as its main examples, but most of it applies to other coding agents. [Agent Concepts](claude-intro.md) provides a vendor-neutral conceptual template, and [Coding Agents](other-agents.md) shows how the two harnesses implement it.

{: .note }
> **Our working stack, in one view**
>
> Use [Visual Studio Code](https://code.visualstudio.com/) as the editor, but run coding agents and most tools from the terminal. Command-line workflows are the ones agents can see and drive directly. For remote or long-running sessions, use [`tmux`](working-across-computers.md#keep-remote-sessions-alive-with-tmux) so the agent keeps working when your connection closes.
>
> Prefer text-based files that both Git and an agent can inspect: Markdown or LaTeX instead of Word documents, CSV or TSV instead of Excel workbooks, and scripts or configuration files instead of settings that exist only in a GUI. Agents work more effectively and efficiently with plain text because they can search, compare, edit, and verify it directly, without first translating a complicated file format or driving the application that owns it.
>
> Put each project in [Git](https://git-scm.com/) and [GitHub](https://github.com/) from the beginning. Let the agent make small, descriptive commits after verified steps, and install the [GitHub CLI](https://cli.github.com/) so it can work with repositories, issues, pull requests, and checks from the terminal.
>
> [Getting Started](getting-started.md#the-stack) explains these choices and then covers languages, environments, and agent setup. Ask your agent to explain or help configure anything unfamiliar.

## Table of contents

- [Using AI in Research](using-ai.md) — What changes and what does not: accountability, reviewing generated code, handling data, reporting AI use, and journal and funder policy. No terminal required.
- [Quick Reference](quick-reference.md) — The whole thing on one page: setup, the working rhythm, permission modes, sessions, and tmux. Start here if you want the shape before the detail.
- [Getting Started](getting-started.md) — The computational stack we recommend, and how to install and verify Claude Code or Codex.
- [Agent Concepts](claude-intro.md) — A vendor-neutral guide to models, harnesses, agent loops, context, tools, permissions, and sessions.
- [Coding Agents](other-agents.md) — How Claude Code and Codex map onto those concepts, where they differ, and what carries between them.
- [Managing Security](managing-security.md) — Permissions, sandboxing, and containers. What can go wrong and what actually stops it.
- [Working Across Computers](working-across-computers.md) — Remote agents, SSH and tmux, and separating the control plane from heavy computation.
- [Managing Context](managing-context.md) — Giving an agent the right information: project instructions, rules, memory, skills, and plugins.
- [Working Effectively](working-effectively.md) — How to frame the work: asking broadly, separating planning from building, and committing the plan.
- [DunnLab Plugin](plugin.md) — The skills, commands, and assets in this repository, and how to run them.
- [Example Workflows](example-workflows.md) — A project from empty directory to working code, start to finish.
- [Computing at Yale](yale.md) — YCRC clusters, and running coding agents on shared hardware.
- [Dunn Lab Practices](lab-practices.md) — Lab-specific practices, and the reasoning behind the conventions the plugin encodes.

The last two chapters contain information specific to our institution and lab.

## For contributors

Corrections and additions are welcome, please file issues at <https://github.com/caseywdunn/dunnlab_code/issues>. `dev_docs/contributing.md` in the repository covers the branching model, the checks that run on every change, and the release process.

## AI use

This manual, the plugin, and the scripts in this repository were written by Casey Dunn with Claude Code from the first commit in March 2026 onward, and later with OpenAI Codex as well.

Together, these agents drafted or rewrote most of the prose in these chapters, wrote the plugin skills and check scripts, and checked factual claims against vendor and YCRC documentation. I set the structure, decided every convention, edited throughout, and am responsible for all of it, including any errors.

Following this manual's own advice on [rolling your own](using-ai.md#roll-your-own) and borrowing GAIDeT's vocabulary, the tasks delegated under human supervision were: literature search and systematization, text generation, proofreading and editing, code generation, and process automation.

Agents: Anthropic Claude Code and OpenAI Codex.

Models: Claude Opus 4.6, 4.7, 4.8, and Opus 5; OpenAI GPT-5 via Codex.

The git history is the detailed record. Most earlier commits carry a `Co-Authored-By` trailer naming the Claude model that contributed to them.
