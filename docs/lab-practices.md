---
title: Dunn Lab Practices
nav_order: 14
---

# Dunn Lab Practices

This chapter is the most opinionated in the manual, and deliberately so. Everything before it is guidance we would stand behind for anyone; this is how *we* have settled the questions that have more than one defensible answer.

If you are outside the lab, treat it as a worked example rather than a recommendation. The value is less in our specific choices than in the fact that they are written down and encoded somewhere a tool can apply them — the alternative is a convention that exists only in the head of whoever set it up.

## Conventions

These conventions are encoded as skills in [the plugin](plugin.md), so Claude applies them as you work — that chapter maps what is in there. What follows is the reasoning, which the skills themselves do not carry.

A few are more consequential than a style preference, and they are the ones most likely to surprise someone joining:

**Python by default, R when a library requires it.** We prefer industry-standard tools over domain-specific ones, as [Getting Started](getting-started.md#languages) argues. R remains the right answer when the analysis needs a package that only exists there, when it is what you know and it works, or when a collaboration has already chosen it.

**Raw data is immutable, enforced structurally.** Preserve acquired inputs unchanged, commonly under `data/raw/`, and write derivatives separately using rerunnable transformations. This is a general principle — [Using AI in Research](using-ai.md#working-with-data) makes the case — owned by workflow design. Bioinformatics adds biological checks and identifier conventions.

**Cross-species gene IDs are namespaced as `Genus_species@gene_id`.** Reserve `@` as the separator and check source identifiers for conflicts. Every renaming keeps a mapping file and is checked for collisions. Merging datasets with ambiguous identities is a class of silent error that can surface months later in a tree.

**Never abbreviate an author list, and never guess a bibliographic field.** A missing DOI gets a `% TODO` comment, not a plausible-looking value. This sounds pedantic until an AI assistant fills one in for you.

**Shared project instructions stay under 100 lines.** Keep the canonical instructions in `AGENTS.md`, with `CLAUDE.md` importing it. Put details in linked documents or supported directory-scoped instructions so standing context remains small — see [Managing Context](managing-context.md#rules).

**Reuse depends on execution evidence.** An existing output is reusable when a completed run matches the required inputs, relevant code, environment, and settings, and the artifact still verifies. Use the workflow engine's dependency tracking and logs, adding records only for missing evidence. File existence alone cannot distinguish a valid result from an interrupted or obsolete run. Preserve baselines and use the orchestrator's rerun controls for affected stages.

**Exploration and reporting share computation.** Apply workflow design from the first consequential experiment. Distillation selects configurations and outputs, prunes the maintained scope, and closes verification gaps while preserving scientific history. Retained code should need a specific reason to be rewritten.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, and retention.
