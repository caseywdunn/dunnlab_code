---
title: Home
nav_order: 1
---

# Dunn Lab Code

[This repository](https://github.com/caseywdunn/dunnlab_code) is a resource for scientists using AI in their research. It is really three things. First, it is a manual about using AI assistance in computational research. You are reading the manual now. Second, it is a Claude Code plugin that implements some of the conventions described here as skills, so Claude can apply them directly and consistently. Third, it has assorted other resources such as example configuration files.


## Table of contents

- [Using AI in Research](using-ai.md) — What changes and what does not: accountability, reviewing generated code, handling data, disclosure, and journal and funder policy. No terminal required.
- [Getting Started](getting-started.md) — The computational stack we recommend, and how to install and verify Claude Code.
- [Claude Code Concepts](claude-intro.md) — How it works: interfaces, the working directory, how it is extended, and the habits that make it effective.
- [Managing Security](managing-security.md) — Permissions, sandboxing, and containers. What can go wrong and what actually stops it.
- [Managing Context](managing-context.md) — Giving Claude the right information: CLAUDE.md, rules, memory, skills, and plugins.
- [DunnLab Plugin](plugin.md) — The skills, commands, and assets in this repository, and how to run them.
- [Example Workflows](example-workflows.md) — A project from empty directory to working code, start to finish.
- [Computing at Yale](yale.md) — YCRC clusters, and running Claude Code on shared hardware.
- [Dunn Lab Practices](lab-practices.md) — Lab-specific practices, and the reasoning behind the conventions the plugin encodes.

The last two chapters contain information specific to our institution and lab.


## For contributors

Corrections and additions are welcome, please file issues at <https://github.com/caseywdunn/dunnlab_code/issues>. `dev_docs/contributing.md` in the repository covers the branching model, the checks that run on every change, and the release process.
