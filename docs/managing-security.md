---
title: Managing Security
nav_order: 5
---

# Managing Security

Claude Code can read your files, run commands, and reach the network. This chapter is about deciding what it may do without asking, what it must ask about, and what it may never do — and about the difference between a rule Claude follows and a boundary the operating system enforces.

Worth reading before you let Claude work unsupervised, and again before you run it on a shared system.

## Why security matters

Claude Code runs directly on your machine with access to your shell, filesystem, and network. This is what makes it powerful — it can read your code, run commands, edit files, and install packages. But that same access creates real risks:

- **Accidental damage.** Claude may delete or overwrite the wrong files, run a destructive command, or make edits based on a misunderstanding of your intent. On shared systems like an HPC cluster, a mistake can affect other users' files or waste compute resources.
- **Exposure of private information.** Claude can read anything your user account can read — API keys, credentials, SSH configs, environment variables, private data. If this information ends up in a prompt sent to the API, it leaves your machine.
- **Prompt injection.** Malicious content hidden in files, web pages, or tool outputs can manipulate Claude's behavior. For example, a cloned repository could contain instructions in a file that trick Claude into running harmful commands or exfiltrating data. This is especially concerning when working with untrusted code or fetching content from the web.

The permission system described below is your primary defense. It lets you decide exactly which actions Claude can take automatically, which require your approval, and which are blocked entirely.

## Configuring permissions with settings.json

Claude Code uses `settings.json` files to control what actions Claude can take. This is how you restrict dangerous commands, protect sensitive files, and tailor permissions per project or environment.

## Settings file locations

There are three places you can put a `settings.json`:

| Scope | Location | Purpose |
|-------|----------|---------|
| **User** | `~/.claude/settings.json` | Personal defaults, applied to all projects |
| **Project (shared)** | `.claude/settings.json` | Team settings, committed to git |
| **Project (local)** | `.claude/settings.local.json` | Personal project overrides, gitignored |

An organization can also deploy **managed settings** (e.g. `/etc/claude-code/managed-settings.json` on Linux), which outrank everything below.

## Priority order

When the same setting appears at multiple levels, higher-priority scopes win:

1. **Managed settings** — highest; not even command-line flags override these
2. **Local project** (`.claude/settings.local.json`)
3. **Shared project** (`.claude/settings.json`)
4. **User** (`~/.claude/settings.json`) — lowest

Permission arrays (`allow`, `ask`, `deny`) merge across scopes rather than replacing each other, so restrictions accumulate. If a tool is denied at any level, no other level can allow it.

{: .warning }
One exception worth knowing: `"defaultMode": "auto"` in a project's `.claude/settings.json` or `.claude/settings.local.json` has no effect. Auto mode can only be set from user settings, managed settings, or the `--permission-mode` flag.

## The permissions object

