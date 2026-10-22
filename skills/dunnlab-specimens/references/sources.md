# Sources

When ingesting a specimen, query every source that may hold it, compare them, and record disagreements. The tool's fetch commands handle the common cases; this page describes what each source offers and how to use it directly when needed.

## Yale Peabody Museum

YPM's catalog is the authority for specimens the lab collects. It reaches the public two ways:

- **GBIF:** dataset `854e35e6-f762-11e1-a439-00145eb45e9a` ("Invertebrate Zoology Division, Yale Peabody Museum", CC0), with `institutionCode` `YPM`, `collectionCode` `IZ`, and `catalogNumber` such as `YPM IZ 115611`. Look up one record with `https://api.gbif.org/v1/occurrence/search?catalogNumber=YPM%20IZ%20115611`.
- **LUX:** Yale's collections platform, with Linked Art JSON-LD records at `https://lux.collections.yale.edu/data/object/<uuid>`. Search by catalog number with the full-text field (`{"text": "YPM IZ 035362"}`, used by [luxy](https://github.com/project-lux/luxy) as `Objects().filter(text=...)`); the identifier filter does not find catalog numbers. LUX matches only the museum's zero-padded form.

`fetch-museum` queries both, trying the padded and unpadded forms. It keeps a candidate only if the institution, collection, and number inside the record match the voucher. A numeric search hit alone is not a match.

**Availability is not validity.** Many vouchers are in LUX but not in GBIF; in one audit, LUX confirmed 148 of 168 YPM vouchers while GBIF had none. A failed lookup does not show that a voucher is wrong or private. `catalog_audit.tsv` records each lookup's result, URL, and date separately from the specimen's identity.

Corrections to YPM records go to the museum's collection database, which feeds both LUX and GBIF. Record them in `corrections.tsv` with `upstream` set to `to_submit`, and update it as they are submitted and applied.

## NCBI and ENA

- **BioSample attributes:** `efetch` by accession, e.g. `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id=SAMN32803035`. It works for ENA samples (`SAMEA…`) too, through INSDC mirroring.
- **Runs and experiments:** the ENA Portal API, which covers SRA projects as well: `https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA925656&result=read_run&fields=...&format=tsv`. `returnFields?result=read_run` lists the fields.
- Without an API key, NCBI allows three requests a second; the tool batches and pauses accordingly.

The Invertebrate.1.0 BioSample package requires `sample_name`, `organism`, `collection_date`, `geo_loc_name`, `tissue`, either `isolate` or `breed`, and either `host` or `isolation_source`. NCBI wants one BioSample per specimen part with differentiating attributes, so separate tissues of one animal are separate BioSamples sharing `isolate` and `specimen_voucher`. ENA's default checklist is ERC000011; ERC000053 (Tree of Life) has separate decimal coordinate fields and more required fields.

## GBIF downloads

Data used in an analysis come from a GBIF **download**, which has a DOI to cite, rather than from search results. Request the download on gbif.org or through the API: `POST https://api.gbif.org/v1/occurrence/download/request` with a GBIF account and a JSON predicate, choosing the `SIMPLE_CSV` format. Then run `fetch-gbif-download <key>`. It saves the archive, the metadata, and the DOI, and records the citation, "GBIF.org (date) GBIF Occurrence Download https://doi.org/10.15468/dl.…". Cite that DOI in the paper; it credits every contributing dataset.

## WoRMS

`fetch-worms` matches names in batches (`AphiaRecordsByMatchNames`) and adds NCBI taxonomy IDs (`AphiaExternalIDByAphiaID?type=ncbi`), writing `generated/taxon_matches.tsv` for review. Accept a match by recording it in `determinations.tsv`. The tool never edits determinations itself. Check the match type and status: an unaccepted name points to its `valid_AphiaID`.

## OBIS

`check-obis` sends every coordinate to the OBIS lookup service (`https://api.obis.org/xylookup`). The service returns distance to shore in metres, negative on land, and bathymetry, positive below sea level. It also fetches each AphiaID's depth distribution (`https://api.obis.org/v3/statistics/env?taxonid=`). `validate` uses these for its warnings. A taxon with few OBIS records has a narrow apparent range, so a depth outside it is a question to check, not an error.

## Field records

The lab's field log is a source in `field_records.tsv`. Keep dive logs, station sheets, and photographs as files and cite them in `source_locator` when they support a correction: a page, a cell, a file name.
