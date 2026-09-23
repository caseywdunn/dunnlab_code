# Snakemake organization

Read this when implementing or refactoring a Snakemake workflow, including during
exploration. These are lab readability conventions; preserve working equivalents
unless a change improves the actual workflow. Small workflows can remain in one
Snakefile. Use per-rule `conda:` environments where dependencies need isolation,
and declare actual consumed artifacts and helper scripts as dependencies.

Generic completion and reuse requirements live in
[execution provenance](provenance.md). Yale submission, storage, and executor
settings belong to `dunnlab-hpc`.

## Use thin entry points and stage-specific rules

For a substantial multi-stage analysis, keep the main workflow file thin: load
configuration, include named rule files grouped by scientific purpose, and
declare final targets. In Snakemake, a suitable layout is a domain `Snakefile` with
`rules/discovery.smk`, `rules/matrices.smk`, `rules/inference.smk`,
`rules/topology.smk` and `rules/reports.smk`, adapted to the actual analysis.
Use a small common configuration loader only where shared setup warrants it.
Keep stage-specific helpers with their rules and external analysis commands
visible there. Do not replace a large Snakefile with opaque Python orchestration,
deep include chains, or one file per trivial rule; small workflows can stay whole.

Start each rule file with a short comment block or module docstring explaining
its scientific purpose and data flow. State what its inputs represent and what
its products are used for, then list the scientific steps in data-flow order,
with the exact relevant rule names after each step. Identify the downstream
handoff when it crosses a file boundary. For thin entry points, summarize the
included stages and final aggregate target instead of duplicating their rule
lists. A one-step file needs only a one-step summary.

For example, a taxon-sampling rule file could begin:

```python
"""
Build broad reference trees for distance-based taxon selection. These sampling
trees guide matrix construction for final phylogenetic inference and AU tests.

1. Validate the input sequence catalog: validate_catalog.
2. Extract eligible regions from catalog sequences: prepare_sampling_sequences,
   search_sampling_domains_hmmsearch, extract_sampling_regions.
3. Build profile-based alignments: align_sampling_sequences_hmmalign,
   build_sampling_matrices.
4. Infer and validate sampling trees: infer_sampling_tree_iqtree,
   validate_sampling_tree.

Next: select_taxon_panel in panels_matrices.smk uses these trees to select
sequences for downstream matrix construction.
"""
```

Adapt the summary to the actual rules, not a generic pipeline. Keep it scientific
and reader-facing: no development history, repeated command options or detailed
validation internals. Update the summary and rule lists whenever rules are
renamed, moved or their purpose changes; check that the listed names exist and
the stated handoffs match the dependencies.

Order stage includes and rules in data-flow order: producers before consumers,
with input preparation followed by analysis, validation and summaries. Put imports,
configuration and necessary helper definitions before their uses. Place `rule all`
at the bottom of the entry point, after the stage includes, and mark it explicitly
with `default_target: True`; do not rely on the first rule being the default.
Apply the same convention to restricted entry points. This is a readability
convention, not execution sequencing: Snakemake schedules from dependencies.
Direct references such as `rules.catalog.output.receipt` do require the producer
rule to have been defined earlier. Do not use `ruleorder` to express execution
sequence; it resolves competing producers, not dependencies.

Provide one coherent full-workflow entry point per domain and named stage targets.
Define the default target's scope explicitly; a target called `all` should cover
the declared full analysis, while targets such as `inference` or `topology`
select bounded scientific stages. Connected downstream analyses should be part
of that dependency graph, not accessible only through an unrelated entry point.
Document that stage targets normally build missing upstream dependencies.

Where an established workflow must consume completed inputs without rebuilding
them, retain a thin restricted entry point that includes the same configuration
and downstream rules but omits upstream construction rules. This is a bounded
view of the same analysis, not a duplicate implementation or a second parameter
set. Test that missing staged inputs fail rather than triggering upstream work.
Do not add such entry points without an actual reuse or execution-boundary need.

