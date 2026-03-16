---
name: dunnlab-new-project
description: >
  Step-by-step workflow for scaffolding a new Dunn Lab project from
  scratch. Use whenever starting a new analysis, pipeline, tool, or
  package — including when the user says "new project", "set up a repo",
  "start a new analysis", "initialize a project", or asks to create
  project structure, directory layout, or boilerplate for a new codebase.
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
2. If `devcontainer: true` and `in_devcontainer: false`, check whether you're now inside a container (e.g., `/.dockerenv` exists or `$REMOTE_CONTAINERS` is set). If so, update `in_devcontainer: true` in the progress file — this confirms the user successfully reopened in the devcontainer and you can continue to Phase 2.
3. Load it into TodoWrite.
4. Resume from the first task that is not `completed` or `skipped`.

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

2. **Create `.claude/settings.json`** with reasonable permissions for local development. Use `acceptEdits` as the default mode so file edits don't require individual approval — this lets Claude work fluidly for reading and running code while still requiring confirmation for file modifications, package installs, and git mutations. Read `references/settings-permissions.md` for the full permission rules (allow, ask, deny), then generate the settings file using the same rule syntax shown in `.claude/settings.json` examples from the managing-security docs.

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

- **README.md** with a project title and placeholder sections for the overview, setup instructions, usage examples, and development notes. If `devcontainer: true` in the progress file, include a "Development container" section explaining how to use it (install Docker and the VS Code Dev Containers extension, then reopen the project in the container).
- **`dev_docs/overview.md`** outlining the scientific question or engineering goal, key data sources and their formats, and the planned analysis workflow or architecture. This serves as a reference that can be loaded into context by Claude Code when working on relevant parts of the project.
- **Additional `dev_docs/` files** as needed to document the project (e.g., data model, analysis workflow, interpretation notes). Keep each file atomic and focused on a single topic — this way Claude Code can load only the relevant file into context rather than pulling in the entire project's documentation, which helps stay within the context window on larger projects.
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

Add language-specific ignores (e.g., `target/` for Rust; `.Rhistory`, `.RData`, `.Rproj.user/` for R).

### Step 7: Set up the environment

- **Python**: Create `environment.yml` with the project name, Python version, and initial dependencies. Run `conda env create -f environment.yml` or `mamba env create -f environment.yml`.
- **R**: Initialize `renv` with `renv::init()`. Install initial packages and snapshot with `renv::snapshot()`. If the project needs Bioconductor packages, configure the Bioconductor repository in `renv` before installing them.
- **Rust**: `Cargo.toml` is created by `cargo init`. Add dependencies as needed.

Include instructions for environment setup in README.md.

### Step 8: Enter development mode

Read `dev_docs/overview.md` and the project scope notes from the progress file, then break development into atomic tasks tailored to the project type. The decomposition depends on what's being built:

- **Analysis/pipeline**: first task gets a minimal end-to-end pipeline running (read input → stub processing → write output), then subsequent tasks fill in each processing step.
- **CLI tool**: first task sets up argument parsing and the entry point, then subsequent tasks implement each subcommand or feature.
- **Package/library**: first task defines the public API with stub implementations and a test file, then subsequent tasks implement each function.

Write these tasks into the progress file and TodoWrite. Then implement them one by one. After each task:
- Run tests to verify functionality.
- Run linters and formatters to maintain code quality.
- Update documentation to reflect new functionality or changes.
- Commit changes with descriptive messages.

Do not move on to the next task until the current one is fully implemented, tested, and documented. Each task should be small enough to complete in a single session — this prevents context overload and keeps diffs reviewable.

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
