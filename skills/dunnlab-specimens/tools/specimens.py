#!/usr/bin/env python3
"""Specimen metadata tools: fetch from public sources, build integrated tables, validate, export.

Run from a project's root; tables live under specimens/ (override with --root).

  specimens.py fetch-museum YPM:IZ:110226 ...     GBIF and LUX records for museum vouchers
  specimens.py fetch-insdc SAMN32803035 PRJNA925656 ...   BioSamples and runs (NCBI, ENA)
  specimens.py fetch-gbif-download 0021738-260928105237408 ...   an existing GBIF download, with DOI
  specimens.py fetch-worms "Nanomia septata" ...  WoRMS matches and NCBI taxids
  specimens.py build                              integrate sources and curation into generated/
  specimens.py check-obis                         ocean and depth context for coordinates and taxa
  specimens.py validate                           check generated tables; exit 1 on errors
  specimens.py export-biosample                   NCBI BioSample Invertebrate.1.0 table

Standard library only. Raw downloads under sources/ are never modified; generated/ is rebuilt.
"""

import argparse
import csv
import datetime
import hashlib
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

USER_AGENT = "dunnlab-specimens/1.0 (+https://github.com/caseywdunn/dunnlab_code)"
SCHEMA = Path(__file__).resolve().parent.parent / "schema" / "fields.tsv"
TABLES = ("specimen", "sample", "library", "tube")
# Which source wins when sources disagree and no correction applies. Lower is stronger.
PRECEDENCE = {"museum": 0, "lux": 1, "insdc": 2, "field_records": 3, "gbif": 4}
SPECIMEN_LEVEL_FROM_BIOSAMPLE = {"collection_date", "geo_loc_name", "collected_by", "identified_by",
                                 "decimal_latitude", "decimal_longitude", "verbatim_coordinates",
                                 "depth_m", "depth_min_m", "depth_max_m", "depth_basis", "verbatim_depth",
                                 "specimen_voucher", "institution_code", "collection_code", "catalog_number",
                                 "scientific_name", "ncbi_taxid"}
NCBI_MISSING = {"", "missing", "not collected", "not applicable", "not provided", "restricted access",
                "unknown", "na", "n/a"}


# ----------------------------------------------------------------------------- tables

def read_schema():
    with open(SCHEMA, newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    return [{k: (v or "") for k, v in r.items()} for r in rows]


def fields_for(schema, table):
    return [r for r in schema if r["table"] == table]


def read_tsv(path):
    path = Path(path)
    if not path.is_file():
        return []
    with open(path, newline="") as f:
        return [{k: (v or "").strip() for k, v in row.items() if k is not None}
                for row in csv.DictReader(f, delimiter="\t")]


def write_tsv(path, rows, columns):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "") for c in columns})


# ----------------------------------------------------------------------------- identifiers and values

VOUCHER_PATTERNS = [
    re.compile(r"^(?P<inst>[A-Za-z]+(?:<[A-Z-]+>)?)[:\s_-]+(?P<coll>[A-Za-z]+)[:\s_-]+(?P<num>[0-9][0-9A-Za-z.-]*)$"),
    re.compile(r"^(?P<coll>IZ)\.(?P<num>[0-9][0-9A-Za-z.-]*)$"),  # YPM internal form IZ.108450
]


def parse_voucher(text, default_institution=None):
    """Return (institution, collection, number) or None. Prefixes are never discarded or guessed,
    except that a YPM internal 'IZ.n' form needs default_institution."""
    text = (text or "").strip()
    for pattern in VOUCHER_PATTERNS:
        match = pattern.match(text)
        if match:
            inst = match.groupdict().get("inst") or default_institution
            if not inst:
                return None
            return inst.upper(), match.group("coll").upper(), match.group("num")
    return None


def voucher_insdc(parts):
    return f"{parts[0]}:{parts[1]}:{parts[2]}"


def voucher_match_key(parts):
    """Compare vouchers across formatting differences: case, separators, and leading zeros."""
    inst, coll, num = parts
    head, _, suffix = num.partition(".")
    return (inst.upper(), coll.upper(), head.lstrip("0") or "0", suffix.upper())


TUBE_PATTERNS = {
    "dunnlab_datamatrix": re.compile(r"^DunnLab[0-9]{6}$"),
    "fluidx": re.compile(r"^[A-Z]{2}[0-9]{8}$"),
    "handwritten": re.compile(r"^[A-Z]{2,4}[0-9]{1,6}$"),
}


def classify_tube_id(tube_id):
    """Label type implied by a tube ID's form, checked in this order; 'other' if none fits."""
    for kind, pattern in TUBE_PATTERNS.items():
        if pattern.match(tube_id or ""):
            return kind
    return "other"


def specimen_key_from(voucher=None, field_id=None):
    if voucher:
        return re.sub(r"[^A-Za-z0-9.-]+", "_", voucher)
    return re.sub(r"[^A-Za-z0-9._-]+", "_", field_id or "")


def clean(value):
    value = "" if value is None else str(value).strip()
    return "" if value.lower() in NCBI_MISSING else value


def parse_insdc_lat_lon(text):
    match = re.match(r"^\s*([0-9.]+)\s*([NS])\s+([0-9.]+)\s*([EW])\s*$", text or "")
    if not match:
        return None
    lat = float(match.group(1)) * (-1 if match.group(2) == "S" else 1)
    lon = float(match.group(3)) * (-1 if match.group(4) == "W" else 1)
    return lat, lon


def format_insdc_lat_lon(lat, lon):
    lat, lon = float(lat), float(lon)
    return f"{abs(lat):.4f} {'S' if lat < 0 else 'N'} {abs(lon):.4f} {'W' if lon < 0 else 'E'}"


def fmt_number(x):
    return ("%.4f" % x).rstrip("0").rstrip(".")


FEET = 0.3048


def resolve_depth(point=None, minimum=None, maximum=None, verbatim=None, unit_default="m"):
    """Apply the depth rules. Returns depth_m, depth_min_m, depth_max_m, depth_basis, verbatim_depth, note."""
    out = {"depth_m": "", "depth_min_m": "", "depth_max_m": "", "depth_basis": "", "verbatim_depth": clean(verbatim)}
    note = ""

    def num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    p, lo, hi = num(point), num(minimum), num(maximum)
    if p is None and lo is None and hi is None and out["verbatim_depth"]:
        text = out["verbatim_depth"].lower().replace("meters", "m").replace("metres", "m").replace("meter", "m")
        unit = "ft" if re.search(r"\b(ft|feet|foot)\b", text) else ("m" if re.search(r"\bm\b", text) else "")
        numbers = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
        if not unit and unit_default != "m":
            return out, f"depth unit not stated in '{out['verbatim_depth']}'; left blank"
        factor = FEET if unit == "ft" else 1.0
        if unit == "ft":
            note = f"converted from feet ('{out['verbatim_depth']}')"
        elif not unit and numbers:
            note = f"no unit in depth '{out['verbatim_depth']}'; taken as metres, the unit of the source field"
        if len(numbers) == 1:
            p = numbers[0] * factor
        elif len(numbers) == 2:
            lo, hi = sorted(n * factor for n in numbers)
        elif numbers:
            return out, f"could not interpret depth '{out['verbatim_depth']}'; left blank"
    if lo is not None and hi is not None:
        if lo > hi:
            return out, f"minimum depth {lo} exceeds maximum {hi}; left blank"
        out["depth_min_m"], out["depth_max_m"] = fmt_number(lo), fmt_number(hi)
    if p is not None:
        out["depth_m"], out["depth_basis"] = fmt_number(p), "measured"
    elif lo is not None and hi is not None:
        if lo == hi:
            out["depth_m"], out["depth_basis"] = fmt_number(lo), "measured"
        else:
            out["depth_m"], out["depth_basis"] = fmt_number((lo + hi) / 2), "interval_midpoint"
    elif lo is not None or hi is not None:
        note = "only one depth bound recorded; depth left blank"
    return out, note


