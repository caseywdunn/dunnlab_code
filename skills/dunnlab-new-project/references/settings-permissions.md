# Claude Code Permissions for New Projects

Use these permission rules when generating `.claude/settings.json`. The goal is to let Claude work fluidly for reading and running code while requiring confirmation for anything that modifies files, installs packages, or touches git history.

## JSON format

The settings file uses three arrays — `allow`, `ask`, and `deny` — each containing permission strings. Tool permissions use `ToolName(glob)` syntax; Bash command permissions use the command prefix as a string.

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Read(**)",
      "Glob",
      "Grep",
      "Task",
      "Bash(git status*)",
      "Bash(git log*)",
      "Bash(git diff*)",
      "Bash(git branch*)",
      "Bash(git remote*)",
      "Bash(git show*)",
      "Bash(ls*)",
      "Bash(cat*)",
      "Bash(head*)",
      "Bash(tail*)",
      "Bash(wc*)",
      "Bash(find*)",
      "Bash(du*)",
      "Bash(df*)",
      "Bash(file*)",
      "Bash(which*)",
      "Bash(echo*)",
      "Bash(pwd*)",
      "Bash(tree*)",
      "Bash(diff*)",
      "Bash(curl*)",
      "Bash(wget*)",
      "Bash(python*)",
      "Bash(python3*)",
      "Bash(conda activate*)",
      "Bash(conda deactivate*)",
      "Bash(conda env list*)",
      "Bash(conda list*)",
      "Bash(conda info*)",
      "Bash(mamba activate*)",
      "Bash(mamba deactivate*)",
      "Bash(mamba env list*)",
      "Bash(mamba list*)",
      "Bash(mamba info*)",
      "Bash(pip list*)",
      "Bash(pip show*)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(.ssh/**)",
      "Read(.netrc)",
      "Read(*credentials*)",
      "Read(*secret*)",
      "Read(*token*)",
      "Read(*.pem)",
      "Read(*.key)",
      "Read(.aws/**)",
      "Edit(.env)",
      "Edit(.env.*)",
      "Edit(.ssh/**)",
      "Edit(.netrc)",
      "Edit(*credentials*)",
      "Edit(*secret*)",
      "Edit(*token*)",
      "Edit(*.pem)",
      "Edit(*.key)",
      "Edit(.aws/**)",
      "Bash(rm -rf /)*",
      "Bash(sudo*)",
      "Bash(su *)",
      "Bash(shutdown*)",
      "Bash(reboot*)",
      "Bash(dd if=*)",
      "Bash(ssh *)",
      "Bash(nc *)",
      "Bash(netcat*)",
      "Bash(nmap*)",
      "Bash(kill -9*)",
      "Bash(killall*)",
      "Bash(pkill*)"
    ]
  }
}
```

Everything not in `allow` or `deny` falls through to `ask` (the user gets prompted). This covers mutating git commands, package installs, file operations, `Edit`, `Write`, etc. — no need to list them explicitly.

## Permission rules reference

### Allow without prompting

Read-only tools and commands that don't modify the project:

- `Read(**)`, `Glob`, `Grep`, `Task`
- Read-only git: `git status`, `git log`, `git diff`, `git branch`, `git remote`, `git show`
- Read-only shell: `ls`, `cat`, `head`, `tail`, `wc`, `find`, `du`, `df`, `file`, `which`, `echo`, `pwd`, `tree`, `diff`
- Network reads: `curl`, `wget`
- Python: `python`, `python3`
- Conda/Mamba info: `conda activate/deactivate/env list/list/info`, `mamba activate/deactivate/env list/list/info`
- Package info: `pip list`, `pip show`

### Ask for confirmation (default for unlisted commands)

Commands that modify files, packages, or git state — these don't need explicit `ask` entries because anything not in `allow` or `deny` is automatically prompted:

- `Edit(**)`, `Write(**)`
- Mutating git: `git push`, `git commit`, `git checkout`, `git merge`, `git rebase`, `git reset`, `git stash`, `git add`
- Package management: `conda install/create/remove/env create/env remove/update`, `mamba install/create/remove/env create/env remove/update`, `pip install`, `pip uninstall`
- File operations: `cp`, `mv`, `rm`, `mkdir`, `rsync`
- `chmod`
- `WebFetch`

### Deny

Sensitive file access and destructive commands:

- Reading/editing sensitive files: `.env`, `.env.*`, `.ssh/**`, `.netrc`, `*credentials*`, `*secret*`, `*token*`, `*.pem`, `*.key`, `.aws/**`
- Destructive commands: `rm -rf /`, `sudo`, `su`, `shutdown`, `reboot`, `dd if=`
- Network probing: `ssh`, `nc`, `netcat`, `nmap`
- Process killing: `kill -9`, `killall`, `pkill`
