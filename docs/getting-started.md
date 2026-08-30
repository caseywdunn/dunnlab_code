---
title: Getting Started
nav_order: 4
---

# Getting Started

The stack we recommend, and how to get Claude Code or Codex running on your own machine.

## The stack

**Prefer industry-standard tools over domain-specific ones.** This is the single principle behind most of the choices below. It lets you draw on the enormous investment industry makes in data tooling, it gives you skills that are portable outside academia, and it means that when something breaks, someone has already written about it.

The optional [`dunnlab-defaults` skill](plugin.md#the-skills) encodes these preferences for Claude Code. With either agent, put durable conventions in `AGENTS.md` so they apply without being restated.

### Terminal-first and text-first

[Visual Studio Code](https://code.visualstudio.com/docs) is our editor. Its integrated terminal, source-control tools, and language extensions put the project in one window. Both [Claude Code](https://code.claude.com/docs/en/vs-code) and [Codex](https://learn.chatgpt.com/docs/codex/ide) have editor integrations, but the terminal is the center of the workflow rather than an accessory to it.

We usually launch coding agents in the terminal, even while editing in VS Code. We use agent plugins and skills for instructions and context, but prefer ordinary command-line tools for the work itself. An agent can run a command, inspect its complete output, retry it, and record what happened; a workflow that depends on clicking through a GUI is much harder for it to operate autonomously.

Prefer text-based formats whenever they can represent the work adequately: Markdown (`.md`) or LaTeX (`.tex`) rather than Word (`.docx`), CSV or TSV rather than Excel (`.xlsx`), and scripts or configuration files rather than settings stored only in an application. Plain text is searchable, diffable, easy for agents to read and edit, and durable across software versions. Use a binary format when its features are genuinely needed, but keep the source of record in text where practical.

### Git and GitHub are the backbone

We rely heavily on [Git](https://git-scm.com/doc) and [GitHub](https://docs.github.com/en/get-started/start-your-journey/what-is-github). They are how code, plans, documentation, and configuration are shared, backed up, reviewed, and tracked over time. With an AI assistant doing much of the work, a clean commit history becomes more valuable, not less.

Treat the repository as the durable project workspace. A plan is a real Markdown file in the repository; code and documentation evolve beside it; issues record work that has not happened yet; commits record verified steps that have. This gives people and agents the same history and makes it possible to reconstruct why the project took its current shape.

Let the agent create a small commit after each verified step and write a message that explains why the change was made. The resulting history is both a recovery mechanism and a detailed record of the work delegated to AI. Review changes before they leave your machine, but do not spend your time manually composing commit messages the agent is better positioned to write.

Install the [GitHub CLI](https://cli.github.com/) and authenticate it once:

```bash
gh auth login
```

Once authorized, the agent can use commands such as `gh repo create`, `gh issue create`, `gh issue comment`, `gh issue close`, and `gh pr create`, as well as inspect pull-request checks and reviews. This puts GitHub's project-management surface in the same terminal the agent already controls. Authentication grants the agent actions under your account, so do this only in an environment you trust and with access appropriate to the project.

If any part of this stack is unfamiliar, ask the agent to explain it, install it, or walk you through the setup, and use the official documentation linked above for more depth.

Do not store large data files or analysis results in git repositories. Git is designed for small, mostly text files. GitHub blocks any individual file over 100 MB and recommends keeping a repository under 1 GB; in practice a well-kept analysis repo should be far smaller than that — if yours is approaching 100 MB, something belongs elsewhere.

### Languages

#### Python

**[Python](https://www.python.org/)** (3.10+) is the default for data analysis and scripting. Though R is common in biology, it is a niche language by comparison, and Python skills travel further. For learning data analysis in Python, [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781098121211/) is an excellent introduction and is [free online](https://jakevdp.github.io/PythonDataScienceHandbook/).

The Python ecosystem we use includes:

- **[conda](https://docs.conda.io/)** or **[mamba](https://mamba.readthedocs.io/)** for environment management
- **[Jupyter](https://jupyter.org/) notebooks** for exploratory work, refactored into scripts once something is worth keeping
- **[ruff](https://docs.astral.sh/ruff/)** for formatting and linting — it replaces the older black and flake8 combination
- **[Quarto](https://quarto.org/)** for executable manuscripts

#### R

**R** is the right choice when an analysis needs libraries that only exist there — Seurat, much of Bioconductor — when it is what you already know and it works for you, or when you are joining a team that has chosen it. Falling back to R is a normal outcome, not a failure.

#### Rust

**[Rust](https://www.rust-lang.org/)** when performance and low-level control are dominant concerns.

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
