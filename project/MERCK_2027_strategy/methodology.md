# Merck 2027 analysis methodology

Snapshot date: 20 November 2026, Asia/Bangkok. This analysis supports the [strategy memo](strategy_memo.md) and [meeting outline](meeting_outline.md). It does not modify the revenue export, category pipeline, CRM, database or GitHub workflow.

## Inputs and scope

- Revenue: repository-root `searched.csv`, 36,385 rows. SHA-256 is recorded in `analysis_summary.json` so the memo's exact input can be identified.
- Customer segmentation: `account_segmentations/Account_Segmentations_2026_05_18.csv`, 1,792 records. Join its `Account Code` to sales `รหัสลูกค้า`. The file has no duplicate nonblank account codes; the script stops if duplicates appear. `Winspeed CUSTID` is not the matching field.
- Revenue amount: `ยอดมูลค่าขายและลดหนี้ก่อนVAT`, summed at the existing exported-row grain using Python Decimal. This analysis does not sum invoice header amounts or multiply revenue by quantity.
- Currency: THB is the explicit currency of all segmentation records. The revenue export has no currency column; confirm the reporting currency against source accounting before financial sign-off. No foreign-exchange conversion is performed.
- Merck-family scope follows the existing pipeline: Merck, Sigma-Aldrich, Supelco, Roche, Sigma, Millipore and Aldrich. Not all listed brands have records. No additional brand mapping is inferred.
- Account labels use `บริษัทหรือหน่วยงาน`, not the contact-name field `ลูกค้า`. Accounts are distinct account codes, not deduplicated legal entities; departments with different codes remain separate.

## Filters and reconciliation

First exclude dates after 20 November 2026; then exclude any remaining row with a nonblank `บิลปลอม` flag. This ordering makes the exclusion buckets mutually exclusive. YTD comparisons use 1 January–20 November in all three years. Include legitimate negative adjustments if present; the current eligible 2026 dataset contains none.

| Reconciliation of the 2026 export | Rows | Revenue THB |
|---|---:|---:|
| Export before these analysis exclusions | 11,286 | 105,212,978.34 |
| Future-dated rows | −14 | −137,840.00 |
| Flagged invoices through the cutoff | −46 | −1,024,417.17 |
| **Eligible 2026 YTD** | **11,226** | **104,050,721.17** |

Across 2024–2026, 35,957 rows remain eligible. Missing subcategory/SBU values, including literal `nan`, become `Unclassified`; they are retained in revenue totals. Normalize whitespace in category descriptions. There is THB 3,364,196.46 of eligible 2026 revenue without a subcategory. This retained unclassified revenue is separate from sales already dropped upstream for lacking a business-unit category.

Segmentation matches 454 of 648 active accounts and 84.6994% of eligible 2026 revenue. All unmatched revenue remains in `Unclassified`. Apply the same May 2026 segmentation snapshot to all comparison years; this is a consistent grouping, not a reconstruction of historical industry assignments. Do not join multiple rows per account or infer missing classifications from names.

### Known upstream limitations

The source script queries `bi_revenue` using only `docuno LIKE 'IVZ%'`, years 2024–2026 and a fixed brand list. It subsequently deduplicates on invoice and product without line number, and drops missing business-unit categories. These steps can affect completeness. No missing amount has been established, and source database totals were not obtained for this analysis. Do not relabel this export as audited total Merck net sales.

The analysis checks arithmetic within the export. It cannot validate accounting completeness, cancellations, credit-note treatment, price/quantity causality, or pipeline coverage. Revenue changes are not attributed to pricing or volume because SKU units and transaction mix differ.

## Customer cohorts and account selection

A buying account has positive aggregate eligible revenue in the period. Comparable-YTD cohorts comprise 489 retained buyers, 138 prior-period buyers without current purchases, and 159 current buyers without prior-YTD purchases. The latter group is split using full-year history: 14 bought late in 2025, 27 bought in 2024 but not 2025, and 118 are first observed in 2026. “First observed” does not establish acquisition date before the available history.

The historical bridge separates positive and negative changes within retained accounts. It reconciles exactly: 98,503,851.59 +24,514,453.80 −18,886,477.51 −3,405,587.71 +3,324,481.00 =104,050,721.17.

Full-year 2025 inactive accounts total 149 and THB 3,721,867.71 of prior revenue; this is the reactivation planning pool. Late-year buying patterns and account-code changes need review before interpreting inactivity as churn.

All historical accounts appear in `account_opportunities.csv`. Select the 65-account first wave in this order, removing selected account codes from subsequent pools:

1. The 15 largest absolute Biology YTD declines.
2. The 15 largest full-year 2025 revenues among accounts without 2026 purchases.
3. The 20 largest remaining 2026 accounts by revenue.
4. The 15 largest remaining 2026 accounts buying Analytical Chemistry and Solvents but not Reference Materials.

This gives each selected account one primary initiative. Additional product/application opportunities can be recorded later but must not duplicate an incremental revenue amount. `initiative_signal_thb` is the relevant historical decline or spend, not a forecast. The latest salesperson is stripped of telephone details and included only for routing; ownership is unconfirmed. The organization label is taken from the latest eligible transaction.

