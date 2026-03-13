---
title: Getting Started
nav_order: 2
---

# Getting Started

## AI in academic science

Generative AI changes how scientific work can be done, but it does not change the responsibilities of scientists and authors. The same scholarly standards apply as before — evaluate your sources, be skeptical, and review your own work carefully. You are accountable for everything you submit, whether you wrote it by hand or with AI assistance.

AI poses particular challenges for code. If you do not understand generated code well enough to review it, you cannot vouch for its correctness. For this reason, you still need to learn coding even when using AI tools for data analysis. These tools are most effective when you can read, evaluate, and modify what they produce.

AI also presents exciting opportunities for code. AI can help you work faster, explore further, and gain new insight. On the technical coding front, it can achieve better test coverage, perform regular automated code review, and learn new coding methods as you work. It can introduce errors you need to find, but it can also help find errors that you introduce manually.

Be cautious when using AI to directly transform data (e.g., reformatting tables or restructuring files). Always review the results, and prefer having AI write a script you can inspect and re-run rather than having it act directly on your data.

### Journal policies

Check your target journal's AI guidelines before starting a project. Policies vary, but common patterns include:

- Most journals allow AI for coding assistance but require disclosure of how it was used
- Many journals prohibit AI-generated text in manuscripts, or require specific disclosure
- Journals generally do not allow AI to be listed as an author — see [COPE's position on AI and authorship](https://publicationethics.org/news-opinion/artificial-intelligence-and-authorship)

Consult the specific guidelines early so you can plan your workflow and documentation accordingly.

### Funding agency policies

Many of the same considerations apply to writing grants as to writing manuscripts. Make sure you understand AI policy *before* you start writing a proposal for a particular funding agency.

## Setting up Claude Code

This guide walks you through setting up Claude Code with the Dunn Lab plugin.

## 1. Install Claude Code

Follow the official installation instructions at [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview). Claude Code runs in your terminal and works alongside your existing editor and tools.

## 2. Install the plugin

Register the dunnlab marketplace and install the plugin:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code
```

This pulls the plugin from GitHub and caches it locally. To update after changes are pushed, run `claude plugin update dunnlab-code`.

## 3. Verify installation

Run the following slash command to confirm everything is wired up:

```
/dunnlab-check
```

You should see a welcome message and a list of available skills.

## 4. What's in the plugin?

- **Skills** are sets of instructions that Claude loads when relevant. They encode lab conventions like preferred languages, file naming, and project structure. See the `skills/` directory.
- **Commands** are slash commands (like `/dunnlab-check`) that trigger specific Claude behaviors. See the `commands/` directory.
- **Hooks** are event-driven scripts that run automatically in response to Claude Code events (e.g., before a commit or after a file is created). See the `hooks/` directory.

Browse the [Data Analysis](data-analysis.md), [Managing Security](managing-security.md), and [Managing Context](managing-context.md) pages for more.

## 5. Install recommended marketplace skills

The Anthropic official plugin marketplace includes several skills that are useful for coding workflows. Install them via the `/plugin` command or the CLI:

```bash
claude plugin install <skill-name>@claude-plugins-official
```

Recommended skills:

| Skill | What it does |
|-------|-------------|
| **skill-creator** | Structured workflow for building new skills, running evaluations, and optimizing skill descriptions. Essential if you plan to create or refine skills for the lab. See [Creating and evaluating skills](managing-context.md#creating-and-evaluating-skills) for details. |
| **claude-api** | Guidance for building applications with the Claude API and Anthropic SDKs. Triggers automatically when your code imports `anthropic` or `@anthropic-ai/sdk`. |
| **simplify** | Reviews changed code for reuse, quality, and efficiency, then fixes issues it finds. Useful as a post-editing cleanup pass. |
| **mcp-builder** | Guide for creating MCP (Model Context Protocol) servers that let Claude interact with external services. Helpful if you're building tool integrations. |

You can browse all available marketplace plugins by running `/plugin` and selecting the marketplace view. Use `/context` to check which skills are loaded and their context cost.
