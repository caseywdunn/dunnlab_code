---
name: dunnlab-specimens
description: >
  Manage field-collected specimen and sample metadata with provenance: identifiers,
  vouchers, tubes, collecting data, taxonomy, and crosswalks among YPM/LUX, GBIF,
  iNaturalist, SRA/ENA, and lab records. Use when ingesting, curating, validating,
  or depositing specimen data.
---

# Dunn Lab Specimens

Many projects build on field-collected marine invertebrates: sequenced, examined morphologically, and placed in space and depth. This skill keeps their metadata traceable from the first field record through public archives and back into analyses. `dunnlab-bioinformatics` owns sequence identifiers and biological checks downstream; `dunnlab-workflow-design` owns the analysis workflow; `dunnlab-manuscript` owns how specimen tables reach a paper.

## Principles

- **Plain text, in the repository.** Every table is a TSV file that people and agents can read and diff. No database.
- **Raw data is immutable.** Downloads and field logs are kept exactly as received, with what was asked, when, and checksums. Integrated tables are computed from them and never edited by hand.
- **Every value has a source.** The build records, for each value, the source and the specific record it came from. Corrections record the original value, the new value, and the evidence.
- **Identity needs explicit evidence.** Records are joined only through matching identifiers or reviewed crosswalk entries. Taxon names and similar labels are never enough.
- **Disagreement is reported, not resolved silently.** When sources differ, the build chooses by a fixed precedence and lists every conflict for review.
- **Gaps stay visible.** A missing value is reported as "not recorded in the reviewed sources", never filled by inference from related rows.
- **YPM is the authority for specimens the lab collects.** Lasting corrections to those records go upstream to YPM, whose database feeds LUX and GBIF; the project's correction record tracks them until YPM reflects the change.

## What is recorded

Four linked levels, following the SRA model, plus tubes. See [Data model](references/data-model.md).

| Level | One row per | Key | Holds |
|---|---|---|---|
| Specimen | organism or lot, with its collecting event | `specimen_key` | voucher, field ID, taxonomy, date, place, depth, collector, method |
| Sample | tissue or part of one specimen (one BioSample) | `sample_id` | tissue, stage, sex, BioSample accession |
| Library | one sequencing library (one SRA experiment) | `library_id` | strategy, platform, experiment and run accessions |
| Tube | physical tube | `tube_id` | contents, the sample or library, parent tube |

Field names follow the NCBI BioSample attributes where one exists, and Darwin Core where SRA has none. [`schema/fields.tsv`](schema/fields.tsv) is the field dictionary: type, format, whether it is required, and the matching field in BioSample, ENA, Darwin Core/GBIF, LUX, and iNaturalist. [Crosswalks](references/crosswalks.md) explains the mappings and their pitfalls.

## The specimen key

`specimen_key` identifies a specimen in analyses: FASTA headers, workflow wildcards, trees, and file names.

- Use the **museum voucher** if the specimen has one when analysis begins, written as the INSDC voucher with `:` replaced by `_` (`YPM:IZ:110226` becomes `YPM_IZ_110226`). Colons are not allowed, because Newick trees read them as branch lengths.
- Otherwise use the **field ID** (`D1399-SS10`). For public data without a voucher, use the **BioSample accession**.
- **A key must be unique across all of the lab's work.** Field IDs are often unique only within a trip: `BW` marks a blue-water SCUBA dive, and `BW3-4` is dive 3, specimen 4 of that trip. As a key, such an ID must include the trip, e.g. `26Mar19-BW3-39` or `KiloMoana2018-BW7-4`.
- **Within a project, the key never changes once used.** A voucher assigned later, a re-catalogued specimen, or a transfer to another museum is recorded in `crosswalk.tsv` as an identifier of the same key. A later project chooses its own key by the rule above, so it may use a voucher where an earlier project used the field ID; the voucher links the specimen across projects.
- One specimen may have several samples and BioSamples, for example separate zooids of one siphonophore. They share the specimen key.

## Taxonomy

