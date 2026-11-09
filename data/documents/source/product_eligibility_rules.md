# Product Eligibility Rules

**Policy ID:** ELIG-001   
**Version:** V1.0    
**Status:** Effective  
**Effective date:** January 1, 2024  
**In force until:** December 31, 2026  
**Superseded by:** ELIG-001 V2.0 (`product_eligibility_rules_v2.md`), effective January 1, 2027  
**Prepared:** December 15, 2023    
**Proposed owner:** Credit Risk Function   
**Proposed approver:** Credit Risk Committee  
**Review cycle:** Annually

---

## Purpose

Defines the borrower and collateral eligibility criteria for each product level within the three product lines: **Mortgage**, **Credit Card**, and **Auto**. Used as a quick reference for loan officers and underwriters to determine which product a borrower and application qualify for.

*"Product level" in this document means the product variant (for example FHA or Elite). It is not the applicant risk tier (T1 to T5), which is defined in RISK-TIER (`applicant_risk_policy.md`).*

## Product Code Reference

| Product Line | Product level | Product Code (this project's data) |
|---|---|---|
| Mortgage | FHA | `MTG-FH` |
| Mortgage | Conventional | `MTG-CV` |
| Mortgage | Jumbo | `MTG-JB` |
| Credit Card | Secured | `CRD-SC` |
| Credit Card | Standard | `CRD-ST` |
| Credit Card | Elite (720+) | `CRD-EL` |
| Auto | Subprime | `AUT-SP` |
| Auto | Traditional | `AUT-TR` |
| Auto | Top-tier credit | `AUT-TT` |

*(Note: `loan_product.csv` uses these same nine product codes and is the system of record for the numerical gates in the next section. Sections 1 to 3 describe each product; where a figure appears in both places, the two must agree.)*

---

## Catalog Gates (system of record: `loan_product.csv`)

| Code | Minimum risk tier | Minimum FICO | Accepts no score | Max. payment DTI | Maximum amount | Bankruptcy allowed | Collections allowed |
|---|---|---|---|---|---|---|---|
| `MTG-FH` | T4 | 620 | Yes | 50% | $500,000 | Yes | Yes |
| `MTG-CV` | T3 | 680 | No | 45% | $1,000,000 | No | Yes |
| `MTG-JB` | T2 | 740 | No | 43% | $2,500,000 | No | No |
| `CRD-SC` | T5 | 300 | Yes | 60% | $3,000 | Yes | Yes |
| `CRD-ST` | T4 | 620 | No | 50% | $15,000 | No | Yes |
| `CRD-EL` | T2 | 720 | No | 45% | $50,000 | No | No |
| `AUT-SP` | T5 | 300 | Yes | 60% | $35,000 | Yes | Yes |
| `AUT-TR` | T3 | 680 | No | 50% | $60,000 | No | Yes |
| `AUT-TT` | T1 | 800 | No | 45% | $100,000 | No | No |

- **Minimum risk tier** is tested against the applicant's `risk_tier` under RISK-TIER (`applicant_risk_policy.md`). It is never tested against a band of the FICO score.
- **Minimum FICO** is tested against the applicant's FICO score: the latest score returned by a credit pull on or before the application date.
- **Max. payment DTI** is tested against `dti_pct` only, never against the applicant risk policy's `debt_burden_ratio`.
- An application that fails any gate is not eligible for that product. A favorable risk tier does not override a failed gate.

---

## 1. Mortgage

| Product level | Code | Min. Credit Score | Max. DTI | Down Payment | Maximum loan amount | Notes |
|---|---|---|---|---|---|---|
| **FHA** | `MTG-FH` | 620 | ≤ 50% | 3.5% | Up to $500,000 | Requires upfront + annual MIP; owner-occupied primary residence only |
| **Conventional** | `MTG-CV` | 680 | ≤ 45% | 3-20% | Up to $1,000,000 | PMI required if <20% down; PMI cancels at 78% LTV |
| **Jumbo** | `MTG-JB` | 740 | ≤ 43% | 10-20%+ | Up to $2,500,000 | Larger cash reserve requirements (6-12 months PITI); tighter appraisal review |

**Common eligibility items across all mortgage products:**
- 2 years of employment/income history (or documented explanation of gaps)
- Property must pass appraisal at or above purchase price/loan amount
- Collections in the past 12 months: allowed for `MTG-FH` and `MTG-CV`, not allowed for `MTG-JB` (Catalog Gates). Any collection or judgment that affects title must be resolved at closing.
- Bankruptcy in the past 7 years: allowed only for `MTG-FH`; `MTG-CV` and `MTG-JB` do not accept it (Catalog Gates). For `MTG-FH`, the underwriter also confirms a Chapter 7 discharge at least 2 years old, or at least 1 year of on-time Chapter 13 plan payments with trustee approval.

---

## 2. Credit Card

| Product level | Code | Min. Credit Score | Income Requirement | Maximum credit limit | Notes |
|---|---|---|---|---|---|
| **Secured** | `CRD-SC` | Minimum FICO 300; no score accepted (building credit) | Sufficient income to make min. payments | Equal to the security deposit, up to $3,000 | Deposit held as collateral; graduates to unsecured after 6-12 months of on-time payments |
| **Standard** | `CRD-ST` | 620 | Verifiable income, debt-to-income within issuer policy | Up to $15,000 | Standard APR range; may include intro APR promos |
| **Elite (720+)** | `CRD-EL` | 720 | Higher income threshold, strong revolving utilization history | Up to $50,000 | Premium rewards/travel benefits; often requires low overall utilization (<30%) across existing tradelines |

**Common eligibility items across all credit card products:**
- No recent charge-offs on similar unsecured tradelines (varies by product)
- Applicant must be 18+ (21+ if income alone doesn't support repayment, per CARD Act)
- Existing relationship/deposit history with the institution may be weighted favorably

---

## 3. Auto Loan

| Product level | Code | Min. Credit Score | Max. DTI | Maximum loan amount | Max. LTV | Term Range | Notes |
|---|---|---|---|---|---|---|---|
| **Subprime** | `AUT-SP` | Minimum FICO 300; no score accepted | ≤ 60% | Up to $35,000 | Up to 125% (incl. taxes/fees/GAP) | 60-75 months | Higher rate; often requires proof of income/residence stability; may require larger down payment on older/high-mileage vehicles |
| **Traditional** | `AUT-TR` | 680 | ≤ 50% | Up to $60,000 | Up to 110% | 48-72 months | Standard documentation; vehicle age/mileage caps typically apply (e.g., ≤10 years, ≤120K miles) |
| **Top-tier credit** | `AUT-TT` | 800 | ≤ 45% | Up to $100,000 | Up to 100-105% | 36-72 months | Best available rate; minimal stipulations; may qualify for manufacturer/dealer incentive rate stacking |

**Common eligibility items across all auto products:**
- Vehicle must meet lender's age/mileage eligibility (varies by product; subprime lenders often have looser vehicle-age limits but higher rate offset)
- Valid proof of insurance (comprehensive/collision) required to fund
- Lien must be perfected on title per state rules (see *Regional/State Lending Requirements*)

---

## 4. Cross-Product Disqualifiers (all products)

- Active bankruptcy without court/trustee approval to incur new debt
- Unresolved fraud alert or identity-verification failure
- OFAC/sanctions list match
- Insufficient documented income to support minimum required payment (ability-to-repay standard)
- No credit score, for any product other than `MTG-FH`, `CRD-SC` and `AUT-SP`

**Applicants with no credit score (NO_HISTORY):** `MTG-FH`, `CRD-SC` and `AUT-SP` accept an applicant who has no credit score. The application goes to manual underwriting, which assesses verified income, reserves or down payment, and non-traditional credit such as rent and utility payment history. All other products require a FICO score at or above the minimum in the Catalog Gates table.

---

## 5. Planned Enhancements (not part of this version)

- Confirm exact DTI/LTV thresholds against current investor/agency guidelines (Fannie Mae/Freddie Mac/FHA handbooks); these are illustrative industry-standard ranges, not confirmed program guidelines.
- Confirm current credit card issuer-specific underwriting matrix (if this doc maps to a specific institution's actual card products).
- Confirm auto lender-specific vehicle age/mileage caps by product.
- Add a compensating-factor list (reserves, low LTV, etc.) for requirements outside the Catalog Gates. Catalog gates are never waived.

---

*This document uses representative industry-standard criteria for an academic microcosm. It does not represent any lender's actual program guidelines or investor overlays.*
