---
name: dunnlab-defaults
description: >
  Applies Dunn Lab coding conventions and defaults. Use when starting
  and modifying new analysis scripts, writing documentation, or setting up project
  structure. Includes preferred languages, formatting, and file
  organization patterns.
---

# Dunn Lab Defaults

When working on Dunn Lab projects, follow these conventions:

## Preferred languages and tools

Languages for data analysis and scripting:
- **Python** for data analysis and scripting (prefer Python 3.10+)
- Fall back to **R** for when analyses require specific R libraries such as seurat (use tidyverse conventions)
- Use **conda** or **mamba** for environment management
- Use **Jupyter notebooks** for exploratory work; refactor into scripts for production; use quarto for manuscripts

Languages for performant critical code:
- Use **Rust** for performance-critical code.

### Python best practices
- Follow PEP 8 style guidelines, using `black` for formatting and `flake8` for linting.
- Use type hints and `mypy` for static type checking.
- Use `pydantic` for data validation and settings management.
- Prefer the following libraries for common tasks:
  - Data manipulation: `pandas`
  - Scientific computing: `numpy`, `scipy`
  - Machine learning: `scikit-learn`, `xgboost`
  - Deep learning: `pytorch`
  - Bioinformatics: `biopython`, `scanpy`
  - Visualization: `matplotlib`, `seaborn`, `plotly`

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
- Use `renv` for R projects to manage package dependencies and ensure reproducibility.
- For Rust projects, manage dependencies with `Cargo.toml` and use `cargo` for building and testing.

Use bioconda for installing bioinformatics tools when possible.

## File naming conventions

Always follow idiomatic conventsions for the language you're using. For example:
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

## Workflow orchestration

Choose the orchestration tool based on workflow complexity:

### Snakemake for complex workflows

Use **Snakemake** when a workflow involves multiple independent tools, fan-out/fan-in patterns, or complex dependency graphs. Snakemake handles parallelism, cluster submission, and dependency resolution automatically.

- Define each stage as a rule with explicit `input` and `output` files.
- Use `conda:` directives per rule to isolate tool environments.
- Store the `Snakefile` at the project root and keep per-rule wrapper scripts in `scripts/` if rule logic exceeds a few lines.

### Bash or Python orchestrators for simple workflows

For simpler multi-step pipelines that form a linear chain (A → B → C), a plain **bash** or **Python** script is sufficient. Use this when introducing Snakemake would add more complexity than it removes.

- In bash, chain steps with `set -euo pipefail` and check for existing outputs before each step.
- In Python, use `subprocess.run(..., check=True)` and `pathlib.Path.exists()` checks.

### Checkpointing — skip completed stages

All orchestrators must implement checkpointing: **do not re-run a stage if its output already exists**. This applies to Snakemake (built-in via output file tracking) and to bash/Python scripts (explicit existence checks).

- Each stage should write its output to a well-defined path.
- Before running a stage, check whether the output file or directory already exists; if so, skip it.
- To re-run a specific stage, the user deletes that stage's output and re-launches the pipeline — the orchestrator picks up from there.
- Never use sentinel/lock files or hidden state to track completion; the presence of the output itself is the checkpoint.

### Multi-analysis projects

When a project contains multiple distinct analyses that share raw data but have independent processing pipelines, organize each analysis in its own subdirectory (e.g., `analyses_kmer/`, `analyses_qc/`, `analyses_assembly/`). Each subdirectory gets its own Snakefile (or orchestration script), config file, and output directory. Shared raw data stays in `data/raw/` at the project root or is referenced from an external location.

### Logging tool outputs

Redirect stdout and stderr from external tools to structured log files in `logs/`. Use a consistent naming convention: `logs/{tool}/{sample}.log` or `logs/{stage}.log`. This keeps the working directory clean and makes debugging easier. In Snakemake, use the `log:` directive. In bash scripts, use `> logfile 2>&1` or `&> logfile` redirection. Exclude `logs/` from version control.

## Testing

### Standard test frameworks

Use the idiomatic test framework for each language — do not introduce third-party runners unless there is a specific need:

