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

1. **Reproducibility.** A scientific analysis does not need to work once. It needs to work again, on another machine, months later.
2. **Safety.** If you let an LLM execute commands on your computer — in a Claude Code session, for instance — it can damage, exfiltrate, or corrupt your data. [Managing Security](managing-security.md) covers how to bound what it can reach.

And for prose in particular:

1. **Citation standards.** LLMs fabricate references convincingly: plausible authors, plausible titles, DOIs that either resolve to something else or to nothing. Every citation needs to be checked against the actual source, and you should have read what you cite. This is the failure mode most likely to reach print, because a fabricated reference looks exactly like a real one until someone follows it.

## Working with data

Adopt these two practices when an assistant has access to your files.

**Raw data is immutable.** Transformations produce new files in a separate processed directory. If a script would modify something in your raw data directory, that is a bug regardless of what it was asked to do. Raw data is often irreplaceable and frequently the most expensive thing you own.

**Prefer a script over a direct transformation.** When you need data reshaped — a table reformatted, files restructured, columns renamed — have the assistant write a script you can read and re-run, rather than letting it edit the data in place. A script is reviewable, reproducible, and reversible. A direct edit is none of those, and you will not be able to reconstruct what happened six months later.

## Disclosure

There is considerable variation in how AI use is disclosed in science. When coding with AI agents, disclosure is largely a solved problem: if you have the agent make your git commits, the record of what it did is detailed and quite informative.

Approaches to prose vary much more widely — and are often missing entirely. A [systematic map of 230 ecology and evolutionary biology journals](https://doi.org/10.1186/s41073-026-00230-1) (Drobniak et al. 2026) found that nearly half offered no guidance on AI use at all. Where policies did exist they were largely generic and publisher-driven: text-mining of 124 guideline documents turned up highly standardised precautionary language about responsibility and prohibitions, but little operational guidance on acceptable uses or disclosure formats. Explicit AI disclosures appeared in fewer than 6% of papers, even in journals that had a formal policy.

So the variation is not really in what journals demand of you. It is that half say nothing, and most of the rest say something too vague to act on. It is important to identify the relevant policies early, so you can plan your workflow and documentation around them — and to expect that you will often be deciding for yourself.

You should obviously not use AI where it is explicitly forbidden and then fail to disclose it. If you would prefer to use AI on a project and your preferred journal does not allow it, find a journal that does — or do not use AI. Where policies permit AI use but say nothing about whether or how to disclose it, err on the side of over-disclosing.

Third-party tools for identifying AI-generated text are notoriously unreliable. Model providers, however, are starting to mark content generated by their tools. This includes clearly identifiable marks, such as metadata in generated files, as well as [statistical patterns in text](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) that are imperceptible to humans but readily identified if you know the pattern.

There are two parts to such a system: the model embeds a pattern, and a tool detects it. Who will have access to the detectors is not yet clear, and depends on why the marking exists in the first place. One motivation is regulatory — the EU AI Act's Article 50(2) requires that AI-generated content be marked in a machine-readable format, with the accompanying Code of Practice on Transparency of AI-Generated Content and the obligation taking effect in August 2026. Regulation of that kind may require detection methods to be broadly available. Another motivation is to keep AI-generated content out of training runs: model trainers do not want to train on the output of their own earlier models, and a large fraction of text on the internet now is exactly that. If marking exists mainly to filter training data, the detectors may never be shared.

The practical conclusion is the same either way. Assume that AI-generated text will be reliably identifiable in the near future, if it is not already, and that your use of AI will be known to others whether or not you disclose it.

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

### Disclosure ontologies

Most AI disclosures today are freeform text or publisher-supplied boilerplate. That makes them hard to compare across papers, hard to aggregate, and hard to check. Several efforts are underway to define richer, better-specified vocabularies for describing what was actually done.

#### The Vancouver Standard

Under development by the [International Science Council](https://council.science/) together with COPE, STM, and the Global Young Academy, and named for the World Conference on Research Integrity held in Vancouver in May 2026.

*The principle:* one shared standard, across disciplines, publishers, and countries. The problem it targets is not that disclosure is hard to write but that every venue wants it differently, so authors face a new format each time and nobody can compare disclosures across the literature. It is being developed by open consultation rather than decree — three rounds running into 2027.

There is no example to give yet. Nothing has been published to adopt, and the taxonomy of what should be disclosed is still being settled. Worth tracking rather than using.

#### STM Classification of AI Use

Published by the [STM Association](https://stm-assoc.org/document/recommendations-for-a-classification-of-ai-use-in-academic-manuscript-preparation/) in September 2025.

*The principle:* classify the activity, and leave permission to the publisher. It enumerates nine things an author might do with AI while preparing a manuscript and deliberately takes no position on which are acceptable. Each publisher then decides, for each activity, whether it is permitted, whether it must be declared at submission, and whether that declaration appears in the published paper. The scope is manuscript preparation, not the research behind it.

The nine cover language refinement; drafting content; translation; refining reported data; generating illustrative images or diagrams; generating visualizations of research data; formatting code; gathering references; and — the one nobody considers acceptable — presenting AI-generated content as though it were original research data.

A disclosure in this shape names the activities rather than the tool:

> AI was used in preparing this manuscript for language refinement and for translation. AI was not used to draft manuscript content, gather references, or generate figures or data visualizations.

#### GAIDeT

The Generative AI Delegation Taxonomy, [published in *Accountability in Research*](https://doi.org/10.1080/08989621.2025.2544331), with a [free declaration generator](https://panbibliotekar.github.io/gaidet-declaration/).

*The principle:* frame AI use as *delegation*. A human decides to hand a specific task to a tool and remains accountable for the result, so a disclosure should name the tasks delegated and who supervised them — not simply assert that AI was used. Unlike the STM classification, it spans the whole research lifecycle rather than just writing, with eight categories: conceptualization, literature review, methodology, software development and automation, data management, writing and editing, ethics review, and supervision.

The generator produces a statement you paste into the manuscript, conventionally as a short subsection before the references:

> The authors declare the use of generative AI in the research and writing process. According to the GAIDeT taxonomy, the following tasks were delegated to the generative AI tool Claude under full human supervision: code generation; data visualization; proofreading and editing.

#### AIdIT

AI disclosure for Improved Transparency, proposed in the [systematic map](https://doi.org/10.1186/s41073-026-00230-1) cited above.

*The principle:* a disclosure standard is only worth having if compliance with it can be checked. Having found that existing policies produced almost no actual disclosures, the authors designed for measurability. AIdIT is taxonomy-based, spans the whole research lifecycle rather than manuscript preparation alone, and pairs structured categories of AI use with explicit human-oversight statements. It emits machine-readable output, so uptake can be counted rather than assumed — which is what lets you tell a standard that is working from one that is merely published.

It is also the only one of these to come from within a research community rather than from publishers or a standards body. Whether that is a strength or a limitation depends on whether it travels beyond ecology and evolutionary biology.

The framework is recent enough that worked examples in published papers are still scarce.

#### Writing a disclosure now

Until one of these settles, borrow their common structure. A useful disclosure names three things: **which tool** and version, **which specific tasks** it was given, and **who checked the result**. That is considerably more informative than "AI was used in the preparation of this manuscript", it costs a sentence, and it is close enough to what any of these standards will eventually ask for that you will not have to rethink it.
