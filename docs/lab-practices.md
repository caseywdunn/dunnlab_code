---
title: Dunn Lab Practices
nav_order: 11
---

# Dunn Lab Practices

This chapter is the most opinionated in the manual, and deliberately so. Everything before it is guidance we would stand behind for anyone; this is how *we* have settled the questions that have more than one defensible answer.

If you are outside the lab, treat it as a worked example rather than a recommendation. The value is less in our specific choices than in the fact that they are written down and encoded somewhere a tool can apply them — the alternative is a convention that exists only in the head of whoever set it up.

## The choices worth knowing about

These conventions are encoded as skills in [the plugin](plugin.md), so Claude applies them as you work — that chapter maps what is in there. What follows is the reasoning, which the skills themselves do not carry.

A few are more consequential than a style preference, and they are the ones most likely to surprise someone joining:

**Python by default, R when a library requires it.** We prefer industry-standard tools over domain-specific ones, as [Getting Started](getting-started.md#languages) argues. R remains the right answer when the analysis needs a package that only exists there, when it is what you know and it works, or when a collaboration has already chosen it.

**Raw data is immutable, enforced structurally.** `data/raw/` is never written to. Every transformation produces a new file under `data/processed/` from a script that can be re-run. This is a general principle — [Using AI in Research](using-ai.md#working-with-data) makes the case — but the bioinformatics skill turns it into specific checks.

**Cross-species gene IDs are namespaced as `Genus_species@gene_id`.** The `@` separator is chosen because it does not appear in standard gene IDs and is not a shell metacharacter. Every renaming keeps a mapping file, so the transformation is always reversible. Merging datasets without this is a class of silent error that surfaces months later in a tree.

**Never abbreviate an author list, and never guess a bibliographic field.** A missing DOI gets a `% TODO` comment, not a plausible-looking value. This sounds pedantic until an AI assistant fills one in for you.

**CLAUDE.md stays under 100 lines.** The [official guidance](https://code.claude.com/docs/en/memory) targets 200; we hold to half that, because everything in a CLAUDE.md is paid for in every session. When project guidance outgrows it, the answer is a path-scoped rule in `.claude/rules/`, not a longer CLAUDE.md — see [Managing Context](managing-context.md#rules).

**Checkpointing is by output existence, not sentinel files.** A pipeline stage is skipped if its output already exists. To re-run a stage you delete its output. There is no hidden state tracking what has completed.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, and retention.

Two conventions from it are worth restating here, because AI tools make them easy to violate by accident:

- **Raw data is immutable.** If a script would modify something in `data/raw/`, that is a bug regardless of what it was asked to do.
- **Prefer a script over a direct transformation.** Have Claude write something you can read and re-run rather than editing data in place. The script is reviewable, reproducible, and reversible.

## Contributing back

If a convention here is wrong, or you have settled a question this chapter does not cover, change it rather than working around it. `dev_docs/contributing.md` in the repository covers the branching model, the checks, and the release process.
