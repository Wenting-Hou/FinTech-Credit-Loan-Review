"""
generate_quality_reports.py

Runs data-quality validation queries against the constrained tables built by
build_relational_model.py and exports each result as a curated CSV report.
These are the "curated structured outputs" deliverable for the Database &
Analytics Lead role: not raw data, but processed, ready-to-read findings.

Prerequisite: run build_relational_model.py first to produce fintech.duckdb.

Usage:
    python generate_quality_reports.py
"""

import duckdb

DB_PATH = "fintech.duckdb"
OUTPUT_DIR = "reports"


def report_amount_exceeds_max(con: duckdb.DuckDBPyConnection) -> "duckdb.DuckDBPyRelation":
    """Applicants who requested more than their product's maximum allowed amount.

    A business-rule violation, not a referential integrity problem: the
    product reference is valid, but the requested value breaks the rule.
    """
    return con.execute("""
        SELECT a.applicant_id, a.requested_product_code, a.requested_amount_usd,
               lp.maximum_amount_usd
        FROM applicants a
        JOIN loan_products lp
            ON a.requested_product_code = lp.product_code
        WHERE a.requested_amount_usd > lp.maximum_amount_usd
    """).df()


def report_incomplete_records(con: duckdb.DuckDBPyConnection, null_threshold: int = 3) -> "duckdb.DuckDBPyRelation":
    """Applicant rows with an unusually high number of NULL fields
    (e.g. APP-00060 -- 10 of 11 nullable fields missing)."""
    nullable_columns = [
        "annual_income_usd", "employment_duration_months", "credit_risk_tier",
        "fico_score", "region_state", "requested_amount_usd",
        "requested_product_code", "dti_pct", "military_scra_flag",
        "bankruptcy_last_7y_flag", "preliminary_decision",
    ]
    null_count_expr = " + ".join(f"CASE WHEN {c} IS NULL THEN 1 ELSE 0 END" for c in nullable_columns)

    return con.execute(f"""
        SELECT applicant_id, ({null_count_expr}) AS null_field_count
        FROM applicants
        WHERE ({null_count_expr}) >= {null_threshold}
        ORDER BY null_field_count DESC
    """).df()


def report_duplicate_credit_events(con: duckdb.DuckDBPyConnection) -> "duckdb.DuckDBPyRelation":
    """Same applicant with more than one credit event on the same date --
    a potential duplicate/idempotency problem."""
    return con.execute("""
        SELECT applicant_id, event_date, COUNT(*) AS event_count
        FROM credit_pull
        GROUP BY applicant_id, event_date
        HAVING COUNT(*) > 1
    """).df()


def report_quarantine_summary(con: duckdb.DuckDBPyConnection) -> "duckdb.DuckDBPyRelation":
    """One row per quarantined/excluded row across the pipeline, with the
    reason -- so nothing that got dropped is invisible to a reader of the
    reports/ folder alone."""
    return con.execute("""
        SELECT 'loan_product.csv' AS source_file, 'line 20 ("SOL")' AS location,
               'truncated row, likely SOLAR-01 definition' AS reason
        UNION ALL
        SELECT 'credit_pull.csv', 'line 77 ("EVT-000076,APP-00")',
               'truncated row, cut off mid-value'
        UNION ALL
        SELECT 'applicant.csv (via applicants)', 'APP-00032 (SOLAR-01 reference)',
               'excluded: requested_product_code has no matching product'
    """).df()


def main() -> None:
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    con = duckdb.connect(DB_PATH)

    reports = {
        "amount_exceeds_max.csv": report_amount_exceeds_max(con),
        "incomplete_records.csv": report_incomplete_records(con),
        "duplicate_credit_events.csv": report_duplicate_credit_events(con),
        "quarantine_summary.csv": report_quarantine_summary(con),
    }

    for filename, df in reports.items():
        path = f"{OUTPUT_DIR}/{filename}"
        df.to_csv(path, index=False)
        print(f"{path}: {len(df)} row(s)")


if __name__ == "__main__":
    main()
