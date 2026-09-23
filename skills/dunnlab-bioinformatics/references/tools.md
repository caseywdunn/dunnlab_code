# Bioinformatics tool and analysis preferences

Use these defaults for analyses within the task's scope. Choose alternatives when justified by the data or scientific question, and retain the reason with the analysis. Record reference database releases alongside tool versions and settings.

## Core tools

| Task | Preferred tool | Use details |
|------|----------------|-------------|
| Multiple sequence alignment | **MAFFT** | `--auto` for general use; L-INS-i (`--localpair --maxiterate 1000`) for high accuracy on smaller, locally alignable sets. See the [MAFFT manual](https://mafft.ddbj.nig.ac.jp/alignment/software/manual/manual.html). |
| Phylogenetic inference | **IQ-TREE 3** | ModelFinder (`-m MFP`) for deep searches; a fixed model such as `Q.PFAM+F+R6` for faster protein searches, including gene trees for monophyly masking. Use ultrafast bootstrap (`-B 1000`) when estimating support. Distinguish exploratory approximations from settings used for reported inference. |
| Alignment trimming | **trimAl** | Prefer `-automated1` when trimming poorly aligned regions before tree inference. Assess retained sites and taxa so trimming does not silently remove the evidence needed for the analysis. |
| Sequence similarity search | **DIAMOND** | `blastp` for proteins or `blastx` for translated nucleotide queries against proteins. Choose sensitivity and hit-retention settings for the biological use, including whether multiple homologs are needed. |
| ORF prediction | **TransDecoder** | Use for transcriptomes. Use `-S` only when transcripts are already oriented to the sense strand. Prefer one best ORF per transcript with `--single_best_only` when that is the desired output. This does not select one transcript isoform per gene; `.p1` is an ORF identifier suffix, not evidence of a primary isoform. See the [TransDecoder usage guide](https://github.com/TransDecoder/TransDecoder/wiki) and [ORF-selection option](https://github.com/TransDecoder/TransDecoder/blob/master/util/TransDecoder.Predict). |
| Completeness assessment | **BUSCO** | Select the mode for transcriptome, proteome, or genome and an appropriate lineage. Confirm available lineage names with `busco --list-datasets`; `metazoa_odb12` is an example, not a permanent database requirement. Keep lineage and database release consistent across comparisons. |

Prefer **bioconda** for these tools when available, within the environment conventions in [dunnlab-defaults](../../dunnlab-defaults/SKILL.md). Include only dependencies the project uses. Require IQ-TREE major version 3 explicitly when using these conventions (for example, `iqtree>=3` in a conda specification), and verify the installed version. Handle PROST or other dependencies unavailable through the chosen channel with a documented project-specific installation.

## Functional annotation

For comprehensive functional annotation, prefer both:

- **EggNOG-mapper:** Orthology-based functional annotation, including GO, KEGG, and COG categories.
- **PROST:** Structure-based remote homology detection and annotation.

Integrate their results with source labels; retain conflicting annotations rather than silently choosing one. Keep annotation evidence distinguishable from inferred function. Store results with filenames indicating tool and input, such as `results/annotations/eggnog_Genus_species.tsv` and `prost_Genus_species.tsv`. A task limited to a particular annotation source or question need not run both tools.

## Duplicate and paralog resolution

Resolve within-species duplicates when the downstream analysis requires a representative per species. Determine whether candidates represent paralogs, isoforms, or assembly artifacts before interpreting the result as orthology; multiple copies can be biologically meaningful.

- **Monophyletic pruning for phylogenomics:** When within-species duplicates form a monophyletic gene-tree clade, prefer the sequence with the lowest long-branch score, using length as a tie-breaker when scores are similar. Prefer **PhyKIT** for long-branch scores and **ETE3** for tree manipulation. Make the tie policy explicit.
- **Branch-length thresholding for transcriptomic workflows:** Group sequences from the same species within a defined tree-distance threshold, retaining the longest in each group. Define the distance and grouping criterion so chained pairwise matches cannot silently change the intended threshold. Compare multiple thresholds and evaluate BUSCO completeness alongside retained diversity and the downstream biological objective.

Write a pruning summary with `gene`, `retained_id`, `removed_id`, and `reason`. Check for remaining within-species duplicates when preparing single-copy gene trees for species-tree inference. Unresolved nonmonophyletic copies need an explicit selection/exclusion decision; do not force a single-copy result without biological justification. Flag sequences absent from gene trees, or exclude them when phylogenetic validation is required by the analysis.

## Sequence orientation

When transcript orientation is unknown and affects translation or alignment, or when requested, use DIAMOND `blastx` evidence to assess it. Request `qframe` (or a supported query-strand field); negative query frames indicate reverse-strand matches. Query coordinate direction can also provide strand information. The subject is a protein, so comparing query and subject coordinate directions is not the orientation rule. See [DIAMOND's documented query and output fields](https://github.com/bbuchfink/diamond/wiki/3.-Command-line-options).

Use a stated policy for selecting credible hits and handling conflicting strand evidence. Reverse-complement a derivative only when supported, preserve a sequence-level orientation record, and leave no-hit or ambiguous cases explicitly unresolved. Apply sense-strand-only ORF prediction only to inputs for which that assumption is justified.

## Contamination screening

Consider screening raw reads when requested or when contamination is plausible, such as field-collected or mixed-species material. Prefer **Kraken2** for taxonomic classification. Use **BWA** mapping to relevant human or rRNA references, such as **SILVA**, when those contamination measurements address the question. Specify the reference/database and interpretation criteria; biological associates and homologous sequences are not automatically contaminants. Preserve screening evidence separately from any decision to filter reads.
