---
title: Reproducibility
nav_order: 12
---

# Reproducibility

A scientific analysis does not need to work once. It needs to work again: for a reviewer, for a colleague extending it, and for you in two years when a reader asks how a number was obtained. This chapter covers what that requires and how agents change it. [Correctness](correctness.md) covers the related question of whether the result is right, and [Software Engineering](software-engineering.md) covers the practices that implement both.

## What reproducibility means

An analysis is **reproducible** when the same data, run through the same code in the same software environment, give the same results. This is narrower than **replicability**, where a new study with new data reaches the same conclusion. Reproducibility does not show that a result is right; a reproducible analysis can reproduce a mistake perfectly. But it is the minimum for a result to be checked at all, because a result that cannot be regenerated cannot be examined.

In practice, the question is concrete: **could someone with your repository, your data, and the instructions in your README regenerate every reported result, without asking you anything?**

## Data, code, and runtime

We frame reproducibility as in our tutorial [*Designing reproducible large-language-model-assisted scientific analyses*](https://doi.org/10.1016/j.patter.2026.101644) (Dunn, Schultz, and Musser, 2026, *Patterns*). A reproducible computational analysis preserves three things:

- **Data:** the inputs the analysis starts from.
- **Code:** the instructions that transform the data into results.
- **Runtime:** everything the code needs in order to run, such as the language, the libraries and tools with their versions, and any services it calls.

The paper also defines the **data path**: the sequence of operations that transforms the declared inputs into the outputs reported in the paper. Reproducing a result requires the data, code, and runtime of everything on that path, and nothing off it. The framing is especially useful with AI, because it makes clear what role a model plays in an analysis. A model that helped write a script is off the data path; the script is code, and the model is not needed to rerun it. A model that classifies records while the analysis runs is on the data path, and becomes part of the runtime. [Using AI in Research](using-ai.md#reproducibility-and-the-data-path) explains the consequences.

### Data

Preserve the exact inputs, unchanged.

- **Never modify raw data.** Keep originals read-only and separate from derived files, and produce every derived file with code. Then you can always start over from the source.
- **Record the identity of every input:** accession numbers, download dates, database releases, and checksums, so you can tell later whether a file is the one that was used.
- **Store data appropriately.** Large data belong in suitable storage, not in Git. The code should record where to obtain them.
- **Do not treat intermediate files as data.** Anything derived can be regenerated, and should be regenerated rather than copied by hand when the inputs or code change.

### Code

Preserve the exact code that produced each result, and make it do all of the work.

- **Commit every verified step** to Git, and tie each reported result to a commit.
- **Capture every step,** from raw data to final results, in code. Ideally a workflow runs the whole analysis with one command; see [Workflow frameworks](software-engineering.md#workflow-frameworks). An unavoidable manual step must be written down exactly.
- **Put settings in configuration files,** not typed at the command line, so the parameters are part of the record.
- **Fix random seeds** where results depend on randomness.
- **Generate everything you report,** including the numbers in a manuscript; see [Writing with AI](writing-with-ai.md#principles-behind-our-approach).
- **Write the instructions:** a README with the exact commands, for a reader who was not there.

### Runtime

Preserve what the code needs in order to run. The runtime is the easiest of the three to forget, because it is invisible until it changes.

- **Specify the environment** in a file, such as a conda `environment.yml`, listing the tools and their versions. For long-term preservation, a container image captures the whole environment.
- **Record what actually ran:** tool versions as reported by the tools themselves, and the commit and environment behind each run. See [Preserve provenance across machines](working-across-computers.md#preserve-provenance-across-machines).
- **Count external services as runtime.** An analysis that queries an online database or calls a hosted model depends on that service still existing and behaving the same way. Record the release or version used, and where possible save the responses so the analysis does not have to query again.
- **Keep models off the data path** when ordinary code can do the same job. A hosted model is the most fragile runtime dependency of all: it can change or disappear without notice.

## How agents change the picture

Agents make reproducibility much easier and, if you are careless, much harder.

**Easier:** the tedious work of reproducibility is exactly what agents do well and people skip. An agent will write the environment file, record tool versions, turn a series of commands into a workflow, write the README's reproduction instructions, and commit each step with an explanation, all without complaint.

**Harder:** agents work fast and interactively. In one session they can reshape a table directly, edit an intermediate file in place, try ten variants of an analysis, and summarize a result in the chat, leaving no durable record of which variant produced the figure you kept. Each of these puts something on the data path that is not preserved as data, code, or runtime.

The remedy is the same in every case: insist that every result comes from committed code, run on recorded data in a recorded runtime, never from something that happened only in a conversation.

## Test that it reproduces

Reproducibility is a claim, and it can be tested. The test is to start from nothing:

1. Take a fresh copy of the repository on a different machine, or a clean virtual machine or container.
2. Build the environment from its specification alone.
3. Obtain the data the way the README says.
4. Run the documented command.
5. Compare the results with the ones you reported.

This is an ideal job for an agent: ask it to follow the README literally in a clean environment and report every place where it had to guess, fix something, or ask. Each of those is a gap in the instructions. For a large analysis, a reduced run on a small subset tests the route without repeating the full computation.

Some differences are expected and harmless, such as timestamps or the order of lines in an unsorted file. Others reveal a real dependency on something unrecorded. Know which is which, and make comparisons that ignore the harmless kind.

## Archive what you publish

GitHub is not an archive: repositories can be renamed, rewritten, or deleted. For anything you publish:

- **Archive the code** as a tagged release with a permanent identifier, for example by connecting the repository to [Zenodo](https://zenodo.org/), which gives each release a DOI.
- **Deposit the data** in an appropriate repository, such as the SRA for sequencing reads or [Dryad](https://datadryad.org/) or Zenodo for other data, and cite their accessions.
- **Cite specific versions** of your code, data, software, and databases in the paper, so a reader can find exactly what you used.

## Proportion and timing

Not every exploratory notebook needs a container image. Match the effort to what depends on the result. A quick look at a dataset needs little more than committed code; a result that will be published, built on, or used by others needs everything above.

But start early. Reproducibility is cheap to keep and expensive to recover. Rebuilding an environment a year later, or working out which of five similar scripts made a figure, costs far more than recording it at the time. Since agents do most of this bookkeeping, there is little reason to defer it.
