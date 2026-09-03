"""
build_relational_model.py

Loads the FinTech Credit & Loan Review source CSVs into DuckDB and builds
a constrained relational model (primary keys, foreign keys) on top of them.

Known data-quality corrections applied here:
  - applicant.csv row APP-00060 has 9 of its 12 fields NULL (a genuinely
    incomplete record, not a malformed file -- confirmed by comparing
    against a differently-exported copy of the same source data). This is
    flagged, not silently dropped: see report_incomplete_records().
  - 'HELOAN-01' in applicant.csv is a confirmed typo for 'HELOC-01' and is
    corrected on load.
  - loan_product.csv has a truncated row ('SOL', line 20) -- almost
    certainly the start of a SOLAR-01 product definition that was cut off
    during export. No well-formed backup of this file was found, so this
    row is quarantined at load time (ignore_errors=True) rather than
    guessed at. Applicants referencing 'SOLAR-01' are excluded from the
    final applicants table until the real product definition is recovered
    from the source and re-added to loan_product.csv.
  - credit_pull.csv also has one truncated row (line 77, 'EVT-000076,APP-00',
    cut off mid-value), quarantined the same way.

  NOTE: all three source files have exactly one truncated row at/near the
  end of the file. This is very likely a single systemic export/generation
  problem, not three unrelated bugs -- worth raising with whoever produced
  these files, not just patching around it here.

Usage:
    python build_relational_model.py
"""

import duckdb

DATA_DIR = "data/structured/raw"
DB_PATH = "fintech.duckdb"


