---
title: Example Workflows
nav_order: 12
---

# Example Workflows

A complete walkthrough, from an empty directory to working code, combining what the previous chapters covered separately.

The skill names below (`dunnlab-new-project`, `dunnlab-devcontainer`) are an optional Claude Code implementation of the pattern, not the pattern itself. Codex can follow the same workflow directly from a prompt and `AGENTS.md`. The transferable shape is: plan interactively, review before code exists, then let the agent implement autonomously inside a container against that plan.

## New project: from idea to working code

This workflow walks through the full lifecycle of starting a new project—from an empty folder to a working codebase written by Claude Code or Codex inside a dev container.

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

With the DunnLab Claude Code plugin, run:

```
/dunnlab-new-project
```

With Codex, or with Claude Code without the plugin, ask for the same outcome directly:

> Help me plan and scaffold this research project. Define the scientific question, inputs, outputs, tests, and verification gates with me. Create `README.md`, `.gitignore`, `AGENTS.md`, a one-line `CLAUDE.md` importing it, `dev_docs/overview.md`, and an appropriate `.devcontainer/`. Do not implement the analysis until I have reviewed and committed the plan.

The agent then walks you through a structured planning process:

- **Define scope** — It asks about the scientific question, language choice, expected inputs and outputs, and whether this is a one-off analysis or reusable tool.
- **Scaffold the repo** — It creates a `README.md`, `.gitignore`, initializes Git, and adds a `.devcontainer/`. The `dunnlab-devcontainer` skill automates the Claude Code branch; Codex can create the equivalent files directly.
- **Create planning docs** — It generates `dev_docs/overview.md`, shared instructions in `AGENTS.md`, and the `CLAUDE.md` compatibility import.
- **Review the plan** — Before any code is written, you review the project plan and documentation together. This is the time to catch architectural issues or missing requirements.
- **Commit the plan** — Once you're satisfied, commit the scaffolding. This gives you a clean baseline to build from.

At this point you have a Git repository with a clear plan, a dev-container configuration, and no code yet. The documentation is the product-independent specification that will guide either agent's implementation.

### 3. Open the project in the dev container

Exit the agent session, then open the project in VS Code. You will be prompted to “Reopen in Container” (or use the Command Palette: `Dev Containers: Reopen in Container`). You can also use the CLI: `devcontainer up`.

A hardened container should use a default-deny firewall that allows only the services the chosen agent and project need. Anthropic's [Claude Code reference firewall](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh) is one starting point; a Codex container must instead allow the OpenAI authentication and API endpoints it uses. Have the agent enumerate and verify the allowlist before relying on it. See [Managing Security](managing-security.md) for the surrounding principle.

### 4. Authenticate the agent

The dev container is isolated and normally has no access to your host's authentication, so sign in inside it:

```bash
claude auth login  # Claude Code
codex              # Codex prompts for sign-in on first launch
```

Persist the chosen agent's configuration directory in a named volume if you want sign-in and settings to survive **Dev Containers: Rebuild Container**. Do not mount your entire host home directory.

For Claude Code, you can optionally install the DunnLab plugin:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

Verify it by launching Claude Code and running `/dunnlab-code:dunnlab-check`. Codex does not require this plugin to follow the committed plan and `AGENTS.md` instructions.

### 5. Launch the agent in the container with autonomy

Only after verifying that the container is disposable, properly mounted, and restricted to the necessary network destinations, either harness can run without its own approval layer:

```bash
claude --permission-mode bypassPermissions               # Claude Code
codex --dangerously-bypass-approvals-and-sandbox         # Codex
```

These settings remove the harness-level boundary so the agent can create files, run commands, install packages, and execute tests without stopping. **This is defensible only because the surrounding container supplies the boundary.** Never use either unrestricted mode on an ordinary host or shared system.

To keep a harness-level safety net, use Claude Code's Auto mode or Codex's normal workspace sandbox:

```bash
claude --permission-mode auto
codex --sandbox workspace-write --ask-for-approval on-request
```

Both support long stretches of routine work while retaining review or sandbox controls. The exact interruptions and network defaults differ; inspect them with `/permissions` before starting.

### 6. Have the agent implement the project

With the planning documents already in place, ask the agent to implement `dev_docs/overview.md`, stopping at each gate and committing each verified step. With the DunnLab Claude Code plugin, you can run the project skill again:

```
/dunnlab-new-project
```

The skill checks which steps have already been completed and moves into implementation. Codex can do the same directly from the committed plan.

The agent should:

- **Build incrementally** — one component at a time, with tests after each
- **Run linters and formatters** — maintaining code quality throughout
- **Update documentation** — keeping the README and docs in sync with the implementation
- **Commit after each milestone** — so you have a clean git history

Because the planning documents act as a specification, either agent can stay on track without constant guidance. `AGENTS.md` supplies the shared conventions; Claude Code can additionally use `dunnlab-defaults` through its plugin.

### 7. Review and iterate

Once the agent finishes the initial implementation, review the results:

- Check the git log to see what was built and in what order
- Run the test suite to verify everything passes
- Read through the code to make sure it matches your expectations
- Try running the tool or analysis on real data

If anything needs changes, continue inside the container or start a fresh session with specific refinement instructions.

### Why this workflow works

The key insight is separating **planning** from **implementation**:

- **Steps 1–2** happen interactively on your machine, with you guiding the project's direction and reviewing the plan. The dev container is scaffolded as part of step 2.
- **Steps 3–4** move into the container and set up agent authentication and any optional extensions there.
- **Steps 5–6** happen autonomously inside the isolated container, with the agent following the plan you approved.
- **Step 7** brings you back in to review the result.

This gives you control over *what* gets built while letting either agent handle *how* it gets built—inside a container where mistakes are cheap and reversible.