WoRMS is the authority for names; each determination carries its AphiaID. The NCBI taxonomy ID is required alongside it, since INSDC submissions use it, and WoRMS provides the link. GBIF taxon keys are recorded on GBIF ingest but are not authoritative. Names change: a specimen collected as one species turns out to be another, or undescribed; a taxonomic revision renames a species after its data were deposited. So each specimen carries three identifications:

- **`initial_identification`:** the first determination, usually made at collection.
- **`public_identification`:** the names under which public records list it, e.g. `Nanomia sp. (insdc)`. These are generated from the sources and kept as they are, since the archives keep their deposited names.
- **`scientific_name`:** the current determination.

Determinations are a dated history in `determinations.tsv`, with the verbatim name, any qualifier (cf., aff., sp.), the identifier, the date, and the **evidence**, such as a COI barcode, morphology, or a revision with its citation. One row is marked initial and one current. `validate` warns when the current identification differs from the initial or a public one and no evidence is recorded. Undescribed or incompletely identified taxa use NCBI's practice: the lowest confident taxon with "sp." and the voucher, for an informal name such as `Apolemia sp. 3 CWD-2005`. Use the same informal name for the same taxon across projects.

## Tools

[`tools/specimens.py`](tools/specimens.py) uses only Python's standard library. Run it from the project root; tables live in `specimens/`.

| Command | Does |
|---|---|
| `fetch-museum YPM:IZ:110226 ...` | GBIF and LUX records for vouchers, confirming institution, collection, and number inside each record |
| `fetch-insdc SAMN... PRJNA...` | BioSample records from NCBI and run tables from ENA |
| `fetch-gbif-download <key>` | an existing GBIF download, with its DOI |
| `fetch-worms <names>` / `--from-determinations` | WoRMS matches and NCBI taxonomy IDs, for review |
| `build` | integrate sources and curation into `generated/` |
| `check-obis` | distance to shore and bathymetry for each point, and each taxon's recorded depths |
| `validate` | check the generated tables; exit 1 on errors |
| `export-biosample` | an NCBI BioSample Invertebrate.1.0 table |

Fetching only adds new folders under `sources/`. `build` and `validate` work offline and run quickly, so curation can be rebuilt at any time without touching sequence data. Results are in `generated/`: the integrated `specimens.tsv`, `samples.tsv`, `libraries.tsv`, and `tubes.tsv`; a library-level `manifest.tsv` for analyses; `provenance.tsv`; and the review reports `conflicts.tsv`, `missing_fields.tsv`, `unmatched_records.tsv`, `catalog_audit.tsv`, `build_problems.tsv`, and `validation.tsv`.

## Workflows

Read [Workflows](references/workflows.md) for the steps of each:

1. **Specimens the lab collects:** field records and tubes, then cataloguing at YPM, sequencing, and deposit to SRA or ENA.
2. **Public data from others:** SRA or ENA accessions, and GBIF downloads including iNaturalist observations.
3. **The lab's own archived data,** reused in a new project.
4. **Curation:** review the reports, add crosswalk entries, corrections, and determinations, rebuild, and validate.
5. **Publication:** a specimen table for the paper and BioSample records for deposit.

When ingesting a specimen, query every relevant source and compare them; see [Sources](references/sources.md). Curation rules for identity, corrections, depth, coordinates, tissue, notes, and catalog audits are in [Curation](references/curation.md).

## Validation

`validate` checks that identifiers are well formed and unique at their level, joins between tables resolve, coordinates are in range, depth bounds are ordered, dates are ISO 8601, tube labels match their declared type, and each depth set by convention names the convention. After `check-obis`, it also warns when a point is on land, a depth exceeds the bathymetry, or a depth lies outside the depths at which the taxon has been recorded. Treat warnings as items to review, not automatic errors.

Changes to metadata can change figures or summaries. The analysis workflow never reads `generated/` directly, because every `build` rewrites it. It reads a committed copy of `manifest.tsv` among its own inputs, and copying a rebuilt manifest there is the explicit refresh step; its diff shows what changed. After curation, confirm that frozen analysis inputs are unchanged.
