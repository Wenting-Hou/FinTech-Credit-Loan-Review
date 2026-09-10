# Applicant Credit Risk Classification Policy

**Policy ID:** RISK  
**Version:** V1.0  
**Status:** active 
**Prepared:** September 10, 2026  
**Proposed owner:** Quality & Governance Lead: Wenting Hou
**Proposed approver:** Credit Risk Committee 
**Review cycle:** Annually and following a material policy change

## Policy Purpose

This policy establishes a standardized methodology for classifying loan applicants into **five credit-risk tiers (T1 through T5)** using credit history and financial information available at the time of application.

The risk tiers are ordered from lowest to highest observed credit risk:
- T1 – Very Low Risk
- T2 – Low Risk
- T3 – Moderate Risk
- T4 – High Risk
- T5 – Very High Risk

The methodology is designed solely for this academic microcosm. The thresholds, scoring weights, and classifications are synthetic assumptions and do not represent actual lender underwriting standards, regulatory requirements, or credit bureau methodologies.

**Policy ID:** RISK-TIER
**Policy Version:** 1.0
**Effective Date:** September 1, 2026


## Policy Principle

Risk classification must be based only on information that was available **on or before the loan application date**.

Information generated after the application date, including subsequent credit events, lending decisions, approved amounts, or decision outcomes, must not be used to derive the applicant's risk tier.

The policy uses a **24-month credit-history lookback period** measured from the application date.


## Permitted Risk Factors

The following information may be used in determining an applicant's risk tier:

### Applicant Financial Information

* Annual income

### Credit History Information

* Credit event date
* Days overdue
* Outstanding debt
* Overdue amount

Only credit events occurring within the 24 months preceding and including the application date are eligible for risk assessment.


## Prohibited Risk Factors

The following information must not be used in calculating the risk tier:

* Gender
* Family status
* Region
* Default outcome or target
* Loan decision status
* Decision reason code
* Approved loan amount
* Credit events occurring after the application date

These fields are excluded to prevent outcome leakage and to separate the risk-classification process from subsequent lending decisions.


## Credit History Classification

Before calculating a risk score, the applicant's available credit history must be classified based on the amount of observable history within the 24-month lookback period.

| Observed Credit History | Classification      |
| ----------------------- | ------------------- |
| 0 months                | **NO_HISTORY**      |
| 1–5 months              | **LIMITED_HISTORY** |
| 6+ months               | **ESTABLISHED**     |

Applicants with **NO_HISTORY** are assigned **T3 – Moderate Risk** rather than being scored using unavailable credit-history information.

Applicants with **LIMITED_HISTORY** are scored using the standard methodology but must be identified with a limited-credit-history flag.

Applicants with **ESTABLISHED** credit history are evaluated using the standard scoring methodology.


**For LIMITED or ESTABLISHED history, calculate three risk factors as following**

The risk assessment considers three primary dimensions:

### 1. Delinquency Severity

The maximum number of days overdue across eligible credit events is used to measure delinquency severity.

| Maximum Days Overdue | Risk Points |
| -------------------: | ----------: |
|                    0 |           0 |
|                 1–29 |           1 |
|                30–59 |           2 |
|                60–89 |           3 |
|               90-119 |           4 |
|                 120+ |           5 |

### 2. Debt Burden

Total outstanding debt is calculated using the most recent outstanding debt observation for each credit record within the eligible lookback period.

Debt burden is calculated as:

**Debt-to-Income Ratio = Total Outstanding Debt ÷ Annual Income**

| Debt-to-Income Ratio | Risk Points |
| -------------------: | ----------: |
|                ≤ 25% |           0 |
|             >25%–50% |           1 |
|             >50%–75% |           2 |
|                 >75% |           3 |

### 3. Overdue Debt Burden

Total overdue amount is calculated using the most recent overdue amount observation for each credit record within the eligible lookback period.

The overdue burden ratio is calculated as:

**Overdue Amount-to-Income Ratio = Total Overdue Amount ÷ Annual Income**

| Overdue Amount / Income | Risk Points |
| ----------------------: | ----------: |
|                      0% |           0 |
|                  >0%–2% |           1 |
|                  >2%–5% |           2 |
|                     >5% |           3 |


## Risk Score Calculation

For applicants eligible for standard scoring:

**Risk Score = Delinquency Points + Debt Burden Points + Overdue Amount Points**

The possible score ranges from **0 to 11 points**:
- Delinquency Points: 0–5
- Debt Burden Points: 0–3
- Overdue Amount Points: 0–3

A higher score represents greater observed credit risk.

| Total Risk score | Risk tier | Risk Classification |
| ---------------: | --------- | ------------------- |
|    **0–1**       | **T1**    | Very Low Risk       |
|    **2–3**       | **T2**    | Low Risk            |
|    **4–5**       | **T3**    | Moderate Risk       |
|    **6–7**       | **T4**    | High Risk           |
|    **8–11**      | **T5**    | Very High Risk      |

## Special Credit History Rules

### No Credit History

Applicants with no observable credit history during the 24-month lookback period are assigned:

**Risk Tier:** T3
**Risk Classification:** Moderate Risk
**Risk Tier Basis:** NO_CREDIT_HISTORY

A numeric `risk_tier_score` is not calculated when the applicant has no eligible credit history because the underlying credit-history measures are unavailable.

This classification reflects uncertainty caused by insufficient historical information rather than demonstrated delinquency.

### Limited Credit History

Applicants with 1–5 months of observable credit history are evaluated using the standard risk score.

Their classification must additionally identify:

**Risk Tier Basis:** LIMITED_HISTORY
The calculated risk score determines whether the applicant is classified as T1, T2, T3, T4, or T5.

### Established Credit History

Applicants with at least six months of observable credit history are evaluated using the standard risk score.

Their classification must identify:

**Risk Tier Basis:** CREDIT_HISTORY
The calculated risk score determines whether the applicant is classified as T1, T2, T3, T4, or T5.

## Missing Data Policy

Annual income is required to calculate the debt burden measures. If annual income is missing, the risk-tier derivation must fail and the record must be flagged for data-quality review.

Missing `days_overdue` values must not be imputed without confirmation from the source data.

Unknown outstanding debt and overdue amounts must not automatically be treated as zero. Unknown observations are excluded from their respective aggregations and should remain identifiable as missing source information.


## Policy Output

The risk-classification process should produce, at minimum:

* Risk tier (T1, T2, T3, T4, or T5)
* Risk tier score, when applicable
* Risk tier basis
* Credit history status
* Policy version
* Policy effective date

The five-tier structure provides a more granular measure of applicant credit risk while maintaining traceability between the underlying risk factors, calculated score, and resulting classification.


## Academic Methodology Notice

This risk classification policy is a **synthetic academic policy developed for the project microcosm**.

The risk thresholds, scoring weights, lookback periods, and tier definitions are project assumptions. They are not intended to represent actual underwriting policies, regulatory thresholds, credit bureau scoring methodologies, or the practices of Home Credit, Fannie Mae, or any other financial institution.
