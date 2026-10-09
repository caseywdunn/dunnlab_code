---
name: dunnlab-release-cycle
description: >
  Run a project on a release cycle: dev and issue branches, GitHub issues,
  dev_docs/PLAN.md with gates, CHANGELOG, and the release ritual. Use when setting
  up releases, working through a planned release, or cutting one.
---

# Dunn Lab Release Cycle

This skill governs how changes reach a project's users. Scientific questions and readiness belong to `dunnlab-research-lifecycle`, and coding, lint, and test conventions to `dunnlab-coding-defaults`. A research project that ships a tool can use both: its scientific plan stays in `dev_docs/overview.md` and its release plan in `dev_docs/PLAN.md`.

## Choose the mode

**Simple projects work directly on `main`.** A solo or exploratory project that no one else depends on does not need this cycle.

**Use the release cycle** when any of these hold:

- more than one person contributes;
- others rely on the code working while it changes;
- the project is a distributed tool or package; or
- an agent will work unattended for long stretches.

To move an existing project onto the cycle, follow [Setting up the release cycle](references/setup.md). Do not impose the cycle on a project that has not adopted it; ask first.

## Branches

| Branch | Holds | Changes by |
|---|---|---|
| `main` | Released versions only; every commit on it is a tagged release or a hotfix | Merge from `dev` at release, or a hotfix PR |
| `dev` | Work queued for the next release | PRs from issue branches |
| `issue-<N>-<slug>` | One issue's work, branched from current `dev` | Commits |

- **Never commit or push to `main` outside the release ritual.** Use rulesets to enforce this; see [setup](references/setup.md#protect-the-branches).
- All work reaches `main` through `dev`, including release preparation. Do not release from a side branch.
- An urgent fix to a released version branches from `main` as `hotfix-<slug>`, is released as a patch, and is merged back into `dev` immediately. See [the release ritual](references/release.md#hotfixes).
- Keep a `v<major>` maintenance branch only while an older major version is supported.
- Delete issue branches once merged.

## Issues

Every piece of work is a GitHub issue. Its branch and PR name it (`Refs #N`), and its changelog entry cites it.

An issue closes when its fix lands on `dev`. Close it with a comment naming the merge commit and the evidence that it works. `Closes #N` does not do this automatically, because GitHub closes issues only on merges into the default branch, which stays `main`.

When work turns up something new, open an issue for it. Add it to the plan only if it belongs in the current release; otherwise list it under the plan's later releases. Do not expand the current release silently.

## The plan: `dev_docs/PLAN.md`

`PLAN.md` is the only plan for releases. It does not duplicate GitHub milestones or a separate roadmap. Use [the plan template](references/plan-template.md). It holds:

- the current release: version, a one-sentence goal, and its status;
- that release's issues in order, with dependencies;
- a gate on each step and a release gate; and
- brief lists of later releases and out-of-scope work.

The plan is forward-looking and short. Evidence goes in issue comments, PRs, or results files that the plan links to, not in the plan itself. At each release, remove the completed release and promote the next. Code and code comments do not cite `PLAN.md`, because its contents change every release.

### Gates

Each step's gate is a criterion stated before the work starts, and it is one of two kinds:

- **Agent-checkable:** objective and executable, such as a command that exits successfully, a test that passes, or a threshold that is met. An agent evaluates it and proceeds.
- **Human review:** a judgement such as scientific interpretation, interface design, or release approval. An agent stops and asks.

Every gate carries a status line: `not met`, `met <date>` with a link to the evidence, or `waived by <person> <date>` with the reason. **Only a person can waive a gate.** An agent never edits a gate's criterion to make it pass. If a criterion turns out to be wrong, stop and propose the change.

## Changelog

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Each PR into `dev` adds its entry under `## [Unreleased]` in the same change, so release notes are never reconstructed at release time. Write entries for users, as in the README guidance in `dunnlab-coding-defaults`: what changed for them, citing the issue. Keep entries brief; implementation detail belongs in the PR.

## Versions

Use [semantic versioning](https://semver.org/). Keep the version in one place, with any other copies derived from it or checked against it. Between releases, `dev` carries the next version with a development marker: `X.Y.Z-dev` for Cargo, `X.Y.Z.dev0` for Python, and `X.Y.Z.9000` for R packages.

## Working autonomously

An agent working through a release repeats this loop:

1. Read `AGENTS.md` and `dev_docs/PLAN.md`. Pick the first step whose dependencies are done and whose gate is not met.
2. Branch `issue-<N>-<slug>` from an up-to-date `dev`.
3. Implement the change with tests, following `dunnlab-coding-defaults`. Run format, lint, and test checks.
4. Add the changelog entry, and open a PR into `dev` (`gh pr create --base dev`).
5. Evaluate the step's gate on the branch, put the evidence in the PR, and record the gate's status in `PLAN.md` on the same branch, linking the PR. Push, and wait for CI (`gh pr checks --watch`).
6. When CI passes, merge with a merge commit (`gh pr merge --merge --delete-branch`). Close the issue with a comment naming the commit and the evidence.
7. Continue to the next step.

A gate that can only be evaluated after merging, such as a full rebuild on `dev`, is recorded through a small follow-up PR. Plan updates reach `dev` through PRs like any other change.

Stop and report when:

- the next gate requires human review;
- a check fails and the cause is not resolvable within the issue's scope;
- the work raises a scope or design question that the plan does not settle; or
- the release itself is next. A person approves every release.

An agent never:

- commits to `main`;
- merges a PR whose checks fail;
- waives or rewrites a gate; or
- skips a step of the release ritual.

When pausing, record the status, the reason, and the resume point in the plan's status line rather than in a separate handoff file.

## Releasing

Follow [the release ritual](references/release.md). In brief:

1. Run the release check on `dev`: formatting, linting, the full test suite, and consistency between the version and the changelog.
2. Confirm every gate is met or waived.
3. Set the release version and date the changelog section.
4. Merge `dev` into `main` through a PR with a merge commit, after human approval.
5. Tag the release and create the GitHub release from the changelog.
6. Return to `dev`: merge `main` back, bump to the next development version, open `[Unreleased]`, and prune the plan.

The steps after the merge are part of the release, not cleanup.
