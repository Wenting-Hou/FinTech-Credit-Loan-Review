"""
regenerate_source_data.py

Rebuilds every derived field in the four synthetic source CSVs so the files
agree with each other and with the team's policies. The generator-owned
fields (incomes, debts, days overdue, flags, dates, bureaus, reasons) are
kept as they are, except for the plausibility corrections listed below.

What this script changes:

  loan_product.csv
    - minimum_credit_tier is renamed minimum_risk_tier. It is tested against
      applicant_risk_features.risk_tier (policy RISK-TIER), not a FICO band.
    - allow_no_score_flag is added. TRUE only for MTG-FH, CRD-SC and AUT-SP,
      the products that accept an applicant with no credit score through
      manual underwriting (product_eligibility_rules.md section 4).

  credit_pull_event.csv
    - prior_tier, prior_fico, tier_changed_flag and new_tier are dropped and
      new_fico is renamed fico_score. One observation per pull.
    - Pulls belonging to NO_HISTORY applicants are removed.
    - A Pending pull older than PENDING_WINDOW_DAYS before the extract date
      is marked Completed. Error and Pending pulls carry no score.
    - Every scored applicant keeps at least one returned pull on or before
      the application date.

  loan_application.csv
    - Applicants mostly apply for a product their credit score can reach.
      Most applicants below their product's minimum FICO (or with no score on
      a product that needs one) are moved to the best product in the same
      family that they fit; REACH_KEEP_RATE of them stay where they are as
      realistic outliers, and they are declined. Most applicants with a strong
      score on the family's entry product move up one or two products.
    - Requested amounts are redrawn where they are implausible against
      income (mortgage above 5x, card above 0.5x, auto above 1.5x income).
      A jumbo applicant whose income cannot support any jumbo loan gets a
      new income instead.
    - fico_score is the score of the latest returned pull on or before the
      application date. NO_HISTORY applicants have no score.
    - credit_risk_tier is dropped. It was a FICO band with the same T1 to T5
      labels as risk_tier.
    - preliminary_decision is derived from the product rules and the
      applicant-tier overlay (product_risk_policy.md sections 3 and 4).
    - final_decision and final_decision_date are added.

  applicant_risk_features.csv
    - debt_to_income_ratio is renamed debt_burden_ratio and
      overdue_amount_points is added (applicant_risk_policy.md).
    - credit_history_months_observed covers the oldest returned pull in the
      24 month lookback, and the status and basis follow from it.
    - Ratios, points, score and tier are recomputed from the policy tables.
      NO_HISTORY rows carry no points and no score.

Deliberate, documented quality problems are NOT touched: money stored as
text, M/D/YYYY dates and TRUE/FALSE booleans in loan_application.csv, ISO
dates and True/False booleans in credit_pull_event.csv, and applications
dated after the extract date (quarantined at ingestion).

Random choices use a hash of a fixed seed and the record id, so running the
script twice produces identical files.

Usage, from the repository root:
    python src/synthetic/regenerate_source_data.py

Then check the result:
    python src/validation/check_source_consistency.py
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "structured" / "raw"

SEED = "team03-fintech-v1"
EXTRACT_DATE = pd.Timestamp("2026-09-14")   # the date the files represent
PENDING_WINDOW_DAYS = 14                    # a pull can stay Pending this long
LOOKBACK_MONTHS = 24                        # applicant_risk_policy.md
DAYS_PER_MONTH = 30.4375

TIER_RANK = {"T1": 1, "T2": 2, "T3": 3, "T4": 4, "T5": 5}
NO_SCORE_PRODUCTS = {"MTG-FH", "CRD-SC", "AUT-SP"}
RETURNED_STATUSES = {"Completed", "Resubmitted"}
NO_RESULT_STATUSES = {"Error", "Pending"}

# Requested amount over annual income: (redraw above, redraw low, redraw high)
AMOUNT_TO_INCOME = {"MTG": (5.0, 2.5, 5.0), "CRD": (0.5, 0.05, 0.35), "AUT": (1.5, 0.2, 0.9)}
FAMILY_FLOOR = {"MTG": 75_000, "CRD": 300, "AUT": 5_000}
JUMBO_FLOOR = 766_551            # one dollar above the 2024 conforming loan limit
JUMBO_REDRAW_CEILING = 1_200_000

REACH_KEEP_RATE = 0.20   # share of under-qualified applicants who apply anyway
MOVE_UP_RATE = 0.60      # share of strong applicants who leave the entry product
MOVE_UP_MARGIN = 40      # FICO points above a product's minimum before moving up to it


# ---------------------------------------------------------------- helpers

def draw(key: str, salt: str) -> float:
    """Deterministic number in [0, 1) from the seed, a salt and a record id."""
    digest = hashlib.sha256(f"{SEED}|{salt}|{key}".encode()).hexdigest()
    return int(digest[:13], 16) / 16 ** 13


def parse_money(text: str) -> float:
    return float(text.replace("$", "").replace(",", "").strip())


def format_money(value: float) -> str:
    """Keep the source format on purpose: dollar sign, commas, trailing space."""
    return f"${value:,.0f} "


def parse_app_date(text: str) -> pd.Timestamp:
    return pd.to_datetime(text, format="%m/%d/%Y")


def format_app_date(value: pd.Timestamp) -> str:
    return f"{value.month}/{value.day}/{value.year}"


def as_int_text(value) -> str:
    if value is None or value == "" or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(int(round(float(value))))


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name, dtype=str, keep_default_na=False)


def write(df: pd.DataFrame, name: str) -> None:
    df.to_csv(RAW / name, index=False, lineterminator="\n")


# ---------------------------------------------------------------- policy tables

def delinquency_points(max_days_overdue: float) -> int:
    d = max_days_overdue
    if d <= 0:
        return 0
    if d < 30:
        return 1
    if d < 60:
        return 2
    if d < 90:
        return 3
    if d < 120:
        return 4
    return 5


def debt_burden_points(ratio: float) -> int:
    if ratio <= 0.25:
        return 0
    if ratio <= 0.50:
        return 1
    if ratio <= 0.75:
        return 2
    return 3


def overdue_amount_points(ratio: float) -> int:
    if ratio <= 0:
        return 0
    if ratio <= 0.02:
        return 1
    if ratio <= 0.05:
        return 2
    return 3


def tier_from_score(score: int) -> str:
    if score <= 1:
        return "T1"
    if score <= 3:
        return "T2"
    if score <= 5:
        return "T3"
    if score <= 7:
        return "T4"
    return "T5"


def history_status(months: int) -> str:
    if months == 0:
        return "NO_HISTORY"
    if months <= 5:
        return "LIMITED_HISTORY"
    return "ESTABLISHED"


HISTORY_BASIS = {
    "NO_HISTORY": "NO_CREDIT_HISTORY",
    "LIMITED_HISTORY": "LIMITED_HISTORY",
    "ESTABLISHED": "CREDIT_HISTORY",
}


# ---------------------------------------------------------------- steps

def fix_products(lp: pd.DataFrame) -> pd.DataFrame:
    lp = lp.rename(columns={"minimum_credit_tier": "minimum_risk_tier"})
    if "allow_no_score_flag" not in lp.columns:
        position = lp.columns.get_loc("minimum_fico") + 1
        lp.insert(position, "allow_no_score_flag",
                  ["TRUE" if code in NO_SCORE_PRODUCTS else "FALSE" for code in lp["product_code"]])
    return lp


def fix_amounts(la: pd.DataFrame, lp: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
    product_max = dict(zip(lp["product_code"], lp["maximum_amount_usd"].map(parse_money)))
    redrawn = new_income = 0
    for i, row in la.iterrows():
        family = row["product_code"][:3]
        limit, low, high = AMOUNT_TO_INCOME[family]
        income = parse_money(row["annual_income_usd"])
        amount = parse_money(row["requested_amount_usd"])
        if amount / income <= limit:
            continue
        key = row["application_id"]
        if row["product_code"] == "MTG-JB" and income * high < JUMBO_FLOOR:
            amount = round(JUMBO_FLOOR + draw(key, "jumbo-amount") * (JUMBO_REDRAW_CEILING - JUMBO_FLOOR))
            income = round(amount / (3.5 + 1.5 * draw(key, "jumbo-income")))
            la.at[i, "annual_income_usd"] = format_money(income)
            new_income += 1
        else:
            amount = round(income * (low + (high - low) * draw(key, "amount")))
            floor = JUMBO_FLOOR if row["product_code"] == "MTG-JB" else FAMILY_FLOOR[family]
            amount = max(min(amount, product_max[row["product_code"]]), floor)
        la.at[i, "requested_amount_usd"] = format_money(amount)
        redrawn += 1
    return la, redrawn, new_income


def realign_products(la: pd.DataFrame, lp: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
    """Make product choice follow the applicant's credit score, with outliers."""
    minimum = dict(zip(lp["product_code"], lp["minimum_fico"].astype(int)))
    no_score_ok = dict(zip(lp["product_code"], lp["allow_no_score_flag"] == "TRUE"))
    product_max = dict(zip(lp["product_code"], lp["maximum_amount_usd"].map(parse_money)))
    family = {}
    for code in lp["product_code"]:
        family.setdefault(code[:3], []).append(code)
    for codes in family.values():
        codes.sort(key=lambda c: minimum[c])

    moved_down = moved_up = 0
    for i, row in la.iterrows():
        code, key = row["product_code"], row["application_id"]
        options = family[code[:3]]
        target = None
        if row["fico_score"] == "":
            if not no_score_ok[code] and draw(key, "reach") >= REACH_KEEP_RATE:
                target = next(c for c in options if no_score_ok[c])
        else:
            fico = int(row["fico_score"])
            if fico < minimum[code]:
                fitting = [c for c in options if minimum[c] <= fico]
                if fitting and draw(key, "reach") >= REACH_KEEP_RATE:
                    target = fitting[-1]
            elif code == options[0]:
                # Jumbo is chosen by loan size, not by score, so nobody moves up into it.
                higher = [c for c in options[1:] if minimum[c] + MOVE_UP_MARGIN <= fico and c != "MTG-JB"]
                if higher and draw(key, "up") < MOVE_UP_RATE:
                    target = higher[-1]
        if target is None or target == code:
            continue
        if minimum[target] < minimum[code] or (no_score_ok[target] and row["fico_score"] == ""):
            moved_down += 1
        else:
            moved_up += 1
        la.at[i, "product_code"] = target
        amount = parse_money(row["requested_amount_usd"])
        if amount > product_max[target]:
            amount = round(product_max[target] * (0.5 + 0.45 * draw(key, "refit")))
            la.at[i, "requested_amount_usd"] = format_money(amount)
    return la, moved_down, moved_up


