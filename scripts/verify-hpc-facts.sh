#!/usr/bin/env bash
# Dump the cluster facts that skills/dunnlab-hpc/SKILL.md asserts, so they can
# be checked against the live system. Run this ON a YCRC cluster login node.
#
#     ./scripts/verify-hpc-facts.sh > hpc-facts-$(hostname -s).txt
#
# READ-ONLY. It runs no jobs, submits nothing, writes nothing outside stdout,
# and touches no shared state. Safe on a login node.
#
# The skill's numbers came from docs.ycrc.yale.edu, not from a cluster. Where
# this output disagrees with the skill, the cluster wins.

set -uo pipefail

sec() { printf '\n\n══ %s %s\n\n' "$1" "$(printf '═%.0s' $(seq 1 $((60 - ${#1}))))"; }
try() { if command -v "$1" >/dev/null 2>&1; then "$@"; else echo "  (command not found: $1)"; fi; }

echo "host:    $(hostname -f 2>/dev/null || hostname)"
echo "cluster: ${SLURM_CLUSTER_NAME:-$(try scontrol show config 2>/dev/null | awk -F= '/ClusterName/{print $2}' | tr -d ' ')}"
echo "date:    $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "user:    $(id -un)"

sec "ACCOUNT AND GROUPS"
# Skill claims: primary group is your NetID; PI groups are pi_<netid>
echo "primary group: $(id -gn)"
echo "all groups:    $(id -Gn)"
echo
try slurm_checkup.sh

sec "STORAGE PATHS AND QUOTAS"
# Skill claims (Bouchet): home /home/<netid> 125 GiB / 500K;
# project /nfs/roberts/project/pi_<netid> 4 TiB / 5M;
# scratch /nfs/roberts/scratch/pi_<netid> 10 TiB / 15M
echo "\$HOME = $HOME  ->  $(readlink -f "$HOME" 2>/dev/null)"
for l in project scratch palmer_scratch project_pi_* scratch_pi_*; do
  for p in "$HOME"/$l; do
    [ -e "$p" ] && printf '%-28s -> %s\n' "~/$(basename "$p")" "$(readlink -f "$p")"
  done
done
echo
try mydirectories
echo
try getquota

sec "SCRATCH PURGE POLICY  <-- the number that matters most"
# Skill claims 30 days on Bouchet, 60 on McCleary. Getting this wrong loses data.
echo "Look for a purge/retention figure in the getquota output above, in the"
echo "login banner, and in any of these if they exist:"
for f in /etc/motd /etc/motd.d/* /apps/README* ; do
  [ -r "$f" ] && { echo "--- $f"; grep -iE 'purge|scratch|[0-9]+ *day' "$f" 2>/dev/null | head -5; }
done
echo
echo "Also check the scratch filesystem's own documentation file, if present:"
for d in "$HOME"/scratch* /nfs/roberts/scratch; do
  [ -d "$d" ] && ls -la "$d"/ 2>/dev/null | grep -iE 'readme|purge|policy' | head -3
done

sec "PARTITIONS  (skill asserts max time, node counts, CPUs, RAM)"
try sinfo -o "%20P %10l %6D %5c %10m %20f" -e

sec "PER-USER LIMITS  (skill asserts CPU/mem/GPU/job caps per partition)"
try sacctmgr show qos format=Name%20,MaxTRESPerUser%40,MaxJobsPU,MaxWall --noheader

sec "GPU INVENTORY  (skill asserts types, SLURM names, vRAM, per-node counts)"
try sinfo -e -o "%20P %6D %5c %10m %40G"

sec "DEFAULTS  (skill asserts 1 hour walltime, 5 GiB/CPU, day partition)"
try scontrol show config 2>/dev/null | grep -iE 'DefMemPerCPU|DefaultTime|MaxTime|SchedulerType' | sed 's/^/  /'
echo "  default partition (marked * by sinfo):"
try sinfo -o "%P" | grep '\*' | sed 's/^/    /'

sec "MODULE SYSTEM  (skill says: module reset, never module purge)"
echo "StdEnv sticky module present?"
try module --version 2>&1 | head -2
( module list 2>&1 | head -10 ) 2>/dev/null || echo "  (module not available in a non-interactive shell — check by hand)"
echo
echo "CONDA_ENVS_PATH = ${CONDA_ENVS_PATH:-(unset — expected to be set by StdEnv)}"
echo "SLURM_HINT      = ${SLURM_HINT:-(unset)}"
echo "SALLOC_PARTITION= ${SALLOC_PARTITION:-(unset — skill says StdEnv sets this to devel)}"

sec "CLAUDE CODE BASH SANDBOX  (docs page claims this often cannot start here)"
for b in bwrap socat; do
  printf '%-8s %s\n' "$b" "$(command -v $b || echo 'NOT INSTALLED')"
done
printf 'unprivileged userns restricted? '
sysctl -n kernel.apparmor_restrict_unprivileged_userns 2>/dev/null || echo "(key absent — likely unrestricted)"
echo "(1 = restricted, so bubblewrap cannot create namespaces and the sandbox will not start)"

sec "DONE"
echo "Send this file back and it can be diffed against skills/dunnlab-hpc/SKILL.md."
