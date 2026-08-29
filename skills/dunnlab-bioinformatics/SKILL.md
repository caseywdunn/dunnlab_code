---
name: dunnlab-bioinformatics
description: >
  Bioinformatics workflow conventions for the Dunn Lab. Use when building
  or modifying sequence analysis pipelines, phylogenetics, gene annotation,
  or multi-species comparative analyses. Covers data hygiene, tool defaults,
  and naming conventions.
---

# Dunn Lab Bioinformatics Workflows

Follow these conventions for bioinformatics projects. This skill builds on `dunnlab-defaults` (coding standards, project structure, orchestration) and `dunnlab-new-project` (scaffolding) — apply those skills as well when starting or structuring a bioinformatics project.

## Raw data is immutable

**Never modify raw data files.** Raw data lives in `data/raw/` or is referenced from an external source and must remain byte-for-byte identical to what was originally obtained.

All transformations produce derivative files in `data/processed/` (or a descriptive subdirectory). Each processing step should be scripted and reproducible so the processed files can be regenerated from raw data at any time.

## Input validation

Validate all input files before processing. Catch problems early rather than debugging cryptic failures downstream.

- **FASTA/FASTQ**: Check for valid headers, consistent line wrapping, no illegal characters in sequences, no duplicate sequence IDs, and non-empty sequences.
- **GFF/GTF**: Verify tab-delimited structure, required columns, valid strand/phase values, and that coordinates are within sequence bounds.
- **Newick/tree files**: Verify balanced parentheses and parseable structure.
- **CSV/TSV metadata**: Check for expected columns, consistent delimiters, and no encoding issues.

Use BioPython parsers where possible — they will raise on malformed records. For tabular formats, use `pandas` with strict dtype enforcement. Report clear error messages that identify the problematic file and line/record.

## Compressed file handling

Bioinformatics files are often distributed and stored gzip-compressed (`.fasta.gz`, `.fastq.gz`, `.tsv.gz`). Handle compressed inputs transparently — detect `.gz` extensions and decompress on the fly using Python's `gzip` module or BioPython's `SeqIO.parse(gzip.open(...))`. Never require the user to decompress files manually as a preprocessing step. Most bioinformatics tools (MAFFT, DIAMOND, etc.) also accept gzipped input natively.

## Gene name sanitization

When producing derivative datasets, sanitize gene names and identifiers in two steps:

1. **Optional regex extraction**: Always provide the user with an option to specify a regex with a capture group to extract or transform gene IDs before sanitization. This allows stripping prefixes (e.g., `^maker-.*?-(.+)$`), removing version suffixes (e.g., `^(.+)\.\d+$`), or extracting IDs from complex headers (e.g., `^.*\|(.+)$`). Apply this regex first, before character sanitization.
2. **Character sanitization**: Remove or replace characters that are problematic in downstream tools: spaces, parentheses, colons, semicolons, commas, quotes, pipes, and shell-special characters. Replace problematic characters with underscores (`_`). Collapse runs of multiple underscores to a single one.

After both steps:
- Log all name transformations so the mapping back to original names is preserved (write a `name_mapping.tsv` with `original`, `regex_extracted`, and `sanitized` columns).
- Validate that sanitized names are still unique — raise an error if sanitization creates collisions.

## Multi-species analyses — globally unique gene IDs

When integrating datasets from multiple species, gene IDs must be globally unique. Before merging any cross-species data, rename gene IDs using the convention:

```
Genus_species@gene_id
```

For example: `Homo_sapiens@BRCA1`, `Mus_musculus@Brca1`, `Nematostella_vectensis@NVE12345`.

Rules:
- The species prefix uses the full binomial with an underscore: `Genus_species`.
- The `@` separator is chosen because it does not appear in standard gene IDs and is not a shell metacharacter.
- Apply this renaming to FASTA headers, annotation tables, tree tip labels, and any other files that reference gene IDs.
- Maintain a mapping file (`species_gene_mapping.tsv`) with columns: `species`, `original_id`, `global_id`.
- Apply sanitization (above) to the `gene_id` portion before prefixing.

## Gene annotation

Annotate genes using both of these tools:

- **EggNOG-mapper** — for orthology-based functional annotation (GO terms, KEGG, COG categories).
- **PROST** — for structure-based remote homology detection and annotation.

Run both and integrate results. Where annotations conflict, retain both with their source labeled. Store annotation results in `results/annotations/` with clear filenames indicating the tool and input (e.g., `eggnog_Genus_species.tsv`, `prost_Genus_species.tsv`).

## Default bioinformatics tools

Use these tools unless there is a specific reason to choose an alternative:

