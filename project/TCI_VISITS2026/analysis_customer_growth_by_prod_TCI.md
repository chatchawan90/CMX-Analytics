# TCI Customer Growth by Product Analysis

Prepared from the yearly customer-product sales extract joined to account segmentation.
Amounts are THB and rounded to the nearest baht.

## Executive summary

| Metric | Last year | Current year | Change | YoY % | Current share |
| --- | --- | --- | --- | --- | --- |
| Total sales in source extract | 26,163,255 | 13,422,940 | -12,740,315 | -48.7% | 100.0% |

- Largest segment gain: `Chemical manufacturer` added THB 72,010 (+32.6%) and now represents 2.2% of current-year sales.
- Largest segment decline: `University` lost THB 5,793,637 (-54.1%) and now represents 36.6% of current-year sales.
- Universities, research centers, and scientific distributors together added THB -9,714,847 and hold 67.2% of current-year sales.
- Segment mapping covers 7,466/8,486 customer-product rows (88.0%), 323/447 customers (72.3%), and 89.8% of current-year sales value.

## Dashboard-ready movement view

Use this section for a first dashboard page similar to the supplied example: a horizontal segment movement bar, three callout cards, and a drill-down table below.

### Segment movement

| Customer segment | Last year | Current year | Change | YoY % | Current share | Customers | Products |
| --- | --- | --- | --- | --- | --- | --- | --- |
| University | 10,710,566 | 4,916,929 | -5,793,637 | -54.1% | 36.6% | 163 | 2787 |
| Research center | 4,263,252 | 2,289,247 | -1,974,005 | -46.3% | 17.1% | 22 | 1116 |
| Scientific Distributor | 3,764,385 | 1,817,180 | -1,947,205 | -51.7% | 13.5% | 48 | 1147 |
| Unmapped | 2,967,363 | 1,370,885 | -1,596,479 | -53.8% | 10.2% | 124 | 903 |
| Manufacturing | 1,663,874 | 986,594 | -677,280 | -40.7% | 7.4% | 2 | 125 |
| Lab service | 1,373,890 | 1,148,360 | -225,530 | -16.4% | 8.6% | 20 | 197 |
| Consumer Goods | 199,310 | 18,300 | -181,010 | -90.8% | 0.1% | 4 | 7 |
| Petroleum | 326,920 | 171,320 | -155,600 | -47.6% | 1.3% | 5 | 46 |
| Electronics | 84,570 | 2,070 | -82,500 | -97.6% | 0.0% | 2 | 16 |
| Plastic and Rubber | 189,160 | 115,260 | -73,900 | -39.1% | 0.9% | 10 | 69 |
| Healthcare | 71,810 | 0 | -71,810 | -100.0% | 0.0% | 3 | 24 |
| Water Utilities | 38,430 | 0 | -38,430 | -100.0% | 0.0% | 2 | 2 |
| Agricultural | 26,660 | 2,880 | -23,780 | -89.2% | 0.0% | 1 | 4 |
| Building and Construction | 20,730 | 7,060 | -13,670 | -65.9% | 0.1% | 1 | 8 |
| Pharmaceutical | 32,210 | 22,180 | -10,030 | -31.1% | 0.2% | 5 | 21 |
| Packaging | 10,120 | 3,760 | -6,360 | -62.8% | 0.0% | 1 | 10 |
| Energy | 4,980 | 0 | -4,980 | -100.0% | 0.0% | 1 | 1 |
| Printing | 4,270 | 0 | -4,270 | -100.0% | 0.0% | 1 | 2 |
| Nuclear | 4,500 | 3,550 | -950 | -21.1% | 0.0% | 1 | 4 |
| Textile | 5,050 | 6,000 | +950 | +18.8% | 0.0% | 1 | 3 |
| School | 8,530 | 10,940 | +2,410 | +28.3% | 0.1% | 2 | 12 |
| Cosmetic | 24,540 | 28,200 | +3,660 | +14.9% | 0.2% | 2 | 22 |
| Food and Beverage | 37,650 | 42,120 | +4,470 | +11.9% | 0.3% | 7 | 22 |
| Hospital | 8,564 | 13,685 | +5,121 | +59.8% | 0.1% | 1 | 7 |
| Commercial & Professional Services | 101,360 | 153,850 | +52,490 | +51.8% | 1.1% | 2 | 41 |
| Chemical manufacturer | 220,560 | 292,570 | +72,010 | +32.6% | 2.2% | 16 | 34 |

