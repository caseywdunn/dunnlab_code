# Contributing

How to add or modify skills, commands, hooks, and documentation in this repo.

## Adding a new skill

1. Create a directory: `skills/<skill-name>/`
2. Create `skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`) and instructions
3. Keep the `description` to one concise sentence — it's always in context
4. Reference `dunnlab-defaults` for shared conventions rather than duplicating them
5. Test locally: `claude --plugin-dir /path/to/dunnlab_code`, then invoke it as `/dunnlab-code:<skill-name>`
6. Update `README.md` and `dev_docs/plugin-architecture.md` to list the new skill
7. Run `claude plugin validate . --strict` before opening a PR

## Adding a new command

1. Create `commands/<command-name>.md` with frontmatter (`name`, `description`) and instructions
2. Test locally with `/command-name`
3. Update `README.md` to list the new command

## Adding a hook

1. Create a script in `hooks/` (e.g., `pre-commit-check.sh`)
2. Register it in `hooks/hooks.json` at the repo root — plugin hooks live there, not in `.claude/settings.json`
3. Document it in `hooks/README.md`
4. Test by triggering the relevant event

## Modifying existing skills

- Edit the `SKILL.md` file directly, then run `/reload-plugins` to pick it up. Personal and project skills are detected live, but **plugin skills are not** — this repo's skills need the reload.
- If changing a skill's scope or purpose, update its `description` frontmatter.
- If the change affects how other skills reference it, check cross-references.

## Updating the GitHub Pages site

- Pages live in `docs/` and use Jekyll with the just-the-docs remote theme.
- Each page has YAML frontmatter with `title` and `nav_order`.
- See `dev_docs/github-pages.md` for configuration details.
- Preview locally: `cd docs && bundle install && bundle exec jekyll serve` (requires Ruby; optional)

## Updating the example settings.json

- The HPC settings file is at `assets/settings.json`.
- It uses JSON comment arrays (`_comment_*` keys) since JSON doesn't support comments.
- When updating permission rules, follow the deny > ask > allow priority order.
- Test permission changes by copying to a project's `.claude/settings.json` and verifying behavior.

## Pull request process

1. Create a branch from `main`
2. Make changes and test locally
3. Open a PR with a description of what changed and why
4. After the merge, check the repo's Actions tab — the `pages-build-deployment` run tells you whether the site built
