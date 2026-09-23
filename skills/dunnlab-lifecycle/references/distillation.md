# Phase 3: Distillation

Turn the selected exploratory work into durable analyses that meet the spec. Prioritize reproducibility, simplicity, and clarity while meeting the scientific goals. A reader should be able to trace inputs through methods to reported results without an agent interpreting the workflow.

## Retain sound work and close the gaps

Start from the spec and the components identified during Exploration. Keep verified transformations, shared code, and useful execution records. Refactor or replace only what is needed to eliminate ambiguity, implement the specified method, or meet the durability and validation requirements. A rewrite is an option when the existing implementation cannot meet those requirements, not the default.

Preserve exploratory baselines before modifying their code or outputs. Build or promote the selected analysis into `analyses/` or its recorded equivalent, using shared source code where appropriate. Do not move files in ways that break evidence pointers. A promoted analysis must run without hidden notebook state, unrecorded edits, or dependencies on mutable exploratory files.

Define the final analyses and their provenance explicitly. Selecting files from exploration is insufficient unless their inputs, methods, parameters, and outputs are shown to match the spec. Minimizing changes reduces opportunities for inconsistency; it does not waive verification.

Complete the specified sensitivity analyses, controls, and diagnostics alongside the primary analyses. Preserve their outputs and run records so Validation can assess the existing evidence. If a missing analysis requires a new scientific design or a methodological choice, return to Exploration to settle it rather than leaving that investigation for Validation.

When Validation identifies an implementation error, provenance gap, or failure to reproduce the specified analysis, reopen this phase, make the repair, and rerun affected work. Preserve the failed assessment and the evidence of the correction, then return to Validation after this gate passes again. Do not invent missing execution provenance after the fact; recover verifiable records or rerun the affected computation.

Begin the durable build discipline here: close gaps in small coherent steps, verify consequential transformations, and document how to run them. Use `dunnlab-new-project` Step 8 and relevant engineering checks from Step 9 when available. A script, notebook executable from a clean kernel, or workflow engine is acceptable if it meets the same reproducibility requirements.

Plan for a clean recomputation, or reuse an already documented clean run if it covers the final workflow exactly. If cost or an unavailable dependency prevents required execution, prepare a concrete alternative with its evidence limits. Ask only for a tradeoff or resources not already authorized. Do not label a partial or cached run as a successful clean run.

## Document for readers, not developers

Write root and analysis READMEs for readers of the paper or report who want to
understand and reproduce the analyses. Describe the repository as it is: its
scientific scope, methods, inputs, outputs, software requirements and usable
entry points. Do not narrate construction with phrases such as "the new
reanalysis," "what changed," "now migrated," or "no revised workflow has been
launched." Development history, implementation decisions, progress, review gates,
failed attempts and intermediate-input regression instructions belong in
`dev_docs/` or dedicated provenance records, not public usage instructions.

Keep the root README a concise overview linking to the analysis guide and report.
Give each set of execution instructions one canonical home, commonly a workflow
README; link to it from the root and domain READMEs instead of copying commands
and analysis grids between them. Domain guides explain methods, inputs, products
and requirements. Show explicit, copyable execution commands **and** dry-run
commands that display what would run; do not make users derive execution commands
by removing flags. State the working directory and required environment. Identify
the scope of each entry point precisely: a domain-specific `Snakefile` is not a
repository-wide workflow. Define institution-specific services or cluster names
and link their official documentation; preserve separate links to local launchers.

Keep limitations relevant to reproduction visible without turning READMEs into
developer status logs. Distinguish workflow definitions from verified completed
results and link the selected evidence; do not imply completion or publication
merely by calling an analysis "published." Preserve detailed run histories and
failed checks in their records, rather than deleting provenance to simplify prose.

Make the output boundary explicit. In a `workflows/<domain>/` layout,
`results/<domain>/` contains products of those workflows, not a mixture with
exploratory outputs. Keep exploratory scripts, settings, inputs, intermediates,
outputs and run records together under `exploratory/<domain>/` (or the established
equivalent). A short closing archive link in the root README is sufficient.
Inspect actual contents before claiming this boundary holds; preserve evidence
paths when organizing files, and do not move data merely to make prose true.
The maintained analysis report can remain outside the exploratory archive while
its selected results are updated after workflow completion and validation.

Present one normal source-to-result route per analysis. Retrieval should reuse
valid local inputs and download missing inputs under the same command, verifying
their pinned identity. Optional external caches are optimizations, not a required
"local files versus downloads" choice. Handle interrupted downloads safely and
never silently accept mismatched bytes. Frozen-intermediate regression checks
test implementation equivalence; document them for developers rather than listing
them as an alternative public reproduction route.

When revising documentation, search the root and domain guides for repeated
commands, stale development narratives and broken cross-references. Update related
guides consistently while leaving immutable run records intact.

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

## Stable identities and a minimal analysis set

Give each input artifact, analysis, and reported output a stable identity shared by the spec, run records, manifests, and report. Retain clear identities established during Exploration. Use short descriptive filenames or an explicit lookup; filenames need not encode every parameter. Distinguish analysis identity from execution identity so reruns do not overwrite their provenance.

