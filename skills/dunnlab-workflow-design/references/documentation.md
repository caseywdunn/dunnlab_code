# Document workflows for their readers

Write all user-facing analysis documentation for biologists, following
`dunnlab-coding-defaults`. Readers should be able to understand the biological
question, find the relevant inputs and results, and see how the analysis was done
without running it or knowing the project's development history. Start with those
descriptions, then give execution instructions. Define necessary technical terms;
explain safeguards through their practical consequences rather than opening with
an agent instruction, binding rule, or software specification.

Keep the root README concise. Give each set of execution instructions one
canonical home, commonly an analysis README, and link to it from other guides.
Apply the same focused style to methods, data, software, setup, and cluster guides.
Describe the current analysis and retain limitations that affect interpretation
or reproduction. Remove obsolete methods, superseded results, migration notes,
failed attempts, and development chronology from these guides. Preserve the
underlying records in their existing archive or developer documentation.

## Connect the manuscript to the repository

For a repository accompanying a paper, read the current manuscript source before
organizing the README. Use the draft when the paper is not yet published. Introduce
the repository as its companion, with the manuscript title, citation, and public
link when available. Use a clearly marked placeholder for an unavailable citation
or link; do not invent metadata or expose a private manuscript path as a public link.
If the manuscript is unavailable, leave its mapping explicitly pending instead of
inventing Results headings or figure numbers.

Near the beginning of the root README, include a table that connects the paper
directly to repository contents. Copy the Results headings and their order, use
the same biological terms, and include the relevant main and supplementary figure
or table identifiers. Link each row to the actual analysis guide or code and the
available inputs or results. This is the table's shape, with illustrative paths:

```markdown
| Results section in the paper | Figures and tables | Analyses and files |
| --- | --- | --- |
| Tissue-specific expression | Figure 2; Table S1 | [Analysis and code](workflows/expression/README.md), [sample metadata](resources/expression/samples.tsv), [abundance table](results/expression/abundance.tsv) |
```

Use real tracked paths, durable deposits, or clear retrieval instructions. Explain
where experimental results or analyses performed elsewhere are documented without
implying that this repository contains their code or raw data. Keep the manuscript,
its supplementary materials, and repository resources distinguishable.

A broader preliminary analysis report may remain in the repository, but do not
send readers to it as the starting point, present it as the manuscript or
supplementary information, or use its outline and figure numbers for this table.
Reader-facing guides describe the selected analyses and supporting controls;
retaining research history does not require narrating or advertising it there.

The table provides navigation over the established directory layout; it does not
require moving files or rebuilding analyses. Keep it current when manuscript
headings, ordering, figure identifiers, or selected outputs change. Check its links
against the files and the manuscript, and provide the repository link in the paper
when editing the manuscript is within scope.

## Make launching the analysis explicit

Give the analysis README a clearly labeled run section containing:

- The working directory, environment setup/activation, and required inputs or
  their acquisition command.
- A copyable execution command, with the actual entry point, configuration,
  target, and cores or execution profile where relevant. For Snakemake, also give
  a separate dry-run command. For other tools, document a supported preview or
  bounded check when useful; do not invent a dry-run mode for a script or notebook.
- What the command runs and where its main outputs appear. Distinguish the full
  analysis from optional or bounded stages and explain required upstream work.

For a repository with several analyses, make the root README an obvious index
to each analysis's canonical launch instructions. For a single analysis, those
instructions can live directly in the root README. Do not leave the only launch
command in an agent instruction file, a development note, or an unexplained batch
script. Check the documented launch route with an appropriate dry run, small
execution, or existing matching execution evidence when the environment and inputs
are available; record unavailable checks honestly.

Do not make readers derive execution commands by removing dry-run flags. A
domain-specific Snakefile is not a repository-wide workflow. Identify restricted
entry points that deliberately consume only completed staged inputs.

For Snakemake projects, embed a generated `--rulegraph` visualization next to the
launch instructions. Use [rule graph generation](rulegraphs.md) for the shared
generation command and CI freshness check; do not maintain a second diagram by
hand. The graph explains dependency structure, while the commands explain launch.

## Keep the reproduction route and evidence clear

Present one normal source-to-result route that reuses verified local inputs and
obtains missing ones. External caches are optional optimizations. Document access
or import procedures for restricted or manually collected inputs, and preserve the
source version used. Frozen-intermediate regression checks belong in developer
documentation; they are not a substitute public reproduction route.

Keep provisional and selected products distinguishable in paths or an explicit
inventory. For example, `exploratory/<domain>/` can preserve investigations while
`results/<domain>/` contains selected workflow products. Shared source can remain
in the normal source tree. Inspect contents before claiming this distinction
holds; do not move data or break evidence pointers merely to make prose true.

Distinguish workflow definitions from verified completed results and link the
selected evidence. Keep reproduction limits visible, including unavailable inputs,
external services, model dependencies, or required human work. Define institution-
specific services and link official documentation as well as local launchers.

Preserve data underlying figures and the code used to generate them. Keep human
interpretation or presentation steps explicit. Link readers to the selected
outputs and their methods, with detailed execution evidence available separately.

After a change, check all related user-facing guides for stale commands,
duplicated instructions, obsolete analyses, incorrect output boundaries, and
broken references. For a manuscript companion, also compare its navigation table
with the current paper. Update active documentation without rewriting immutable
run histories or relabeling preliminary outputs as published results.
