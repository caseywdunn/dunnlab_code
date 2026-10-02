# Phase 2: Exploration

Learn what the inputs support and which analyses are worth retaining. Let findings
change the design. Use `dunnlab-workflow-design` throughout: share each retained
method's implementation, express exploratory choices through inputs and settings, and
capture enough execution evidence to preserve consequential findings. The phase
boundary changes the evidence required, not the implementation by default.

## Spend effort where it changes a decision

Start with the cheapest informative comparison for each distinct question before
investing heavily in one direction. State the decision a run will inform; do not
automatically sweep every method, preprocessing choice, and subset. Add replication
when variability obscures the answer, and test interactions when choices may matter
jointly. One comparison cannot establish that a parameter never matters.

Subsample, reduce scope, or use cheaper settings when these preserve the relevant
groups, dependencies, and rare features. A cheap null may reflect low information
or approximation error: assess what it could have detected before retiring a
direction. Confirm retained approaches at appropriate precision and intended scale.

Set a budget and stopping criterion per question within authorized resources.
At the limit, summarize what was learned and reassess. Extract compact summaries
and relevant exceptions with reusable scripts; do not fill context with entire
datasets or logs. Preserve a durable handoff when the session or question changes.

Keep the checks that protect scientific decisions: relevant units, dimensions,
identifiers and joins, missingness, sampling assumptions, and successful tool
completion. Use focused known-answer checks for consequential uncertain
transformations. Improve pieces likely to survive; defer speculative interfaces,
exhaustive engineering, and presentation polish for abandoned branches.

## Investigate robustness as part of the science

Use early sensitivity checks when they affect whether to pursue a result or trust
the method. As claims settle, investigate defensible alternatives in preprocessing,
modeling, data subsets, and missing-data assumptions. Vary individual factors for
attribution and combinations where interactions are plausible; respect sampling
structure and budget. Preserve null findings and instability, and narrow claims
when warranted rather than tuning sensitivity away.

Carry selected sensitivity analyses, controls, and diagnostics into the spec.
Final Validation assesses this evidence. A missing investigation returns here for
a focused scientific decision; an already specified analysis with missing output
is a Distillation gap.

## Preserve decisions and their evidence

Keep a short findings entry per meaningful decision or result, including negative,
null, and inconclusive findings, in `exploratory/findings.md` or its equivalent:

- The question, finding, limitations, and resulting decision.
- The actual outputs and execution records supporting that decision, including
  recoverable inputs, code, parameters, software/model versions, and stochastic settings.

Reuse the project's provenance records; a pointer to a mutable file alone does
not preserve evidence. Exploratory code can be disposable; evidence behind
scientific decisions cannot. If model-assisted transformations are on the data
path, retain their inputs, prompts, settings, and responses needed to interpret
the finding. Preserve whether hypotheses preceded or followed inspection of the
results: promotion cannot make a post hoc finding confirmatory retrospectively.

## Gate: a selected, reviewable scope

Narrow when further runs no longer change the relevant design decisions and
targeted checks can address the remaining uncertainty. Null results and documented
limits are valid outcomes. Write `dev_docs/analysis-spec.md` or its equivalent with:

- **Inputs and derivations:** roles and scientifically consequential differences.
- **Selected analyses:** stable identities, entry points, resolved parameters,
  selected samples/features and exclusions, expected outputs, stochastic settings,
  components to retain, and remaining gaps.
- **Claims and deliverables:** the analyses supporting each claim, figure, table,
  or other result, including its scope, controls, diagnostics, and sensitivity
  analyses. Carry forward the applicable design safeguards from the plan and
  record consequential changes learned during exploration.
- **Validation criteria:** preserved baselines or alternative correctness evidence,
  relevant sensitivity results, comparison metrics, and justified tolerances.
  Establish criteria before examining validation differences.

Include applicable publication or release handoff criteria when that is the
deliverable; keep them with the existing spec rather than creating another plan.

Check both directions: every result has support and every selected analysis serves
a result or explicit checking need. Carry the working implementation and evidence
forward. The spec fixes reviewable scope, not an immutable conclusion; amend it
with reasons when evidence changes the design, reopening only affected readiness
decisions and preserving earlier scientific choices.
