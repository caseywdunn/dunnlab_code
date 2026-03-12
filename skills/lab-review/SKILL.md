---
name: lab-review
description: >
  Code review checklist and process for Dunn Lab projects. Use when
  reviewing pull requests, auditing code quality, or giving feedback
  on scripts and analyses.
---

# Dunn Lab Code Review

When reviewing code in Dunn Lab projects, follow this process and checklist.

## Review process

1. **Understand the goal** — Read the PR description, linked issue, or commit messages to understand what the change is trying to accomplish before reading the code.
2. **Check the big picture first** — Does the approach make sense? Is it the right place for this change? Are there simpler alternatives?
3. **Walk through the diff** — Review the code in logical order (not file order). Start with the entry point and follow the data flow.
4. **Run the code** — Pull the branch locally. Run the tests. Try the new functionality. Check that outputs look correct.
5. **Leave constructive feedback** — Be specific, suggest alternatives, and distinguish between blocking issues and nits.

## Checklist

### Correctness

- [ ] Does the code do what it claims to do?
- [ ] Are edge cases handled (empty inputs, missing data, unexpected types)?
- [ ] Are numerical computations correct (off-by-one errors, floating-point issues, units)?
- [ ] For data analysis: are filtering, grouping, and aggregation steps correct?

### Error handling

- [ ] Are errors handled gracefully, not silently swallowed?
- [ ] Python: are exceptions specific (not bare `except:`)?
- [ ] Rust: are errors propagated with `?` instead of `.unwrap()`?
- [ ] Are error messages informative enough to diagnose the problem?

### Testing

- [ ] Are there tests for new or changed functionality?
- [ ] Do tests cover both happy paths and edge cases?
- [ ] Are tests deterministic (no flaky tests depending on timing or randomness)?
- [ ] Do all existing tests still pass?

### Style and conventions

- [ ] Does the code follow lab conventions (see `lab-defaults` skill)?
- [ ] Is formatting consistent (ran through `black`/`styler`/`cargo fmt`)?
- [ ] Are linters clean (`flake8`/`lintr`/`clippy`)?
- [ ] Are variable and function names descriptive and consistent with the codebase?

### Documentation

- [ ] Are new functions documented with docstrings/doc comments?
- [ ] Is the README or guide/ updated if behavior changed?
- [ ] Do comments explain *why*, not *what*?

### Data and reproducibility

- [ ] Is raw data left unmodified?
- [ ] Are random seeds set where reproducibility matters?
- [ ] Are dependencies pinned or specified in `environment.yml` / `renv.lock` / `Cargo.toml`?
- [ ] Can someone else reproduce the results from a clean environment?

### Performance and resources

- [ ] Are there unnecessary copies of large data structures?
- [ ] Will this scale to the expected data size?
- [ ] Are file handles and database connections properly closed?

### Security and data integrity

- [ ] Are file paths constructed safely (no injection risks)?
- [ ] Are sensitive data (keys, patient IDs) excluded from version control?
- [ ] Are outputs written to the correct locations (not overwriting raw data)?

## Giving feedback

- **Be specific**: "This filter drops rows where `gene_id` is NA — was that intentional?" is better than "Check the filtering logic."
- **Suggest, don't demand**: "Consider using `pd.merge` here for clarity" rather than "Change this to `pd.merge`."
- **Distinguish severity**: Prefix with `blocking:`, `suggestion:`, or `nit:` so the author knows what must be fixed vs. what's optional.
- **Acknowledge good work**: Call out clean abstractions, thorough tests, or clever solutions.
