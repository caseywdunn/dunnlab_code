---
name: dunnlab-hpc
description: >
  YCRC HPC cluster reference for the Dunn Lab. Use when writing SLURM
  batch scripts, configuring job resources, managing storage, or running
  analyses on Bouchet, McCleary, or Misha clusters. Covers partitions,
  storage, job scheduling, and cluster-specific details.
---

# YCRC HPC Clusters

The Dunn Lab runs computationally intensive analyses on Yale Center for Research Computing (YCRC) clusters. Full documentation: <https://docs.ycrc.yale.edu/>

**Bouchet is the lab's primary cluster.** McCleary is retained only for YCGA raw sequence data work.

## Cluster overview

| Cluster | Focus | Status | SSH | OOD Portal |
|---------|-------|--------|-----|------------|
| **Bouchet** | General HPC (successor to Grace & McCleary) | Active — primary cluster | `bouchet.ycrc.yale.edu` | `ood-bouchet.ycrc.yale.edu` |
| **McCleary** | YCGA sequencing & CryoEM | **YCGA-only** — non-YCGA work has moved to Bouchet | `mccleary.ycrc.yale.edu` | `ood-mccleary.ycrc.yale.edu` |
| **Misha** | Wu Tsai Institute (neuroscience & data science) | Active | `misha.ycrc.yale.edu` | `ood-misha.ycrc.yale.edu` |
| **Hopper** | Regulated/sensitive data (incl. NIH Controlled Access) | Active | — | — |
| **Grace** | Former general HPC | **Retired** — decommissioned in the 2026 migration | — | — |

Request accounts at <https://research.computing.yale.edu/account-request>. New McCleary accounts are only approved for groups using YCGA resources, CryoEM resources, or dedicated nodes.