def fix_pulls(ev: pd.DataFrame, app_date: dict, no_history: set) -> pd.DataFrame:
    if "new_fico" in ev.columns:
        ev = ev.drop(columns=["prior_tier", "prior_fico", "tier_changed_flag", "new_tier"])
        ev = ev.rename(columns={"new_fico": "fico_score"})
    ev = ev[~ev["application_id"].isin(no_history)].copy()

    event_date = pd.to_datetime(ev["event_date"])
    stale_pending = (ev["event_status"] == "Pending") & (
        event_date < EXTRACT_DATE - pd.Timedelta(days=PENDING_WINDOW_DAYS))
    ev.loc[stale_pending, "event_status"] = "Completed"

    on_or_before = event_date <= ev["application_id"].map(app_date)
    returned = ev["event_status"].isin(RETURNED_STATUSES) & (ev["fico_score"] != "")
    covered = set(ev.loc[on_or_before & returned, "application_id"])
    for app in sorted(set(ev.loc[on_or_before, "application_id"]) - covered):
        candidates = ev[(ev["application_id"] == app) & on_or_before & (ev["fico_score"] != "")]
        latest = candidates.assign(_d=event_date).sort_values(["_d", "event_id"]).index[-1]
        ev.loc[latest, "event_status"] = "Completed"

    ev.loc[ev["event_status"].isin(NO_RESULT_STATUSES), "fico_score"] = ""
    return ev


