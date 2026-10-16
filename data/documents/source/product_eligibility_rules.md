# Product Eligibility Rules

**Policy ID:** ELIG-001   
**Version:** V1.0    
**Status:** active   
**Prepared:** December 15, 2023    
**Proposed owner:** Credit Risk Function   
**Proposed approver:** Credit Risk Committee  
**Review cycle:** Annually

---

## Purpose

Defines the borrower and collateral eligibility criteria for each tier within the three product lines: **Mortgage**, **Credit Card**, and **Auto**. Used as a quick-reference for loan officers/underwriters to determine which tier a borrower and application qualify for.

## Product Code Reference

| Product Line | Tier | Product Code (this project's data) |
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

| Tier | Code | Min. Credit Score | Max. DTI | Down Payment | Loan Limit | Notes |
|---|---|---|---|---|---|---|
| **FHA** | `MTG-FH` | 620 | ≤ 50% | 3.5% | County FHA limit | Requires upfront + annual MIP; owner-occupied primary residence only |
| **Conventional** | `MTG-CV` | 680 | ≤ 45% | 3-20% | County conforming limit (Fannie/Freddie) | PMI required if <20% down; PMI cancels at 78% LTV |
| **Jumbo** | `MTG-JB` | 740 | ≤ 43% | 10-20%+ | Above conforming limit | Larger cash reserve requirements (6-12 months PITI); tighter appraisal review |

**Common eligibility items across all mortgage tiers:**
- 2 years of employment/income history (or documented explanation of gaps)
- Property must pass appraisal at or above purchase price/loan amount
- No open collections/judgments that affect title (or must be resolved at closing)
- Bankruptcy seasoning: typically 2 years post-Chapter 7 discharge, 1–2 years into a Chapter 13 plan with trustee approval

---

## 2. Credit Card

| Tier | Code | Min. Credit Score | Income Requirement | Credit Limit Range | Notes |
|---|---|---|---|---|---|
| **Secured** | `CRD-SC` | Minimum FICO 300; no score accepted (building credit) | Sufficient income to make min. payments | Equal to security deposit ($200-$2,500 typical) | Deposit held as collateral; graduates to unsecured after 6-12 months of on-time payments |
| **Standard** | `CRD-ST` | 620 | Verifiable income, debt-to-income within issuer policy | $500-$5,000 typical | Standard APR range; may include intro APR promos |
| **Elite (720+)** | `CRD-EL` | 720 | Higher income threshold, strong revolving utilization history | $5,000-$25,000+ | Premium rewards/travel benefits; often requires low overall utilization (<30%) across existing tradelines |

**Common eligibility items across all credit card tiers:**
- No recent charge-offs on similar unsecured tradelines (varies by tier tolerance)
- Applicant must be 18+ (21+ if income alone doesn't support repayment, per CARD Act)
- Existing relationship/deposit history with the institution may be weighted favorably

---

## 3. Auto Loan

| Tier | Code | Min. Credit Score | Max. DTI | Max. LTV | Term Range | Notes |
|---|---|---|---|---|---|---|
| **Subprime** | `AUT-SP` | No minimum; no score accepted | ≤ 60% | Up to 125% (incl. taxes/fees/GAP) | 60-75 months | Higher rate; often requires proof of income/residence stability; may require larger down payment on older/high-mileage vehicles |
| **Traditional** | `AUT-TR` | 680 | ≤ 50% | Up to 110% | 48-72 months | Standard documentation; vehicle age/mileage caps typically apply (e.g., ≤10 years, ≤120K miles) |
| **Top-tier credit** | `AUT-TT` | 800 | ≤ 45% | Up to 100-105% | 36-72 months | Best available rate; minimal stipulations; may qualify for manufacturer/dealer incentive rate stacking |

**Common eligibility items across all auto tiers:**
- Vehicle must meet lender's age/mileage eligibility (varies by tier — subprime lenders often have looser vehicle-age limits but higher rate offset)
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
- Confirm auto lender-specific vehicle age/mileage caps by tier.
- Add compensating-factor list (reserves, low LTV, etc.) that allows exceptions to standard thresholds.

---

*This document uses representative industry-standard criteria for an academic microcosm. It does not represent any lender's actual program guidelines or investor overlays.*
