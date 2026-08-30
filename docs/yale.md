---
title: Computing at Yale
nav_order: 13
---

# Computing at Yale

Everything up to this point applies anywhere. This chapter does not: it covers Yale's research computing environment and how to use Claude Code or Codex with it safely.

Start with [Working Across Computers](working-across-computers.md) for the general pattern: SSH, persistent sessions, file movement, and keeping the control plane separate from scheduled computation.

If you are reading this from another institution, the useful part is the shape rather than the specifics — most universities have an equivalent of the policies and constraints below, and the reasoning transfers even though the hostnames do not.

## High performance computing

We make extensive use of Yale's High Performance Computing (HPC) resources at the [Yale Center for Research Computing](https://docs.ycrc.yale.edu/clusters/). YCRC maintains detailed [documentation](https://docs.ycrc.yale.edu/clusters-at-yale/) on using the clusters, including the [SLURM](https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/) scheduler you will use to launch and run analyses.

Most interaction with the clusters happens through [Open OnDemand](https://docs.ycrc.yale.edu/clusters-at-yale/access/ood/#remote-desktop), YCRC's web portal.

## Coding agents and the clusters

A cluster is a shared, powerful, and largely irreversible environment. The stakes are different from your laptop: you can create work for cluster maintainers and deny other people access, you can delete or leak a colleague's data, and you can silently modify your own in ways you will not notice until much later.

### Follow YCRC policy first

YCRC **does not formally support** AI coding agents on the clusters, and publishes [guidance on the risks](https://docs.ycrc.yale.edu/ai/aicodingtools/) — data exposure, credential leakage, unauthorized actions taken with your permissions, and execution of code the agent generated or downloaded. Read it. These tools are new and the policy may change faster than this page does; where the two disagree, YCRC wins.

YCRC also documents connecting Claude Science to a cluster over an SSH tunnel to a **compute node, not a login node**. That product-specific example does not make Claude Code the default; the same policy and data-exposure questions apply when Codex reaches the cluster locally or through SSH.

### Use restrictive permissions

Because of the stakes above, run with tighter permissions on a cluster than you would locally.

Start either harness with read-only access and explicit approvals, then broaden access only for actions the environment and policy permit. For Codex, a conservative starting command is:

```bash
codex --sandbox read-only --ask-for-approval on-request
```

For Claude Code, [`assets/settings.json`](https://github.com/caseywdunn/dunnlab_code/blob/main/assets/settings.json) is a full working example built for Bouchet. Place it in `~/.claude/` on the cluster. It starts in plan mode, allows read-only inspection and job monitoring freely, requires confirmation for file modifications and network access, and denies destructive system operations outright.

The same cluster quick reference—partitions, storage paths, SLURM templates, and conda workflow—belongs in shared `AGENTS.md` instructions so both agents receive it. The Claude settings example also includes a copy in its comment blocks.

See [Managing Security](managing-security.md) for what the permission rules mean and how they are evaluated.

### Check whether the sandbox works before trusting it

Permission and approval rules constrain what a harness will run. A functioning sandbox constrains what a running command *can reach*, which is the guarantee you actually want on shared storage—a Python script the agent runs is inside it too.

In Claude Code, run `/sandbox` and check whether a Dependencies tab appears. Its sandbox needs `bubblewrap`, `socat`, and unprivileged user namespaces, and shared systems commonly restrict the last of these. **When it cannot start, Claude Code warns and runs commands unsandboxed**, unless `sandbox.failIfUnavailable` is set to `true`.

In Codex, use `/permissions` to inspect the active sandbox and writable roots. For either harness, test that a deliberately out-of-scope read or write is actually blocked before trusting the boundary. If the required isolation is unavailable, keep the agent off the cluster and use the [local-control, remote-compute](working-across-computers.md#let-a-local-agent-control-remote-computation) arrangement instead.

### Never run heavy work on a login node

This predates AI tooling but is easier to violate with it, because an agent will happily run whatever gets the answer fastest. Lightweight orchestration is fine on a login node — dispatching SLURM jobs, git operations, conda environment management, inspecting files. Everything else belongs in a submitted job.

If you are running a long orchestration such as Snakemake on a login node, wrap it in `tmux` so a dropped connection does not kill it. This repository ships a [shared tmux configuration and cheat sheet](https://github.com/caseywdunn/dunnlab_code/tree/main/assets/tmux) set up for exactly that, including clipboard support that works over SSH.
