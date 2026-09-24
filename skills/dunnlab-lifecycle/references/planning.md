# Phase 1: Planning

Turn a scientific question into feasible next actions. An actionable plan needs
no extra review cycle solely because this phase has a name. Extend
`dev_docs/overview.md` or its existing equivalent; use `dunnlab-new-project` only
for needed scaffolding and apply `dunnlab-workflow-design` from the start.

## Establish the scientific plan

- **Questions and deliverable.** State the question and target quantity or
  qualitative claim, how it relates to prior work, and the intended report,
  paper, release, or other output. Identify the contribution without presuming
  novelty or a positive result; retain key sources in the existing plan.
- **Inputs and access.** Identify datasets, source material, or simulations by
  stable versions, locations, or acquisition protocols. Distinguish available
  inputs from future collection and restricted or collaborator dependencies.
- **Candidate methods.** Connect proposed methods and assumptions to each
  question. Exploration may revise the choices.
- **Decision safeguards.** Identify independent sampling units, replication versus
  repeated measurement, paired or clustered observations, essential controls,
  uncertainty, and plausible confounding where relevant. When selecting or
  evaluating predictive models, prevent leakage between training, tuning, and
  evaluation data, respecting related samples and preprocessing. When testing
  multiple hypotheses or selecting among many comparisons, state how multiplicity
  and selection affect the claims. Preserve preregistered commitments and the
  distinction between exploratory choices and confirmatory tests. These are
  question-dependent safeguards, not a requirement to add statistical tests.
- **Constraints.** Record known compute and time budgets, access limits, and
  deadlines. Do not invent a budget or assume permission to exceed one.

When a publication or public release is intended, identify known access,
preservation, citation, and reporting requirements early enough to retain the
needed evidence. Use the [handoff guidance](publication.md) for those requirements;
an unspecified venue does not block useful analysis.

Keep provisional findings distinguishable from selected reported results using
the project's existing organization. Shared computation serves both. Computational
reproduction starts from preserved original inputs; it does not require repeating
the physical experiment or data collection campaign.

## Gate: an actionable plan

Each question has a candidate analysis and an interpretable possible result.
The next actions have identified inputs, accessible resources, and no unresolved
decision that blocks execution. Verify access or inspect a representative input
where feasible. Future dependencies remain explicit rather than silently blocking
independent work.

Record whether feasibility follows from an executed check or scientific judgment.
A plan alone does not demonstrate data access, and a successful file read does
not establish that the method answers the question. Resolve specific gaps; when
ready, continue authorized Exploration under the shared gate rules.
