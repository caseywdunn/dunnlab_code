---
name: dunnlab-bioinformatics
description: >
  Design sequence, phylogenetic, annotation, and comparative analyses using Dunn
  Lab tool preferences, biological input checks, and identifier conventions.
  Use for bioinformatics method and tool choices; general workflow architecture
  belongs to dunnlab-workflow-design.
---

# Dunn Lab Bioinformatics Design

Use this skill for biological methods, tool settings, identifiers, and scientific checks. Apply the relevant guidance during exploration as well as later analysis. The preferred tools are defaults for a requested analysis, not a requirement to add every analysis below.

For dependencies, configuration, provenance, output reuse, and reproduction, use [dunnlab-workflow-design](../dunnlab-workflow-design/SKILL.md). Scientific questions and readiness for reporting belong to [dunnlab-lifecycle](../dunnlab-lifecycle/SKILL.md); coding and environment conventions belong to [dunnlab-defaults](../dunnlab-defaults/SKILL.md). Repository scaffolding and HPC execution belong to their respective skills when needed.

Read [Tool and analysis preferences](references/tools.md) when choosing or configuring alignment, tree inference, annotation, ORF prediction, completeness assessment, duplicate resolution, orientation, or contamination screening. Preserve a project's justified alternatives and record consequential departures from these defaults.

## Biological inputs and checks

Establish the biological unit and expected input type before choosing a method: reads, transcripts, coding sequences, proteins, genes, or orthogroups. Keep gene, transcript, and protein identifiers distinguishable. Record the relevant species, assembly/annotation release, sequence type, coordinate conventions, and reference database release with the analysis inputs.

Validate inputs before the consuming stage, including relationships between files:

- **FASTA/FASTQ:** Check non-empty sequences, usable and unique record IDs, and the alphabet expected for nucleotide, protein, or aligned data. For FASTQ, also check sequence/quality lengths and paired-read identity when relevant. Valid FASTA need not have uniform line wrapping.
- **GFF/GTF:** Check the nine-column structure, strand/phase values as appropriate to the feature, sequence IDs, and coordinates against the matching reference. Preserve the format's coordinate and attribute semantics during conversion.
- **Trees and alignments:** Parse the tree, check unique tip labels, and reconcile them with sequence and species mappings. Check equal aligned sequence lengths and required taxon coverage before tree inference.
- **Metadata tables:** Check expected columns, types, uniqueness of keys, and join cardinality. Detect unmatched identifiers rather than silently losing samples or sequences.

Prefer Biopython for supported sequence/tree formats and pandas for tables. Parsing alone does not establish these biological invariants; add explicit checks for the conditions the analysis relies on. Errors should identify the file and offending record or identifier.

For single-cell expression analyses, prefer Scanpy when Python fits the task;
retain R methods such as Seurat when their capabilities are needed. Choose the
library for the biological method rather than adding a second implementation.

Support gzip-compressed inputs without requiring manual decompression. Use text-mode gzip streams with parsers, or a workflow-managed derivative for tools that require an uncompressed file. Check the selected tool's actual compression support; DIAMOND supports gzip queries, but this is not universal across bioinformatics tools.

## Identifier transformations

When producing sanitized derivative identifiers:

1. Provide an optional regex with a capture group for extraction before sanitization, such as `^(.+)\.\d+$` to remove a version suffix. Leave extraction disabled unless selected for the dataset; check unmatched and empty results.
2. Replace characters problematic for the downstream formats/tools with underscores: spaces, parentheses, colons, semicolons, commas, quotes, pipes, and shell-special characters. Collapse repeated underscores.
3. Write `name_mapping.tsv` with `original`, `regex_extracted`, and `sanitized` columns. Check that transformed IDs are non-empty and unique; fail on collisions.

Apply mappings consistently to sequence headers, annotation tables, tree tips, and other files referencing the transformed IDs. Sanitization does not replace correct shell quoting.

### Multi-species gene IDs

Before merging cross-species datasets, use globally unique IDs with the lab convention:

```text
Genus_species@gene_id
Homo_sapiens@BRCA1
Nematostella_vectensis@NVE12345
```

Use the full binomial with an underscore for the species prefix, and sanitize the gene ID portion before prefixing. Reserve `@` as the separator and check source IDs for conflicts. For unnamed species or datasets requiring specimen/assembly distinctions, document an unambiguous prefix in the species mapping rather than inventing a binomial or allowing collisions.

Maintain `species_gene_mapping.tsv` with `species`, `original_id`, and `global_id` columns, linked to any sanitization mapping. Carry the resulting IDs through FASTA, annotations, trees, and all cross-file joins. When multiple transcripts or proteins are retained for one gene, preserve their distinct IDs and gene relationships.

## Quality summaries

For multi-sample workflows, aggregate metrics from the stages actually run into a per-sample TSV, such as `results/sample_summary.tsv`. Include input/retained sequence counts, filtering and mapping losses, and relevant tool metrics such as BUSCO completeness. Represent failed or unassessed samples explicitly so they cannot disappear from comparisons. Use these summaries to identify outliers and evaluate biological consequences of filtering; do not add unrelated analyses merely to populate a table.
