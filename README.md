# CMX-Analytics
MERCK
Currently it can group Merck product categories. THe categories file is from Merck [Last updated since Mid year 2023].

TCI
For TCI, we only need to clean the categories. HEnce there is no script. 


Updated 4/11/2024
- New BioM files with more details 1102024_NewBioM_2025 SKU LIST.xlsx
- Scripts for testing: 112024_BioM_NewFileTest.py and TEMP_PANDAS_TESTING (jupyter notebook)
- Convert to csv 112024_bioM2025_processed


Important files:
Main script
    -merck_revenue_with_categories_V2.py
    


## Revenue exports

Run from the repository root with the existing SQL Server environment variables
(`SERVER`, `DB`, `USERNAME`, `PASSWORD`) and dependencies installed:

```bash
python project/merck_revenue_with_categories_V2.py
```

The script now writes two versions:

- `searched_all.csv`: every row returned by the revenue query, with category
  enrichment. Keeps unmatched products with blank category fields, repeated
  products on separate invoice lines, and even identical source rows. Original
  source columns, values, and row order are preserved; `found` indicates whether
  a category lookup matched. Row alignment and original values are checked before
  writing. CSV uses UTF-8 with BOM for Thai text in Excel, without an added index.
- `searched.csv`: the existing categorized, deduplicated export used by the
  Merck 2027 strategy analysis.

“Every row” refers to the existing query scope: `bi_revenue`, `IVZ%` invoices,
2024–2026, and Merck, Sigma-Aldrich, Supelco, Roche, Sigma, Millipore, Aldrich.
The complete export adds no exclusions for missing categories, flagged invoices,
or future dates within those years. It does not expand the SQL query scope.
The existing GitHub Actions job runs this script and will produce both files once
this change is deployed. Generating `searched_all.csv` requires a fresh database
query; missing rows cannot be recovered from the old `searched.csv`.

Export regression checks (no database required):

```bash
python -m unittest discover -s tests -v
```
