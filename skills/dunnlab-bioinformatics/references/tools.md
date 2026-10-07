# Bioinformatics tool and analysis preferences

Use these defaults for analyses within the task's scope. Choose alternatives when justified by the data or scientific question, and retain the reason with the analysis. Record reference database releases alongside tool versions and settings.

## Core tools

| Task | Preferred tool | Use details |
|------|----------------|-------------|
| Multiple sequence alignment | **MAFFT** | `--auto` for general use; L-INS-i (`--localpair --maxiterate 1000`) for high accuracy on smaller, locally alignable sets. See the [MAFFT manual](https://mafft.ddbj.nig.ac.jp/alignment/software/manual/manual.html). |
| Phylogenetic inference | **IQ-TREE 3** | See [IQ-TREE](#iq-tree) for models, replicate searches, and constrained-tree topology tests. |
| Alignment trimming | **trimAl** | Prefer `-automated1` when trimming poorly aligned regions before tree inference. Assess retained sites and taxa so trimming does not silently remove the evidence needed for the analysis. |
| Sequence similarity search | **DIAMOND** | `blastp` for proteins or `blastx` for translated nucleotide queries against proteins. Choose sensitivity and hit-retention settings for the biological use, including whether multiple homologs are needed. |
| ORF prediction | **TransDecoder** | Use for transcriptomes. Use `-S` only when transcripts are already oriented to the sense strand. Prefer one best ORF per transcript with `--single_best_only` when that is the desired output. This does not select one transcript isoform per gene; `.p1` is an ORF identifier suffix, not evidence of a primary isoform. See the [TransDecoder usage guide](https://github.com/TransDecoder/TransDecoder/wiki) and [ORF-selection option](https://github.com/TransDecoder/TransDecoder/blob/master/util/TransDecoder.Predict). |
| Completeness assessment | **BUSCO** | Select the mode for transcriptome, proteome, or genome and an appropriate lineage. Confirm available lineage names with `busco --list-datasets`; `metazoa_odb12` is an example, not a permanent database requirement. Keep lineage and database release consistent across comparisons. |

Prefer **bioconda** for these tools when available, within the environment conventions in [dunnlab-coding-defaults](../../dunnlab-coding-defaults/SKILL.md). Include only dependencies the project uses. Require IQ-TREE major version 3 explicitly when using these conventions (for example, `iqtree>=3` in a conda specification), and verify the installed version. Handle PROST or other dependencies unavailable through the chosen channel with a documented project-specific installation.

## IQ-TREE

Use **IQ-TREE 3** (`iqtree3`) for maximum-likelihood tree inference. Give each analysis its own `--prefix` so runs do not overwrite one another, and record the version, model, seed, and full command with the outputs. See the [IQ-TREE documentation](https://iqtree.github.io/doc/).

### Models and support

Use ModelFinder (`-m MFP`) for deep searches. For faster protein searches, such as gene trees for monophyly masking, use a fixed model such as `Q.PFAM+F+R6`. Use ultrafast bootstrap (`-B 1000`) when estimating support. Distinguish exploratory approximations from the settings used for reported inference.

### Replicate searches

ML tree search is heuristic, and a single search can stop at a local optimum. When the likelihoods of searches will be compared, run multiple independent searches with `--runs NUM`. IQ-TREE's own default is 1; the lab default is `--runs 5`. Use more runs for large or difficult data, or when the runs disagree.

With `--runs`, the `.treefile` holds the tree from the best-scoring run. `.runtrees` holds each run's tree prefixed by `[ lh=... ]`, and the `MULTIPLE RUNS` section of `.iqtree` lists each run's log-likelihood. Check how many runs reached the best log-likelihood. If only one run reached it, the search may not have converged, so increase `--runs`.

`--runs` (greater than 1) and `-z` cannot be used in the same IQ-TREE call; IQ-TREE exits with an error. They belong to different steps: `--runs` to tree searches, and `-z` to evaluating a fixed set of trees, as in the topology test below.

### Constrained searches and AU tests

Use constrained searches with the approximately unbiased (AU) test to ask whether the data reject an alternative hypothesis relative to the ML tree. Follow the workflow in the [IQ-TREE tutorial on testing constrained trees](https://iqtree.github.io/doc/Advanced-Tutorial#testing-constrained-tree), with replicate searches added at each search step.

#### Constraint trees

Write each hypothesis as a Newick constraint tree for `-g`. Constraint trees can be multifurcating and need not include all taxa; check that their tip labels match the alignment. Constraints are unrooted: `((A,B),(C,D));` only separates {A,B} from {C,D}. To force a clade, include a taxon outside it, for example `((A,B),(C,D),E);`. Check that each constraint expresses the intended hypothesis and nothing more.

#### Searches

Use the same alignment, partition scheme (if any), and fixed model (`-m`) for every search and for the test, so the log-likelihoods are comparable. If the model is selected with ModelFinder, select it once, for example from an unconstrained run, and pass that model to all later steps.

Run the unconstrained search and each constrained search with replicate searches:

```bash
iqtree3 -s aln.faa -m MODEL --runs 5 --seed 1 --prefix unconstr
iqtree3 -s aln.faa -m MODEL --runs 5 --seed 1 -g hyp1.nwk --prefix hyp1
iqtree3 -s aln.faa -m MODEL --runs 5 --seed 1 -g hyp2.nwk --prefix hyp2
```

Replicate searches matter in particular when the data carry little or no information about the constrained node. In that case the constrained and unconstrained searches are essentially the same problem. With one search each, which one finds the better tree is largely a matter of chance, and the constrained search regularly finds a better tree than the unconstrained one.

Before testing, check that the best unconstrained log-likelihood is at least as high as every best constrained log-likelihood. The unconstrained tree space contains every constrained space, so a constrained tree that scores higher means the unconstrained search did not find the ML tree. Increase `--runs` and rerun rather than testing these trees. Small differences within IQ-TREE's optimization tolerance are not evidence of a failed search.

#### Topology test

Concatenate the best tree from each search into one tree file in a recorded order. Keep a table mapping tree number to hypothesis.

```bash
cat unconstr.treefile hyp1.treefile hyp2.treefile > hypotheses.treels
iqtree3 -s aln.faa -m MODEL -z hypotheses.treels -n 0 -zb 1000 -au --prefix au_test
```

`-n 0` estimates the model parameters on an initial parsimony tree instead of running a tree search. `-zb` sets the number of RELL replicates, and 1000 is the recommended minimum. `-au` adds the AU test to the other RELL-based tests. Do not pass `--runs` to this call: replicate searches belong to the search steps above, and IQ-TREE rejects `--runs` together with `-z`.

#### Interpretation

Read the `USER TREES` section of the `.iqtree` file. A tree with `p-AU < 0.05` (marked `-`) is significantly rejected; failing to reject a tree is not support for it. Prefer the AU test over KH and SH: the KH test does not correct for multiple testing, and the SH test is too conservative when many trees are tested. IQ-TREE detects and omits duplicate topologies, and a constrained search can return the unconstrained topology when the data already satisfy the constraint, so check the tree-to-hypothesis mapping against the reported trees. Report `deltaL` and `p-AU` for each hypothesis, along with the model, the number of runs per search, and the number of RELL replicates.

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
