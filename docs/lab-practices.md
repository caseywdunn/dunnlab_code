---
title: Lab Practices
nav_order: 3
---

# Lab Practices

This is a partial description of the Dunn Lab's conventions for code development. Where the [Getting Started](getting-started.md) page covers the tools, this page covers what we expect of each other when using them.

## Code review expectations for AI-generated code

The governing principle is simple: **you are responsible for code you commit, regardless of who or what wrote it.** "Claude wrote it" is not an explanation for a bug, a wrong result, or a security problem. It is your name on the commit and, eventually, on the paper.

In practice:

- **Read every diff before you commit it.** Not skim — read. If a change is too large to read carefully, it was too large a task to hand over in one go. Break it up.
- **If you cannot evaluate the code, you cannot vouch for it.** This is the main reason you still need to learn to program while using these tools. Where a generated approach uses something you do not understand, either learn it or ask for an approach you do.
- **Apply the same standard as to human-written code.** The `dunnlab-codereview` skill has the checklist we use; ask Claude to run through it, and then check its work.
- **Scrutinize the science, not just the code.** Claude will write syntactically perfect code that computes the wrong thing. Filtering that silently drops rows, a join that duplicates records, a statistical test that does not apply — these pass every linter. Sanity-check intermediate outputs and row counts, not just whether the script exits cleanly.
- **Be more careful in proportion to how far the result travels.** An exploratory notebook you will throw away needs less scrutiny than a pipeline that will produce a figure in a manuscript.

### Work that needs a human before it lands

Some things should not be committed on a fast review:

- Anything that touches raw data, or that writes into `data/raw/`
- Statistical analysis and the choice of test
- Anything that will produce a number or figure appearing in a manuscript
- Changes to a shared pipeline others depend on
- Permission settings, `.gitignore`, and anything affecting credentials

### Disclosure

Claude's commits carry a `Co-Authored-By` trailer, so the git history records where AI assistance was used. Leave it in place — it is useful provenance, and it costs nothing.

For manuscripts and proposals, follow the policy of the specific journal or funding agency; see [Journal policies](getting-started.md#journal-policies). Check before you start writing, not after. AI is not listed as an author.

## Data privacy considerations

- Put all secure information (API keys, tokens, passwords, account usernames) in dedicated files that are in the `.gitignore`
- Use placeholder or synthetic data when developing analysis pipelines
- Deny rules in your `settings.json` should block Claude from reading credential files at all — see [Managing Security](managing-security.md). Note that these rules are anchored relative to your working directory unless you write them with `~/` or `//`.
- Assume anything Claude reads may be sent to the API. On shared systems this includes anything your account can read, which on a cluster may include other people's work.

## Data management

Consult our separate data management plan for requirements and conventions on where to store data, how to share files, archival, etc.

Two conventions worth restating here, because AI tools make it easy to violate them by accident:

- **Raw data is immutable.** Transformations produce new files in `data/processed/`. If a script would modify something in `data/raw/`, that is a bug regardless of what it was asked to do.
- **Prefer a script over a direct transformation.** When you need data reshaped, have Claude write a script you can read and re-run, rather than having it edit the file in place. The script is reviewable, reproducible, and reversible; a direct edit is none of those.
