"""
check_source_consistency.py

Checks that the four synthetic source CSVs and the document metadata agree
with each other and with the team's policies. Every check prints PASS or
FAIL with the number of offending rows; the script exits with status 1 if
any check fails.

This is written separately from src/synthetic/regenerate_source_data.py on
purpose, so a mistake in the generator is not repeated here.

Usage, from the repository root:
    python src/validation/check_source_consistency.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "structured" / "raw"
DOCS = ROOT / "data" / "documents" / "source"
DOC_METADATA = ROOT / "metadata" / "document _metadata .csv"

EXTRACT_DATE = pd.Timestamp("2026-09-14")
PENDING_WINDOW_DAYS = 14
LOOKBACK_DAYS = 24 * 30.4375
TIERS = ["T1", "T2", "T3", "T4", "T5"]

EXPECTED_COLUMNS = {
    "loan_product.csv": [
        "product_code", "product_name", "product_family", "eligibility_criteria",
        "minimum_risk_tier", "minimum_fico", "allow_no_score_flag", "base_rate_pct",
        "maximum_amount_usd", "max_dti_pct", "allow_bankruptcy_flag", "allow_collections_flag",
        "tier_rate_adjustment_rule", "collections_rate_adjustment_pct",
        "bankruptcy_rate_adjustment_pct", "scra_rate_cap_pct"],
    "loan_application.csv": [
        "application_id", "annual_income_usd", "employment_duration_months", "fico_score",
        "region_state", "requested_amount_usd", "product_code", "dti_pct", "military_scra_flag",
        "bankruptcy_last_7y_flag", "collections_past_12_months_flag", "preliminary_decision",
        "date", "final_decision", "final_decision_date"],
    "credit_pull_event.csv": [
        "event_id", "application_id", "event_date", "fico_score", "bureau_source",
        "event_status", "event_reason"],
    "applicant_risk_features.csv": [
        "appli_risk_id", "application_id", "as_of_date", "credit_history_status",
        "credit_history_months_observed", "max_days_overdue", "delinquent_event_count",
        "total_outstanding_debt", "total_overdue_amount", "debt_burden_ratio",
        "overdue_amount_to_income", "delinquency_points", "debt_burden_points",
        "overdue_amount_points", "risk_tier_score", "risk_tier", "risk_tier_basis",
        "risk_tier_ruleset_version"],
}
INTERNAL_POLICIES = {
    "enterprise_risk_policy.md", "applicant_risk_policy.md", "product_risk_policy.md",
    "product_eligibility_rules.md", "approval_escalation_procedures.md",
    "regional_state_lending_requirements.md"}

results: list[tuple[str, bool, str]] = []


def check(name: str, bad: int | bool, detail: str = "") -> None:
    ok = (bad == 0) if not isinstance(bad, bool) else not bad
    results.append((name, ok, detail if not ok else ""))


def money(series: pd.Series) -> pd.Series:
    return series.str.replace(r"[$, ]", "", regex=True).astype(float)


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name, dtype=str, keep_default_na=False)


def main() -> int:
    lp, la = read("loan_product.csv"), read("loan_application.csv")
    ev, rf = read("credit_pull_event.csv"), read("applicant_risk_features.csv")

    # ------------------------------------------------ structure and keys
    for name, df in [("loan_product.csv", lp), ("loan_application.csv", la),
                     ("credit_pull_event.csv", ev), ("applicant_risk_features.csv", rf)]:
        check(f"{name}: columns match the contract", list(df.columns) != EXPECTED_COLUMNS[name],
              f"got {list(df.columns)}")
    check("product_code unique", lp["product_code"].duplicated().sum())
    check("application_id unique", la["application_id"].duplicated().sum())
    check("event_id unique", ev["event_id"].duplicated().sum())
    check("one risk row per application",
          len(rf) != len(la) or set(rf["application_id"]) != set(la["application_id"]))
    check("every product_code resolves", (~la["product_code"].isin(lp["product_code"])).sum())
    check("every pull resolves to an application", (~ev["application_id"].isin(la["application_id"])).sum())

    la["_date"] = pd.to_datetime(la["date"], format="%m/%d/%Y")
    la["_income"] = money(la["annual_income_usd"])
    la["_amount"] = money(la["requested_amount_usd"])
    ev["_date"] = pd.to_datetime(ev["event_date"])
    ev["_app_date"] = ev["application_id"].map(dict(zip(la["application_id"], la["_date"])))
    risk = rf.set_index("application_id")
    no_history = set(rf.loc[rf["credit_history_status"] == "NO_HISTORY", "application_id"])

    # ------------------------------------------------ products
    check("minimum_risk_tier is T1 to T5", (~lp["minimum_risk_tier"].isin(TIERS)).sum())
    check("allow_no_score_flag is TRUE or FALSE", (~lp["allow_no_score_flag"].isin(["TRUE", "FALSE"])).sum())

    # ------------------------------------------------ credit pulls
    no_result = ev["event_status"].isin(["Error", "Pending"])
    check("Error and Pending pulls carry no score, all others do",
          ((ev["fico_score"] == "") != no_result).sum())
    scores = pd.to_numeric(ev["fico_score"], errors="coerce")
    check("pull scores are 300 to 850", ((scores < 300) | (scores > 850)).sum())
    check("Pending pulls are recent",
          (no_result & (ev["event_status"] == "Pending")
           & (ev["_date"] < EXTRACT_DATE - pd.Timedelta(days=PENDING_WINDOW_DAYS))).sum())
    check("pulls fall on or before their application date", (ev["_date"] > ev["_app_date"]).sum())
    check("pulls fall inside the 24 month lookback",
          ((ev["_app_date"] - ev["_date"]).dt.days > LOOKBACK_DAYS).sum())
    check("NO_HISTORY applicants have no pulls", ev["application_id"].isin(no_history).sum())

    scored = ev[ev["fico_score"] != ""].sort_values(["application_id", "_date", "event_id"])
    latest = scored.groupby("application_id")["fico_score"].last()
    expected_fico = la["application_id"].map(latest).fillna("")
    check("fico_score is the latest returned pull on or before the application date",
          (expected_fico != la["fico_score"]).sum())
    has_history = ~la["application_id"].isin(no_history)
    check("every applicant with history has a score", (has_history & (la["fico_score"] == "")).sum())
    check("NO_HISTORY applicants have no score", (~has_history & (la["fico_score"] != "")).sum())

    # ------------------------------------------------ application plausibility
    ratio = la["_amount"] / la["_income"]
    family = la["product_code"].str[:3]
    limits = family.map({"MTG": 5.0, "CRD": 0.5, "AUT": 1.5})
    check("requested amount is plausible against income", (ratio > limits).sum())
    check("jumbo requests are above the conforming limit",
          ((la["product_code"] == "MTG-JB") & (la["_amount"] <= 766_550)).sum())
    fico_num = pd.to_numeric(la["fico_score"], errors="coerce")
    min_fico = la["product_code"].map(dict(zip(lp["product_code"], lp["minimum_fico"].astype(int))))
    reach = (fico_num < min_fico).sum()
    check("most applicants apply for a product their score reaches (outliers under 15%)",
          reach > 0.15 * fico_num.notna().sum(), f"{reach} below their product's minimum FICO")
    medians = pd.DataFrame({"family": family, "minimum": min_fico, "fico": fico_num}).groupby(
        ["family", "minimum"])["fico"].median()
    check("within each family, median FICO rises with the product's FICO minimum",
          sum(not medians[f].is_monotonic_increasing for f in medians.index.get_level_values(0).unique()))
    check("money keeps its documented text format",
          (~la["annual_income_usd"].str.fullmatch(r"\$\d{1,3}(,\d{3})* ")).sum()
          + (~la["requested_amount_usd"].str.fullmatch(r"\$\d{1,3}(,\d{3})* ")).sum())

    # ------------------------------------------------ risk features
    rf_dates = rf["application_id"].map(dict(zip(la["application_id"], la["_date"])))
    check("as_of_date equals the application date", (pd.to_datetime(rf["as_of_date"]) != rf_dates).sum())
    months = rf["credit_history_months_observed"].astype(int)
    status = months.map(lambda m: "NO_HISTORY" if m == 0 else "LIMITED_HISTORY" if m <= 5 else "ESTABLISHED")
    check("credit_history_status follows months observed", (status != rf["credit_history_status"]).sum())
    basis = rf["credit_history_status"].map({"NO_HISTORY": "NO_CREDIT_HISTORY",
                                             "LIMITED_HISTORY": "LIMITED_HISTORY",
                                             "ESTABLISHED": "CREDIT_HISTORY"})
    check("risk_tier_basis follows credit_history_status", (basis != rf["risk_tier_basis"]).sum())
    oldest = (scored["_app_date"] - scored["_date"]).dt.days.groupby(scored["application_id"]).max()
    oldest_months = rf["application_id"].map(oldest).map(
        lambda d: 0 if pd.isna(d) else min(24, math.ceil(d / 30.4375)))
    check("months observed covers the oldest returned pull", (months < oldest_months).sum())

    hist = rf[rf["credit_history_status"] != "NO_HISTORY"].copy()
    nohist = rf[rf["credit_history_status"] == "NO_HISTORY"]
    empty_cols = ["max_days_overdue", "total_outstanding_debt", "total_overdue_amount",
                  "debt_burden_ratio", "overdue_amount_to_income", "delinquency_points",
                  "debt_burden_points", "overdue_amount_points", "risk_tier_score"]
    check("NO_HISTORY rows carry no measures, points or score", (nohist[empty_cols] != "").sum().sum())
    check("NO_HISTORY rows are T3", (nohist["risk_tier"] != "T3").sum())

    inc = hist["application_id"].map(dict(zip(la["application_id"], la["_income"])))
    num = {c: hist[c].astype(float) for c in empty_cols + ["delinquent_event_count"]}
    check("debt_burden_ratio = total_outstanding_debt / annual income",
          ((num["debt_burden_ratio"] - num["total_outstanding_debt"] / inc).abs() > 0.00005).sum())
    check("overdue_amount_to_income = total_overdue_amount / annual income",
          ((num["overdue_amount_to_income"] - num["total_overdue_amount"] / inc).abs() > 0.00005).sum())
    days = num["max_days_overdue"]
    p1 = pd.cut(days, [-1, 0, 29, 59, 89, 119, float("inf")], labels=[0, 1, 2, 3, 4, 5]).astype(int)
    p2 = pd.cut(num["debt_burden_ratio"], [-1, 0.25, 0.50, 0.75, float("inf")], labels=[0, 1, 2, 3]).astype(int)
    p3 = pd.cut(num["overdue_amount_to_income"], [-1, 0, 0.02, 0.05, float("inf")], labels=[0, 1, 2, 3]).astype(int)
    check("delinquency_points follow the policy table", (p1 != num["delinquency_points"]).sum())
    check("debt_burden_points follow the policy table", (p2 != num["debt_burden_points"]).sum())
    check("overdue_amount_points follow the policy table", (p3 != num["overdue_amount_points"]).sum())
    check("risk_tier_score is the sum of the three points", ((p1 + p2 + p3) != num["risk_tier_score"]).sum())
    tier = pd.cut(num["risk_tier_score"], [-1, 1, 3, 5, 7, 11], labels=TIERS).astype(str)
    check("risk_tier follows the score table", (tier != hist["risk_tier"]).sum())
    check("delinquent events agree with days overdue",
          ((num["delinquent_event_count"] > 0) != (days > 0)).sum())
    check("overdue amount agrees with days overdue", ((num["total_overdue_amount"] > 0) != (days > 0)).sum())
    check("overdue amount does not exceed outstanding debt",
          (num["total_overdue_amount"] > num["total_outstanding_debt"]).sum())

    # ------------------------------------------------ decisions
    prod = lp.set_index("product_code")
    expected = []
    for _, a in la.iterrows():
        p, r = prod.loc[a["product_code"]], risk.loc[a["application_id"]]
        fails = (a["_amount"] > float(p["maximum_amount_usd"].replace(",", ""))
                 or float(a["dti_pct"]) > float(p["max_dti_pct"])
                 or (a["bankruptcy_last_7y_flag"] == "TRUE" and p["allow_bankruptcy_flag"] == "FALSE")
                 or (a["collections_past_12_months_flag"] == "TRUE" and p["allow_collections_flag"] == "FALSE")
                 or TIERS.index(r["risk_tier"]) > TIERS.index(p["minimum_risk_tier"])
                 or (a["fico_score"] == "" and p["allow_no_score_flag"] == "FALSE")
                 or (a["fico_score"] != "" and int(a["fico_score"]) < int(p["minimum_fico"])))
        if fails:
            expected.append("Declined")
        elif r["credit_history_status"] != "ESTABLISHED" or r["risk_tier"] in ("T4", "T5"):
            expected.append("Review")
        else:
            expected.append("Approved")
    check("preliminary_decision follows the product rules and tier overlay",
          (pd.Series(expected, index=la.index) != la["preliminary_decision"]).sum())

    final, final_date = la["final_decision"], la["final_decision_date"]
    check("final_decision values are allowed",
          (~final.isin(["", "Approved", "Declined", "Withdrawn"])).sum())
    check("final_decision and its date are filled together", ((final == "") != (final_date == "")).sum())
    decided = pd.to_datetime(final_date.where(final_date != ""), format="%m/%d/%Y")
    check("final decision is on or after the application date", (decided < la["_date"]).sum())
    check("final decision is on or before the extract date", (decided > EXTRACT_DATE).sum())
    check("applications after the extract date have no final decision",
          ((la["_date"] > EXTRACT_DATE) & (final != "")).sum())
    check("a preliminary decline is never approved later",
          ((la["preliminary_decision"] == "Declined") & (final == "Approved")).sum())
    check("a preliminary approval is never declined later",
          ((la["preliminary_decision"] == "Approved") & (final == "Declined")).sum())

    # ------------------------------------------------ documents
    meta = pd.read_csv(DOC_METADATA, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    corpus = {p.name for p in DOCS.iterdir() if p.name != ".gitkeep"}
    check("every corpus document has a metadata row", len(corpus - set(meta["file_name"])),
          str(sorted(corpus - set(meta["file_name"]))))
    check("every metadata row points at a real file", len(set(meta["file_name"]) - corpus),
          str(sorted(set(meta["file_name"]) - corpus)))
    check("doc_id is unique", meta["doc_id"].duplicated().sum())
    internal = meta[meta["file_name"].isin(INTERNAL_POLICIES)]
    effective = pd.to_datetime(internal["effective_date"], errors="coerce")
    check("internal policies are Effective", (internal["authority_status"] != "Effective").sum())
    check("internal policies were in force before the first application",
          (effective.isna() | (effective > la["_date"].min())).sum())
    every = pd.to_datetime(meta["effective_date"], errors="coerce")
    check("every document has an ISO effective date", every.isna().sum())

    # The Catalog Gates table in the eligibility rules must restate loan_product.csv exactly.
    text = (DOCS / "product_eligibility_rules.md").read_text(encoding="utf-8")
    gates = {}
    for line in text.split("## Catalog Gates", 1)[1].splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 8 and cells[0] in set(lp["product_code"]):
            gates[cells[0]] = cells
    yes_no = {"TRUE": "Yes", "FALSE": "No"}
    mismatched = 0
    for _, p in lp.iterrows():
        expected_row = [p["product_code"], p["minimum_risk_tier"], p["minimum_fico"],
                        yes_no[p["allow_no_score_flag"]], f"{p['max_dti_pct']}%",
                        f"${p['maximum_amount_usd']}", yes_no[p["allow_bankruptcy_flag"]],
                        yes_no[p["allow_collections_flag"]]]
        mismatched += gates.get(p["product_code"]) != expected_row
    check("eligibility rules Catalog Gates table matches loan_product.csv", mismatched)

    # ------------------------------------------------ report
    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
