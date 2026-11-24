"""Rank exact Biology SKUs sold in 2025 but not in 2026 through the cutoff."""
from collections import defaultdict
from decimal import Decimal as D


def build_biology_absent(rows, as_of, write_csv, root):
    current=[r for r in rows if r['year']==2026]
    # Search all recorded categories, so a category move does not create a false absence.
    sold_current={r['sku'].strip().upper() for r in current if r['revenue']>0}
    by_product=defaultdict(list)
    for row in rows:
        if row['year']==2025 and row['category']=='Biology':
            by_product[row['sku'].strip().upper()].append(row)
    results=[]
    account_details=[]
    for sku,previous in by_product.items():
        total=sum((r['revenue'] for r in previous),D(0))
        if sku in sold_current or total<=0:continue
        positive=[r for r in previous if r['revenue']>0]
        if not positive:continue
        latest=max(positive,key=lambda r:(r['date'],r['invoice']))
        comparable=sum((r['revenue'] for r in previous if (r['date'].month,r['date'].day)<=(as_of.month,as_of.day)),D(0))
        related_current=[r for r in current if r['sku'].strip().upper()==sku]
        results.append({'product_code':sku,'product_description':latest['description'],
                        'category_2025':'Biology','subcategory_2025':latest['subcategory'],
                        '2025_full_year_revenue_thb':total,'2025_comparable_ytd_revenue_thb':comparable,
                        '2025_after_comparison_cutoff_revenue_thb':total-comparable,
                        '2026_ytd_revenue_all_categories_thb':sum((r['revenue'] for r in related_current),D(0)),
                        '2026_positive_sales_rows_all_categories':0,
                        '2025_customer_count':len({r['customer'] for r in positive}),
                        '2025_invoice_count':len({r['invoice'] for r in positive}),
                        '2025_active_months':len({r['date'].month for r in positive}),
                        'last_positive_sale_2025':str(latest['date']),
                        'only_sold_after_comparison_cutoff_in_2025':comparable<=0,
                        '2025_customer_codes':'; '.join(sorted({r['customer'] for r in positive})),
                        'interpretation':'No positive sale of this exact SKU in the eligible export; aliases and substitutes unverified'})
        for cid in sorted({r['customer'] for r in positive}):
            sales=[r for r in previous if r['customer']==cid]
            last=max(sales,key=lambda r:(r['date'],r['invoice']))
            account_details.append({'product_code':sku,'product_description':latest['description'],
                                    'account_code':cid,'organization':last['name'],
                                    '2025_revenue_thb':sum((r['revenue'] for r in sales),D(0)),
                                    '2025_last_sale_date':str(last['date']),
                                    '2025_latest_recorded_salesperson':last['sales'],
                                    'owner_status':'Confirm current owner',
                                    'follow_up':'Check repeat need, project status, substitute or pack-size change'})
    results.sort(key=lambda r:(-r['2025_full_year_revenue_thb'],r['product_code']))
    ranked=[{'rank':i,**r} for i,r in enumerate(results,1)]
    top=ranked[:20]
    top_codes={r['product_code']:r['rank'] for r in top}
    details=[{'product_rank':top_codes[r['product_code']],**r} for r in account_details if r['product_code'] in top_codes]
    details.sort(key=lambda r:(r['product_rank'],-r['2025_revenue_thb'],r['account_code']))
    write_csv('biology_sold_2025_not_2026_all.csv',ranked)
    write_csv('biology_sold_2025_not_2026_top20.csv',top)
    write_csv('biology_sold_2025_not_2026_top20_accounts.csv',details)
    assert set(top_codes).isdisjoint(sold_current)
    assert sum((r['2025_revenue_thb'] for r in details),D(0))==sum((r['2025_full_year_revenue_thb'] for r in top),D(0))
    escape=lambda x:x.replace('|','\\|').replace('\n',' ')
    text=['# Biology products sold in 2025 with no 2026 sales','',
          f'Cutoff: {as_of}. Rank by full-year 2025 Biology revenue, excluding `บิลปลอม` invoices. Search for positive 2026 sales of the same exact SKU across all recorded categories; exclude future-dated rows. Category changes therefore do not by themselves mark a product as absent.','',
          f'**{len(ranked)} SKUs** meet this definition, representing **THB {sum((r["2025_full_year_revenue_thb"] for r in ranked),D(0)):,.2f}** of full-year 2025 revenue. The top 20 account for **THB {sum((r["2025_full_year_revenue_thb"] for r in top),D(0)):,.2f}**, including **THB {sum((r["2025_comparable_ytd_revenue_thb"] for r in top),D(0)):,.2f}** in the comparable January–20 November 2025 period.','',
          'This is an exact-SKU inactivity list, not proof of lost product-family demand. Custom assay configurations, pack sizes, renamed codes and substitutes require account review. The revenue is historical and is not automatically recoverable; the full missing-SKU amount is not the net Biology decline because other products grew or began selling.','',
          '| Rank | Product code | Source description | 2025 full year THB | 2025 comparable YTD THB | Customers | Last 2025 sale |',
          '|---|---|---|---:|---:|---:|---|']
    for r in top:
        text.append(f'| {r["rank"]} | {escape(r["product_code"])} | {escape(r["product_description"])} | {r["2025_full_year_revenue_thb"]:,.2f} | {r["2025_comparable_ytd_revenue_thb"]:,.2f} | {r["2025_customer_count"]} | {r["last_positive_sale_2025"]} |')
    text.extend(['','## Follow-up files','',
                 '- [Top 20 products](biology_sold_2025_not_2026_top20.csv): exact codes, full descriptions, revenue, buying frequency, customer codes and seasonality flags.',
                 '- [Customers for those products](biology_sold_2025_not_2026_top20_accounts.csv): organization, prior revenue and latest recorded 2025 salesperson for owner validation.',
                 '- [Complete absent-product list](biology_sold_2025_not_2026_all.csv): all qualifying SKUs, ranked by prior revenue.','',
                 'Before outreach, confirm the present account owner and check whether the same requirement moved to another SKU, marker configuration, pack size or supplier. Check project completion and ordering cadence before treating an absent purchase as a recovery opportunity. Product descriptions are preserved from the source, including any incomplete wording.'])
    (root/'project/MERCK_2027_strategy/biology_sold_2025_not_2026.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
