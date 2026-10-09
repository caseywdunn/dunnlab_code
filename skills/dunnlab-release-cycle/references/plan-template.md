# `dev_docs/PLAN.md` template

Copy the skeleton and replace the placeholders. Keep it short enough to read in a few minutes: one line of goal, one line per step, and gate criteria precise enough to check. Link to evidence rather than pasting it.

```markdown
# Plan

**Current release:** vX.Y.Z — <one-sentence goal>
**Status:** active | paused <date>: <reason>; resume at step <n>

## vX.Y.Z — <goal>

After this release, users can <what they can do that they cannot now>.

### Steps

1. [#12](https://github.com/OWNER/REPO/issues/12) <title>
   - Gate (agent): `pytest tests/test_parser.py` passes, and `scripts/check_counts.py data/fixture.fa` reports 1,204 records.
   - Status: met 2026-10-07 ([PR #31](https://github.com/OWNER/REPO/pull/31))
2. [#15](https://github.com/OWNER/REPO/issues/15) <title>. Depends on 1.
   - Gate (agent): runtime on `tests/data/large.fa` under 60 s on 4 CPUs, recorded in the PR.
   - Status: not met
3. [#18](https://github.com/OWNER/REPO/issues/18) <title>. Depends on 2.
   - Gate (human): <person> reviews the revised output format before it is documented.
   - Status: not met

### Release gate

- (agent) `scripts/release-check` passes on `dev`. Status: not met
- (human) <person> approves the release. Status: not met

## Later releases

- vX.(Y+1).0 — <goal>: #20, #22
- Unscheduled: #25

## Out of scope

- <what this project will not do, and why, in one line each>

## Standing gates

Criteria every release must meet, for example a known-answer test or a clean rebuild that matches the incremental one. Omit this section if there are none.
```

## Rules for keeping it useful

- Steps reference issues; the issue holds the discussion and the PR holds the evidence.
- A gate's criterion is fixed once work on the step starts. Changing it is a human decision recorded in the plan.
- Statuses are `not met`, `met <date>` with an evidence link, or `waived by <person> <date>: <reason>`.
- At release, delete the finished release's section and promote the next. The changelog and Git history are the record of what was done.
- Do not add evidence logs, dated narratives, or implementation notes. If a step needs a design note, put it in `dev_docs/` and link it.
