# Phase 4: Validation

Assess whether the selected analyses support the claims and whether the deliverable
matches the evidence. Successful execution and agreement with an earlier
implementation do not alone establish scientific correctness.

## Assess existing evidence and route gaps

Rerun specified analyses, check calculations, inspect provenance, compare outputs,
and apply correctness checks as needed. Small verification scripts can summarize
existing evidence or check specified behavior. New scientific investigations,
including newly designed sensitivity analyses, belong to Exploration. Record the
unsupported claim or unresolved choice and return only that scope for a decision.
Complete already specified missing outputs or implementation repairs through
Distillation and recheck affected evidence. Correct reporting directly when
existing evidence establishes the correction.

Keep failed assessments and the gate open until required gaps are resolved. A
minor repair need not trigger whole-project state changes or duplicate reports;
preserve the finding, correction, and new assessment. Continue independent checks
and use existing authorization without expanding scientific scope or spending.

## Compare results using the specified criteria

Use comparison metrics and acceptance criteria established before inspecting
validation differences. Match criteria to the result: exact equality for
deterministic counts, justified numerical tolerances for estimates,
distributional or uncertainty-based checks for stochastic outputs, and explicit
criteria for qualitative judgments. Assess scientific implications and uncertainty
alongside point estimates.

Missing criteria or unresolved scientific judgments return the affected analysis
to Exploration. If criteria change after inspecting results, preserve the failed
assessment and scientific rationale; do not loosen them merely to pass.

Locate preserved exploratory baselines and verify their input versions, settings,
code, and outputs. Compare like with like, identifying deliberate differences.
Resolve discrepancies in writing: an exploratory error, a promotion error,
superseded inputs, or dependence on defensible choices requires different action.
Do not choose the preferred result when the cause remains unresolved.

When no usable baseline exists, assess the alternative evidence identified in the
spec: an independent implementation, analytic result, known-answer benchmark,
controlled simulation, or independent assessment against a protocol. If it must
be newly designed or produced, route that gap to the appropriate earlier work.
A second execution of the same code establishes reproducibility, not independent
correctness. Shared exploratory and retained code can share errors; assess
domain-appropriate controls even when outputs agree. Missing adequate evidence
keeps the criterion open rather than waiving it.

## Assess robustness and reproduction

Check whether existing sensitivity analyses and controls address the claims'
plausible failure modes, consequential choices, input dependencies, and relevant
interactions. Assess instability, null findings, exclusions, and uncertainty, and
verify that limitations are reported. Judge coverage in proportion to the claims;
an inapplicable class of sensitivity analysis needs a rationale, not an automatic
extra run. Missing investigations require an explicit scientific scope decision.

Reuse [Distillation's clean execution evidence](distillation.md#establish-reproducibility)
when it covers the relevant source, inputs, settings, and environment. Record
the identity match and actual coverage. Repeat expensive computation only when
existing evidence no longer covers it or an independent rerun is required by the
validation criteria. Verify selected artifacts and regenerated manifests, applying
the specified scientific comparison criteria to new runs. Do not silently replace
a baseline because run metadata or outputs differ.

Check model-free execution evidence where no model dependency is declared. For
on-path models, external services, and human steps, report what was replayed or
repeated, how it was verified, and the remaining reproduction limits.

## Trace the deliverable to the analysis

Every result produced here and reported in the deliverable must trace to a selected
verified output or documented interpretation:

- Numbers, units, uncertainty, tables, and figures agree with generated artifacts,
  allowing documented display rounding.
- Methods and software versions match execution records.
- Figures and summaries regenerate from preserved outputs; human interpretation
  and presentation steps are explicit.
- Controls, sensitivity results, exclusions, and post hoc choices are described
  where they affect interpretation.

Reuse the spec's claim-to-output mapping where sufficient. Literature claims need
citations, not entries in the project's output manifest. Confirm that readers can
understand the analysis and its reproduction route using the workflow design
guidance. Apply relevant `dunnlab-codereview` checks, reusing valid engineering
evidence; review alone does not replace comparison or execution.

## Gate: ready for the intended deliverable

- [ ] Claims have baseline comparisons or justified alternative evidence meeting
  stated criteria, with discrepancies resolved.
- [ ] Robustness, controls, and uncertainty support the claims with limitations
  and any inapplicable checks justified.
- [ ] Clean execution and relevant engineering evidence cover the selected workflow;
  records and artifacts agree and reproduction limits are explicit.
- [ ] Reported results trace to verified outputs and accurately describe the
  methods, uncertainty, and scientific choices.
- [ ] Relevant code review is complete and reader documentation explains reproduction
  and access to preserved exploratory evidence.

Record executed checks, reused evidence, and scientific judgments. Unresolved
required checks keep the gate open. When the assessed scope passes, record
Validation as passed; publication, submission, or removal of exploratory evidence
still requires authorization for that action.
