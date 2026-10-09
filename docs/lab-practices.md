---
title: Dunn Lab Practices
nav_order: 18
---

# Dunn Lab Practices

This chapter is the most opinionated in the manual, and deliberately so. Everything before it is guidance we would stand behind for anyone; this is how *we* have settled the questions that have more than one defensible answer.

If you are outside the lab, treat it as a worked example rather than a recommendation. The value is less in our specific choices than in the fact that they are written down and encoded somewhere a tool can apply them — the alternative is a convention that exists only in the head of whoever set it up.

## Conventions

These conventions are encoded as skills in [the plugin](plugin.md), so Claude applies them as you work — that chapter maps what is in there. What follows is the reasoning, which the skills themselves do not carry.

A few are more consequential than a style preference, and they are the ones most likely to surprise someone joining:

**Python by default, R when a library requires it.** We prefer industry-standard tools over domain-specific ones, as [The Toolkit](toolkit.md#python) argues. R remains the right answer when the analysis needs a package that only exists there, when it is what you know and it works, or when a collaboration has already chosen it.

**Raw data is immutable, enforced structurally.** Preserve acquired inputs unchanged, commonly under `data/raw/`, and write derivatives separately using rerunnable transformations. This is a general principle, explained in [Reproducibility](reproducibility.md#data) and owned by workflow design. Bioinformatics adds biological checks and identifier conventions.

**Cross-species gene IDs are namespaced as `Genus_species@gene_id`.** Reserve `@` as the separator and check source identifiers for conflicts. Every renaming keeps a mapping file and is checked for collisions. Merging datasets with ambiguous identities is a class of silent error that can surface months later in a tree.

**`AGENTS.md` stays under 100 lines.** General guidance allows up to about 200, but everything in it loads into every session, and a shorter file is followed more reliably. Detail goes in linked documents under `dev_docs/`, which the agent reads when it needs them. See [Managing Context](managing-context.md#keep-it-short).

**Exploration and reporting share computation.** Apply workflow design from the first consequential experiment. Distillation selects configurations and outputs, prunes the maintained scope, and closes verification gaps while preserving scientific history. Retained code should need a specific reason to be rewritten.

## Manuscripts

**Each manuscript gets two repositories.** The analysis repository holds the code and workflow. It may start private but will eventually be public. The manuscript repository holds the text and will probably stay private. Keeping them separate means the analysis can be released without also releasing drafts, reviewer correspondence, and co-author comments.

**Name them as a pair.** Use kebab case for the analysis repository and add `-ms` for the manuscript: `project-a` and `project-a-ms`. That way they sort next to each other in any listing.

**Write in Quarto, and render both PDF and Word.** The `.qmd` source is the source of record. Render a PDF for reading, through LaTeX and with the `.tex` source kept for journals that want it, and a `.docx` for co-authors who edit in Word. Neither rendered file is ever edited and committed back.

**Results are generated, never typed.** We follow the principle in [Writing with AI](writing-with-ai.md#principles-behind-our-approach): every reported number, table, and figure comes from code. In practice, the analysis repository stages everything the paper reports in a committed `manuscript/` directory: a `values.json` file of formatted values, together with the analysis's repository, commit, version, and DOI, plus tables and figures. A script in the manuscript repository copies that bundle into `_results/`, pinned to the analysis commit, and the sync is committed on its own so its diff shows what changed. Quarto then inserts values with shortcodes such as `{{< meta results.n_species >}}`, with no code running in the manuscript. A check before every render fails if the text refers to a value or figure the bundle lacks, and warns when the analysis has moved on since the last sync.

**Figures are vector, generated at final size, twice.** The analysis code saves each figure as a vector PDF for the PDF build, rasterizing only very dense layers such as huge scatter plots, and as a PNG for the Word build. The manuscript includes it without a file extension, so each build picks the right one. A figure that needs hand assembly, such as photographs combined with plots, keeps its editable source in the manuscript repository and is re-exported whenever the results change.

**Co-authors edit the `.docx` with track changes on.** Track changes is not for approving or rejecting edits in Word. It lets them, you, and the agent see exactly what was changed.

**Incorporate edits through a gitignored `tmp/` folder.** Each manuscript repository has a `tmp/` directory listed in `.gitignore`. Put each returned `.docx` there and ask the agent to carry its changes into the `.qmd` file. Commit before and after every incorporation. The diff between the two commits is then the complete record of what one co-author's edits did to the source. That diff is what you review, and it is easy to revert if something went wrong. If a co-author edits a generated number or figure, the change goes back to the analysis rather than being typed in.

The [`dunnlab-manuscript` skill](plugin.md#the-skills) encodes these conventions, including the repository layout, the sync and check scripts, and figure settings.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, and retention.
