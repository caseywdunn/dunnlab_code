# Phase 2: Exploration

Find out what the data support and what the paper should claim. You are buying information about what to do next, and the cost of a wrong turn is low. Work fast.

Exploration is a loop: run something, look at it, let it change the design. New datasets and new methods appear here in response to what earlier results showed. That is the phase working, not a failure of planning.

## What is allowed here

Nearly everything. Specifically:

- **AI on the data path is fine.** Have a model classify records, reconcile messy metadata, or interpret a plot. Exploration is not reproducing anything; it is deciding what is worth reproducing.
- **Inconsistent naming is fine.** So are dated files, v2 files, one-off scripts, notebooks, and analyses you never look at again.
- **Dead ends are fine and worth keeping.** An approach that failed is information, and it is often what a reviewer asks about.

All of it lives in `exploratory/`, and none of it is ever cited by the paper. That constraint is what makes the freedom safe: because nothing here has to be defensible, nothing here has to be tidy.

## What still applies

Two rules survive into exploration because violating them is unrecoverable rather than untidy:

- **Raw data is immutable.** Transformations write new files elsewhere. A script that modifies `data/raw/` is a bug regardless of what it was asked to do.
- **Prefer a script to a direct transformation.** Even a throwaway reshaping should be a file you can re-run, because six months from now you will need to know what it did. A model editing a table in place leaves no such record.

## Keep a running note of what is working

Maintain `exploratory/findings.md` as you go — one short entry per result that changed your thinking, with a pointer to the analysis that produced it.

This is not bookkeeping for its own sake. Distillation needs to know which results the paper depends on, and reconstructing that from a directory of eighty analyses months later is exactly the expensive, error-prone task the lifecycle is meant to avoid. Validation later checks distilled results against these entries, so a finding recorded here with its number is worth far more than a vague memory of it.

## Gate: the scope is final

Exploration ends when you can write the spec — a complete list of what the paper will contain. Write it to `dev_docs/analysis-spec.md` and commit it.

The spec fixes:

- **The matrix set.** Every matrix the paper uses, with its short name and one-clause description. Nothing else gets built.
- **The analysis set.** Every analysis, as a command template plus the values filling it.
- **The claim each analysis supports.** A figure, a table, or a specific sentence in the results.

Check the gate by working backwards: take each claim the paper intends to make and find the spec'd analysis that supports it. Then take each spec'd analysis and find the claim it serves. Anything unmatched in either direction means the scope is not final — either a claim has no support, or an analysis is being carried along because it exists rather than because it is needed.

The second direction is the one people skip, and it is where the sprawl comes from.

Resist the pull to keep exploring. There is always another variant worth trying, and the spec can be amended if something genuinely changes — but amending it is a deliberate act with a commit attached, not a drift.
