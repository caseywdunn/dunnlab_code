#!/usr/bin/env python3
"""Check the manuscript's references to synced results before rendering.

Runs as a Quarto pre-render script. Fails if a value, table, or figure the
manuscript uses is missing from _results/. Warns about placeholders and about
an analysis bundle that has changed since the last sync.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

RESULTS = Path("_results")
META = re.compile(r"\{\{<\s*meta\s+((?:analysis|results)\.\S+?)\s*>\}\}")
INCLUDE = re.compile(r"\{\{<\s*include\s+(_results/\S+?)\s*>\}\}")
FIGURE = re.compile(r"\]\((_results/figures/[^)\s]+)\)")
PLACEHOLDER = re.compile(r"\[\[TBD[^\]]*\]\]")


def flatten(values: dict, prefix: str = "") -> set[str]:
    keys = set()
    for name, value in values.items():
        key = f"{prefix}{name}"
        keys |= flatten(value, key + ".") if isinstance(value, dict) else {key}
    return keys


def stale_warning() -> str | None:
    source_file = RESULTS / "SOURCE.json"
    if not source_file.is_file():
        return "no _results/SOURCE.json; run scripts/sync_results.py"
    source = json.loads(source_file.read_text())
    repo = Path(source["path"])
    if not (repo / ".git").exists():
        return None  # analysis repository not checked out here; nothing to compare
    current = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%H", "--", "manuscript"],
        capture_output=True, text=True,
    ).stdout.strip()
    if current and current != source["bundle_commit"]:
        return (f"results were synced from {source['bundle_commit'][:7]}, but the analysis "
                f"bundle is now at {current[:7]}; run scripts/sync_results.py")
    return None


def main() -> int:
    if not (RESULTS / "values.json").is_file():
        sys.exit("error: no _results/values.json; run scripts/sync_results.py")
    values = json.loads((RESULTS / "values.json").read_text())
    keys = flatten(values)

    errors, warnings = [], []
    for qmd in sorted(Path(".").glob("*.qmd")):
        for number, line in enumerate(qmd.read_text().splitlines(), 1):
            where = f"{qmd}:{number}"
            errors += [f"{where}: unknown value {k}" for k in META.findall(line) if k not in keys]
            errors += [f"{where}: missing file {p}" for p in INCLUDE.findall(line) if not Path(p).is_file()]
            for path in FIGURE.findall(line):
                base = Path(path)
                found = [base] if base.suffix else [base.with_suffix(".pdf"), base.with_suffix(".png")]
                errors += [f"{where}: missing figure {f}" for f in found if not f.is_file()]
            warnings += [f"{where}: placeholder {p}" for p in PLACEHOLDER.findall(line)]

    if values.get("analysis", {}).get("uncommitted_changes"):
        warnings.append("the analysis had uncommitted changes when these results were generated")
    stale = stale_warning()
    if stale:
        warnings.append(stale)
    for message in warnings:
        print(f"warning: {message}", file=sys.stderr)
    for message in errors:
        print(f"error: {message}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
