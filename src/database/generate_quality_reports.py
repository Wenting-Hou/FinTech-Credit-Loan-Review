"""
generate_quality_reports.py

Runs data-quality validation queries against the constrained tables built by
build_relational_model.py and exports each result as a curated CSV report.
These are the "curated structured outputs" deliverable for the Database &
Analytics Lead role: not raw data, but processed, ready-to-read findings.

Prerequisite: run build_relational_model.py first to produce fintech.duckdb.

Usage, from the repository root:
    python src/database/generate_quality_reports.py
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = (ROOT / "fintech.duckdb").as_posix()
OUTPUT_DIR = ROOT / "reports"


def report_amount_exceeds_max(con: duckdb.DuckDBPyConnection):
    """Applications that requested more than their product's maximum amount.

    A business-rule violation, not a referential integrity problem: the
    product reference is valid, but the requested value breaks the rule.
    The preliminary decision should be Declined for every row.
    """
    return con.execute("""
        SELECT a.application_id, a.applicant_id, a.product_code, a.requested_amount_usd,
               p.maximum_amount_usd, a.preliminary_decision
        FROM loan_applications a
        JOIN loan_products p USING (product_code)
        WHERE a.requested_amount_usd > p.maximum_amount_usd
        ORDER BY a.application_id
    """).df()


def report_incomplete_records(con: duckdb.DuckDBPyConnection):
    """Applications missing a value the contract requires.

    fico_score is excluded on purpose: it is empty by design for the
    NO_HISTORY applicants. final_decision is empty while an application is open.
    """
    required = ["applicant_id", "annual_income_usd", "employment_duration_months",
                "region_state", "requested_amount_usd", "product_code", "dti_pct",
                "military_scra_flag", "bankruptcy_last_7y_flag",
                "collections_past_12_months_flag", "preliminary_decision", "application_date"]
    missing = " + ".join(f"CASE WHEN {c} IS NULL THEN 1 ELSE 0 END" for c in required)
    return con.execute(f"""
        SELECT application_id, ({missing}) AS missing_required_fields
        FROM loan_applications
        WHERE ({missing}) > 0
        ORDER BY missing_required_fields DESC, application_id
    """).df()


def report_duplicate_credit_events(con: duckdb.DuckDBPyConnection):
    """Same application pulled from the same bureau more than once on the same date:
    a potential duplicate or idempotency problem."""
    return con.execute("""
        SELECT application_id, bureau_source, event_date, COUNT(*) AS event_count
        FROM credit_pull_events
        GROUP BY application_id, bureau_source, event_date
        HAVING COUNT(*) > 1
        ORDER BY application_id, event_date
    """).df()


def report_after_extract_date(con: duckdb.DuckDBPyConnection):
    """Applications dated after the extract date (controlled quality issue, quarantined)."""
    return con.execute("""
        SELECT application_id, applicant_id, application_date, preliminary_decision, final_decision
        FROM loan_applications
        WHERE after_extract_date
        ORDER BY application_date, application_id
    """).df()


def report_repeat_applicants(con: duckdb.DuckDBPyConnection):
    """Applicants with more than one application, side by side, to review consistency."""
    return con.execute("""
        SELECT a.applicant_id, a.application_id, a.application_date, a.product_code,
               a.annual_income_usd, a.employment_duration_months, a.fico_score,
               r.risk_tier, a.preliminary_decision
        FROM loan_applications a
        JOIN applicant_risk_features r USING (application_id)
        WHERE a.applicant_id IN (
            SELECT applicant_id FROM loan_applications GROUP BY applicant_id HAVING COUNT(*) > 1)
        ORDER BY a.applicant_id, a.application_date, a.application_id
    """).df()


def report_quarantine_summary(con: duckdb.DuckDBPyConnection):
    """One row per quality finding with its row count, so nothing flagged is invisible."""
    return con.execute("""
        SELECT 'loan_applications' AS table_name,
               'dated after the 2026-09-14 extract date' AS reason,
               COUNT(*) AS row_count
        FROM loan_applications WHERE after_extract_date
        UNION ALL
        SELECT 'loan_applications', 'requested amount above the product maximum', COUNT(*)
        FROM loan_applications a JOIN loan_products p USING (product_code)
        WHERE a.requested_amount_usd > p.maximum_amount_usd
        UNION ALL
        SELECT 'credit_pull_events', 'Error or Pending pull with no score', COUNT(*)
        FROM credit_pull_events WHERE event_status IN ('Error', 'Pending')
    """).df()


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    con = duckdb.connect(DB_PATH, read_only=True)

    reports = {
        "amount_exceeds_max.csv": report_amount_exceeds_max(con),
        "incomplete_records.csv": report_incomplete_records(con),
        "duplicate_credit_events.csv": report_duplicate_credit_events(con),
        "after_extract_date.csv": report_after_extract_date(con),
        "repeat_applicants.csv": report_repeat_applicants(con),
        "quarantine_summary.csv": report_quarantine_summary(con),
    }

    for filename, df in reports.items():
        path = OUTPUT_DIR / filename
        df.to_csv(path, index=False)
        print(f"reports/{filename}: {len(df)} row(s)")
    con.close()


if __name__ == "__main__":
    main()
