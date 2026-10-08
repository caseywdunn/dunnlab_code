---
title: Computing at Yale
nav_order: 17
---

# Computing at Yale

Everything up to this point applies anywhere. This chapter does not: it covers Yale's research computing environment and how to use Claude Code or Codex with it safely.

Start with [Working Across Computers](working-across-computers.md) for the general pattern: SSH, persistent sessions, file movement, and keeping the agent plane separate from scheduled computation.

If you are reading this from another institution, the useful part is the shape rather than the specifics — most universities have an equivalent of the policies and constraints below, and the reasoning transfers even though the hostnames do not.

## High performance computing

We make extensive use of Yale's High Performance Computing (HPC) resources at the [Yale Center for Research Computing](https://docs.ycrc.yale.edu/clusters/). YCRC maintains detailed [documentation](https://docs.ycrc.yale.edu/clusters-at-yale/) on using the clusters, including the [SLURM](https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/) scheduler you will use to launch and run analyses.

Most interaction with the clusters happens through [Open OnDemand](https://docs.ycrc.yale.edu/clusters-at-yale/access/ood/#remote-desktop), YCRC's web portal.

## Coding agents and the clusters

[Agents on shared clusters](working-across-computers.md#agents-on-shared-clusters) covers the general precautions: start with restrictive permissions, check that the sandbox works, and keep heavy work off login nodes. This section adds what is specific to Yale.

### Follow YCRC policy first

YCRC **does not formally support** AI coding agents on the clusters, and publishes [guidance on the risks](https://docs.ycrc.yale.edu/ai/aicodingtools/) — data exposure, credential leakage, unauthorized actions taken with your permissions, and execution of code the agent generated or downloaded. Read it. These tools are new and the policy may change faster than this page does; where the two disagree, YCRC wins.

YCRC also documents connecting Claude Science to a cluster over an SSH tunnel to a **compute node, not a login node**. That product-specific example does not make Claude Code the default; the same policy and data-exposure questions apply when Codex reaches the cluster locally or through SSH.

### A settings file for Bouchet

For Claude Code, [`assets/settings.json`](https://github.com/caseywdunn/dunnlab_code/blob/main/assets/settings.json) is a full working example built for Bouchet. Place it in `~/.claude/` on the cluster. It starts in plan mode, allows read-only inspection and job monitoring freely, requires confirmation for file modifications and network access, and denies destructive system operations outright.

The cluster quick reference (partitions, storage paths, SLURM templates, and conda workflow) belongs in shared `AGENTS.md` instructions so both agents receive it. The Claude settings example also includes a copy in its comment blocks, and the `dunnlab-hpc` skill carries the same reference for Claude Code.

This repository's [tmux configuration and cheat sheet](https://github.com/caseywdunn/dunnlab_code/tree/main/assets/tmux) is set up for long orchestration runs on the login nodes, including clipboard support that works over SSH.
