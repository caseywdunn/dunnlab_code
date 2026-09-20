# Phase 2: Exploration

Learn what the inputs support and which analyses are worth developing. Run something, inspect it, and let the finding change the design. Spend compute and context where they can change a scientific decision, while keeping the path to a durable analysis short.

## Explore with distillation in mind

Reduce the work needed to retain a successful analysis. Use lightweight conventions that prevent inconsistencies without committing to a design prematurely:

- Give inputs and runs clear identities, record consequential parameters, and preserve the outputs behind findings. Reuse a derivative when its provenance and assumptions match the new question.
- Put transformations in rerunnable scripts, functions, or notebooks executable from a clean kernel. Keep key parameters easy to locate; a small configuration or explicit function arguments are enough.
- Reuse sound transformations and existing project tools across investigations. Extract shared code when actual reuse warrants it, rather than copying and allowing versions to diverge.
- Keep exploratory choices and run-specific settings separate from reusable computation. A retained analysis should be expressible by selecting inputs and parameters, with as little rewriting as practical.
- As an approach stabilizes, improve the specific pieces likely to survive. Defer speculative abstractions, generalized interfaces, and exhaustive hardening of branches likely to be discarded.

The phase boundary separates provisional findings from verified reported results; it need not separate two implementations of the same method. Distillation can promote verified components and add the missing evidence. It should not require reconstructing what an exploratory script did or rewriting sound code merely because it originated here.

## Breadth before depth

Start with the cheapest informative comparison for each distinct question before investing heavily in one direction. Avoid an automatic sweep of every method, preprocessing choice, and data subset. State the decision a proposed set of runs will inform.

This is a default, not a one-run limit. Add replication when variability obscures the answer, test interactions when choices may matter jointly, and use a structured design when the question warrants one. Failure to detect a change in one comparison does not establish that a parameter never matters. Record the conditions under which it appeared unimportant.

Use early sensitivity checks when they affect whether to pursue a result or whether the method is credible. Defer extensive robustness testing until the central claims are settled. Validation checks the claims that survive; it should not be the first opportunity to notice an obvious dependence on an arbitrary choice.

## Spend the least that answers the question

- **Subsample** when a smaller input preserves the relevant groups, dependencies, or rare features.
- **Use cheaper settings** to assess feasibility, then confirm findings at appropriate precision and scale.
- **Reduce scope** to a representative part of the data or a shorter simulation when that answers the immediate question.

A cheap null result may reflect limited information or approximation error. Before retiring a direction, assess whether the reduced run could have detected the effect or failure of interest. Escalate or record the result as inconclusive when it could not.

State a budget per question within the user's authorized resources. At the limit, summarize what was learned and reassess; do not automatically continue spending. Set a stopping criterion where possible, such as a resolved design choice or evidence that the method cannot answer the question.

### Context is a budget too

- Extract relevant statistics or examples with a small reusable script; avoid loading entire large datasets or logs into context.
- Compare runs with compact summaries, including exceptions that could change the conclusion.
- Keep the active question focused and record a durable handoff before a session or context change. Do not require a context reset after every question.
- Store findings and evidence pointers in `exploratory/findings.md`, rather than relying on the conversation transcript.

## Keep checks that protect scientific decisions

Check required inputs, expected dimensions and units, sensible ranges, appropriate handling of missing values, valid joins and identifiers, and successful completion of external commands. Add a focused known-answer check when an uncertain transformation could change the conclusion. Apply checks relevant to the data; unique identifiers, for example, may be required for a join key but not for repeated observations.

One-off scripts, notebooks, and provisional names are acceptable. Improve naming or structure when the small effort saves repeated interpretation or prevents errors; do not polish every abandoned branch. Keep original inputs immutable. Preserve model-assisted transformations and outputs when code cannot express them. Exploratory code may be disposable; the evidence behind scientific decisions is not.

## Record what you learn

Keep one short findings entry per meaningful decision or result, including negative, null, and inconclusive results:

- The question, finding, limitations, and resulting decision.
- Pointers to the script or notebook, resolved parameters, relevant software or model versions, and seed if used.
- Input identities or versions and the actual output used to reach the conclusion.

Preserve a recoverable snapshot of the inputs, code, and outputs for findings that motivate reported claims. A pointer to a mutable file alone is insufficient. Large or restricted artifacts may live in an appropriate archive with persistent identifiers and checksums rather than in git. Reuse the project's existing run records when they already capture this evidence; do not maintain a duplicate provenance system.

Preserve the distinction between hypotheses formed after inspecting results and tests specified beforehand. Distillation improves the implementation and its evidence; it does not make an exploratory finding confirmatory retroactively.

## Narrowing

Narrow when further runs no longer change the relevant design decisions and remaining uncertainty can be addressed by targeted checks. Confirm that the chosen approach behaves appropriately at the intended scale before fixing the scope. A useful outcome may be a null result or a documented limit on what can be concluded.

Identify which components can be retained, which need small changes, and which must be replaced. Carry the working implementation and its evidence forward with the spec so Distillation starts from verified understanding, not reconstruction.

## Gate: the analysis scope is specified

Write `dev_docs/analysis-spec.md` or the project's equivalent. Include:

- **Inputs and derivations.** Identify inputs and necessary derivatives, their roles, and scientifically consequential differences. Do not require a particular data representation.
- **Analyses.** Give stable analysis IDs, entry points or command templates, resolved parameters, expected outputs, and relevant stochastic settings. Identify existing components to retain and the gaps to close during Distillation.
- **Claims and deliverables.** Link each intended claim, figure, table, or other result to its supporting analyses. Include controls and diagnostics with an explicit purpose even if they do not produce a headline claim.
- **Validation plan.** Identify exploratory baselines or alternative evidence, comparison metrics and tolerances with rationale, and targeted robustness checks. Specify these before examining validation differences. Record uncertainty where a criterion still needs scientific input.

Check the mapping in both directions: every planned result has an analysis, and every analysis serves a result, control, diagnostic, or validation need. Required inputs and parameters are identified, and validation criteria are usable. Save the spec and evidence through the project's version-control workflow and apply the shared gate rules.

The spec fixes a reviewable scope, not an immutable conclusion. Amend it deliberately when evidence changes the design, documenting the reason and reopening affected gates. New validation checks need a spec entry before execution; they are not a reason to resume an unlimited exploration sweep.