### Suggested callouts

1. **Academic and distributor demand is the lead story.** University, research center, and scientific distributor accounts now contribute THB 9,023,356 (67.2% of current-year sales). Their combined movement is -9,714,847 versus last year.
2. **Unmapped accounts need cleanup before dashboard launch.** Unmapped rows account for THB 1,370,885 of current-year sales, which can hide segment-level opportunity and risk.
3. **University is the clearest listen-and-diagnose segment.** It moved -5,793,637 versus last year; check whether this is product mix, project timing, or share loss.

## Segment-product opportunities

These rows are the strongest candidates for product-level drill-downs. They combine the account segment and SKU, so they can drive a heatmap or ranked opportunity table.

### Top segment-product gains

| Segment | GoodID | Product | Last year | Current year | Change | YoY % | Customers | 2026 txns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Manufacturing | 7443 | N,N-Dicyclohexylmethylamine "TCI"   500ML       | 112,960 | 666,000 | +553,040 | +489.6% | 2 | 7 |
| Lab service | 127278 | BSTFA-TMCS (99:1) [Derivatizing Reagent for GC] "TCI" 100ML | 378,000 | 493,400 | +115,400 | +30.5% | 5 | 8 |
| Chemical manufacturer | 3322 | Platinum(0) - 1,3-Divinyltetramethyldisiloxane Complex (19.0-21.5% as Pt) (contains 1,3-Divinyltetramethyldisiloxane) "TCI" 5G | 0 | 84,700 | +84,700 | n/a | 1 | 1 |
| Commercial & Professional Services | 30954 | 2,2'-Bipyridyl >99.0%(T) "TCI"  500G | 0 | 76,520 | +76,520 | n/a | 1 | 1 |
| Unmapped | 7000 | Diclofenac Sodium Salt "TCI"   25G         | 3,770 | 72,000 | +68,230 | +1809.8% | 2 | 1 |
| Research center | 103404 | 2-Methyltetrahydrofuran (stabilized with BHT) >98.0%(GC) "TCI"  500ML | 0 | 57,120 | +57,120 | n/a | 1 | 2 |
| Lab service | 8730 | BSTFA-TMCS (99:1) [Derivatizing Reagent for GC] "TCI" 25ML | 14,030 | 69,670 | +55,640 | +396.6% | 3 | 4 |
| Scientific Distributor | 6329 | 5-Fluoroorotic Acid Monohydrate >95.0%(T)(HPLC) "TCI" 1G | 0 | 52,650 | +52,650 | n/a | 1 | 3 |
| University | 9306 | gamma-Butyrolactone >99.0%(GC) "TCI"  500ML | 100,860 | 147,600 | +46,740 | +46.3% | 1 | 2 |
| Manufacturing | 132308 | Allyl Sulfide >98.0%(GC) "TCI"  250ML | 0 | 46,000 | +46,000 | n/a | 1 | 2 |
| Chemical manufacturer | 5037 | 4-Methoxyphenol "TCI"   500 G       | 2,320 | 46,400 | +44,080 | +1900.0% | 2 | 2 |
| University | 6477 | 1-Ethyl-3-methylimidazolium Acetate >94.0%(HPLC) "TCI"  25G | 0 | 41,560 | +41,560 | n/a | 1 | 2 |
| Petroleum | 128879 | 2-Chloropropionic Acid >98.0%(GC)(T) "TCI"  500G | 24,360 | 64,960 | +40,600 | +166.7% | 1 | 2 |
| Plastic and Rubber | 10355 | Acrylic Acid (stabilized with MEHQ) >99.0%(GC) "TCI"  500G | 7,800 | 46,900 | +39,100 | +501.3% | 2 | 4 |
| Unmapped | 334996 | Nickel(II) Acetate >98.0%(T) "TCI" 250G | 0 | 39,000 | +39,000 | n/a | 1 | 1 |

### Top segment-product declines