def latest_scores(ev: pd.DataFrame, app_date: dict) -> pd.DataFrame:
    scored = ev[ev["fico_score"] != ""].copy()
    scored["_d"] = pd.to_datetime(scored["event_date"])
    scored["_app"] = scored["application_id"].map(app_date)
    scored = scored[scored["_d"] <= scored["_app"]]
    scored["_age_months"] = (scored["_app"] - scored["_d"]).dt.days / DAYS_PER_MONTH
    scored = scored[scored["_age_months"] <= LOOKBACK_MONTHS]
    return scored.sort_values(["application_id", "_d", "event_id"])


def derive_fico(la: pd.DataFrame, scored: pd.DataFrame) -> pd.DataFrame:
    latest = scored.groupby("application_id")["fico_score"].last()
    la["fico_score"] = la["application_id"].map(latest).fillna("")
    return la.drop(columns=["credit_risk_tier"], errors="ignore")


def derive_risk_features(rf: pd.DataFrame, la: pd.DataFrame, scored: pd.DataFrame) -> pd.DataFrame:
    rf = rf.rename(columns={"debt_to_income_ratio": "debt_burden_ratio"})
    if "overdue_amount_points" not in rf.columns:
        rf.insert(rf.columns.get_loc("debt_burden_points") + 1, "overdue_amount_points", "")
    income = dict(zip(la["application_id"], la["annual_income_usd"].map(parse_money)))
    oldest_pull = scored.groupby("application_id")["_age_months"].max().map(math.ceil)

    for i, row in rf.iterrows():
        app = row["application_id"]
        months = int(row["credit_history_months_observed"])
        if app in oldest_pull.index:
            months = max(months, min(LOOKBACK_MONTHS, int(oldest_pull[app])))
        status = history_status(months)
        rf.at[i, "credit_history_months_observed"] = str(months)
        rf.at[i, "credit_history_status"] = status
        rf.at[i, "risk_tier_basis"] = HISTORY_BASIS[status]

        if status == "NO_HISTORY":
            for col in ("max_days_overdue", "total_outstanding_debt", "total_overdue_amount",
                        "debt_burden_ratio", "overdue_amount_to_income", "delinquency_points",
                        "debt_burden_points", "overdue_amount_points", "risk_tier_score"):
                rf.at[i, col] = ""
            rf.at[i, "delinquent_event_count"] = "0"
            rf.at[i, "risk_tier"] = "T3"
            continue

        inc = income[app]
        debt = float(row["total_outstanding_debt"])
        overdue = float(row["total_overdue_amount"])
        burden = float(row["debt_burden_ratio"]) if row["debt_burden_ratio"] != "" else None
        overdue_ratio = float(row["overdue_amount_to_income"]) if row["overdue_amount_to_income"] != "" else None
        # Only recompute a stored ratio when it no longer matches the income.
        if burden is None or abs(burden - debt / inc) > 0.00005:
            burden = round(debt / inc, 4)
        if overdue_ratio is None or abs(overdue_ratio - overdue / inc) > 0.00005:
            overdue_ratio = round(overdue / inc, 4)
        rf.at[i, "debt_burden_ratio"] = str(burden)
        rf.at[i, "overdue_amount_to_income"] = str(overdue_ratio)

        days = float(row["max_days_overdue"])
        p1, p2, p3 = delinquency_points(days), debt_burden_points(burden), overdue_amount_points(overdue_ratio)
        score = p1 + p2 + p3
        rf.at[i, "max_days_overdue"] = as_int_text(days)
        rf.at[i, "delinquency_points"] = str(p1)
        rf.at[i, "debt_burden_points"] = str(p2)
        rf.at[i, "overdue_amount_points"] = str(p3)
        rf.at[i, "risk_tier_score"] = str(score)
        rf.at[i, "risk_tier"] = tier_from_score(score)
    return rf


