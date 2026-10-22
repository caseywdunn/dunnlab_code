# Curation

These rules guide judgement; adapt them when a project's data call for it, and record why.

## Authoritative records and the editing path

Decide, for each value, which record is authoritative and where a correction is made. Raw sources and the lab's field log are never edited. Lasting changes go in `corrections.tsv`, and in YPM's database for YPM specimens. Never edit a generated table: the next build overwrites it. A completed project may keep its frozen analysis inputs beside the curated metadata; it does not need two competing master tables.

## Matching records

- Join records only by explicit identifiers or reviewed entries in `crosswalk.tsv`. A taxon name, a similar label, or a numeric search hit is not identity.
- Normalize known formatting differences (separators, case, leading zeros) but keep institution and collection prefixes.
- Keep documented aliases and museum transfers as `alias_voucher` rows of the same specimen key.
- Check that a matched assay or sample belongs to the intended set of specimens.
- Records the build cannot link appear in `unmatched_records.tsv`. Resolve each one by adding a confirmed crosswalk entry, or leave it unlinked with a reason.

## Value-level provenance

Each correction records the key, field, original value, new value, source, `source_locator`, and notes. A locator identifies one place: a spreadsheet cell, a repository row, an accession, a log page. Keep source versions, repository commits, retrieval dates, and checksums; the fetch commands record these automatically. The build applies a correction only when the original value still matches. Agreeing sources can coexist; conflicting values need a decision, recorded as a correction or a note, never a silent overwrite.

## Collecting context

Seek latitude, longitude, place, depth, and tissue for every specimen and sample.

- **Coordinates** are decimal degrees, WGS84, south and west negative. Keep the verbatim text and the uncertainty when given.
- **Place:** keep the broad locality (`locality`) and the specific site (`collection_site`) separately when both are known.
- **Tissue** must come from a record about that sample. A study's general extraction protocol does not fill an unspecified tissue.
- **Never invent an identifier** because related rows have one.

## Depth

Depth is in metres, positive below the surface; 0 is a valid depth, not a missing value.

- Keep an explicit point depth when recorded (`depth_basis` `measured`).
- If there is no point depth but both bounds are recorded, `depth_m` is their mean (`interval_midpoint`), and the bounds and the verbatim text are kept. Equal bounds are a point depth.
- A single bound is not enough: leave `depth_m` blank and explain in `notes`.
- Conflicting point measurements are not an interval; reconcile them.
- Resolve uncertain units before converting. The tool converts explicit feet, and notes any depth whose source gave no unit.
- A depth assigned by an ecological convention, such as surface depth for blue-water dives, uses `depth_basis` `convention`, and `notes` must name the convention.

## Notes

`notes` is for people: missing information, disagreements between sources, derived values, unusual identifier mappings. Write "not recorded in the reviewed sources" when that is what the evidence supports. Computational annotations, such as GBIF quality flags, go in `analysis_notes`. Structured provenance in `provenance.tsv` carries the technical detail.

## Catalog availability

Audit public availability separately from voucher identity. `catalog_audit.tsv` keeps each lookup's result, URL, and date. Verify institution, collection, and number inside each candidate record. A failed lookup does not show that a voucher is invalid or private.

## Taxonomy

Record each determination with the verbatim name, the person, the date, and the evidence, and mark the initial and the current ones. When the current identification differs from the initial or the public one, the evidence must say why: a barcode or phylogenetic placement, morphology, or a taxonomic revision with its citation. Match names to WoRMS with `fetch-worms` and accept matches deliberately. For undescribed or incompletely identified taxa, use "*Genus* sp." with the voucher, so NCBI can assign an informal name and taxonomy ID, and keep a lab-wide informal name for the taxon.

## Review loop

1. Run `build`, then `check-obis` if coordinates or taxa changed, then `validate`.
2. Work through `build_problems.tsv`, `validation.tsv`, `conflicts.tsv`, `unmatched_records.tsv`, and `missing_fields.tsv`.
3. Add crosswalk entries, corrections, and determinations; fetch additional sources where a gap might be filled.
4. Rebuild. Metadata curation never requires rerunning sequence analyses. Refreshing figures or summaries that use the metadata is a separate step.
