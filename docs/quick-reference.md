---
title: Quick Reference
nav_order: 3
---

# Quick Reference

Everything you need to get going, on one page. Each section links to the chapter that explains why.

If you are reading straight through, skim this for the shape and keep moving — the chapters that follow cover all of it properly. If you have done this before and just want the command, this is the page to bookmark.

## Set up

**Before you install, decide where this will run.** Your everyday machine, a separate user account on it, a container, a virtual machine, or a dedicated machine. This is much easier to choose now than to retrofit later, and the more autonomy you plan to give Claude, the more that choice has to carry. → [System-level control](managing-security.md#system-level-control)

```bash
# 1. Install Claude Code (macOS, Linux, WSL)
curl -fsSL https://claude.ai/install.sh | bash

# 2. Install the lab plugin — optional, but it is what makes Claude
#    follow our conventions rather than guessing
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code@dunnlab

# 3. Start it, from your project directory
cd ~/repos/my-project
claude
```

Then, inside a session:

| Command | What it tells you |
|---------|-------------------|
| `/dunnlab-code:dunnlab-check` | The plugin loaded, and which skills it provides |
| `/context` | What is currently loaded and what it costs you |
| `/doctor` | Setup checkup, including what your skills and plugins cost |
| `/help` | Everything available |

**Once it runs, set your own defaults.** `~/.claude/settings.json` holds your permission rules and the mode sessions start in; `~/.claude/CLAUDE.md` holds preferences that apply to every project. Deciding these once beats re-deciding them every session. → [Claude-level control](managing-security.md#claude-level-control), [Managing Context](managing-context.md)

→ [Getting Started](getting-started.md)

## A working session

The rhythm matters more than the prompting. In rough order:

1. **Start in plan mode.** Describe what you want and let Claude propose an approach before it writes anything. This is the cheapest place to catch a wrong direction.
2. **Review the plan, then approve it.** Argue with it here rather than after the code exists.
3. **Work in small, verifiable steps.** A change too large to read carefully was too large to ask for in one go.
4. **Let Claude run the code.** Do not paste error messages — ask it to run the thing and read the error itself.
5. **Commit after each verified step**, and let Claude write the message.
6. **`/clear` before the next task.** A stale conversation makes everything worse.

→ [Claude Code Concepts](claude-intro.md#best-practices-for-effective-use)

## Permission modes

`Shift+Tab` cycles through them mid-session. The status bar shows which one you are in.

| Mode | Runs without asking |
|------|---------------------|
| **Manual** (`default`) | Reads only |
| **Accept edits** | Reads, file edits, common filesystem commands |
| **Plan** | Reads; proposes but does not change anything |
| **Auto** | Everything, with a classifier reviewing each action |

The cycle runs `Manual → Accept edits → Plan → Auto → Manual`. So plan to auto is a single press forward, but getting from auto back to plan takes three. Auto appears in the cycle only if your account supports it, and is the mode sessions start in by default on Pro, Max, and Team plans.

To start in a particular mode:

```bash
claude --permission-mode plan
```

→ [Managing Security](managing-security.md#permission-modes)

## Sessions

Closing the terminal does not lose the conversation.

```bash
claude                          # new session
claude -c                       # continue the most recent one here
claude -r                       # pick from past sessions
claude -r auth-refactor         # resume one by name
claude -r <id> --fork-session   # branch from it, leaving the original intact
```

And within a session:

| Command | What it does |
|---------|--------------|
| `/clear` | Drop the conversation, reload your standing instructions |
| `/rewind` | Restore the conversation *and the files* to an earlier point |
| `/context` | See what is loaded |

→ [Managing Context](managing-context.md)

## Remote work with tmux

When you run Claude Code over SSH — on a cluster, or on a dedicated machine — a dropped connection kills whatever was running. `tmux` keeps the process alive on the remote host so you can reconnect to it.

```bash
tmux new -s work           # start a named session
                           # ... work; Ctrl-b d to detach ...
tmux ls                    # list sessions
tmux a -t work             # reattach
tmux kill-session -t work  # end it
```

`Ctrl-b d` is the one to remember: press `Ctrl-b`, release, then `d`. Your work keeps running and you can log out.

This pairs with `claude -c`, and the two solve different halves of the problem. `tmux` keeps the *process* alive; `-c` recovers the *conversation* if the process did die. For a long unattended run you want tmux.

This repository ships a [tmux configuration and cheat sheet](https://github.com/caseywdunn/dunnlab_code/tree/main/assets/tmux) with saner defaults, including copy-paste that works over SSH without X11 forwarding.

→ [Computing at Yale](yale.md)
