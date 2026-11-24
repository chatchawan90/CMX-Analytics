"""Export Biology products lacking detailed categories and audit lookup coverage."""
import csv
from collections import defaultdict
from decimal import Decimal as D


def build_biology_missing(ytd, write_csv, root):
    missing_rows={year:[r for r in ytd[year] if r['category']=='Biology' and
                       (r['subcategory']=='Unclassified' or r['sbu']=='Unclassified')]
                  for year in (2025,2026)}
    lookup_path=root/'project/Millipore product - LR4_Biology 2023.csv'
    older_path=root/'project/cleaned_unique_category.csv'
    lookup=defaultdict(list)
    with lookup_path.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):lookup[r['Stockcode'].strip().upper()].append(r)
    with older_path.open(encoding='unicode_escape',newline='') as f:
        older={r['product_code'].strip().upper() for r in csv.DictReader(f)}
    grouped=defaultdict(lambda:{2025:[],2026:[]})
    for year,rows in missing_rows.items():
        for row in rows:grouped[row['sku']][year].append(row)
    records=[]
    for sku,years in grouped.items():
        all_rows=years[2025]+years[2026]
        latest=max(all_rows,key=lambda r:(r['date'],r['invoice']))
        current=years[2026]
        amounts={year:sum((r['revenue'] for r in rs),D(0)) for year,rs in years.items()}
        matches=lookup.get(sku.strip().upper(),[])
        fields=lambda field:'; '.join(sorted({r[field].strip() for r in matches if r[field].strip()}))
        records.append({'product_code':sku,'product_description':latest['description'],
                        'brand':latest['brand'],'category':'Biology',
                        'missing_subcategory':any(r['subcategory']=='Unclassified' for r in all_rows),
                        'missing_sbu':any(r['sbu']=='Unclassified' for r in all_rows),
                        'unclassified_revenue_2025_ytd_thb':amounts[2025],
                        'unclassified_revenue_2026_ytd_thb':amounts[2026],
                        'unclassified_revenue_change_thb':amounts[2026]-amounts[2025],
                        '2026_transaction_rows':len(current),
                        '2026_invoice_count':len({r['invoice'] for r in current}),
                        '2026_customer_count':len({r['customer'] for r in current}),
                        'last_unclassified_sale_date':str(latest['date']),
                        'exact_match_in_biology_product_list':bool(matches),
                        'biology_list_subcategory':fields('Sub Cat'),
                        'biology_list_sbu':fields('SBU'),
                        'exact_match_in_older_category_lookup':sku.strip().upper() in older,
                        'subcategory_to_confirm_with_merck':'','sbu_to_confirm_with_merck':''})
    records.sort(key=lambda r:(-r['unclassified_revenue_2026_ytd_thb'],r['product_code']))
    current=[r for r in records if r['2026_transaction_rows']>0]
    write_csv('biology_missing_categories_2026.csv',current)
    write_csv('biology_missing_categories_2025_2026.csv',records)
    for year in (2025,2026):
        assert sum((r[f'unclassified_revenue_{year}_ytd_thb'] for r in records),D(0))==sum((r['revenue'] for r in missing_rows[year]),D(0))
    current_total=sum((r['unclassified_revenue_2026_ytd_thb'] for r in current),D(0))
    all_biology=sum((r['revenue'] for r in ytd[2026] if r['category']=='Biology'),D(0))
    blank_both=sum(bool(r['exact_match_in_biology_product_list']) and not r['biology_list_subcategory'] and not r['biology_list_sbu'] for r in current)
    older_matches=sum(r['exact_match_in_older_category_lookup'] for r in current)
    def escape(value):return value.replace('|','\\|').replace('\n',' ')
    lines=['# Biology products missing detailed categories','',
           'Sales cutoff: 20 November 2026. Both comparison periods run from 1 January through 20 November. Excludes `บิลปลอม` and future-dated rows.','',
           f'**{len(current)} SKUs** have missing subcategory and/or SBU labels in current-year Biology sales. They represent **THB {current_total:,.2f}**, or **{current_total/all_biology*100:.2f}% of eligible Biology revenue**, across {len(missing_rows[2026])} exported transaction rows and {len({r["customer"] for r in missing_rows[2026]})} customers. Their sales are included in the export; detailed classification is missing.','',
           f'Exact-code lookup audit: **{blank_both} of {len(current)}** appear in `Millipore product - LR4_Biology 2023.csv` with both `Sub Cat` and `SBU` blank. **{older_matches}** have an exact, case-insensitive product-code match in `cleaned_unique_category.csv`. This establishes the missing lookup data; it does not assign a replacement category or exhaust fuzzy/alias matching.','',
           '## Largest current-year items','',
           '| Product code | Source product description | 2026 revenue THB | Customers |',
           '|---|---|---:|---:|']
    for r in current[:15]:
        lines.append(f'| {escape(r["product_code"])} | {escape(r["product_description"])} | {r["unclassified_revenue_2026_ytd_thb"]:,.2f} | {r["2026_customer_count"]} |')
    lines.extend(['','## Complete mapping lists','',
                  f'- [Current-year list: {len(current)} SKUs](biology_missing_categories_2026.csv), sorted by current revenue. Includes full descriptions, comparative unclassified sales, customer counts, lookup status and blank columns for Merck to confirm the subcategory and SBU.',
                  f'- [2025–2026 comparison: {len(records)} distinct SKUs](biology_missing_categories_2025_2026.csv). Includes products without 2026 sales so that the unclassified revenue decline can be investigated without omitting inactive products.','',
                  'Amounts in these files are sales on unclassified Biology rows, not a claim about total product revenue outside that scope. Product descriptions are preserved from the source, including any spelling or encoding issues. No category has been inferred from a product name and no master mapping has been changed.','',
                  'Ask Merck for its business-field/subcategory and SBU assignment by exact stock code and pack size. After confirmation, update the category mapping and reconcile total revenue before and after classification; mapping should redistribute revenue, not remove sales.'])
    (root/'project/MERCK_2027_strategy/biology_missing_items.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
