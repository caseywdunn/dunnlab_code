---
name: dunnlab-new-project
description: >
  Step-by-step workflow for scaffolding a new Dunn Lab project from
  scratch. Use when creating a new analysis, tool, or pipeline. Sets
  up directory structure, environment, git, and documentation.
---

# Dunn Lab New Project Setup

Follow these steps when starting a new project from scratch. This skill references conventions from the `dunnlab-defaults` skill — apply those standards throughout.

## Progress tracking

This skill persists its progress to `.claude/new-project-progress.yaml` so it can resume after `/clear` or a new session.

### On first invocation (no progress file exists)

1. Inspect the repo to detect which steps have already been completed (e.g., README.md exists, git is initialized, `.devcontainer/` is present).
2. Build the initial task list and write it to `.claude/new-project-progress.yaml` with this format:

```yaml
# Dunn Lab new-project progress — do not edit manually
updated: 2024-01-15T10:30:00
devcontainer: true  # whether user opted for devcontainer
in_devcontainer: false  # whether currently running inside a devcontainer
tasks:
  - id: step-1
    name: Define the project scope
    status: completed  # completed | in-progress | pending | skipped
    notes: "Python RNA-seq pipeline"
  - id: step-2
    name: Initialize repo and configure permissions
    status: in-progress
    notes: ""
  # ... remaining steps
```

3. Load the task list into TodoWrite so it is visible during the session.

### On subsequent invocations (progress file exists)

1. Read `.claude/new-project-progress.yaml`.
2. Load it into TodoWrite.
3. Resume from the first task that is not `completed` or `skipped`.

### Keeping progress up to date

- When you finish a step, mark it `completed` in both TodoWrite and the progress file.
- When you start a step, mark it `in-progress`.
- If the plan changes (steps added, removed, reordered, or revised based on user feedback), update the progress file to reflect the new plan. The progress file is the durable source of truth; TodoWrite is the in-session view.
- Use the `notes` field to capture key decisions (e.g., chosen language, project type) so they survive across sessions.

---

## Phase 1: Bootstrap

The goal of this phase is to get the repo initialized and permissions configured as quickly as possible so that subsequent steps can run with minimal user intervention.

### Step 1: Define the project scope

Before writing any code, clarify with the user:

- **What is the goal?** (e.g., analyze single-cell RNA-seq data, build a phylogenetic pipeline, create a CLI tool)
- **What language(s) will be used?** (default to Python unless there's a reason for R or Rust)
- **What are the expected inputs and outputs?**
- **Will this be a one-off analysis, a reusable tool, or a package?**
- **Would they like to use a devcontainer?** Explain that devcontainers provide a reproducible, isolated environment via Docker and VS Code, but are optional. Record the choice in the progress file.

If there are problems with the user's plans (e.g., they suggest inappropriate tools, there are missing or unnecessary steps, there are better approaches, the data can't be used for this purpose, etc.), point out the issues and suggest better approaches.

Use the answers to guide decisions in the following steps.

### Step 2: Initialize repo and configure permissions

Do these in order — settings.json first so all subsequent tool calls benefit from the permissions:

1. **Initialize git** with `git init` (skip if already initialized).

2. **Create `.claude/settings.json`** with reasonable permissions for local development. Use `acceptEdits` as the default mode so file edits don't require individual approval. The settings should:
   - **Allow without prompting**: `Read(**)`, `Glob`, `Grep`, `Task`, read-only git commands (`git status`, `git log`, `git diff`, `git branch`, `git remote`, `git show`), read-only shell commands (`ls`, `cat`, `head`, `tail`, `wc`, `find`, `du`, `df`, `file`, `which`, `echo`, `pwd`, `tree`, `diff`), `curl` and `wget`, `python` and `python3`, `conda activate/deactivate/env list/list/info`, `mamba activate/deactivate/env list/list/info`, `pip list`, `pip show`
   - **Ask for confirmation**: `Edit(**)`, `Write(**)`, mutating git commands (`git push`, `git commit`, `git checkout`, `git merge`, `git rebase`, `git reset`, `git stash`, `git add`), package management (`conda install/create/remove/env create/env remove/update`, `mamba install/create/remove/env create/env remove/update`, `pip install`, `pip uninstall`), file operations (`cp`, `mv`, `rm`, `mkdir`, `rsync`), `chmod`, `WebFetch`
   - **Deny**: reading sensitive files (`.env`, `.env.*`, `.ssh/**`, `.netrc`, `*credentials*`, `*secret*`, `*token*`, `*.pem`, `*.key`, `.aws/**`), editing sensitive files (same patterns), destructive commands (`rm -rf /`, `sudo`, `su`, `shutdown`, `reboot`, `dd if=`), network probing (`ssh`, `nc`, `netcat`, `nmap`), process killing (`kill -9`, `killall`, `pkill`)
   Use the same rule syntax shown in `.claude/settings.json` examples from the managing-security docs. The goal is to let Claude work fluidly for reading and running code while requiring confirmation for anything that modifies files, installs packages, or touches git history.