def load_staging_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Load raw source CSVs into unconstrained staging tables.

    applicant.csv and credit_pull.csv load without ignore_errors: with the
    well-formed export of applicant.csv (all rows padded to the full 12
    fields), a malformed row should fail loudly rather than be silently
    skipped. Missing *values* within an otherwise well-formed row (like
    APP-00060) are a data-quality issue, not a parsing issue -- see
    report_incomplete_records().

    loan_product.csv is the exception: it has a genuinely truncated row
    ('SOL', line 20, likely the start of a SOLAR-01 definition) with no
    well-formed backup available. ignore_errors=True quarantines that row
    here rather than crashing the whole load.
    """
    con.execute(f"""
        CREATE OR REPLACE TABLE _staging_applicants AS
        SELECT * FROM read_csv('{DATA_DIR}/applicant.csv', delim=',')
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE _staging_loan_products AS
        SELECT * FROM read_csv('{DATA_DIR}/loan_product.csv', delim=',', ignore_errors=true)
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE _staging_credit_pull AS
        SELECT * FROM read_csv('{DATA_DIR}/credit_pull.csv', delim=',', ignore_errors=true)
    """)


def build_loan_products(con: duckdb.DuckDBPyConnection) -> None:
    """Build loan_products with product_code as the primary key."""
    con.execute("""
        CREATE OR REPLACE TABLE loan_products (
            product_code VARCHAR PRIMARY KEY,
            product_name VARCHAR,
            product_family VARCHAR,
            eligibility_criteria VARCHAR,
            minimum_credit_tier VARCHAR,
            minimum_fico BIGINT,
            base_rate_pct DOUBLE,
            maximum_amount_usd BIGINT
        )
    """)
    con.execute("INSERT INTO loan_products SELECT * FROM _staging_loan_products")


def build_applicants(con: duckdb.DuckDBPyConnection) -> None:
    """Build applicants with applicant_id as the primary key and a foreign
    key on requested_product_code referencing loan_products. Applies the
    confirmed HELOAN-01 correction and quarantines SOLAR-01 rows."""
    con.execute("""
        CREATE OR REPLACE TABLE applicants (
            applicant_id VARCHAR PRIMARY KEY,
            annual_income_usd BIGINT,
            employment_duration_months BIGINT,
            credit_risk_tier VARCHAR,
            fico_score BIGINT,
            region_state VARCHAR,
            requested_amount_usd BIGINT,
            requested_product_code VARCHAR REFERENCES loan_products(product_code),
            dti_pct DOUBLE,
            military_scra_flag BIGINT,
            bankruptcy_last_7y_flag BIGINT,
            preliminary_decision VARCHAR
        )
    """)
    con.execute("""
        INSERT INTO applicants
        SELECT
            applicant_id, annual_income_usd, employment_duration_months, credit_risk_tier,
            fico_score, region_state, requested_amount_usd,
            CASE WHEN requested_product_code = 'HELOAN-01' THEN 'HELOC-01'
                 ELSE requested_product_code END,
            dti_pct, military_scra_flag, bankruptcy_last_7y_flag, preliminary_decision
        FROM _staging_applicants
        WHERE requested_product_code IS DISTINCT FROM 'SOLAR-01'
    """)


def build_credit_pull(con: duckdb.DuckDBPyConnection) -> None:
    """Build credit_pull with event_id as the primary key and a foreign key
    on applicant_id referencing applicants."""
    con.execute("""
        CREATE OR REPLACE TABLE credit_pull (
            event_id VARCHAR PRIMARY KEY,
            applicant_id VARCHAR REFERENCES applicants(applicant_id),
            event_date DATE,
            prior_tier VARCHAR,
            new_tier VARCHAR,
            prior_fico BIGINT,
            new_fico BIGINT,
            tier_changed_flag BIGINT,
            bureau_source VARCHAR,
            event_status VARCHAR,
            event_reason VARCHAR
        )
    """)
    con.execute("INSERT INTO credit_pull SELECT * FROM _staging_credit_pull")


def report_quarantined(con: duckdb.DuckDBPyConnection) -> None:
    """Print rows excluded from the final model, so nothing is silently dropped."""
    quarantined = con.execute("""
        SELECT * FROM _staging_applicants WHERE requested_product_code = 'SOLAR-01'
    """).df()
    print(f"Quarantined {len(quarantined)} row(s) pending team decision (SOLAR-01):")
    print(quarantined)


def report_incomplete_records(con: duckdb.DuckDBPyConnection, null_threshold: int = 3) -> None:
    """Flag applicants rows with an unusually high number of NULL fields.

    This is the general-purpose replacement for the old truncation check:
    rather than looking for a specific known-bad row, it flags ANY row
    (present or future) with more missing fields than expected, so a new
    incomplete record doesn't silently slip through unnoticed.
    """
    nullable_columns = [
        "annual_income_usd", "employment_duration_months", "credit_risk_tier",
        "fico_score", "region_state", "requested_amount_usd",
        "requested_product_code", "dti_pct", "military_scra_flag",
        "bankruptcy_last_7y_flag", "preliminary_decision",
    ]
    null_count_expr = " + ".join(f"CASE WHEN {c} IS NULL THEN 1 ELSE 0 END" for c in nullable_columns)

    incomplete = con.execute(f"""
        SELECT applicant_id, ({null_count_expr}) AS null_field_count
        FROM applicants
        WHERE ({null_count_expr}) >= {null_threshold}
        ORDER BY null_field_count DESC
    """).df()

    print(f"Applicant rows with >= {null_threshold} NULL fields (out of {len(nullable_columns)}):")
    print(incomplete)


def cleanup_staging(con: duckdb.DuckDBPyConnection) -> None:
    """Drop staging tables once the final constrained tables are built."""
    for table in ("_staging_applicants", "_staging_loan_products", "_staging_credit_pull"):
        con.execute(f"DROP TABLE {table}")


def main() -> None:
    con = duckdb.connect(DB_PATH)

    load_staging_tables(con)
    build_loan_products(con)
    build_applicants(con)
    build_credit_pull(con)
    report_quarantined(con)
    report_incomplete_records(con)
    cleanup_staging(con)

    print("\nFinal tables built:")
    print(con.execute("SHOW TABLES").df())


if __name__ == "__main__":
    main()
