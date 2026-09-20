# Phase 3: Distillation

Turn the selected exploratory work into durable analyses that meet the spec. Prioritize reproducibility, simplicity, and clarity while meeting the scientific goals. A reader should be able to trace inputs through methods to reported results without an agent interpreting the workflow.

## Retain sound work and close the gaps

Start from the spec and the components identified during Exploration. Keep verified transformations, shared code, and useful execution records. Refactor or replace only what is needed to eliminate ambiguity, implement the specified method, or meet the durability and validation requirements. A rewrite is an option when the existing implementation cannot meet those requirements, not the default.

Preserve exploratory baselines before modifying their code or outputs. Build or promote the selected analysis into `analyses/` or its recorded equivalent, using shared source code where appropriate. Do not move files in ways that break evidence pointers. A promoted analysis must run without hidden notebook state, unrecorded edits, or dependencies on mutable exploratory files.

Define the final analyses and their provenance explicitly. Selecting files from exploration is insufficient unless their inputs, methods, parameters, and outputs are shown to match the spec. Minimizing changes reduces opportunities for inconsistency; it does not waive verification.

Begin the durable build discipline here: close gaps in small coherent steps, verify consequential transformations, and document how to run them. Use `dunnlab-new-project` Step 8 and relevant engineering checks from Step 9 when available. A script, notebook executable from a clean kernel, or workflow engine is acceptable if it meets the same reproducibility requirements.

Plan for a clean recomputation, or reuse an already documented clean run if it covers the final workflow exactly. If cost or an unavailable dependency prevents required execution, prepare a concrete alternative with its evidence limits. Ask only for a tradeoff or resources not already authorized. Do not label a partial or cached run as a successful clean run.

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

- [ ] The workflow runs from preserved original inputs through all specified computational outputs in a clean workspace and reconstructed environment.
- [ ] Manual, external-service, and model dependencies are explicit, with recoverable inputs and verification evidence; model access is disabled successfully where no LLM dependency is declared.
- [ ] Every output traces to its analysis, completed run, inputs, and executed settings.
- [ ] Audit manifests regenerate deterministically from selected records and agree with the actual artifacts.
- [ ] Every required analysis, control, diagnostic, and validation implementation is accounted for; unplanned outputs are investigated and excluded from the selected set or added through a deliberate spec amendment.
- [ ] Relevant tests and engineering checks pass, with any inapplicable checks justified.

Record commands, source/input identities, results, and limitations in the gate report. Build the environment in isolation instead of deleting the user's working environment. Identify the clean run so Validation can reuse its evidence if the relevant source, inputs, and environment have not changed. Required execution that remains unavailable keeps the gate open.
