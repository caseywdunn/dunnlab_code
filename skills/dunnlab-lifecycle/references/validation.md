# Phase 4: Validation

Distillation showed the analyses run. Validation checks they are *right* — that rebuilding from the spec did not quietly change a result, and that what the manuscript says matches what was computed.

The risk this phase addresses is specific. Distillation rewrote the analyses, so every reported number now comes from code that has never been compared against anything. A rebuild that runs cleanly and produces subtly different answers is the expected failure, not an unlikely one.

## Check distilled results against exploratory ones

For each claim in the paper, find the exploratory result that originally motivated it — `exploratory/findings.md` should point at it — and compare it to the distilled result.

Agreement is reassuring. Disagreement is the point of the exercise, and it has to be resolved rather than noted:

- **The distilled version is correct.** Exploration had a bug, or used data superseded since. Record this — it may change what the paper claims.
- **The exploratory version is correct.** Distillation introduced an error. Fix it and rerun.
- **Both are defensible.** Usually a parameter or matrix differs in a way the spec did not pin down. Pin it down, then rerun.

What is not acceptable is discovering the discrepancy and moving on because the distilled number is the one in the manuscript. The comparison only has value if it can change something.

Where a distilled analysis has no exploratory counterpart, say so explicitly. It means a reported result has never been computed a second way, which is worth the reader's — and the user's — attention.

## Rerun everything from clean

- **Full workflow from a fresh clone**, with the environment built from its specification, starting from raw data fetched by the acquisition scripts. Not from cached intermediates.
- **The test suite**, including known-answer cases.
- **The rerun-without-LLM test.** Run the workflow with no model available. If it completes, AI is off the data path. If it fails, either that step needs to become code or it is a documented on-path step — there is no third option.
- **Regenerate the manifests** and diff against the committed `matrices.tsv` and `analyses.tsv`. A difference means the tables and the runs have diverged, which is exactly the failure the generated-manifest design exists to catch. Investigate it rather than committing the new version.

## Check the manuscript against the manifests

Every number, table, and figure in the manuscript should trace to a distilled output:

- Matrix statistics quoted in the text match `matrices.tsv` — taxa, sites, occupancy.
- The methods command template, populated with each row of `analyses.tsv`, is the command that actually ran.
- Tool versions in the methods match what the run captured.
- Every figure regenerates from committed outputs.
- Nothing cited traces back to `exploratory/`.

That last one is worth checking directly rather than assuming. A number carried into the manuscript during exploration and never re-derived is easy to miss and is the kind of error that survives to print.

## Code review

Distillation already ran the engineering checks — environment builds, tests pass, README accurate (`dunnlab-new-project` Stage 9). Do not repeat them here; this phase is about whether the science is right, which no amount of green tests establishes.

Run the `dunnlab-codereview` checklist over `analyses/`. Pay particular attention to the acquisition and validation scripts — they run first, are tested least, and a silent failure there propagates through everything downstream.

## Gate: ready for publication

- [ ] Every claim compared against its exploratory counterpart, with discrepancies resolved in writing
- [ ] Full workflow reruns from a fresh clone and raw data
- [ ] Tests pass
- [ ] Rerun-without-LLM completes, or on-path steps are documented and verified
- [ ] Manifests regenerate identically to what is committed
- [ ] Every manuscript number traces to a distilled output
- [ ] Code review complete
- [ ] `exploratory/` is either included as-is or removed deliberately, and the README says which

Report what you ran and what it showed. If something could not be checked — a step needing cluster time nobody has, a comparison with no exploratory counterpart — name it. An honest gap is useful; a quietly skipped check is the thing that makes the whole structure worthless.
