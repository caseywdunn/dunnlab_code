---
title: Correctness
nav_order: 13
---

# Correctness

[Reproducibility](reproducibility.md) means a result can be regenerated. Correctness means the result is right. They are different: a reproducible analysis can faithfully reproduce a bug, and a correct result obtained once by hand cannot be checked again. You need both.

Correctness matters more, not less, when agents write the code. An agent produces plausible-looking code and output quickly, and plausibility is not correctness. The checks in this chapter are how you find out whether a result deserves your trust. [Software Engineering](software-engineering.md) covers how to implement them.

## Three questions

"Is it correct?" hides three separate questions:

1. **Does the code do what it was meant to do?** A filter meant to keep reads of at least 50 bases might keep reads longer than 50 instead. This is **verification**, and it is what tests and code review mostly address.
2. **Was it meant to do the right thing?** Code can do exactly what was intended while the intention was wrong: the wrong statistical test, a normalization that removes the signal, an outgroup that is not an outgroup. This is **validation**, and it needs scientific knowledge.
3. **Does the result hold up?** A correct analysis of a dataset can still give an answer that changes with a reasonable alternative choice, a different subsample, or new data. This is **robustness**.

Agents help most with the first question. The second and third depend most on you.

## How hard is it to do, and how hard to check?

A useful way to plan the checks for any task is to ask two questions separately: how hard is it to *do*, and how hard is it to *check* that it was done right? The answers place every task in one of four quadrants, and each quadrant calls for a different strategy.

| | **Easy to check** | **Hard to check** |
|---|---|---|
| **Easy to do** | Let the agent do it and check it automatically. | Be most careful here. |
| **Hard to do** | Ideal work for agents: build the check first. | Break it down, and gather independent evidence. |

### Easy to do, easy to check

*Examples:* converting sequence files between formats, renaming sample identifiers through a mapping table, counting reads per sample, merging per-sample tables.

These are routine tasks with simple invariants: the number of sequences is the same before and after conversion, every identifier maps to exactly one new identifier, the counts sum to the total. **Strategy:** have the agent do the work and encode the invariants as automatic checks, so they run every time. Do not spend review effort here beyond confirming the checks exist. The main risk is that the checks are never written because the task seemed too easy to need them.

### Hard to do, easy to check

*Examples:*

- **Rewriting a slow program to be fast.** A k-mer counter rewritten in Rust is hard to write, but easy to check: it must give exactly the same counts as the slow version on the same data.
- **Designing primers or guide RNAs.** Finding a sequence that meets every constraint is hard, but checking a proposed sequence's melting temperature, specificity, and position is straightforward.
- **Searching for a better tree.** Finding a high-likelihood phylogeny is computationally hard, but computing the likelihood of a proposed tree is easy.

**Strategy:** build the checker first, then let the agent work against it. This is where agents are most powerful, because they can try many approaches and keep only what passes. Keep a simple reference implementation, even a slow one, as the standard to compare against. An agent can work autonomously for a long time in this quadrant, because every attempt is checked objectively.

### Easy to do, hard to check

*Examples:*

- **Differential expression with default settings.** One command produces a list of significant genes. Whether the normalization, the design formula, and the handling of batches were right for this experiment is hard to tell from the output.
- **Automated functional annotation.** A pipeline assigns functions to thousands of genes in an hour. Whether those assignments are right for a distantly related, non-model organism is much harder to know.
- **Summarizing a literature or a dataset.** A fluent summary is easy to produce and hard to verify without doing the reading yourself.

This is the most dangerous quadrant, especially with agents. The output looks finished and authoritative, nothing fails, and the errors are silent. **Strategy:** create checks that the task does not provide by itself:

- **Positive and negative controls:** genes with well-established functions or expression changes that the analysis must recover, and comparisons where there should be no difference.
- **Known-answer data:** simulate data where you know the truth, or use a published dataset with an accepted result, and confirm the analysis recovers it.
- **Sensitivity analysis:** vary reasonable choices, such as parameters, filters, or reference databases, and see whether the conclusions change.
- **Independent methods:** compare with a different tool or approach. Agreement is reassuring; disagreement tells you where to look.
- **Inspection by hand:** pick a few results at random and trace each one back to its raw data.

### Hard to do, hard to check

*Examples:*

- **Deep phylogenetic relationships,** such as which animal lineage branched first. There is no ground truth to compare against, and results can depend on models, gene sampling, and taxon sampling.
- **De novo genome assembly** of a non-model organism. Summary statistics measure completeness and contiguity, but not whether the assembly's structure is right.
- **Reconstructing ancestral traits** across a tree, where the answer depends on the tree and on modeling assumptions that are hard to test.

**Strategy:**

