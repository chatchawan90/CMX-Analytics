# Biology products missing detailed categories

Sales cutoff: 20 November 2026. Both comparison periods run from 1 January through 20 November. Excludes `บิลปลอม` and future-dated rows.

**122 SKUs** have missing subcategory and/or SBU labels in current-year Biology sales. They represent **THB 3,364,196.46**, or **14.85% of eligible Biology revenue**, across 192 exported transaction rows and 78 customers. Their sales are included in the export; detailed classification is missing.

Exact-code lookup audit: **122 of 122** appear in `Millipore product - LR4_Biology 2023.csv` with both `Sub Cat` and `SBU` blank. **0** have an exact, case-insensitive product-code match in `cleaned_unique_category.csv`. This establishes the missing lookup data; it does not assign a replacement category or exhaust fuzzy/alias matching.

## Largest current-year items

| Product code | Source product description | 2026 revenue THB | Customers |
|---|---|---:|---:|
| HCYTA-60K-04 | MILLIPLEX Human Cytokine/Chemokine/Growth Factor Panel A - Immunology Multiplex Assay "Merck" 4markers (HCYTA-60K-04) marker : IL1B, IL6, IL10 และ IL12 | 250,852.00 | 1 |
| 12659-500GM | Albumin, Bovine Serum, Fraction V, Low Heavy Metals "Merck" 500G | 191,530.00 | 3 |
| S2GPT05RE | Sterile 500 mL Steritop Quick Release-GP 45 mm threaded bottle top filter with 0.22 um pore size "Merck" 12/Pk | 146,330.00 | 8 |
| UFC501096 | Amicon Ultra 0.5ML 10KDa "Merck" 96PK | 102,700.00 | 5 |
| 53702-250KU | PRONASE Protease, Streptomyces griseus "Merck" 250 KU | 99,600.00 | 1 |
| HCYTA-60K-10 | MILLIPLEX Human Cytokine/Chemokine/Growth Factor Panel A - Immunology Multiplex Assay "Merck" 10 markers | 91,470.00 | 1 |
| S2GPU05RE | Stericup-GP Sterile Vacuum Filtration System 500mL, PES, 0.22um,RS "Merck"  12/PK | 80,280.00 | 1 |
| SCME002 | ENDOGRO-VEGF COMPLETE MEDIA KIT "Merck" | 80,215.34 | 2 |
| RECYTMAG-65K-05 | MILLIPLEX MAP Rat Cytokine/Chemokine Magnetic Bead Panel - Immunology Multiplex Assay "Merck" 5 Markers: IL-1?,IL-6,IL-10,TNF? , IFN-gamma | 77,930.00 | 1 |
| SCC043 | C28/I2 Human Chondrocyte Cell Line "Merck" VIAL | 70,000.00 | 1 |
| HCYTA-60K-05 | MILLIPLEX Human Cytokine/Chemokine/Growth Factor Panel A "Merck" 5markers : EGF, bFGF, VEGF, PDGF, IL | 69,170.00 | 1 |
| 650345-1MG | Trypsin Inhibitor, CornINornINHIBITORS - PROTEASES "Merck" 1MG | 69,100.00 | 1 |
| ZTC18S096 | ZipTip with 0.6 uL C18 resin "Merck" 96/PK | 69,000.00 | 3 |
| IF009 | Interferon-a A Protein, Recombinant mouse 100000 units "Merck" | 67,050.00 | 1 |
| 02-102 | Endothelial Cell Growth Supplement, "Merck" 150MG | 61,190.00 | 3 |

## Complete mapping lists

- [Current-year list: 122 SKUs](biology_missing_categories_2026.csv), sorted by current revenue. Includes full descriptions, comparative unclassified sales, customer counts, lookup status and blank columns for Merck to confirm the subcategory and SBU.
- [2025–2026 comparison: 248 distinct SKUs](biology_missing_categories_2025_2026.csv). Includes products without 2026 sales so that the unclassified revenue decline can be investigated without omitting inactive products.

Amounts in these files are sales on unclassified Biology rows, not a claim about total product revenue outside that scope. Product descriptions are preserved from the source, including any spelling or encoding issues. No category has been inferred from a product name and no master mapping has been changed.

Ask Merck for its business-field/subcategory and SBU assignment by exact stock code and pack size. After confirmation, update the category mapping and reconcile total revenue before and after classification; mapping should redistribute revenue, not remove sales.
