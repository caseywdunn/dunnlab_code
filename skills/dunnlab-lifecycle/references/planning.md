# Phase 1: Planning

Turn a high-level scientific question into feasible next actions. Iterate where decisions are missing; a plan that is already actionable does not need extra rounds of review.

## Scaffolding

For a new repository, use `dunnlab-new-project` when available and within the requested scope. For an established project, preserve its structure and environment. Extend `dev_docs/overview.md` or its existing equivalent rather than duplicating the plan. Record the path in lifecycle state.

Keep exploratory work and the durable analysis distinguishable. The default is:

```text
exploratory/     # Investigations and preserved findings
analyses/        # Reproducible analyses supporting reported results
```

Create these as needed and preserve an established equivalent layout. Shared transformation code may live in the project's normal source directory and serve both phases. Original measurements, observations, source documents, or simulation inputs remain immutable; derivatives go elsewhere. Reproducing the computational analysis starts from those preserved inputs, not from repeating a physical experiment or data collection campaign.

## What the plan contains

- **Questions and deliverable.** State questions that a result could answer and identify the intended report, paper, release, or other output. For example, “Does the intervention change the measured response?” is more actionable than “Explore the measurements.” Include null or negative outcomes as possible answers.
- **Inputs and access.** Identify datasets, source material, or simulation specifications by stable identifiers, versions, locations, or acquisition protocols. Record restrictions and dependencies on people or future collection. Distinguish inputs available now from those still needed.
- **Candidate methods.** Describe the proposed analyses, named methods or tools, and assumptions connecting them to each question. Exploration may revise these choices.
- **Decision safeguards.** Identify essential controls, units, sampling structure, uncertainty, and likely biases where relevant. Preserve preregistered commitments and distinguish exploratory choices from confirmatory tests.
- **Constraints.** Record the known compute and time budgets, access limits, collaborator dependencies, and deadlines. Do not invent a budget or assume permission to exceed one.

## Gate: an actionable plan

Record evidence for each criterion in the gate report:

- Each question maps to at least one candidate analysis and an interpretable possible result.
- The next concrete actions have identified inputs and no ambiguity that prevents execution.
- Inputs needed for those actions are accessible; verify access or inspect a representative input where feasible. Future or restricted inputs have explicit dependencies and do not silently block the proposed work.
- The approach is feasible within the known constraints, with important assumptions and unresolved scientific decisions identified.

State which checks were executed and which conclusions are judgments about feasibility. A plan document alone does not demonstrate data access, and a successful file read does not establish that a method answers the scientific question.

If a required criterion is unmet, keep the gate open and resolve the specific gap. Continue independent planning work; ask for missing decisions only when needed. If the criteria pass, follow the shared gate and authorization rules in `SKILL.md` to enter Exploration.
