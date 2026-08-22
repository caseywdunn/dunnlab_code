# Hooks

Claude Code hooks are event-driven scripts that run automatically in response to specific events, such as before a commit, after a file is created, or when a session starts.

## How to add a hook

1. Create a script in this directory (e.g., `pre-commit-check.sh`)
2. Register it in `hooks/hooks.json` at the plugin root
3. Test it by triggering the relevant event in Claude Code

Because this repo is distributed as a plugin, hooks belong in `hooks/hooks.json` rather than in a `.claude/settings.json` file. The JSON structure is the same as the `hooks` object in a settings file:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs ruff format" }]
      }
    ]
  }
}
```

Hook commands receive their input as JSON on stdin.

## Resources

- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)

<!-- TODO: Add lab-specific hooks as they are developed -->
