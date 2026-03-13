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

## Cluster overview

| Cluster | Focus | Status | SSH | OOD Portal |
|---------|-------|--------|-----|------------|
| **Bouchet** | General HPC (successor to Grace & McCleary) | Active — primary cluster | `bouchet.ycrc.yale.edu` | `ood-bouchet.ycrc.yale.edu` |
| **McCleary** | School of Medicine & life sciences | **Decommissioning 2026** — migrate to Bouchet | `mccleary.ycrc.yale.edu` | `ood-mccleary.ycrc.yale.edu` |
| **Misha** | Wu Tsai Institute (neuroscience & data science) | Active | `misha.ycrc.yale.edu` | `ood-misha.ycrc.yale.edu` |

Request accounts at <https://research.computing.yale.edu/account-request>.

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

Docs: <https://docs.ycrc.yale.edu/clusters/bouchet/>

Hardware: ~10,000 direct-liquid-cooled cores, 80 NVIDIA H200 GPUs, 48 NVIDIA RTX 5000 ADA GPUs. Standard nodes have 64 cores and 990 GiB RAM; bigmem nodes have 4 TiB RAM.

### Bouchet partitions

| Partition | Max Time | Nodes | CPUs/Node | RAM/Node | Notes |
|-----------|----------|-------|-----------|----------|-------|
| **day** | 1 day | 83 | 64 | 990 GiB | Default partition |
| **devel** | 6 hours | 4 | 64 | 990 GiB | Interactive; max 2 jobs/user |
| **week** | 7 days | 4 | 64 | 990 GiB | Extended runtime |
| **gpu** | 2 days | 8 | 48 | 479 GiB | RTX 5000 ADA (4/node, 32 GB each) |
| **gpu_h200** | 2 days | 9 | 48 | 1,995 GiB | H200 (8/node, 141 GB each) |
| **gpu_devel** | 6 hours | 5 | 48 | varies | 1 GPU/user max |
| **bigmem** | 1 day | 4 | 64 | 4,014 GiB | High-memory |
| **mpi** | 2 days | 60 | 64 | 487 GiB | Tightly-coupled parallel |
| **scavenge** | preemptable | 94 | 64 | 990 GiB | Idle private nodes |

### Bouchet storage

| Name | Path | Quota | Backed Up | Purge Policy |
|------|------|-------|-----------|--------------|
| Home | `/home` | 125 GiB/user | Yes (snapshots >= 2 days) | None |
| Project | `/nfs/roberts/project` | 4 TiB/group | Yes (snapshots >= 2 days) | None |
| Scratch | `/nfs/roberts/scratch` | 10 TiB/group | No | **60-day purge** |
| PI | `/nfs/roberts/pi` | Variable | Snapshots >= 2 days | None |

---

## McCleary

Docs: <https://docs.ycrc.yale.edu/clusters/mccleary/>

**McCleary is being decommissioned in 2026.** Plan new work on Bouchet. McCleary serves School of Medicine and life science researchers.

Hardware: Intel 8358 (64 CPUs, 983 GiB) and Intel 6240 (36 CPUs, 180 GiB) nodes. GPU nodes include A5000, A100, RTX3090, and RTX5000 cards.

### McCleary partitions

| Partition | Max Time | Max CPUs/User | Notes |
|-----------|----------|---------------|-------|
| **day** | 1 day | 256 | Default partition |
| **devel** | 6 hours | 4 | Interactive debugging |
| **week** | 7 days | 192 | Extended runtime |
| **long** | 28 days | 36 | Very long jobs |
| **gpu** | 2 days | — (12 GPUs/user) | A5000, A100 |
| **gpu_devel** | 6 hours | 10 (2 GPUs/user) | GPU testing |
| **bigmem** | 1 day | — | Up to 3,960 GiB/node |
| **scavenge** | 1 day | 1000 | Preemptable |
| **scavenge_gpu** | 1 day | — (64 GPUs/user) | Preemptable GPU |
| **ycga** | — | — | YCGA work; exempt from compute charges |

### McCleary storage

| Name | Path | Quota | Backed Up | Purge Policy |
|------|------|-------|-----------|--------------|
| Home | `~/` | 125 GiB, 500K files | Yes (backed up + snapshotted) | None |
| Project | `~/project` (`/gpfs/gibbs/project`) | 4 TiB/group | Snapshotted | None |
| Scratch | `~/palmer_scratch` (`/vast/palmer/scratch`) | Large | No | **60-day purge** |
| PI | `/gpfs/gibbs/pi/<grp>` or `/vast/palmer/pi/<grp>` | Purchased | Varies | None |

