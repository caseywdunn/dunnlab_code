# Setting up the release cycle

Use this when a project adopts the release cycle, either at creation through `dunnlab-new-project` or when an existing project outgrows working on `main`. Confirm with the user before changing branches or repository settings. Complete only the steps that are missing.

## Branches

The default branch is `main`, so visitors see released code. Create `dev` from the current `main` and push it:

```bash
git switch main && git pull
git switch -c dev && git push -u origin dev
```

If the project has never been released, consider tagging the current `main` as its first version so the cycle has a starting point.

## Protect the branches

Rules that nothing enforces get skipped. Create a ruleset for each branch so GitHub refuses direct pushes and merges that have not passed CI. The `context` value is the name of the CI job that must pass:

```bash
gh api repos/OWNER/REPO/rulesets -X POST --input - <<'EOF'
{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 0,
      "dismiss_stale_reviews_on_push": false,
      "require_code_owner_review": false,
      "require_last_push_approval": false,
      "required_review_thread_resolution": false}},
    {"type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": false,
      "required_status_checks": [{"context": "checks"}]}}
  ]
}
EOF
```

Create the same ruleset for `dev` by changing the name and `refs/heads/main`. Check the result with `gh api repos/OWNER/REPO/rulesets`.

Rulesets on private repositories require a paid GitHub plan. Without one, keep the rules in `AGENTS.md` and `CONTRIBUTING.md`, and add a local `pre-push` hook that refuses pushes to `main`.

## Continuous integration

Run format, lint, and test checks on every push and PR to `dev` and `main`. Run the full [release check](release.md#the-release-check) on PRs into `main`. Add the [tag check](release.md#check-the-tag-in-ci). The job name used as the ruleset's required check must match the workflow's job name.

## Files

- **`CHANGELOG.md`:** a Keep a Changelog header and an empty `## [Unreleased]` section.
- **Version:** one source of truth, carrying the development marker on `dev`.
- **`dev_docs/PLAN.md`:** from [the plan template](plan-template.md), with the first release's goal, steps, and gates. Draft gates with the user; they define how far an agent can go unattended.
- **`scripts/release-check`:** the release check.
- **`CONTRIBUTING.md`:** the branching model, everyday checks, and the release ritual with this project's concrete commands, linking the shared steps rather than restating them.

## Agent instructions

Add a short section to `AGENTS.md`, keeping within its line limit:

```markdown
## Development cycle

This project uses a release cycle (see CONTRIBUTING.md and dev_docs/PLAN.md).
- Never commit or push to `main`. Work on `issue-<N>-<slug>` branches from `dev`; merge to `dev` by PR after CI passes.
- Each PR updates `CHANGELOG.md` under [Unreleased] and its step's status in `dev_docs/PLAN.md`.
- Close an issue when its fix lands on `dev`, with a comment naming the commit and evidence.
- Stop at human-review gates and before any release. Never waive or rewrite a gate.
```
