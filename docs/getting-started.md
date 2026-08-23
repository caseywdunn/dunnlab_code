---
title: Getting Started
nav_order: 3
---

# Getting Started

The stack we recommend, and how to get Claude Code running on your own machine.

## The stack

**Prefer industry-standard tools over domain-specific ones.** This is the single principle behind most of the choices below. It lets you draw on the enormous investment industry makes in data tooling, it gives you skills that are portable outside academia, and it means that when something breaks, someone has already written about it.

The `dunnlab-defaults` skill encodes these preferences, along with best practices for each language, so Claude applies them without being asked.

### IDE

[Visual Studio Code](https://code.visualstudio.com/) is our editor. Its extensions integrate git, GitHub, Claude, and language-specific tooling, and it is where most of the day goes. Claude Code also has a [VS Code extension](https://code.claude.com/docs/en/vs-code), so you can work in the same window rather than alternating with a terminal.

### Version control

We rely on [git](https://git-scm.com/) and [GitHub](https://github.com/) heavily. This is how code (and often prose) is shared, backed up, and tracked over time. With an AI assistant writing code, a clean commit history becomes considerably more valuable.

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

## Setting up Claude Code

The rest of this chapter sets up Claude Code and the optional DunnLab plugin on your own computer.

### 1. Install Claude Code

There are a few ways to run Claude Code:

- **The Claude desktop application**, a dedicated graphical interface.
- **An extension in another tool**, such as the Claude Code extension for VS Code.
- **A command line program**, running in your terminal alongside your existing editor and tools.

I use the command line most often. It works in a wider variety of situations and gives clearer, more direct control, and it is where most developers use Claude Code — so it tends to be the most up to date and best supported interface. This manual assumes the command line throughout; if you are using another interface, the equivalent is usually easy to find.

Follow the official installation instructions at [Claude Code Overview](https://code.claude.com/docs/en/overview).

### 2. Install the plugin

Register the dunnlab marketplace and install the plugin:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

This pulls the plugin from GitHub and caches it locally. To pick up changes later, run `/plugin update dunnlab-code@dunnlab`. Auto-update is off by default for third-party marketplaces like this one, so nothing arrives on its own unless you enable it under `/plugin` → **Marketplaces**.

Note that methods for installing plugins differ when using the desktop app or extension.

### 3. Verify installation

Run the following slash command to confirm everything is wired up:

```
/dunnlab-code:dunnlab-check
```

You should see a welcome message and a list of available skills. Plugin skills are namespaced by the plugin name; the bare `/dunnlab-check` also works as long as nothing else has claimed that name.

### 4. Know what you already have

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

### 5. Install recommended plugins

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
