---
title: Using AI in Research
nav_order: 2
---

# Using AI in Research

## What AI changes, and what it does not

Generative AI changes how scientific work can be done. It does not change the responsibilities of scientists and authors. The same scholarly standards apply as before: evaluate your sources, be skeptical, and review your own work carefully. You are accountable for everything you produce, whether you wrote it entirely by hand or with AI assistance.

AI poses a particular challenge for code. If you do not understand generated code well enough to review it, it is difficult to vouch for its correctness. This is why you still need to learn to program while using these tools. They are most effective in the hands of someone who can read, evaluate, and modify what they produce. And though AI can create new problems, there are many ways it can assist and improve your work: it can spot bugs, achieve better test coverage than you would practically write by hand, and teach you methods as you go.

## You are responsible for what you write

Whether it is code or prose, you are responsible for what you write, with or without AI.

For both code and prose, these responsibilities include:

1. **Originality.** LLMs can reproduce text taken directly from other sources without your knowledge. It is your responsibility to check. When drafting a manuscript with LLM assistance, run it through [Turnitin](https://www.turnitin.com/) or another plagiarism detector.
2. **Correctness.** LLMs get things wrong all the time — code that quietly does the wrong thing, confident statements in text that are simply false. Finding and correcting these is your job.
3. **Privacy.** LLMs can pull private information into material that then gets shared. This includes passwords or keys accidentally committed with code, files on your computer you did not expect to be read, and content carried over from earlier conversations. Be vigilant and defensive.

For code in particular:

1. **Reproducibility.** A scientific analysis does not need to work once. It needs to work again, on another machine, years later.
2. **Safety.** If you let an LLM execute commands on your computer — in a Claude Code session, for instance — it can damage, exfiltrate, or corrupt your data. [Managing Security](managing-security.md) covers how to bound what it can reach.

And for prose in particular:

1. **Citation standards.** LLMs fabricate references convincingly: plausible authors, plausible titles, DOIs that either resolve to something else or to nothing. Every citation needs to be checked against the actual source, and you should review what you cite. This is the failure mode most likely to reach print, because a fabricated reference looks exactly like a real one until someone follows it.

## Reproducibility and the data path

A reproducible computational analysis preserves its data, code, and runtime. When an analysis invokes an LLM as it runs, that model and the software around it become part of the runtime. This is a fragile dependency: hosted models can change, disappear, or produce different outputs when given the same inputs. The tutorial [*Designing reproducible large-language-model-assisted scientific analyses*](https://doi.org/10.1016/j.patter.2026.101644) by Dunn, Schultz, and Musser (2026) organizes this problem around the **data path**: the sequence of operations that transforms the declared inputs into the outputs evaluated in the paper.

- **Off the data path:** the LLM helps produce a durable artifact, such as code, but the published analysis runs without calling an LLM. The artifact sits on the data path; the LLM does not. For example, an assistant writes a Python script, you review and test it, and the committed script transforms the data.
- **On the data path:** data pass through an LLM at run time, or the LLM makes a decision required to produce the reported result. For example, the model directly classifies records, standardizes values, or decides which analysis step to run. Reproducing the result then depends on access to the model and its surrounding harness as well as the data and code.

The operational test is simple: **can the published analysis be rerun from inputs to results without invoking an LLM?** If yes, the LLM is off the data path. If no, it is on the data path. Keep it off the path when ordinary code can do the same job; on-path use can be appropriate when the required capability cannot readily be reduced to a fixed, inspectable pipeline.

{: .recommendations }
> - **Place the LLM off the data path where possible.** Prefer durable, inspectable code to a live model call when either can perform the task.
> - **Preserve LLM-related artifacts in a versioned, archived repository.** For on-path use, this includes prompts, skills, schemas, invocation records, and relevant intermediate outputs.
> - **Verify LLM results, and document how.** Test off-path code with standard software-engineering methods; assess on-path outputs with several task-appropriate checks, such as held-out benchmarks, known-answer fixtures, random spot-checks, cross-method agreement, and sensitivity tests.
> - **Consider open-weight models.** Published weights make the model more archivable, though exact reproduction can still depend on the tokenizer, inference software, hardware, and sampling settings.
> - **Record the model and its version at the time of analysis.** For on-path calls, also record the harness version when available, sampling parameters, and timestamp.
> - **Measure determinism within a model and agreement across models.** Repeat the same call and compare results across models, especially when the LLM step is central to the analysis.

## Working with data

Adopt these two practices when an assistant has access to your files.

**Raw data is immutable.** Transformations produce new files in a separate processed directory. If a script would modify something in your raw data directory, that is a bug regardless of what it was asked to do. Raw data is often irreplaceable and frequently the most expensive thing you own.

**Prefer a script over a direct transformation.** When you need data reshaped — a table reformatted, files restructured, columns renamed — have the assistant write a script you can read and re-run, rather than letting it edit the data in place. A script is reviewable, reproducible, and reversible. A direct edit is none of those, and you will not be able to reconstruct what happened six months later.

## Reporting AI use

{: .note }
> **AI reporting in three steps**
>
> 1. **Before the work, check the rules and agree on a plan.** Review the AI policies and reporting requirements of the intended journal, funder, institution, or other recipient. If they do not fit your planned use, change the AI plan or reconsider where you will send the work. Decide what information you need to record, and communicate the plan clearly to every collaborator before the work begins.
>
> 2. **Before drafting the statement, check again.** Once the work is complete, reread every applicable policy and note what must be reported, where the statement belongs, and whether a format is required. Requirements can change during a project. If none apply, still consider including a short description of your AI use.
>
> 3. **Write a statement that satisfies every requirement.** Many journals and funding agencies specify what must be reported without prescribing the wording. In that case, use the [GAIDeT](#gaidet)-based [Roll your own](#roll-your-own) approach below.

There is considerable variation in how AI use is reported in science. There is more transparency when coding with AI agents: if you have the agent make your git commits, the record of what it did is detailed and quite informative. If you write prose with coding tools — a text editor and git, with LaTeX or markdown documents — you get the same provenance and version tracking for free.

Most people write prose in other tools, such as Google Docs or Microsoft Word, which do not record changes at the same granularity. Approaches to describing AI use when writing prose vary much more widely — and are often missing entirely. A [systematic map of 230 ecology and evolutionary biology journals](https://doi.org/10.1186/s41073-026-00230-1) (Drobniak et al. 2026) found that nearly half offered no guidance on AI use at all. Where policies did exist they were largely generic and publisher-driven: text-mining of 124 guideline documents turned up highly standardized precautionary language about responsibility and prohibitions, but little operational guidance on acceptable uses or disclosure formats. Explicit AI disclosures appeared in fewer than 6% of papers, even in journals that had a formal policy.

A note on wording. This chapter says *reporting* rather than *disclosure*. Disclosure is borrowed from the conflict-of-interest frame, where the thing disclosed is a potential taint and silence would be concealment. Using a tool is not that, and the confessional framing is plausibly part of why the rates above are so low. GAIDeT's authors designed their taxonomy specifically so that researchers could say what they delegated "briefly and without stigma". AI is one method among many available to scientists, and should be reported the way other methods are.

You should obviously not use AI where it is explicitly forbidden and then say nothing about it. If you would prefer to use AI on a project and your preferred journal does not allow it, find a journal that does — or do not use AI. Where policies permit AI use but say nothing about whether or how to report it, err on the side of saying more rather than less.

Third-party tools for identifying AI-generated text are notoriously unreliable. Model providers, however, are starting to mark content generated by their tools. This includes clearly identifiable marks, such as metadata in generated files, as well as [statistical patterns in text](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) that are imperceptible to humans but readily identified if you know the pattern.

There are two parts to such a system: the model embeds a pattern, and a tool detects it. Who will have access to the detectors is not yet clear, and depends on why the marking exists in the first place. One motivation is regulatory — the EU AI Act's Article 50(2) requires that AI-generated content be marked in a machine-readable format, with the accompanying Code of Practice on Transparency of AI-Generated Content and the obligation taking effect in August 2026. Regulation of that kind may require detection methods to be broadly available. Another motivation is to keep AI-generated content out of training runs: model trainers do not want to train on the output of their own earlier models, and a large fraction of text on the internet now is exactly that. If marking exists mainly to filter training data, the detectors may never be shared.

The practical conclusion is the same either way. Assume that AI-generated text will be reliably identifiable in the near future, if it is not already, and that your use of AI will be known to others whether or not you report it.

### Policies

#### Journal policies

Check your target journal's AI guidelines at the start of a project, not at submission. Policies vary, but common patterns include:

- Most journals allow AI for coding assistance but require disclosure of how it was used
- Many also allow AI-generated text in manuscripts, again requiring specific disclosure
- AI is not accepted as an author — see [COPE's position statement on authorship and AI tools](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools). AI tools cannot be authors because they cannot take responsibility for the work, but their use should be declared

#### Funding agency policies

The same considerations apply to grants as to manuscripts, and the policies are not the same ones. Make sure you understand a particular agency's position *before* you start writing a proposal for it.

#### Institution policies

Institutions are scrambling to develop policies on AI use. This is particularly true in academia, and especially for student work. Make sure your use of AI in documents that fulfill academic requirements is fully compliant — papers for classes, or manuscripts that will become chapters of a PhD thesis.

### Standards for reporting AI use

Most statements about AI use today are freeform text or publisher-supplied boilerplate. That makes them hard to compare across papers, hard to aggregate, and hard to check. Several efforts are underway to define richer, better-specified vocabularies for describing what was actually done.

#### The Vancouver Standard

Under development by the [International Science Council](https://council.science/) together with COPE, STM, and the Global Young Academy, and named for the World Conference on Research Integrity held in Vancouver in May 2026.

*The principle:* one shared standard, across disciplines, publishers, and countries. The problem it targets is not that disclosure is hard to write but that every venue wants it differently, so authors face a new format each time and nobody can compare disclosures across the literature. It is being developed by open consultation rather than decree — three rounds running into 2027.

There is no example to give yet. Nothing has been published to adopt, and the taxonomy of what should be disclosed is still being settled. Worth tracking rather than using.

#### STM Classification of AI Use

Published by the [STM Association](https://stm-assoc.org/document/recommendations-for-a-classification-of-ai-use-in-academic-manuscript-preparation/) in September 2025.

*The principle:* classify the activity, and leave permission to the publisher. It enumerates nine things an author might do with AI while preparing a manuscript and deliberately takes no position on which are acceptable. Each publisher then decides, for each activity, whether it is permitted, whether it must be declared at submission, and whether that declaration appears in the published paper. The scope is manuscript preparation, not the research behind it.

The nine cover language refinement; drafting content; translation; refining reported data; generating illustrative images or diagrams; generating visualizations of research data; formatting code; gathering references; and — the one nobody considers acceptable — presenting AI-generated content as though it were original research data.

A statement in this shape names the activities rather than the tool:

> AI was used in preparing this manuscript for language refinement and for translation. AI was not used to draft manuscript content, gather references, or generate figures or data visualizations.

#### GAIDeT

The Generative AI Delegation Taxonomy, [published in *Accountability in Research*](https://doi.org/10.1080/08989621.2025.2544331), with a [declaration generator](https://panbibliotekar.github.io/gaidet-declaration/).

*The principle:* frame AI use as *delegation*. A human decides to hand a specific task to a tool and remains accountable for the result, so a statement should name the tasks delegated and who supervised them — not simply assert that AI was used. Unlike the STM classification, it spans the whole research lifecycle rather than just writing, with eight categories: conceptualization, literature review, methodology, software development and automation, data management, writing and editing, ethics review, and supervision.

The generator produces a statement you paste into the manuscript, conventionally as a short subsection before the references:

> The authors declare the use of generative AI in the research and writing process. According to the GAIDeT taxonomy, the following tasks were delegated to the generative AI tool Claude under full human supervision: code generation; data visualization; proofreading and editing.

#### AIdIT

AI disclosure for Improved Transparency, proposed in the [systematic map](https://doi.org/10.1186/s41073-026-00230-1) cited above.

*The principle:* a disclosure standard is only worth having if compliance with it can be checked. Having found that existing policies produced almost no actual disclosures, the authors designed for measurability. AIdIT is taxonomy-based, spans the whole research lifecycle rather than manuscript preparation alone, and pairs structured categories of AI use with explicit human-oversight statements. It emits machine-readable output, so uptake can be counted rather than assumed — which is what lets you tell a standard that is working from one that is merely published.

It is also the only one of these to come from within a research community rather than from publishers or a standards body. Whether that is a strength or a limitation depends on whether it travels beyond ecology and evolutionary biology.

The framework is recent enough that worked examples in published papers are still scarce.

#### Roll your own

If your journal or institution does not require a particular format, you can write your own statement. **Freeform should not mean taxonomy-free, though.** Drawing the task categories from a formal taxonomy makes omissions less likely and lets readers compare your use with other work. [GAIDeT](#gaidet) is a good default because it covers the whole research lifecycle and records AI use as tasks delegated under human supervision.

A useful statement names the tool and model or version, the specific tasks delegated, and how people reviewed the work and retained responsibility. This manual's [AI-use statement](index.md#ai-use) is a fuller example. A concise statement can be enough when the work was limited:

> Following the GAIDeT taxonomy, we used Claude Code with Claude Opus 4.8 for code generation, data visualization, and proofreading and editing. The authors reviewed all outputs, independently verified the analyses, and take responsibility for the final work.