The 341 Reference Materials candidates are buyers of Analytical Chemistry and Solvents with no positive recorded Reference Materials revenue in 2026. No technical compatibility, customer budget or competitor share is inferred. Repeat-purchase industry evidence counts at least two distinct invoices, not multiple lines on one invoice.

## Portfolio prioritization

The category push playbook uses the actual category/subcategory pair, preserving the source hierarchy even for labels such as Biochemistry under Chemistry. Revenue, buying accounts and repeat buyers are calculated at that pair's grain. A repeat buyer has at least two distinct invoices carrying positive revenue in that subcategory during current YTD. The concentration sensitivity identifies the largest 2026 customer for each subcategory and removes that same customer from both periods. It is a sensitivity test, not an adjusted forecast or proof of a one-off order.

Growth and recovery rankings are separate qualitative commercial judgments based on scale, growth, buyer breadth, repeat purchases and concentration. They are not an automated scoring model or a margin ranking. Industry recommendations use observed subcategory purchases in the existing segmentation. Missing subcategories remain unclassified and are not assigned to an adjacent label. Category/subcategory and industry evidence files each reconcile to eligible revenue. The playbook's additional reviews and support requests are proposed activities, not additional revenue beyond the account-based scenario bridge.

## Forecast and scenario arithmetic

Use the 2025 seasonal factor `111,574,550.71 / 98,503,851.59 = 1.1326922644`. Multiply 2026 YTD revenue by this factor to obtain the THB 117,857,446.97 baseline estimate. Using the equivalent 2024 factor yields THB 116,712,619.31. The selected factor is applied consistently across accounts for planning; individual account seasonality may differ materially.

For each active 2026 account, estimate full-year 2026 revenue with that common factor. Its recovery pool is `max(2025 full-year revenue − estimated 2026 revenue, 0)`. The sum is THB 21,455,897.53. For accounts without 2026 revenue, use full-year 2025 revenue as the separate inactive recovery pool. Accounts in these two pools are disjoint.

Targets are 105%, 110% and 115% of the estimated baseline. Assume revenue retention of 96%, 97% and 98%; recovery of active-account shortfalls of 20%, 35% and 50%; and recovery of inactive prior revenue of 15%, 25% and 35%. These percentages are explicit commercial planning assumptions, not empirically estimated probabilities.

Compute residual growth required after the retained baseline and both recovery components. Assign 75% / 75% / 70% of that residual to additional expansion and the remainder to new customers. The residual is a requirement to substantiate, not a bottom-up forecast. It is never hidden as an unnamed confirmed opportunity.

For future tracking, count active-account recovery up to the historical shortfall ceiling; only incremental revenue above that ceiling belongs to additional expansion for the same account. Inactive account sales belong to reactivation. New accounts must be checked against historical account identities. Apply one incremental amount and one expected invoice quarter per opportunity; category, industry and support-request totals are alternative views, not additions to the bridge.

No qualified-opportunity dataset was supplied. Consequently the supplied-data amount of documented 2027 incremental pipeline is zero, and the entire positive initiative requirement remains unvalidated by this dataset. This does not imply the commercial team has no pipeline elsewhere. The proposed 3× unweighted coverage threshold is an operating assumption to replace with actual conversion evidence.

Quarter targets use full-year 2025 revenue weights. Monetary calculations use Decimal and report cents in CSVs; the memo rounds to millions, so displayed component sums may differ slightly. The Q4 CSV target absorbs any cent-level rounding residual to keep the four reported quarters equal to the reported annual target.

## Validation and refresh

Run from the repository root:

```bash
python3 project/MERCK_2027_strategy/analyze_merck_2027.py
```

The analysis uses only the Python standard library. It rewrites its own evidence CSVs, JSON and the Biology missing-items note; it does not change input files or regenerate the strategy memo, portfolio playbook or meeting outline. Those narratives are dated snapshots and must be reviewed after any source or cutoff change. The cutoff is explicit in `AS_OF`; update it deliberately with the comparison-period and narrative review.

Checks reconcile raw rows and amounts to exclusions, account/category/subcategory/industry/brand totals to eligible revenue, customer cohorts to the historical revenue bridge, scenario components to annual targets, and quarterly targets to annual targets. The priority list must have 65 unique account codes for this snapshot. Input hashes are captured in the JSON summary.

Before committing the 2027 target, obtain a source-to-export revenue reconciliation, replace the estimated baseline with 2026 full-year actuals, validate current account owners and opportunities, and agree Merck support. Do not assume those steps have already been completed because the analysis checks pass.

## External references

Merck's [Analytical Chemistry Learning Hub](https://www.sigmaaldrich.com/US/en/life-science/learning-center/analytical-chemistry) and [webinar library](https://www.sigmaaldrich.com/US/en/collections/webinars), accessed 20 November 2026, support the existence of educational resources relevant to the proposed sessions. They are not evidence for Thailand market growth, local specialist availability, funding, demand or conversion rates. All quantitative commercial findings come from the local datasets above.
