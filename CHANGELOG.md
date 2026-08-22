# Changelog

Notable changes to the dunnlab-code plugin. Versions follow the release
process in [`dev_docs/contributing.md`](dev_docs/contributing.md#releasing).

Lab members pick up a new version with `/plugin update dunnlab-code@dunnlab`;
auto-update is off by default for third-party marketplaces.

## 0.3.0

Accuracy pass against current Claude Code and YCRC documentation.

### Fixed
- **Bouchet scratch is purged at 30 days, not 60.** Corrected in the HPC skill
  and the example cluster settings.
- Bouchet partition and GPU tables: added the missing `gpu_h100` partition and
  H100, corrected B200 vRAM and several per-user job limits.
- Removed three commands that do not exist: `claude plugin add`,
  `claude login`, and unnamespaced `/dunnlab-check`.
- `deny` rules apply in *every* permission mode, including
  `bypassPermissions` — the security page said the opposite.
- Deny rules in the example HPC settings were anchored to the working
  directory, so they did not protect `~/.ssh`, `~/.aws`, or `~/.netrc`.
- Permission patterns in the new-project template had no word boundary
  (`Bash(ls*)` also matched `lsof`) and allowed arbitrary code execution
  through `curl`, `wget`, and `python`.
- Skill listing budget is 1% of the context window, not 2%.

### Added
- Bash sandbox, `.claude/rules/`, and auto memory documentation.
- Dev Container Feature as the default devcontainer path, with the hardened
  firewall configuration retained as a variant.
- `scripts/check.sh` and `scripts/test-devcontainer.sh`, run in CI.
- Lab code review expectations in `docs/lab-practices.md`.

### Changed
- Python formatting and linting moved from `black` + `flake8` to `ruff`.