| Segment | GoodID | Product | Last year | Current year | Change | YoY % | Customers | 2026 txns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Petroleum | 7158 | Decahydronaphthalene (cis- and trans- mixture) "TCI"  500 ML      | 172,800 | 0 | -172,800 | -100.0% | 1 | 0 |
| Consumer Goods | 9306 | gamma-Butyrolactone >99.0%(GC) "TCI"  500ML | 171,120 | 0 | -171,120 | -100.0% | 1 | 0 |
| Manufacturing | 8562 | (+-)-10-Camphorsulfonic Acid >98.0%(T) "TCI"  500G | 163,040 | 0 | -163,040 | -100.0% | 1 | 0 |
| Manufacturing | 325944 | 2-(Bromoacetyl)-6-methoxynaphthalene >98.0%(GC) "TCI" 5G | 153,400 | 0 | -153,400 | -100.0% | 1 | 0 |
| Research center | 111527 | 1,3-Dioxolane (stabilized with BHT) "TCI" 500ML | 181,000 | 45,600 | -135,400 | -74.8% | 1 | 1 |
| University | 9527 | Bilirubin >80.0%(HPLC) "TCI" 1G | 128,510 | 0 | -128,510 | -100.0% | 3 | 0 |
| University | 310420 | Lead(II) Iodide (99.99%, trace metals basis) [for Perovskite precursor], >98.0%(T) "TCI" 100G | 171,930 | 58,120 | -113,810 | -66.2% | 2 | 1 |
| Manufacturing | 7543 | 2,3-Dimercapto-1-propanol, >95.0%(GC)(T) "TCI" 25G | 98,040 | 0 | -98,040 | -100.0% | 1 | 0 |
| University | 3634 | Polyethylene Glycol 6,000 "TCI"   500G        | 97,080 | 0 | -97,080 | -100.0% | 1 | 0 |
| University | 309840 | Cyproterone Acetate, >98.0%(HPLC) "TCI" 1G | 96,800 | 0 | -96,800 | -100.0% | 1 | 0 |
| Unmapped | 321213 | Bosutinib >95.0%(T)(HPLC) "TCI" 250MG | 90,000 | 0 | -90,000 | -100.0% | 1 | 0 |
| Unmapped | 327125 | 3-Methoxy-3-methylbutanol >98.0%(GC) "TCI" 500ML | 90,000 | 0 | -90,000 | -100.0% | 1 | 0 |
| Research center | 4968 | 2-Methylimidazole >98.0%(GC)(T) "TCI"  500G | 85,450 | 0 | -85,450 | -100.0% | 2 | 0 |
| Manufacturing | 138016 | S-Potassium Thioacetate >97.0%(T) "TCI"  250 G | 84,870 | 0 | -84,870 | -100.0% | 1 | 0 |
| Unmapped | 321214 | 1,3-Diaminopentane >96.0%(GC) "TCI" 25ML | 80,000 | 0 | -80,000 | -100.0% | 1 | 0 |

## Account and SKU drill-downs

### Top current-year accounts

