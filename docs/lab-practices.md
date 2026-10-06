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

**Exploration and reporting share computation.** Apply workflow design from the first consequential experiment. Distillation selects configurations and outputs, prunes the maintained scope, and closes verification gaps while preserving scientific history. Retained code should need a specific reason to be rewritten.

## Manuscripts

**Each manuscript gets two repositories.** The analysis repository holds the code and workflow. It may start private but will eventually be public. The manuscript repository holds the text and will probably stay private. Keeping them separate means the analysis can be released without also releasing drafts, reviewer correspondence, and co-author comments.

**Name them as a pair.** Use kebab case for the analysis repository and add `-ms` for the manuscript: `project-a` and `project-a-ms`. That way they sort next to each other in any listing.

**Write in LaTeX, and render both PDF and Word.** The `.tex` source is the source of record. Render a PDF for reading and a `.docx` for co-authors who edit in Word. Neither rendered file is ever edited and committed back.

**Co-authors edit the `.docx` with track changes on.** Track changes is not for approving or rejecting edits in Word. It lets them, you, and the agent see exactly what was changed.

**Incorporate edits through a gitignored `tmp/` folder.** Each manuscript repository has a `tmp/` directory listed in `.gitignore`. Put each returned `.docx` there and ask the agent to carry its changes into the `.tex` file. Commit before and after every incorporation. The diff between the two commits is then the complete record of what one co-author's edits did to the source. That diff is what you review, and it is easy to revert if something went wrong.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, and retention.
