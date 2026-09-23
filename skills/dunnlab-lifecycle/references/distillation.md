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

## Keep analysis commands in the rules

Treat the workflow rules as the reader's view of the scientific computation. Keep external executables and their meaningful options visible in `shell:` blocks. Resolve simple values from configuration in `params:`; do not move the entire command into a Python function or opaque option bundle. Declare consumed artifacts in `input:` and produced artifacts in `output:` so the data flow is visible without tracing wrapper code.

For example, this illustrative Snakemake rule keeps the inference visible while delegating checks to small scripts (the model and search count come from the scientific design, not this example):

```python
rule constrained_inference:
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
- [ ] The workflow runs from preserved original inputs through all specified computational outputs in a clean workspace and reconstructed environment.
- [ ] Manual, external-service, and model dependencies are explicit, with recoverable inputs and verification evidence; model access is disabled successfully where no LLM dependency is declared.
- [ ] Every output traces to its analysis, completed run, inputs, and executed settings.
- [ ] Audit manifests regenerate deterministically from selected records and agree with the actual artifacts.
- [ ] Every specified primary analysis, sensitivity analysis, control, and diagnostic has produced its required outputs and run records. Unplanned scientific analyses return to Exploration for a scope decision before joining the selected set.
- [ ] Relevant tests and engineering checks pass, with any inapplicable checks justified.

Record commands, source/input identities, results, and limitations in the gate report. Build the environment in isolation instead of deleting the user's working environment. Identify the clean run so Validation can reuse its evidence if the relevant source, inputs, and environment have not changed. Required execution that remains unavailable keeps the gate open.