- **Decompose** the problem into parts that fall in easier quadrants, and check each part.
- **Use simulation** to test the method under conditions where you know the answer, including conditions that mimic the suspected difficulties of the real data.
- **Seek independent lines of evidence:** different data types, gene sets, or methods that do not share the same weaknesses.
- **Test explicitly whether alternatives can be rejected,** for example with [topology tests](https://iqtree.github.io/doc/Advanced-Tutorial#testing-constrained-tree) of competing phylogenetic hypotheses, rather than reporting only the best answer.
- **State assumptions,** and scale the strength of claims to the strength of the evidence.
- **Get outside review** from people with expertise in the problem, early.

### Moving between quadrants

The quadrants are not fixed. Building a good check moves a task from "hard to check" to "easy to check": a simulation framework, a set of positive controls, or a reference implementation is often the most valuable thing an agent can build early in a project. Agents also move many tasks from "hard to do" to "easy to do". They do much less to make anything easier to check. **As agents take over more of the doing, checking becomes the bottleneck**, and it is where your time and expertise matter most.

## Tests

Tests check that code does what it was meant to do, automatically and every time it changes. They are the main tool for the first question above, and they make the easy-to-check quadrants work. [Software Engineering](software-engineering.md#testing-how-you-know-it-works) describes the kinds of test and how to use them. Two points from this chapter's perspective:

- **Tests check intentions, not truth.** A test confirms the code matches what someone expected. If the expectation was wrong, the test passes anyway.
- **The most valuable tests encode biological knowledge,** such as a known answer, a conserved quantity, or a case that must be rejected. These are tests you can design even if you never write code.

## External validation

External validation compares results with evidence from outside the analysis. It addresses the second and third questions, which tests cannot reach.

- **Published results:** rerun the analysis on a dataset whose result is established, and confirm it is recovered.
- **Orthogonal data:** check RNA-seq expression changes against qPCR for a few genes, or a predicted gene structure against long-read transcripts.
- **Independent datasets:** check whether a pattern found in one dataset appears in another.
- **Simulation:** generate data from a known process, including the complications you expect in real data, and measure how well the analysis recovers the truth.
- **Experiments:** for a central claim, the most convincing validation may be at the bench or in the field, not in the computer.

### Orthogonal validation

A check is only as useful as its independence from what it checks. A validation is **orthogonal** when it shares as little as possible with the original analysis: different data, a different measurement, different methods, different assumptions, and different sources of error. An error shared by the analysis and its check cannot be caught by that check. Two read aligners that both map to the same flawed reference genome will agree with each other, and both be wrong.

To judge how orthogonal a check is, list what it shares with the analysis it is checking:

- **Data:** the same samples, the same sequencing run, the same preprocessing?
- **References:** the same genome assembly, annotation, or database release?
- **Methods and assumptions:** the same software, the same statistical model, the same filters?
- **Authorship:** the same person or the same agent session? A check written by the agent that wrote the analysis can share its misunderstanding of the problem. Have the expected answer come from you, the literature, or a separate session or model.

The fewer shared elements, the more a passing check means.

**Use multiple orthogonal validations where possible.** Each check catches some kinds of error and is blind to others, and each has weaknesses of its own. Several checks that fail in different ways cover each other's blind spots, and when they converge on the same answer, the result rests on more than one foundation. For example, a claim that a gene is expressed more strongly in tentacles than in the body can draw on:

- the differential expression analysis of RNA-seq data that suggested it;
- qPCR on independent samples, a different measurement technique;
- in situ hybridization, which shows where in the animal the gene is expressed rather than how much; and
- reanalysis of an independent published dataset from another lab.

Each of these can be wrong, but it is unlikely that all of them are wrong in the same direction. Similarly, a phylogenetic result is more convincing when it holds across different gene sets, different substitution models, and different kinds of data, than when it holds across several programs analyzing the same alignment.

Be wary of agreement among checks that are not orthogonal. Five analyses of the same alignment that agree tell you less than two that share nothing, because a problem in the alignment would affect all five.

## Code review

Review catches what automated checks miss: logic that runs without error but does the wrong thing, assumptions nobody wrote down, and checks that should exist but do not.

**Review by you.** You may not read every line an agent writes, but read the lines that decide results: filters, joins, thresholds, and statistical calls. A join that silently drops samples whose names do not match exactly, or a filter applied before a step it should have followed, is invisible in the output and obvious in the code. Read the tests, which tell you what the code claims to do. Ask the agent to explain any part you do not understand, and to point out where it made choices.

**Review by agents.** A second agent session with fresh context, given the code and asked to find problems, catches errors the author session is blind to. A different model is even more independent. Ask adversarially: *what would make this give a wrong answer without failing?* rather than *does this look right?*

**Review by colleagues.** For results that matter, nothing replaces a colleague who knows the biology reading the analysis. Make it easy for them: a clear README, a readable workflow, and a short description of the decisions that matter.

Match the depth of review to the consequences. A plotting tweak needs a glance. The code that produces the central result of a paper deserves careful review from more than one source.