| Task | Tool | Notes |
|------|------|-------|
| Multiple sequence alignment | **MAFFT** | Use `--auto` for general use; `--linsi` for high-accuracy on smaller sets |
| Phylogenetic inference | **IQ-TREE 3** | Use ModelFinder (`-m MFP`) for automatic model selection on deep searches, or a fixed model such as `Q.PFAM+F+R6` for faster protein searches (e.g. monophyly masking of gene trees). Use ultrafast bootstrap (`-B 1000`) for support values |
| Alignment trimming | **trimAl** | Trim poorly-aligned regions before tree inference; use `-automated1` for general use |
| Sequence similarity search | **DIAMOND** | Use `blastp` or `blastx` mode as appropriate; significantly faster than BLAST for large-scale searches |
| ORF prediction | **TransDecoder** | Predict ORFs from transcriptomes; use `-S` for strand-specific data; retain primary isoforms (`.p1`) only |
| Completeness assessment | **BUSCO** | Assess transcriptome/proteome/genome completeness; use the appropriate lineage database (e.g. `metazoa_odb12`). Confirm the lineage name against `busco --list-datasets` — the `odb` version advances with BUSCO releases |

Install all tools via **bioconda** when possible (consistent with `dunnlab-defaults`).

## Duplicate and paralog resolution

When gene trees contain multiple sequences from the same species (paralogs, isoforms, or assembly artifacts), resolve them before downstream analysis. Two complementary strategies:

- **Monophyletic pruning** (phylogenomic workflows): When within-species duplicates form a monophyletic clade in a gene tree, retain a single representative — preferring the sequence with the lowest long-branch score or, if scores are similar, the longest sequence. Use tools like **PhyKIT** for long-branch score calculation and **ETE3** for tree manipulation.
- **Branch-length thresholding** (transcriptomic workflows): Collapse sequences from the same species that are separated by less than a branch-length threshold. Test multiple thresholds and evaluate with BUSCO to find the optimal collapse point. Retain the longest sequence from each collapsed group.

In both cases:
- Track which sequences were removed and why (write a pruning summary with columns: `gene`, `retained_id`, `removed_id`, `reason`).
- After pruning, validate that no within-species duplicates remain in gene trees intended for species-tree inference.
- Sequences not present in any gene tree cannot be phylogenetically validated — flag or exclude them depending on the analysis.

## Sequence orientation

When working with transcriptome data where strand orientation may be unknown, verify and correct sequence orientation before translation or alignment. Use DIAMOND `blastx` hits to infer orientation — compare query and subject coordinate order to determine if a reverse complement is needed. Apply this step when the user requests it or when the data source does not guarantee strand orientation.

## Summary tables

For multi-sample workflows, produce per-sample metrics at each processing stage and aggregate them into a single summary TSV (e.g., `results/sample_summary.tsv`). Include key quality metrics such as input sequence counts, filtering statistics, BUSCO completeness, and any tool-specific outputs. This provides at-a-glance quality assessment across all samples and makes it easy to identify outliers or failed samples.

## Contamination screening

Not required for every project, but when working with raw sequencing reads — especially from non-model organisms — consider screening for contamination before downstream analysis. Use **Kraken2** for taxonomic classification to detect human, bacterial, and other contaminant sequences. Map reads against human and rRNA references (e.g., SILVA) with **BWA** to quantify contamination levels. Apply this step when the user requests it or when contamination is a plausible concern (e.g., field-collected samples, mixed-species extractions).

## Project structure additions

Bioinformatics projects extend the standard `dunnlab-defaults` structure, for example:

```
project-name/
├── data/
│   ├── raw/              # Immutable original data
│   └── processed/        # Sanitized, renamed, validated derivatives
│       └── name_mapping.tsv
├── results/
│   ├── alignments/       # MAFFT output
│   ├── trees/            # IQ-TREE output
│   ├── searches/         # DIAMOND output
│   └── annotations/      # EggNOG and PROST output
├── scripts/
│   ├── validate_inputs.py
│   ├── sanitize_names.py
│   └── ...
└── environment.yml       # Include mafft, iqtree3, diamond, eggnog-mapper, etc.
```

## Environment setup

The `environment.yml` should include bioinformatics dependencies from bioconda:

```yaml
channels:
  - conda-forge
  - bioconda
  - defaults
dependencies:
  - python>=3.10
  - biopython
  - pandas
  - mafft
  - iqtree>=3
  - trimal
  - diamond
  - eggnog-mapper
  - busco
```

Pin `iqtree>=3` explicitly — bioconda still carries 2.x under the same package name, and the conventions above assume IQ-TREE 3.

Add PROST and any other tools as needed per project.