def eligibility_failures(app: pd.Series, product: pd.Series, risk: pd.Series) -> list[str]:
    """Hard product rules. A favorable tier never overrides one of these."""
    fails = []
    if parse_money(app["requested_amount_usd"]) > parse_money(product["maximum_amount_usd"]):
        fails.append("amount")
    if float(app["dti_pct"]) > float(product["max_dti_pct"]):
        fails.append("dti")
    if app["bankruptcy_last_7y_flag"] == "TRUE" and product["allow_bankruptcy_flag"] == "FALSE":
        fails.append("bankruptcy")
    if app["collections_past_12_months_flag"] == "TRUE" and product["allow_collections_flag"] == "FALSE":
        fails.append("collections")
    if TIER_RANK[risk["risk_tier"]] > TIER_RANK[product["minimum_risk_tier"]]:
        fails.append("risk_tier")
    if app["fico_score"] == "":
        if product["allow_no_score_flag"] == "FALSE":
            fails.append("no_score")
    elif int(app["fico_score"]) < int(product["minimum_fico"]):
        fails.append("fico")
    return fails


def needs_manual_review(risk: pd.Series) -> bool:
    """Applicant-tier overlay, product_risk_policy.md section 3."""
    return (risk["credit_history_status"] in ("NO_HISTORY", "LIMITED_HISTORY")
            or risk["risk_tier"] in ("T4", "T5"))


