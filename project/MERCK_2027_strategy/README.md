# Merck 2027 strategy package

Start with the [strategy memo](strategy_memo.md), then use the [eight-slide meeting outline](meeting_outline.md) to prepare the Merck partner discussion. Both are editable Markdown documents. Revenue scenarios and account lists are provisional planning evidence, not agreed targets or qualified pipeline.

| File | Purpose |
|---|---|
| [strategy_memo.md](strategy_memo.md) | Recommendation, performance evidence, growth initiatives, three revenue scenarios, Merck support requests and execution plan |
| [meeting_outline.md](meeting_outline.md) | Slide messages, figures, speaker guidance, decision requests and anticipated questions |
| [category_push_playbook.md](category_push_playbook.md) | Ranked category and subcategory choices: push, cross-sell, pilot, recover and maintain |
| [category_subcategory_priorities.csv](category_subcategory_priorities.csv) | Hierarchical portfolio decisions with buyer breadth, repeat-invoice counts and concentration sensitivity |
| [subcategory_industry_evidence.csv](subcategory_industry_evidence.csv) | Industry evidence for the customer groups proposed in each subcategory |
| [biology_missing_items.md](biology_missing_items.md) | Biology products missing subcategory/SBU labels, largest items and lookup audit |
| [biology_missing_categories_2026.csv](biology_missing_categories_2026.csv) | All current-year unclassified Biology SKUs, with revenue and blank mapping-confirmation columns |
| [biology_missing_categories_2025_2026.csv](biology_missing_categories_2025_2026.csv) | Two-period product comparison, including items without current-year sales |
| [biology_sold_2025_not_2026.md](biology_sold_2025_not_2026.md) | Top Biology products sold in 2025 with no exact-SKU sales through the 2026 cutoff |
| [biology_sold_2025_not_2026_top20.csv](biology_sold_2025_not_2026_top20.csv) | Top 20 absent products ranked by full-year 2025 revenue |
| [biology_sold_2025_not_2026_top20_accounts.csv](biology_sold_2025_not_2026_top20_accounts.csv) | Prior customers and recorded salespeople for recovery review |
| [biology_sold_2025_not_2026_all.csv](biology_sold_2025_not_2026_all.csv) | Complete ranked list of absent Biology SKUs |
| [priority_accounts.csv](priority_accounts.csv) | 65 unique accounts for the first review wave, with one primary initiative and the latest recorded salesperson |
| [account_opportunities.csv](account_opportunities.csv) | Full historical account register, cohorts, sales changes, recovery signals and cross-sell candidates |
| [revenue_scenarios.csv](revenue_scenarios.csv) | Exact scenario arithmetic, assumptions and unvalidated growth requirements |
| [quarterly_targets.csv](quarterly_targets.csv) | Seasonal quarterly allocations for all three scenarios |
| [category_performance.csv](category_performance.csv) | Comparable YTD category totals, growth and concentration |
| [subcategory_performance.csv](subcategory_performance.csv) | Comparable YTD subcategory totals, including unclassified revenue |
| [industry_performance.csv](industry_performance.csv) | Comparable YTD industry view using the May 2026 segmentation snapshot |
| [industry_category_opportunities.csv](industry_category_opportunities.csv) | Current industry/category purchase breadth and repeat-invoice evidence |
| [brand_performance.csv](brand_performance.csv) | Merck-family brand breakdown |
| [account_category_changes.csv](account_category_changes.csv) | Account-level category contributions to growth and decline |
| [analysis_summary.json](analysis_summary.json) | Exact baseline, source hashes, exclusions, cohort bridge and assumptions |
| [methodology.md](methodology.md) | Definitions, formulas, limitations and reconciliation checks |
| [analyze_merck_2027.py](analyze_merck_2027.py) | Reproducible standard-library analysis; no database or network access |
| [portfolio_decisions.py](portfolio_decisions.py) | Portfolio decision labels and the supporting category/subcategory analysis, called by the main script |

Evidence cutoff: **20 November 2026**. Excludes future dates and `บิลปลอม`. Keep the account files as execution appendices and select the relevant account detail when preparing the partner meeting. No materials have been sent to Merck.

The analysis script regenerates CSV and JSON evidence and both Biology item notes. The strategy memo, portfolio playbook and meeting outline are reviewed narrative snapshots and require an editorial update if the source data or assumptions change.