| Segment | CustID | Account | Last year | Current year | Change | YoY % | Products | 2026 txns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| University | 150156 | มหาวิทยาลัยจุฬาลงกรณ์ คณะวิทยาศาสตร์ ภาควิชาเคมี | 1,392,346 | 734,550 | -657,796 | -47.2% | 654 | 271 |
| Manufacturing | 150628 | บริษัท ไทยออพติคอล กรุ๊ป จำกัด (มหาชน) | 308,674 | 729,234 | +420,560 | +136.2% | 6 | 11 |
| Research center | 150028 | สถาบันวิจัยจุฬาภรณ์ | 1,284,200 | 719,100 | -565,100 | -44.0% | 388 | 153 |
| Lab service | 150505 | บริษัท เอสจีเอส (ประเทศไทย) จำกัด | 692,070 | 640,930 | -51,140 | -7.4% | 51 | 43 |
| University | 150006 | มหาวิทยาลัยมหิดล คณะวิทยาศาสตร์ ภาควิชาเคมี | 1,141,495 | 525,700 | -615,795 | -53.9% | 469 | 185 |
| Research center | 150302 | สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ ศูนย์พันธุวิศวกรรมและเทคโนโลยีชีวภาพแห่งชาติ | 790,580 | 470,920 | -319,660 | -40.4% | 202 | 93 |
| Research center | 150301 | สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ นาโนเทค | 1,143,070 | 394,900 | -748,170 | -65.5% | 278 | 112 |
| Scientific Distributor | 150890 | บริษัท ทีทีเค ซาย เอนซ์ จำกัด | 525,000 | 296,100 | -228,900 | -43.6% | 184 | 78 |
| Scientific Distributor | 151175 | บริษัท ซีทีแลบอราตอรี่ จำกัด | 345,760 | 290,840 | -54,920 | -15.9% | 161 | 77 |
| University | 150783 | มหาวิทยาลัยเทคโนโลยีสุรนารี สำนักวิทยาศาสตร์ | 518,526 | 265,770 | -252,756 | -48.7% | 254 | 99 |
| Manufacturing | 150234 | Essilor Manufacturing (Thailand) Co.,Ltd. | 1,355,200 | 257,360 | -1,097,840 | -81.0% | 121 | 23 |
| Scientific Distributor | 151029 | ห้างหุ้นส่วนจำกัด เอ.ซี.เอส.ซีนอน | 122,400 | 243,120 | +120,720 | +98.6% | 63 | 41 |
| University | 150163 | มหาวิทยาลัยบูรพา คณะวิทยาศาสตร์ ภาควิชาเคมี | 279,560 | 217,819 | -61,741 | -22.1% | 159 | 80 |
| Lab service | 155012 | บริษัท ศูนย์ห้องปฏิบัติการและวิจัยทางการแพทย์และการเกษตรแห่งเอเซีย จำกัด (มหาชน) | 29,230 | 211,540 | +182,310 | +623.7% | 19 | 13 |
| University | 150023 | มหาวิทยาลัยมหิดล คณะเภสัชศาสตร์ | 411,687 | 204,081 | -207,606 | -50.4% | 221 | 96 |
| Commercial & Professional Services | 151397 | บริษัท ออโรเม็กซ์ จำกัด | 100,420 | 153,850 | +53,430 | +53.2% | 40 | 19 |
| University | 151193 | มหาวิทยาลัยมหิดล คณะวิทยาศาสตร์ ศูนย์วิจัยเทคโนโลยียาง | 101,840 | 150,930 | +49,090 | +48.2% | 3 | 3 |
| Unmapped | 174043 | Unmapped customer | 135,950 | 139,870 | +3,920 | +2.9% | 65 | 25 |
| University | 150429 | มหาวิทยาลัยศิลปากร คณะวิทยาศาสตร์ ภาควิชาเคมี | 238,060 | 128,570 | -109,490 | -46.0% | 76 | 33 |
| Research center | 150177 | สถาบันวิทยสิริเมธี | 65,540 | 127,530 | +61,990 | +94.6% | 52 | 30 |

### Top current-year products

