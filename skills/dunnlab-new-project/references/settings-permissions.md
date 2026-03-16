# Claude Code Permissions for New Projects

Use these permission rules when generating `.claude/settings.json`. The goal is to let Claude work fluidly for reading and running code while requiring confirmation for anything that modifies files, installs packages, or touches git history.

## Allow without prompting

Read-only tools and commands that don't modify the project:

- `Read(**)`, `Glob`, `Grep`, `Task`
- Read-only git: `git status`, `git log`, `git diff`, `git branch`, `git remote`, `git show`
- Read-only shell: `ls`, `cat`, `head`, `tail`, `wc`, `find`, `du`, `df`, `file`, `which`, `echo`, `pwd`, `tree`, `diff`
- Network reads: `curl`, `wget`
- Python: `python`, `python3`
- Conda/Mamba info: `conda activate/deactivate/env list/list/info`, `mamba activate/deactivate/env list/list/info`
- Package info: `pip list`, `pip show`

## Ask for confirmation

Commands that modify files, packages, or git state:

- `Edit(**)`, `Write(**)`
- Mutating git: `git push`, `git commit`, `git checkout`, `git merge`, `git rebase`, `git reset`, `git stash`, `git add`
- Package management: `conda install/create/remove/env create/env remove/update`, `mamba install/create/remove/env create/env remove/update`, `pip install`, `pip uninstall`
- File operations: `cp`, `mv`, `rm`, `mkdir`, `rsync`
- `chmod`
- `WebFetch`

## Deny

Sensitive file access and destructive commands:

- Reading/editing sensitive files: `.env`, `.env.*`, `.ssh/**`, `.netrc`, `*credentials*`, `*secret*`, `*token*`, `*.pem`, `*.key`, `.aws/**`
- Destructive commands: `rm -rf /`, `sudo`, `su`, `shutdown`, `reboot`, `dd if=`
- Network probing: `ssh`, `nc`, `netcat`, `nmap`
- Process killing: `kill -9`, `killall`, `pkill`
