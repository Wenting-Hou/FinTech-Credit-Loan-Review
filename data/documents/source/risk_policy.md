# Applicant Credit Risk Classification Policy

## 1. Policy Purpose

This policy establishes a standardized methodology for classifying loan applicants into **Low, Medium, or High credit risk tiers** using credit history and financial information available at the time of application.

The methodology is designed solely for this academic microcosm. The thresholds, scoring weights, and classifications are synthetic assumptions and do not represent actual lender underwriting standards, regulatory requirements, or credit bureau methodologies.

**Policy ID:** RISK-TIER
**Policy Version:** 1.0
**Effective Date:** September 1, 2026


## 2. Policy Principle

Risk classification must be based only on information that was available **on or before the loan application date**.

Information generated after the application date, including subsequent credit events, lending decisions, approved amounts, or decision outcomes, must not be used to derive the applicant's risk tier.

The policy uses a **24-month credit-history lookback period** measured from the application date.


## 3. Permitted Risk Factors

The following information may be used in determining an applicant's risk tier:

### Applicant Financial Information

* Annual income

### Credit History Information

* Credit event date
* Days overdue
* Outstanding debt
* Overdue amount

Only credit events occurring within the 24 months preceding and including the application date are eligible for risk assessment.


## 4. Prohibited Risk Factors

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


## 5. Credit History Classification

Before calculating a risk score, the applicant's available credit history must be classified based on the amount of observable history within the 24-month lookback period.

| Observed Credit History | Classification      |
| ----------------------- | ------------------- |
| 0 months                | **NO_HISTORY**      |
| 1–5 months              | **LIMITED_HISTORY** |
| 6+ months               | **ESTABLISHED**     |

Applicants with **NO_HISTORY** are assigned a **Medium Risk** tier rather than being scored using unavailable credit-history information.

Applicants with **LIMITED_HISTORY** are scored using the standard methodology but must be identified with a limited-credit-history flag.

Applicants with **ESTABLISHED** credit history are evaluated using the standard scoring methodology.


## 6. Risk Assessment Factors

The risk assessment considers three primary dimensions:

### Delinquency Severity

The maximum number of days overdue across eligible credit events is used to measure delinquency severity.

| Maximum Days Overdue | Risk Points |
| -------------------: | ----------: |
|                    0 |           0 |
|                 1–29 |           1 |
|                30–59 |           2 |
|                60–89 |           3 |
|                  90+ |           5 |

### Debt Burden

Total outstanding debt is calculated using the most recent outstanding debt observation for each credit record within the eligible lookback period.

Debt burden is calculated as:

**Debt-to-Income Ratio = Total Outstanding Debt ÷ Annual Income**

| Debt-to-Income Ratio | Risk Points |
| -------------------: | ----------: |
|                ≤ 25% |           0 |
|             >25%–50% |           1 |
|             >50%–75% |           2 |
|                 >75% |           3 |

### Overdue Debt Burden

Total overdue amount is calculated using the most recent overdue amount observation for each credit record within the eligible lookback period.

The overdue burden ratio is calculated as:

**Overdue Amount-to-Income Ratio = Total Overdue Amount ÷ Annual Income**

| Overdue Amount / Income | Risk Points |
| ----------------------: | ----------: |
|                      0% |           0 |
|                  >0%–2% |           1 |
|                  >2%–5% |           2 |
|                     >5% |           3 |


## 7. Risk Score Calculation

For applicants eligible for standard scoring:

**Risk Score = Delinquency Points + Debt Burden Points + Overdue Amount Points**

The resulting score determines the applicant's risk classification.

| Total Risk Score | Risk Tier  |
| ---------------: | ---------- |
|              0–2 | **LOW**    |
|              3–5 | **MEDIUM** |
|               6+ | **HIGH**   |

A higher score represents greater observed credit risk.


## 8. Special Credit History Rules

### No Credit History

Applicants with no observable credit history during the 24-month lookback period are assigned:

**Risk Tier:** MEDIUM
**Risk Tier Basis:** NO_CREDIT_HISTORY

This classification reflects uncertainty caused by insufficient historical information rather than demonstrated delinquency.

### 9. Limited Credit History

Applicants with 1–5 months of observable credit history are evaluated using the standard risk score.

Their classification must additionally identify:

**Risk Tier Basis:** LIMITED_HISTORY

### 10. Established Credit History

Applicants with at least six months of observable credit history are evaluated using the standard risk score.

Their classification must identify:

**Risk Tier Basis:** CREDIT_HISTORY

## 11. Missing Data Policy

Annual income is required to calculate the debt burden measures. If annual income is missing, the risk-tier derivation must fail and the record must be flagged for data-quality review.

Missing `days_overdue` values must not be imputed without confirmation from the source data.

Unknown outstanding debt and overdue amounts must not automatically be treated as zero. Unknown observations are excluded from their respective aggregations and should remain identifiable as missing source information.


## Policy Output

The risk-classification process should produce, at minimum:

* Risk tier
* Risk tier score, when applicable
* Risk tier basis
* Credit history status
* Policy version
* Policy effective date

These fields provide traceability between the applicant's classification and the policy used to generate it.


## Academic Methodology Notice

This risk classification policy is a **synthetic academic policy developed for the project microcosm**.

The risk thresholds, scoring weights, lookback periods, and tier definitions are project assumptions. They are not intended to represent actual underwriting policies, regulatory thresholds, credit bureau scoring methodologies, or the practices of Home Credit, Fannie Mae, or any other financial institution.
