# dunnlab_code

This repo has two purposes:

- Documenting our best practices, onboarding, and instruction on using AI in our research.
- Shared skills, hooks, and commands for the Dunn Lab. The focus is in Claude Code.


**[View the full documentation site](https://dunnlab.github.io/dunnlab_code)**

## Installation

### Option A: Install from the marketplace (recommended)

Once this plugin is published to a marketplace, install it directly in Claude Code:

```
/plugin install dunnlab-code@dunnlab
```

### Option B: Install from a local clone

1. Clone the repo somewhere on your machine:

   ```bash
   git clone https://github.com/dunnlab/dunnlab_code.git ~/dunnlab_code
   ```

2. Launch Claude Code with the plugin directory:

   ```bash
   claude --plugin-dir ~/dunnlab_code
   ```

   This loads the plugin for that session. To make it persistent, add the marketplace (see below).

### Option C: Add as a team marketplace

To make the plugin available to all lab members via a shared project, add it to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "dunnlab": {
      "source": {
        "source": "github",
        "repo": "dunnlab/dunnlab_code"
      }
    }
  }
}
```

When a lab member opens the project and trusts the folder, they'll be prompted to install the plugin.

## Using skills and commands

Once the plugin is installed, everything is available automatically — no extra activation steps.

- **Skills** load based on context. For example, the `lab-defaults` skill activates when you start a new analysis script or set up a project. You can also invoke skills explicitly as `/dunnlab-code:lab-defaults`.
- **Slash commands** are available immediately. Try `/lab-check` to verify the plugin is working.
- **Hooks** run automatically in response to events (once configured).

To see what's available, run:

```
/lab-check
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

### Local clone installs (`--plugin-dir`)

If you're loading from a local clone, pull the latest changes and restart Claude Code:

```bash
cd ~/dunnlab_code
git pull
```

Then restart Claude Code. Changes are picked up on launch — there's no separate update command for local plugins.

## What's included

| Directory    | Contents |
|-------------|----------|
| `skills/`   | Reusable Claude Code skills for lab workflows |
| `commands/` | Slash commands for common tasks |
| `hooks/`    | Event-driven automation hooks |
| `docs/`     | GitHub Pages site with setup guides and lab practices |

### Skills

- **lab-defaults** — Lab-wide coding conventions: preferred languages, file naming, project structure
- **example-skill** — A template to copy when creating new skills

### Commands

- **/lab-check** — Verifies the plugin is loaded and lists available skills

Full documentation, including onboarding instructions and lab conventions, is available on the [Pages site](https://dunnlab.github.io/dunnlab_code).
