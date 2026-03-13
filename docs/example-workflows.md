---
title: Example Workflows
nav_order: 8
---

# Example Workflows

Step-by-step walkthroughs for common tasks in the lab. Each workflow combines multiple skills and tools into a complete process you can follow from start to finish.

## New project: from idea to working code

This workflow walks through the full lifecycle of starting a new project — from an empty folder to a working codebase written by Claude inside a dev container.

### 1. Create a project folder

Pick a location and create an empty directory for your project:

```bash
mkdir ~/repos/my-new-project
cd ~/repos/my-new-project
```

### 2. Scaffold the project with `/dunnlab-new-project`

Launch Claude Code in the new directory:

```bash
claude
```

Then run the skill:

```
/dunnlab-new-project
```

Claude will walk you through a structured planning process:

- **Define scope** — Claude asks about the scientific question, language choice, expected inputs/outputs, and whether this is a one-off analysis or reusable tool.
- **Scaffold the repo** — Claude creates a `README.md`, `.gitignore`, and initializes git. It also adds a `.devcontainer/` directory using the `dunnlab-devcontainer` skill, which provides a secure, pre-configured container with Claude Code, a restrictive firewall, and VS Code integration.
- **Create planning docs** — Claude generates `documentation/overview.md` with the scientific question and planned workflow, and a `CLAUDE.md` that ties everything together.
- **Review the plan** — Before any code is written, you review the project plan and documentation together. This is the time to catch architectural issues or missing requirements.
- **Commit the plan** — Once you're satisfied, commit the scaffolding. This gives you a clean baseline to build from.

At this point you have a git repo with a clear plan, a dev container configuration, and no code yet. The documentation acts as a specification that will guide Claude's implementation.

### 3. Open the project in the dev container

Exit your Claude session, then open the project in VS Code. You'll be prompted to "Reopen in Container" (or use the Command Palette: `Dev Containers: Reopen in Container`). You can also use the CLI: `devcontainer up`.

The container includes a [firewall](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh) that restricts outbound network access to only necessary services (GitHub, npm, Anthropic API, VS Code). This default-deny policy is what makes it safe to run Claude with permissions bypassed. See [Managing Security](managing-security.md) for details.

### 4. Launch Claude in the container with full autonomy

Once you're inside the running dev container, open a terminal in VS Code and launch Claude with the plugin and permissions bypassed:

```bash
claude --plugin-dir /path/to/dunnlab_code --dangerously-skip-permissions
```

The `--dangerously-skip-permissions` flag disables all permission prompts, so Claude can create files, run commands, install packages, and execute tests without asking for approval on each step. **This is safe here because the dev container is disposable** — it cannot touch your host filesystem, credentials, or other projects. See [Managing Security](managing-security.md) for why you should never use this flag outside of an isolated container.

### 5. Have Claude implement the project

With the planning docs already in place from step 2, Claude has all the context it needs. Tell it to start building:

```
Implement the project according to the plan in documentation/overview.md.
Work through it incrementally — implement one component at a time, test it,
then move on to the next.
```

Claude will follow the `dunnlab-new-project` development workflow:

- **Build incrementally** — one component at a time, with tests after each
- **Run linters and formatters** — maintaining code quality throughout
- **Update documentation** — keeping the README and docs in sync with the implementation
- **Commit after each milestone** — so you have a clean git history

Because the planning docs act as a specification, Claude stays on track without needing constant guidance. The `CLAUDE.md` file points it to the `dunnlab-defaults` skill for coding conventions, so the generated code follows lab standards.

### 6. Review and iterate

Once Claude finishes the initial implementation, review the results:

- Check the git log to see what was built and in what order
- Run the test suite to verify everything passes
- Read through the code to make sure it matches your expectations
- Try running the tool or analysis on real data

If anything needs changes, you can continue the conversation inside the container or start a new Claude session with specific instructions for refinements.

### Why this workflow works

The key insight is separating **planning** from **implementation**:

- Steps 1–2 happen interactively, with you guiding the project's direction and reviewing the plan. The dev container is scaffolded automatically as part of step 2.
- Steps 4–5 happen autonomously inside the isolated container, with Claude following the plan you approved.

This gives you control over *what* gets built while letting Claude handle *how* it gets built — safely, inside a container where mistakes are cheap and reversible.