def normalize_date(text):
    """ISO 8601 date, partial date, or interval; also accepts M/D/YYYY and DD-Mon-YYYY."""
    text = clean(text)
    if not text:
        return ""
    if "/" in text and re.match(r"^\d{4}", text):
        return "/".join(normalize_date(t) for t in text.split("/"))
    text = text.split("T")[0]
    for fmt, out in (("%Y-%m-%d", "%Y-%m-%d"), ("%Y-%m", "%Y-%m"), ("%Y", "%Y"),
                     ("%m/%d/%Y", "%Y-%m-%d"), ("%d-%b-%Y", "%Y-%m-%d"), ("%b-%Y", "%Y-%m")):
        try:
            return datetime.datetime.strptime(text, fmt).strftime(out)
        except ValueError:
            pass
    return text  # left as given; validation reports it


# ----------------------------------------------------------------------------- retrieval

def http_get(url, accept=None, data=None, headers=None):
    request = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT, **(headers or {})})
    if accept:
        request.add_header("Accept", accept)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read()
        except urllib.error.HTTPError as err:
            if err.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise


def save_retrieval(root, source, slug, files, requests_made, extra=None):
    """Write raw files under sources/<source>/<timestamp>_<slug>/ with retrieval.json."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    folder = Path(root) / "sources" / source / f"{stamp}_{re.sub(r'[^A-Za-z0-9._-]+', '_', slug)[:60]}"
    folder.mkdir(parents=True, exist_ok=False)
    record = {"source": source, "retrieved_utc": stamp, "requests": requests_made, "files": {}, **(extra or {})}
    for name, content in files.items():
        (folder / name).write_bytes(content)
        record["files"][name] = {"sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
    (folder / "retrieval.json").write_text(json.dumps(record, indent=2) + "\n")
    return folder


def cmd_fetch_museum(args):
    """GBIF occurrence and LUX records for each voucher, with identity checked inside each record."""
    gbif_files, lux_files, gbif_requests, lux_requests = {}, {}, [], []
    for voucher in args.vouchers:
        parts = parse_voucher(voucher)
        if not parts:
            sys.exit(f"error: cannot parse voucher '{voucher}'; give institution and collection, e.g. YPM:IZ:110226")
        inst, coll, num = parts
        catalog = f"{inst} {coll} {num}"
        candidates = {catalog}
        if num.isdigit():
            candidates.add(f"{inst} {coll} {num.zfill(6)}")
        stem = voucher_insdc(parts).replace(":", "_")
        results = []
        for cat in sorted(candidates):
            url = ("https://api.gbif.org/v1/occurrence/search?" +
                   urllib.parse.urlencode({"catalogNumber": cat, "institutionCode": inst, "limit": 50}))
            gbif_requests.append(url)
            results += json.loads(http_get(url))["results"]
        gbif_files[f"{stem}.json"] = json.dumps({"query": voucher, "results": results}, indent=1).encode()
        if args.no_lux or inst != "YPM":
            continue
        records, seen = [], set()
        for cat in sorted(candidates):  # LUX full-text search matches only the museum's padded form
            url = ("https://lux.collections.yale.edu/api/search/item?" +
                   urllib.parse.urlencode({"q": json.dumps({"text": cat})}))
            lux_requests.append(url)
            hits = json.loads(http_get(url, accept="application/json"))
            for item in hits.get("orderedItems", [])[:10]:
                record_url = item.get("id")
                if record_url and record_url not in seen:
                    seen.add(record_url)
                    lux_requests.append(record_url)
                    records.append(json.loads(http_get(record_url, accept="application/json")))
        lux_files[f"{stem}.json"] = json.dumps({"query": voucher, "records": records}, indent=1).encode()
    print(save_retrieval(args.root, "gbif_occurrence", "museum_" + "_".join(args.vouchers[:3]), gbif_files, gbif_requests))
    if lux_files:
        print(save_retrieval(args.root, "lux", "museum_" + "_".join(args.vouchers[:3]), lux_files, lux_requests))


def cmd_fetch_insdc(args):
    """BioSample XML from NCBI and run tables from ENA, for BioSample or BioProject accessions."""
    files, requests_made, biosamples = {}, [], []
    for accession in args.accessions:
        if accession.startswith("PRJ"):
            fields = ("run_accession,experiment_accession,sample_accession,study_accession,library_name,"
                      "library_strategy,library_source,library_selection,library_layout,instrument_platform,"
                      "instrument_model,scientific_name,tax_id")
            url = ("https://www.ebi.ac.uk/ena/portal/api/filereport?" +
                   urllib.parse.urlencode({"accession": accession, "result": "read_run", "fields": fields, "format": "tsv"}))
            requests_made.append(url)
            content = http_get(url)
            files[f"runs_{accession}.tsv"] = content
            biosamples += [r["sample_accession"] for r in csv.DictReader(io.StringIO(content.decode()), delimiter="\t")
                           if r.get("sample_accession")]
        elif accession.startswith("SAM"):
            biosamples.append(accession)
        else:
            sys.exit(f"error: expected a BioProject (PRJ...) or BioSample (SAM...) accession, got '{accession}'")
    biosamples = sorted(set(biosamples))
    for start in range(0, len(biosamples), 100):
        batch = biosamples[start:start + 100]
        url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" +
               urllib.parse.urlencode({"db": "biosample", "id": ",".join(batch)}))
        requests_made.append(url)
        files[f"biosamples_{start // 100 + 1:03d}.xml"] = http_get(url)
        time.sleep(0.4)  # NCBI allows three requests a second without an API key
    if biosamples and not any(a.startswith("PRJ") for a in args.accessions):
        url = ("https://www.ebi.ac.uk/ena/portal/api/search?" + urllib.parse.urlencode({
            "result": "read_run", "format": "tsv",
            "query": " OR ".join(f'sample_accession="{b}"' for b in biosamples),
            "fields": "run_accession,experiment_accession,sample_accession,study_accession,library_name,library_strategy,"
                      "library_source,library_selection,library_layout,instrument_platform,instrument_model,scientific_name,tax_id"}))
        requests_made.append(url)
        files["runs_samples.tsv"] = http_get(url)
    print(save_retrieval(args.root, "insdc", "_".join(args.accessions[:3]), files, requests_made))


def cmd_fetch_gbif_download(args):
    """An existing GBIF download (request it on gbif.org or through the API first), with its DOI."""
    for key in args.keys:
        meta_url = f"https://api.gbif.org/v1/occurrence/download/{key}"
        meta = json.loads(http_get(meta_url))
        if meta.get("status") != "SUCCEEDED":
            sys.exit(f"error: download {key} has status {meta.get('status')}")
        data = http_get(meta["downloadLink"])
        folder = save_retrieval(args.root, "gbif_download", key, {"metadata.json": json.dumps(meta, indent=1).encode(),
                                                                  f"{key}.zip": data},
                                [meta_url, meta["downloadLink"]],
                                {"doi": meta.get("doi"), "citation": f"GBIF.org ({meta.get('created', '')[:10]}) GBIF Occurrence Download https://doi.org/{meta.get('doi')}"})
        print(folder, "DOI:", meta.get("doi"))


def cmd_fetch_worms(args):
    names = list(args.names)
    if args.from_determinations:
        names += [r["scientific_name"] for r in read_tsv(Path(args.root) / "determinations.tsv")
                  if r.get("scientific_name") and not r.get("aphia_id")]
    names = sorted(set(n for n in names if n))
    if not names:
        sys.exit("no names to look up")
    requests_made, matches = [], {}
    for start in range(0, len(names), 50):
        batch = names[start:start + 50]
        url = ("https://www.marinespecies.org/rest/AphiaRecordsByMatchNames?" +
               "&".join("scientificnames[]=" + urllib.parse.quote(n) for n in batch) + "&marine_only=false")
        requests_made.append(url)
        for name, result in zip(batch, json.loads(http_get(url) or b"[]")):
            matches[name] = result or []
    for name, records in matches.items():
        for record in records:
            aphia = record.get("valid_AphiaID") or record.get("AphiaID")
            url = f"https://www.marinespecies.org/rest/AphiaExternalIDByAphiaID/{aphia}?type=ncbi"
            requests_made.append(url)
            body = http_get(url)
            record["ncbi_taxids_of_valid_name"] = json.loads(body) if body else []
    folder = save_retrieval(args.root, "worms", "_".join(names[:3]),
                            {"matches.json": json.dumps(matches, indent=1).encode()}, requests_made)
    print(folder)
    rows = []
    for name, records in matches.items():
        if not records:
            rows.append({"query": name, "match_type": "none"})
        for r in records:
            rows.append({"query": name, "match_type": r.get("match_type"), "scientificname": r.get("scientificname"),
                         "status": r.get("status"), "aphia_id": r.get("AphiaID"), "valid_name": r.get("valid_name"),
                         "valid_aphia_id": r.get("valid_AphiaID"),
                         "ncbi_taxid": ";".join(r.get("ncbi_taxids_of_valid_name", []))})
    out = Path(args.root) / "generated" / "taxon_matches.tsv"
    write_tsv(out, rows, ["query", "match_type", "scientificname", "status", "aphia_id", "valid_name",
                          "valid_aphia_id", "ncbi_taxid"])
    print(f"Review {out}, then record accepted matches in determinations.tsv.")


# ----------------------------------------------------------------------------- parsing sources into observations

def obs(source, locator, retrieved, level="specimen", **ids):
    return {"source": source, "locator": locator, "retrieved": retrieved, "level": level,
            "ids": {k: v for k, v in ids.items() if v}, "values": {}, "notes": []}


def put(o, field, value):
    value = clean(value)
    if value:
        o["values"][field] = value


def add_depth(o, **kw):
    depth, note = resolve_depth(**kw)
    for k, v in depth.items():
        put(o, k, v)
    if note:
        o["notes"].append(note)


def from_gbif_record(r, source_tag, retrieved):
    gbif_id = str(r.get("gbifID") or r.get("key") or "")
    parts = parse_voucher(r.get("catalogNumber", ""))
    voucher = voucher_insdc(parts) if parts else ""
    occurrence_url = r.get("occurrenceID", "") if str(r.get("occurrenceID", "")).startswith("http") else r.get("references", "")
    o = obs(source_tag, f"https://www.gbif.org/occurrence/{gbif_id}", retrieved, specimen_voucher=voucher,
            gbif_id=gbif_id, occurrence_url=occurrence_url if source_tag == "gbif" else "")
    put(o, "gbif_id", gbif_id)
    if parts:
        put(o, "specimen_voucher", voucher)
        put(o, "institution_code", r.get("institutionCode"))
        put(o, "collection_code", r.get("collectionCode"))
        put(o, "catalog_number", r.get("catalogNumber"))
    put(o, "occurrence_url", occurrence_url)
    put(o, "scientific_name", r.get("scientificName"))
    put(o, "collection_date", normalize_date(r.get("eventDate")))
    put(o, "verbatim_date", r.get("verbatimEventDate"))
    for field, key in (("decimal_latitude", "decimalLatitude"), ("decimal_longitude", "decimalLongitude"),
                       ("coordinate_uncertainty_m", "coordinateUncertaintyInMeters")):
        if r.get(key) not in (None, ""):
            put(o, field, fmt_number(float(r[key])))
    put(o, "locality", r.get("locality"))
    put(o, "collected_by", r.get("recordedBy"))
    put(o, "identified_by", r.get("identifiedBy"))
    put(o, "preservation", r.get("preparations"))
    put(o, "type_status", r.get("typeStatus"))
    put(o, "field_id", r.get("recordNumber") or r.get("fieldNumber"))
    # GBIF folds ranges into one interpreted depth, so prefer the explicit bounds or the verbatim text.
    add_depth(o, minimum=r.get("minimumDepthInMeters"), maximum=r.get("maximumDepthInMeters"),
              verbatim=r.get("verbatimDepth") or (str(r["depth"]) + " m" if r.get("depth") not in (None, "") else ""))
    if r.get("issues"):
        o["notes"].append("GBIF issues: " + ", ".join(r["issues"]) if isinstance(r["issues"], list) else str(r["issues"]))
    return o


def from_lux_record(r, retrieved):
    catalog = ""
    for ident in r.get("identified_by", []):
        labels = " ".join(c.get("_label", "") for c in ident.get("classified_as", []))
        if "External Catalog Number" in labels or re.match(r"^[A-Z]+ [A-Z]+ \S+$", ident.get("content", "")):
            catalog = ident.get("content", "")
            break
    parts = parse_voucher(catalog)
    voucher = voucher_insdc(parts) if parts else ""
    o = obs("lux", r.get("id", ""), retrieved, specimen_voucher=voucher, lux_uri=r.get("id", ""))
    put(o, "lux_uri", r.get("id"))
    if parts:
        put(o, "specimen_voucher", voucher)
        put(o, "catalog_number", catalog)
    return o


INSDC_ATTRIBUTES = {"collection_date": "collection_date", "geo_loc_name": "geo_loc_name", "collected_by": "collected_by",
                    "identified_by": "identified_by", "tissue": "tissue", "dev_stage": "dev_stage", "sex": "sex"}


def from_biosample(b, retrieved):
    accession = b.get("accession")
    attrs = {a.get("attribute_name"): (a.text or "").strip() for a in b.findall("Attributes/Attribute")}
    voucher_parts = parse_voucher(attrs.get("specimen_voucher", ""))
    voucher = voucher_insdc(voucher_parts) if voucher_parts else ""
    sample_name = next((i.text for i in b.findall("Ids/Id") if i.get("db_label") == "Sample name"), "")
    o = obs("insdc", f"https://www.ncbi.nlm.nih.gov/biosample/{accession}", retrieved, level="sample",
            biosample_accession=accession, specimen_voucher=voucher)
    put(o, "biosample_accession", accession)
    put(o, "sample_name_in_biosample", sample_name)
    organism = b.find("Description/Organism")
    if organism is not None:
        put(o, "scientific_name", organism.get("taxonomy_name"))
        put(o, "ncbi_taxid", organism.get("taxonomy_id"))
    for attr, field in INSDC_ATTRIBUTES.items():
        put(o, field, normalize_date(attrs.get(attr)) if field == "collection_date" else attrs.get(attr))
    if voucher:
        put(o, "specimen_voucher", voucher)
        put(o, "institution_code", voucher_parts[0])
        put(o, "collection_code", voucher_parts[1])
    elif clean(attrs.get("specimen_voucher")):
        o["notes"].append(f"unstructured specimen_voucher '{attrs['specimen_voucher']}' not used as an identifier")
    put(o, "isolate", attrs.get("isolate"))
    lat_lon = clean(attrs.get("lat_lon"))
    if lat_lon:
        put(o, "verbatim_coordinates", lat_lon)
        parsed = parse_insdc_lat_lon(lat_lon)
        if parsed:
            put(o, "decimal_latitude", fmt_number(parsed[0]))
            put(o, "decimal_longitude", fmt_number(parsed[1]))
        else:
            o["notes"].append(f"could not parse lat_lon '{lat_lon}'")
    add_depth(o, verbatim=attrs.get("depth"))
    return o


def from_ena_run(r, retrieved):
    o = obs("insdc", f"https://www.ebi.ac.uk/ena/browser/view/{r.get('run_accession')}", retrieved, level="library",
            experiment_accession=r.get("experiment_accession"), biosample_accession=r.get("sample_accession"))
    for field, key in (("experiment_accession", "experiment_accession"), ("run_accessions", "run_accession"),
                       ("biosample_accession", "sample_accession"), ("bioproject_accession", "study_accession"),
                       ("library_strategy", "library_strategy"), ("library_source", "library_source"),
                       ("library_selection", "library_selection"), ("library_layout", "library_layout"),
                       ("platform", "instrument_platform"), ("instrument_model", "instrument_model"),
                       ("library_name", "library_name")):
        put(o, field, r.get(key))
    if o["values"].get("library_layout"):
        o["values"]["library_layout"] = o["values"]["library_layout"].lower()
    return o


def latest_retrievals(root, source):
    """Every retrieval folder for a source, oldest first; later retrievals of the same record override earlier."""
    base = Path(root) / "sources" / source
    return sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []


def load_observations(root, home_institutions):
    observations = []
    for folder in latest_retrievals(root, "gbif_occurrence"):
        retrieved = folder.name.split("_")[0]
        for f in sorted(folder.glob("*.json")):
            if f.name == "retrieval.json":
                continue
            payload = json.loads(f.read_text())
            query = parse_voucher(payload["query"])
            for r in payload["results"]:
                parts = parse_voucher(r.get("catalogNumber", ""))
                # Identity must be confirmed inside the record: institution, collection, and number.
                if not (query and parts and voucher_match_key(parts) == voucher_match_key(query)
                        and r.get("institutionCode", "").upper() == query[0]
                        and r.get("collectionCode", "").upper() == query[1]):
                    continue
                tag = "museum" if query[0] in home_institutions or r.get("institutionCode", "").upper() == query[0] else "gbif"
                observations.append(from_gbif_record(r, tag, retrieved))
    for folder in latest_retrievals(root, "lux"):
        retrieved = folder.name.split("_")[0]
        for f in sorted(folder.glob("*.json")):
            if f.name == "retrieval.json":
                continue
            payload = json.loads(f.read_text())
            query = parse_voucher(payload["query"])
            for r in payload["records"]:
                o = from_lux_record(r, retrieved)
                vparts = parse_voucher(o["values"].get("specimen_voucher", ""))
                if query and vparts and voucher_match_key(vparts) == voucher_match_key(query):
                    observations.append(o)
    for folder in latest_retrievals(root, "insdc"):
        retrieved = folder.name.split("_")[0]
        for f in sorted(folder.glob("biosamples_*.xml")):
            for b in ET.fromstring(f.read_bytes()).findall("BioSample"):
                observations.append(from_biosample(b, retrieved))
        for f in sorted(folder.glob("runs_*.tsv")):
            for r in csv.DictReader(io.StringIO(f.read_text()), delimiter="\t"):
                observations.append(from_ena_run(r, retrieved))
    for folder in latest_retrievals(root, "gbif_download"):
        retrieved = folder.name.split("_")[0]
        meta = json.loads((folder / "retrieval.json").read_text())
        for z in folder.glob("*.zip"):
            with zipfile.ZipFile(z) as archive:
                name = next(n for n in archive.namelist() if n.endswith((".csv", ".txt")))
                text = archive.read(name).decode("utf-8")
            for r in csv.DictReader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE):
                o = from_gbif_record(r, "gbif", retrieved)
                o["notes"].append(f"GBIF download DOI {meta.get('doi')}")
                observations.append(o)
    for n, row in enumerate(read_tsv(Path(root) / "field_records.tsv"), start=2):
        parts = parse_voucher(row.get("specimen_voucher", ""))
        o = obs("field_records", f"field_records.tsv:{n}", "", field_id=row.get("field_id"),
                specimen_voucher=voucher_insdc(parts) if parts else "")
        for k, v in row.items():
            if k in ("depth_m", "depth_min_m", "depth_max_m", "verbatim_depth", "depth_basis"):
                continue
            put(o, k, normalize_date(v) if k == "collection_date" else v)
        add_depth(o, point=row.get("depth_m"), minimum=row.get("depth_min_m"), maximum=row.get("depth_max_m"),
                  verbatim=row.get("verbatim_depth"))
        if row.get("depth_basis") == "convention" and row.get("depth_m"):
            o["values"]["depth_basis"] = "convention"
        observations.append(o)
    return observations


# ----------------------------------------------------------------------------- build

def comparable(field, value):
    if field in ("decimal_latitude", "decimal_longitude", "depth_m", "depth_min_m", "depth_max_m",
                 "coordinate_uncertainty_m"):
        try:
            return round(float(value), 3)
        except ValueError:
            return value
    if field == "specimen_voucher":
        parts = parse_voucher(value)
        return voucher_match_key(parts) if parts else value
    return re.sub(r"\s+", " ", value).strip().casefold()


def index_crosswalk(crosswalk, problems):
    """Map (id_type, normalized id) -> specimen_key, from confirmed rows only."""
    index = {}
    for n, row in enumerate(crosswalk, start=2):
        if row.get("status") != "confirmed":
            continue
        id_type, value = row.get("id_type", ""), row.get("id_value", "")
        key = (id_type, comparable("specimen_voucher", value) if "voucher" in id_type else value)
        if key in index and index[key] != row["specimen_key"]:
            problems.append(("error", "crosswalk", row["specimen_key"], "id_value",
                             f"crosswalk.tsv:{n}: {id_type} {value} is mapped to both {index[key]} and {row['specimen_key']}"))
        index[key] = row["specimen_key"]
    return index


def resolve_specimen(o, index):
    for id_type in ("specimen_voucher", "field_id", "biosample_accession", "gbif_id", "lux_uri", "occurrence_url"):
        value = o["ids"].get(id_type)
        if not value:
            continue
        candidates = [(id_type, value)]
        if id_type == "specimen_voucher":
            parts = parse_voucher(value)
            norm = voucher_match_key(parts) if parts else value
            candidates = [("specimen_voucher", norm), ("alias_voucher", norm)]
        for key in candidates:
            if key in index:
                return index[key], id_type
    return None, None


def assemble(rows_by_key, field_names, candidates, corrections, entity, provenance, conflicts, problems, voucher_inst):
    """Choose a value per field: correction, then authored value, then the strongest source."""
    for key, row in rows_by_key.items():
        for field in field_names:
            options = candidates.get((key, field), [])
            authored = row.get(field, "")
            ranked = sorted(options, key=lambda c: PRECEDENCE.get(c["source"], 9))
            chosen = authored or (ranked[0]["value"] if ranked else "")
            chosen_src = ("authored", f"{entity}s.tsv") if authored else (
                (ranked[0]["source"], ranked[0]["locator"]) if ranked else ("", ""))
            distinct = {}
            for c in ([{"value": authored, "source": "authored", "locator": f"{entity}s.tsv"}] if authored else []) + ranked:
                distinct.setdefault(comparable(field, c["value"]), c)
            if len(distinct) > 1 and field not in ("notes", "analysis_notes", "verbatim_date", "verbatim_depth",
                                                   "verbatim_coordinates", "catalog_number", "occurrence_url"):
                conflicts.append({"entity": entity, "key": key, "field": field, "chosen": chosen,
                                  "chosen_source": chosen_src[0],
                                  "alternatives": " | ".join(f"{c['value']} ({c['source']}: {c['locator']})"
                                                              for c in distinct.values() if c["value"] != chosen)})
            correction = corrections.get((entity, key, field))
            if correction and chosen and comparable(field, chosen) == comparable(field, correction.get("value", "")):
                if correction.get("upstream", "") not in ("", "none", "applied"):
                    problems.append(("info", entity, key, field,
                                     "the source now has the corrected value; mark the correction's upstream as applied"))
            elif correction:
                expected = correction.get("original_value", "")
                if comparable(field, expected) != comparable(field, chosen) if expected or chosen else False:
                    problems.append(("error", entity, key, field,
                                     f"correction expects original '{expected}' but the assembled value is '{chosen}'; not applied"))
                else:
                    chosen = correction.get("value", "")
                    chosen_src = ("correction", correction.get("source_locator") or correction.get("source", ""))
            if chosen:
                row[field] = chosen
                provenance.append({"entity": entity, "key": key, "field": field, "value": chosen,
                                   "source": chosen_src[0], "locator": chosen_src[1]})


def cmd_build(args):
    root = Path(args.root)
    schema = read_schema()
    problems, provenance, conflicts, unmatched = [], [], [], []
    crosswalk = read_tsv(root / "crosswalk.tsv")
    index = index_crosswalk(crosswalk, problems)
    home = {i.upper() for i in args.home_institution}
    observations = load_observations(root, home)

    specimen_fields = [f["field"] for f in fields_for(schema, "specimen")]
    sample_fields = [f["field"] for f in fields_for(schema, "sample")]
    library_fields = [f["field"] for f in fields_for(schema, "library")]

    specimens = {}
    for row in crosswalk:
        if row.get("status") == "confirmed":
            specimens.setdefault(row["specimen_key"], {"specimen_key": row["specimen_key"]})
    samples = {r["sample_id"]: dict(r) for r in read_tsv(root / "samples.tsv") if r.get("sample_id")}
    libraries = {r["library_id"]: dict(r) for r in read_tsv(root / "libraries.tsv") if r.get("library_id")}
    for s in samples.values():
        specimens.setdefault(s.get("specimen_key", ""), {"specimen_key": s.get("specimen_key", "")})
    specimens.pop("", None)

    tubes = {r["tube_id"]: dict(r) for r in read_tsv(root / "tubes.tsv") if r.get("tube_id")}
    sample_by_biosample = {s["biosample_accession"]: sid for sid, s in samples.items() if s.get("biosample_accession")}
    # A BioSample's sample_name is often the sample ID or the label on its tube.
    sample_by_name = {sid: sid for sid in samples}
    sample_by_name.update({tid: t["sample_id"] for tid, t in tubes.items() if t.get("sample_id") in samples})
    library_by_experiment = {l["experiment_accession"]: lid for lid, l in libraries.items() if l.get("experiment_accession")}
    spec_candidates, samp_candidates, lib_candidates = {}, {}, {}
    for o in observations:
        if o["level"] == "library":
            lid = library_by_experiment.get(o["ids"].get("experiment_accession", ""))
            if lid:
                for f, v in o["values"].items():
                    lib_candidates.setdefault((lid, f), []).append({"value": v, **o})
            continue
        key, matched_by = resolve_specimen(o, index)
        if o["level"] == "sample":
            sid = sample_by_biosample.get(o["ids"].get("biosample_accession", ""))
            if not sid:
                sid = sample_by_name.get(o["values"].get("sample_name_in_biosample", ""))
                if sid and samples[sid].get("biosample_accession"):
                    sid = None  # the sample already has a different BioSample; do not merge by name
            if sid:
                key = key or samples[sid].get("specimen_key")
                for f, v in o["values"].items():
                    if f in sample_fields:
                        samp_candidates.setdefault((sid, f), []).append({"value": v, **o})
        if not key:
            unmatched.append({"source": o["source"], "locator": o["locator"],
                              "identifiers": "; ".join(f"{k}={v}" for k, v in o["ids"].items()),
                              "reason": "no confirmed crosswalk entry or matching sample"})
            continue
        specimens.setdefault(key, {"specimen_key": key})
        for f, v in o["values"].items():
            if f in specimen_fields:
                spec_candidates.setdefault((key, f), []).append({"value": v, **o})
        for note in o["notes"]:
            spec_candidates.setdefault((key, "analysis_notes"), []).append({"value": f"{o['source']}: {note}", **o})

    corrections = {}
    for n, c in enumerate(read_tsv(root / "corrections.tsv"), start=2):
        k = (c.get("entity", "specimen"), c.get("key", ""), c.get("field", ""))
        if k in corrections:
            problems.append(("error", k[0], k[1], k[2], f"corrections.tsv:{n}: more than one correction for this field"))
        corrections[k] = c

    # Notes from sources are combined rather than chosen between.
    for key in specimens:
        notes = [c["value"] for c in spec_candidates.pop((key, "analysis_notes"), [])]
        if notes:
            specimens[key]["analysis_notes"] = "; ".join(dict.fromkeys(notes))

    # Names in public records are kept as a separate field rather than competing with determinations.
    for key in specimens:
        names = {}
        for c in spec_candidates.get((key, "scientific_name"), []):
            names.setdefault(c["value"], set()).add(c["source"])
        if names:
            specimens[key]["public_identification"] = "; ".join(
                f"{name} ({', '.join(sorted(srcs))})" for name, srcs in sorted(names.items()))
    assemble(specimens, [f for f in specimen_fields
                         if f not in ("specimen_key", "analysis_notes", "public_identification", "initial_identification",
                                      "identification_evidence", "scientific_name")],
             spec_candidates, corrections, "specimen", provenance, conflicts, problems, None)
    assemble(samples, [f for f in sample_fields if f not in ("sample_id", "specimen_key")],
             samp_candidates, corrections, "sample", provenance, conflicts, problems, None)
    assemble(libraries, [f for f in library_fields if f not in ("library_id", "sample_id")],
             lib_candidates, corrections, "library", provenance, conflicts, problems, None)

    # Determinations supply the initial and current identifications; public records supply their own names.
    determinations = read_tsv(root / "determinations.tsv")
    by_specimen = {}
    for d in determinations:
        by_specimen.setdefault(d.get("specimen_key"), []).append(d)
    for key, ds in by_specimen.items():
        if key not in specimens:
            continue
        initial = [d for d in ds if d.get("initial", "").lower() in ("yes", "y", "true")]
        if not initial:
            initial = sorted([d for d in ds if d.get("date_identified")], key=lambda d: d["date_identified"])[:1]
        if initial:
            specimens[key]["initial_identification"] = initial[0].get("informal_name") or initial[0].get("scientific_name", "")
    for key, row in specimens.items():
        if "_determined" not in row and not by_specimen.get(key):
            # Without a determination, the strongest public name stands in, and is reported as missing.
            ranked = sorted(spec_candidates.get((key, "scientific_name"), []), key=lambda c: PRECEDENCE.get(c["source"], 9))
            if ranked:
                row["scientific_name"] = ranked[0]["value"]
                provenance.append({"entity": "specimen", "key": key, "field": "scientific_name", "value": ranked[0]["value"],
                                   "source": ranked[0]["source"], "locator": ranked[0]["locator"]})
    for d in determinations:
        if d.get("current", "").lower() in ("yes", "y", "true") and d.get("specimen_key") in specimens:
            row = specimens[d["specimen_key"]]
            if d.get("evidence"):
                row["identification_evidence"] = d["evidence"]
            for f in ("scientific_name", "identification_qualifier", "informal_name", "aphia_id", "ncbi_taxid",
                      "identified_by", "date_identified"):
                if d.get(f):
                    row[f] = d[f]
                    provenance.append({"entity": "specimen", "key": d["specimen_key"], "field": f, "value": d[f],
                                       "source": "determination", "locator": d.get("source", "determinations.tsv")})
            row["_determined"] = "yes"

    missing = []
    for entity, rows, fields in (("specimen", specimens, fields_for(schema, "specimen")),
                                 ("sample", samples, fields_for(schema, "sample")),
                                 ("library", libraries, fields_for(schema, "library"))):
        for key, row in rows.items():
            for f in fields:
                if f["required"] in ("yes", "recommended") and not row.get(f["field"]):
                    missing.append({"entity": entity, "key": key, "field": f["field"], "required": f["required"],
                                    "status": "not recorded in the reviewed sources"})
            if entity == "specimen" and not row.get("_determined"):
                missing.append({"entity": entity, "key": key, "field": "determination", "required": "yes",
                                "status": "no current determination in determinations.tsv"})

    out = root / "generated"
    write_tsv(out / "specimens.tsv", sorted(specimens.values(), key=lambda r: r["specimen_key"]), specimen_fields)
    write_tsv(out / "samples.tsv", sorted(samples.values(), key=lambda r: r["sample_id"]), sample_fields)
    write_tsv(out / "libraries.tsv", sorted(libraries.values(), key=lambda r: r["library_id"]), library_fields)
    write_tsv(out / "tubes.tsv", sorted(tubes.values(), key=lambda r: r["tube_id"]),
              [f["field"] for f in fields_for(schema, "tube")])
    manifest = []
    for lib in libraries.values():
        sample = samples.get(lib.get("sample_id"), {})
        spec = specimens.get(sample.get("specimen_key"), {})
        manifest.append({"library_id": lib["library_id"], "sample_id": lib.get("sample_id"),
                         "specimen_key": sample.get("specimen_key"), "specimen_voucher": spec.get("specimen_voucher"),
                         "scientific_name": spec.get("scientific_name"), "tissue": sample.get("tissue"),
                         "collection_date": spec.get("collection_date"), "decimal_latitude": spec.get("decimal_latitude"),
                         "decimal_longitude": spec.get("decimal_longitude"), "depth_m": spec.get("depth_m"),
                         "biosample_accession": sample.get("biosample_accession"),
                         "run_accessions": lib.get("run_accessions"),
                         "tube_ids": ";".join(sorted(tid for tid, tb in tubes.items()
                                                     if tb.get("library_id") == lib["library_id"]
                                                     or (tb.get("sample_id") == lib.get("sample_id") and not tb.get("library_id"))))})
    write_tsv(out / "manifest.tsv", sorted(manifest, key=lambda r: r["library_id"]),
              ["library_id", "sample_id", "specimen_key", "specimen_voucher", "scientific_name", "tissue",
               "collection_date", "decimal_latitude", "decimal_longitude", "depth_m", "biosample_accession",
               "run_accessions", "tube_ids"])
    write_tsv(out / "provenance.tsv", provenance, ["entity", "key", "field", "value", "source", "locator"])
    write_tsv(out / "conflicts.tsv", conflicts, ["entity", "key", "field", "chosen", "chosen_source", "alternatives"])
    write_tsv(out / "missing_fields.tsv", missing, ["entity", "key", "field", "required", "status"])
    write_tsv(out / "unmatched_records.tsv", unmatched, ["source", "locator", "identifiers", "reason"])
    write_tsv(out / "build_problems.tsv", [dict(zip(("level", "table", "key", "field", "message"), p)) for p in problems],
              ["level", "table", "key", "field", "message"])
    write_catalog_audit(root, out)
    print(f"Built {len(specimens)} specimens, {len(samples)} samples, {len(libraries)} libraries in {out}/: "
          f"{len(conflicts)} conflicts, {len(missing)} missing values, {len(unmatched)} unmatched records, "
          f"{len(problems)} build problems.")
    return 1 if any(p[0] == "error" for p in problems) else 0


def write_catalog_audit(root, out):
    """Public availability of each voucher, separate from whether the voucher is valid."""
    audit = {}
    for source in ("gbif_occurrence", "lux"):
        for folder in latest_retrievals(root, source):
            looked_up = folder.name.split("_")[0]
            for f in folder.glob("*.json"):
                if f.name == "retrieval.json":
                    continue
                payload = json.loads(f.read_text())
                query = parse_voucher(payload["query"])
                if not query:
                    continue
                entry = audit.setdefault(voucher_insdc(query), {"specimen_voucher": voucher_insdc(query)})
                records = payload.get("results") or payload.get("records") or []
                urls = []
                for r in records:
                    o = from_gbif_record(r, "museum", "") if source == "gbif_occurrence" else from_lux_record(r, "")
                    parts = parse_voucher(o["values"].get("specimen_voucher", ""))
                    if parts and voucher_match_key(parts) == voucher_match_key(query):
                        urls.append(o["locator"])
                prefix = "gbif" if source == "gbif_occurrence" else "lux"
                entry[f"{prefix}_status"] = "found" if urls else "no exact match"
                entry[f"{prefix}_url"] = "; ".join(urls)
                entry[f"{prefix}_lookup_date"] = looked_up
    write_tsv(out / "catalog_audit.tsv", sorted(audit.values(), key=lambda r: r["specimen_voucher"]),
              ["specimen_voucher", "gbif_status", "gbif_url", "gbif_lookup_date", "lux_status", "lux_url", "lux_lookup_date"])


# ----------------------------------------------------------------------------- OBIS context

def cmd_check_obis(args):
    root = Path(args.root)
    specimens = read_tsv(root / "generated" / "specimens.tsv")
    points, keys = [], []
    for s in specimens:
        try:
            points.append([float(s["decimal_longitude"]), float(s["decimal_latitude"])])
            keys.append(s["specimen_key"])
        except (KeyError, ValueError):
            pass
    files, requests_made = {}, []
    if points:
        url = "https://api.obis.org/xylookup"
        body = json.dumps({"points": points, "shoredistance": True, "grids": True, "areas": False}).encode()
        requests_made.append(url)
        result = json.loads(http_get(url, data=body, headers={"Content-Type": "application/json"}))
        files["xylookup.json"] = json.dumps({"specimen_keys": keys, "points": points, "results": result}, indent=1).encode()
    taxa = sorted({s["aphia_id"] for s in specimens if s.get("aphia_id")})
    stats = {}
    for aphia in taxa:
        url = f"https://api.obis.org/v3/statistics/env?taxonid={aphia}"
        requests_made.append(url)
        stats[aphia] = json.loads(http_get(url))
    if stats:
        files["depth_stats.json"] = json.dumps(stats, indent=1).encode()
    if not files:
        sys.exit("no coordinates or AphiaIDs in generated/specimens.tsv; run build first")
    print(save_retrieval(root, "obis", "context", files, requests_made))


def latest_obis(root):
    folders = latest_retrievals(root, "obis")
    lookup, depth = {}, {}
    for folder in folders:
        if (folder / "xylookup.json").exists():
            payload = json.loads((folder / "xylookup.json").read_text())
            for key, point, result in zip(payload["specimen_keys"], payload["points"], payload["results"]):
                lookup[key] = (point, result)
        if (folder / "depth_stats.json").exists():
            depth.update(json.loads((folder / "depth_stats.json").read_text()))
    return lookup, depth


# ----------------------------------------------------------------------------- validation

def check_value(field, value):
    t, fmt = field["type"], field["format"]
    if t in ("key", "accession", "voucher") or (t in ("string", "integer") and fmt.startswith("^")):
        if fmt.startswith("^") and not re.match(fmt, value):
            return f"'{value}' does not match {fmt}"
    if t == "decimal":
        try:
            x = float(value)
        except ValueError:
            return f"'{value}' is not a number"
        if field["field"] == "decimal_latitude" and not -90 <= x <= 90:
            return f"latitude {x} outside -90 to 90"
        if field["field"] == "decimal_longitude" and not -180 <= x <= 180:
            return f"longitude {x} outside -180 to 180"
        if field["field"].startswith("depth") or field["field"] == "coordinate_uncertainty_m":
            if x < 0:
                return f"{x} is negative; depths are positive metres below the surface"
    if t == "date":
        for part in value.split("/"):
            if not re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", part):
                return f"'{value}' is not an ISO 8601 date, partial date, or interval"
    if t == "enum" and value not in fmt.split("|"):
        return f"'{value}' is not one of {fmt}"
    return None


def cmd_validate(args):
    root = Path(args.root)
    schema = read_schema()
    out = root / "generated"
    issues = [dict(zip(("level", "table", "key", "field", "message"), (p["level"], p["table"], p["key"], p["field"], p["message"])))
              for p in read_tsv(out / "build_problems.tsv")]
    tables = {"specimen": read_tsv(out / "specimens.tsv"), "sample": read_tsv(out / "samples.tsv"),
              "library": read_tsv(out / "libraries.tsv"), "tube": read_tsv(out / "tubes.tsv")}
    if not tables["specimen"]:
        sys.exit("no generated/specimens.tsv; run build first")
    id_field = {"specimen": "specimen_key", "sample": "sample_id", "library": "library_id", "tube": "tube_id"}

    def issue(level, table, key, field, message):
        issues.append({"level": level, "table": table, "key": key, "field": field, "message": message})

    for table, rows in tables.items():
        seen = {}
        for row in rows:
            key = row.get(id_field[table], "")
            if key in seen:
                issue("error", table, key, id_field[table], "duplicate identifier")
            seen[key] = row
            for field in fields_for(schema, table):
                value = row.get(field["field"], "")
                if value:
                    message = check_value(field, value)
                    if message:
                        issue("error", table, key, field["field"], message)
    vouchers = {}
    for s in tables["specimen"]:
        key = s["specimen_key"]
        if s.get("specimen_voucher"):
            parts = parse_voucher(s["specimen_voucher"])
            match_key = voucher_match_key(parts) if parts else s["specimen_voucher"]
            if match_key in vouchers:
                issue("error", "specimen", key, "specimen_voucher", f"same voucher as {vouchers[match_key]}")
            vouchers[match_key] = key
        lo, hi, d = s.get("depth_min_m"), s.get("depth_max_m"), s.get("depth_m")
        try:
            if lo and hi and float(lo) > float(hi):
                issue("error", "specimen", key, "depth_min_m", f"minimum depth {lo} exceeds maximum {hi}")
            if d and lo and hi and not float(lo) <= float(d) <= float(hi):
                issue("error", "specimen", key, "depth_m", f"depth {d} outside the recorded range {lo}-{hi}")
        except ValueError:
            pass
        if s.get("depth_basis") == "convention" and "convention" not in (s.get("notes", "") + s.get("analysis_notes", "")).lower():
            issue("error", "specimen", key, "depth_basis", "depth set by convention, but no note names the convention")
    for s in tables["specimen"]:
        current = (s.get("informal_name") or s.get("scientific_name", "")).casefold()
        others = []
        if s.get("initial_identification") and s["initial_identification"].casefold() != current:
            others.append(f"initial '{s['initial_identification']}'")
        for part in filter(None, s.get("public_identification", "").split("; ")):
            name = part.rsplit(" (", 1)[0]
            if name.casefold() not in (current, s.get("scientific_name", "").casefold()):
                others.append(f"public '{part}'")
        if current and others and not s.get("identification_evidence"):
            issue("warning", "specimen", s["specimen_key"], "identification_evidence",
                  f"current identification '{s.get('informal_name') or s.get('scientific_name')}' differs from "
                  + ", ".join(others) + "; record the evidence in determinations.tsv")
    for s in tables["specimen"]:
        if re.match(r"^BW[0-9]+-[0-9]+", s["specimen_key"]):
            issue("warning", "specimen", s["specimen_key"], "specimen_key",
                  "looks like a blue-water dive ID without its trip; BW dive numbers repeat on every trip, so the key "
                  "should include the trip, e.g. 26Mar19-BW3-39")
    specimen_keys = {s["specimen_key"] for s in tables["specimen"]}
    for s in tables["sample"]:
        if s.get("specimen_key") not in specimen_keys:
            issue("error", "sample", s["sample_id"], "specimen_key", f"specimen '{s.get('specimen_key')}' not in specimens")
    sample_ids = {s["sample_id"] for s in tables["sample"]}
    for lib in tables["library"]:
        if lib.get("sample_id") not in sample_ids:
            issue("error", "library", lib["library_id"], "sample_id", f"sample '{lib.get('sample_id')}' not in samples")

    tube_ids = {tb["tube_id"] for tb in tables["tube"]}
    library_ids = {lib["library_id"] for lib in tables["library"]}
    parents = {tb["tube_id"]: tb.get("parent_tube_id", "") for tb in tables["tube"]}
    for tb in tables["tube"]:
        tid = tb["tube_id"]
        implied = classify_tube_id(tid)
        if tb.get("tube_id_type") and tb["tube_id_type"] != "other" and tb["tube_id_type"] != implied:
            issue("error", "tube", tid, "tube_id_type",
                  f"declared {tb['tube_id_type']}, but the ID's form is {implied}")
        if not tb.get("sample_id") and not tb.get("library_id"):
            issue("warning", "tube", tid, "sample_id", "tube is not linked to a sample or library")
        if tb.get("sample_id") and tb["sample_id"] not in sample_ids:
            issue("error", "tube", tid, "sample_id", f"sample '{tb['sample_id']}' not in samples")
        if tb.get("library_id") and tb["library_id"] not in library_ids:
            issue("error", "tube", tid, "library_id", f"library '{tb['library_id']}' not in libraries")
        if tb.get("parent_tube_id") and tb["parent_tube_id"] not in tube_ids:
            issue("error", "tube", tid, "parent_tube_id", f"parent tube '{tb['parent_tube_id']}' not in tubes")
        seen, current = set(), tid
        while parents.get(current):
            if current in seen:
                issue("error", "tube", tid, "parent_tube_id", "parent_tube_id chain loops back on itself")
                break
            seen.add(current)
            current = parents[current]

    lookup, depth_stats = latest_obis(root)
    for s in tables["specimen"]:
        key = s["specimen_key"]
        if key in lookup:
            point, result = lookup[key]
            try:
                same_point = abs(point[0] - float(s["decimal_longitude"])) < 1e-6 and abs(point[1] - float(s["decimal_latitude"])) < 1e-6
            except (KeyError, ValueError):
                same_point = False
            if not same_point:
                issue("warning", "specimen", key, "decimal_latitude", "coordinates changed since the last check-obis; rerun it")
            else:
                shore = result.get("shoredistance")
                bathymetry = (result.get("grids") or {}).get("bathymetry")
                if shore is not None and shore < 0:
                    issue("warning", "specimen", key, "decimal_latitude", f"point is {-shore} m inland according to OBIS")
                if bathymetry is not None and s.get("depth_m"):
                    if float(s["depth_m"]) > bathymetry + max(50, 0.1 * bathymetry):
                        issue("warning", "specimen", key, "depth_m",
                              f"depth {s['depth_m']} m exceeds the bathymetry ({bathymetry} m) at this point")
        stats = depth_stats.get(s.get("aphia_id", ""))
        if stats and s.get("depth_m"):
            bins = [b for b in stats.get("depth", []) if b.get("records")]
            if bins:
                width = (stats["depth"][1]["from"] - stats["depth"][0]["from"]) if len(stats["depth"]) > 1 else 10
                lo, hi = bins[0]["from"], bins[-1]["from"] + width
                if not lo <= float(s["depth_m"]) <= hi:
                    issue("warning", "specimen", key, "depth_m",
                          f"depth {s['depth_m']} m outside the OBIS records for this taxon ({lo}-{hi} m)")
    for c in read_tsv(out / "conflicts.tsv"):
        issue("warning", c["entity"], c["key"], c["field"], f"sources disagree; chose '{c['chosen']}' ({c['chosen_source']}); others: {c['alternatives']}")
    write_tsv(out / "validation.tsv", issues, ["level", "table", "key", "field", "message"])
    errors = sum(1 for i in issues if i["level"] == "error")
    print(f"{errors} errors, {len(issues) - errors} warnings; see {out / 'validation.tsv'}")
    return 1 if errors else 0


# ----------------------------------------------------------------------------- export

def cmd_export_biosample(args):
    root = Path(args.root)
    specimens = {s["specimen_key"]: s for s in read_tsv(root / "generated" / "specimens.tsv")}
    samples = read_tsv(root / "generated" / "samples.tsv")
    columns = ["*sample_name", "sample_title", "bioproject_accession", "*organism", "isolate", "*collection_date",
               "*geo_loc_name", "*tissue", "isolation_source", "collected_by", "depth", "identified_by", "lat_lon",
               "specimen_voucher", "dev_stage", "sex", "derived_from", "description"]
    rows, gaps = [], []
    for s in samples:
        if args.only_new and s.get("biosample_accession"):
            continue
        sp = specimens.get(s.get("specimen_key"), {})
        organism = sp.get("informal_name") or sp.get("scientific_name", "")
        lat_lon = (format_insdc_lat_lon(sp["decimal_latitude"], sp["decimal_longitude"])
                   if sp.get("decimal_latitude") and sp.get("decimal_longitude") else "")
        depth = ""
        if sp.get("depth_min_m") and sp.get("depth_max_m") and sp.get("depth_basis") == "interval_midpoint":
            depth = f"{sp['depth_min_m']}-{sp['depth_max_m']} m"
        elif sp.get("depth_m"):
            depth = f"{sp['depth_m']} m"
        row = {"*sample_name": s["sample_id"], "sample_title": s.get("sample_title", ""),
               "bioproject_accession": args.bioproject or "", "*organism": organism,
               "isolate": s.get("specimen_key", ""), "*collection_date": sp.get("collection_date", ""),
               "*geo_loc_name": sp.get("geo_loc_name", ""), "*tissue": s.get("tissue", ""),
               "isolation_source": sp.get("collection_method", ""), "collected_by": sp.get("collected_by", ""),
               "depth": depth, "identified_by": sp.get("identified_by", ""), "lat_lon": lat_lon,
               "specimen_voucher": sp.get("specimen_voucher", ""), "dev_stage": s.get("dev_stage", ""),
               "sex": s.get("sex", ""), "derived_from": s.get("derived_from", ""), "description": s.get("notes", "")}
        for column in columns:
            if column.startswith("*") and not row[column]:
                gaps.append(f"{s['sample_id']}: {column[1:]}")
                row[column] = "missing"
        if not row["isolation_source"]:
            row["isolation_source"] = "missing"
            gaps.append(f"{s['sample_id']}: isolation_source (collection_method)")
        rows.append(row)
    out = root / "generated" / "biosample_invertebrate.tsv"
    write_tsv(out, rows, columns)
    print(f"Wrote {len(rows)} rows to {out}")
    for gap in gaps:
        print(f"warning: {gap} is missing; filled with 'missing'", file=sys.stderr)


# ----------------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default="specimens", help="specimen data directory (default: specimens)")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("fetch-museum"); p.add_argument("vouchers", nargs="+"); p.add_argument("--no-lux", action="store_true")
    p.set_defaults(func=cmd_fetch_museum)
    p = sub.add_parser("fetch-insdc"); p.add_argument("accessions", nargs="+"); p.set_defaults(func=cmd_fetch_insdc)
    p = sub.add_parser("fetch-gbif-download"); p.add_argument("keys", nargs="+"); p.set_defaults(func=cmd_fetch_gbif_download)
    p = sub.add_parser("fetch-worms"); p.add_argument("names", nargs="*")
    p.add_argument("--from-determinations", action="store_true"); p.set_defaults(func=cmd_fetch_worms)
    p = sub.add_parser("build"); p.add_argument("--home-institution", nargs="*", default=["YPM"])
    p.set_defaults(func=cmd_build)
    p = sub.add_parser("check-obis"); p.set_defaults(func=cmd_check_obis)
    p = sub.add_parser("validate"); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("export-biosample"); p.add_argument("--bioproject"); p.add_argument("--only-new", action="store_true")
    p.set_defaults(func=cmd_export_biosample)
    args = parser.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
