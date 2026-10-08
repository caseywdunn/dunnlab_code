---
title: The Toolkit
nav_order: 4
---

# The Toolkit

Coding agents do not replace the ordinary tools of computational work; they use them. The agent runs commands in a shell, records its work with Git, shares it through GitHub, and writes Python, Markdown, and LaTeX. You do not need to master these tools before starting, but you should know what each one is for, so you can follow what the agent does and judge whether it is doing the right thing.

This chapter is a bill of materials: what each tool is, why we use it, and where to learn more. It is not a tutorial.

{: .note }
> **Ask the agent to teach you.**
>
> Agents are patient, knowledgeable tutors for every tool here, and they can read this manual. Give the agent this page and ask about the tool you want to understand, for example: *"Read https://dunnlab.org/dunnlab_code/toolkit.html, then explain what Git is and show me how I would use it in this project."* The agent then explains with the same framing as the manual, and can show you on your own files.

## Principles behind the choices

**Prefer industry-standard tools over domain-specific ones.** This single principle is behind most of the choices below. It lets you draw on the enormous investment industry makes in data tooling, it gives you skills that are useful outside academia, and it means that when something breaks, someone has already written about it. It also matters for agents: they work best with tools that are widely used, because those are the tools they have seen most.

**Work from the terminal.** We run agents and most tools from the command line, even while editing in an editor. An agent can run a command, read its complete output, retry it, and record what happened. A workflow that depends on clicking through a graphical interface is much harder for an agent to operate on its own.

**Keep work in plain text.** Prefer text formats whenever they can represent the work adequately: Markdown or LaTeX rather than Word documents, CSV or TSV rather than Excel workbooks, and scripts or configuration files rather than settings stored inside an application. Plain text can be searched, compared line by line, tracked by Git, and read and edited directly by agents, and it stays readable as software changes. Use a binary format when its features are genuinely needed, but keep the source of record in text.

