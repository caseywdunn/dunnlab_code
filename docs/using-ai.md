---
title: Using AI in Research
nav_order: 2
---

# Using AI in Research

This chapter is about judgment rather than tooling. It applies whether you use Claude, some other assistant, or none of the ones that exist as this is written — and you can read it without opening a terminal.

Everything here is general. Nothing in it is specific to this lab or to Yale.

## What AI changes, and what it does not

Generative AI changes how scientific work can be done. It does not change the responsibilities of scientists and authors. The same scholarly standards apply as before: evaluate your sources, be skeptical, and review your own work carefully. You are accountable for everything you submit, whether you wrote it by hand or with AI assistance.

AI poses a particular challenge for code. **If you do not understand generated code well enough to review it, you cannot vouch for its correctness.** This is why you still need to learn to program while using these tools. They are most effective in the hands of someone who can read, evaluate, and modify what they produce — and least safe in the hands of someone who cannot tell a working analysis from a plausible-looking one.

The opportunities are real too. AI can help you work faster, explore further, and gain insight you would not have reached alone. It can achieve better test coverage than you would write by hand, review code on every change rather than occasionally, and teach you methods as you work. It will introduce errors you have to find. It will also find errors you introduced yourself.

## You are responsible for what you commit

The governing principle: **you are responsible for code you commit, regardless of who or what wrote it.** "The AI wrote it" is not an explanation for a bug, a wrong result, or a security problem. It is your name on the commit and, eventually, on the paper.

In practice:

- **Read every diff before you commit it.** Not skim — read. If a change is too large to read carefully, it was too large a task to hand over in one go. Break it up.
- **If you cannot evaluate the code, you cannot vouch for it.** Where a generated approach uses something you do not understand, either learn it or ask for an approach you do.
- **Apply the same standard you would to code from a collaborator.** A checklist helps; this plugin ships one as the `dunnlab-codereview` skill, but any consistent standard beats an inconsistent one.
- **Scrutinize the science, not just the code.** An assistant will write syntactically perfect code that computes the wrong thing. A filter that silently drops rows, a join that duplicates records, a statistical test that does not apply to your design — these pass every linter. Sanity-check intermediate outputs and row counts, not just whether the script exits cleanly.
- **Scale your care to how far the result travels.** An exploratory notebook you will throw away needs less scrutiny than a pipeline that will produce a figure in a manuscript.

### Work that needs a human before it lands

Some things should never be committed on a fast review:

- Anything that touches raw data, or that writes into a raw data directory
- Statistical analysis, and the choice of test in particular
- Anything that will produce a number or figure appearing in a manuscript
- Changes to a shared pipeline that other people depend on
- Permission settings, `.gitignore`, and anything affecting credentials

## Working with data

Two habits matter more than any other when an assistant has access to your files.

**Raw data is immutable.** Transformations produce new files in a separate processed directory. If a script would modify something in your raw data directory, that is a bug regardless of what it was asked to do. Raw data is often irreplaceable and frequently the most expensive thing you own.

**Prefer a script over a direct transformation.** When you need data reshaped — a table reformatted, files restructured, columns renamed — have the assistant write a script you can read and re-run, rather than letting it edit the data in place. A script is reviewable, reproducible, and reversible. A direct edit is none of those, and you will not be able to reconstruct what happened six months later.

## Keeping private things private

- Put secure information — API keys, tokens, passwords, account credentials — in dedicated files that are listed in `.gitignore`, and never inline in a script.
- Use placeholder or synthetic data while developing a pipeline, and switch to the real thing only once it works.
- **Assume anything the assistant reads may be sent to the API.** On a shared system this includes anything your account can read, which on a cluster may include other people's work.
- Configure the tool to refuse to read credential files at all, rather than relying on it to decline. [Managing Security](managing-security.md) covers how.

## Disclosure

Claude Code adds a `Co-Authored-By` trailer to commits it writes, so the git history records where assistance was used. Leave it in place — it is useful provenance and it costs nothing.

For manuscripts and proposals, follow the policy of the specific journal or funding agency, and check before you start writing rather than after.

### Journal policies

Check your target journal's AI guidelines at the start of a project, not at submission. Policies vary, but common patterns include:

- Most journals allow AI for coding assistance but require disclosure of how it was used
- Many prohibit AI-generated text in manuscripts, or require specific disclosure of it
- AI is not accepted as an author — see [COPE's position statement on authorship and AI tools](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools). AI tools cannot be authors because they cannot take responsibility for the work, but their use should be declared

Consulting the guidelines early lets you plan your workflow and documentation around them.

### Funding agency policies

The same considerations apply to grants as to manuscripts, and the policies are not the same ones. Make sure you understand a particular agency's position *before* you start writing a proposal for it.

---

Next: [Getting Started](getting-started.md) covers the tools and how to set them up.
