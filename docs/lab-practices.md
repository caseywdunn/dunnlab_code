---
title: Lab Practices
nav_order: 3
---

# Lab Practices

This is a partial description of the Dunn Lab's conventions for code development. Where the [Getting Started](getting-started.md) page covers the tools, this page covers what we expect of each other when using them.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, etc.

Two conventions worth restating here, because AI tools make it easy to violate them by accident:

- **Raw data is immutable.** Transformations produce new files in `data/processed/`. If a script would modify something in `data/raw/`, that is a bug regardless of what it was asked to do.
- **Prefer a script over a direct transformation.** When you need data reshaped, have Claude write a script you can read and re-run, rather than having it edit the file in place. The script is reviewable, reproducible, and reversible; a direct edit is none of those.
