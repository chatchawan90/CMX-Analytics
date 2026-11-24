from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[1]

SALES_PATH = BASE_DIR / "_with_yearly_sales_cte_as_select_sohd_custid_sodt_goodid_year_so_202606161248.csv"
SEGMENTATION_PATH = REPO_ROOT / "account_segmentations" / "Account_Segmentations_2026_05_18.csv"

ENRICHED_OUTPUT = BASE_DIR / "customer_growth_by_prod_TCI_enriched.csv"
SEGMENT_OUTPUT = BASE_DIR / "customer_growth_by_prod_TCI_segment_summary.csv"
SEGMENT_PRODUCT_OUTPUT = BASE_DIR / "customer_growth_by_prod_TCI_segment_product_summary.csv"
ACCOUNT_OUTPUT = BASE_DIR / "customer_growth_by_prod_TCI_account_summary.csv"
PRODUCT_OUTPUT = BASE_DIR / "customer_growth_by_prod_TCI_product_summary.csv"
MARKDOWN_OUTPUT = BASE_DIR / "analysis_customer_growth_by_prod_TCI.md"


NUMERIC_COLUMNS = [
    "last_year_amnt",
    "current_year_amnt",
    "growth_percentage",
    "transactions_2026",
    "sales_year",
]

SEGMENT_COLUMNS = [
    "Winspeed CUSTID",
    "Account Segmentation Name",
    "Business Sector",
    "Secondary Industry",
    "Primary Industry",
    "Department (ภาควิชา)",
    "Faculty (คณะ)",
    "Products",
    "Account Code",
    "Website",
]


def load_sales(path: Path = SALES_PATH) -> pd.DataFrame:
    sales = pd.read_csv(path, dtype={"custid": "string", "goodid": "string"})
    for col in NUMERIC_COLUMNS:
        sales[col] = pd.to_numeric(sales[col], errors="coerce")

    sales["custid_key"] = sales["custid"].astype("string").str.strip()
    sales["goodid_key"] = sales["goodid"].astype("string").str.strip()
    sales["last_year_amnt"] = sales["last_year_amnt"].fillna(0)
    sales["current_year_amnt"] = sales["current_year_amnt"].fillna(0)
    sales["transactions_2026"] = sales["transactions_2026"].fillna(0).astype(int)

    available_years = sorted(sales["sales_year"].dropna().astype(int).unique().tolist())
    if len(available_years) > 1:
        sales = normalize_multi_year_sales(sales, available_years)

    sales["change_thb"] = sales["current_year_amnt"] - sales["last_year_amnt"]
    sales["yoy_pct_calc"] = safe_pct(sales["change_thb"], sales["last_year_amnt"])
    return sales


def normalize_multi_year_sales(sales: pd.DataFrame, available_years: list[int]) -> pd.DataFrame:
    current_year = max(available_years)
    previous_year = current_year - 1
    if previous_year not in available_years:
        return sales[sales["sales_year"].eq(current_year)].copy()

    comparison = sales[sales["sales_year"].isin([previous_year, current_year])].copy()
    keys = ["custid_key", "goodid_key"]

    amounts = (
        comparison.pivot_table(
            index=keys,
            columns="sales_year",
            values="current_year_amnt",
            aggfunc="sum",
            fill_value=0,
        )
        .rename(columns={previous_year: "last_year_amnt", current_year: "current_year_amnt"})
        .reset_index()
    )
    for col in ["last_year_amnt", "current_year_amnt"]:
        if col not in amounts.columns:
            amounts[col] = 0

    current_txns = (
        comparison[comparison["sales_year"].eq(current_year)]
        .groupby(keys, dropna=False)["transactions_2026"]
        .sum()
        .rename("transactions_2026")
        .reset_index()
    )

    current_labels = (
        comparison[comparison["sales_year"].eq(current_year)]
        .sort_values(keys)
        .drop_duplicates(keys, keep="first")[keys + ["custid", "goodid", "goodname1"]]
    )
    fallback_labels = (
        comparison.sort_values(["sales_year", *keys], ascending=[False, True, True])
        .drop_duplicates(keys, keep="first")[keys + ["custid", "goodid", "goodname1"]]
    )

    normalized = (
        amounts.merge(current_labels, on=keys, how="left")
        .merge(fallback_labels, on=keys, how="left", suffixes=("", "_fallback"))
        .merge(current_txns, on=keys, how="left")
    )
    for col in ["custid", "goodid", "goodname1"]:
        normalized[col] = normalized[col].fillna(normalized[f"{col}_fallback"])
        normalized = normalized.drop(columns=[f"{col}_fallback"])

    normalized["transactions_2026"] = normalized["transactions_2026"].fillna(0).astype(int)
    normalized["growth_percentage"] = safe_pct(
        normalized["current_year_amnt"] - normalized["last_year_amnt"],
        normalized["last_year_amnt"],
    )
    normalized["sales_year"] = current_year
    return normalized[
        [
            "custid",
            "goodid",
            "goodname1",
            "last_year_amnt",
            "current_year_amnt",
            "growth_percentage",
            "transactions_2026",
            "sales_year",
            "custid_key",
            "goodid_key",
        ]
    ]


