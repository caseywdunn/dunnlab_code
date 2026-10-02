---
name: dunnlab-biblio
description: >
  Manage verified manuscript, data, and software citations with Dunn Lab
  BibTeX conventions and conservative editing of existing references.
---

# Bibliographic Reference Management

Standards for managing `.bib` files and bibliographic references in Dunn Lab
manuscripts. This skill owns citation identity, attribution, and formatting;
`dunnlab-lifecycle` owns the scientific assessment and publication handoff.

## Connect claims and research objects to sources

When adding citations to prose or reviewing their use, read the source and check
that it supports the specific claim, population, method, and strength of inference.
Distinguish primary findings from background, reviews, and the manuscript's own
interpretation. Correct metadata alone does not establish support. Record an
unavailable source or unresolved claim instead of implying it has been verified.
A formatting-only request does not require a new literature review.

Cite datasets, reference databases, and software that materially support the work,
as well as method papers. Obtain preferred citation metadata from the actual
release or its authoritative record; identify the version or accession used in
the citation or associated methods. A methods paper alone may not identify the
executed software or database release. Prefer a version-specific persistent
identifier when available; retain a stable URL when it is the only locator.
Keep execution detail in workflow records rather than duplicating logs in BibTeX.
These practices follow the [Software Citation Principles](https://force11.org/info/software-citation-principles-published-2016/).

## Core principle: be conservative

**Never guess or fabricate bibliographic data.** If information is missing or uncertain, flag it for the user rather than filling in a plausible value. This applies to:

- DOIs
- Full author lists
- Titles
- Journal names
- Volume/issue/page numbers
- Publication years

If a field is missing from the source material, leave it out and add a comment (`% TODO: missing <field>`) rather than guessing.

## BibTeX file conventions

### Entry keys

Use the format `AuthorYear` for entry keys (e.g., `Dunn2008`, `HejnolMartindale2009`). For multiple papers by the same first author in the same year, append lowercase letters: `Dunn2008a`, `Dunn2008b`.

### Author lists

**Always retain the full author list.** Never abbreviate with "and others", "et al.", or truncate the list. Every author must be listed in the `author` field exactly as published.

```bibtex
% CORRECT
author = {Dunn, Casey W. and Hejnol, Andreas and Matus, David Q. and Pang, Kevin and Browne, William E. and Smith, Stephen A. and Seaver, Elaine and Rouse, Greg W. and Obst, Matthias and Edgecombe, Gregory D. and S{\o}rensen, Martin V. and Haddock, Steven H. D. and Schmidt-Rhaesa, Andreas and Okusu, Akiko and Kristensen, Reinhardt M{\o}bjerg and Wheeler, Ward C. and Martindale, Mark Q. and Giribet, Gonzalo},

% WRONG — do not truncate
author = {Dunn, Casey W. and others},
```

### Title capitalization

Protect words with non-standard capitalization by wrapping them in curly braces `{}`. This prevents BibTeX styles from down-casing them. Words that need protection include:

- **Proper nouns**: `{Bayesian}`, `{Darwin}`, `{Atlantic}`
- **Tool and software names**: `{RAxML}`, `{BLAST}`, `{Python}`, `{GitHub}`
- **Acronyms and initialisms**: `{DNA}`, `{RNA}`, `{HIV}`, `{MCMC}`, `{HPC}`
- **Species names** (when in the title): `{Nematostella}`, `{Drosophila}`
- **Other words with intentional capitalization**: `{pH}`, `{mRNA}`

Wrap only the individual words, not the entire title:

```bibtex
% CORRECT
title = {Broad phylogenomic sampling improves resolution of the animal tree of life using {Bayesian} methods},

% WRONG — wrapping entire title prevents style-driven formatting
title = {{Broad phylogenomic sampling improves resolution of the animal tree of life using Bayesian methods}},
```

### Fields to exclude

Do **not** include the following fields, as they add bulk without value for our use cases:

- `abstract`
- `keywords`
- `file`
- `local-url`
- `url` (unless it is the only way to locate the work, e.g., for preprints without DOIs)

### Required and recommended fields

For **articles**:
- Required: `author`, `title`, `journal`, `year`
- Recommended: `volume`, `number`, `pages`, `doi`

For **books**:
- Required: `author` or `editor`, `title`, `publisher`, `year`
- Recommended: `edition`, `doi`, `isbn`

For **incollection** (book chapters):
- Required: `author`, `title`, `booktitle`, `publisher`, `year`
- Recommended: `editor`, `pages`, `doi`

For **unpublished/preprints**:
- Required: `author`, `title`, `year`
- Recommended: `doi`, `note` (e.g., "Preprint on bioRxiv")

For **software and datasets**:
- Preserve verified creators (including corporate or consortium authors), title,
  release date/year, version or accession, repository/publisher, and DOI or other
  locator where available. Do not invent absent fields.
- Use the entry type supported by the project's citation renderer; `@misc` with
  version/accession information in `note` is a portable BibTeX fallback. Check the
  rendered citation before adopting richer software/data entry types or fields.

### Formatting conventions

- Use standard BibTeX entry types: `@article`, `@book`, `@incollection`, `@inproceedings`, `@phdthesis`, `@misc`, `@unpublished`
- Use `and` to separate authors in the `author` field
- Use LaTeX-encoded special characters: `{\"o}` for ö, `{\o}` for ø, `{\'e}` for é, etc.
- Keep one field per line, with consistent indentation
- End each field line with a comma
- Use double braces for the `journal` field only when needed to preserve exact capitalization

Example of a well-formatted entry:

```bibtex
@article{Dunn2008,
  author  = {Dunn, Casey W. and Hejnol, Andreas and Matus, David Q. and Pang, Kevin and Browne, William E. and Smith, Stephen A. and Seaver, Elaine and Rouse, Greg W. and Obst, Matthias and Edgecombe, Gregory D. and S{\o}rensen, Martin V. and Haddock, Steven H. D. and Schmidt-Rhaesa, Andreas and Okusu, Akiko and Kristensen, Reinhardt M{\o}bjerg and Wheeler, Ward C. and Martindale, Mark Q. and Giribet, Gonzalo},
  title   = {Broad phylogenomic sampling improves resolution of the animal tree of life},
  journal = {Nature},
  year    = {2008},
  volume  = {452},
  number  = {7188},
  pages   = {745--749},
  doi     = {10.1038/nature06614},
}
```

## Workflow for adding references

1. **Obtain the reference from a reliable source** — publisher website, PubMed, or CrossRef. Do not reconstruct citations from memory.
2. **Verify the full author list** — check the original publication. If the source only provides abbreviated authors, look up the full list before adding the entry.
3. **Apply title capitalization rules** — identify words needing curly-brace protection.
4. **Remove excluded fields** — strip `abstract`, `keywords`, `file`, and other unnecessary fields.
5. **Verify entry key uniqueness** — ensure the key doesn't conflict with existing entries in the `.bib` file.
6. **Check for duplicates** — search the `.bib` file for the same DOI or a similar author/year/title combination before adding.

## Workflow for editing existing references

When editing entries already in a `.bib` file:

- **Do not modify fields you are not specifically asked to change.** Even if formatting differs slightly from these conventions, leave existing correct data alone unless the user requests cleanup.
- **Never replace a full author list with an abbreviated one.**
- **Never add a DOI, title, or other substantive field by guessing.** If you believe a field is wrong or missing, flag it with a `% TODO` comment and inform the user.
- **When fixing capitalization**, only add curly braces around words that clearly need protection — do not wrap ambiguous cases without confirming.

## Checking and validating `.bib` files

When asked to review a `.bib` file, check for:

1. Truncated author lists (look for "and others", "et al", or suspiciously short lists for multi-author papers)
2. Missing curly braces on proper nouns, tool names, and acronyms in titles
3. Presence of `abstract` or other excluded fields
4. Missing required fields for each entry type
5. Duplicate entries (same DOI or very similar author/title/year)
6. Malformed LaTeX special characters
7. Inconsistent entry key formatting
