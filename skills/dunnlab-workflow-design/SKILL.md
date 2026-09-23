---
name: dunnlab-workflow-design
description: >
  Design or revise computational analysis workflows in any discipline, from
  exploratory runs to reproducible results, with explicit data flow, reusable
  computation, and traceable execution.
---

# Dunn Lab Workflow Design

Apply these principles when building or changing an analysis workflow, including
its first consequential exploratory runs. Preserve established project structure
unless changing it solves a concrete problem. A design review does not itself
authorize moving files or running analyses.

This skill owns computational structure and execution evidence. Use
`dunnlab-bioinformatics` for biological methods and tool settings,
`dunnlab-lifecycle` for scientific scope and readiness, `dunnlab-defaults` for code
conventions, and `dunnlab-hpc` for Yale execution details. Use `dunnlab-new-project`
only when repository scaffolding is needed. Load companions for the actual task;
ordinary workflow changes do not require running a research lifecycle.

## Design for reuse during exploration

Keep inputs, parameters, reusable computation, and run outputs distinguishable.
Explore alternatives through configuration and small method-specific additions.
Share transformations when actual reuse warrants it; avoid copied pipelines and
speculative frameworks. A notebook executable from a clean kernel, a script, or
a workflow engine can all be retained when they meet the same requirements.

Start with a small informative path through the intended implementation. Record
subsamples, cheaper settings, and other approximations explicitly. Increase scale
and evidence as the scientific scope settles. Preserve the code and outputs behind
meaningful findings; disposable scratch work need not receive publication polish.

Selection for a report should normally retain the same implementation and choose
its inputs, configurations, and targets. Keep provisional and selected outputs
distinguishable without requiring parallel source trees or relocation. Archive
unselected investigations without erasing decisions, negative results, or evidence.

## Make the computation readable

Declare each stage's inputs, outputs, and scientifically meaningful parameters.
Keep external executables and their important options visible in workflow rules
or a simple orchestration script. Use focused scripts for substantive transforms
and checks; do not hide straightforward commands in generic runners, command
builders, or provenance wrappers. Record the command that ran instead of keeping
a second implementation just to describe it.

Name stages for their scientific purpose. Separate checks, provenance recording,
and reporting from the computation they assess. A reader should be able to follow
the data from inputs to reported outputs without an agent interpreting it.

## Choose orchestration and execution scope

Use Snakemake for multiple independent tools, fan-out/fan-in, or a substantial
dependency graph. A simple linear workflow can use bash or Python; fail on failed
commands and make dependencies and completion checks explicit. Do not introduce
an engine solely to satisfy a directory convention.

For Snakemake implementation or refactoring, read
[Snakemake organization](references/snakemake.md): thin entry points, stage rules,
visible commands, meaningful names, and shared full and bounded execution.

Provide one normal source-to-result route per analysis. Retrieval reuses verified
local inputs and obtains missing inputs using their recorded identity. Optional
caches are optimizations. Preserve original inputs unchanged, write derivatives
separately, and handle interrupted writes/downloads so partial artifacts cannot
be mistaken for successful outputs.

Keep resource settings separate from scientific choices where possible. A local
pilot and cluster run should share computation; record settings that can affect
results. Estimate resources from representative runs before scaling up. For Yale
execution, let `dunnlab-hpc` supply the launcher or executor configuration.
Prefer HPC for workloads impractical on a laptop: roughly more than ten minutes
of computation, memory beyond local capacity, GPU needs, or large sample batches.
Use representative local pilots where feasible; preserve the same scientific
implementation when changing execution platforms.

## Identify runs and reuse valid work

Give inputs and analyses stable identities; give each execution a distinct run
identity so reruns preserve their history. Capture input versions, resolved
parameters, source and environment identity, completion status, and outputs when
the run happens. A mutable path or today's configuration cannot establish what
produced yesterday's result.

Reuse output only when successful execution evidence covers the relevant inputs,
computation, environment, and parameters, and the artifacts still verify. File
existence alone is insufficient. Prefer the engine's dependency tracking and logs;
add records only for gaps. Read [execution provenance](references/provenance.md)
when implementing run capture, output reuse, or selected-result manifests.
For a small analysis, a directly executable command and a contemporaneous run
record can suffice. Do not add a custom runner solely to automate that record;
automate capture when repeated execution makes it worthwhile.

Invalidate only affected computations and downstream evidence. Preserve historical
source identity, but do not require expensive reruns solely because documentation,
rule names, or unrelated code changed. Verify that a purported organizational
change leaves commands, settings, inputs, and scheduled scope equivalent.

## Check what can change the conclusion

From exploration onward, check consequential assumptions: units, dimensions,
identifiers, joins, missingness, ranges, and successful tool completion. Use small
known-answer or independent checks for uncertain transformations where feasible.
Scale engineering checks to consequences and retained scope; avoid exhaustive
hardening of abandoned experiments. Agreement with a previous run is not by
itself evidence of scientific correctness.

Assume trusted project inputs unless the task says otherwise. Keep ordinary shell
quoting and accidental-data-loss safeguards; add validation only for a concrete
scientific or operational need. Avoid nested receipts and repeated checks at every
layer. Changes to a reporting or validation helper should not invalidate expensive
analysis jobs unless their computation depends on that helper.

## Make reproduction usable

Specify the environment and preserve consequential tool/reference versions. Test
reconstruction in an isolated environment, leaving the user's working environment
intact. Distinguish a clean run from preserved original inputs, reuse of verified
existing execution, and a partial or cached run; report actual coverage.

Make human, external-service, and model steps explicit. Prefer durable code for
model-assisted transformations when it preserves the intended method. If a model
is part of the method, preserve its inputs, prompts, settings, responses, and
verification; replaying responses differs from a fresh invocation. Lifecycle
assesses whether those limits meet the intended scientific deliverable.

When writing execution instructions or preparing a handoff, read
[reader documentation](references/documentation.md). Keep public usage instructions
canonical and current, with development history and detailed run evidence linked
separately.
