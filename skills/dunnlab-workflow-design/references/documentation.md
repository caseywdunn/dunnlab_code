# Document workflows for their readers

Write root and analysis READMEs for people who need to understand and reproduce
the work. Describe its current scope, methods, inputs, outputs, software
requirements, and usable entry points. Keep development history, implementation
decisions, progress, review gates, and failed attempts in `dev_docs/` or linked
provenance records. Do not turn public instructions into a construction narrative.

Keep the root README concise and link to the analysis guide and report. Give each
set of execution instructions one canonical home, commonly a workflow README;
link to it from other guides instead of copying commands or analysis grids.
Domain guides explain methods, inputs, products, and requirements.

## Make launching the analysis explicit

Give the analysis README a clearly labeled run section containing:

- The working directory, environment setup/activation, and required inputs or
  their acquisition command.
- A copyable dry-run command and a separate execution command, with the actual
  Snakefile, configuration, target, and cores or execution profile where relevant.
- What the command runs and where its main outputs appear. Distinguish the full
  analysis from optional or bounded stages and explain required upstream work.

For a repository with several analyses, make the root README an obvious index
to each analysis's canonical launch instructions. For a single analysis, those
instructions can live directly in the root README. Do not leave the only launch
command in an agent instruction file, a development note, or an unexplained batch
script. Check the documented dry-run command against the actual project when the
required environment and inputs are available; record unavailable checks honestly.

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
interpretation or presentation steps explicit. The maintained report may live
outside the exploratory archive while linking the evidence behind its results.

After a change, check related guides for stale commands, duplicated instructions,
incorrect output boundaries, and broken references. Update active documentation
without rewriting immutable run histories.