def review_approval_rate(app: pd.Series, risk: pd.Series) -> float:
    rate = 0.75
    if risk["credit_history_status"] == "LIMITED_HISTORY":
        rate = min(rate, 0.70)
    if risk["credit_history_status"] == "NO_HISTORY":
        rate = min(rate, 0.50)
    if risk["risk_tier"] == "T4":
        rate = min(rate, 0.55)
    if risk["risk_tier"] == "T5":
        rate = min(rate, 0.30)
    if "TRUE" in (app["bankruptcy_last_7y_flag"], app["collections_past_12_months_flag"]):
        rate -= 0.15
    return rate


def final_outcome(app: pd.Series, risk: pd.Series, preliminary: str) -> tuple[str, str]:
    submitted = parse_app_date(app["date"])
    if submitted > EXTRACT_DATE:
        return "", ""
    key = app["application_id"]
    r, t = draw(key, "final-outcome"), draw(key, "final-days")
    if preliminary == "Declined":
        outcome, days = "Declined", int(t * 4)
    elif preliminary == "Approved":
        outcome, days = ("Withdrawn", 3 + int(t * 28)) if r < 0.05 else ("Approved", 1 + int(t * 7))
    else:
        days = 5 + int(t * 41)
        approve = review_approval_rate(app, risk)
        if r < 0.07:
            outcome = "Withdrawn"
        elif r < 0.07 + 0.93 * approve:
            outcome = "Approved"
        else:
            outcome = "Declined"
    decided = submitted + pd.Timedelta(days=days)
    if decided > EXTRACT_DATE:
        return "", ""          # still open on the extract date
    return outcome, format_app_date(decided)


def derive_decisions(la: pd.DataFrame, lp: pd.DataFrame, rf: pd.DataFrame) -> pd.DataFrame:
    products = lp.set_index("product_code")
    risks = rf.set_index("application_id")
    preliminary, final, final_date = [], [], []
    for _, app in la.iterrows():
        product, risk = products.loc[app["product_code"]], risks.loc[app["application_id"]]
        if eligibility_failures(app, product, risk):
            decision = "Declined"
        elif needs_manual_review(risk):
            decision = "Review"
        else:
            decision = "Approved"
        outcome, decided = final_outcome(app, risk, decision)
        preliminary.append(decision)
        final.append(outcome)
        final_date.append(decided)
    la["preliminary_decision"] = preliminary
    la["final_decision"] = final
    la["final_decision_date"] = final_date
    return la


def main() -> None:
    la = read("loan_application.csv")
    ev = read("credit_pull_event.csv")
    rf = read("applicant_risk_features.csv")
    lp = read("loan_product.csv")

    lp = fix_products(lp)
    la, redrawn, new_income = fix_amounts(la, lp)
    app_date = dict(zip(la["application_id"], la["date"].map(parse_app_date)))
    no_history = set(rf.loc[rf["credit_history_status"] == "NO_HISTORY", "application_id"])
    ev = fix_pulls(ev, app_date, no_history)
    scored = latest_scores(ev, app_date)
    la = derive_fico(la, scored)
    la, moved_down, moved_up = realign_products(la, lp)
    la, redrawn_after_move, _ = fix_amounts(la, lp)
    rf = derive_risk_features(rf, la, scored)
    la = derive_decisions(la, lp, rf)

    write(lp, "loan_product.csv")
    write(la, "loan_application.csv")
    write(ev, "credit_pull_event.csv")
    write(rf, "applicant_risk_features.csv")

    print(f"amounts redrawn: {redrawn + redrawn_after_move} (incomes raised for jumbo: {new_income})")
    print(f"products realigned to the applicant's score: {moved_down} down, {moved_up} up")
    print(f"credit pulls: {len(ev)}")
    print("preliminary_decision:", la["preliminary_decision"].value_counts().to_dict())
    print("final_decision:", la["final_decision"].replace("", "(open)").value_counts().to_dict())
    print("credit_history_status:", rf["credit_history_status"].value_counts().to_dict())
    print("risk_tier:", rf["risk_tier"].value_counts().sort_index().to_dict())


if __name__ == "__main__":
    main()
