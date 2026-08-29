---
paths:
  - "docs/**/*.md"
---

# Editing the manual

## Quick Reference duplicates other chapters on purpose

`docs/quick-reference.md` restates commands that later chapters explain. That duplication is deliberate — it is the only page someone can look a command up on — but it drifts silently.

**If you change a command, a permission mode, a session flag, or the working rhythm in any chapter, check whether Quick Reference states it too.**

`./scripts/check.sh` validates the plugin install commands against the manifests, so those cannot rot. Nothing checks the rest: `claude -c` / `-r` / `--fork-session`, the `Shift+Tab` cycle, the mode table, and the tmux commands appear only in Quick Reference and are yours to keep honest.

Keep Quick Reference to commands and one-line descriptions. Explanation belongs in the chapter it links to; that is what stops the two copies from diverging in substance as well as detail.

## The chapters are ordered by audience

Chapters 2 through 10 must contain nothing specific to this lab or to Yale — they are meant to be handed to someone at another institution unchanged. Institution-specific material goes in `yale.md`, lab-specific material in `lab-practices.md`. A statement that would have to be deleted before sharing the manual is in the wrong chapter.

## After any structural change

`nav_order` must stay contiguous from 1, every page must be linked from `index.md`, and the page table in `dev_docs/github-pages.md` must match. `check.sh` enforces the first two and **not** the third.

Run `./scripts/check.sh` before committing. `./scripts/preview-docs.sh` renders the site if you changed anything structural.
