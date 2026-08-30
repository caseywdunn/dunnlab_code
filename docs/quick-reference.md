---
title: Quick Reference
nav_order: 3
---

# Quick Reference

Everything you need to get going, on one page. Each section links to the chapter that explains why.

## Set up

**Before you install, decide where this will run.** Your everyday machine, a separate user account on it, a container, a virtual machine, or a dedicated machine. This is much easier to choose now than to retrofit later, and the more autonomy you plan to give an agent, the more that choice has to carry. → [System-level control](managing-security.md#system-level-control)

```bash
# Install Claude Code, Codex, or both (macOS and Linux)
curl -fsSL https://claude.ai/install.sh | bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh

# Start either agent from your project directory
cd ~/repos/my-project
claude  # or: codex
```

The DunnLab plugin is an optional Claude Code implementation of this manual's conventions. Install it with:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab
```

Codex can follow the same durable project guidance from `AGENTS.md`; [Getting Started](getting-started.md) covers both paths.

Also install the [GitHub CLI](https://cli.github.com/) and run `gh auth login` so the agent can work with repositories, issues, pull requests, and checks from the terminal.

Useful orientation commands differ by harness:

| Need | Claude Code | Codex |
|---|---|---|
| Session status | `/status` | `/status` |
| Loaded context or instructions | `/context` | `/status`; inspect `AGENTS.md` |
| Permissions | `/permissions` | `/permissions` |
| Help | `/help` | `/help` |
| DunnLab plugin check | `/dunnlab-code:dunnlab-check` | Not applicable |

**Once it runs, set your own defaults.** Claude Code uses `~/.claude/settings.json`; Codex uses `~/.codex/config.toml`. Put shared project guidance in `AGENTS.md`, with a one-line `CLAUDE.md` import for Claude Code. Deciding these once beats re-deciding them every session. → [Harness-level control](managing-security.md#harness-level-control), [Managing Context](managing-context.md)

→ [Getting Started](getting-started.md)

## A working session

The rhythm matters more than the prompting. In rough order:

1. **Start with planning, not edits.** Describe what you want and let the agent propose an approach before it writes anything. This is the cheapest place to catch a wrong direction.
2. **Review the plan, then approve it.** For substantial work, have the agent write it to `PLAN.md` or `dev_docs/overview.md` in the repository and commit it before implementation.
3. **Work in small, verifiable steps.** A change too large to read carefully was too large to ask for in one go.
4. **Let the agent run the code.** Do not paste error messages—ask it to run the thing and read the error itself.
5. **Commit after each verified step**, and let the agent write the message.
6. **Start fresh before the next task.** A stale conversation makes everything worse.

→ [Working Effectively](working-effectively.md)

## Permissions

Claude Code and Codex expose the same two ideas—what can technically run and when the agent must ask—through different controls:

| Goal | Claude Code | Codex |
|---|---|---|
| Inspect and plan | Plan mode | `read-only` sandbox |
| Normal local work | Accept edits or Auto | `workspace-write` sandbox with `on-request` approvals |
| Change interactively | `Shift+Tab` or `/permissions` | `/permissions` |
| Unrestricted inside trusted isolation | `bypassPermissions` | `danger-full-access` with approvals bypassed |

Use the least privileged configuration that still lets routine work proceed without babysitting. → [Managing Security](managing-security.md), [Coding Agents](other-agents.md#permissions)

## Sessions

Both agents can resume saved local sessions:

```bash
claude                          # new Claude Code session
claude -c                       # continue the most recent Claude Code session
claude -r                       # choose a Claude Code session

codex                           # new Codex session
codex resume                    # choose a Codex session to resume
```

→ [Managing Context](managing-context.md)

## Remote work with tmux

When you run a coding agent over SSH—on a cluster or a dedicated machine—a dropped connection kills whatever was running. `tmux` keeps the process alive on the remote host so you can reconnect to it.

```bash
tmux new -s work           # start a named session
                           # ... work; Ctrl-b d to detach ...
tmux ls                    # list sessions
tmux a -t work             # reattach
tmux kill-session -t work  # end it
```

`Ctrl-b d` is the one to remember: press `Ctrl-b`, release, then `d`. Your work keeps running and you can log out.

This pairs with `claude -c` or `codex resume`, and the two solve different halves of the problem. `tmux` keeps the *process* alive; the harness's resume command recovers the *conversation* if the process did die. For a long unattended run you want tmux.

This repository ships a [tmux configuration and cheat sheet](https://github.com/caseywdunn/dunnlab_code/tree/main/assets/tmux) with saner defaults, including copy-paste that works over SSH without X11 forwarding.

→ [Working Across Computers](working-across-computers.md) · [Computing at Yale](yale.md)
