---
name: dunnlab-new-project
description: >
  Scaffold a new Dunn Lab repository or fill missing project setup: source and
  test directories, environment, README, and agent instructions. Use for project
  initialization, not ongoing development or scientific lifecycle management.
---

# Dunn Lab New Project Setup

Create the minimum useful scaffold for the requested project, preserving existing work. This skill owns setup and then hands off; it does not run an ongoing development lifecycle. Apply `dunnlab-defaults` for language, dependency, coding, and documentation conventions.

## Establish scope and inspect what exists

Infer the goal, language, project type, and expected inputs and outputs from the request and repository. Ask only for missing information that changes setup. Default to Python, use R when the needed packages warrant it, and Rust for performance-critical code. Do not require confirmation of an obvious choice or a separate planning approval when implementation is already authorized.

Inspect existing source, documentation, environment specifications, git state, and agent instructions. Complete only the missing setup relevant to the task; an existing analysis does not need a new repository or a restart of its lifecycle. Do not replace established layouts or permissions because they differ from a template.

A devcontainer is optional. Offer it when isolation would materially help and the preference is unknown; continue useful setup without one unless the user chooses it. Do not make container selection a universal pause.

## Repository and execution environment

- Initialize git when creating a repository and it is not already initialized. Preserve existing git configuration and work.
- Create or update `.gitignore` for the language and actual layout. Default ignores include `.DS_Store`, Python caches, notebook checkpoints, bulk data/results, and logs; preserve tracked fixtures and provenance records. Add `target/` for Rust and `.Rhistory`, `.RData`, `.Rproj.user/` for R where relevant.
- Preserve the active harness's permissions and sandbox policy. Configure permissions only when the user requests it. For requested Claude Code permission setup, read [references/settings-permissions.md](references/settings-permissions.md); do not translate or apply those settings to another harness automatically.
- If a devcontainer was chosen, use `dunnlab-devcontainer` for its configuration. If further work requires reopening in it, record the handoff and explain the needed action. Do not require a commit or context reset as part of scaffolding.

## Minimum documentation and directories

Create useful initial documentation from known information, leaving unresolved scientific choices explicit rather than inventing a detailed plan:

- **README.md**: project purpose, current setup and entry points, and links to developer checks. For scientific analyses, follow workflow-design's reader-facing documentation guidance. Add development-container instructions only when one is configured.
- **AGENTS.md**: a brief project summary, working/test commands, and links to relevant documentation; follow the 100-line limit in `dunnlab-defaults`. Reference companion skills only when they apply.
- **CLAUDE.md**: use the single line `@AGENTS.md` for a new shared-instructions setup. Preserve and reconcile existing instructions instead of overwriting them.
- **`dev_docs/overview.md`** when a plan is useful: goal, known inputs and outputs, current approach, and unresolved choices. For research, lifecycle Planning extends this same document; do not create a competing scientific plan here.
- **CONTRIBUTING.md** or additional focused `dev_docs/` documents only when their content warrants a separate home.

Use an idiomatic source layout (`scripts/` for analysis scripts, a package layout for reusable software) and add `notebooks/` when needed. Create test directories when there is behavior or a representative input to check; do not add placeholder tests merely to fill the scaffold. `dunnlab-workflow-design` owns workflow-specific organization, including data, results, and analysis entry points.

## Dependencies

Use the project's existing dependency mechanism when present. A specification's existence is not evidence that it builds; inspect it and verify the setup relevant to the task.

- **Python**: prefer conda or mamba and `environment.yml` with the project name, Python version, and initial dependencies. Use separate files in `env/` only when distinct tool requirements warrant them. If environment creation is within scope, create it with `conda env create -f environment.yml` or the mamba equivalent. Diagnose dependency conflicts and adjust the specification when needed; report an unresolved setup failure instead of marking it complete.
- **R**: use `renv`. For a new environment, initialize with `renv::init()`, install needed packages, and snapshot. Configure Bioconductor when needed, and document required system libraries.
- **Rust**: use `Cargo.toml` and cargo; initialize a crate only when the project needs one and it does not already exist.

Document environment setup before usage. When checking reconstruction, create an isolated environment with a distinct name or path; never delete or overwrite the user's working environment to prove reproducibility. Large downloads or unavailable services do not justify fabricating a successful setup check; record the concrete limitation and continue independent work within scope.

## Verify the scaffold and hand off

Verify what was created: dependency specifications parse, documented paths and commands match the files, and available starter code or a small representative case runs when execution is within scope. Run relevant formatting and tests for actual code changes. Do not require a full analysis, production hardening, or clean recomputation before scaffolding can finish.

Summarize the scaffold, checks performed, unresolved setup dependencies, and the next action. Continue already authorized work under the appropriate skill:

- **Scientific research goals**: `dunnlab-lifecycle` determines the current phase from existing evidence and extends the same plan.
- **Computational workflows and pipelines**: `dunnlab-workflow-design` supplies design and execution principles from the first exploration onward; add the relevant domain skill for methods and tool choices.
- **Ordinary software development**: `dunnlab-defaults` supplies coding and verification conventions.
- **Yale execution**: `dunnlab-hpc` supplies cluster and SLURM details when needed.

These routes can combine: a research pipeline uses lifecycle for scientific decisions and workflow-design for its computational implementation. A reusable CLI does not need research phase gates merely because it processes scientific data.

## Resume across sessions only when needed

For setup that spans sessions, keep a compact checklist and handoff in `.agent/new-project-progress.yaml` if the project has no equivalent. Record completed setup, unresolved decisions, and any devcontainer transition. Keep this record limited to scaffolding; lifecycle and ongoing implementation own their own evidence and tasks.

Read an existing `.agent/new-project-progress.yaml`, or legacy `.claude/new-project-progress.yaml` when that is the only record. Verify its notes against actual files and current scope; do not interpret old step numbers as commands to restart work or invoke the former build loop. No migration or new state file is required just to review or explain setup. Existing `devcontainer` and `in_devcontainer` fields can inform a pending handoff, but confirm the active environment before resuming dependent work.

Follow the user's scope and the project's version-control workflow. Scaffolding does not require automatic commits, repeated approval pauses, or a context reset after each step.
