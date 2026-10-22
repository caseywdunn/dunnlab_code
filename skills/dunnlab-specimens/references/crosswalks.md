# Crosswalks among sources

[`schema/fields.tsv`](../schema/fields.tsv) gives the field-by-field mapping. This page covers how each source structures its records, and the differences that cause errors.

## Identifiers

| Thing | Lab | YPM / LUX | GBIF | NCBI | ENA |
|---|---|---|---|---|---|
| Specimen | `specimen_key`, `field_id` | catalog number `YPM IZ 110226`; LUX URI | `catalogNumber`, `occurrenceID`, `gbifID` | `specimen_voucher` `YPM:IZ:110226`; `isolate` | `specimen_voucher` |
| Sample | `sample_id`, tube labels | — | — | BioSample `SAMN…`, `sample_name` | `SAMEA…`, `sample_alias` |
| Library | `library_id` | — | — | SRA Experiment `SRX…` | `ERX…` |
| Run | — | — | — | `SRR…` | `ERR…` |
| Project | — | — | — | BioProject `PRJNA…` | `PRJEB…` |

INSDC partners mirror each other, so an ENA sample also appears in NCBI BioSample, and SRA runs are listed by the ENA Portal API.

**Vouchers.** The INSDC form is `institution:collection:catalog`, with codes from the [INSDC controlled vocabulary](https://www.insdc.org/submitting-standards/controlled-vocabulary-specimenvoucher-qualifier/), maintained through [NCBI BioCollections](https://www.ncbi.nlm.nih.gov/biocollections/). Yale Peabody Invertebrate Zoology is `YPM:IZ`. YPM writes catalog numbers with spaces and six-digit zero padding, sometimes with a suffix: `YPM IZ 000001.BV`. Older lab tables also used `YPM-IZ-111756` and the YPM internal form `IZ.108450`. Store the institution and collection codes explicitly. Never infer them, and never drop them when normalizing. Use `bio_material` rather than `specimen_voucher` for tissue or DNA that is not itself a voucher.

## Collecting data

| Field | Internal | BioSample | ENA | Darwin Core / GBIF |
|---|---|---|---|---|
| Date | `collection_date`, ISO 8601 | `collection_date`, ISO 8601 or DD-Mmm-YYYY, intervals with `/` | `collection date`, ISO 8601 | `eventDate`, ISO 8601 with `/` intervals |
| Coordinates | `decimal_latitude`, `decimal_longitude`, south and west negative, WGS84 | `lat_lon` as `38.98 N 77.11 W` | `lat_lon` (ERC000011), or separate decimal fields (ERC000053) | `decimalLatitude`, `decimalLongitude` |
| Place | `geo_loc_name`, `locality`, `collection_site` | `geo_loc_name` from the INSDC list, e.g. `Pacific Ocean: Monterey Bay` | `geographic location (country and/or sea)` and `(region and locality)` | `country`, `waterBody`, `locality` |
| Depth | `depth_m`, `depth_min_m`, `depth_max_m`, `depth_basis`, `verbatim_depth` | `depth`, `{float} m` or an interval | `depth` (m) | `minimumDepthInMeters`, `maximumDepthInMeters`, `verbatimDepth`; GBIF adds an interpreted `depth` |
| Collector | `collected_by` | `collected_by` | `collected_by` | `recordedBy` |
| Tissue | `tissue` (sample) | `tissue` | `tissue_type` or `organism_part` | `preparations`, loosely |

Pitfalls:

- **BioSample `lat_lon` is text**, not decimal degrees. Parse it on ingest and generate it on export; never store it as the coordinate.
- **GBIF folds depth ranges into one interpreted `depth`.** A YPM record with `verbatimDepth` "1864-1864 m" has `depth` 1864 and no minimum or maximum. Prefer explicit bounds or the verbatim text.
- **BioSample `sample_name` is often a tube label or a lab sample ID** (`CWD146`, `NA8`), not a field ID. Match it through `tubes.tsv` and `samples.tsv`, never by assuming.
- **NCBI missing-value terms** (`not collected`, `not applicable`, `missing`, `not provided`, `restricted access`) mean no value. They are not data.
- **LUX records for YPM specimens often lack a structured date and coordinates.** The collecting event appears as a place and as text. GBIF's copy of the YPM record is usually the better source for date and coordinates; LUX confirms the catalog number and gives the record URI.
- **GBIF `basisOfRecord`** uses uppercase in the API (`PRESERVED_SPECIMEN`) and CamelCase in Darwin Core (`PreservedSpecimen`).

## Taxonomy

| Source | Name | Identifier |
|---|---|---|
| WoRMS (authority) | accepted name, with status | AphiaID |
| NCBI / ENA | `organism` / `scientific_name` | taxonomy ID |
| GBIF | `scientificName`, matched to the GBIF backbone | `taxonKey`, `acceptedTaxonKey` |
| LUX | taxon as a concept in `classified_as` | concept URI |

WoRMS links each AphiaID to NCBI taxonomy IDs. GBIF's backbone draws on WoRMS through the Catalogue of Life, so GBIF names can differ from WoRMS; record GBIF's keys, but take the name from WoRMS. A sequence-archive name can lag the determination ("Nanomia sp." in SRA, *N. septata* in the paper). The archive's name is kept in `public_identification`, the current determination in `scientific_name`, and the evidence for the difference in `identification_evidence`. Archives keep deposited names, so updating the public record, where the archive allows it, is a separate step.

## iNaturalist

Use iNaturalist observations through a GBIF download, never by scraping iNaturalist directly, so the data have a citable DOI. Research-grade observations are in the GBIF dataset `50c9509d-22c7-4a22-a47d-8c48425ef4a7`. The observation URL is in `occurrenceID`, and the observation number in `catalogNumber`. Only observations licensed CC0, CC BY, or CC BY-NC reach GBIF. Keep each record's licence, since CC BY-NC restricts reuse.
