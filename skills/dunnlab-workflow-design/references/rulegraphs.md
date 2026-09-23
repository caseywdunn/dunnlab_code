# Generated rule graphs in analysis READMEs

Prefer a generated SVG from `snakemake --rulegraph` embedded beside the analysis's
launch instructions. Generate it from the actual rules and keep it current with
an executable CI check. A manually redrawn diagram or a regeneration reminder
alone does not provide that check.

## Keep launch, preview, and graph scope aligned

Use the same working directory, Snakefile, scientifically relevant configuration,
and explicit target for execution, dry run, and graph generation. Include settings
supplied by workflow profiles if they affect the graph. Cluster submission options
belong in the launch command/profile, not in a diagram-only job.

For example, adapt these paths and resources to the actual project. All commands
run from the repository root after activating its environment:

```bash
# Preview the selected full analysis.
snakemake all --snakefile workflows/main/Snakefile \
  --configfile config/analysis.yaml --cores 4 --dry-run

# Run the same analysis locally; document the actual HPC command when applicable.
snakemake all --snakefile workflows/main/Snakefile \
  --configfile config/analysis.yaml --cores 4
```

Explain the target and principal output paths in the README. Put positional
targets before options such as `--configfile` that can accept multiple arguments.
Use separate labeled graphs only when distinct analysis entry points or materially
different configurations warrant them; do not generate a diagram for every sample.

## One generation command

Use the project's existing documentation build, Make target, or a small script.
Keep it outside the scientific dependency graph so graph generation does not
recursively depend on its own documentation output. Do not write a second parser
for Snakefiles or a hand-maintained list of graph edges.

For example, `scripts/update-rulegraph.sh` can contain:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p docs/figures
graph_tmp=$(mktemp docs/figures/.rulegraph.XXXXXX)
trap 'rm -f "$graph_tmp"' EXIT

# Match the README's scientific scope. Keep diagnostics off stdout.
PYTHONHASHSEED=0 snakemake all --snakefile workflows/main/Snakefile \
  --configfile config/analysis.yaml --rulegraph \
  | dot -Tsvg > "$graph_tmp"

mv "$graph_tmp" docs/figures/rulegraph.svg
```

The temporary output and `pipefail` preserve the previous diagram if either
Snakemake or Graphviz fails. Make the script executable and document
`./scripts/update-rulegraph.sh` as the regeneration command. Adapt the output path
to the project's layout. Avoid timestamps and machine-specific paths in the image.

Embed the generated file with a relative link from the analysis README, for example:

```markdown
![Rule dependencies for the main analysis](docs/figures/rulegraph.svg)

Generated from `workflows/main/Snakefile`, `config/analysis.yaml`, target `all`.
Regenerate with `./scripts/update-rulegraph.sh`.
```

Treat the image as generated: update the workflow or configuration and regenerate,
rather than editing the SVG. Pin Snakemake and Graphviz in the documentation
environment; use the same environment in development and CI. Keep sample/target
ordering deterministic. Fixing `PYTHONHASHSEED` helps, but verify that two repeated
generations produce identical output; it does not make arbitrary workflow code
deterministic. Use a shared container/platform if renderer or font differences
otherwise cause irrelevant changes. Do not hide genuine graph changes by
discarding differences or blindly sorting DOT/SVG lines.

## Enforce freshness

For a checked-in README image, commit the generated SVG and run the same generation
command in CI on pull requests and pushes. After installing the pinned documentation
environment and supplying the required inputs/configuration, use:

```bash
set -euo pipefail
./scripts/update-rulegraph.sh
git ls-files --error-unmatch docs/figures/rulegraph.svg >/dev/null
git diff --exit-code -- docs/figures/rulegraph.svg
```

This fails for a missing/untracked image or a stale tracked image. Tell contributors
to regenerate and include the updated image with their workflow change; CI need
not make commits. Require this check before merging to enforce freshness. Prefer
running this inexpensive job for every PR; narrow path filters can miss included
rules, imported code, profiles, sample manifests, or configuration changes.

For a documentation site whose images are generated on every build, generate the
graph as a build dependency. That keeps the built site current, but does not update
a separately checked-in README image: that image still needs the check above.

## What the graph does and does not establish

`--rulegraph` shows rules and their dependency relationships, collapsing repeated
jobs. It is usually clearer in a README than `--dag`, which shows individual jobs.
It does not prove successful execution, show every sample, or document all tool
options. Repeated use of a rule can even produce cycles in the collapsed view.
Keep the explicit launch commands and scientific descriptions alongside it.

Graph generation does not execute analysis jobs, but parsing the workflow and
evaluating input functions still happens. Keep parse-time code free of downloads,
submissions, or other analysis side effects; send diagnostics to stderr so they
do not corrupt DOT output. A graph can require input files or sample metadata,
and checkpoint-dependent branches may be unresolved before checkpoint outputs
exist. Do not claim an incomplete graph represents the complete analysis.

Make graph construction possible from tracked configuration and small appropriate
metadata where feasible. If production inputs cannot be available in CI, use a
documented representative configuration of the same workflow and label the figure's
scope, or generate/check it in an environment with access to the required inputs.
Do not fabricate scientific inputs, silently skip a failed check, or launch a full
analysis merely to draw its graph.

For repositories that prefer native GitHub diagrams, supported Snakemake versions
can emit `--rulegraph mermaid-js`. Generate the README's marked Mermaid block with
the same regeneration and freshness policy; never maintain its topology separately.
SVG is the default here because it also works in ordinary Markdown viewers.

See the official [Snakemake graph options](https://snakemake.readthedocs.io/en/stable/executing/cli.html#utilities)
and [GitHub diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).
