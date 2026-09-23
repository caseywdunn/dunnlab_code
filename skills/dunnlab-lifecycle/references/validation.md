# Phase 4: Validation

Assess whether the distilled analyses support the reported claims, whether changes since exploration altered results, and whether the deliverable matches the computed evidence. Successful execution and agreement with an earlier implementation are useful evidence, but neither alone establishes scientific correctness.

## Scope: assess what is present

Validation evaluates the existing analysis set, its evidence, and its reporting. Rerunning the same specified analysis, checking calculations, inspecting provenance, comparing outputs, and running correctness tests are within scope. Small verification scripts may check specified behavior or summarize existing evidence; they must not introduce a new scientific analysis.

Designing or running a new sensitivity analysis is outside this phase. Changing a model, exclusion threshold, data subset, or other scientific choice to investigate its effect belongs in Exploration, with selected analyses carried through Distillation. Validation may assess existing sensitivity results and rerun their specified implementation for reproducibility.

Record deficiencies in the gate report and route the work before attempting to fill them:

| Finding | Return to |
|---|---|
| Missing sensitivity evidence requiring investigation, unresolved methodological choices, or insufficient scientific support for a claim | Exploration to settle the scientific question and revise the spec or claims, then Distillation for the selected analysis set |
| Implementation error, missing output from an already specified analysis, provenance gap, or failure to reproduce the specified analysis | Distillation to repair or complete the implementation and evidence |
| Reporting error where the existing evidence already establishes the correction | Correct the report and recheck traceability within Validation; reopen Exploration if the scientific interpretation must change |

Keep the validation gate open, preserve the finding, and update lifecycle state when returning to an earlier phase. After the affected earlier gates pass, resume Validation and reassess the corrected analysis set. Continue independent assessment work where useful, but do not expand the scientific scope under the label of validation. Follow the shared authorization rules for all additional work.

## Apply the comparison criteria

Use the metrics and acceptance criteria recorded in the spec before examining validation differences. Assess whether they are appropriate to the result: exact equality for deterministic counts or labels, justified numerical tolerances for estimates, distributional or uncertainty-based comparisons for stochastic outputs, and explicit assessment criteria for qualitative judgments. Compare uncertainty and scientific implications as well as point estimates where relevant.

If required criteria are missing or need a new scientific judgment, record the gap and return to Exploration to establish them before comparing. If a criterion must change after inspecting results, preserve the failed assessment and document the reason in the revised spec; do not loosen it merely to make a discrepancy pass.

## Compare with preserved evidence

For each claim, locate its exploratory baseline through `exploratory/findings.md` and verify the baseline's input versions, parameters, code, and outputs. Compare like with like, or identify deliberate differences before interpreting disagreement.

Resolve discrepancies in writing:

- **Exploration had an error or used superseded inputs.** Document the explanation supported by existing evidence and preserve the original finding. If further investigation or a scientific revision is needed, reopen Exploration; if the specified implementation needs repair, reopen Distillation.
- **Distillation introduced an error.** Reopen Distillation, fix the implementation, and rerun the affected analysis and checks.
- **Both results follow from defensible choices.** Record the dependence and assess whether the current spec and claim already account for it. Reopen Exploration if the choice or scientific interpretation remains unsettled.
- **The cause is unresolved.** Keep the required check open and route the investigation to Exploration or Distillation according to the deficiency; do not select the preferred result by convenience.

Where no usable exploratory counterpart exists, assess the alternative evidence already identified and available: an independent implementation, an analytic result, a known-answer benchmark or controlled simulation, or an independent assessment against a documented protocol. If that evidence must be newly designed or produced, record the gap and return to the appropriate earlier phase. A second execution of the same code is a reproducibility check, not an independent correctness check. Reusing exploratory components may preserve their errors, so assess the available domain-appropriate controls even when the baseline and distilled results agree.

The comparison criterion can pass with justified existing alternative evidence that meets the stated acceptance criteria. Merely noting that a baseline is missing is insufficient. If adequate evidence is unavailable, keep the gate open and return to Exploration to address the gap or revise the scientific claims; do not waive the requirement within Validation.

## Assess existing robustness evidence

Assess whether the sensitivity analyses and controls already present address plausible failure modes of central claims:

- **Coverage.** Do the existing analyses address the consequential methodological choices, input dependencies, and plausible interactions? Are omissions justified for these claims?
- **Results.** What changed under the alternatives already examined, and are null findings, instability, and limitations reported accurately?
- **Controls and uncertainty.** Do the existing controls and uncertainty or agreement measures support the claimed interpretation?

Judge sufficiency in proportion to the claims. An inapplicable class of sensitivity analyses needs a rationale, not an automatic extra run. Missing or inadequate evidence is a validation finding: specify the unsupported claim and the unresolved issue, then reopen Exploration for the scientific investigation. If the necessary analysis is already specified and only its implementation or output is missing, reopen Distillation. Do not add analyses to the spec or run new variants while remaining in Validation.

## Verify reproducibility without redundant full runs

Require evidence for a full computational run from original preserved inputs in an isolated clean workspace with the environment reconstructed from its specification. Use public acquisition scripts or the documented access procedure for restricted inputs. Do not start from cached intermediates and call that a clean run.

Reuse Distillation's clean run and engineering checks when they cover the current source, spec, inputs, and environment. Record that identity match. Rerunning the unchanged workflow for reproducibility remains in scope. If verification exposes a required implementation change, reopen Distillation before making it; after returning to Validation, reassess the repaired workflow and its updated execution evidence. Repeat the full expensive computation only when earlier evidence no longer covers it or an independent rerun is itself a validation requirement. Report actual coverage without describing a partial rerun as a fresh full run.

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

Check human auditability by reading the workflow rules: can a reviewer see which analyses run, with which scientific options, on which inputs, and how outputs feed subsequent steps? Flag external tool calls buried in command builders or validation wrappers, and validation overhead that obscures the computation. Assess checks against concrete scientific or operational needs, assuming trusted project inputs. Record unnecessary complexity as a maintainability finding; route any implementation refactor through Distillation without automatically repeating expensive analyses whose scientific execution is unchanged.

Run `dunnlab-codereview` when available, focusing on consequential transformations and acquisition checks. Reuse still-valid engineering evidence and record scientific checks separately. Review alone does not substitute for comparison or execution.

## Gate: ready for the intended scientific deliverable

- [ ] Each reported claim has a baseline comparison or justified alternative evidence meeting the stated criteria; discrepancies are resolved.
- [ ] Existing sensitivity analyses and controls adequately support central claims, with reported limitations or a justified explanation of inapplicability; gaps requiring earlier-phase work have been resolved and reassessed.
- [ ] Clean execution and relevant engineering checks cover the final workflow, with evidence identities recorded.
- [ ] External, human, and model dependencies are verified to the stated level; reproducibility limits are explicit.
- [ ] Manifests agree with selected run records and preserved artifacts; new-run comparisons meet specified criteria.
- [ ] Reported results trace to the distilled analysis and accurately describe its methods and uncertainty.
- [ ] Relevant code review is complete.
- [ ] The README or release documentation states how to obtain inputs, rerun the analysis, and access preserved exploratory evidence, including any restrictions.

Record which checks ran, which valid evidence was reused, and which scientific judgments were made. Required unresolved checks keep the gate open. When all criteria pass, record `phase: validation` and `gate_status: passed`; do not publish, submit, or remove exploratory evidence unless the user has authorized that action.
