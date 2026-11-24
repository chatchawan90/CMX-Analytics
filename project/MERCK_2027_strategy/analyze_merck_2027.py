"""Reproduce Merck 2027 planning evidence without changing source exports.

Usage: python3 project/MERCK_2027_strategy/analyze_merck_2027.py
All amounts are Decimal THB; outputs are provisional categorized-export evidence.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal as D
from pathlib import Path
from portfolio_decisions import build_portfolio
from biology_missing_items import build_biology_missing
from biology_absent_products import build_biology_absent

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
AS_OF = date(2026, 11, 20)
AMOUNT = 'ยอดมูลค่าขายและลดหนี้ก่อนVAT'
ZERO = D(0)
MISSING = {'', 'nan', 'none', 'null'}


def clean(value):
    text = (value or '').strip()
    return 'Unclassified' if text.lower() in MISSING else text


def total(rows):
    return sum((r['revenue'] for r in rows), ZERO)


def group(rows, field):
    result = defaultdict(lambda: ZERO)
    for row in rows:
        result[row[field]] += row['revenue']
    return dict(result)


def write_csv(name, records):
    if not records:
        return
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        for record in records:
            writer.writerow({k: format(v.quantize(D('.01')), 'f') if isinstance(v, D) else v
                             for k, v in record.items()})


def main():
    source = ROOT / 'searched.csv'
    segpath = ROOT / 'account_segmentations/Account_Segmentations_2026_05_18.csv'
    with segpath.open(encoding='utf-8-sig', newline='') as f:
        segrows = list(csv.DictReader(f))
    segments = {}
    for r in segrows:
        code = r['Account Code'].strip()
        if code:
            assert code not in segments, 'Resolve duplicate segmentation keys before analysis'
            segments[code] = clean(r['Primary Industry'])
    assert {r['Currency'] for r in segrows} == {'THB'}
    with source.open(encoding='utf-8-sig', newline='') as f:
        raw = list(csv.DictReader(f))
    rows, excluded = [], defaultdict(lambda: {'rows': 0, 'revenue': ZERO})
    for r in raw:
        d = date.fromisoformat(r['docudate'])
        amount = D(r[AMOUNT])
        # Mutually exclusive exclusion counts: future dates first, then flagged invoices.
        reason = 'future_dated' if d > AS_OF else ('flagged_invoice' if r['บิลปลอม'].strip() else None)
        if reason:
            bucket = excluded[f'{reason}_{d.year}']
            bucket['rows'] += 1
            bucket['revenue'] += amount
            continue
        cid = r['รหัสลูกค้า'].strip()
        rows.append({'date': d, 'year': d.year, 'customer': cid, 'name': r['บริษัทหรือหน่วยงาน'].strip(),
                     'invoice': r['docuno'], 'line': r['ลำดับ'], 'sku': r['รหัสสินค้า'],
                     'description': r['รายละเอียดสินค้า'], 'brand': clean(r['แบรนด์']),
                     'category': clean(r['business_unit_desc']),
                     'subcategory': clean(r['business_field_desc']), 'sbu': clean(r['sbu_description']),
                     'industry': segments.get(cid, 'Unclassified'),
                     'sales': re.sub(r'\s*\(?T\..*$', '', r['Sales']).strip(), 'revenue': amount})
    full = {y: [r for r in rows if r['year'] == y] for y in (2024, 2025, 2026)}
    ytd = {y: [r for r in full[y] if (r['date'].month, r['date'].day) <= (AS_OF.month, AS_OF.day)]
           for y in full}
    build_portfolio(ytd, write_csv)
    build_biology_missing(ytd, write_csv, ROOT)
    build_biology_absent(rows, AS_OF, write_csv, ROOT)
    annualization = total(full[2025]) / total(ytd[2025])
    estimate = total(ytd[2026]) * annualization
    estimate_2024 = total(ytd[2026]) * total(full[2024]) / total(ytd[2024])
    ycust = {y: group(rs, 'customer') for y, rs in ytd.items()}
    fcust = {y: group(rs, 'customer') for y, rs in full.items()}
    detail = defaultdict(list)
    for r in rows:
        detail[r['customer']].append(r)
    accounts = []
    for cid, rs in detail.items():
        latest = max(rs, key=lambda r: (r['date'], r['invoice'], r['line']))
        current = [r for r in rs if r['year'] == 2026]
        prev = [r for r in rs if r['year'] == 2025 and (r['date'].month,r['date'].day) <= (AS_OF.month,AS_OF.day)]
        a, b = ycust[2025].get(cid, ZERO), ycust[2026].get(cid, ZERO)
        annual_previous = fcust[2025].get(cid, ZERO)
        projected = b * annualization
        if b > 0 and a > 0:
            cohort = 'Retained'
        elif b > 0 and annual_previous > 0:
            cohort = 'Prior year late-period buyer'
        elif b > 0 and fcust[2024].get(cid, ZERO) > 0:
            cohort = 'Reactivated from 2024'
        elif b > 0:
            cohort = 'First observed in 2026'
        elif annual_previous > 0:
            cohort = '2025 buyer inactive in 2026'
        else:
            cohort = '2024 only or zero revenue'
        bio_a = total([r for r in prev if r['category'] == 'Biology'])
        bio_b = total([r for r in current if r['category'] == 'Biology'])
        sub = group(current, 'subcategory')
        cats = group(current, 'category')
        recovery = max(annual_previous - projected, ZERO) if b > 0 else ZERO
        inactive_pool = annual_previous if b == 0 else ZERO
        cross_sell = sub.get('Analytical Chemistry & Solvents', ZERO) > 0 and sub.get('Reference Materials (RM)', ZERO) <= 0
        if inactive_pool > 0:
            action = 'Validate inactivity and win back 2025 demand'
            priority_basis = inactive_pool
        elif recovery > 0:
            action = 'Recover declining existing-account demand'
            priority_basis = recovery
        else:
            action = 'Protect and expand current demand'
            priority_basis = b
        accounts.append({'account_code': cid, 'customer': latest['name'], 'industry': latest['industry'],
                         'latest_recorded_salesperson': latest['sales'], 'sales_owner_status': 'Confirm current owner',
                         'cohort': cohort, 'revenue_2024_fy_thb': fcust[2024].get(cid,ZERO),
                         'revenue_2025_fy_thb': annual_previous, 'revenue_2025_ytd_thb': a,
                         'revenue_2026_ytd_thb': b, 'ytd_change_thb': b-a,
                         'estimated_2026_fy_thb': projected, 'decline_recovery_pool_thb': recovery,
                         'inactive_recovery_pool_thb': inactive_pool,
                         'biology_2025_ytd_thb': bio_a, 'biology_2026_ytd_thb': bio_b,
                         'biology_ytd_change_thb': bio_b-bio_a,
                         '2026_invoice_count': len({r['invoice'] for r in current}),
                         '2026_active_months': len({r['date'].month for r in current}),
                         'last_purchase_date': str(max(r['date'] for r in rs if r['revenue'] > 0)) if any(r['revenue'] > 0 for r in rs) else '',
                         '2026_category_count': sum(v > 0 for v in cats.values()),
                         '2026_categories': '; '.join(sorted(k for k,v in cats.items() if v > 0)),
                         'reference_materials_cross_sell_candidate': cross_sell,
                         'recommended_action': action, 'priority_basis_thb': priority_basis,
                         'qualification_status': 'Unqualified historical signal; not pipeline',
                         'confirmed_2027_incremental_revenue_thb': '', 'next_review_date': '2027-01-29'})
    accounts.sort(key=lambda r: r['revenue_2026_ytd_thb'], reverse=True)
    write_csv('account_opportunities.csv', accounts)
    ranked = []
    # One primary action per selected account avoids double-counting across initiative lists.
    selected = set()
    selectors = [
        ('Biology recovery', lambda r: max(-r['biology_ytd_change_thb'], ZERO), 15),
        ('Inactive account recovery', lambda r: r['inactive_recovery_pool_thb'], 15),
        ('Core account protection and expansion', lambda r: r['revenue_2026_ytd_thb'], 20),
        ('Reference materials qualification', lambda r: r['revenue_2026_ytd_thb'] if r['reference_materials_cross_sell_candidate'] else ZERO, 15),
    ]
    for initiative, key, limit in selectors:
        candidates = sorted((r for r in accounts if r['account_code'] not in selected and key(r)>0), key=key, reverse=True)[:limit]
        for rank, r in enumerate(candidates,1):
            selected.add(r['account_code'])
            ranked.append({'initiative': initiative, 'rank_within_initiative': rank,
                           'initiative_signal_thb': key(r), **r})
    write_csv('priority_accounts.csv', ranked)
    summaries = {}
    for field in ['category', 'subcategory', 'industry', 'brand']:
        sums = {y: group(rs,field) for y,rs in ytd.items()}
        result = []
        for key in set().union(*(set(x) for x in sums.values())):
            a,b = sums[2025].get(key,ZERO),sums[2026].get(key,ZERO)
            current = [r for r in ytd[2026] if r[field]==key]
            csum = group(current,'customer')
            product = {'group': key, '2024_ytd_thb': sums[2024].get(key,ZERO),
                       '2025_ytd_thb': a, '2026_ytd_thb': b, 'change_thb': b-a,
                       'growth_pct': (b/a-1)*100 if a else '',
                       '2026_customers': sum(v>0 for v in csum.values()),
                       '2026_top5_customer_share_pct': sum(sorted(csum.values(),reverse=True)[:5],ZERO)/b*100 if b else ZERO}
            result.append(product)
        result.sort(key=lambda r:r['2026_ytd_thb'],reverse=True)
        write_csv(f'{field}_performance.csv',result)
        summaries[field]=result
    # Historical bridge uses comparable YTD periods, with mutually exclusive account sets.
    active_a = {k for k,v in ycust[2025].items() if v>0}
    active_b = {k for k,v in ycust[2026].items() if v>0}
    both = active_a & active_b
    expansion = sum((max(ycust[2026][k]-ycust[2025][k],ZERO) for k in both),ZERO)
    contraction = sum((min(ycust[2026][k]-ycust[2025][k],ZERO) for k in both),ZERO)
    lapsed = sum((ycust[2025][k] for k in active_a-active_b),ZERO)
    addition = sum((ycust[2026][k] for k in active_b-active_a),ZERO)
    assert total(ytd[2025])+expansion+contraction-lapsed+addition == total(ytd[2026])
    bridge_hist={'2025_ytd':total(ytd[2025]),'retained_expansion':expansion,'retained_contraction':contraction,
                 'inactive_previous_buyers':-lapsed,'additional_current_buyers':addition,'2026_ytd':total(ytd[2026])}
    recovery_pool=sum((r['decline_recovery_pool_thb'] for r in accounts),ZERO)
    inactive_pool=sum((r['inactive_recovery_pool_thb'] for r in accounts),ZERO)
    scenarios=[]
    for name,growth,retention,decline_rate,inactive_rate,existing_share in [
        ('Conservative','.05','.96','.20','.15','.75'),
        ('Base','.10','.97','.35','.25','.75'),
        ('Supported stretch','.15','.98','.50','.35','.70')]:
        g,retain,dr,ir,es=map(D,[growth,retention,decline_rate,inactive_rate,existing_share])
        target=estimate*(1+g)
        attrition=estimate*(1-retain)
        decline=recovery_pool*dr
        inactive=inactive_pool*ir
        unallocated=target-(estimate-attrition+decline+inactive)
        assert unallocated>=0,'Scenario requires different allocation; do not hide a negative residual'
        existing=unallocated*es;new=unallocated-existing
        assert (estimate-attrition+decline+inactive+existing+new).quantize(D('.01'))==target.quantize(D('.01'))
        scenarios.append({'scenario':name,'estimated_2026_revenue_thb':estimate,'growth_pct':g*100,
                          '2027_target_thb':target,'retention_assumption_pct':retain*100,
                          'attrition_allowance_thb':-attrition,
                          'decline_recovery_assumption_pct':dr*100,'decline_recovery_thb':decline,
                          'inactive_recovery_assumption_pct':ir*100,'inactive_recovery_thb':inactive,
                          'required_existing_expansion_thb':existing,'required_new_customer_revenue_thb':new,
                          'total_gross_growth_required_thb':target-estimate+attrition,
                          'documented_incremental_pipeline_in_supplied_data_thb':ZERO,
                          'growth_not_validated_by_pipeline_data_thb':target-estimate+attrition})
    write_csv('revenue_scenarios.csv',scenarios)
    quarter_weights={q:total([r for r in full[2025] if (r['date'].month-1)//3+1==q])/total(full[2025]) for q in range(1,5)}
    quarterly=[]
    for scenario in scenarios:
        allocated=ZERO
        for quarter,weight in quarter_weights.items():
            value=(scenario['2027_target_thb']*weight).quantize(D('.01')) if quarter<4 else scenario['2027_target_thb'].quantize(D('.01'))-allocated
            allocated+=value
            quarterly.append({'scenario':scenario['scenario'],'quarter':f'Q{quarter}',
                              '2025_seasonality_weight_pct':weight*100,'2027_revenue_target_thb':value})
        assert allocated==scenario['2027_target_thb'].quantize(D('.01'))
    write_csv('quarterly_targets.csv',quarterly)
    # Named-account category changes provide evidence for recommendations, never probabilities.
    account_category=[]
    ca={y:group([{**r,'key':(r['customer'],r['category'])} for r in rs],'key') for y,rs in ytd.items()}
    names={r['account_code']:r for r in accounts}
    for cid,cat in set(ca[2025])|set(ca[2026]):
        a,b=ca[2025].get((cid,cat),ZERO),ca[2026].get((cid,cat),ZERO)
        account_category.append({'account_code':cid,'customer':names[cid]['customer'],'industry':names[cid]['industry'],
                                 'category':cat,'2025_ytd_thb':a,'2026_ytd_thb':b,'change_thb':b-a})
    account_category.sort(key=lambda r:r['change_thb'],reverse=True)
    write_csv('account_category_changes.csv',account_category)
    top_growth_accounts=sorted(accounts,key=lambda r:r['ytd_change_thb'],reverse=True)[:2]
    top_growth_ids={r['account_code'] for r in top_growth_accounts}
    ex_top_prior=total([r for r in ytd[2025] if r['customer'] not in top_growth_ids])
    ex_top_current=total([r for r in ytd[2026] if r['customer'] not in top_growth_ids])
    indcat=[]
    for ind in {r['industry'] for r in ytd[2026]}:
        for cat in {r['category'] for r in ytd[2026]}:
            rs=[r for r in ytd[2026] if r['industry']==ind and r['category']==cat]
            if not rs:continue
            cust=group(rs,'customer');inv=defaultdict(set)
            for r in rs:inv[r['customer']].add(r['invoice'])
            indcat.append({'industry':ind,'category':cat,'2026_ytd_thb':total(rs),
                           'customers':sum(v>0 for v in cust.values()),
                           'customers_with_2plus_invoices':sum(len(v)>=2 for v in inv.values()),
                           'top_customer_share_pct':max(cust.values())/total(rs)*100 if total(rs)>0 else ZERO})
    indcat.sort(key=lambda r:r['2026_ytd_thb'],reverse=True)
    write_csv('industry_category_opportunities.csv',indcat)
    metrics={'as_of':str(AS_OF),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
             'segmentation_sha256':hashlib.sha256(segpath.read_bytes()).hexdigest(),
             'raw_rows':len(raw),'eligible_rows':len(rows),'exclusions':dict(excluded),
             'years':{y:{'ytd_revenue':total(ytd[y]),'full_year_or_ytd_revenue':total(full[y]),
                         'ytd_accounts_with_records':len(ycust[y]),'ytd_buying_accounts':sum(v>0 for v in ycust[y].values()),
                         'ytd_rows':len(ytd[y])} for y in full},
             'annualization_factor_2025':annualization,'estimated_2026_fy':estimate,
             'estimated_2026_fy_using_2024':estimate_2024,
             'historical_bridge':bridge_hist,'retained_buyers':len(both),
             'inactive_ytd_buyers':len(active_a-active_b),'additional_ytd_buyers':len(active_b-active_a),
             '2026_top10_share_pct':sum(sorted(ycust[2026].values(),reverse=True)[:10],ZERO)/total(ytd[2026])*100,
             'top_two_growth_accounts':[r['account_code'] for r in top_growth_accounts],
             'top_two_growth_contribution':sum((r['ytd_change_thb'] for r in top_growth_accounts),ZERO),
             'growth_excluding_top_two_accounts_pct':(ex_top_current/ex_top_prior-1)*100,
             'matched_segmentation_revenue_pct':total([r for r in ytd[2026] if r['customer'] in segments])/total(ytd[2026])*100,
             'decline_recovery_pool':recovery_pool,'inactive_recovery_pool':inactive_pool,
             'reference_cross_sell_candidates':sum(r['reference_materials_cross_sell_candidate'] for r in accounts),
             'priority_account_count':len(ranked),'scenarios':scenarios,'summaries':summaries,
             'quarter_weights':quarter_weights,
             'cohort_summary':{c:{'accounts':sum(r['cohort']==c for r in accounts),
                                  '2026_ytd_revenue':sum((r['revenue_2026_ytd_thb'] for r in accounts if r['cohort']==c),ZERO)}
                               for c in sorted({r['cohort'] for r in accounts})}}
    # Reconciliation checks detect lost rows, fan-out and inconsistent grouping.
    assert len(rows)+sum(v['rows'] for v in excluded.values())==len(raw)
    assert total(rows)+sum((v['revenue'] for v in excluded.values()),ZERO)==sum((D(r[AMOUNT]) for r in raw),ZERO)
    for field, summary in summaries.items():
        assert sum((r['2026_ytd_thb'] for r in summary),ZERO)==total(ytd[2026]),field
    assert sum((r['revenue_2026_ytd_thb'] for r in accounts),ZERO)==total(ytd[2026])
    assert len(selected)==len(ranked)
    for scenario in scenarios:
        assert sum((scenario['2027_target_thb']*quarter_weights[q] for q in quarter_weights),ZERO).quantize(D('.01'))==scenario['2027_target_thb'].quantize(D('.01'))
    (OUT/'analysis_summary.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in metrics.items() if k not in ['summaries','quarter_weights']},ensure_ascii=False,indent=2,default=str))
    print('PASS: source exclusions, grouped totals, account totals, historical bridge, scenario bridges and unique priorities reconcile.')


if __name__=='__main__':
    main()
