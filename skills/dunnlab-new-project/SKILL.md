---
name: dunnlab-new-project
description: >
  Step-by-step workflow for scaffolding a new Dunn Lab project from
  scratch. Use when creating a new analysis, tool, or pipeline. Sets
  up directory structure, environment, git, and documentation.
---

# Dunn Lab New Project Setup

Follow these steps when starting a new project from scratch. This skill references conventions from the `dunnlab-defaults` skill — apply those standards throughout.

## Step 1: Define the project scope

Before writing any code, clarify with the user:

- **What is the goal?** (e.g., analyze single-cell RNA-seq data, build a phylogenetic pipeline, create a CLI tool)
- **What language(s) will be used?** (default to Python unless there's a reason for R or Rust)
- **What are the expected inputs and outputs?**
- **Will this be a one-off analysis, a reusable tool, or a package?**

Use the answers to guide decisions in the following steps.

## Create README.md stub and .gitignore

Create a README.md with a project title and placeholder sections for the overview, setup instructions, usage examples, and development notes. This will be fleshed out in later steps but serves as a starting point.

Create a .gitignore with .DS_Store and other common ignores.

Initialize git repository with `git init`.

Use the `dunnlab-devcontainer` skill to add a `.devcontainer/` directory with the standard Claude Code devcontainer configuration. Add a "Development container" section to README.md explaining how to use it (install Docker and the VS Code Dev Containers extension, then reopen the project in the container).


## Step 1.5: Create project planning documentation

Before writing any code, create the following:
- README.md with a project overview and setup instructions
 `documentation/overview.md` file that outlines the scientific question or engineering goal, key data sources and their formats, and the planned analysis workflow or architecture. This serves as a reference for the project and can be loaded into context by Claude Code when working on relevant parts of the project.
- Any other documentation/ files needed to document the project (e.g., data model, analysis workflow, interpretation notes). These should be atomic and focused on specific aspects of the project, and should be written in a way that they can be loaded into context by Claude Code when working on relevant parts of the project. The goal is to have a comprehensive set of documentation that covers all aspects of the project and can be easily referenced by both humans and Claude Code as needed. These serve as a guardrail on context.
- CLAUDE.md with a brief project summary, links to the above documentation, and any project-specific instructions for using Claude Code. Also specify to use the dunnlab-defaults skill for coding conventions and project structure.

Ask the user any clarifying questions needed to fill in these documents. 

Once finalized, review the plan to make sure there aren't better options for the project structure, environment, or documentation based on the project scope and goals. This is a good time to catch any potential issues before scaffolding the project.

Then prompt the user to ask to commit and move on to the next steps. This ensures they have a clear plan and reference documentation before writing any code, which will help guide development and keep things organized from the start.


## Step 2: Create the remaining directory structure

Scaffold the project following the `dunnlab-defaults` project structure. Always prefer idiomatic structures for the language and project type.

## Step 3: Update version control



Update `.gitignore` as appropriate for the languages in the project. Always exclude:

```
data/
results/
*.pyc
__pycache__/
.ipynb_checkpoints/
.DS_Store
```

Add language-specific ignores (e.g., `target/` for Rust, `.Rhistory` for R).

## Step 4: Set up the environment

- **Python**: Create `environment.yml` with the project name, Python version, and initial dependencies. Run `conda env create -f environment.yml` or `mamba env create -f environment.yml`.
- **R**: Initialize `renv` with `renv::init()`. Install initial packages and snapshot with `renv::snapshot()`.
- **Rust**: `Cargo.toml` is created by `cargo init`. Add dependencies as needed.

Include instructions for environment setup in README.md.



## Step 6: Enter development mode

Break development into atomic, manageable tasks. For example:
- Get the main function up with arguments parsing and minimal external facing interface (e.g., CLI, API).
- Implement core functionality with placeholder logic.
- Add error handling and edge case management.

Use an incremental approach. Once tasks are defined, start implementing them one by one. After each task:
- Run tests to verify functionality.
- Run linters and formatters to maintain code quality.
- Update documentation to reflect new functionality or changes.
- commit changes with descriptive messages.

Do not move on to the next task until the current one is fully implemented, tested, and documented. This ensures a clean development process and prevents context overload. It is critical to not get too far ahead of yourself.

After completing each task, commit your changes and then run /clear before starting the next task.


## Step 7: Final verification

Run through this checklist when wrapping up:

- [ ] Environment can be created from scratch using the config file
- [ ] The starter script runs without errors
- [ ] Look over the project for performance issues, security concerns, or potential bugs. If a refactor is needed, break it into a new task and implement it before moving on.
- [ ] Tests pass
- [ ] Linters and formatters run clean
- [ ] README setup instructions are accurate and complete
- [ ] CLAUDE.md and documentation/ files are comprehensive and up to date
