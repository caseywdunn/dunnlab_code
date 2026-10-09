#!/usr/bin/env python3
"""Copy the analysis repository's manuscript/ bundle into _results/.

Records the analysis commit in _results/SOURCE.json so every render traces
back to the analysis version it reports. Commit the result on its own.
"""

import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_ANALYSIS_REPO = "../project-a"  # set when creating the manuscript repository
BUNDLE = "manuscript"
RESULTS = Path("_results")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "analysis_repo",
        nargs="?",
        default=DEFAULT_ANALYSIS_REPO,
        help=f"path to the analysis repository (default: {DEFAULT_ANALYSIS_REPO})",
    )
    args = parser.parse_args()

    repo = Path(args.analysis_repo)
    bundle = repo / BUNDLE
    if not (bundle / "values.json").is_file():
        sys.exit(f"error: no {BUNDLE}/values.json in {repo}")
    if git(repo, "status", "--porcelain", "--", BUNDLE):
        sys.exit(f"error: {bundle} has uncommitted changes; commit them in the analysis repository first")

    bundle_commit = git(repo, "log", "-1", "--format=%H", "--", BUNDLE)
    if not bundle_commit:
        sys.exit(f"error: {bundle} has never been committed in the analysis repository")
    try:
        remote = git(repo, "remote", "get-url", "origin")
    except subprocess.CalledProcessError:
        remote = None

    if RESULTS.exists():
        shutil.rmtree(RESULTS)
    shutil.copytree(bundle, RESULTS)
    source = {
        "repository": remote,
        "path": args.analysis_repo,
        "bundle_commit": bundle_commit,
        "synced": datetime.date.today().isoformat(),
    }
    (RESULTS / "SOURCE.json").write_text(json.dumps(source, indent=2) + "\n")

    print(f"Synced {bundle} at {bundle_commit[:7]} into {RESULTS}/")
    analysis = json.loads((RESULTS / "values.json").read_text()).get("analysis", {})
    if analysis.get("uncommitted_changes"):
        print("warning: the analysis had uncommitted changes when these results were generated", file=sys.stderr)
    print(f'Commit with: git add {RESULTS} && git commit -m "Sync results from {repo.resolve().name}@{bundle_commit[:7]}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
