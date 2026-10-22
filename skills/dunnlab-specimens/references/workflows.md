# Workflows

All commands are `python3 <skill>/tools/specimens.py <command>`, run from the project root. Start a project's `specimens/` directory from the skill's [`templates/`](../templates/).

## 1. Specimens the lab collects

1. **In the field,** record each specimen in `field_records.tsv` with its field ID (dive or station plus sampler, e.g. `D1399-SS10`), date, coordinates, depth, method, vessel, collector, preservation, and permit. Record each tube in `tubes.tsv` with its label and contents. Photograph specimens, and name the photo files by field ID.
2. **Choose the specimen key** when analysis begins: the YPM voucher if the specimen is catalogued, otherwise the field ID. Register the key in `crosswalk.tsv` with its identifiers.
3. **Catalogue at YPM.** Add each catalog number to `crosswalk.tsv`, as `specimen_voucher` or, if the key is already the field ID, as `alias_voucher`, and to `field_records.tsv`.
4. **Record samples and libraries** in `samples.tsv` and `libraries.tsv`, with the tubes they occupy.
5. **Fetch the museum records** (`fetch-museum`) and the taxa (`fetch-worms`); record determinations; then build, check, and validate. Fix disagreements with YPM in YPM's database.
6. **Deposit:** `export-biosample` writes the BioSample Invertebrate.1.0 table. Review it, fill any value marked `missing`, and submit. After submission, add the BioSample, experiment, and run accessions to `samples.tsv` and `libraries.tsv`, then fetch them back (`fetch-insdc`), so the build confirms the archive matches the lab's records.

## 2. Public data from others

1. **Sequence data:** `fetch-insdc PRJNA… SAMN…` fetches BioSamples and runs. Add a sample row for each BioSample and a library row for each experiment. For specimen keys, use the voucher if the BioSample has one, otherwise the BioSample accession. Register each in `crosswalk.tsv`.
2. **Occurrence data,** including iNaturalist: request a GBIF download, then `fetch-gbif-download <key>`. Cite the DOI.
3. **Cross-check:** for each voucher, also run `fetch-museum` for the holding museum where it is in GBIF or LUX. Compare collecting data, and record conflicts rather than choosing silently.
4. Build, check, validate, and review. Expect gaps: public records often lack depth, tissue, or a voucher.

## 3. The lab's own archived data

Treat archived data as public data (workflow 2), but link it to the lab's records: the voucher in the BioSample connects it to YPM, and the lab's field records and earlier project tables are sources for missing values. A specimen reused across papers keeps its YPM voucher as the stable link; each project's key follows the rule in force when that project's analysis began.

## 4. Curation

Follow the review loop in [Curation](curation.md). It is metadata-only: rebuilding never touches sequence data, and analysis inputs stay frozen because the analysis reads its own committed copy of `manifest.tsv`, not `generated/manifest.tsv`. Refreshing that copy, and the figures or summaries that use it, is a separate, explicit step in the analysis workflow.

## 5. Publication

- **Specimen table:** produce the paper's specimen table from `generated/specimens.tsv` and `manifest.tsv` with a script in the analysis workflow. `dunnlab-manuscript` covers how it enters the manuscript.
- **Deposits:** confirm every sequenced sample has a BioSample with its voucher, and every specimen used is catalogued, or its absence explained.
- **Citations:** cite GBIF download DOIs and the archives used, following `dunnlab-biblio`.
- **Upstream corrections:** confirm the corrections marked `to_submit` have been sent to YPM.