Record parent inputs and transformations for derivatives. Reuse a derivative when it serves multiple analyses under the same assumptions. When two derivatives differ, state the scientifically relevant difference; merge them only after verifying equivalence. The required set includes inputs for controls, diagnostics, and validation, as well as primary results.

Use provenance records for execution history. Preserve dates or collection labels when they identify scientifically meaningful inputs. Simplifying the workflow must not erase sampling differences, post hoc choices, or the distinction between exploratory and confirmatory analyses.

For stochastic methods, configure and capture seeds or random streams where supported. Replicates need explicit identities and appropriately distinct streams. Record remaining nondeterminism; a seed alone does not promise identical results across environments.

## Capture completed runs, then generate manifests

Capture provenance at execution time. Reading the current configuration after a run does not establish what produced an existing output. Each execution record must identify:

- Analysis ID, run ID, and role from the spec.
- Source revision or preserved source snapshot, spec/configuration fingerprint, and the command or entry point actually executed with resolved parameters.
- Input identities and hashes or immutable versions; include consequential reference resources or external service responses.
- Actual software/model versions, environment specification or lockfile identity, and stochastic settings where applicable.
- Completion status, logs or verification evidence, and output identities, locations, and hashes.

Record failed attempts as failures. Mark a run complete only after its expected outputs pass relevant integrity checks. An existing output may be reused only when a completed record matches the current inputs, code, environment requirements, and parameters and the stored outputs still verify. Otherwise rebuild affected steps. This overrides existence-only checkpointing in companion skills.

Generate compact audit manifests from these records and the actual artifacts. A default layout is:

| Artifact | Contents |
|---|---|
| `analyses/manifests/artifacts.tsv` | Artifact ID, role, location, hash/version, parent IDs, producing run ID, and relevant measured summaries |
| `analyses/manifests/analyses.tsv` | Analysis ID, selected completed run ID, purpose, input/output IDs, and a pointer to the full execution record |

Use a schema suited to the project; JSON or another structured format may be clearer for nested relationships. Define the fields, units, and missing-value conventions. Do not force all scientific inputs into a table or a common set of summary statistics. Generate method and result summaries from these records where useful.

Version the small manifests and keep their referenced records and artifacts recoverable. Store large or restricted content in an appropriate versioned archive, with access requirements documented; do not assume all outputs belong in git.

Regenerating a manifest from the same preserved run records should be deterministic. A new execution has a new run ID and may have different timestamps or stochastic outputs. Compare those reruns using the validation criteria; do not demand byte-identical execution metadata or silently replace the selected baseline.

## Complete the computational path

Include the following where applicable:

- Acquisition scripts for obtainable inputs, or documented access/import procedures for restricted data, physical measurements, or manually collected material. Preserve the exact source snapshot or version used.
- Input and transformation checks for relevant assumptions, such as schemas, units, ranges, missingness, or sampling relationships.
- Focused tests, including a small known-answer, analytic, or controlled synthetic case for consequential computations where feasible. If no such case is appropriate, document the alternative check and its limits.
- Configuration containing consequential parameters and paths, plus an environment specification sufficient to reconstruct the tools.
- Executable generation of reported computational results and figures. For human interpretation or annotation, preserve the protocol, decisions, and material used as explicit inputs; state which parts require renewed human work.

## LLMs on the data path

Replace model-assisted transformations with durable code wherever that preserves the intended method. For an analysis with no required LLM step, verify it runs with model access disabled.

If an LLM capability is part of the scientific method, document it as an explicit exception. Preserve the model/version, prompts, input/output schemas, settings, responses, and task-appropriate verification. Record access requirements and nondeterminism. Verify downstream replay from saved responses separately from a fresh model invocation; replay establishes reproducibility conditional on those responses. Do not describe it as a model-free reproduction of the entire method.

## Gate: the specified analysis runs

- [ ] Public documentation describes the current analyses, clearly separates workflow and exploratory products, and links to one canonical set of explicit execution and dry-run commands. Development notes and regression instructions are separate; reproduction limits remain visible.
- [ ] A reader can identify the analysis executables, meaningful options, inputs, outputs, and dependencies directly in the rules. Necessary validation is separate and proportionate; straightforward external calls are not buried in wrappers.
- [ ] Full-workflow and bounded entry points share stage rules and configuration. Dry runs confirm their documented scope, including any no-upstream-rebuild boundary; launchers and packaged dependencies match that organization.
- [ ] The workflow runs from preserved original inputs through all specified computational outputs in a clean workspace and reconstructed environment.
- [ ] Manual, external-service, and model dependencies are explicit, with recoverable inputs and verification evidence; model access is disabled successfully where no LLM dependency is declared.
- [ ] Every output traces to its analysis, completed run, inputs, and executed settings.
- [ ] Audit manifests regenerate deterministically from selected records and agree with the actual artifacts.
- [ ] Every specified primary analysis, sensitivity analysis, control, and diagnostic has produced its required outputs and run records. Unplanned scientific analyses return to Exploration for a scope decision before joining the selected set.
- [ ] Relevant tests and engineering checks pass, with any inapplicable checks justified.

Record commands, source/input identities, results, and limitations in the gate report. Build the environment in isolation instead of deleting the user's working environment. Identify the clean run so Validation can reuse its evidence if the relevant source, inputs, and environment have not changed. Required execution that remains unavailable keeps the gate open.
