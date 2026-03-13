# DunnLab Code

This repo has two purposes:

- Documenting our best practices, onboarding, and instruction on using AI in our research.
- Shared skills, hooks, and commands for the Dunn Lab. The focus is in Claude Code.


**[View the full documentation site](https://dunnlab.org/dunnlab_code)**

## Installation

### Option A: Persistent install from a local clone

1. Clone the repo somewhere on your machine:

   ```bash
   git clone https://github.com/caseywdunn/dunnlab_code.git ~/repos/dunnlab_code
   ```

2. Register the plugin:

   ```bash
   claude plugin add ~/repos/dunnlab_code
   ```

   This persistently installs the plugin so it's available in every future session. The plugin is copied to Claude's local cache at install time, so after pulling new changes with `git pull` you need to re-run `claude plugin add` to update the cached copy.

### Option B: Per-session loading with `--plugin-dir`

If you want to load the plugin for a single session without installing it permanently (useful during development or testing):

```bash
claude --plugin-dir ~/repos/dunnlab_code
```

This loads the plugin for that session alongside any other installed plugins — it does not replace them. The flag is repeatable, so you can load multiple plugin directories at once (e.g., `--plugin-dir ~/pluginA --plugin-dir ~/pluginB`). If a `--plugin-dir` plugin shares a name with an installed marketplace plugin, the local copy takes precedence for that session.

There is no way to specify `--plugin-dir` for the Claude VS Code extension. But you can run `claude --plugin-dir` within the VS Code terminal to use the plugin there.

Because `--plugin-dir` reads directly from the directory, changes take effect immediately on the next session — no update command needed.

### Option C: Add as a marketplace

Register the repo as a marketplace, then install the plugin from it:

```bash
claude plugin marketplace add caseywdunn/dunnlab_code
claude plugin install dunnlab-code
```

This pulls the plugin from GitHub and caches it locally. Useful inside dev containers or on machines where you don't want to clone the repo.

## Using skills and commands

Once the plugin is installed, everything is available automatically — no extra activation steps.

- **Skills** load based on context. For example, the `dunnlab-defaults` skill activates when you start a new analysis script or set up a project. You can also invoke skills explicitly as `/dunnlab-code:dunnlab-defaults`.
- **Slash commands** are available immediately. Try `/dunnlab-check` to verify the plugin is working.
- **Hooks** run automatically in response to events (once configured).

To see what's available, run:

```
/dunnlab-check
```

You can disable the plugin without uninstalling it:

```
/plugin disable dunnlab-code
/plugin enable dunnlab-code
```

## Updating the plugin

How you update depends on how you installed it.

### Marketplace installs

If you installed via a marketplace, update from within Claude Code:

```
/plugin update dunnlab-code@dunnlab
```

Marketplaces auto-update by default, so in most cases you don't need to do anything — new versions are picked up automatically.

### Persistent local installs (`plugin add`)

Pull the latest changes, then re-register the plugin to update the cache:

```bash
cd ~/repos/dunnlab_code
git pull
claude plugin add ~/repos/dunnlab_code
```

### Per-session installs (`--plugin-dir`)

Pull the latest changes and restart Claude Code:

```bash
cd ~/repos/dunnlab_code
git pull
```

Changes are picked up on the next session automatically — no separate update command needed.

## What's included

| Directory    | Contents |
|-------------|----------|
| `skills/`   | Reusable Claude Code skills for lab workflows |
| `commands/` | Slash commands for common tasks |
| `hooks/`    | Event-driven automation hooks |
| `docs/`     | GitHub Pages site with setup guides and lab practices |

### Skills

- **dunnlab-defaults** — Lab-wide coding conventions: preferred languages, file naming, project structure
- **dunnlab-devcontainer** — Add a `.devcontainer/` configuration for secure, reproducible Claude Code development environments
- **example-skill** — A template to copy when creating new skills

### Commands

- **/dunnlab-check** — Verifies the plugin is loaded and lists available skills

Full documentation, including onboarding instructions and lab conventions, is available on the [Pages site](https://dunnlab.org/dunnlab_code).
