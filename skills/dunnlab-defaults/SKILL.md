---
name: dunnlab-defaults
description: >
  Dunn Lab language, coding, dependency, testing, and documentation conventions.
  Use when writing or reviewing code. Workflow architecture belongs to
  dunnlab-workflow-design; repository scaffolding belongs to dunnlab-new-project.
---

# Dunn Lab Defaults

Apply these coding preferences within the requested task and established project conventions. Use `dunnlab-workflow-design` for computational workflow architecture and execution, `dunnlab-new-project` for repository scaffolding, and `dunnlab-lifecycle` for scientific analysis phases. These skills own their respective requirements; this skill does not define a second workflow or lifecycle.

## Preferred languages and tools

Languages for data analysis and scripting:
- **Python** for data analysis and scripting (prefer Python 3.10+)
- Fall back to **R** when analyses require specific R libraries such as Seurat (use tidyverse conventions)
- Use **conda** or **mamba** for environment management
- Use **Jupyter notebooks** for exploratory work and **Quarto** for manuscripts. A retained notebook is acceptable when it runs from a clean kernel with explicit inputs and settings. Extract scripts or shared functions when reuse or execution needs warrant it; do not rewrite solely because work began in a notebook.

Languages for performant critical code:
- Use **Rust** for performance-critical code.

