# Execution provenance and output reuse

Capture evidence while executing meaningful analyses, starting in exploration.
Use existing engine records, tool logs, and environment specifications when they
contain the needed facts. A small record linking them is enough; do not build a
second workflow system or require a new schema for every scratch experiment.

## A minimal record for a small analysis

For one or a handful of executions, run the existing analysis command directly
and record its actual execution alongside it. One run note can contain the
command, settings, identities, result, and checks, with links to existing logs.
Preserve the relevant source and settings once per changed version through git
or a small snapshot; unchanged reruns can reference that preserved version.
There is no requirement for a new runner, a manifest generator, a copy of the
whole repository per run, or a separate environment file when a recorded runtime
and its reconstruction command fully describe a standard-library-only analysis.

For example, a run note could contain these fields (fill identities and versions
from the actual execution, never infer them from later files):

```yaml
analysis_id: threshold-summary
run_id: threshold-summary-01
command: python src/summarize.py --input data/raw/observations.csv --config selected.json --output runs/01/summary.json
source: preserved revision or source snapshot and its identity
inputs: data/raw/observations.csv and its measured checksum
settings: {minimum: 3}
environment: actual Python version; standard library only; reconstruction command
status: complete
outputs: runs/01/summary.json and its measured checksum
checks: exact count 2 and sum 13; agrees with the specified known answer
```

Record the command and identities when running it, and completion/checks only
after observing the outcome. This run note can also be the selected inventory
for a single-result analysis. Reference it from the scientific assessment instead
of transcribing its facts into parallel manifests. Automate repetitive capture
when useful, using engine/tool support first; completeness of evidence does not
require a bespoke execution framework.

## Identities and run records

Distinguish an input or analysis identity from a particular execution. Filenames
can be short and descriptive; they need not encode all parameters. Preserve dates
when they identify collection periods or releases, and track execution history
in records rather than repeatedly renaming the analysis.

For a run that informs a scientific decision or produces a retained result,
preserve:

- Analysis and run IDs, and the question or role the run serves. Link the analysis
  spec when one exists; exploration need not invent a final spec in advance.
- Source revision or recoverable source snapshot, resolved configuration, and the
  command or entry point actually executed. A commit ID alone does not identify
  uncommitted code.
- Input identities and hashes or immutable versions, including consequential
  reference databases and saved external-service responses.
- Actual tool/model versions, environment specification or lockfile identity, and
  stochastic settings. Give replicates distinct identities and appropriate random
  streams; record nondeterminism a seed does not eliminate.
- Completion status, logs or checks, and output identities and locations. Preserve
  hashes or immutable artifact versions sufficient to verify retained outputs.

Record failures as failures. Mark completion only after expected outputs pass the
relevant integrity checks. Do not reconstruct missing provenance by inspecting
current settings and assuming they produced an old file. Recover verifiable
records or rerun the affected computation.

Record parent inputs and transformations for derivatives. Reuse a derivative when
its identity and assumptions match. When two derivatives differ, identify the
scientific difference and verify equivalence before consolidating them.

## Deciding whether to reuse

An existing output is reusable when its completed run evidence matches the
required inputs, relevant code, environment requirements, and parameters, and its
stored artifacts still verify. Use the engine's rerun detection where it covers
these dependencies. Inspect gaps such as external databases, undeclared helper
code, or manually supplied intermediates; add only the missing tracking.

For a simple script, make the completion and identity check explicit; an
existence-only `if output.exists()` is insufficient. Do not treat interrupted or
partially written output as a checkpoint. Preserve valid baselines before replacing
outputs, and use the orchestrator's supported rerun controls where available.

An unrelated source commit does not invalidate every result. Record which relevant
dependencies changed and rerun their affected descendants. A rule rename or
reorganization still needs a check that commands, parameters, paths, environment
resolution, and requested targets are equivalent. Keep historical records intact.

## Selected-result manifests

Once a set of results is selected, generate its inventory from preserved run
records and actual artifacts. Reuse an existing inventory if it already supplies
the required traceability; do not maintain parallel hand-edited tables.

| Inventory | Useful fields |
|---|---|
| Artifacts | Artifact ID, role, location, hash/version, parent IDs, producing run ID, relevant measured summaries |
| Analyses | Analysis ID, selected completed run ID, purpose, input/output IDs, pointer to execution evidence |

Small TSV files under `analyses/manifests/` are one option; JSON or existing project
records may suit the relationships better. Define fields, units, and missing-value
conventions. Generate method/result summaries from the same records when useful.

The same preserved records should produce the same manifest. A new execution has
a new run ID and may have different timestamps or stochastic outputs; compare its
scientific outputs using the stated criteria rather than demanding identical run
metadata or silently replacing the baseline.

Version small inventories and keep their referenced evidence recoverable. Large
or restricted inputs, outputs, and logs may belong in an appropriate archive with
checksums and documented access, rather than git. Ignoring generated directories
in git does not provide preservation or backup.
