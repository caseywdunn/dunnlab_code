# Phase 3: Distillation

Select and promote the analyses supporting the deliverable, prune the maintained
surface, and close the gaps against the spec. Use `dunnlab-workflow-design` for
architecture, execution records, valid reuse, and reader documentation; these
principles already apply during Exploration.

## Retain the implementation; complete the evidence

Start with the selected configurations, verified transformations, shared rules or
functions, and execution records. Refactor only to remove ambiguity, implement the
specified method, or meet a concrete durability requirement. A rewrite needs a
reason; moving to a new directory is not itself promotion.

Preserve exploratory baselines before editing their code or outputs. Mark the
selected analysis set and its outputs clearly, using the established layout.
Shared source can continue to serve exploratory and selected runs. Avoid moves
that break evidence pointers, and remove dependencies on hidden notebook state,
unrecorded edits, or mutable exploratory artifacts.

Prune unused branches from the maintained entry points and reported result set.
Preserve the findings, failed attempts, alternatives, and post hoc decisions that
explain how the scope was chosen. Retain controls, diagnostics, and sensitivity
analyses needed to support the claims, even when they are not headline results.
Selecting existing files is insufficient without verifying that their inputs,
methods, parameters, and outputs match the spec.

Close implementation and evidence gaps in small coherent changes with focused
verification. Complete all specified analyses. New methodological choices or
scientific investigations return the affected scope to Exploration; do not hide
them inside consolidation. Recover verifiable missing provenance or rerun affected
work rather than inventing execution history after the fact.

## Establish reproducibility

Use the workflow design's [execution records and provenance guidance](../../dunnlab-workflow-design/references/provenance.md).
Select completed runs matching the specified analyses and verify their outputs.
Reuse an existing inventory that supplies the required traceability, or generate
a compact audit manifest from the run records when needed. Preserve distinct
execution identities; expected changes in run IDs or timestamps are not scientific
failures.

Establish a full computational run from preserved original inputs through all
specified outputs in an isolated clean workspace with a reconstructed environment.
Reuse an already documented clean run if it covers the relevant final computation;
do not repeat expensive work merely for a rename or organizational refactor.
Cached intermediates or a partial run do not establish a new clean run. If cost or
an unavailable dependency prevents required execution, record the gap and a
concrete alternative with its evidence limits. Ask only for resources or tradeoffs
not already authorized; unavailable required evidence keeps the gate open.

Track whether an LLM is on the data path: does reproducing a reported result require
calling a model, or did the model only help write durable code? Replace on-path
steps with code where that preserves the intended method. If no LLM dependency is
declared, verify execution with model access disabled. When the LLM is part of the
scientific method, preserve model/version, prompts, schemas, settings, responses,
and task-appropriate checks. Verify replay of saved responses separately from a
fresh invocation; replay is conditional on those responses. Record similar limits
for external services, manual interpretation, or renewed human work.

## Gate: the specified analysis is reproducible

- [ ] The selected primary, sensitivity, control, and diagnostic analyses meet the
  spec and have verified outputs and completed execution records.
- [ ] Each reported output traces to its analysis, inputs, executed settings, and
  selected run; the selected inventory agrees with artifacts, and any generated
  manifests regenerate from preserved records.
- [ ] Clean execution evidence covers the selected computation and reconstructed
  environment, with relevant engineering checks passed.
- [ ] External, human, and model dependencies have recoverable inputs, verification
  evidence, and explicit reproduction limits.
- [ ] Reader documentation identifies the maintained scope, its reproduction route,
  verified results, limitations, and preserved exploratory evidence.

Record evidence identities, checks actually run, reused evidence, and limitations
so Validation can assess the result without repeating unchanged expensive work.
