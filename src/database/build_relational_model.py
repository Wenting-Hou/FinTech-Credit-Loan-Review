"""
build_relational_model.py

Loads the five FinTech Credit & Loan Review source CSVs into DuckDB and
builds a constrained relational model (primary keys, foreign keys, typed
columns) on top of them.

Tables (see architecture/erd_diagram.md and metadata/structured_data_dictionary.csv):

  applicants               PK applicant_id
  loan_products            PK product_code
  loan_applications        PK application_id, FK applicant_id, FK product_code
  credit_pull_events       PK event_id, FK application_id
  applicant_risk_features  PK application_id (also FK), unique appli_risk_id

What the load normalizes, per the dataset contracts in metadata/:
  - money stored as text ("$147,346 ", "500,000") becomes DECIMAL(12,2)
  - M/D/YYYY dates in loan_application.csv and applicant.csv become DATE
  - TRUE/FALSE text becomes BOOLEAN
  - empty strings become NULL (a NO_HISTORY applicant has no FICO score)

Controlled quality issue handled here:
  - Applications dated after the 2026-09-14 extract date are loaded but
    flagged (after_extract_date = TRUE) instead of being dropped, so the
    quarantine is visible. Analytics should filter them out.

Usage, from the repository root:
    python src/database/build_relational_model.py

Then:
    python src/database/generate_quality_reports.py
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = (ROOT / "data" / "structured" / "raw").as_posix()
DB_PATH = (ROOT / "fintech.duckdb").as_posix()
EXTRACT_DATE = "2026-09-14"

MONEY = "CAST(NULLIF(REPLACE(REPLACE(TRIM({c}), '$', ''), ',', ''), '') AS DECIMAL(12,2))"
MDY = "CAST(strptime(NULLIF({c}, ''), '%m/%d/%Y') AS DATE)"
ISO = "CAST(NULLIF({c}, '') AS DATE)"
INT = "CAST(NULLIF({c}, '') AS INTEGER)"
DEC = "CAST(NULLIF({c}, '') AS DECIMAL(12,4))"
BOOL = "CASE WHEN {c} = '' THEN NULL ELSE UPPER({c}) = 'TRUE' END"
TEXT = "NULLIF({c}, '')"


def load_staging_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Load every CSV as all-text staging tables, so nothing is mis-typed or dropped on read."""
    for table, file in [
        ("_stg_applicant", "applicant.csv"),
        ("_stg_product", "loan_product.csv"),
        ("_stg_application", "loan_application.csv"),
        ("_stg_pull", "credit_pull_event.csv"),
        ("_stg_risk", "applicant_risk_features.csv"),
    ]:
        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM read_csv('{DATA_DIR}/{file}', header = true, all_varchar = true)
        """)


def select_list(columns: dict[str, str]) -> str:
    return ",\n            ".join(f"{expr.format(c=name)} AS {name}" for name, expr in columns.items())


def build_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Create the constrained tables, parents first, and insert typed rows."""
    for table in ("applicant_risk_features", "credit_pull_events", "loan_applications",
                  "loan_products", "applicants"):
        con.execute(f"DROP TABLE IF EXISTS {table}")

    con.execute("""
        CREATE TABLE applicants (
            applicant_id VARCHAR PRIMARY KEY,
            first_name VARCHAR, middle_name VARCHAR, last_name VARCHAR,
            birth_date DATE,
            address_line_1 VARCHAR, address_line_2 VARCHAR, city VARCHAR,
            state VARCHAR, zip_code VARCHAR, country_code VARCHAR,
            phone_number VARCHAR, email_address VARCHAR, preferred_contact_method VARCHAR,
            marital_status VARCHAR, citizenship_status VARCHAR, occupation VARCHAR
        )
    """)
    applicant_cols = {c: TEXT for c in [
        "applicant_id", "first_name", "middle_name", "last_name"]}
    applicant_cols["birth_date"] = MDY
    applicant_cols.update({c: TEXT for c in [
        "address_line_1", "address_line_2", "city", "state", "zip_code", "country_code",
        "phone_number", "email_address", "preferred_contact_method", "marital_status",
        "citizenship_status", "occupation"]})
    con.execute(f"INSERT INTO applicants SELECT {select_list(applicant_cols)} FROM _stg_applicant")

    con.execute("""
        CREATE TABLE loan_products (
            product_code VARCHAR PRIMARY KEY,
            product_name VARCHAR, product_family VARCHAR, eligibility_criteria VARCHAR,
            minimum_risk_tier VARCHAR, minimum_fico INTEGER, allow_no_score_flag BOOLEAN,
            base_rate_pct DECIMAL(5,2), maximum_amount_usd DECIMAL(12,2), max_dti_pct DECIMAL(5,2),
            allow_bankruptcy_flag BOOLEAN, allow_collections_flag BOOLEAN,
            tier_rate_adjustment_rule VARCHAR, collections_rate_adjustment_pct DECIMAL(5,2),
            bankruptcy_rate_adjustment_pct DECIMAL(5,2), scra_rate_cap_pct DECIMAL(5,2)
        )
    """)
    product_cols = {
        "product_code": TEXT, "product_name": TEXT, "product_family": TEXT,
        "eligibility_criteria": TEXT, "minimum_risk_tier": TEXT, "minimum_fico": INT,
        "allow_no_score_flag": BOOL, "base_rate_pct": DEC, "maximum_amount_usd": MONEY,
        "max_dti_pct": DEC, "allow_bankruptcy_flag": BOOL, "allow_collections_flag": BOOL,
        "tier_rate_adjustment_rule": TEXT, "collections_rate_adjustment_pct": DEC,
        "bankruptcy_rate_adjustment_pct": DEC, "scra_rate_cap_pct": DEC}
    con.execute(f"INSERT INTO loan_products SELECT {select_list(product_cols)} FROM _stg_product")

    con.execute("""
        CREATE TABLE loan_applications (
            application_id VARCHAR PRIMARY KEY,
            applicant_id VARCHAR NOT NULL REFERENCES applicants(applicant_id),
            annual_income_usd DECIMAL(12,2), employment_duration_months INTEGER,
            fico_score INTEGER, region_state VARCHAR, requested_amount_usd DECIMAL(12,2),
            product_code VARCHAR NOT NULL REFERENCES loan_products(product_code),
            dti_pct DECIMAL(5,2), military_scra_flag BOOLEAN, bankruptcy_last_7y_flag BOOLEAN,
            collections_past_12_months_flag BOOLEAN, preliminary_decision VARCHAR,
            application_date DATE, final_decision VARCHAR, final_decision_date DATE,
            after_extract_date BOOLEAN
        )
    """)
    application_cols = {
        "application_id": TEXT, "applicant_id": TEXT, "annual_income_usd": MONEY,
        "employment_duration_months": INT, "fico_score": INT, "region_state": TEXT,
        "requested_amount_usd": MONEY, "product_code": TEXT, "dti_pct": DEC,
        "military_scra_flag": BOOL, "bankruptcy_last_7y_flag": BOOL,
        "collections_past_12_months_flag": BOOL, "preliminary_decision": TEXT}
    con.execute(f"""
        INSERT INTO loan_applications
        SELECT {select_list(application_cols)},
            {MDY.format(c='date')} AS application_date,
            {TEXT.format(c='final_decision')} AS final_decision,
            {MDY.format(c='final_decision_date')} AS final_decision_date,
            {MDY.format(c='date')} > DATE '{EXTRACT_DATE}' AS after_extract_date
        FROM _stg_application
    """)

    con.execute("""
        CREATE TABLE credit_pull_events (
            event_id VARCHAR PRIMARY KEY,
            application_id VARCHAR NOT NULL REFERENCES loan_applications(application_id),
            event_date DATE, fico_score INTEGER, bureau_source VARCHAR,
            event_status VARCHAR, event_reason VARCHAR
        )
    """)
    pull_cols = {"event_id": TEXT, "application_id": TEXT, "event_date": ISO, "fico_score": INT,
                 "bureau_source": TEXT, "event_status": TEXT, "event_reason": TEXT}
    con.execute(f"INSERT INTO credit_pull_events SELECT {select_list(pull_cols)} FROM _stg_pull")

    con.execute("""
        CREATE TABLE applicant_risk_features (
            application_id VARCHAR PRIMARY KEY REFERENCES loan_applications(application_id),
            appli_risk_id VARCHAR UNIQUE NOT NULL,
            as_of_date DATE, credit_history_status VARCHAR, credit_history_months_observed INTEGER,
            max_days_overdue INTEGER, delinquent_event_count INTEGER,
            total_outstanding_debt DECIMAL(12,2), total_overdue_amount DECIMAL(12,2),
            debt_burden_ratio DECIMAL(12,4), overdue_amount_to_income DECIMAL(12,4),
            delinquency_points INTEGER, debt_burden_points INTEGER, overdue_amount_points INTEGER,
            risk_tier_score INTEGER, risk_tier VARCHAR, risk_tier_basis VARCHAR,
            risk_tier_ruleset_version VARCHAR
        )
    """)
    risk_cols = {
        "application_id": TEXT, "appli_risk_id": TEXT, "as_of_date": ISO,
        "credit_history_status": TEXT, "credit_history_months_observed": INT,
        "max_days_overdue": INT, "delinquent_event_count": INT,
        "total_outstanding_debt": DEC, "total_overdue_amount": DEC,
        "debt_burden_ratio": DEC, "overdue_amount_to_income": DEC,
        "delinquency_points": INT, "debt_burden_points": INT, "overdue_amount_points": INT,
        "risk_tier_score": INT, "risk_tier": TEXT, "risk_tier_basis": TEXT,
        "risk_tier_ruleset_version": TEXT}
    con.execute(f"INSERT INTO applicant_risk_features SELECT {select_list(risk_cols)} FROM _stg_risk")


def report_quarantined(con: duckdb.DuckDBPyConnection) -> None:
    """Applications loaded but flagged because they are dated after the extract date."""
    n = con.execute("SELECT COUNT(*) FROM loan_applications WHERE after_extract_date").fetchone()[0]
    print(f"Applications dated after the {EXTRACT_DATE} extract date (flagged, not dropped): {n}")


def cleanup_staging(con: duckdb.DuckDBPyConnection) -> None:
    for table in ("_stg_applicant", "_stg_product", "_stg_application", "_stg_pull", "_stg_risk"):
        con.execute(f"DROP TABLE {table}")


def main() -> None:
    con = duckdb.connect(DB_PATH)
    load_staging_tables(con)
    build_tables(con)
    report_quarantined(con)
    cleanup_staging(con)

    print("\nFinal tables built:")
    for (table,) in con.execute("SHOW TABLES").fetchall():
        rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {rows} rows")
    con.close()


if __name__ == "__main__":
    main()
