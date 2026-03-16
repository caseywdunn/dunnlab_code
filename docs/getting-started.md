---
title: Getting Started
nav_order: 2
---

# Getting Started

This manual is not a comprehensive guide to the tools we use in the lab. It is a formalization of the stack of tools we use so you know where to get started, with some lab-specific information. 

There are many excellent resources for learning about all the technologies mentioned here. To learn more about them, ask your favorite LLM, consult the documentation, and find some tutorials.

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

## Conventions

When possible, we use industry-standard tools rather than domain-specific tools. This lets us tap into the massive investment industry makes in data analysis tools, and gives you skills that are the most portable. There are also many more resources available for learning widely used tools.

The plugin's `dunnlab-defaults` skill encodes these preferences (along with best practices for each language) so that Claude applies them automatically when writing code.

### IDE

We use [Visual Studio Code](https://code.visualstudio.com/) as our Interactive Development Environment (IDE). It has excellent extensions that integrate git, GitHub access, Claude, and language-specific tools. I spend most of my time at the computer in this program.

### Version control

We rely on [git](https://git-scm.com/) and [GitHub](https://github.com/) extensively for code version control. This is how we share code, back it up, and keep track of progress.

Do not store large data files or analysis results in git repositories. It is designed for small files (often text), and your entire repository optimally stays under 100MB.

### Languages

We default to **[Python](https://www.python.org/)** (3.10+) for data analysis and scripting. We fall back to **R** when analyses require specific R libraries (e.g., Seurat). Though R is common in biology, it is a niche language compared to Python. R is still an excellent choice when you need libraries and resources only available in the language, it is what you are comfortable with and it works for you, or when working with a team that has chosen to use R.

I highly recommend [Python Data Science Handbook: Essential Tools for Working with Data](https://www.oreilly.com/library/view/python-data-science/9781098121211/) as an introduction to data analysis with Python. It is also [available online](https://jakevdp.github.io/PythonDataScienceHandbook/).

Other conventions regarding Python:

- Use **[conda](https://docs.conda.io/)** or **[mamba](https://mamba.readthedocs.io/)** for environment management
- Use **[Jupyter](https://jupyter.org/) notebooks** for exploratory work; refactor into scripts for production
- Use **[Quarto](https://quarto.org/)** for executable manuscripts

We prefer **[Rust](https://www.rust-lang.org/)** when writing code where performance is a top concern.

## High performance computing

We make extensive use of Yale's excellent High Performance Computing (HPC) resources at [YCRC](https://docs.ycrc.yale.edu/clusters/). They have detailed [documentation](https://docs.ycrc.yale.edu/clusters-at-yale/) on using the clusters, including the [SLURM](https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/) system you will use to launch and run analyses.

You will interact with the clusters mostly (or entirely) with [OOD](https://docs.ycrc.yale.edu/clusters-at-yale/access/ood/#remote-desktop).

We use McCleary for all analyses that touch raw sequence data. We use Bouchet for all other analyses.

## Setting up Claude Code

This guide walks you through setting up Claude Code on your own computer with the Dunn Lab plugin. The plugin helps Claude follow conventions in the lab and speed development.

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

You can browse all available marketplace plugins by running `/plugin` and selecting the marketplace view. Use `/context` to check which skills are loaded and their context cost.
