---
name: dunnlab-lifecycle
description: >
  Plan, explore, distill, and validate scientific analyses in any discipline,
  with evidence recorded at each phase gate. Use when organizing a research
  analysis, turning exploratory work into reproducible reported results,
  preparing analyses for a manuscript or public repository, or assessing
  a project's lifecycle phase and analysis provenance.
---

# Dunn Lab Analysis Lifecycle

A scientific analysis moves through four phases. Each ends at a gate supported by recorded evidence: executable checks where possible, and explicit scientific judgments where execution alone cannot decide. The lifecycle applies to measurements, observations, simulations, and qualitative or quantitative analyses; it does not prescribe a data format, method, or workflow engine.

| Phase | Produces | Gate |
|---|---|---|
| 1. Planning | Questions, inputs, candidate methods | Feasible next actions and explicit dependencies |
| 2. Exploration | Findings that shape the design | A spec linking planned claims, analyses, and validation checks |
| 3. Distillation | Reproducible analyses behind reported results | A clean run with traceable outputs and documented external or model dependencies |
| 4. Validation | Assessment of existing analyses, evidence, and reported claims | Correctness, reproducibility, existing robustness evidence, and report traceability meet stated criteria |

Exploration should be fast, branching, and inexpensive enough to change direction. Use clear identities, rerunnable transformations, and lightweight provenance from the start so successful work is easy to retain. Reported results need a small, consistent, auditable set that a human can inspect without an agent interpreting it for them. Keep provisional findings distinguishable from verified results while sharing sound code and preserving the evidence behind scientific decisions.

Avoid both premature hardening of uncertain branches and throwaway work that must be reconstructed later. [Exploration](references/exploration.md) balances inexpensive investigation with preparation for reuse.

**Distillation retains verified work and closes the gaps against a spec.** Minimize rewriting and duplicate implementations; see [references/distillation.md](references/distillation.md).

