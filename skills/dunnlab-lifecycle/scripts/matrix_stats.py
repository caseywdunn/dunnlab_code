#!/usr/bin/env python3
"""Compute matrix statistics for the distilled matrices.tsv manifest.

Reads sequence alignments and reports taxa, sites, and occupancy so the
manifest is generated from the alignments themselves rather than transcribed
by hand. Supports FASTA, sequential/interleaved relaxed PHYLIP, and NEXUS.

Usage:
    matrix_stats.py aln1.fasta aln2.phy ... > matrices.tsv
    matrix_stats.py --derived-from hydro62-18s28s hydro62-18s28s-trimmed.fasta
"""

import argparse
import sys
from pathlib import Path

GAP_CHARS = set("-?.~")
MISSING_CHARS = set("nNxX")


def parse_fasta(text):
    records, name, chunks = {}, None, []
    for line in text.splitlines():
        if line.startswith(">"):
            if name is not None:
                records[name] = "".join(chunks)
            name, chunks = line[1:].strip().split()[0], []
        elif name is not None:
            chunks.append(line.strip())
    if name is not None:
        records[name] = "".join(chunks)
    return records


def parse_phylip(text):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    ntax, nchar = (int(x) for x in lines[0].split()[:2])
    records, order = {}, []
    for line in lines[1:]:
        parts = line.split(None, 1)
        if len(order) < ntax and len(parts) == 2 and len(records.get(parts[0], "")) == 0:
            records[parts[0]] = parts[1].replace(" ", "")
            order.append(parts[0])
        else:
            # Interleaved continuation block, in the same taxon order.
            idx = sum(1 for n in order if len(records[n]) >= nchar)
            if idx < len(order):
                records[order[idx]] += line.replace(" ", "").strip()
    return records


def parse_nexus(text):
    lines, in_matrix, records = text.splitlines(), False, {}
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("matrix"):
            in_matrix = True
            continue
        if in_matrix:
            if stripped.startswith(";") or stripped.lower().startswith("end"):
                break
            parts = stripped.split(None, 1)
            if len(parts) == 2:
                records.setdefault(parts[0], "")
                records[parts[0]] += parts[1].replace(" ", "")
    return records


def read_alignment(path):
    text = Path(path).read_text()
    head = text.lstrip()[:100].lower()
    if head.startswith(">"):
        return parse_fasta(text)
    if head.startswith("#nexus"):
        return parse_nexus(text)
    return parse_phylip(text)


def stats(records):
    """Occupancy is the fraction of cells that carry data, not gaps or missing."""
    if not records:
        raise ValueError("no sequences found")
    lengths = {len(s) for s in records.values()}
    if len(lengths) > 1:
        raise ValueError(f"ragged alignment: sequence lengths {sorted(lengths)}")
    nsites = lengths.pop()
    total = len(records) * nsites
    filled = sum(
        1
        for seq in records.values()
        for c in seq
        if c not in GAP_CHARS and c not in MISSING_CHARS
    )
    return len(records), nsites, (filled / total if total else 0.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("alignments", nargs="+")
    ap.add_argument("--derived-from", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--no-header", action="store_true")
    args = ap.parse_args()

    if not args.no_header:
        print("name\tdescription\ttaxa\tsites\toccupancy\tderived_from")

    failed = False
    for path in args.alignments:
        name = Path(path).stem
        try:
            ntax, nsites, occ = stats(read_alignment(path))
        except (ValueError, OSError, IndexError) as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            failed = True
            continue
        print(
            f"{name}\t{args.description}\t{ntax}\t{nsites}\t{occ:.3f}\t{args.derived_from}"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