- **Python**: `pytest` (with `pytest-cov` for coverage)
- **R**: `testthat`
- **Rust**: built-in `#[cfg(test)]` module and `cargo test`

### Unit tests

- Write unit tests for every nontrivial function. If a function has branching logic, error handling, or non-obvious transformations, it needs tests.
- Keep tests focused — one behavior per test, with a clear name describing what is being verified (e.g., `test_parse_fasta_handles_empty_input`).
- Use fixtures and parameterized tests to avoid duplication.

### Test fixtures and helpers

- Build reusable test fixtures for common data structures (e.g., sample DataFrames, mock FASTA records, temporary file trees).
  - **Python**: use `pytest` fixtures in `conftest.py`
  - **R**: use `testthat` helper files in `tests/testthat/helper-*.R`
  - **Rust**: use a shared `mod test_utils` or builder patterns in the test module
- Keep fixture data small and deterministic — avoid relying on external files or network access in unit tests.

### Integration tests

- Write integration tests that exercise end-to-end workflows (e.g., raw input → processed output).
- Place integration tests in a dedicated location:
  - **Python**: `tests/integration/`
  - **R**: `tests/testthat/test-integration-*.R`
  - **Rust**: `tests/` directory (Rust's built-in integration test location)
- Integration tests may use real data files stored in a `tests/data/` or `tests/fixtures/` directory, but keep them small.

## Default project structure

Use idiomatic project structures for each language, but generally follow this example pattern for organization:

```
project-name/
├── .gitignore
├── README.md
├── CLAUDE.md
├── documentation/
│   ├── overview.md
│   └── data-model.md # These are example documents
├── CONTRIBUTING.md
├── data/
│   ├── raw/          # Never modify raw data
│   └── processed/
├── scripts/
├── notebooks/
├── results/
│   ├── figures/
│   └── tables/
├── logs/             # Tool and pipeline stdout/stderr
└── environment.yml   # or requirements.txt
```

README.md should include a project overview, setup instructions (for environment, dependencies, and the project itself), and usage examples. Also include a Development section at the running tests and any relevant notes about data sources or analysis workflows.

documentation/ should include any relevant documentation for the project, such as an overview of the data model, descriptions of analysis workflows, or notes on interpretation of results. It is intended to be both human readable and to be loaded into context by Claude Code when working on relevant parts of the project.

CLAUDE.md should document how to use Claude Code for this project, including any custom skills or commands. Keep it to 100 lines or less. It must also include links and descriptions to the following files at a minimum so they can be loaded into context as needed:
- README.md
- CONTRIBUTING.md
- Each file in `documentation/` (e.g., `overview.md`, `data-model.md`)

CONTRIBUTING.md should include all details needed for formatting, linting, testing, and any other project-specific development practices.

## Version control best practices

Exclude data and results from version control with `.gitignore`, unless user specifically adds something to track. For example:

```
# Ignore data and results
data/
results/
```

Always include .DS_Store and other common OS artifacts in .gitignore.

Before adding something to version control, check the file size and contents. If it's large or contains sensitive information, warn the user before committing.

Use descriptive commit messages that explain *why* a change was made, not just *what* changed. For example:
- Good: "Refactor data cleaning to handle missing values and edge cases"
- Bad: "Update clean_data.py"

### Running formatting and linting before commits

- Always run formatters and linters before committing. Use pre-commit hooks to automate this where possible.
- For Python, run `black .` and `flake8 .` before committing.
- For R, run `styler::style_dir()` and `lintr::lint_dir()` before committing.
- For Rust, run `cargo fmt` and `cargo clippy` before committing.

### Running tests before commits

- **Always run the full test suite before committing.** Do not commit code with failing tests.
- Use pre-commit hooks or CI checks to enforce this. At minimum, run:
  - `pytest` for Python projects
  - `testthat::test_local()` for R packages
  - `cargo test` for Rust projects

### Updating documentation before commits

- Update README.md and documentation/ files as needed to reflect changes in functionality, usage, or project structure.
- If the change introduces new features or modifies existing ones, update the relevant sections in README.md and any relevant documentation/ files to keep documentation accurate and up to date.
