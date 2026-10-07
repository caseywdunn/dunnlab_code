---
title: Example Workflows
nav_order: 13
---

# Example Workflows

A complete walkthrough, from an empty directory to working code, combining what the previous chapters covered separately.

The skill below (`dunnlab-new-project`) is an optional Claude Code implementation of the pattern, not the pattern itself. Codex can follow the same workflow directly from a prompt and `AGENTS.md`. The transferable shape is: plan interactively, review before code exists, then let the agent implement autonomously against that plan.

## New project: from idea to working code

This workflow walks through the full lifecycle of starting a new project—from an empty folder to a working codebase written by Claude Code or Codex.

### 1. Create a project folder

Pick a location and create an empty directory for your project:

```bash
mkdir ~/repos/my-new-project
cd ~/repos/my-new-project
```

### 2. Plan and scaffold the project

Launch either agent in the new directory:

```bash
claude  # or: codex
```

With the DunnLab Claude Code plugin, invoke the scaffolding skill:

```
/dunnlab-new-project
```

Then provide the scope below. It explicitly requests a review before
implementation; this is a choice for this example, not an automatic effect
of invoking the skill. Use `dunnlab-research-lifecycle` for the scientific planning alongside
the scaffold. With Codex, or Claude Code without the plugin, provide the same scope
directly:

> Help me plan and scaffold this research project. Define the scientific question, inputs, outputs, tests, and verification gates with me. Create `README.md`, `.gitignore`, `AGENTS.md`, a one-line `CLAUDE.md` importing it, and `dev_docs/overview.md`. Do not implement the analysis until I have reviewed and committed the plan.

The agent then walks you through a structured planning process:

- **Define scope** — It asks about the scientific question, language choice, expected inputs and outputs, and whether this is a one-off analysis or reusable tool.
- **Scaffold the repo** — It creates a `README.md`, `.gitignore`, initializes Git, and documents the project dependencies and environment setup.
- **Create planning docs** — It generates `dev_docs/overview.md`, shared instructions in `AGENTS.md`, and the `CLAUDE.md` compatibility import.
- **Review the plan** — Before any code is written, you review the project plan and documentation together. This is the time to catch architectural issues or missing requirements.
- **Commit the plan** — Once you're satisfied, commit the scaffolding. This gives you a clean baseline to build from.

At this point you have a Git repository with a clear plan, environment setup, and no code yet. The documentation is the product-independent specification that will guide either agent's implementation.

### 3. Authenticate the agent and install optional tools

If you have not already signed in, authenticate on the computer where you will run the agent:

```bash
claude auth login  # Claude Code
codex              # Codex prompts for sign-in on first launch
```

For Claude Code, you can optionally install the DunnLab plugin:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

Verify it by launching Claude Code and running `/dunnlab-code:dunnlab-check`. Codex does not require this plugin to follow the committed plan and `AGENTS.md` instructions.

### 4. Launch the agent with autonomy

Use Claude Code's Auto mode or Codex's normal workspace sandbox:

```bash
claude --permission-mode auto
codex --sandbox workspace-write --ask-for-approval on-request
```

Both support long stretches of routine work while retaining review or sandbox controls. The exact interruptions and network defaults differ; inspect them with `/permissions` before starting.

### 5. Have the agent implement the project

With the planning documents already in place, ask the agent to implement
`dev_docs/overview.md`, evaluate its verification gates, and commit verified
milestones. For a scientific analysis with the DunnLab Claude Code plugin, use:

```
/dunnlab-research-lifecycle
```

Lifecycle selects the current scientific work; `dunnlab-workflow-design` guides
its computational structure from exploration onward, and `dunnlab-bioinformatics`
adds domain methods when relevant. For a software tool or package, ask for
implementation directly using `dunnlab-coding-defaults`. Invoke `dunnlab-new-project`
again only if setup remains unfinished. Either agent can follow the same committed
plan and evaluate routine gates without pausing for a new approval at each one.

The agent should:

- **Build incrementally** — one component at a time, with tests after each
- **Run linters and formatters** — maintaining code quality throughout
- **Update documentation** — keeping the README and docs in sync with the implementation
- **Commit after each milestone** — so you have a clean git history

Because the planning documents act as a specification, either agent can stay on track without constant guidance. `AGENTS.md` supplies the shared conventions; Claude Code can additionally use `dunnlab-coding-defaults` through its plugin.

### 6. Review and iterate

Once the agent finishes the initial implementation, review the results:

- Check the git log to see what was built and in what order
- Run the test suite to verify everything passes
- Read through the code to make sure it matches your expectations
- Try running the tool or analysis on real data

If anything needs changes, continue the current session or start a fresh session with specific refinement instructions.

### Why this workflow works

The key insight is separating **planning** from **implementation**:

- **Steps 1–2** happen interactively on your machine, with you guiding the project's direction and reviewing the plan.
- **Steps 3–4** set up authentication, any optional tools, and the agent's permissions and sandbox.
- **Step 5** proceeds autonomously, with the agent following the plan you approved.
- **Step 6** brings you back in to review the result.

This gives you control over *what* gets built while letting either agent handle *how* it gets built. See [Managing Security](managing-security.md) for choosing an appropriate system-level boundary for unattended work.
