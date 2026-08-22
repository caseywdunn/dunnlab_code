---
title: Example Workflows
nav_order: 7
---

# Example Workflows

A complete walkthrough, from an empty directory to working code, combining what the previous chapters covered separately.

The skill names below (`dunnlab-new-project`, `dunnlab-devcontainer`) are this lab's instance of the pattern, not the pattern itself. The shape — plan interactively, review before any code exists, then let the assistant implement autonomously inside a container against that plan — is what transfers. Substitute your own skills, or none, and the sequence still holds.

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
- **Scaffold the repo** — Claude creates a `README.md`, `.gitignore`, and initializes git. It also adds a `.devcontainer/` directory using the `dunnlab-devcontainer` skill. That skill offers two configurations: a standard one built on the official Claude Code dev container feature, and a hardened one that adds a default-deny egress firewall. Pick the hardened variant for this workflow — the firewall is much of what makes step 5 defensible.
- **Create planning docs** — Claude generates `dev_docs/overview.md` with the scientific question and planned workflow, and a `CLAUDE.md` that ties everything together.
- **Review the plan** — Before any code is written, you review the project plan and documentation together. This is the time to catch architectural issues or missing requirements.
- **Commit the plan** — Once you're satisfied, commit the scaffolding. This gives you a clean baseline to build from.

At this point you have a git repo with a clear plan, a dev container configuration, and no code yet. The documentation acts as a specification that will guide Claude's implementation.

### 3. Open the project in the dev container

Exit your Claude session, then open the project in VS Code. You'll be prompted to "Reopen in Container" (or use the Command Palette: `Dev Containers: Reopen in Container`). You can also use the CLI: `devcontainer up`.

The hardened container includes a [firewall](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh) that restricts outbound network access to only the services it needs (GitHub, npm, the Anthropic API, conda, PyPI, VS Code). This default-deny policy is what makes it defensible to run Claude with permissions bypassed. See [Managing Security](managing-security.md) and the [devcontainer guide](https://code.claude.com/docs/en/devcontainer) for details.

### 4. Authenticate Claude and install the plugin

The dev container is isolated and has no access to your host's authentication, so you sign in inside it:

```bash
claude auth login
```

Or just run `claude` and follow the prompt. Because the `dunnlab-devcontainer` configuration mounts a named volume at `~/.claude` and points `CLAUDE_CONFIG_DIR` at it, your sign-in survives a **Dev Containers: Rebuild Container** — you log in once per project, not once per rebuild.

Next, add the dunnlab marketplace and install the plugin so all lab skills are available:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

This pulls the plugin from GitHub and caches it inside the container. Verify it by launching Claude and running `/dunnlab-code:dunnlab-check`.

### 5. Launch Claude in the container with full autonomy

With authentication and the plugin in place, launch Claude with permissions bypassed:

```bash
claude --permission-mode bypassPermissions
```

`bypassPermissions` mode (equivalent to the older `--dangerously-skip-permissions` flag) disables permission prompts, so Claude can create files, run commands, install packages, and execute tests without stopping for approval. **This is defensible here because the container is disposable and its egress is restricted** — it cannot touch your host filesystem, credentials, or other projects. See [Managing Security](managing-security.md) for why you should never use this mode outside an isolated container.

If you would rather keep a safety net, use `auto` mode instead:

```bash
claude --permission-mode auto
```

It is now the default mode on Pro, Max, and Team plans. You still get long uninterrupted stretches of work, but a classifier reviews each action before it runs. The cost is a little latency on shell and network commands.

### 6. Have Claude implement the project

With the planning docs already in place from step 2, Claude has all the context it needs. Run the new project skill again:

```
/dunnlab-new-project
```

The skill checks which steps have already been completed and picks up where you left off. Since the planning docs and scaffolding are already in place from step 2, Claude will move straight into implementation.

Claude will follow the `dunnlab-new-project` development workflow:

- **Build incrementally** — one component at a time, with tests after each
- **Run linters and formatters** — maintaining code quality throughout
- **Update documentation** — keeping the README and docs in sync with the implementation
- **Commit after each milestone** — so you have a clean git history

Because the planning docs act as a specification, Claude stays on track without needing constant guidance. The `CLAUDE.md` file points it to the `dunnlab-defaults` skill for coding conventions, so the generated code follows lab standards.

### 7. Review and iterate

Once Claude finishes the initial implementation, review the results:

- Check the git log to see what was built and in what order
- Run the test suite to verify everything passes
- Read through the code to make sure it matches your expectations
- Try running the tool or analysis on real data

If anything needs changes, you can continue the conversation inside the container or start a new Claude session with specific instructions for refinements.

### Why this workflow works

The key insight is separating **planning** from **implementation**:

- **Steps 1–2** happen interactively on your machine, with you guiding the project's direction and reviewing the plan. The dev container is scaffolded as part of step 2.
- **Steps 3–4** move into the container and set up authentication and the plugin there.
- **Steps 5–6** happen autonomously inside the isolated container, with Claude following the plan you approved.
- **Step 7** brings you back in to review the result.

This gives you control over *what* gets built while letting Claude handle *how* it gets built — safely, inside a container where mistakes are cheap and reversible.
