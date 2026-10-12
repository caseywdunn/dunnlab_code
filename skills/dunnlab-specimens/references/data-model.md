# Data model

## Layout

```text
specimens/
├── sources/                 # raw retrievals; never edited
│   ├── gbif_occurrence/<timestamp>_<slug>/   # files + retrieval.json
│   ├── gbif_download/
│   ├── lux/
│   ├── insdc/
│   ├── worms/
│   └── obis/
├── field_records.tsv        # the lab's field log for specimens it collected
├── crosswalk.tsv            # reviewed identifiers for each specimen key
├── corrections.tsv          # value-level corrections with evidence
├── determinations.tsv       # identification history
├── samples.tsv              # samples (tissues or parts)
├── libraries.tsv            # sequencing libraries
├── tubes.tsv                # physical tubes
└── generated/               # rebuilt by tools/specimens.py; never edited
```

Copy the header-only files in [`templates/`](../templates/) to start. Field definitions, formats, and requirements are in [`schema/fields.tsv`](../schema/fields.tsv).

Each `retrieval.json` records the source, the UTC time, every request URL, and a SHA-256 checksum for each file, plus the DOI for a GBIF download. Later retrievals of the same record are added beside earlier ones rather than replacing them.

## Edited tables

### `field_records.tsv`

The lab's own collecting record: one row per specimen, keyed by `field_id`, with the voucher once assigned.

Field IDs record how and where a specimen was collected, and are often meaningful only within a trip. `BW` means a blue-water SCUBA dive: `BW3-4` is dive 3, specimen 4. ROV specimens are named by dive and sampler, e.g. `D1399-SS10`. Subsamples get suffixes such as `.1` and `.2`. A bare trip-specific ID such as `BW3-4` is not a GUID: record the trip in `event_id`, and include it in the field ID whenever the field ID becomes a specimen key (`26Mar19-BW3-39`). Record each trip's naming convention with its field records. It is a source like any other: when it disagrees with the museum catalog, the build reports the conflict, and the fix goes to whichever record is wrong.

### `crosswalk.tsv`

The registry of specimen keys and their identifiers. Every specimen key appears with at least one confirmed identifier.

| Column | Contents |
|---|---|
| `specimen_key` | the frozen key |
| `id_type` | `specimen_voucher`, `alias_voucher` (earlier or later catalog numbers, transfers), `field_id`, `biosample_accession`, `gbif_id`, `lux_uri`, or `occurrence_url` |
| `id_value` | the identifier as written by its source |
| `status` | `confirmed`, `candidate`, or `rejected`; only `confirmed` rows are used |
| `evidence`, `source_locator` | why the identifier belongs to this specimen, and where that is shown |
| `reviewed_by`, `date`, `notes` | who confirmed it and when |

Vouchers match across formatting differences: case, separators, and leading zeros (`YPM IZ 035362` and `YPM:IZ:35362`). Institution and collection codes must still agree. An identifier mapped to two keys is an error.

### `corrections.tsv`

One row per corrected value: `entity` (`specimen`, `sample`, or `library`), `key`, `field`, `original_value`, `value`, `source`, `source_locator`, `notes`, `recorded_by`, `date`, and `upstream`. The build applies a correction only if `original_value` equals the value it would otherwise have chosen; otherwise it reports an error, because the underlying data changed and the correction needs review. `upstream` tracks corrections to YPM records: `none`, `to_submit`, `submitted <date>`, or `applied`. Once YPM reflects the change, the correction no longer changes anything and can be marked `applied`.

### `determinations.tsv`

The identification history: `specimen_key`, `verbatim_name`, `scientific_name`, `identification_qualifier`, `informal_name`, `aphia_id`, `ncbi_taxid`, `identified_by`, `date_identified`, `initial` (`yes` for the first determination; otherwise the earliest dated one counts), `current` (`yes` for exactly one row per specimen), `evidence`, `source`, and `notes`. The current determination supplies the specimen's taxonomy and `identification_evidence`; the initial one supplies `initial_identification`. Names in public records become `public_identification`, generated rather than edited. A specimen without a current determination uses its strongest public name and is listed in `missing_fields.tsv`.

### `samples.tsv`, `libraries.tsv`, `tubes.tsv`

Authored by the lab. Blank fields are filled from matched public records, and corrections apply as for specimens. A sample is matched to a BioSample by `biosample_accession`, or, if that is blank, by the BioSample's `sample_name` equalling the sample ID or one of its tube IDs. A library is matched to SRA data by `experiment_accession`.

Tubes record the physical chain: which tube holds which sample or library, and which tube each aliquot or extract came from (`parent_tube_id`). Lab tube labels have three forms:

| `tube_id_type` | Form | Example |
|---|---|---|
| `handwritten` | initials and an index | `CWD16` |
| `dunnlab_datamatrix` | `DunnLab` and six digits | `DunnLab001707` |
| `fluidx` | two letters and eight digits | `FA27205833` |

Use `other` for anything else. BioSample `sample_name` values are often tube labels. Freezer locations and inventory are outside this skill.

## Generated tables

| File | Contents |
|---|---|
| `specimens.tsv`, `samples.tsv`, `libraries.tsv`, `tubes.tsv` | integrated tables |
| `manifest.tsv` | one row per library, with its sample, specimen, key metadata, accessions, and tubes; the table analyses read |
| `provenance.tsv` | for every value: entity, key, field, value, source, and locator |
| `conflicts.tsv` | fields where sources disagree, the value chosen, and the alternatives |
| `missing_fields.tsv` | required and recommended values not found in any reviewed source |
| `unmatched_records.tsv` | source records not linked to any specimen |
| `catalog_audit.tsv` | per voucher: whether GBIF and LUX have an exact matching record, with URLs and lookup dates |
| `build_problems.tsv`, `validation.tsv` | errors and warnings |
| `taxon_matches.tsv`, `biosample_invertebrate.tsv` | WoRMS matches for review; BioSample export |

When sources disagree and no correction applies, the build takes the value from the strongest source: the holding museum's record in GBIF, then LUX, then INSDC, then the lab's field records, then other GBIF records. A value entered directly in `samples.tsv` or `libraries.tsv` takes precedence over public records for that sample or library.
