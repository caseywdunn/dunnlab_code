# Claude Code Permissions for New Projects

Use these permission rules when generating `.claude/settings.json`. The goal is to let Claude work fluidly for reading and running code while requiring confirmation for anything that modifies files, installs packages, or touches git history.

## JSON format

The settings file uses three arrays — `allow`, `ask`, and `deny`. Tool permissions use `ToolName(specifier)` syntax.

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Read(**)",
      "Glob",
      "Grep",

      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git branch:*)",
      "Bash(git remote:*)",
      "Bash(git show:*)",

      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(find:*)",
      "Bash(du:*)",
      "Bash(df:*)",
      "Bash(file:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(pwd:*)",
      "Bash(tree:*)",
      "Bash(diff:*)",

      "Bash(conda activate:*)",
      "Bash(conda deactivate:*)",
      "Bash(conda env list:*)",
      "Bash(conda list:*)",
      "Bash(conda info:*)",
      "Bash(mamba activate:*)",
      "Bash(mamba deactivate:*)",
      "Bash(mamba env list:*)",
      "Bash(mamba list:*)",
      "Bash(mamba info:*)",
      "Bash(pip list:*)",
      "Bash(pip show:*)",

      "Bash(pytest:*)",
      "Bash(ruff check:*)",
      "Bash(ruff format:*)",
      "Bash(mypy:*)"
    ],
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.netrc)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/.ssh/**)",
      "Read(**/.netrc)",
      "Read(**/*credentials*)",
      "Read(**/*secret*)",
      "Read(**/*token*)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Read(**/.aws/**)",

      "Edit(**/.env)",
      "Edit(**/.env.*)",
      "Edit(**/.ssh/**)",
      "Edit(**/.netrc)",
      "Edit(**/*credentials*)",
      "Edit(**/*secret*)",
      "Edit(**/*token*)",
      "Edit(**/*.pem)",
      "Edit(**/*.key)",

      "Bash(rm -rf /:*)",
      "Bash(rm -rf ~:*)",
      "Bash(sudo:*)",
      "Bash(su :*)",
      "Bash(shutdown:*)",
      "Bash(reboot:*)",
      "Bash(dd if=:*)",
      "Bash(ssh :*)",
      "Bash(nc :*)",
      "Bash(netcat:*)",
      "Bash(nmap:*)",
      "Bash(kill -9:*)",
      "Bash(killall:*)",
      "Bash(pkill:*)"
    ]
  }
}
```

## Rule syntax gotchas

These are easy to get wrong, and both failure modes are silent.

**Always put a boundary before the wildcard.** `Bash(ls:*)` and the equivalent `Bash(ls *)` match `ls -la` but not `lsof`. Writing `Bash(ls*)` with no space and no colon matches both, so a rule meant to allow `find` also allows anything else starting with those letters. The `:*` form only works at the *end* of a pattern.

**File rules are anchored by their leading characters:**

| Pattern | Anchored at |
|---------|-------------|
| `**/.env`, `./secrets/**` | Current working directory |
| `/src/**` | The directory of the settings file |
| `~/.ssh/**` | Home directory |
| `//etc/**` | Filesystem root |

Since this file goes in a project's `.claude/settings.json`, the `**/` patterns cover the project, which is what you want. The `~/` entries are there because a project-scoped rule would not otherwise protect your actual SSH keys if Claude wandered outside the tree.

**Only `Read` and `Edit` take paths.** `Edit(...)` covers every built-in tool that writes files, and a `Read` deny also blocks writes to the same path. Rules written for `Write`, `NotebookEdit`, `Glob`, or `MultiEdit` are accepted, never consulted, and warned about at startup. Use `Edit(docs/**)`, not `Write(docs/**)`.

**Deny rules bound Claude's file tools and the file commands it recognizes in Bash** (`cat`, `head`, `sed`). They do not stop a Python script Claude runs from opening the same file. Only the [Bash sandbox](https://code.claude.com/docs/en/sandboxing) enforces that at the OS level.

## What each list is for

### Allow — no prompt

Read-only tools and commands that cannot modify the project, plus the project's own test, lint, and type-check commands so the edit-test loop runs uninterrupted.

**Do not put interpreters or network fetchers in `allow`.** `Bash(python:*)`, `Bash(curl:*)`, and `Bash(wget:*)` amount to arbitrary code execution: they let Claude run anything without a prompt, which defeats every other rule in the file. Claude Code drops rules like these automatically when entering auto mode, for exactly this reason. Allow the specific commands you want (`Bash(pytest:*)`, `Bash(python scripts/build.py)`) instead of the interpreter.

### Unlisted — prompted, or governed by the mode

Anything not in `allow` or `deny` falls through to the permission mode. This covers mutating git commands, package installs, `cp`/`mv`/`rm`/`mkdir`, and `WebFetch`.

**Edits are deliberately not listed.** Permission rules are evaluated before the mode is consulted, so an `ask` rule on `Edit(**)` would force a prompt in *every* mode and defeat `acceptEdits` — which is the mode this file sets. Leaving edits unlisted makes them mode-driven instead: blocked in plan mode, prompted in Manual mode, auto-accepted in `acceptEdits` and `auto`. The `deny` block is the hard floor, enforced first and in every mode, so secrets stay protected regardless.

If a project needs edits to prompt, change `defaultMode` rather than adding an `ask` rule for `Edit`.

### Deny — blocked outright

Sensitive file access, destructive commands, network probing, and process killing.

Deny rules apply in **every** mode, `bypassPermissions` included, and no other settings scope can re-allow something denied at any level. This is the only control that holds unconditionally, which is why the interesting rules live here rather than in `ask`.

Claude Code separately refuses to let any allow rule or hook approve an `rm` against a critical path (`/`, its top-level directories, your home directory, the working directory and its parents), so those rules are belt-and-braces — but a deny still blocks where the built-in check only prompts.
