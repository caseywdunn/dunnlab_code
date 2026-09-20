# Phase 1: Planning

Turn a high-level idea into a plan specific enough that the work can proceed without stopping to ask what was meant.

Planning is a loop. It usually starts with a sentence or two and iterates until the detail is there. Do not try to finish it in one pass, and do not pad it with detail nobody needs — the target is *actionable*, not *complete*.

## Scaffolding

If the repo is empty or unstructured, run the `dunnlab-new-project` skill for setup: git, permissions, devcontainer, directory structure, environment, `README.md`, project instructions, `dev_docs/`. Do not reimplement any of it here.

That skill will also draft `dev_docs/overview.md`. Extend that file with what follows rather than creating a second planning document — two documents describing the same project is how they start contradicting each other, and a reader will not know which one is current.

Put the project instructions in `AGENTS.md` and make `CLAUDE.md` a one-line `@AGENTS.md` import, so both harnesses read the same file rather than two copies that drift.

Beyond its standard layout, a lifecycle project needs two directories from the start:

```
exploratory/     # Phase 2 lives here. Never cited by the paper.
analyses/        # Phase 3 lives here. Everything the paper cites.
```

Creating both up front matters more than it looks. When only one analysis directory exists, exploratory work accretes in it and the boundary has to be reconstructed later under deadline — which is the situation this skill exists to prevent.

## What the plan has to contain

These go in `dev_docs/overview.md`, committed.

**Questions.** What is actually being asked, stated so that a result could answer it. "Characterize the phylogeny" is not a question. "Is Family X monophyletic with respect to Y?" is.

**Resources.** Every dataset named concretely enough to fetch: accessions, repository URLs, paths on a cluster, or the person who holds it. For private or embargoed data, note the restriction — it changes what can go in a public repo later.

**Candidate methods.** What you would run, at the level of named tools. Not a committed design; Exploration exists to revise it.

**Known constraints.** Compute budget, embargoes, collaborator dependencies, deadlines.

## Gate: an actionable plan

Check by attempting the work, not by reading the document:

- Can you state the first three concrete things you would run, with inputs, and no unresolved "depends on what they meant"?
- Is every dataset either in hand or fetchable by a script you could write today?
- Does each question map to at least one candidate analysis?

If yes, the gate passes. Record it, tell the user what you checked, and ask before moving to Exploration.

If not, the loop continues — ask about the specific gap rather than asking the user to review the plan generally. "Which reference genome?" gets an answer; "does this plan look right?" gets a shrug.

Raise problems with the plan itself here, while it is cheap: inappropriate tools, data that cannot answer the question asked, a missing control, an approach with a better alternative. This is the last phase where saying so costs nothing.
