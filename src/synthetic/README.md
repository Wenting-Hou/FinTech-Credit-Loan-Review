# Synthetic Source Data

The four CSVs in `data/structured/raw/` are synthetic. Some fields come straight from the original generator. Others are **derived** from those fields and from the team's policies, and `regenerate_source_data.py` rebuilds them so the files never contradict each other.

## Run it

```bash
python src/synthetic/regenerate_source_data.py      # rebuild the derived fields
python src/validation/check_source_consistency.py   # prove the result (57 checks)
```

The script uses a fixed seed, so running it twice gives identical files. Run the checker after any manual edit to the raw data or to `loan_product.csv`.

## Which fields are derived, and from what

| File | Field | Rule | Source |
|---|---|---|---|
| loan_application | `fico_score` | Score of the latest pull with a returned score on or before `date`. Empty for NO_HISTORY applicants | applicant_risk_policy.md, Policy Principle |
| loan_application | `preliminary_decision` | Declined if any product gate fails; otherwise Review for NO_HISTORY, LIMITED_HISTORY, T4 or T5; otherwise Approved | product_eligibility_rules.md Catalog Gates, product_risk_policy.md sections 3 and 4 |
| loan_application | `final_decision`, `final_decision_date` | Simulated underwriting outcome (Approved, Declined, Withdrawn). Empty while open on the extract date (2026-09-14) and for every application dated after it | approval_escalation_procedures.md |
| applicant_risk_features | `credit_history_months_observed`, `credit_history_status`, `risk_tier_basis` | Months cover the oldest scored pull in the 24 month lookback; status and basis follow the policy bands | applicant_risk_policy.md, Credit History Classification |
| applicant_risk_features | `debt_burden_ratio`, `overdue_amount_to_income` | Debt or overdue amount divided by annual income, 4 decimals | applicant_risk_policy.md, sections 2 and 3 |
| applicant_risk_features | `delinquency_points`, `debt_burden_points`, `overdue_amount_points`, `risk_tier_score`, `risk_tier` | Policy points tables, score is the sum, tier from the score table. NO_HISTORY rows are T3 with no points and no score | applicant_risk_policy.md, Risk Score Calculation |
| credit_pull_event | `fico_score` | Empty on Error and Pending pulls (no result returned). Pending only within 14 days of the extract date | |

**Gates tested by `preliminary_decision`:** requested amount above `maximum_amount_usd`, `dti_pct` above `max_dti_pct`, bankruptcy or collections on a product that does not allow it, `risk_tier` worse than `minimum_risk_tier`, `fico_score` below `minimum_fico`, or no score on a product with `allow_no_score_flag` = FALSE.

Everything else (income, debts, days overdue, flags, dates, bureaus, reasons, product terms) is generator-owned and is left as it is, apart from two plausibility rules:

- **Product fits the applicant.** People mostly apply for a product their credit score can reach. An applicant below the product's minimum FICO, or with no score on a product that needs one, moves to the best product in the same family they fit. 20% of them stay where they are as realistic outliers and are declined; these are the cases a later counteroffer feature (smaller loan or higher rate) would pick up. An applicant whose score is at least 40 points above a better product's minimum leaves the entry product (FHA, secured card, subprime auto) 60% of the time. Nobody moves up into Jumbo, because Jumbo is chosen by loan size. If the new product's maximum is lower, the requested amount is redrawn under it.
- **Amount fits income.** Requested amounts above 5x income (mortgage), 0.5x (card) or 1.5x (auto) are redrawn, and a jumbo applicant who cannot support the smallest jumbo loan gets a higher income.

## Do not "fix" these

They are documented, controlled quality problems (README section 5) that ingestion is expected to handle:

- Money stored as text (`"$147,346 "`) and quoted catalog amounts (`"500,000"`)
- `M/D/YYYY` dates and `TRUE/FALSE` booleans in loan_application, ISO dates and `True/False` in credit_pull_event
- 71 applications dated after the extract date, still carrying a `preliminary_decision`
- The `risk_policy.md` filename reference in enterprise_risk_policy.md and the applicant policy's Prepared date falling after its effective date

`event_reason` values and the order of `event_id` are synthetic and carry no meaning.