Transfer nodes: `transfer-bouchet.ycrc.yale.edu`, `transfer-mccleary.ycrc.yale.edu`. For large or cross-cluster transfers, YCRC recommends [Globus](https://docs.ycrc.yale.edu/data/globus/).

## Login node policy

**Never run heavy computation on login nodes.** The following lightweight tasks are acceptable on login nodes:

- Snakemake orchestration (dispatching jobs to SLURM)
- Git operations
- Conda environment management
- File inspection, editing scripts
- Small interactive commands (`wc`, `head`, `ls`, etc.)

Everything else must be submitted as a SLURM job.

---

## Bouchet

Docs: <https://docs.ycrc.yale.edu/clusters/bouchet/> · Getting started: <https://docs.ycrc.yale.edu/clusters/bouchet_getting_started/>

Bouchet is hosted at MGHPCC and is where all HPC growth and refreshes are deployed. Compute is a mix of Intel Emerald Rapids (Xeon 8562Y, 64 cores / 990 GiB) and AMD Turin (EPYC 9575F, 128 cores / 2,251 GiB; EPYC 9655, 192 cores / 1,487 GiB) nodes. GPUs span RTX 5000 Ada, A40, L40S, H100, H200, B200, and RTX PRO 6000 Blackwell.

### Bouchet account and path conventions

Bouchet differs from the older clusters in ways that break copied scripts:

- Your **primary group is your NetID**; PI groups are `pi_<netid>` (not the PI's last name). Check with `groups` and `slurm_checkup.sh`.
- Project and scratch live under `/nfs/roberts/` on the all-flash **Roberts** filesystem. **There is no GPFS and no `/vast/palmer`** — paths like `/gpfs/gibbs/project` and `~/palmer_scratch` do not exist here. Disable any GPFS-specific optimizations in tools.
- **Scratch is purged at 30 days on Bouchet**, not the 60 days you may be used to from Grace and McCleary. Move anything you want to keep to project storage.
- Home symlinks are `~/project_pi_<netid>` and `~/scratch_pi_<netid>` (not `~/project` / `~/palmer_scratch`).
- Software is built against the 2022b and 2024a toolchains only.
- Conda environments **cannot be copied** from Grace/McCleary — rebuild them, or migrate with `conda-pack`.

Run `mydirectories` to print your actual paths and `getquota` to check usage.

### Bouchet partitions

Public partitions (private `priority*`, `pi_*`, and `education*` partitions are excluded). Verify against live state with `sinfo`.

| Partition | Max Time | Nodes | CPUs/Node | RAM/Node | Per-user limits |
|-----------|----------|-------|-----------|----------|-----------------|
| **day** | 1 day | ~110 | 64 / 128 / 192 | 990 / 2,251 / 1,487 GiB | 1,000 CPUs, 15 TiB mem — **default partition** |
| **devel** | 6 hours | 5 | 64 / 192 | 990 / 1,487 GiB | 4 CPUs, 60 GiB, 2 jobs |
| **week** | 7 days | 14 | 128 | 2,251 GiB | 96 CPUs, 1.5 TiB mem |
| **bigmem** | 1 day | 4 | 64 | 4,014 GiB | 128 CPUs, 8 TiB mem |
| **mpi** | 2 days | 60 | 64 | 487 GiB | 48 nodes, 10 jobs |
| **gpu** | 2 days | 29 | 48 | 479–976 GiB | 16 GPUs, 12 jobs |
| **gpu_h100** | 2 days | 15 | 48 | 976 GiB | 16 GPUs, 12 jobs |
| **gpu_h200** | 2 days | 9 | 48 | 1,995 GiB | 16 GPUs, 6 jobs |
| **gpu_b200** | 2 days | 7 | 128 | 2,251 GiB | 16 GPUs, 6 jobs |
| **gpu_rtx6000** | 2 days | 7 | 128 | 2,251 GiB | 16 GPUs, 16 jobs |
| **gpu_devel** | 6 hours | 6 | 48 / 128 | 479–2,251 GiB | 2 GPUs, 1 job |
| **scavenge** | 1 day | 177 | 32–192 | 487–2,251 GiB | Preemptable; idle private nodes |
| **scavenge_gpu** | 1 day | 70 | 32–128 | 488–2,251 GiB | Preemptable GPU nodes |

### Bouchet GPUs

Request GPUs by type, not just count, so you land on hardware that fits the job:

| GPU type | SLURM name | vRAM | Per node | Partition |
|----------|-----------|------|----------|-----------|
| NVIDIA RTX 5000 Ada | `rtx_5000_ada` | 32 GB | 4 | `gpu`, `gpu_devel` |
| NVIDIA A40 | `a40` | 48 GB | 4 | `gpu` |
| NVIDIA L40S | `l40s` | 48 GB | 4 | `gpu` |
| NVIDIA H100 | `h100` | 80 GB | 4 | `gpu_h100`, `gpu_devel` |
| NVIDIA H200 | `h200` | 141 GB | 8 | `gpu_h200`, `gpu_devel` |
| NVIDIA RTX PRO 6000 Blackwell | `rtx_pro_6000_blackwell` | 96 GB | 8 | `gpu_rtx6000`, `gpu_devel` |
| NVIDIA B200 | `b200` | 193 GB | 8 | `gpu_b200`, `gpu_devel` |

Example: `#SBATCH --gpus=h200:1`. List current inventory with `sinfo -e -o "%20P %6D %60G"`.

### Bouchet storage

| Name | Path | Home symlink | Quota | File limit | Backed Up | Purge Policy |
|------|------|--------------|-------|-----------|-----------|--------------|
| Home | `/home/<netid>` | `~/` | 125 GiB/user | 500K | Yes (snapshots >= 2 days) | None |
| Project | `/nfs/roberts/project/pi_<netid>` | `~/project_pi_<netid>` | 4 TiB/group | 5M | Yes (snapshots >= 2 days) | None |
| Scratch | `/nfs/roberts/scratch/pi_<netid>` | `~/scratch_pi_<netid>` | 10 TiB/group | 15M | No | **30-day purge** |
| PI | `/nfs/roberts/pi/<grp>` | — | Purchased | — | Snapshots >= 2 days | None |

No sensitive or regulated data may be stored on Bouchet — use Hopper.

---

## McCleary

Docs: <https://docs.ycrc.yale.edu/clusters/mccleary/> · Decommission plan: <https://docs.ycrc.yale.edu/clusters/grace-mccleary-decommission/>

**McCleary is winding down to a YCGA-only cluster.** The lab retains access for YCGA raw sequence data work; run everything else on Bouchet.

Migration status:

- **Phase 1 (complete)** — groups without dedicated nodes, CryoEM, or YCGA affiliation lost Grace/McCleary access on **June 1, 2026**.
- **Phase 2 (late 2026 / early 2027)** — non-YCGA workloads and data belonging to YCGA-affiliated groups move to Bouchet. Anything you want to keep off McCleary must be transferred by then.
- **Phase 3 (late 2026 / early 2027)** — newer commons and dedicated nodes relocate to Bouchet; Grace shuts down. McCleary persists as YCGA-only for the remaining life of YCGA-owned hardware.

NIH Controlled Access Data **cannot** move to Bouchet — it must go to Hopper.

Hardware: heterogeneous Intel Xeon (Skylake, Cascade Lake, Ice Lake), 163–3,960 GiB per node. GPUs include A100 (40/80 GB), V100, A5000, RTX 3090, RTX 5000, L40S.

### McCleary partitions

| Partition | Max Time | Max CPUs/User | Max Mem/User | Max GPUs/User |
|-----------|----------|---------------|--------------|---------------|
| **day** | 1 day | 256 | 3,000 GiB | — |
| **devel** | 6 hours | 4 | 32 GiB | — |
| **week** | 7 days | 192 | 2,949 GiB | — |
| **long** | 28 days | 36 | — | — |
| **gpu** | 2 days | — | — | 12 |
| **gpu_devel** | 6 hours | 10 | — | 2 |
| **bigmem** | 1 day | 32 | 3,960 GiB | — |
| **scavenge** | 1 day | 1,000 | 20,000 GiB | — |
| **scavenge_gpu** | 1 day | — | — | 64 |
| **ycga** | — | — | — | Submit YCGA work here to avoid CPU charges |

### McCleary storage

| Name | Path | Quota | Backed Up | Purge Policy |
|------|------|-------|-----------|--------------|
| Home | `~/` | 125 GiB, 500K files | Yes (backed up + snapshotted) | None |
| Project | `~/project` (`/gpfs/gibbs/project`) | 4 TiB/group, 5M files | Snapshotted | None |
| Scratch | `~/palmer_scratch` (`/vast/palmer/scratch`) | 10 TiB/group, 15M files | No | **60-day purge** |
| PI | `/gpfs/gibbs/pi/<grp>` or `/vast/palmer/pi/<grp>` | Purchased | Varies | None |

Check quotas: `getquota` | List paths: `mydirectories`

### McCleary defaults

Unless overridden: 1 hour walltime, 1 node, 1 task, 1 CPU, 5120 MB memory per CPU.

---

## Misha

Docs: <https://docs.ycrc.yale.edu/clusters/misha/>

The lab rarely uses Misha; the tables below have not been re-verified as recently as the Bouchet ones. Confirm against `sinfo` and `getquota` before relying on them.

Hardware: Intel Sapphire Rapids and Emerald Rapids (6458, 6542, 6442, 6326). Standard nodes: 64 CPUs, 479 GiB. GPUs: H100 (80 GB), H200 (141 GB), A100 (80 GB), A40 (48 GB), L40S (48 GB).

### Misha partitions

| Partition | Max Time | Nodes | CPUs/Node | RAM/Node | Per-User Limits |
|-----------|----------|-------|-----------|----------|-----------------|
| **day** | 1 day | 18 | 64 | 479 GiB | 512 CPUs, 20 TiB mem |
| **devel** | 6 hours | 2 | 64 | 479 GiB | 10 CPUs, 70 GiB |
| **week** | 7 days | 6 | 64 | 479 GiB | 128 CPUs, 1,280 GiB |
| **gpu** | 2 days | 31 | 32-48 | 975-1000 GiB | 192 CPUs, 18 GPUs |
| **gpu_devel** | 6 hours | 2 | 32 | 975 GiB | 4 CPUs, 1 GPU |
| **bigmem** | 1 day | 2 | 64 | 1,991 GiB | 64 CPUs, 2 TiB mem |

### Misha storage

| Name | Path | Quota | Backed Up | Purge Policy |
|------|------|-------|-----------|--------------|
| Home | `/gpfs/radev/home` | 125 GiB, 500K files | Snapshots >= 2 days | None |
| Project | `/gpfs/radev/project` | 1 TiB/group, 5M files | Snapshots >= 2 days | None |
| Scratch | `/gpfs/radev/scratch` | 10 TiB/group, 15M files | No | **60-day purge** |

---

## SLURM job scheduling

Full docs: <https://docs.ycrc.yale.edu/clusters-at-yale/job-scheduling/>

### Batch script template

```bash
#!/bin/bash
#SBATCH --job-name=my_job
#SBATCH --partition=day
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=5G
#SBATCH --mail-type=ALL
#SBATCH --output=logs/slurm-%j.out

module reset
module load miniconda
conda activate myenv
<command>
```

**Critical**: No space between `#` and `SBATCH` — otherwise the directive is ignored.

**Use `module reset`, not `module purge`.** `module reset` restores the sticky `StdEnv` module, which sets `CONDA_ENVS_PATH`, `SLURM_HINT=nomultithread`, the default `salloc` partition, and the `/apps/bin` PATH entry. `module purge` strips `StdEnv` and leaves a broken environment.

### `batch.sh` conventions

Every computationally intensive script or pipeline should include a companion `batch.sh` SLURM submission script in the same directory. This makes it clear how to run the code and with what resources.

- Name the file `batch.sh` and place it alongside the script it runs. If there are multiple stages, use separate scripts (`batch_align.sh`, `batch_assemble.sh`, etc.).
- Set `--job-name` to something descriptive (e.g., the analysis name or script name).
- Direct SLURM output to `logs/` (e.g., `--output=logs/slurm-%j.out`) — ensure the directory exists before submission.
- Include `module reset` before loading modules to avoid environment conflicts.
- Size resource requests to match actual needs — check with `jobstats` after initial runs and adjust.
- For array jobs processing many samples, use `--array` and document the expected input format.
- Document how to launch jobs in the project README. At minimum, include the submission command (e.g., `sbatch batch.sh`) and any prerequisites such as creating the `logs/` directory or activating a conda environment beforehand.

### Common directives

| Directive | Short | Default | Purpose |
|-----------|-------|---------|---------|
| `--job-name` | `-J` | — | Job identification |
| `--time` | `-t` | 1 hour | Walltime (`D-HH:MM:SS`) |
| `--partition` | `-p` | `day` | Target partition |
| `--nodes` | `-N` | 1 | Compute nodes |
| `--ntasks` | `-n` | 1 | MPI task count |
| `--cpus-per-task` | `-c` | 1 | Cores per task (for threading) |
| `--mem-per-cpu` | — | 5 GiB | RAM per CPU |
| `--gpus` | `-G` | 0 | GPU count (`--gpus=<type>:<n>`) |
| `--output` | `-o` | — | Output file (`%j` = job ID) |
| `--mail-type` | — | — | Email notifications (`ALL`, `FAIL`, etc.) |

### GPU jobs

```bash
#!/bin/bash
#SBATCH --partition=gpu_h200
#SBATCH --gpus=h200:1
#SBATCH --time=8:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=5G

module reset
module load CUDA miniconda
conda activate myenv
python train.py
```

GPUs must be explicitly requested with `--gpus`; none are allocated by default. On Bouchet, match the partition to the GPU type — see the Bouchet GPU table above.

### Interactive jobs

```bash
salloc -p devel -t 2:00:00 --mem=8G
```

`StdEnv` sets `SALLOC_PARTITION=devel`, so `salloc` targets `devel` unless you pass `-p`. Add `--x11` for graphical forwarding (requires X11 setup). Wrap interactive sessions in `tmux` so a dropped connection does not kill the job.

### Job monitoring

| Command | Purpose |
|---------|---------|
| `squeue --me` | List your running/pending jobs |
| `sacct -j <id>` | Job status and resource usage |
| `jobstats <id>` | Efficiency metrics (CPU/memory utilization) |
| `scancel <id>` | Cancel a job |
| `sbatch --test-only script.sh` | Estimate queue start time without submitting |
| `slurm_checkup.sh` | Show your SLURM accounts and group membership |

### Job arrays and bulk submission

For many similar jobs, use **job arrays** (`--array`) or **Dead Simple Queue** rather than looping over `sbatch`. YCRC enforces job submission rate limits, and a submission loop will trip them.

```bash
module load dSQ
dsq --job-file joblist.txt --mem-per-cpu 4g -t 2:00:00 --submit
dsqa -j <arrayjobid>   # post-hoc report, regenerate failed tasks
```

### Resource efficiency

Always check resource usage with `jobstats` after jobs complete. Request only what you need — wasteful allocations slow scheduling for everyone. Match `--cpus-per-task` to the actual thread count your tool uses. Match `--mem-per-cpu` to observed memory usage.

---

## Snakemake + SLURM integration

Snakemake with `--executor slurm` (via `snakemake-executor-plugin-slurm`) submits each rule as an independent SLURM job. Snakemake itself runs on the login node as a lightweight orchestrator — this is acceptable.

### Setup

```bash
module load miniconda
conda create -n snakemake -c conda-forge -c bioconda snakemake snakemake-executor-plugin-slurm
conda activate snakemake
```

### Running

```bash
# Dry run first
snakemake -n --executor slurm

# Execute
snakemake --executor slurm --jobs 50
```

### Per-rule resources in Snakefile

```python
rule align:
    resources:
        slurm_partition="day",
        runtime=240,          # minutes
        mem_mb=20000,
        cpus_per_task=4,
        slurm_extra="'--mail-type=FAIL'"
```

For GPU rules, add: `slurm_partition="gpu", slurm_extra="'--gpus=rtx_5000_ada:1'"`

### Snakemake profile (recommended)

Create `~/.config/snakemake/slurm/config.yaml`:

```yaml
executor: slurm
jobs: 50
default-resources:
  slurm_partition: day
  runtime: 60
  mem_mb: 5000
  cpus_per_task: 1
latency-wait: 120
```

Then run: `snakemake --profile slurm`

### Use tmux for long-running orchestration

```bash
tmux new -s pipeline
module load miniconda
conda activate snakemake
snakemake --executor slurm --jobs 50
# Ctrl-b d to detach; tmux attach -t pipeline to reconnect
```

---

## Conda environment management

Prefer **conda/mamba** over pip. Always use **conda-forge** as the primary channel. Add **bioconda** when bioinformatics tools are needed.

```bash
module load miniconda

# Create
conda create -n myenv -c conda-forge python=3.11 <packages>

# From file
conda env create -f environment.yml

# Export
conda env export > environment.yml

# Add package
conda install -c conda-forge <pkg>

# Pip fallback (only if not in conda-forge)
pip install <pkg>
```

Store environments in your project directory or home — **never in scratch** (on Bouchet they will be purged after 30 days). Environments are not portable between clusters: rebuild on Bouchet, or migrate with `conda-pack`.

---

## Important policies

- **Scratch purge**: Scratch files are automatically deleted once they exceed the age limit — **30 days on Bouchet**, 60 days on McCleary. Do not artificially extend file modification times to circumvent the policy.
- **Sensitive data**: No sensitive or regulated data on any cluster except Hopper. NIH Controlled Access Data must go to Hopper, not Bouchet.
- **Max interactive apps**: 4 concurrent OOD interactive instances per user.
- **Job rate limits**: YCRC enforces submission rate limits — use job arrays or `dsq` instead of submission loops.
- **Module system**: Use `module reset` then `module load` for software. Run `module avail` to see available packages.
- **AI coding agents**: YCRC does not formally support coding agents on the clusters and warns about data exposure, credential leakage, and destructive actions taken with your permissions. See <https://docs.ycrc.yale.edu/ai/aicodingtools/> and use restrictive Claude Code permissions (`assets/settings.json` in this repo). YCRC also documents connecting Claude Science to a cluster by SSH tunnel to a **compute node, not a login node**.
- **Paid storage**: YCRC cannot accept new or increased paid storage allocations on Bouchet, Grace, or McCleary; availability may return in late 2026.
