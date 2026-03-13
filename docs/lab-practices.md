---
title: Lab Practices
nav_order: 4
---

# Lab Practices

These are the Dunn Lab's conventions for working with Claude Code and AI-assisted development.

## When to use AI assistance

<!-- TODO: Fill in with lab-specific guidance. Some starting points below. -->

- Use Claude Code for boilerplate, data wrangling scaffolding, and exploratory analysis scripts
- Prefer writing your own code for novel methods, statistical models, and anything going into a publication's methods section
- When in doubt, use AI to get a first draft, then rewrite with understanding

## Code review expectations for AI-generated code

<!-- TODO: Fill in with lab-specific expectations. -->

- All AI-generated code must be reviewed as carefully as human-written code
- You are responsible for code you commit, regardless of who (or what) wrote it
- Flag AI-generated sections in PRs so reviewers know to look closely

## Data privacy considerations

<!-- TODO: Fill in with lab-specific data policies. -->

- Put all secure information (API keys, tokens, passwords, account usernames) in dedicated files that are in the `.gitignore`
- Use placeholder or synthetic data when developing analysis pipelines
- Check with the PI before using Claude Code on any dataset with access restrictions

## Contributing new skills or commands

<!-- TODO: Expand with detailed contribution workflow. -->

1. Create a branch from `main`
2. Add your skill in `skills/your-skill-name/SKILL.md` or your command in `commands/your-command.md`
3. Test locally by registering the plugin and running the skill or command
4. Open a pull request with a description of what the skill does and when it should trigger
