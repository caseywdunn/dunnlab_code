# Phase 4: Validation

Assess whether the distilled analyses support the reported claims, whether changes since exploration altered results, and whether the deliverable matches the computed evidence. Successful execution and agreement with an earlier implementation are useful evidence, but neither alone establishes scientific correctness.

## Establish comparison criteria

Use the metrics and acceptance criteria recorded in the spec before examining validation differences. Choose criteria appropriate to the result: exact equality for deterministic counts or labels, justified numerical tolerances for estimates, distributional or uncertainty-based comparisons for stochastic outputs, and explicit assessment criteria for qualitative judgments. Compare uncertainty and scientific implications as well as point estimates where relevant.

If criteria are missing, record them and their rationale before comparing. If a criterion must change after inspecting results, disclose the change and why; do not loosen it merely to make a discrepancy pass.

## Compare with preserved evidence

For each claim, locate its exploratory baseline through `exploratory/findings.md` and verify the baseline's input versions, parameters, code, and outputs. Compare like with like, or identify deliberate differences before interpreting disagreement.

Resolve discrepancies in writing:

- **Exploration had an error or used superseded inputs.** Establish the correction with appropriate checks, revise the claim if needed, and preserve the original finding and the reason it changed.
- **Distillation introduced an error.** Reopen Distillation, fix the implementation, and rerun the affected analysis and checks.
- **Both results follow from defensible choices.** State the dependence, clarify the spec, and assess whether the claim needs qualification or additional validation.
- **The cause is unresolved.** Keep the required check open; do not select the preferred result by convenience.

Where no usable exploratory counterpart exists, identify alternative evidence in the spec: an independent implementation, an analytic result, a known-answer benchmark or controlled simulation, or an independent assessment against a documented protocol. A second execution of the same code is a reproducibility check, not an independent correctness check. Reusing exploratory components may preserve their errors, so retain domain-appropriate controls even when the baseline and distilled results agree.

The comparison criterion can pass with justified alternative evidence that meets the stated acceptance criteria. Merely noting that a baseline is missing is insufficient. If adequate evidence is unavailable, keep the gate open or explicitly revise the deliverable and claims so the unsupported result is no longer required.

## Robustness of the reported results

Target plausible failure modes of central claims. Build on early sensitivity checks rather than repeating them without cause:

- **Analytical choices.** Test defensible alternatives in preprocessing, modeling, measurement interpretation, or inference. Vary one factor at a time when useful for attribution; test combinations when interactions are plausible.
- **Inputs and sampling.** Examine dependence on relevant subsets, collection batches, missing-data assumptions, boundary conditions, or simulation settings while respecting the sampling structure.
- **Controls and uncertainty.** Check known controls and whether the reported uncertainty or agreement measures support the claimed interpretation.

Keep checks proportionate to the claims and authorized budget. Report changes, null findings, and limitations. Sensitivity may justify a narrower claim; it should not be tuned away. If a class of robustness checks is inapplicable, justify that judgment in the report.

Add new checks and their expected outputs to the spec before running them, following the reopening rules in `SKILL.md`. Preserve their run records and include reported sensitivity results in the same provenance system as primary analyses. A check that needs new implementation reopens Distillation; a changed scientific scope reopens Exploration.

## Verify reproducibility without redundant full runs

Require evidence for a full computational run from original preserved inputs in an isolated clean workspace with the environment reconstructed from its specification. Use public acquisition scripts or the documented access procedure for restricted inputs. Do not start from cached intermediates and call that a clean run.

Reuse Distillation's clean run and engineering checks when they cover the current source, spec, inputs, and environment. Record that identity match. After changes, rerun affected checks and establish clean execution evidence covering the final workflow; repeat the full expensive computation only when earlier evidence no longer covers it or an independent rerun is itself a validation requirement. Report actual coverage without describing a partial rerun as a fresh full run.

Regenerate audit manifests from selected preserved run records and verify artifact hashes. Investigate unexpected differences before replacing a baseline. Compare a new execution's scientific outputs using the defined criteria; expected changes in run IDs or timestamps are not scientific failures.

Verify model-free execution where no LLM dependency is declared. For documented on-path LLM steps, distinguish replay of preserved responses from a new invocation and report which was tested, how outputs were assessed, and what remains dependent on model availability or nondeterminism. Apply the same clarity to other external or human dependencies.

## Trace the deliverable to the analysis

Every result produced by this project and reported in the deliverable must trace to a selected distilled output or a documented interpretation of it:

- Reported numbers, units, uncertainty, tables, and figures agree with generated artifacts, allowing documented display rounding.
- Described methods and software versions match actual execution records.
- Figures and result summaries regenerate from preserved outputs using recorded code; separately document human interpretation or presentation steps.
- Controls, sensitivity results, exclusions, and post hoc choices are described where they affect interpretation.
- No reported computational result depends solely on an exploratory file that was never re-derived or explicitly validated.

Use a compact claim-to-output mapping when the spec does not already provide sufficient traceability. External literature claims should have citations rather than being forced into the project's output manifest.

Run `dunnlab-codereview` when available, focusing on consequential transformations and acquisition checks. Reuse still-valid engineering evidence and record scientific checks separately. Review alone does not substitute for comparison or execution.

## Gate: ready for the intended scientific deliverable

- [ ] Each reported claim has a baseline comparison or justified alternative evidence meeting the stated criteria; discrepancies are resolved.
- [ ] Central claims have appropriate robustness evidence and reported limitations, or a justified explanation of inapplicability.
- [ ] Clean execution and relevant engineering checks cover the final workflow, with evidence identities recorded.
- [ ] External, human, and model dependencies are verified to the stated level; reproducibility limits are explicit.
- [ ] Manifests agree with selected run records and preserved artifacts; new-run comparisons meet specified criteria.
- [ ] Reported results trace to the distilled analysis and accurately describe its methods and uncertainty.
- [ ] Relevant code review is complete.
- [ ] The README or release documentation states how to obtain inputs, rerun the analysis, and access preserved exploratory evidence, including any restrictions.

Record which checks ran, which valid evidence was reused, and which scientific judgments were made. Required unresolved checks keep the gate open. When all criteria pass, record `phase: validation` and `gate_status: passed`; do not publish, submit, or remove exploratory evidence unless the user has authorized that action.
