---
title: Managing Security
nav_order: 6
---

# Managing Security

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

## Priority order

When the same setting appears at multiple levels, higher-priority scopes win:

1. **Local project** (`.claude/settings.local.json`) — highest
2. **Shared project** (`.claude/settings.json`)
3. **User** (`~/.claude/settings.json`) — lowest

Permission arrays (`allow`, `ask`, `deny`) merge across scopes rather than replacing each other, so restrictions accumulate.

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

A permission mode sets Claude's baseline behavior — how often it pauses to ask before editing a file, running a command, or making a network request. You can cycle modes mid-session with `Shift+Tab` in the CLI (or the mode selector in VS Code, Desktop, and claude.ai), start in a mode with `claude --permission-mode <mode>`, or set a persistent `defaultMode` in `settings.json`. For the full reference, see the official [permission modes documentation](https://code.claude.com/docs/en/permission-modes).

| Mode | What runs without asking | Best for |
|------|--------------------------|----------|
| `"default"` | Reads only | Getting started, sensitive work |
| `"acceptEdits"` | Reads, file edits, and common filesystem commands (`mkdir`, `mv`, `cp`, etc.) | Iterating on code you're reviewing |
| `"plan"` | Reads only — Claude analyzes and proposes but never modifies | Exploring a codebase before changing it |
| `"auto"` | Everything, with background safety checks | Long tasks, reducing prompt fatigue |
| `"dontAsk"` | Only pre-approved tools | Locked-down CI and scripts |
| `"bypassPermissions"` | Everything, no checks | Isolated containers and VMs only |

**For most day-to-day work, prefer `auto` mode.** It lets Claude work in long uninterrupted stretches, but a separate classifier model reviews each action before it runs and blocks anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read in a file or web page. You get far fewer prompts than `default` without surrendering the safety net that `bypassPermissions` removes entirely. (Auto mode is a research preview with model and plan requirements — see the [docs](https://code.claude.com/docs/en/permission-modes) if it doesn't appear in your `Shift+Tab` cycle.)

In every mode except `bypassPermissions`, `deny` rules and explicit `ask` rules still apply, and writes to protected paths (`.git`, `.claude`, shell configs, etc.) are never auto-approved.

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

The `*` wildcard matches any arguments. A space before `*` enforces a word boundary (`ls *` matches `ls -la` but not `lsof`).

### File access (Read/Edit/Write)

File rules use gitignore-style glob patterns:

```json
"allow": [
  "Read(**)"
],
"ask": [
  "Edit(**)"
],
"deny": [
  "Read(**/.env)",
  "Read(**/.ssh/**)",
  "Edit(**/*credentials*)"
]
```

- `*` matches within a single directory
- `**` matches recursively across directories

### Other tools

```json
"ask": [
  "WebFetch"
],
"deny": [
  "mcp__dangerous-server"
]
```

## Example: HPC cluster settings

When using agents such as claude code on a cluster, it is essential to follow all policies. These tools are still new so these may change rapidly. See [YCRC's guidance on using coding agents on Yale clusters](https://docs.ycrc.yale.edu/ai/aicodingtools/).

Furthermore, because these are shared powerful resources it is essential to have highly restricted permissions. The risks are high - you could harm the cluster (creating work for cluster maintainers and denying others access), you could delete or leak other peoples' work, or you could erase or silently modify your own data in ways you didn't expect.

For a full working example, see [assets/settings.json](https://github.com/caseywdunn/dunnlab_code/blob/main/assets/settings.json) — a settings file designed for use on the Yale YCRC McCleary cluster. Place it in your `~/.claude/` folder on McCleary and other clusters where you would use Claude Code. It starts in plan mode, allows read-only commands freely, requires confirmation for job submissions and file modifications, and denies destructive system operations.

## Sandboxed environments

For fully automated workflows where no human is approving each action — CI pipelines, batch processing, or experimental scripts — permission prompts get in the way. Two options can help:

### Dev containers

Running Claude Code inside a [development container](https://code.claude.com/docs/en/devcontainer) gives you isolation at the OS level. Claude has full access inside the container but cannot touch your host filesystem, credentials, or network unless you explicitly mount or forward them. This is the recommended approach for automated or unattended use.

Docker Desktop (macOS/Windows) or Docker Engine (Linux) must be installed on the host.

To get started:

1. Install VS Code and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. Add a `.devcontainer/` directory to your project (the `dunnlab-devcontainer` skill can scaffold this for you — just ask Claude to set up a devcontainer).
3. Open the project in VS Code and click "Reopen in Container" when prompted (or use the Command Palette: `Dev Containers: Reopen in Container`).

For the full reference implementation, see the [Claude Code .devcontainer directory](https://github.com/anthropics/claude-code/tree/main/.devcontainer).

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

For long, mostly-unattended runs where you still want a safety net, reach for [`auto` mode](#permission-modes) instead: it eliminates most prompts but keeps a background classifier that blocks escalations and injection-driven actions. Use `bypassPermissions` only when isolation — not the classifier — is what protects you.

For unattended use, Claude Code refuses to start `bypassPermissions` as `root`/`sudo` outside a recognized sandbox; the [dev container](https://code.claude.com/docs/en/devcontainer) configuration runs as a non-root user so it works there.