Repository READMEs address readers of the scientific work, not its developers.
Describe current analyses and reproduction; keep development history, internal
regression instructions and launch-review notes in `dev_docs/`. Follow the
[distillation documentation guidance](references/distillation.md#document-for-readers-not-developers).

## Scope of invocation

For reviews, explanations, naming advice, or phase assessments, read and report without creating state, moving files, running analyses, or committing changes. Execute the lifecycle only to the extent authorized by the user's task. Existing authorization persists across phases; this skill does not require asking again for work already requested.

Use “reported results” below to mean the outputs of a paper, report, dataset release, or other scientific deliverable. Adapt the required artifacts to that deliverable; do not require a manuscript for a project that has none.

## Where am I?

Read `dev_docs/lifecycle.yaml` when resuming. Verify that its evidence still applies to the current inputs, spec, and code. A missing state file does not mean an existing project must restart:

1. Inspect existing equivalents of the plan, spec, reproducible workflow, and validation evidence. No actionable plan suggests Planning; a plan without settled scope suggests Exploration; a spec without a verified run suggests Distillation; a verified run with scientific checks outstanding suggests Validation.
2. Report the inferred phase and uncertainty. Ask only if an ambiguity affects the next action; do not downgrade a mature project just because its documents use different names.
3. During authorized lifecycle work, create or update the state file using the actual artifact paths. A completed project remains `phase: validation` with `gate_status: passed`.

```yaml
# Dunn Lab analysis lifecycle — updated by the dunnlab-lifecycle skill
updated: 2026-09-19       # use the actual update date
phase: exploration        # planning | exploration | distillation | validation
gate_status: open         # open | passed
artifacts:
  plan: dev_docs/overview.md
  spec: null
gate_report: null         # e.g. dev_docs/gates/exploration.md
assessed_revision: null   # source revision or immutable snapshot evaluated
notes: ""
```

Track this file and gate reports in version control, following the project's commit workflow and the user's scope. It records phase state, not a task checklist. The scientific record lives in the plan, spec, findings, and run records. Use `dev_docs/` so the record is readable independently of the agent harness.

Projects run for months across many sessions with the context cleared between them, so re-read this file whenever you resume rather than trusting conversation context.

## Working a phase

During execution, read the current phase's reference; load another only for a transition or a specific dependency. A review of the skill may inspect all phases. Keep exploration's lighter engineering requirements distinct from those for durable results.

- [Planning](references/planning.md)
- [Exploration](references/exploration.md)
- [Distillation](references/distillation.md)
- [Validation](references/validation.md)

## Gates

A gate is a decision rule you evaluate. Write a report, normally `dev_docs/gates/<phase>.md`, containing the criteria, checks actually run and their results, scientific judgments and rationale, unresolved gaps, and the decision. Identify the evaluated source revision and, where applicable, spec fingerprint, input versions or hashes, and relevant run records. For uncommitted source, identify a preserved snapshot; a commit ID alone does not describe those edits.

- **Passes** — record `gate_status: passed` and link the evidence. Announce the transition and continue if the next phase is already authorized. Otherwise, prepare the proposed scope and cost before asking for the missing decision. On entry to the next phase, reset its gate status to `open` and its evidence pointers to `null`; retain the previous report.
- **Fails** — keep the gate `open`, identify the failed criterion, and continue feasible work within scope.
- **Cannot be evaluated** — keep the gate `open` and record the missing evidence. Continue independent work; ask only for information or authorization needed to resolve the gap. An unavailable required check is not a pass.

When inputs, methods, claims, or code change, assess which evidence is invalidated. Reopen the earliest affected phase and mark dependent gate reports superseded until their checks are re-established. A scope change returns to Exploration; an implementation correction generally returns to Distillation. Editorial changes need not invalidate computational evidence. Preserve the reason and earlier evidence in version history.

Validation assesses what is present. It may rerun the specified analysis, check calculations, compare outputs, and inspect provenance and existing sensitivity evidence. It does not design or run new scientific analyses, vary scientific settings to investigate their effects, or expand the spec to fill an evidence gap while remaining in Validation.

If validation finds missing sensitivity evidence requiring investigation, unresolved methodological choices, or inadequate scientific support for a claim, record the deficiency and reopen Exploration before doing that scientific work. If it finds an implementation error, a missing output from an already specified analysis, a provenance gap, or failure to reproduce the specified analysis, reopen Distillation before making the repair. Update phase state, preserve the failed assessment, and return to Validation after the affected earlier gates pass. Announce these transitions and follow the existing authorization rules; a failed assessment does not itself authorize expanded scope or spending.

## Relationship to other skills

This skill sequences work. Use available companion skills when relevant; if absent, follow existing project conventions and the requirements here:

- **`dunnlab-new-project`** — owns scaffolding and the build loop. See the boundary below; getting it wrong is the most likely way these two skills work against each other.
- **`dunnlab-defaults`** — coding standards, project structure, and workflow orchestration appropriate to the analysis.
- **Domain skills** — scientific methods and data-specific checks only when relevant to the project.
- **`dunnlab-codereview`** — run its checklist during Validation instead of inventing a second one.
- **`dunnlab-biblio`** — methods and reference formatting when writing up.

### The boundary with `dunnlab-new-project`

That skill is two things joined together, and only one of them is yours to drive:

| Its steps | Who owns it |
|---|---|
| Steps 1–3, 6–7 — repository and environment setup | `dunnlab-new-project`, when scaffolding is needed and authorized. |
| Steps 4–5 — planning documents | Shared. Extend `dev_docs/overview.md` with the scientific plan; do not create a duplicate. |
| Step 8 — the build loop | Exploration uses a lighter loop; Distillation uses incremental implementation and verification. |
| Step 9 — final verification | Distillation establishes engineering evidence; Validation assesses existing analyses and scientific support, reusing valid evidence. |

At Step 8, research projects use the phase established here rather than automatically restarting Exploration. Reuse sound components and retain checks that protect scientific decisions during Exploration; defer speculative interfaces and exhaustive engineering work. Apply the durable build discipline to remaining gaps at the start of Distillation.

Two state files coexist and do not conflict because they work at different scales: `dev_docs/lifecycle.yaml` records which phase the project is in, and `.agent/new-project-progress.yaml` is a within-stage task checklist. Keep it that way — if this file starts tracking tasks, they will drift apart.

### Directory layout

`exploratory/` and `analyses/` are the default split for provisional and durable analysis artifacts; shared source code can serve both. Preserve an established equivalent layout and record its paths. Keep original inputs immutable and write derivatives separately. Organize analysis subdirectories and use a workflow engine only when the project's complexity warrants them.

### Precedence for analysis artifacts

Use stable identities for distilled outputs and explicit provenance for history. Dates may be meaningful input identifiers, such as an observation period or release. Override existence-only checkpointing: an existing output is reusable only when its completed run record matches the current inputs, code, and parameters. Exploration's limited hardening requirements override generic demands to fully test and document every throwaway script, but never waive basic correctness checks.

## The data path

### Make the analysis visible

Keep external analysis tool calls directly in workflow rules as shell commands wherever practical. A reader scanning the rules should see the executable, scientifically meaningful options, inputs, outputs, and dependencies. Use named parameters and configuration values for variation, but do not hide the command or its options in a command-builder helper, generic runner, or subprocess wrapper.

Keep validation logic in focused scripts called before or after the analysis command, or in separate rules with explicit dependencies. The analysis should be readable at a glance without reading the validation implementation. Use scripts for substantive transformations and methods that need them; wrapping a straightforward external command solely to attach validation or provenance is unnecessary indirection.

Prefer the simplest implementation that makes the scientific method reproducible and clear. Assume project inputs and configuration are trusted: do not add security frameworks, adversarial-input checks, or defensive layers without a concrete requirement. Retain scientific correctness checks, ordinary shell quoting, useful execution records, and safeguards against accidental data loss. Reuse the workflow engine's dependency tracking and logs; add custom validation or provenance machinery only for a specific gap, and keep it separate from the visible analysis commands. See the [Distillation example](references/distillation.md#keep-analysis-commands-in-the-rules).

Throughout, track whether an LLM sits *on* the data path — whether reproducing a reported result requires invoking a model — or *off* it, having produced durable code that does. The operational test: can the published analysis be rerun from inputs to results without calling an LLM?

Exploration may use LLMs on the data path while preserving inputs, transformations, and outputs needed to interpret findings. Distillation replaces those steps with durable code wherever feasible. If an LLM capability is part of the scientific method, retain it explicitly with model/version, prompts, settings, saved responses, and task-appropriate verification. The gates allow this documented exception and must state the resulting reproducibility limits; replaying saved responses is distinct from reproducing a new model invocation. Details belong in the phase references.
