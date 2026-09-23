---
name: dunnlab-lifecycle
description: >
  Plan, explore, distill, and validate scientific analyses, preserving the
  decisions and evidence behind reported results. Use when organizing research,
  selecting analyses for a deliverable, or assessing scientific readiness.
  Workflow architecture belongs to dunnlab-workflow-design.
---

# Dunn Lab Analysis Lifecycle

This skill manages scientific questions, analysis scope, and evidence of readiness.
Use [dunnlab-workflow-design](../dunnlab-workflow-design/SKILL.md) from the first
experiment: exploration and reported analyses share implementation and design
principles. Their uncertainty, selected scope, and required evidence differ.

| Phase | Purpose | Ready when |
|---|---|---|
| Planning | Turn a scientific question into feasible actions | Inputs, candidate methods, constraints, and next decisions are clear |
| Exploration | Investigate alternatives and settle the analysis design | A spec connects selected analyses, claims, and validation criteria |
| Distillation | Select, promote, and complete the retained analysis | The specified outputs have a reproducible path and verifiable execution evidence |
| Validation | Assess the existing analysis and reported claims | Correctness, robustness, reproduction, and report traceability meet stated criteria |

These phases describe work on an analysis or deliverable, not a required global
waterfall. Different analyses can be at different stages. Check correctness
throughout; final Validation assesses the assembled evidence. Distillation should
usually prune the maintained analysis surface and close gaps, while retaining
the implementation and scientific history.

## Scope and companion skills

For reviews, explanations, naming advice, or phase assessments, read and report
without creating state, moving files, running analyses, or committing changes.
Execute only the work authorized by the task; authorization persists across phases.
Adapt artifacts to the deliverable: a manuscript is not required for a dataset release.

- **`dunnlab-workflow-design`** owns architecture, execution records, reuse,
  workflow documentation, and proportional engineering practices across phases.
- **`dunnlab-new-project`** handles repository and environment scaffolding when needed.
  Extend its existing project overview rather than creating a second plan.
- **Domain skills**, such as `dunnlab-bioinformatics`, guide relevant methods,
  tool choices, and scientific checks.
- **`dunnlab-codereview`** provides the relevant engineering review checklist;
  **`dunnlab-biblio`** supports methods and references when writing up.

Load the current phase reference and any reference needed for a transition or
specific dependency. The shared workflow design applies in every phase.

- [Planning](references/planning.md)
- [Exploration](references/exploration.md)
- [Distillation](references/distillation.md)
- [Validation](references/validation.md)

## Resume from evidence

Read `dev_docs/lifecycle.yaml` when resuming and verify that its evidence still
applies to the relevant inputs, methods, and code. If it is absent, inspect the
existing plan, selected scope, workflow, and checks; do not restart a mature
analysis or require new document names. Ask only when uncertainty changes the
next action.

During authorized lifecycle work, keep a small state summary with actual artifact
paths. A small self-contained analysis can keep this summary in its existing spec
or assessment. Use a separate `lifecycle.yaml` when resumable work benefits from
it, rather than requiring another file for every task. Preserve existing fields
and conventions; for example:

```yaml
updated: 2026-09-23       # actual update date
phase: exploration      # planning | exploration | distillation | validation
gate_status: open       # open | passed
artifacts:
  plan: dev_docs/overview.md
  spec: null
gate_report: null
assessed_revision: null # revision or preserved source snapshot evaluated
notes: "Scope: the analysis or deliverable being assessed"
```

The phase summarizes the active scope. When analyses differ in readiness, record
their status in the existing spec or a small table and link it here; do not force
unrelated analyses back through earlier phases. State is a navigation aid, not a
second task list or provenance system. Version it with the project records.

## Evaluate readiness and route gaps

Record a meaningful gate decision in `dev_docs/gates/<phase>.md` or an existing
equivalent. Identify the assessed scope, criteria, checks actually run, scientific
judgments, limitations, decision, and evidence identities. Link existing run
records instead of copying them. Uncommitted code needs a preserved snapshot;
a commit ID alone does not identify those edits.
One assessment can cover Distillation and Validation for a small analysis when
it identifies the evidence for each; separate files are not required by phase.

A pass records `gate_status: passed` and the evidence. Continue already authorized
work; record the next phase as open when entering it. Failed or unavailable
required checks remain open. Preserve failed assessments and superseded evidence.
A completed scope remains in Validation with its gate passed.

When work changes, reopen only the affected criteria and dependent evidence:

- **New scientific choices, scope, or missing sensitivity investigations:** return
  the affected analysis to Exploration, settle the question, and amend the spec.
- **Implementation, provenance, or missing specified outputs:** close the
  Distillation gap and reassess the affected checks.
- **Reporting corrections supported by existing evidence:** correct and recheck
  within Validation.

Identify substantial changes in scientific scope or readiness in the state and
decision record. A small implementation repair does not require ceremonial
whole-project phase transitions or duplicate reports. Preserve the finding and
repair evidence, and do not call new scientific investigations mere validation.
Reuse unaffected checks and expensive runs when their execution evidence still
applies. A failed gate does not authorize expanded scope or spending.
