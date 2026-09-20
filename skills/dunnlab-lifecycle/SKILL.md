---
name: dunnlab-lifecycle
description: >
  Four-phase lifecycle for research analyses — Planning, Exploration,
  Distillation, Validation — with agent-checkable gates between phases.
  Use when starting a research project, when exploratory analyses have
  sprawled and need to be distilled into a publication-ready set, when
  preparing analyses for a manuscript or public repo, or when asked about
  matrix naming, command templates, analysis manifests, or which phase a
  project is in.
---

# Dunn Lab Analysis Lifecycle

A research project moves through four phases. Each ends at a gate you can check by running something, not by eyeballing it.

| Phase | Produces | Gate |
|---|---|---|
| 1. Planning | Questions, datasets, candidate methods | A plan specific enough to implement without further input |
| 2. Exploration | Preliminary results that shape the design | A written spec fixing the final analysis scope |
| 3. Distillation | The analyses behind the figures, tables, and reported numbers | Runs end to end from raw data with no LLM on the data path |
| 4. Validation | Evidence the distilled results are right | Distilled agrees with exploratory; everything reruns clean |

The phases exist because exploration and publication want opposite things. Exploration should be fast, branching, and disposable — you are buying information about what to do next. Publication needs a small, consistent, auditable set that a human can check without an agent interpreting it for them. Trying to get both from one pile of analyses is what produces dozens of near-identical matrices and a methods section nobody can verify.

**Distillation is a rewrite, not a cleanup.** This is the part people get wrong. See `references/distillation.md`.

## Where am I?

Read `dev_docs/lifecycle.yaml`. If it does not exist, this project has not been through this skill:

1. Infer the phase from the repo — no committed plan means Planning; a plan but no spec means Exploration; a spec but no passing distilled run means Distillation.
2. Tell the user what you inferred and let them correct it. Projects arrive mid-flight and the inference is a guess.
3. Write the file.

```yaml
# Dunn Lab analysis lifecycle — updated by the dunnlab-lifecycle skill
updated: 2026-09-19
phase: exploration        # planning | exploration | distillation | validation
gate_status: open         # open | passed
artifacts:
  plan: dev_docs/overview.md
  spec: null              # set when the exploration gate passes
notes: "18S+28S siphonophore phylogeny; awaiting Nematocyst dataset"
```

Commit this file. It tracks *where you are*; the scientific record lives in the plan, the spec, and the generated manifests. It sits in `dev_docs/` rather than a harness directory like `.claude/` for two reasons: a reader auditing the repo should be able to see when the analysis was declared final, and the skill has to work under any harness that reads `SKILL.md`.

Projects run for months across many sessions with the context cleared between them, so re-read this file whenever you resume rather than trusting conversation context.

## Working a phase

Read the reference for the current phase and follow it. Do not load the others — they describe different, partly contradictory ways of working, and an agent holding all four tends to average them into something that is exploratory and slow at the same time.

- `references/planning.md`
- `references/exploration.md`
- `references/distillation.md`
- `references/validation.md`

## Gates

A gate is a decision rule you evaluate, not an appointment for the user to inspect your work. Evaluate it, report the evidence, and act:

- **Passes** — record `gate_status: passed`, tell the user what you checked, and ask before entering the next phase. Phase transitions are consequential and often expensive; the check is yours to make, the decision to proceed is theirs.
- **Fails** — say which criterion failed and what evidence you have, then keep working the current phase. A failed gate is normal and is not a reason to stop and ask.
- **Cannot be evaluated** — that is itself a finding. Usually it means the phase's output is underspecified. Say so rather than substituting a judgment call for the check.

Never advance a phase silently. The whole value of the structure is that someone can later ask "when did this become final, and what was checked?" and get an answer.

## Relationship to other skills

This skill sequences work; it does not restate conventions that live elsewhere. Apply alongside:

- **`dunnlab-new-project`** — owns scaffolding and the build loop. See the boundary below; getting it wrong is the most likely way these two skills work against each other.
- **`dunnlab-defaults`** — coding standards, project structure, Snakemake orchestration, the `analyses_*/` layout.
- **`dunnlab-bioinformatics`** — immutable raw data, input validation, summary tables, gene ID conventions.
- **`dunnlab-codereview`** — run its checklist during Validation instead of inventing a second one.
- **`dunnlab-biblio`** — methods and reference formatting when writing up.

### The boundary with `dunnlab-new-project`

That skill is two things joined together, and only one of them is yours to drive:

| Its stages | Who owns it |
|---|---|
| Stages 1–3, 6–7 — git, permissions, devcontainer, directory layout, environment | `dunnlab-new-project`. Universal scaffolding; do not reimplement or second-guess it. |
| Stages 4–5 — planning documents | Shared. It writes `dev_docs/overview.md`; Planning here fills it with the questions, datasets, and candidate methods that the gate checks. One document, not two. |
| Stage 8 — the build loop | Depends on the phase. |
| Stage 9 — final verification | Engineering checks. Distillation's gate reuses its checklist; Validation adds the scientific layer on top. |

Stage 8 is where these two skills most easily fight. It drives a disciplined incremental build — atomic tasks, tests and docs per task, commit and clear between. That is right for a tool or package, and right for building the distilled pipeline in Phase 3. It is wrong for Exploration, which needs to be fast and disposable and will be actively slowed by it. When a research project reaches Stage 8, hand off to Exploration here and come back to that discipline at Distillation.

Two state files coexist and do not conflict because they work at different scales: `dev_docs/lifecycle.yaml` records which phase the project is in, and `.agent/new-project-progress.yaml` is a within-stage task checklist. Keep it that way — if this file starts tracking tasks, they will drift apart.

### Directory layout

`exploratory/` and `analyses/` are the lifecycle's split. Inside them, the existing conventions still apply: `dunnlab-defaults` for per-analysis subdirectories when a project has several, `dunnlab-bioinformatics` for `data/raw/`, `data/processed/`, and the rest. This skill decides *which side of the line* work goes on, not how it is organized once there.

### One inherited conflict

`dunnlab-defaults` suggests ISO date prefixes on data files when versioning matters. That is right for exploration and wrong for distilled outputs, where the filename encodes identity rather than history. `references/distillation.md` explains why.

## The data path

Throughout, track whether an LLM sits *on* the data path — whether reproducing a reported result requires invoking a model — or *off* it, having produced durable code that does. The operational test: can the published analysis be rerun from inputs to results without calling an LLM?

Exploration may freely put AI on the data path; that is part of what makes it fast. Distillation must take it off wherever the same job can be done by committed code. See `docs/using-ai.md` in the dunnlab_code repo and Dunn, Schultz & Musser (2026), *Designing reproducible large-language-model-assisted scientific analyses*, <https://doi.org/10.1016/j.patter.2026.101644>.
