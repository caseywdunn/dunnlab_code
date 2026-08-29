---
title: Computing at Yale
nav_order: 11
---

# Computing at Yale

Everything up to this point applies anywhere. This chapter does not: it covers Yale's research computing environment and how to use Claude Code on it safely.

If you are reading this from another institution, the useful part is the shape rather than the specifics — most universities have an equivalent of the policies and constraints below, and the reasoning transfers even though the hostnames do not.

## High performance computing

We make extensive use of Yale's High Performance Computing (HPC) resources at the [Yale Center for Research Computing](https://docs.ycrc.yale.edu/clusters/). YCRC maintains detailed [documentation](https://docs.ycrc.yale.edu/clusters-at-yale/) on using the clusters, including the [SLURM](https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/) scheduler you will use to launch and run analyses.

Most interaction with the clusters happens through [Open OnDemand](https://docs.ycrc.yale.edu/clusters-at-yale/access/ood/#remote-desktop), YCRC's web portal.

## Claude Code on the clusters

A cluster is a shared, powerful, and largely irreversible environment. The stakes are different from your laptop: you can create work for cluster maintainers and deny other people access, you can delete or leak a colleague's data, and you can silently modify your own in ways you will not notice until much later.

### Follow YCRC policy first

YCRC **does not formally support** AI coding agents on the clusters, and publishes [guidance on the risks](https://docs.ycrc.yale.edu/ai/aicodingtools/) — data exposure, credential leakage, unauthorized actions taken with your permissions, and execution of code the agent generated or downloaded. Read it. These tools are new and the policy may change faster than this page does; where the two disagree, YCRC wins.

YCRC also documents connecting Claude Science to a cluster over an SSH tunnel to a **compute node, not a login node**.

### Use restrictive permissions

Because of the stakes above, run with tighter permissions on a cluster than you would locally.

[`assets/settings.json`](https://github.com/caseywdunn/dunnlab_code/blob/main/assets/settings.json) in this repository is a full working example built for Bouchet. Place it in `~/.claude/` on the cluster. It starts in plan mode, allows read-only inspection and job monitoring freely, requires confirmation for file modifications and network access, and denies destructive system operations outright.

It also carries a cluster quick reference in its comment blocks — partitions, storage paths, SLURM templates, conda workflow — so Claude has that context in every session on the cluster.

See [Managing Security](managing-security.md) for what the permission rules mean and how they are evaluated.

### Check whether the sandbox works before trusting it

Permission rules constrain what Claude *decides* to run. The [Bash sandbox](managing-security.md#the-bash-sandbox) constrains what a running command *can reach*, which is the guarantee you actually want on shared storage — a Python script Claude runs is inside it too.

Run `/sandbox` once on the cluster and check whether a Dependencies tab appears. The sandbox needs `bubblewrap`, `socat`, and unprivileged user namespaces, and shared systems commonly restrict the last of these. **When it cannot start, Claude Code warns and runs your commands unsandboxed** — so a working sandbox is something to confirm rather than assume. Set `sandbox.failIfUnavailable` to `true` if you would rather that be a hard error.

### Never run heavy work on a login node

This predates AI tooling but is easier to violate with it, because an agent will happily run whatever gets the answer fastest. Lightweight orchestration is fine on a login node — dispatching SLURM jobs, git operations, conda environment management, inspecting files. Everything else belongs in a submitted job.

If you are running a long orchestration such as Snakemake on a login node, wrap it in `tmux` so a dropped connection does not kill it. This repository ships a [shared tmux configuration and cheat sheet](https://github.com/caseywdunn/dunnlab_code/tree/main/assets/tmux) set up for exactly that, including clipboard support that works over SSH.
