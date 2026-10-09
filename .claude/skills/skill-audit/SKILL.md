---
name: skill-audit
description: >
  Audit this repo's skills, summaries, and manual for competing mandates,
  contradictions, unclear instructions, and descriptions that drift from skill
  bodies. Use before a release or after changing skill boundaries.
---

# Skill audit

Find places where the plugin's skills disagree with each other, or where what a skill says it does differs from what it instructs. Mechanical checks in `scripts/check.sh` catch missing names and broken links; this audit covers what only a reader can judge.

Before a release, the audit is required and leaves a report at `dev_docs/skill-audits/<version>.md`, where `<version>` is the version in `.claude-plugin/plugin.json`. `check.sh` fails a release version without a report, or with an open finding in it. After a change to skill boundaries, run it without writing a report, or write one for the upcoming version.

## Read with fresh eyes

Run the review in a fresh context, such as a subagent, that did not write the changes being audited. An author reads what they meant rather than what the text says.

Audit everything, not only the diff. Conflicts usually arise between new text and old text that did not change. Do read the diff since the last release so the changed areas get extra attention:

```bash
last=$(git describe --tags --abbrev=0 origin/main)
git diff "$last"..HEAD --stat -- skills docs README.md dev_docs
```

Read:

- every `skills/*/SKILL.md` and its `references/`;
- the skill summaries in `README.md`, `docs/plugin.md`, and `dev_docs/plugin-architecture.md`, including the ownership notes and the scenario table; and
- manual chapters that describe what a skill does (`grep -rln "dunnlab-" docs`).

## What to look for

1. **Competing mandates.** Two skills claim the same topic, or give instructions that cannot both be followed. Examples are two different files for the same purpose, two defaults for the same choice, or one skill requiring a step that another forbids. Build an ownership map as you read: for each topic, which skill says it owns it, and which skills defer to whom.
2. **Routing.** Every "X belongs to Y" or "use Y for X" points to a skill that actually covers X, and the two skills agree about the boundary.
3. **Description drift.** Each skill's `description` matches its body. Flag a description that promises something the body does not deliver, and a major responsibility of the body that the description omits. The description decides when the skill loads, so an omission means the skill is not used when it should be.
4. **Summary drift.** The summaries in the README, `docs/plugin.md`, and the architecture doc match what each skill now does.
5. **Manual drift.** Manual chapters that describe skill behavior agree with the skills.
6. **Scenarios.** For each row of the scenario table in `dev_docs/plugin-architecture.md`, the listed skills would in fact be chosen and would behave as the expected boundary describes.
7. **Clarity.** Instructions an agent new to the repo could not follow, undefined terms, or unclear strength, where it is not clear whether something is required or preferred.

Report specific locations and quote the conflicting text. Do not report matters of taste as findings.

## Report

Write `dev_docs/skill-audits/<version>.md`:

```markdown
# Skill audit <version>

Date: YYYY-MM-DD · Commit audited: <short sha> · Auditor: <model or person>

| # | Severity | Location | Finding | Resolution |
|---|---|---|---|---|
| 1 | blocking | skills/a/SKILL.md:12; skills/b/SKILL.md:40 | <what conflicts, quoted> | fixed in <sha> |
| 2 | minor | README.md:90 | <what drifted> | accepted by <person> YYYY-MM-DD: <reason> |
| 3 | minor | ... | ... | open |
```

- **Severity:** `blocking` when an agent following the skills would act wrongly or inconsistently; `minor` for drift or unclear wording that would not change behavior.
- **Resolution:** `open`, `fixed in <sha>`, or `accepted by <person> <date>: <reason>`.
- If there are no findings, say so in a single row.

Fix findings in separate commits and update their resolution. **Only a person can accept a finding without fixing it.** An agent leaves the row `open` and asks. The release proceeds when no row is open.
