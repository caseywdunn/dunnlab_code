---
title: Getting Started
nav_order: 5
---

# Getting Started

How to get Claude Code or Codex running on your own machine.

## Before you start

[The Toolkit](toolkit.md) describes the tools this setup relies on, including the shell, Git, GitHub, and Python, and why we chose them. Install [Git](https://git-scm.com/) and the [GitHub CLI](https://cli.github.com/) before setting up an agent; if any of it is unfamiliar, the agent can help once it is running.

## Setting up a coding agent

Install Claude Code, Codex, or both. They occupy the same place in this workflow: each can work locally from the terminal, integrate with an editor, and hand work to a cloud environment. The [Coding Agents](other-agents.md) chapter compares their implementation details.

Both are available through several surfaces:

- **A desktop or web application**, including remote and cloud work.
- **An editor extension**, such as their VS Code integrations.
- **A command-line program**, running in your terminal alongside your existing editor and tools.

We use the command line most often. It works in a wider variety of situations, gives the agent direct access to the surrounding toolchain, and tends to expose new capabilities first. This manual assumes the command line throughout; if you are using another interface, the equivalent is usually easy to find.

### 1. Install an agent

Follow the official instructions for [Claude Code](https://code.claude.com/docs/en/overview), [Codex](https://learn.chatgpt.com/docs/codex/cli), or both. On macOS and Linux, their standalone installers are:

```bash
# Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# Codex
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

From a project directory, run `claude` or `codex` and complete the sign-in flow. Ask either one to explain the repository as a first read-only task.

### 2. Optional: install the DunnLab plugin for Claude Code

Register the dunnlab marketplace and install the plugin:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

This pulls the plugin from GitHub and caches it locally. To pick up changes later, run `/plugin update dunnlab-code@dunnlab`. Auto-update is off by default for third-party marketplaces like this one, so nothing arrives on its own unless you enable it under `/plugin` → **Marketplaces**.

Note that methods for installing plugins differ when using the desktop app or extension.

### 3. Verify the agent

For either agent, start in a Git repository and ask it to report its working directory, active instructions, permission boundary, and Git status. In Codex, `/status` and `/permissions` expose the session configuration. In Claude Code, `/context` and `/permissions` expose the corresponding information.

If you installed the DunnLab plugin, run the following Claude Code slash command:

Run the following slash command to confirm everything is wired up:

```
/dunnlab-code:dunnlab-check
```

You should see a welcome message and a list of available skills. Plugin skills are namespaced by the plugin name; the bare `/dunnlab-check` also works as long as nothing else has claimed that name.

### 4. Optional: know Claude Code's bundled skills

Claude Code ships with a set of **bundled skills** that are available in every session with nothing to install. Several are worth knowing about:

| Skill | What it does |
|-------|-------------|
| `/code-review` | Reviews the current diff, a branch, or a PR for correctness bugs and cleanups |
| `/simplify` | Reviews changed code for reuse, quality, and efficiency, then applies the fixes |
| `/security-review` | Security review of pending changes |
| `/claude-api` | Reference for the Claude API and Anthropic SDKs — model IDs, pricing, tool use, caching |
| `/run`, `/verify` | Launch your project and confirm a change works against the running app, not just the tests |
| `/doctor` | Setup checkup, including what your skills and plugins are costing you in context |
| `/loop` | Repeat a prompt on an interval |

Type `/` to see everything available in the current session.

### 5. Optional: install additional Claude Code plugins

These are actual plugins and do need installing, from Anthropic's official marketplace:

```bash
claude plugin install <plugin-name>@claude-plugins-official
```

| Plugin | What it does |
|--------|-------------|
| **skill-creator** | Structured workflow for building skills, running evals against them, and tuning descriptions. Worth having if you plan to write skills of your own — see [Creating and evaluating skills](managing-context.md#creating-and-evaluating-skills). |
| **pyright-lsp** | Gives Claude a language server for Python: type errors reported immediately after each edit, plus jump-to-definition and find-references. Requires `pyright-langserver` on your PATH. There are equivalents for [most languages](https://code.claude.com/docs/en/discover-plugins#code-intelligence), including `rust-analyzer-lsp`. |
| **security-guidance** | Reviews each change Claude makes for common vulnerabilities and fixes what it finds in the same session. |

Browse everything available by running `/plugin` and opening the **Discover** tab, which shows a context-cost estimate for each plugin before you install it. The **Installed** tab flags plugins you have not used recently — worth checking now and then, since an unused plugin still costs context every turn.