3. **Create a minimal `.gitignore`** with `.DS_Store` and other common ignores. This will be expanded in a later step once the language and project type are known.

### Step 3: Set up devcontainer (optional)

If the user opted for a devcontainer in Step 1:

1. Use the `dunnlab-devcontainer` skill to add a `.devcontainer/` directory with the standard Claude Code devcontainer configuration.
2. Commit all bootstrap files (settings.json, .gitignore, .devcontainer/).
3. Tell the user to reopen the project in the devcontainer now — all remaining work should happen inside it. Update the progress file with `in_devcontainer: false` so that on the next invocation it can detect the transition.
4. **Stop here.** The user will start a new session inside the devcontainer and resume with Step 4.

If the user did not opt for a devcontainer:

1. Commit the bootstrap files (settings.json, .gitignore).
2. Continue directly to Step 4.

---

## Phase 2: Plan

### Step 4: Create project planning documentation

Before writing any code, create the following:

- **README.md** with a project title and placeholder sections for the overview, setup instructions, usage examples, and development notes. If using a devcontainer, include a "Development container" section explaining how to use it (install Docker and the VS Code Dev Containers extension, then reopen the project in the container).
- **`dev_docs/overview.md`** outlining the scientific question or engineering goal, key data sources and their formats, and the planned analysis workflow or architecture. This serves as a reference that can be loaded into context by Claude Code when working on relevant parts of the project.
- **Additional `dev_docs/` files** as needed to document the project (e.g., data model, analysis workflow, interpretation notes). These should be atomic and focused on specific aspects of the project, written so they can be loaded into context by Claude Code as needed. These serve as a guardrail on context.
- **CLAUDE.md** with a brief project summary, links to the above documentation, and any project-specific instructions for using Claude Code. Also specify to use the dunnlab-defaults skill for coding conventions and project structure.

Ask the user any clarifying questions needed to fill in these documents.

### Step 5: Review and finalize the plan

Once the planning documents are drafted:

1. Review the plan to make sure there aren't better options for the project structure, environment, or documentation based on the project scope and goals. This is a good time to catch any potential issues before scaffolding the project.
2. Prompt the user to ask if they would like to make any changes. If they want changes, help them iterate until they're satisfied.
3. Once the user confirms the plan is finalized, commit the planning documents to git.

---

## Phase 3: Scaffold and build

### Step 6: Create directory structure and update .gitignore

Scaffold the project following the `dunnlab-defaults` project structure. Always prefer idiomatic structures for the language and project type.

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

### Step 7: Set up the environment

- **Python**: Create `environment.yml` with the project name, Python version, and initial dependencies. Run `conda env create -f environment.yml` or `mamba env create -f environment.yml`.
- **R**: Initialize `renv` with `renv::init()`. Install initial packages and snapshot with `renv::snapshot()`.
- **Rust**: `Cargo.toml` is created by `cargo init`. Add dependencies as needed.

Include instructions for environment setup in README.md.

### Step 8: Enter development mode

Break development into atomic, manageable tasks. For example:
- Get the main function up with argument parsing and minimal external-facing interface (e.g., CLI, API).
- Implement core functionality with placeholder logic.
- Add error handling and edge case management.

Use an incremental approach. Once tasks are defined, start implementing them one by one. After each task:
- Run tests to verify functionality.
- Run linters and formatters to maintain code quality.
- Update documentation to reflect new functionality or changes.
- Commit changes with descriptive messages.

Do not move on to the next task until the current one is fully implemented, tested, and documented. This ensures a clean development process and prevents context overload. It is critical to not get too far ahead of yourself.

After completing each task, commit your changes and then run /clear before starting the next task.

### Step 9: Final verification

Run through this checklist when wrapping up:

- [ ] Environment can be created from scratch using the config file
- [ ] The starter script runs without errors
- [ ] Look over the project for performance issues, security concerns, or potential bugs. If a refactor is needed, break it into a new task and implement it before moving on.
- [ ] Tests pass
- [ ] Linters and formatters run clean
- [ ] README setup instructions are accurate and complete
- [ ] CLAUDE.md and dev_docs/ files are comprehensive and up to date
