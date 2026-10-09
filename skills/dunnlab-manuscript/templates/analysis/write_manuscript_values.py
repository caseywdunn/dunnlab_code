"""Write manuscript/values.json: the analysis's identity and its reported values.

Call write_values() from the workflow step that builds the manuscript bundle.
Values must already be formatted for display; the manuscript inserts them as-is.
"""

import datetime
import json
import re
import subprocess
from pathlib import Path


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def _https_url(remote: str) -> str | None:
    """Normalize git@github.com:owner/repo.git and https forms to https://github.com/owner/repo."""
    if not remote:
        return None
    match = re.match(r"^(?:git@|ssh://git@|https://)([^/:]+)[:/](.+?)(?:\.git)?/?$", remote)
    return f"https://{match.group(1)}/{match.group(2)}" if match else remote


def analysis_metadata(version: str | None = None, doi: str | None = None) -> dict:
    """Identify the analysis code that produced the results."""
    metadata = {
        "repository": _https_url(_git("remote", "get-url", "origin")),
        "commit": _git("rev-parse", "HEAD") or None,
        "uncommitted_changes": bool(_git("status", "--porcelain", "--", ".", ":!manuscript")),
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }
    version = version or _git("describe", "--tags", "--exact-match") or None
    if version:
        metadata["version"] = version
    if doi:
        metadata["doi"] = doi
    return metadata


def write_values(path: str | Path, results: dict, version: str | None = None, doi: str | None = None) -> None:
    """Write values.json with an `analysis` block and a `results` block."""
    for key, value in results.items():
        if not isinstance(value, (str, dict)):
            raise TypeError(f"results.{key} must be a formatted string, got {type(value).__name__}")
    document = {"analysis": analysis_metadata(version, doi), "results": results}
    Path(path).write_text(json.dumps(document, indent=2) + "\n")
