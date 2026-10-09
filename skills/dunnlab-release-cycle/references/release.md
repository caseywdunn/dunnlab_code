# The release ritual

Every step runs every time. A skipped step tends to surface releases later, as a `dev` that has drifted from `main` or a changelog missing a version. The project's `CONTRIBUTING.md` holds the concrete commands, including project-specific additions such as a bioconda recipe, a Zenodo deposit, or a package upload. This file defines the parts every project shares.

Throughout, `X.Y.Z` is the version being released.

## The release check

Keep one script, for example `scripts/release-check` or a `make release-check` target, that an agent or a person runs locally and CI runs on PRs into `main`. It exits non-zero on any failure. It runs:

- the formatter in check mode (`ruff format --check`, `cargo fmt --check`, or `styler` with a diff check);
- the linter with warnings as errors (`ruff check`, `cargo clippy -- -D warnings`, `lintr`);
- the full test suite, including integration tests;
- a version check: the version file and `CHANGELOG.md` agree, and the changelog has entries for the release; and
- any project-specific release checks, such as a clean-environment install or a known-answer analysis.

Use the same formatter and linter configuration as everyday development. A check that only runs at release time is one that fails at release time.

## Steps

1. **Check readiness.** On an up-to-date `dev`, confirm that every gate in `dev_docs/PLAN.md` is `met` or `waived`, and run the release check.
2. **Prepare the release on a branch.** Branch `release-X.Y.Z` from `dev`. Set the version to `X.Y.Z` with no development marker. Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`. Run the release check again, then open a PR into `dev` and merge it once CI passes.
3. **Get approval.** Open a PR from `dev` into `main` titled `Release X.Y.Z`, with the changelog section as its body. A person approves the release. Agents stop here and ask.
4. **Merge.** When CI passes and the release is approved, merge with a merge commit, not a squash, so `dev`'s history survives and the release diff is reviewable.
5. **Tag and publish.**

   ```bash
   git fetch origin
   git tag -a vX.Y.Z origin/main -m "Release X.Y.Z"
   git push origin vX.Y.Z
   awk '/^## \[X.Y.Z\]/{p=1; next} /^## \[/{p=0} p' CHANGELOG.md > /tmp/notes.md
   gh release create vX.Y.Z --title "X.Y.Z" --notes-file /tmp/notes.md
   ```

   Then run any project-specific publication steps.
6. **Return to `dev`.** Branch `post-release-X.Y.Z` from `origin/main`, so the branch carries the release merge commit. On it:
   - bump the version to the next development version, such as `X.(Y+1).0-dev`;
   - add an empty `## [Unreleased]` section to the changelog; and
   - prune `PLAN.md`: delete the released section and promote the next release.

   Open a PR into `dev` and merge it.
7. **Verify.** Run `git merge-base --is-ancestor vX.Y.Z origin/dev`, which must succeed. Check that the tag check in CI passed.

## Check the tag in CI

Add a workflow that runs when a tag is pushed and fails if the tag and the project disagree. Replace the version command with the project's own:

```yaml
name: tag-check
on:
  push:
    tags: ["v*"]
jobs:
  tag-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          version=$(python -c "import mypkg; print(mypkg.__version__)")
          test "v$version" = "$GITHUB_REF_NAME"
          grep -q "^## \[$version\]" CHANGELOG.md
```

## Hotfixes

When a released version needs an urgent fix:

1. Open an issue. Branch `hotfix-<slug>` from `main`.
2. Fix it with a test, bump the patch version, and add a dated changelog section.
3. Open a PR into `main`. After approval and passing CI, merge it, then tag and publish as in step 5.
4. Merge `main` back into `dev` at once, as in step 6, resolving any conflicts there.

A hotfix is the only change that reaches `main` without passing through `dev` first. Step 4 is what keeps it from becoming drift.
