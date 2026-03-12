---
title: Getting Started
nav_order: 2
---

# Getting Started

This guide walks you through setting up Claude Code with the Dunn Lab plugin.

## 1. Install Claude Code

Follow the official installation instructions at [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview). Claude Code runs in your terminal and works alongside your existing editor and tools.

## 2. Clone this repo

```bash
git clone https://github.com/dunnlab/dunnlab_code.git
```

Put it somewhere stable on your machine — the plugin registration points to this directory.

## 3. Register the plugin

```bash
claude plugin add /path/to/dunnlab_code
```

Replace `/path/to/dunnlab_code` with the actual path where you cloned the repo.

## 4. Verify installation

Run the following slash command to confirm everything is wired up:

```
/lab-check
```

You should see a welcome message and a list of available skills.

## 5. What's in the plugin?

- **Skills** are sets of instructions that Claude loads when relevant. They encode lab conventions like preferred languages, file naming, and project structure. See the `skills/` directory.
- **Commands** are slash commands (like `/lab-check`) that trigger specific Claude behaviors. See the `commands/` directory.
- **Hooks** are event-driven scripts that run automatically in response to Claude Code events (e.g., before a commit or after a file is created). See the `hooks/` directory.

Browse the [Data Analysis](data-analysis.md), [Managing Security](managing-security.md), and [Managing Context](managing-context.md) pages for more.