The optional [`dunnlab-coding-defaults` skill](plugin.md#the-skills) encodes these preferences for Claude Code.

## The shell and terminal

**What it is.** The **shell** is a program that runs commands you type: listing files, moving them, starting programs, and combining small programs into larger tasks. The **terminal** is the window the shell runs in. On macOS and Linux the shell is usually `zsh` or `bash`.

**Why we use it.** The shell is how agents act on your computer. Nearly every scientific tool can be run from it, commands can be saved in scripts and rerun exactly, and the same commands work on your laptop, a lab server, or a cluster. You will mostly read commands rather than write them, so the useful skill is being able to tell what a command will do before approving it.

**Learn more:** [The Unix Shell](https://swcarpentry.github.io/shell-novice/) from Software Carpentry.

## Git

**What it is.** [Git](https://git-scm.com/) is a version-control system. It records the history of a project's files as a series of snapshots called **commits**, each with a message explaining the change. A project tracked by Git is a **repository**. Git can also keep parallel lines of work, called **branches**, and **merge** them back together.

**Why we use it.** Git is how you can let an agent make changes without fear: any change can be inspected, compared with what came before, and undone. The commit history is also a record of how the project reached its current state, including the work you delegated to AI. Let the agent make a small commit after each verified step and write the message explaining why the change was made.

Git is designed for code and other small text files, not data. Do not store large data files or analysis results in a repository. GitHub blocks any single file over 100 MB, and a well-kept analysis repository is usually far smaller than that.

**Learn more:** [Version Control with Git](https://swcarpentry.github.io/git-novice/) from Software Carpentry, and the free book [Pro Git](https://git-scm.com/book).

## GitHub

**What it is.** [GitHub](https://github.com/) hosts Git repositories online. Beyond storing a copy, it adds tools for working together: **issues** for tracking tasks, **pull requests** for proposing and reviewing changes, and **actions** that run checks such as tests automatically on every change.

**Why we use it.** GitHub is the backbone of how we share and coordinate work. Treat the repository as the project's durable workspace: the plan is a file in it, code and documentation evolve beside it, issues record work not yet done, and commits record verified steps. People and agents then share the same history. [Software Engineering](software-engineering.md) describes how issues, branches, and releases fit together.

Install the [GitHub CLI](https://cli.github.com/) (`gh`) and authenticate it once with `gh auth login`. The agent can then create repositories, file and close issues, and open pull requests from the terminal. Authentication lets the agent act under your account, so do this only in an environment you trust.

**Learn more:** [GitHub's getting-started guide](https://docs.github.com/en/get-started/start-your-journey/about-github-and-git).

## Visual Studio Code

**What it is.** [Visual Studio Code](https://code.visualstudio.com/) (VS Code) is a free code editor. It shows a project's files, highlights code, displays Git changes, and has a built-in terminal.

**Why we use it.** It puts the files, the terminal, and Git changes in one window, which makes it easy to watch and review what an agent is doing. Its extensions support every language here, and its Remote SSH extension edits files on another computer as if they were local. Both [Claude Code](https://code.claude.com/docs/en/vs-code) and [Codex](https://learn.chatgpt.com/docs/codex/ide) integrate with it, but we still run agents in the terminal.

**Learn more:** [VS Code documentation](https://code.visualstudio.com/docs).

## Python

**What it is.** [Python](https://www.python.org/) is a general-purpose programming language, and our default for data analysis and scripting.

**Why we use it.** Python is one of the most widely used languages in the world, in industry as well as science. Its libraries cover data handling, statistics, machine learning, plotting, and bioinformatics, and Python skills transfer far beyond biology. Agents also write it especially well, because so much Python exists to learn from.

Its usual companions:

- **[conda](https://docs.conda.io/)** or **[mamba](https://mamba.readthedocs.io/)** install Python and other software into separate **environments**, so each project gets the versions it needs without interfering with others. [Bioconda](https://bioconda.github.io/) provides thousands of bioinformatics tools this way.
- **[Jupyter](https://jupyter.org/) notebooks** mix code, results, and notes in one document. They are good for exploration; reusable analysis usually moves into scripts or a workflow.
- **[Ruff](https://docs.astral.sh/ruff/)** formats and checks Python code. [Software Engineering](software-engineering.md#linting-and-formatting) explains why that matters.

**Learn more:** the [official Python tutorial](https://docs.python.org/3/tutorial/), and the free [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/).

## R

**What it is.** [R](https://www.r-project.org/) is a language built for statistics, widely used in biology.

**Why we use it.** R is the right choice when an analysis needs packages that exist only there, such as Seurat or much of [Bioconductor](https://bioconductor.org/), when it is what you know and it works, or when you join a team that has chosen it. Using R in those cases is a normal outcome, not a failure. Otherwise we prefer Python, because R is a niche language by comparison and its skills travel less far.

**Learn more:** the free book [R for Data Science](https://r4ds.hadley.nz/).

## Rust

**What it is.** [Rust](https://www.rust-lang.org/) is a programming language for fast, reliable software.

**Why we use it.** For tools where speed and memory use dominate, such as processing billions of sequencing reads, Rust runs far faster than Python. Its strict compiler catches many mistakes before the program ever runs, which suits agent-written code: much of the checking happens automatically. Most analyses never need it.

**Learn more:** [The Rust Programming Language](https://doc.rust-lang.org/book/), the official free book.

## Markdown

**What it is.** Markdown is a lightweight way to format plain text: `#` for headings, `*asterisks*` for emphasis, `-` for bullet lists. The file stays readable as plain text, and tools render it as formatted pages. This manual is written in Markdown.

**Why we use it.** Markdown is the format for everything in a project that is not code or a manuscript: README files, plans, notes, and agent instructions such as `AGENTS.md`. It is easy to write, easy for agents to read and edit, and displayed nicely on GitHub.

**Learn more:** [GitHub's guide to writing Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

## LaTeX

**What it is.** [LaTeX](https://www.latex-project.org/) is a typesetting system. You write plain text with commands such as `\section{Methods}` or `\cite{dunn2008}`, and LaTeX produces a professionally typeset PDF.

**Why we use it.** LaTeX is our format for manuscripts. Its source is plain text, so Git tracks every change and agents can edit it directly. Many journals provide LaTeX templates. It handles citations, equations, and cross-references well. And it can include numbers, tables, and figures generated directly by the analysis code, so the manuscript never contains results copied by hand. Co-authors who prefer Word can receive a converted copy. [Dunn Lab Practices](lab-practices.md#manuscripts) describes how we do this.

**Learn more:** [Overleaf's LaTeX documentation](https://www.overleaf.com/learn).

## Quarto

**What it is.** [Quarto](https://quarto.org/) creates documents in which code and text are mixed: the code runs when the document is built, and its results appear in place. It produces HTML, PDF, and Word.

**Why we use it.** Quarto suits documents where the analysis is the document, such as analysis reports, supplementary reports, internal summaries, and tutorials. There, every result is computed by code in plain view, and rebuilding updates everything. For manuscripts we prefer LaTeX, which gives finer control over typesetting and journal templates.

**Learn more:** the [Quarto guide](https://quarto.org/docs/guide/).

## Elsewhere in this manual

- **SSH and tmux,** for working on other computers and keeping sessions alive: [Working Across Computers](working-across-computers.md).
- **Snakemake,** for multi-step analyses: [Software Engineering](software-engineering.md#workflow-frameworks).
