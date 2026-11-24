"""Export category enrichment without filtering or changing source revenue rows."""

import pandas as pd


CATEGORY_COLUMNS = (
    'sbu_code', 'sbu_description', 'business_field_desc',
    'business_field_code', 'business_unit_code', 'business_unit_desc',
)
FALLBACK_COLUMNS = ('sbu_description', 'business_field_desc', 'business_unit_desc')
SKU = 'รหัสสินค้า'


def export_all_revenue(raw, first_pass, fallback, path):
    """Keep source order, duplicates and original values; append category fields.

    first_pass must still have one row per source row, in source order.
    fallback is the existing pipeline's one-row-per-product category lookup.
    Completeness is relative to the SQL result, including its scope filters.
    """
    source = raw.reset_index(drop=True)
    enriched = first_pass.reset_index(drop=True)
    if len(source) != len(enriched):
        raise ValueError('Category matching changed the source row count')
    keys = ['docuno', 'ลำดับ', SKU]
    expected_keys = source[keys].copy()
    expected_keys[SKU] = expected_keys[SKU].str.upper()
    if not expected_keys.equals(enriched[keys]):
        raise ValueError('Category matching changed the source row order or keys')
    if fallback[SKU].duplicated().any():
        raise ValueError('Fallback category lookup must have unique product codes')

    result = source.copy()
    for column in CATEGORY_COLUMNS:
        result[column] = enriched[column] if column in enriched else pd.Series(
            None, index=result.index, dtype=object)
    result['found'] = enriched['found'].fillna(False).astype(bool)
    lookup = fallback.set_index(SKU)
    matched = ~result['found'] & enriched[SKU].isin(lookup.index)
    for column in FALLBACK_COLUMNS:
        result.loc[matched, column] = enriched.loc[matched, SKU].map(lookup[column])
    result.loc[matched, 'found'] = True

    # Check every original field, not just totals: offsetting losses could hide
    # behind an unchanged revenue sum. This also protects duplicate source rows.
    if not result[source.columns].equals(source):
        raise ValueError('Complete export changed original revenue values')
    result.to_csv(path, index=False, encoding='utf-8-sig')
    return result
