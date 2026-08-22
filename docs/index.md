---
title: Home
nav_order: 1
---

# Dunn Lab Code

This manual is about using AI assistance in computational research: what it changes about your responsibilities, how to set the tools up, and how to keep them from doing damage. It is written for the [Dunn Lab](https://dunnlab.org/) but most of it is not lab-specific, and it is meant to be shared.

It is also a Claude Code plugin — the conventions described here are packaged as skills, so Claude applies them while you work instead of you having to remember them. The manual and the plugin live in the same repository: <https://github.com/caseywdunn/dunnlab_code>.

This is not a comprehensive guide to any of the tools it mentions. It is a map of the stack, with enough opinion to get you started and pointers to the real documentation for everything else.

## How this manual is organized

The chapters narrow as they go. Read until they stop applying to you.

**Anyone** — nothing here is specific to our lab or institution:

- [Using AI in Research](using-ai.md) — What changes and what does not: accountability, reviewing generated code, handling data, disclosure, and journal and funder policy. No terminal required.
- [Getting Started](getting-started.md) — The computational stack we recommend, and how to install and verify Claude Code.
- [Claude Code Concepts](claude-intro.md) — How it works: interfaces, the working directory, how it is extended, and the habits that make it effective.
- [Managing Security](managing-security.md) — Permissions, sandboxing, and containers. What can go wrong and what actually stops it.
- [Managing Context](managing-context.md) — Giving Claude the right information: CLAUDE.md, rules, memory, skills, and plugins.
- [Example Workflows](example-workflows.md) — A project from empty directory to working code, start to finish.

**Anyone at Yale:**

- [Computing at Yale](yale.md) — YCRC clusters, and running Claude Code on shared hardware without causing harm.

**The Dunn Lab** — deliberately opinionated; useful to others as a template:

- [Dunn Lab Practices](lab-practices.md) — What our skills encode, the choices behind them, and data management.

## Where to start

**New to the lab?** Read [Using AI in Research](using-ai.md) first — it is short and it is the part you are accountable for. Then [Getting Started](getting-started.md) to set up your machine, and [Dunn Lab Practices](lab-practices.md) before you commit anything.

**Here for the tooling?** [Getting Started](getting-started.md), then [Managing Security](managing-security.md) before you let Claude run anything unsupervised.

**Evaluating this for your own group?** The first six chapters should transfer unchanged. [Dunn Lab Practices](lab-practices.md) shows what a filled-in version of the last one looks like.

## For contributors

Corrections and additions are welcome, from inside the lab or outside it. `dev_docs/contributing.md` in the repository covers the branching model, the checks that run on every change, and the release process.