Permissions are defined in three arrays inside `settings.json`:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [ ... ],
    "ask": [ ... ],
    "deny": [ ... ]
  }
}
```

- **`allow`** — Claude can use these tools without asking
- **`ask`** — Claude will prompt you for confirmation each time
- **`deny`** — Claude is blocked from these entirely

Rules are evaluated in order: **deny > ask > allow**. A deny rule always wins over an allow rule at the same scope.

## Permission modes

A permission mode sets Claude's baseline behavior — how often it pauses to ask before editing a file, running a command, or making a network request. You can cycle modes mid-session with `Shift+Tab` in the CLI (or the mode selector in VS Code, JetBrains, Desktop, and claude.ai), start in a mode with `claude --permission-mode <mode>`, or set a persistent `defaultMode` in `settings.json`. For the full reference, see the official [permission modes documentation](https://code.claude.com/docs/en/permission-modes).

| Mode | What runs without asking | Best for |
|------|--------------------------|----------|
| `"default"` | Reads only | Reviewing every action yourself, sensitive work |
| `"acceptEdits"` | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, `rm`, `sed`) inside your working directory | Iterating on code you're reviewing |
| `"plan"` | Reads, plus classifier-approved commands when auto mode is available | Exploring a codebase before changing it |
| `"auto"` | Everything, with a classifier reviewing each action | Long tasks, reducing prompt fatigue |
| `"dontAsk"` | Only pre-approved tools | Locked-down CI and scripts |
| `"bypassPermissions"` | Everything | Isolated containers and VMs only |

The `"default"` mode is labeled **Manual** in the CLI, the VS Code and JetBrains extensions, and the desktop app. Its config value is still `default`, and `manual` is accepted as an alias wherever you type it.

**For most day-to-day work, prefer `auto` mode** — on Pro, Max, and Team plans it is now the mode sessions start in by default. See [Auto mode](#auto-mode) below for how it decides.

What no mode changes:

- **`deny` rules apply in every mode, `bypassPermissions` included.** It is `allow` rules that stop having any effect there. A deny rule is the one control that holds no matter how the session is launched.
- **Explicit `ask` rules always prompt**, even in `auto`.
- **Writes to protected paths are never auto-approved** except under `bypassPermissions`. See below.
- **`rm` and `rmdir` against a critical path** are never approved by an allow rule or a hook. See below.

### Auto mode

Auto mode lets Claude work in long uninterrupted stretches. A separate classifier model reviews each action before it runs and blocks anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read in a file or web page. You get far fewer prompts than Manual mode without surrendering the safety net that `bypassPermissions` removes entirely.

A few properties are worth understanding before you rely on it:

- **The classifier does not see tool results.** It sees your messages, non-read-only tool calls, and your CLAUDE.md — but the contents of files and web pages are stripped out. That is what makes it resistant to the prompt injection it is meant to catch.
- **Broad allow rules are dropped on entering auto mode.** A blanket `Bash(*)`, a wildcarded interpreter like `Bash(python*)`, or a package-manager run command stops applying, because those amount to arbitrary code execution. Narrow rules like `Bash(pytest)` stay in effect and are restored when you leave the mode.
- **Subagents are checked too**, at spawn, on each action, and again on the results they return.
- **It costs something.** The classifier adds a round-trip before shell and network commands. Reads and working-directory edits skip it.

It is not a substitute for review on sensitive operations. Use it where you trust the general direction of the work.

### Protected and critical paths

Two safety checks sit outside the permission rules entirely, so it is worth knowing they exist before you write a rule that appears not to work.

**Protected paths** are never auto-approved for writes: `.git`, `.claude`, `.vscode`, `.devcontainer`, `.cargo`, and files like `.bashrc`, `.zshrc`, `.envrc`, `.npmrc`, `.mcp.json`, and `.gitconfig`. An `allow` rule does not pre-approve them — the check runs before allow rules are evaluated. In modes that prompt, the prompt offers to approve `.claude/` writes for the rest of the session.

**Critical paths** are `rm`/`rmdir` targets that no `allow` rule and no `PreToolUse` hook can approve: the filesystem root and its top-level directories, your home directory, and your working directory and its parents. A glob under a shell variable (`rm -rf "$DIR"/*`) counts, because an empty variable turns it into a removal from `/`. Hiding it in `$(...)` does not evade the check. A matching `deny` rule still blocks the command outright.

## Permission rule syntax

Rules follow the pattern `Tool` or `Tool(specifier)`.

### Bash commands

```json
"allow": [
  "Bash(git status:*)",
  "Bash(conda activate:*)"
],
"ask": [
  "Bash(sbatch:*)",
  "Bash(git push:*)"
],
"deny": [
  "Bash(sudo:*)",
  "Bash(rm -rf /*)"
]
```

The `*` wildcard matches any sequence of characters, including spaces, so one wildcard can span several arguments.

**A space before the `*` enforces a word boundary**, and leaving it out is the most common mistake in these files. `Bash(ls *)` matches `ls -la` but not `lsof`; `Bash(ls*)` matches both. Always include the space.

The `:*` suffix is an equivalent way to write that trailing wildcard, so `Bash(ls:*)` and `Bash(ls *)` match the same commands. It is only recognized at the *end* of a pattern — in `Bash(git:* push)` the colon is a literal character and matches nothing.

Claude Code understands shell operators, so `Bash(safe-cmd *)` does not approve `safe-cmd && other-cmd`; every subcommand must match a rule independently.

### File access

Only two tool names take a path: **`Read`** and **`Edit`**. `Edit(...)` covers every built-in tool that writes files, and a `Read` deny rule also blocks writing to the same path. Path rules written for `Write`, `NotebookEdit`, `Glob`, or `MultiEdit` are accepted but never consulted, and Claude Code warns about them at startup — write `Edit(docs/**)` rather than `Write(docs/**)`.

File rules use gitignore-style glob patterns:

```json
"allow": [
  "Read(**)"
],
"deny": [
  "Read(~/.ssh/**)",
  "Read(**/.env)",
  "Edit(**/*credentials*)"
]
```

- `*` matches within a single directory
- `**` matches recursively across directories

**The leading characters decide where a pattern is anchored**, and this catches people out:

| Pattern | Anchored at |
|---------|-------------|
| `**/.env`, `./secrets/**` | The current working directory |
| `/src/**` | The directory of the settings file that defines it |
| `~/.ssh/**` | Your home directory |
| `//etc/**` | The filesystem root |

A rule like `Read(**/.ssh/**)` in `~/.claude/settings.json` does **not** protect `~/.ssh` — it only matches a `.ssh` directory beneath wherever you launched Claude. For a rule in user settings that should apply everywhere, use the `~/` or `//` form.

{: .warning }
Read and Edit rules apply to Claude's own file tools and to file commands it recognizes in Bash, such as `cat` and `sed`. They do **not** apply to a script that opens the file itself — a Python program Claude runs can read anything your account can read. For enforcement that covers every process, use the [Bash sandbox](#the-bash-sandbox).

### Other tools

```json
"ask": [
  "WebFetch"
],
"deny": [
  "mcp__dangerous-server"
]
```

## Sandboxed environments

Permission rules govern what Claude will *choose* to do. Sandboxing governs what a command *can* do once it runs — an enforcement boundary rather than a judgment call. The two are complementary, and for unattended work you want both.

Three options, from lightest to heaviest:

### The Bash sandbox

Claude Code has a built-in sandbox that confines Bash commands and everything they spawn. The operating system enforces the boundary, so it covers the gap that Read and Edit deny rules cannot: a Python script Claude runs is inside the sandbox too.

By default, sandboxed commands can write only to your working directory and the session temp directory, and the first connection to a new network domain asks for approval.

Turn it on with `/sandbox`, which opens a panel with three tabs:

- **Mode** — *auto-allow* runs sandboxed commands without prompting; *regular permissions* keeps the normal prompts even inside the sandbox.
- **Overrides** — whether a command that fails under the sandbox may retry unsandboxed.
- **Config** — the resolved settings.

Selecting a mode in the panel writes to that project's `.claude/settings.local.json`. To turn it on everywhere, set it in your user settings:

```json
{
  "sandbox": { "enabled": true }
}
```

**Platform support**: macOS uses the built-in Seatbelt framework, with nothing to install. Linux and WSL2 need `bubblewrap` and `socat` (`sudo apt-get install bubblewrap socat`). Native Windows is not supported — run Claude Code inside WSL2 there.

{: .warning }
**If the sandbox cannot start, Claude Code warns and runs your commands unsandboxed.** Bubblewrap needs unprivileged user namespaces, which shared and managed systems commonly restrict, so this is a real possibility rather than an edge case. Run `/sandbox` and check whether a Dependencies tab appears rather than assuming you are protected. Set `sandbox.failIfUnavailable` to `true` to make an unavailable sandbox a hard error instead of a silent fallback.

If you work on an HPC cluster, see [Computing at Yale](yale.md#claude-code-on-the-clusters) — the stakes are higher there and the sandbox is less likely to be available.

A good pairing for local work: Manual mode plus sandbox auto-allow. You get few prompts, and what you get in exchange is a real kernel-enforced boundary rather than a model's judgment.

### Dev containers

Running Claude Code inside a [development container](https://code.claude.com/docs/en/devcontainer) isolates the whole environment, not just Bash. Claude has full access inside the container but cannot touch your host filesystem, credentials, or network unless you explicitly mount or forward them. This is the right choice for automated or unattended use.

Docker Desktop (macOS/Windows) or Docker Engine (Linux) must be installed on the host.

To get started:

1. Install VS Code and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Add a `.devcontainer/` directory to your project — ask Claude to set up a devcontainer and the `dunnlab-devcontainer` skill will scaffold it.
3. Open the project in VS Code and click "Reopen in Container" when prompted (or use the Command Palette: `Dev Containers: Reopen in Container`).

The simplest configuration adds the official [Claude Code Dev Container Feature](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code) to any base image. For a hardened setup with an egress firewall, see the [reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer).

{: .warning }
Only use devcontainers with trusted repositories. While the firewall restricts network access, it does not prevent a malicious project from exfiltrating anything accessible inside the container, including Claude Code credentials.

### `bypassPermissions` mode

`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately. Start in it from the CLI:

```bash
claude --permission-mode bypassPermissions
```

(The older `--dangerously-skip-permissions` flag is equivalent and still works.)

{: .warning }
`bypassPermissions` offers **no protection against prompt injection or unintended actions** — Claude will execute any command, edit any file, and access any resource without asking. Malicious content hidden in a cloned repo, a fetched web page, or a tool output can hijack the session with nothing to stop it. Only use this inside a disposable container or VM where there is nothing sensitive to protect and nothing important to break. Never use it on your host machine or a shared system.

For long, mostly-unattended runs where you still want a safety net, reach for [`auto` mode](#auto-mode) instead: it eliminates most prompts but keeps a classifier that blocks escalations and injection-driven actions. Use `bypassPermissions` only when isolation — not the classifier — is what protects you.

Even here, two things still hold: `deny` rules apply, and `rm` against a [critical path](#protected-and-critical-paths) still prompts.

On Linux and macOS, Claude Code refuses to start `bypassPermissions` as `root` or under `sudo` outside a recognized sandbox. The [dev container](https://code.claude.com/docs/en/devcontainer) configuration runs as a non-root user, so it works there.

To prevent this mode being used at all — on a shared system, say — set `permissions.disableBypassPermissionsMode` to `"disable"` in any settings file. It is most useful in managed settings, but you can also set it in your own to lock yourself out.