Check quotas: `getquota` | List paths: `mydirectories`

### McCleary defaults

Unless overridden: 1 hour walltime, 1 node, 1 task, 1 CPU, 5120 MB memory per CPU.

---

## Misha

Docs: <https://docs.ycrc.yale.edu/clusters/misha/>

Hardware: Intel Xeon (6458, 6542, 6442, 6326) with AVX-512. Standard nodes: 64 CPUs, 479-491 GiB. GPU nodes: H100, H200, A100, A40, L40S (4 GPUs/node, 48-80 GB VRAM each).

### Misha partitions

| Partition | Max Time | Nodes | CPUs/Node | RAM/Node | Per-User Limits |
|-----------|----------|-------|-----------|----------|-----------------|
| **day** | 1 day | 18 | 64 | 479 GiB | 512 CPUs, 20 TiB mem |
| **devel** | 6 hours | 2 | 64 | 479 GiB | Interactive |
| **week** | 7 days | 6 | 64 | 479 GiB | 128 CPUs, 1.28 TiB mem |
| **gpu** | 2 days | 32 | 32-48 | 975-1000 GiB | 192 CPUs, 18 GPUs |
| **gpu_devel** | 6 hours | 2 | 32 | 975 GiB | GPU testing |
| **bigmem** | 1 day | 2 | 64 | 1,991 GiB | High-memory |

### Misha storage

| Name | Path | Quota | Backed Up | Purge Policy |
|------|------|-------|-----------|--------------|
| Home | `/home` | 125 GiB, 500K files | Snapshots >= 2 days | None |
| Project | `/gpfs/radev/project` | 1-4 TiB/group, 5M files | Snapshots >= 2 days | None |
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
#SBATCH --output=slurm-%j.out

module purge
module load miniconda
conda activate myenv
<command>
```

**Critical**: No space between `#` and `SBATCH` — otherwise the directive is ignored.

### `batch.sh` conventions

Every computationally intensive script or pipeline should include a companion `batch.sh` SLURM submission script in the same directory. This makes it clear how to run the code and with what resources.

- Name the file `batch.sh` and place it alongside the script it runs. If there are multiple stages, use separate scripts (`batch_align.sh`, `batch_assemble.sh`, etc.).
- Set `--job-name` to something descriptive (e.g., the analysis name or script name).
- Direct SLURM output to `logs/` (e.g., `--output=logs/slurm-%j.out`) — ensure the directory exists before submission.
- Include `module purge` before loading modules to avoid environment conflicts.
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
| `--gpus` | `-G` | 0 | GPU count |
| `--output` | `-o` | — | Output file (`%j` = job ID) |
| `--mail-type` | — | — | Email notifications (`ALL`, `FAIL`, etc.) |

### GPU jobs

```bash
#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --time=8:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=5G

module purge
module load CUDA miniconda
conda activate myenv
python train.py
```

GPUs must be explicitly requested with `--gpus`. On Bouchet, use `--partition=gpu_h200` for H200 GPUs.

### Interactive jobs

```bash
salloc -p devel -t 2:00:00 --mem=8G
```

Add `--x11` for graphical forwarding (requires X11 setup). Interactive jobs are typically only allowed on `devel` partitions.

### Job monitoring

| Command | Purpose |
|---------|---------|
| `squeue --me` | List your running/pending jobs |
| `sacct -j <id>` | Job status and resource usage |
| `jobstats <id>` | Efficiency metrics (CPU/memory utilization) |
| `scancel <id>` | Cancel a job |
| `sbatch --test-only script.sh` | Estimate queue start time without submitting |

### Job arrays and bulk submission

For many similar jobs, use **job arrays** or **Dead Simple Queue (dsq)** rather than submitting hundreds of individual jobs. Rate limit: **200 job submissions per hour**.

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

For GPU rules, add: `slurm_partition="gpu", slurm_extra="'--gpus=1'"`

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

Store environments in `~/project` or home — **never in scratch** (they will be purged after 60 days).

---

## Important policies

- **Scratch purge**: Files older than 60 days on scratch are automatically deleted. You will receive email notification one week before deletion. Do not artificially extend file modification times to circumvent the policy.
- **Max interactive apps**: 4 concurrent OOD interactive instances per user.
- **Job rate limit**: 200 submissions per hour.
- **Module system**: Use `module load` for software. Run `module avail` to see available packages (300-1000+ depending on cluster).
- **McCleary decommission**: McCleary will be retired in 2026. New projects should target Bouchet.
