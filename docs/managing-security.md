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

## Default mode

The `defaultMode` setting controls Claude's baseline behavior:

| Mode | Behavior |
|------|----------|
| `"default"` | Prompts on first use of each tool |
| `"acceptEdits"` | Automatically accepts file edits |
| `"plan"` | Read-only — Claude can analyze but not modify anything |
| `"dontAsk"` | Auto-denies tools unless pre-approved in `allow` |
| `"bypassPermissions"` | Skips all prompts (only for isolated containers) |

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

For a full working example, see [assets/settings.json](https://github.com/caseywdunn/dunnlab_code/blob/main/assets/settings.json) — a settings file designed for use on the Yale YCRC McCleary cluster. It starts in plan mode, allows read-only commands freely, requires confirmation for job submissions and file modifications, and denies destructive system operations.

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

### `--dangerously-skip-permissions`

Claude Code accepts a `--dangerously-skip-permissions` flag that disables all permission checks. As the name suggests, this is dangerous — Claude will execute any command, edit any file, and access any resource without asking. Only use this inside a disposable container or VM where there is nothing sensitive to protect and nothing important to break. Never use it on your host machine or a shared system.
