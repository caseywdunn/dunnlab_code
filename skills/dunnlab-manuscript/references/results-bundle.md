# The results bundle

Results move from the analysis repository to the manuscript in one direction, through one directory. The analysis repository decides what is reported; the manuscript repository only displays it.

## In the analysis repository

Add a workflow step, such as a Snakemake rule `report_manuscript_results`, that writes the bundle and nothing else:

```text
project-a/manuscript/
├── values.json
├── tables/
│   └── sampling.md
└── figures/
    ├── tree.pdf
    └── tree.png
```

**Commit the bundle.** It is small, and committing it means a release of the analysis archives exactly what the paper reports. The sync script refuses to copy a bundle with uncommitted changes.

### `values.json`

Write it with `write_values()` from [`templates/analysis/write_manuscript_values.py`](../templates/analysis/write_manuscript_values.py):

```python
from write_manuscript_values import write_values

write_values(
    "manuscript/values.json",
    {
        "n_species": f"{n_species:,}",
        "median_length": f"{median_length:,.0f} bp",
        "pct_retained": f"{100 * retained / total:.1f}%",
    },
    version=config.get("version"),  # optional; defaults to an exact git tag if there is one
    doi=config.get("doi"),          # optional
)
```

It produces:

```json
{
  "analysis": {
    "repository": "https://github.com/OWNER/project-a",
    "commit": "3984cd578f329adee4c571a5e8374624815b1695",
    "uncommitted_changes": false,
    "generated": "2026-10-09T12:34:32+00:00",
    "version": "1.0.0",
    "doi": "10.5281/zenodo.1234567"
  },
  "results": {
    "n_species": "215",
    "median_length": "1,204 bp",
    "pct_retained": "87.3%"
  }
}
```

- **`analysis`** identifies the code that produced the results: the GitHub origin URL in https form, the last commit, whether there were uncommitted changes, a UTC timestamp, and the version and DOI when they are specified.
- **`results`** holds every reported value, **already formatted as a string**: rounding, thousands separators, and units are decided in the analysis, so the manuscript never reformats a number and every occurrence matches. `write_values()` rejects unformatted numbers.
- Use descriptive snake_case keys, nested for grouping if useful: `results.sampling.n_species`. The manuscript reads `{{< meta results.n_species >}}`.
- Generate the bundle from committed code. If `uncommitted_changes` is true, the manuscript's check warns on every render.

### Tables

Write each table as a Markdown pipe table, without a caption. The caption stays in the manuscript, directly after the `include`. Keep tables simple, with no merged cells, so they convert cleanly to both PDF and Word.

### Figures

See [Figures](figures.md).

## In the manuscript repository

Copy [`templates/manuscript/`](../templates/manuscript/) into the repository: `_quarto.yml`, `scripts/sync_results.py`, and `scripts/check_results.py`. Both scripts need only Python's standard library.

### Syncing

```bash
python3 scripts/sync_results.py               # uses DEFAULT_ANALYSIS_REPO, e.g. ../project-a
python3 scripts/sync_results.py ~/repos/project-a
```

The script:

- refuses to run if the analysis repository's `manuscript/` has uncommitted changes, or has never been committed;
- replaces `_results/` completely, so results removed from the analysis do not linger;
- writes `_results/SOURCE.json` with the analysis path and the commit that last changed the bundle; and
- prints the commit command. Commit the sync on its own, e.g. `Sync results from project-a@3984cd5`. Its diff is the record of what changed in the paper's numbers and figures.

Nothing under `_results/` is edited by hand. To change a result, change the analysis, rerun it, commit, and sync again.

### Checking

`_quarto.yml` runs `scripts/check_results.py` before every render. It:

- **fails** if a `.qmd` file uses a `{{< meta analysis.* >}}` or `{{< meta results.* >}}` key missing from `values.json`, or includes a table or figure missing from `_results/`. Without this check, Quarto renders a missing value as `?meta:results.name` with only a warning;
- **warns** about `[[TBD ...]]` placeholders;
- **warns** if the results were generated from uncommitted analysis code; and
- **warns** if the analysis repository is checked out at the recorded path and its bundle has changed since the last sync.

## Why copy instead of reading the analysis repository directly

Reading `../project-a/manuscript/` at render time would be thinner, but the manuscript would then show whatever state the sibling checkout happened to be in, and nothing would record which version the paper used. The pinned copy makes every build reproducible from the manuscript repository alone, lets co-authors render without the analysis repository, and turns each update into a reviewable diff.
