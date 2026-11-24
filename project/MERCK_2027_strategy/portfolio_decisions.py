"""Category/subcategory decision evidence for the dated 2027 strategy.

Priorities are commercial judgments, not an automated score or forecasts.
"""
from collections import defaultdict
from decimal import Decimal as D


DECISIONS = {
    ('Chemistry','Analytical Chemistry & Solvents'): ('Push',1,'Expand recurring applications; protect major-account orders'),
    ('Biomonitoring (LA2)','FB&O Microbiology (C52)'): ('Push',2,'Expand validated microbiology workflows in labs and food/beverage accounts'),
    ('Chemistry','Chemical Synthesis & Discovery Chemistry'): ('Push',3,'Expand applications in universities, research and laboratory services'),
    ('Chemistry','Reference Materials (RM)'): ('Push as cross-sell',4,'Attach application-matched standards to analytical workflows; rebuild buyer breadth'),
    ('Biology','Cell & General Workflow Tools'): ('Pilot',5,'Test repeatability before expanding campaign investment'),
    ('Chemistry','Material Science & Flavors and Fragrances (F&F)'): ('Selective expansion',6,'Expand known applications; validate the smaller buyer base'),
    ('Biology','Protein & Pathway Analysis'): ('Recover',1,'Recover application-level spend at declining existing accounts'),
    ('Biology','Cell Biology Reagents'): ('Recover',2,'Diagnose lower spend despite a larger buyer base'),
    ('Biomonitoring (LA2)','Pharma Microbiology (C51)'): ('Recover',3,'Validate projects, ordering cycles and supply before a broad campaign'),
    ('Biology','Partners & Alliances'): ('Selective recovery',4,'Review declining named accounts and portfolio fit'),
    ('Biology','Molecular Reagents & Tools'): ('Maintain and cross-sell',0,'Protect repeat business; qualify expansion without a broad growth claim'),
    ('Chemistry','Biochemistry'): ('Maintain and recover',0,'Protect existing applications and investigate spend declines'),
    ('Chemistry','Analytical Chromatography (AC)'): ('Opportunity-led only',0,'Validate isolated orders; do not extrapolate the headline growth rate'),
    ('Chemistry','Solvents (SOL)'): ('Opportunity-led only',0,'Check mapping and concentration before combining with analytical solvents'),
    ('Chemistry','BioChem Specialty & Kits'): ('Review classification',0,'Keep the recorded hierarchy; review the small unusual category bucket'),
    ('Diagnostics & Regulated Materials','Stains & Dyes'): ('Opportunity-led only',0,'Validate repeat demand beyond the largest account'),
}


def build_portfolio(ytd, write_csv):
    buckets = defaultdict(lambda:{2025:[],2026:[]})
    for year in (2025,2026):
        for row in ytd[year]:
            buckets[(row['category'],row['subcategory'])][year].append(row)
    evidence=[]
    industries=[]
    for (category,subcategory), years in sorted(buckets.items()):
        sums={}; accounts={}; invoices=defaultdict(set)
        for year,rows in years.items():
            customer_sums=defaultdict(lambda:D(0))
            for row in rows:
                customer_sums[row['customer']]+=row['revenue']
                if year==2026 and row['revenue']>0:invoices[row['customer']].add(row['invoice'])
            accounts[year]=dict(customer_sums)
            sums[year]=sum(customer_sums.values(),D(0))
        buyers={year:{k for k,v in accounts[year].items() if v>0} for year in years}
        top=max(accounts[2026],key=accounts[2026].get) if accounts[2026] else ''
        top_amount=accounts[2026].get(top,D(0))
        ex_prior=sums[2025]-accounts[2025].get(top,D(0))
        ex_current=sums[2026]-top_amount
        if subcategory=='Unclassified':
            decision=('Classify before allocation',0,'Map products before allocating subcategory growth or recovery targets')
        else:
            decision=DECISIONS.get((category,subcategory),('Maintain selectively',0,'Serve qualified applications; no broad campaign priority from current evidence'))
        evidence.append({'category':category,'subcategory':subcategory,'decision':decision[0],
                         'rank_within_growth_or_recovery_track':decision[1] or '',
                         'recommended_action':decision[2],
                         '2025_ytd_thb':sums[2025],'2026_ytd_thb':sums[2026],
                         'change_thb':sums[2026]-sums[2025],
                         'growth_pct':(sums[2026]/sums[2025]-1)*100 if sums[2025] else '',
                         '2025_buyers':len(buyers[2025]),'2026_buyers':len(buyers[2026]),
                         'retained_buyers':len(buyers[2025]&buyers[2026]),
                         '2026_buyers_with_2plus_invoices':sum(len(v)>=2 for v in invoices.values()),
                         'largest_2026_account':top,
                         'largest_account_share_pct':top_amount/sums[2026]*100 if sums[2026] else '',
                         'growth_excluding_largest_2026_account_pct':(ex_current/ex_prior-1)*100 if ex_prior else '',
                         'basis':'Revenue opportunity judgment; no margin or qualified pipeline data'})
        for industry in sorted({r['industry'] for r in years[2026]}):
            rows=[r for r in years[2026] if r['industry']==industry]
            industries.append({'category':category,'subcategory':subcategory,'industry':industry,
                               '2026_ytd_thb':sum((r['revenue'] for r in rows),D(0)),
                               '2026_buyers':len({r['customer'] for r in rows if r['revenue']>0})})
    for year in (2025,2026):
        assert sum((r[f'{year}_ytd_thb'] for r in evidence),D(0))==sum((r['revenue'] for r in ytd[year]),D(0))
    assert sum((r['2026_ytd_thb'] for r in industries),D(0))==sum((r['revenue'] for r in ytd[2026]),D(0))
    write_csv('category_subcategory_priorities.csv',evidence)
    write_csv('subcategory_industry_evidence.csv',industries)
