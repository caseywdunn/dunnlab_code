# Changelog

Notable changes to the dunnlab-code plugin and the manual. Versions follow the
release process in [`dev_docs/contributing.md`](dev_docs/contributing.md#releasing).

Lab members pick up a new version with `/plugin update dunnlab-code@dunnlab`;
auto-update is off by default for third-party marketplaces.

## 0.4.0

The manual now treats Claude Code and Codex as peer coding-agent harnesses and
expands its guidance for long-running, autonomous research workflows.

### Added

- **Agent Concepts** — a vendor-neutral conceptual template covering models,
  harnesses, the agent loop, context, tools, permissions, sandboxes, and
  sessions.
- **Working Across Computers** — SSH, SCP, tmux, remote machines, and the
  separation between an agent's control plane and remote compute.
- Guidance on treating the agent as a teacher, reducing routine supervision,
  piloting large analyses, and managing several active agent projects without
  exceeding the user's own attention.
- A quick three-step AI-reporting guide and a concise GAIDeT-based example.
- A project tracker taxonomy and a table of the context worth recording for
  each active, blocked, parked, pending, or completed project.

### Changed

- **Coding Agents** now maps Claude Code and Codex directly onto the same
  concepts, including their instruction files, permissions, sandboxes,
  sessions, skills, MCP servers, plugins, and cloud surfaces. Other agents are
  noted briefly rather than ranked.
- Getting Started, Quick Reference, Managing Security, Managing Context,
  Example Workflows, and Computing at Yale now present Claude Code and Codex as
  equal choices. The DunnLab plugin and cluster `settings.json` remain clearly
  labeled Claude-specific implementations of otherwise portable practices.
- The recommended stack is visible earlier: VS Code, terminal-first operation,
  text-based files, Git and GitHub, the `gh` CLI, and tmux for persistent remote
  sessions.
- Plans are explicitly version-controlled Markdown files such as `PLAN.md` or
  `dev_docs/overview.md`, with pilot runs and verification gates before large
  analyses proceed.
- The project's own AI-use statement now names both Claude Code and Codex and
  uses GAIDeT task categories.

## 0.3.0

An accuracy pass against current Claude Code and YCRC documentation, a
reorganization of the manual around who each chapter is for, and the first test
infrastructure this repository has had.

### Fixed

These were wrong, not merely out of date.

- **Bouchet scratch is purged at 30 days, not 60.** Stated as 60 in five places.
  Anyone trusting the old figure would lose data a month before they expected to.
  60 days remains correct for McCleary and Misha, which is presumably where it
  came from.
- **Three documented commands did not exist**: `claude plugin add`,
  `claude login` (it is `claude auth login`), and the unnamespaced
  `/dunnlab-check` (plugin skills are `/dunnlab-code:dunnlab-check`).
- **`deny` rules apply in every permission mode**, `bypassPermissions` included.
  The security chapter said the opposite. It is `allow` rules that stop having
  effect there.
- **Deny rules in the example cluster settings did not protect credentials.**
  Patterns without a `~/` or `//` prefix anchor to the working directory, so
  `~/.ssh`, `~/.aws`, and `~/.netrc` were never covered.
- **Permission patterns in the new-project template matched too much.**
  `Bash(ls*)` has no word boundary and also matches `lsof`; `Bash(rm -rf /)*`
  was malformed and matched nothing; `curl`, `wget`, and `python` were allowed
  without a prompt, which is arbitrary code execution.
- **Six `{: .warning }` callouts were rendering as ordinary paragraphs**,
  including the scratch purge warning. just-the-docs requires callouts to be
  declared in `_config.yml`.
- Bouchet partition and GPU tables: added the missing `gpu_h100` partition,
  corrected B200 vRAM and several per-user limits.
- The skill listing budget is 1% of the context window, not 2%, and overflow
  shortens descriptions rather than dropping skills.
- Auto mode is no longer a research preview; it is the default starting mode on
  Pro, Max, and Team plans.
- Every `docs.anthropic.com` link, which now redirects to `code.claude.com`.

### Added

**Six new chapters.** The manual is now ordered by audience, narrowing as it
goes: chapters 2–11 apply to anyone and can be shared with another institution
unchanged, chapter 12 is Yale, chapter 13 is this lab.

- **Using AI in Research** — accountability, reviewing generated code, data
  handling, and reporting AI use. No terminal required.
- **Quick Reference** — the whole thing on one page: setup, working rhythm,
  permission modes, sessions, tmux.
- **Working Effectively** — how to frame the work. Asking broadly rather than
  narrowly, separating planning from building, committing the plan as a
  document, and setting gates you can check.
- **DunnLab Plugin** — what the plugin contains and how to run it.
- **Other Coding Agents** — the wider landscape, `AGENTS.md`, and what carries
  between tools.
- **Computing at Yale** — YCRC clusters and running Claude Code on shared
  hardware.

**New coverage in existing chapters**: the Bash sandbox, `.claude/rules/`, auto
memory, the CIA triad framing for security risks, and a two-tier split between
what Claude decides and what the operating system enforces.

**An AI use statement** for this project, on the home page. The manual argues
for reporting AI use and now does so itself.

**Test infrastructure**, where there was none:

- `scripts/check.sh` — 21 checks covering manifests, skill frontmatter, nav
  order, internal and cross-file links, and specific errors fixed here so they
  cannot return by copy-paste. Mutation-tested rather than assumed.
- `scripts/preview-docs.sh` — renders and serves the site in Docker, no Ruby
  needed.
- `scripts/test-devcontainer.sh` — builds the hardened container from the skill
  itself.
- `scripts/verify-hpc-facts.sh` — read-only dump of cluster facts for checking
  the HPC skill against a live system.
- CI running the structural checks and a Jekyll build on every push and PR.

### Changed

- Python formatting and linting move from `black` + `flake8` to `ruff`.
- The devcontainer skill offers the official Dev Container Feature as its
  default path, keeping the hardened firewall configuration as a variant.
- The manual says *reporting* AI use rather than *disclosure*, except where
  naming someone else's standard. Disclosure borrows the conflict-of-interest
  frame, which presumes the thing disclosed is a taint.
- `dev_docs/contributing.md` documents a branching model and release ritual.

### Known limitations

- The Bouchet figures come from YCRC's published documentation and have not been
  checked against the live cluster. `scripts/verify-hpc-facts.sh` exists for
  that; where the two disagree, the cluster is right.
- `check.sh` does not verify the page table in `dev_docs/github-pages.md`, which
  has to be updated by hand.

## 0.2.0 and earlier

No changelog was kept. See the commit history.