Changing includes or default targets can change what existing launch commands
schedule even when scientific parameters are unchanged. Inspect batch scripts,
snapshot packaging and documented commands; make bounded launchers request an
explicit target. Check relative script/environment paths after moving rules.
Dry-run the full graph and bounded paths, checking analysis counts, shared matrix
identities and excluded stages. Preserve submitted snapshots and completed runs;
an organizational refactor alone is not a reason to rerun them.

## Name rules for readable rule graphs

Use consistent snake_case names: `<action>_<scientific_object>_<tool>` for
external scientific tools, for example `align_matrix_mafft`,
`infer_tree_model_selection_iqtree`, `infer_constrained_tree_iqtree`,
`test_topologies_au_iqtree`, and `quantify_expression_salmon`. Use the same tool
suffix wherever that tool performs the scientific step; do not append versions
or implementation languages such as `_python` or `_r`.

For other steps, use action and object without an artificial tool suffix:
`prepare_discovery_sequences`, `select_taxon_panel`, `validate_inferred_tree`,
and `report_matrices`. Reserve `validate_` for checks, `record_` for provenance,
and `report_` for reports. Name substantive custom methods by their scientific
purpose. Avoid vague names, numbered steps and redundant domain prefixes.
Keep short aggregate targets such as `all`, `matrices`, `inference` and `topology`.
A reader should understand each analysis step from its rule-graph label alone.

When renaming, update rule references, launch filters, tests and documented
targets together. Verify that commands and graph dependencies remain unchanged;
do not rewrite names in preserved run records or rerun completed analyses merely
because a rule was renamed.

## Keep analysis commands in the rules

Treat the workflow rules as the reader's view of the scientific computation. Keep external executables and their meaningful options visible in `shell:` blocks. Resolve simple values from configuration in `params:`; do not move the entire command into a Python function or opaque option bundle. Declare consumed artifacts in `input:` and produced artifacts in `output:` so the data flow is visible without tracing wrapper code.

For example, this illustrative Snakemake rule keeps the inference visible while delegating checks to small scripts (the model and search count come from the scientific design, not this example):

```python
rule infer_constrained_tree_iqtree:
    input:
        matrix="matrices/{matrix}.faa",
        constraint="constraints/{matrix}__{hypothesis}.nwk",
    output:
        tree="trees/{matrix}__{hypothesis}.treefile",
        report="trees/{matrix}__{hypothesis}.iqtree",
    params:
        prefix="trees/{matrix}__{hypothesis}",
        model=config["model"],
        runs=config["search_runs"],
        seed=config["seed"],
    threads: config["threads"]
    log: "logs/{matrix}__{hypothesis}.log"
    shell:
        """
        python scripts/check_inputs.py --matrix {input.matrix:q} --constraint {input.constraint:q}
        iqtree3 -s {input.matrix:q} -g {input.constraint:q} \\
          -m {params.model:q} --runs {params.runs} --seed {params.seed} \\
          -T {threads} --prefix {params.prefix:q} > {log:q} 2>&1
        python scripts/check_tree.py --matrix {input.matrix:q} --tree {output.tree:q}
        """
```

Only add those validators when they address an actual correctness requirement. A separate validation rule is also appropriate, provided downstream targets depend on its successful output. Keep version checks, output checks, and provenance generation out of command-building wrappers. Record the command actually executed using the engine's shell-command logging or tool logs instead of maintaining a second command implementation for reporting.

Keep checks proportional to the science and likely mistakes. Trusted research inputs do not require a security-oriented validation framework. Prefer a few focused checks and existing workflow features over custom orchestration, nested receipts, or repeated verification at every layer. Broad shared validation utilities should not become dependencies of expensive analysis jobs unless their changes actually affect those computations; separate validation dependencies where possible.


For syntax and scheduling semantics, consult the official
[Snakemake rules documentation](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html).
The bottom-of-file aggregate target and scientific naming scheme above are lab
preferences, not requirements imposed by Snakemake.
