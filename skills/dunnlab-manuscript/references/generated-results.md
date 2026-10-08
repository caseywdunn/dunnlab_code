# Generated results

Numbers, tables, and figures are produced by the analysis repository's workflow and copied into the manuscript repository by one script. This keeps every reported result traceable to code and to a specific analysis commit.

## In the analysis repository

Add a workflow step, such as a Snakemake rule named `report_manuscript_results`, that writes everything the manuscript reports into one directory:

```text
results/manuscript/
├── values.tex
├── tables/
└── figures/
```

### Values

`values.tex` defines one LaTeX command per reported number:

```latex
\newcommand{\nSpecies}{212}
\newcommand{\medianLength}{1,204}
\newcommand{\pctRetained}{87.3\%}
```

Generate it from the analysis outputs, for example:

```python
values = {
    "nSpecies": f"{n_species:,}",
    "medianLength": f"{median_length:,.0f}",
    "pctRetained": f"{100 * retained / total:.1f}\\%",
}
with open(output_path, "w") as f:
    for name, value in values.items():
        f.write(f"\\newcommand{{\\{name}}}{{{value}}}\n")
```

- **Name commands with letters only.** LaTeX command names cannot contain digits or underscores: `\nSpeciesRaw`, not `\n_species_2`.
- **Format in the code:** rounding, thousands separators, and units. The text then never reformats a number, and every occurrence of a value matches.
- **Escape LaTeX special characters** in values, notably `%`, `_`, and `&`.
- **Use descriptive names.** The `.tex` source should read sensibly: `\nSpecies{} species` rather than `\valA{} species`.

### Tables

Write each table's body as LaTeX from code, for example with pandas `to_latex()`. Keep tables simple, with `booktabs` rules and no merged cells, where the content allows; complex layouts may not survive conversion to Word. The caption and label stay in `manuscript.tex`:

```latex
\begin{table}
  \caption{Taxon sampling. \nSpecies{} species were retained.}
  \label{tab:sampling}
  \input{generated/tables/sampling.tex}
\end{table}
```

### Figures

See [Figures](figures.md).

## Syncing into the manuscript repository

One script in the manuscript repository, such as `scripts/sync_results.sh`, copies `results/manuscript/` from a checkout of the analysis repository into `generated/`, then writes `generated/SOURCE`:

```text
repository: https://github.com/OWNER/project-a
commit: 3f2c9a1
synced: 2026-10-08
```

The script should:

- **refuse to sync** if the analysis checkout has uncommitted changes, since the commit would not identify what produced the results;
- **replace `generated/` completely**, so results deleted from the analysis do not linger; and
- leave a change that is committed on its own, with a message such as `Sync results from project-a@3f2c9a1`.

Nothing under `generated/` is edited by hand. To change a result, change the analysis, rerun it, commit, and sync again.

## Checking for typed results

As a review aid, list the numbers in `manuscript.tex` that are not inside a generated command or a citation, and confirm that each is not a result: a year, a method parameter, or a sample size stated in the design can legitimately be typed. Treat the list as something to read, not as an automatic gate.
