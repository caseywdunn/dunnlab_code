# Hooks

Claude Code hooks are event-driven scripts that run automatically in response to specific events, such as before a commit, after a file is created, or when a session starts.

## How to add a hook

1. Create a script in this directory (e.g., `pre-commit-check.sh`)
2. Register it in `.claude/settings.json` under the `hooks` key
3. Test it by triggering the relevant event in Claude Code

## Resources

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)

<!-- TODO: Add lab-specific hooks as they are developed -->