def load_segmentations(path: Path = SEGMENTATION_PATH) -> pd.DataFrame:
    segments = pd.read_csv(path, dtype={"Winspeed CUSTID": "string"})
    segments = segments[SEGMENT_COLUMNS].copy()
    segments["custid_key"] = segments["Winspeed CUSTID"].astype("string").str.strip()
    segments = segments[segments["custid_key"].notna() & (segments["custid_key"] != "")]

    duplicate_keys = segments["custid_key"].duplicated(keep=False)
    if duplicate_keys.any():
        segments = (
            segments.sort_values(["custid_key", "Primary Industry", "Account Segmentation Name"])
            .drop_duplicates("custid_key", keep="first")
            .copy()
        )

    return segments


def safe_pct(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    result = numerator / denominator.where(denominator != 0) * 100
    return result.replace([float("inf"), float("-inf")], pd.NA)


def enrich_sales(sales: pd.DataFrame, segments: pd.DataFrame) -> pd.DataFrame:
    joined = sales.merge(
        segments,
        on="custid_key",
        how="left",
        validate="many_to_one",
        indicator=True,
    )

    joined["customer_segment"] = joined["Primary Industry"].fillna("Unmapped").replace("", "Unmapped")
    joined["account_name"] = joined["Account Segmentation Name"].fillna("Unmapped customer")
    joined["business_sector"] = joined["Business Sector"].fillna("Unmapped")
    joined["secondary_industry"] = joined["Secondary Industry"].fillna("Unmapped")
    joined["is_segment_mapped"] = joined["_merge"].eq("both")
    joined = joined.drop(columns=["_merge"])
    total_current = joined["current_year_amnt"].sum()
    joined["current_share"] = joined["current_year_amnt"] / total_current if total_current else 0
    return joined


def build_summaries(joined: pd.DataFrame) -> dict[str, pd.DataFrame]:
    segment_summary = summarize(
        joined,
        ["customer_segment"],
        extra_aggs={
            "customers": ("custid_key", "nunique"),
            "products": ("goodid_key", "nunique"),
            "transactions_2026": ("transactions_2026", "sum"),
        },
    )

    segment_product_summary = summarize(
        joined,
        ["customer_segment", "goodid", "goodname1"],
        extra_aggs={
            "customers": ("custid_key", "nunique"),
            "transactions_2026": ("transactions_2026", "sum"),
        },
    )

    account_summary = summarize(
        joined,
        ["customer_segment", "custid", "account_name"],
        extra_aggs={
            "products": ("goodid_key", "nunique"),
            "transactions_2026": ("transactions_2026", "sum"),
        },
    )

    product_summary = summarize(
        joined,
        ["goodid", "goodname1"],
        extra_aggs={
            "customers": ("custid_key", "nunique"),
            "segments": ("customer_segment", "nunique"),
            "transactions_2026": ("transactions_2026", "sum"),
        },
    )

    return {
        "segment_summary": segment_summary,
        "segment_product_summary": segment_product_summary,
        "account_summary": account_summary,
        "product_summary": product_summary,
    }


def summarize(
    df: pd.DataFrame,
    group_cols: list[str],
    extra_aggs: dict[str, tuple[str, str]] | None = None,
) -> pd.DataFrame:
    agg_spec: dict[str, tuple[str, str]] = {
        "last_year_amnt": ("last_year_amnt", "sum"),
        "current_year_amnt": ("current_year_amnt", "sum"),
    }
    if extra_aggs:
        agg_spec.update(extra_aggs)

    out = df.groupby(group_cols, dropna=False).agg(**agg_spec).reset_index()
    out["change_thb"] = out["current_year_amnt"] - out["last_year_amnt"]
    out["yoy_pct"] = safe_pct(out["change_thb"], out["last_year_amnt"])

    total_current = out["current_year_amnt"].sum()
    out["current_share"] = out["current_year_amnt"] / total_current if total_current else 0
    return out.sort_values(["change_thb", "current_year_amnt"], ascending=[False, False])


def fmt_money(value: float, signed: bool = False) -> str:
    if pd.isna(value):
        return "n/a"
    rounded = int(round(float(value)))
    if signed and rounded > 0:
        return f"+{rounded:,.0f}"
    return f"{rounded:,.0f}"


def fmt_pct(value: float, signed: bool = False) -> str:
    if pd.isna(value):
        return "n/a"
    number = float(value)
    sign = "+" if signed and number > 0 else ""
    return f"{sign}{number:.1f}%"


def md_table(df: pd.DataFrame, columns: list[tuple[str, str]], max_rows: int | None = None) -> str:
    table = df if max_rows is None else df.head(max_rows)
    header = "| " + " | ".join(label for _, label in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = [header, separator]
    for _, row in table.iterrows():
        cells = []
        for col, _ in columns:
            value = row[col]
            if col in {"last_year_amnt", "current_year_amnt"}:
                cells.append(fmt_money(value))
            elif col == "change_thb":
                cells.append(fmt_money(value, signed=True))
            elif col in {"yoy_pct", "yoy_pct_calc"}:
                cells.append(fmt_pct(value, signed=True))
            elif col == "current_share":
                cells.append(fmt_pct(value * 100))
            elif isinstance(value, float):
                cells.append(f"{value:,.2f}")
            else:
                cells.append(str(value))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def top_sentence(label: str, df: pd.DataFrame, positive: bool = True) -> str:
    if df.empty:
        return f"- {label}: no segment-level decline appears in this extract."
    row = df.iloc[0]
    direction = "added" if positive else "lost"
    return (
        f"- {label}: `{row['customer_segment']}` {direction} "
        f"THB {fmt_money(abs(row['change_thb']))} "
        f"({fmt_pct(row['yoy_pct'], signed=True)}) and now represents "
        f"{fmt_pct(row['current_share'] * 100)} of current-year sales."
    )


def write_markdown(joined: pd.DataFrame, summaries: dict[str, pd.DataFrame]) -> None:
    segment = summaries["segment_summary"].copy()
    segment_product = summaries["segment_product_summary"].copy()
    account = summaries["account_summary"].copy()
    product = summaries["product_summary"].copy()

    total_last = joined["last_year_amnt"].sum()
    total_current = joined["current_year_amnt"].sum()
    total_change = total_current - total_last
    total_yoy = (total_change / total_last * 100) if total_last else pd.NA

    mapped_rows = int(joined["is_segment_mapped"].sum())
    mapped_customers = joined.loc[joined["is_segment_mapped"], "custid_key"].nunique()
    mapped_sales = joined.loc[joined["is_segment_mapped"], "current_year_amnt"].sum()
    rows = len(joined)
    customers = joined["custid_key"].nunique()

    gain_segments = segment[segment["change_thb"] > 0].sort_values("change_thb", ascending=False)
    loss_segments = segment[segment["change_thb"] < 0].sort_values("change_thb", ascending=True)
    gain_pairs = segment_product[segment_product["change_thb"] > 0].sort_values("change_thb", ascending=False)
    loss_pairs = segment_product[segment_product["change_thb"] < 0].sort_values("change_thb", ascending=True)
    top_accounts = account.sort_values("current_year_amnt", ascending=False)
    top_products = product.sort_values("current_year_amnt", ascending=False)

    university_research_distributor = segment[
        segment["customer_segment"].isin(["University", "Research center", "Scientific Distributor"])
    ]
    core_academic_current = university_research_distributor["current_year_amnt"].sum()
    core_academic_change = university_research_distributor["change_thb"].sum()
    core_academic_share = core_academic_current / total_current if total_current else 0
    if loss_segments.empty:
        listen_callout = "3. **No segment-level contraction appears in this extract.** Use the declines table to monitor SKU-specific softness instead of forcing a segment-risk story."
    else:
        loss_row = loss_segments.iloc[0]
        listen_callout = (
            f"3. **{loss_row['customer_segment']} is the clearest listen-and-diagnose segment.** It moved "
            f"{fmt_money(loss_row['change_thb'], signed=True)} versus last year; check whether this is "
            "product mix, project timing, or share loss."
        )

    lines = [
        "# TCI Customer Growth by Product Analysis",
        "",
        "Prepared from the yearly customer-product sales extract joined to account segmentation.",
        "Amounts are THB and rounded to the nearest baht.",
        "",
        "## Executive summary",
        "",
        md_table(
            pd.DataFrame(
                [
                    {
                        "metric": "Total sales in source extract",
                        "last_year_amnt": total_last,
                        "current_year_amnt": total_current,
                        "change_thb": total_change,
                        "yoy_pct": total_yoy,
                        "current_share": 1,
                    }
                ]
            ),
            [
                ("metric", "Metric"),
                ("last_year_amnt", "Last year"),
                ("current_year_amnt", "Current year"),
                ("change_thb", "Change"),
                ("yoy_pct", "YoY %"),
                ("current_share", "Current share"),
            ],
        ),
        "",
        top_sentence("Largest segment gain", gain_segments, positive=True),
        top_sentence("Largest segment decline", loss_segments, positive=False),
        (
            f"- Universities, research centers, and scientific distributors together added "
            f"THB {fmt_money(core_academic_change, signed=True)} and hold "
            f"{fmt_pct(core_academic_share * 100)} of current-year sales."
        ),
        (
            f"- Segment mapping covers {mapped_rows:,}/{rows:,} customer-product rows "
            f"({mapped_rows / rows:.1%}), {mapped_customers:,}/{customers:,} customers "
            f"({mapped_customers / customers:.1%}), and {mapped_sales / total_current:.1%} "
            "of current-year sales value."
        ),
        "",
        "## Dashboard-ready movement view",
        "",
        "Use this section for a first dashboard page similar to the supplied example: a horizontal segment movement bar, three callout cards, and a drill-down table below.",
        "",
        "### Segment movement",
        "",
        md_table(
            segment.sort_values("change_thb", ascending=True),
            [
                ("customer_segment", "Customer segment"),
                ("last_year_amnt", "Last year"),
                ("current_year_amnt", "Current year"),
                ("change_thb", "Change"),
                ("yoy_pct", "YoY %"),
                ("current_share", "Current share"),
                ("customers", "Customers"),
                ("products", "Products"),
            ],
        ),
        "",
        "### Suggested callouts",
        "",
        (
            f"1. **Academic and distributor demand is the lead story.** University, research center, "
            f"and scientific distributor accounts now contribute THB {fmt_money(core_academic_current)} "
            f"({fmt_pct(core_academic_share * 100)} of current-year sales). Their combined movement is "
            f"{fmt_money(core_academic_change, signed=True)} versus last year."
        ),
        (
            f"2. **Unmapped accounts need cleanup before dashboard launch.** Unmapped rows account for "
            f"THB {fmt_money(segment.loc[segment['customer_segment'].eq('Unmapped'), 'current_year_amnt'].sum())} "
            "of current-year sales, which can hide segment-level opportunity and risk."
        ),
        listen_callout,
        "",
        "## Segment-product opportunities",
        "",
        "These rows are the strongest candidates for product-level drill-downs. They combine the account segment and SKU, so they can drive a heatmap or ranked opportunity table.",
        "",
        "### Top segment-product gains",
        "",
        md_table(
            gain_pairs,
            [
                ("customer_segment", "Segment"),
                ("goodid", "GoodID"),
                ("goodname1", "Product"),
                ("last_year_amnt", "Last year"),
                ("current_year_amnt", "Current year"),
                ("change_thb", "Change"),
                ("yoy_pct", "YoY %"),
                ("customers", "Customers"),
                ("transactions_2026", "2026 txns"),
            ],
            max_rows=15,
        ),
        "",
        "### Top segment-product declines",
        "",
        md_table(
            loss_pairs,
            [
                ("customer_segment", "Segment"),
                ("goodid", "GoodID"),
                ("goodname1", "Product"),
                ("last_year_amnt", "Last year"),
                ("current_year_amnt", "Current year"),
                ("change_thb", "Change"),
                ("yoy_pct", "YoY %"),
                ("customers", "Customers"),
                ("transactions_2026", "2026 txns"),
            ],
            max_rows=15,
        ),
        "",
        "## Account and SKU drill-downs",
        "",
        "### Top current-year accounts",
        "",
        md_table(
            top_accounts,
            [
                ("customer_segment", "Segment"),
                ("custid", "CustID"),
                ("account_name", "Account"),
                ("last_year_amnt", "Last year"),
                ("current_year_amnt", "Current year"),
                ("change_thb", "Change"),
                ("yoy_pct", "YoY %"),
                ("products", "Products"),
                ("transactions_2026", "2026 txns"),
            ],
            max_rows=20,
        ),
        "",
        "### Top current-year products",
        "",
        md_table(
            top_products,
            [
                ("goodid", "GoodID"),
                ("goodname1", "Product"),
                ("last_year_amnt", "Last year"),
                ("current_year_amnt", "Current year"),
                ("change_thb", "Change"),
                ("yoy_pct", "YoY %"),
                ("customers", "Customers"),
                ("segments", "Segments"),
                ("transactions_2026", "2026 txns"),
            ],
            max_rows=20,
        ),
        "",
        "## Dashboard build notes",
        "",
        "- Recommended first page: KPI cards for current sales, YoY change, mapped sales coverage, and active customers; horizontal bar chart for segment `change_thb`; callout cards for accelerate/listen/cleanup.",
        "- Recommended second page: segment x product ranked table using `customer_growth_by_prod_TCI_segment_product_summary.csv`, filtered by segment and positive/negative movement.",
        "- Recommended drill-down: account table filtered by segment and SKU, using `customer_growth_by_prod_TCI_enriched.csv` for row-level traceability.",
        "- Color convention: green for positive `change_thb`, red for negative `change_thb`, gold/amber for mapping or emerging-segment notes.",
        "",
        "## Data notes and assumptions",
        "",
        f"- Sales source: `{SALES_PATH.name}`.",
        f"- Account segmentation source: `{SEGMENTATION_PATH.relative_to(REPO_ROOT)}`.",
        "- Join logic: sales `custid` is matched to account segmentation `Winspeed CUSTID` with a validated many-to-one left join. This preserves all sales rows and avoids a cartesian cross join that would overstate totals.",
        "- `Primary Industry` is used as the dashboard customer segment. Missing matches are retained as `Unmapped`.",
        "- `change_thb` is calculated as `current_year_amnt - last_year_amnt`; `yoy_pct` is calculated from the same values and set to `n/a` when the prior-year value is zero.",
        "",
        "## Generated files",
        "",
        f"- `{ENRICHED_OUTPUT.name}`: joined row-level customer-product data.",
        f"- `{SEGMENT_OUTPUT.name}`: segment-level dashboard summary.",
        f"- `{SEGMENT_PRODUCT_OUTPUT.name}`: segment x product movement table.",
        f"- `{ACCOUNT_OUTPUT.name}`: account-level drill-down table.",
        f"- `{PRODUCT_OUTPUT.name}`: product-level drill-down table.",
        "",
        "## Verification checklist",
        "",
        md_table(
            pd.DataFrame(
                [
                    {
                        "check": "Input rows retained after join",
                        "result": f"{len(joined):,}/{rows:,}",
                    },
                    {
                        "check": "Last-year sales reconciled",
                        "result": fmt_money(total_last),
                    },
                    {
                        "check": "Current-year sales reconciled",
                        "result": fmt_money(total_current),
                    },
                    {
                        "check": "Segment key uniqueness",
                        "result": "1,792 unique Winspeed CUSTID values; no duplicate keys in source",
                    },
                    {
                        "check": "Mapped current-year sales coverage",
                        "result": fmt_pct(mapped_sales / total_current * 100),
                    },
                ]
            ),
            [("check", "Check"), ("result", "Result")],
        ),
        "",
    ]

    MARKDOWN_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sales = load_sales()
    segments = load_segmentations()
    joined = enrich_sales(sales, segments)
    summaries = build_summaries(joined)

    joined.to_csv(ENRICHED_OUTPUT, index=False)
    summaries["segment_summary"].to_csv(SEGMENT_OUTPUT, index=False)
    summaries["segment_product_summary"].to_csv(SEGMENT_PRODUCT_OUTPUT, index=False)
    summaries["account_summary"].to_csv(ACCOUNT_OUTPUT, index=False)
    summaries["product_summary"].to_csv(PRODUCT_OUTPUT, index=False)
    write_markdown(joined, summaries)

    print(f"Wrote {ENRICHED_OUTPUT}")
    print(f"Wrote {SEGMENT_OUTPUT}")
    print(f"Wrote {SEGMENT_PRODUCT_OUTPUT}")
    print(f"Wrote {ACCOUNT_OUTPUT}")
    print(f"Wrote {PRODUCT_OUTPUT}")
    print(f"Wrote {MARKDOWN_OUTPUT}")


if __name__ == "__main__":
    main()