| GoodID | Product | Last year | Current year | Change | YoY % | Customers | Segments | 2026 txns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7443 | N,N-Dicyclohexylmethylamine "TCI"   500ML       | 112,960 | 666,000 | +553,040 | +489.6% | 2 | 1 | 7 |
| 127278 | BSTFA-TMCS (99:1) [Derivatizing Reagent for GC] "TCI" 100ML | 378,000 | 493,400 | +115,400 | +30.5% | 5 | 1 | 8 |
| 9306 | gamma-Butyrolactone >99.0%(GC) "TCI"  500ML | 273,060 | 148,680 | -124,380 | -45.6% | 3 | 3 | 3 |
| 161194 | 1-Ethynyl-1-cyclohexanol, >98.0%(GC) "TCI"  500G | 113,500 | 112,800 | -700 | -0.6% | 2 | 2 | 3 |
| 140005 | 1-(Heptafluorobutyryl)imidazole [Acylating Agent] >97.0%(GC)(T) "TCI"  25G | 146,160 | 100,000 | -46,160 | -31.6% | 1 | 1 | 2 |
| 86965 | Dansyl Chloride, >98.0%(HPLC)(T) "TCI"  5G | 118,060 | 99,800 | -18,260 | -15.5% | 6 | 2 | 6 |
| 310420 | Lead(II) Iodide (99.99%, trace metals basis) [for Perovskite precursor], >98.0%(T) "TCI" 100G | 216,360 | 94,800 | -121,560 | -56.2% | 5 | 3 | 3 |
| 3322 | Platinum(0) - 1,3-Divinyltetramethyldisiloxane Complex (19.0-21.5% as Pt) (contains 1,3-Divinyltetramethyldisiloxane) "TCI" 5G | 0 | 84,700 | +84,700 | n/a | 1 | 1 | 1 |
| 7000 | Diclofenac Sodium Salt "TCI"   25G         | 21,060 | 83,080 | +62,020 | +294.5% | 10 | 4 | 4 |
| 323690 | Bis(chloromethyl) Sulfide >97.0%(GC) "TCI" 25G | 138,840 | 82,640 | -56,200 | -40.5% | 1 | 1 | 1 |
| 30954 | 2,2'-Bipyridyl >99.0%(T) "TCI"  500G | 0 | 76,520 | +76,520 | n/a | 1 | 1 | 1 |
| 8730 | BSTFA-TMCS (99:1) [Derivatizing Reagent for GC] "TCI" 25ML | 14,030 | 69,670 | +55,640 | +396.6% | 3 | 1 | 4 |
| 128879 | 2-Chloropropionic Acid >98.0%(GC)(T) "TCI"  500G | 24,360 | 64,960 | +40,600 | +166.7% | 1 | 1 | 2 |
| 5241 | Lipase from Porcine Pancreas "TCI"  25 G        | 68,950 | 61,530 | -7,420 | -10.8% | 7 | 4 | 5 |
| 10355 | Acrylic Acid (stabilized with MEHQ) >99.0%(GC) "TCI"  500G | 30,790 | 58,490 | +27,700 | +90.0% | 13 | 5 | 10 |
| 6329 | 5-Fluoroorotic Acid Monohydrate >95.0%(T)(HPLC) "TCI" 1G | 4,500 | 57,490 | +52,990 | +1177.6% | 3 | 2 | 4 |
| 103404 | 2-Methyltetrahydrofuran (stabilized with BHT) >98.0%(GC) "TCI"  500ML | 3,880 | 57,120 | +53,240 | +1372.2% | 2 | 2 | 2 |
| 6795 | 1,2-Dipalmitoyl-sn-glycero-3-phosphocholine >98.0%(HPLC) "TCI" 1G | 19,480 | 55,890 | +36,410 | +186.9% | 1 | 1 | 2 |
| 7193 | 1-(3-Dimethylaminopropyl)-3-ethylcarbodiimide Hydrochloride [Coupling Agent for Peptides Synthesis] >98.0%(T) "TCI" 25G | 60,850 | 49,160 | -11,690 | -19.2% | 10 | 4 | 8 |
| 5037 | 4-Methoxyphenol "TCI"   500 G       | 4,490 | 48,720 | +44,230 | +985.1% | 4 | 3 | 3 |

## Dashboard build notes

- Recommended first page: KPI cards for current sales, YoY change, mapped sales coverage, and active customers; horizontal bar chart for segment `change_thb`; callout cards for accelerate/listen/cleanup.
- Recommended second page: segment x product ranked table using `customer_growth_by_prod_TCI_segment_product_summary.csv`, filtered by segment and positive/negative movement.
- Recommended drill-down: account table filtered by segment and SKU, using `customer_growth_by_prod_TCI_enriched.csv` for row-level traceability.
- Color convention: green for positive `change_thb`, red for negative `change_thb`, gold/amber for mapping or emerging-segment notes.

## Data notes and assumptions

- Sales source: `_with_yearly_sales_cte_as_select_sohd_custid_sodt_goodid_year_so_202606161248.csv`.
- Account segmentation source: `account_segmentations/Account_Segmentations_2026_05_18.csv`.
- Join logic: sales `custid` is matched to account segmentation `Winspeed CUSTID` with a validated many-to-one left join. This preserves all sales rows and avoids a cartesian cross join that would overstate totals.
- `Primary Industry` is used as the dashboard customer segment. Missing matches are retained as `Unmapped`.
- `change_thb` is calculated as `current_year_amnt - last_year_amnt`; `yoy_pct` is calculated from the same values and set to `n/a` when the prior-year value is zero.

## Generated files

- `customer_growth_by_prod_TCI_enriched.csv`: joined row-level customer-product data.
- `customer_growth_by_prod_TCI_segment_summary.csv`: segment-level dashboard summary.
- `customer_growth_by_prod_TCI_segment_product_summary.csv`: segment x product movement table.
- `customer_growth_by_prod_TCI_account_summary.csv`: account-level drill-down table.
- `customer_growth_by_prod_TCI_product_summary.csv`: product-level drill-down table.

## Verification checklist

| Check | Result |
| --- | --- |
| Input rows retained after join | 8,486/8,486 |
| Last-year sales reconciled | 26,163,255 |
| Current-year sales reconciled | 13,422,940 |
| Segment key uniqueness | 1,792 unique Winspeed CUSTID values; no duplicate keys in source |
| Mapped current-year sales coverage | 89.8% |
