---
title: Home
nav_order: 1
---

# Dunn Lab Code

[This repository](https://github.com/caseywdunn/dunnlab_code) is a resource for scientists using AI in their research. It is really three things. First, it is a manual about using AI assistance in computational research. You are reading the manual now. Second, it has a Claude Code plugin that implements some of the conventions described here as skills, so Claude can apply them directly and consistently. Third, it has assorted other resources such as example configuration files.


## Table of contents

- [Using AI in Research](using-ai.md) — What changes and what does not: accountability, reviewing generated code, handling data, reporting AI use, and journal and funder policy. No terminal required.
- [Quick Reference](quick-reference.md) — The whole thing on one page: setup, the working rhythm, permission modes, sessions, and tmux. Start here if you want the shape before the detail.
- [Getting Started](getting-started.md) — The computational stack we recommend, and how to install and verify Claude Code.
- [Claude Code Concepts](claude-intro.md) — How it works: interfaces, the working directory, how it is extended, and the habits that make it effective.
- [Managing Security](managing-security.md) — Permissions, sandboxing, and containers. What can go wrong and what actually stops it.
- [Managing Context](managing-context.md) — Giving Claude the right information: CLAUDE.md, rules, memory, skills, and plugins.
- [DunnLab Plugin](plugin.md) — The skills, commands, and assets in this repository, and how to run them.
- [Example Workflows](example-workflows.md) — A project from empty directory to working code, start to finish.
- [Other Coding Agents](other-agents.md) — The wider landscape, and how to keep a project working with more than one agent.
- [Computing at Yale](yale.md) — YCRC clusters, and running Claude Code on shared hardware.
- [Dunn Lab Practices](lab-practices.md) — Lab-specific practices, and the reasoning behind the conventions the plugin encodes.

The last two chapters contain information specific to our institution and lab.


## For contributors

Corrections and additions are welcome, please file issues at <https://github.com/caseywdunn/dunnlab_code/issues>. `dev_docs/contributing.md` in the repository covers the branching model, the checks that run on every change, and the release process.

## AI use

This manual, the plugin, and the scripts in this repository were written by Casey Dunn with Claude, Anthropic's AI assistant, from the first commit in March 2026 onward.

Claude drafted or rewrote most of the prose in these chapters, wrote the plugin skills and the check scripts, and checked factual claims against vendor and YCRC documentation. I set the structure, decided every convention, edited throughout, and am responsible for all of it, including any errors.

Following this manual's own advice on [rolling your own](using-ai.md#roll-your-own) and borrowing GAIDeT's vocabulary, the tasks delegated under human supervision were: literature search and systematization, text generation, proofreading and editing, code generation, and process automation.

Models: Claude Opus 4.6, 4.7, 4.8, and Opus 5.

The git history is the detailed record — almost every commit carries a `Co-Authored-By` trailer naming the model that contributed to it.