### Python best practices
- Follow PEP 8 style guidelines, using [`ruff`](https://docs.astral.sh/ruff/) for both formatting (`ruff format`) and linting (`ruff check`). Ruff replaces the older `black` + `flake8` + `isort` combination; configure it in `pyproject.toml`.
- Use type hints and `mypy` for static type checking. Ruff does not type check.
- Use `pydantic` for data validation and settings management.
- Prefer the following libraries for common tasks:
  - Data manipulation: `pandas`
  - Scientific computing: `numpy`, `scipy`
  - Machine learning: `scikit-learn`, `xgboost`
  - Deep learning: `pytorch`
  - Visualization: `matplotlib`, `seaborn`, `plotly`
- Use `dunnlab-bioinformatics` for biological tool and library preferences.

### R best practices
- Follow tidyverse style guidelines, using `styler` for formatting and `lintr` for linting.
- Use `roxygen2` for documentation
- Use `testthat` for testing and `usethis` for package development.
- Use `renv` for environment management.

### Rust best practices

- **Never use `.unwrap()` or `.expect()` in library/application code** — propagate errors with `?` and return `Result` types instead. Panicking crashes the program with no chance of recovery.
- Use `thiserror` for defining custom error types in libraries; use `anyhow` for error handling in binaries and scripts.
- Prefer `Option::unwrap_or`, `unwrap_or_default`, or `unwrap_or_else` when a sensible fallback exists.
- Use `clippy` with warnings promoted to errors in CI (`-D warnings`).
- Prefer iterators and combinators over manual loops where they improve clarity.
- Avoid `unsafe` unless absolutely necessary, and document the safety invariant with a `// SAFETY:` comment.
- Use `cargo fmt` to enforce consistent formatting.
- Write doc comments (`///`) on all public items.

## Dependencies and environment management

Always include idiomatic dependency management. For example, an `environment.yml` (for Python) or `renv.lock` (for R) to specify dependencies. For Rust, ensure `Cargo.toml` is up to date.

- Use `conda` or `mamba` for managing Python environments. Create an `environment.yml` file to specify dependencies.
  - For complex workflows with multiple stages, consider using separate environment files in an `env/` folder at the project root (e.g., `env/environment_data.yml`, `env/environment_analysis.yml`).
  - This keeps environments organized, allows for more efficient dependency management, and prevents problems resolving complex dependencies.
  - Document environment setup before usage in the canonical setup guide; workflow documentation follows `dunnlab-workflow-design`.
- Use `renv` for R projects to manage package dependencies and ensure reproducibility.
- For Rust projects, manage dependencies with `Cargo.toml` and use `cargo` for building and testing.

## File naming conventions

Always follow idiomatic conventions for the language you're using. For example:
  - Python: `snake_case.py` for scripts, `PascalCase` for classes
  - R: `snake_case.R` for scripts, `snake_case` for functions
  - Rust: `snake_case.rs` for modules, `PascalCase` for structs and enums

Otherwise:
- Use lowercase with hyphens (kebab case) for directories: `raw-data/`, `analysis-scripts/`
- Use lowercase with underscores for scripts: `clean_sequences.py`, `plot_results.R`
- Prefix data files with dates in ISO format when versioning matters: `2026-03-08_sample_metadata.csv`

## Comment and docstring style

- Python: Use Google-style docstrings
- R: Use roxygen2-style comments for functions
- Write comments that explain *why*, not *what*

## Performance considerations

Performance is a high priority. Always consider algorithmic efficiency, for example avoid nested loops over large datasets in favor of vectorized operations or parallel processing where appropriate.

Avoid needless data copying or transformations.

Parallelize where appropriate.

- For Python, use `numpy` and `pandas` vectorized operations instead of loops where possible. Use `numba` or `cython` for performance-critical code.
- For R, use `data.table` for large data frames and vectorized operations. Use `Rcpp` for performance-critical code.
- For Rust, prefer idiomatic Rust patterns and avoid unnecessary allocations.

Avoid premature optimization, but keep performance in mind as you write code. Do not write inefficient code for the sake of "getting something working" — aim for clean, efficient code from the start. Do not make big sacrifices in code quality or readability for small performance gains.

## Testing

### Standard test frameworks

Use the idiomatic test framework for each language — do not introduce third-party runners unless there is a specific need:

- **Python**: `pytest` (with `pytest-cov` for coverage)
- **R**: `testthat`
- **Rust**: built-in `#[cfg(test)]` module and `cargo test`

### Unit tests

- Test consequential behavior: branching logic, error handling, joins, and non-obvious transformations that could change a result or break an interface. Match test effort to the task and consequences; do not exhaustively harden disposable exploratory branches. Keep the scientific correctness checks required by `dunnlab-workflow-design` and `dunnlab-lifecycle`.
- Keep tests focused — one behavior per test, with a clear name describing what is being verified (e.g., `test_parse_fasta_handles_empty_input`).
- Use fixtures and parameterized tests to avoid duplication.

### Test fixtures and helpers

- Build reusable test fixtures for common data structures (e.g., sample DataFrames, mock FASTA records, temporary file trees).
  - **Python**: use `pytest` fixtures in `conftest.py`
  - **R**: use `testthat` helper files in `tests/testthat/helper-*.R`
  - **Rust**: use a shared `mod test_utils` or builder patterns in the test module
- Keep fixture data small and deterministic — avoid relying on external files or network access in unit tests.

### Integration tests

- Use a small integration test when an end-to-end path or component interaction needs verification (e.g., raw input → processed output).
- Place integration tests in a dedicated location:
  - **Python**: `tests/integration/`
  - **R**: `tests/testthat/test-integration-*.R`
  - **Rust**: `tests/` directory (Rust's built-in integration test location)
- Integration tests may use real data files stored in a `tests/data/` or `tests/fixtures/` directory, but keep them small.

## Code and project documentation

Prefer idiomatic source and test structures for the language, preserving established layouts. `dunnlab-new-project` creates the minimum project scaffold; `dunnlab-workflow-design` owns the organization of analyses, inputs, outputs, and execution guides. Do not create directories or documents solely to fill a template.

For software projects, README.md should include a project overview, setup instructions, usage examples, and a link to the development guide. For scientific analyses, follow `dunnlab-workflow-design` for reader-facing READMEs and canonical reproduction instructions; keep developer checks and construction history in linked developer documentation.

Use `dev_docs/` for focused developer material such as the data model, implementation decisions, and internal verification instructions. Keep it readable by people and loadable as needed by coding agents; link to reader-facing methods and usage rather than duplicating them.

AGENTS.md holds the project instructions: how to build, test, and work on this project, plus any custom skills or commands. **Keep it to 100 lines or less** so standing context stays small. Include links and descriptions for the following files when present so they can be loaded as needed:
- README.md
- CONTRIBUTING.md
- Each file in `dev_docs/` (e.g., `overview.md`, `data-model.md`)

Codex reads [`AGENTS.md`](https://agents.md/) directly. Claude Code reads CLAUDE.md and not AGENTS.md, so make CLAUDE.md a one-line import rather than a second copy:

```markdown
@AGENTS.md
```

Two files maintained in parallel drift, and a reader cannot tell which is current. One file with an import gives both harnesses the same version-controlled instructions.

When project guidance outgrows that limit, move detailed instructions into linked documents. Use nested instructions or path-scoped rules only where the active harness supports them; keep shared conventions accessible from the canonical project instructions instead of duplicating them for each agent.

CONTRIBUTING.md should include all details needed for formatting, linting, testing, and any other project-specific development practices.

## Version control best practices

Exclude bulk data, results, and logs from version control by default. Retain small fixtures and the provenance/specification records needed to interpret results; workflow-design defines their role. Respect files the user has chosen to track. For example:

```
# Ignore data and results
data/
results/
logs/
```

Always include .DS_Store and other common OS artifacts in .gitignore.

Before staging files, inspect size and contents to avoid including large artifacts or sensitive information unintentionally. Follow the project's commit workflow and the user's requested scope; using this skill does not require a commit.

Use descriptive commit messages that explain *why* a change was made, not just *what* changed. For example:
- Good: "Refactor data cleaning to handle missing values and edge cases"
- Bad: "Update clean_data.py"

### Running formatting and linting before commits

- Run relevant formatting and lint checks for changed code before committing. Preserve unrelated changes; do not apply repository-wide formatting fixes merely to make a small edit.
- For Python, use `ruff format` and `ruff check`; for R, `styler` and `lintr`; for Rust, `cargo fmt` and `cargo clippy`.
- Use pre-commit hooks or CI checks where the project already supports them, or add them when requested.

### Running tests before commits

- Run tests relevant to the changed behavior and any checks required by the project. Run the full suite when the change crosses components, the suite is inexpensive, or a release or project policy requires it.
- Use `pytest`, `testthat::test_local()`, or `cargo test` as appropriate. Fix failures caused by the change and report unrelated failures or checks that could not run; do not imply unrun checks passed.

### Updating documentation before commits

- Update README.md and dev_docs/ files as needed to reflect changes in functionality, usage, or project structure.
- If the change introduces new features or modifies existing ones, update the relevant sections in README.md and any relevant dev_docs/ files to keep documentation accurate and up to date.

Work in small coherent increments with verification appropriate to each change. Preserve a concise handoff when pausing or changing sessions: current work, decisions, verification, and next action. Clear context when useful, not after every task by rule.
