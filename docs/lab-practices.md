---
title: Dunn Lab Practices
nav_order: 9
---

# Dunn Lab Practices

This chapter is the most opinionated in the manual, and deliberately so. Everything before it is guidance we would stand behind for anyone; this is how *we* have settled the questions that have more than one defensible answer.

If you are outside the lab, treat it as a worked example rather than a recommendation. The value is less in our specific choices than in the fact that they are written down and encoded somewhere a tool can apply them — the alternative is a convention that exists only in the head of whoever set it up.

## Where our conventions actually live

They are not in this chapter. They are in the plugin, as skills, so that Claude applies them while you work rather than requiring you to remember them.

That is the whole design: a convention in a document is one somebody has to read and recall; a convention in a skill is one that gets applied. This chapter is a map of what is in there, not a substitute for it.

You can read any of them directly at `skills/<name>/SKILL.md` in [the repository](https://github.com/caseywdunn/dunnlab_code/tree/main/skills), or invoke one with `/dunnlab-code:<name>`.

### What each skill encodes

| Skill | What it settles |
|-------|-----------------|
| **`dunnlab-defaults`** | The foundational one. Preferred languages and their best practices, dependency and environment management, file naming, project structure, workflow orchestration, testing, and version control. The other skills build on it. |
| **`dunnlab-new-project`** | A staged workflow for starting a project: define scope, initialize the repo and permissions, write planning documents before any code, then build in reviewable increments. Tracks its own progress so it survives `/clear` and resumes in a later session. |
| **`dunnlab-bioinformatics`** | Sequence analysis conventions: input validation, gene name sanitization, globally unique cross-species gene IDs, paralog resolution, contamination screening, and our default tool for each job. |
| **`dunnlab-hpc`** | YCRC cluster reference — partitions, storage, SLURM templates, Snakemake integration. See [Computing at Yale](yale.md). |
| **`dunnlab-devcontainer`** | Scaffolds an isolated container to work in, either the standard configuration or a hardened one with an egress firewall. |
| **`dunnlab-codereview`** | The review checklist and process, including how to give feedback that distinguishes blocking issues from nits. |
| **`dunnlab-biblio`** | BibTeX conventions for manuscripts: entry keys, full author lists, title capitalization, and a strict rule against ever guessing a bibliographic field. |

### The choices worth knowing about

A few of these are more consequential than a style preference, and they are the ones most likely to surprise someone joining:

**Python by default, R when a library requires it.** We prefer industry-standard tools over domain-specific ones, as [Getting Started](getting-started.md#languages) argues. R remains the right answer when the analysis needs a package that only exists there, when it is what you know and it works, or when a collaboration has already chosen it.

**Raw data is immutable, enforced structurally.** `data/raw/` is never written to. Every transformation produces a new file under `data/processed/` from a script that can be re-run. This is a general principle — [Using AI in Research](using-ai.md#working-with-data) makes the case — but the bioinformatics skill turns it into specific checks.

**Cross-species gene IDs are namespaced as `Genus_species@gene_id`.** The `@` separator is chosen because it does not appear in standard gene IDs and is not a shell metacharacter. Every renaming keeps a mapping file, so the transformation is always reversible. Merging datasets without this is a class of silent error that surfaces months later in a tree.

**Never abbreviate an author list, and never guess a bibliographic field.** A missing DOI gets a `% TODO` comment, not a plausible-looking value. This sounds pedantic until an AI assistant fills one in for you.

**Checkpointing is by output existence, not sentinel files.** A pipeline stage is skipped if its output already exists. To re-run a stage you delete its output. There is no hidden state tracking what has completed.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, and retention.

Two conventions from it are worth restating here, because AI tools make them easy to violate by accident:

- **Raw data is immutable.** If a script would modify something in `data/raw/`, that is a bug regardless of what it was asked to do.
- **Prefer a script over a direct transformation.** Have Claude write something you can read and re-run rather than editing data in place. The script is reviewable, reproducible, and reversible.

## Contributing back

If a convention here is wrong, or you have settled a question this chapter does not cover, change it rather than working around it. `dev_docs/contributing.md` in the repository covers the branching model, the checks, and the release process.
