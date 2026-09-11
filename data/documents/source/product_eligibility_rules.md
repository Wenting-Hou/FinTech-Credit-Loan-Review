# Product Eligibility Rules

**Policy ID:** ELIG-001   
**Version:** V1.0    
**Status:** In progress   
**Prepared:** NA    
**Proposed owner:** Credit Risk Function   
**Proposed approver:** Credit Risk Committee  
**Review cycle:** Annually

---

## Purpose

Defines the borrower and collateral eligibility criteria for each tier within the three product lines: **Mortgage**, **Credit Card**, and **Auto**. Used as a quick-reference for loan officers/underwriters to determine which tier a borrower and application qualify for.

## Revision Note (2026-09-08)

A teammate flagged that this document's thresholds appeared to disagree with `loan_product.csv` — specifically, Credit Card Standard minimum FICO. On review: `loan_product.csv` row `CC-STD-02` actually lists **`minimum_fico = 640`**, not 620 (the 620 value belongs to unrelated products — `PL-STD-01`, `AUTO-NEW-01/USED-02`, `DCL-01`). So this document's original 640–689 range was already consistent at the boundary; no change was needed there.

However, cross-referencing our team's actual project files (`loan_application.csv`, `credit_pull_events.csv`, `applicant_risk_features.csv`) surfaced a more useful finding: those files use a different, more specific product-code scheme (`AUT-SP/TR/TT`, `CRD-EL/SC/ST`, `MTG-CV/FH/JB`) that maps directly onto our Mortgage/Credit Card/Auto × 3-tier framework. This revision adds those product codes below, and adds a **Data Notes** section (§5) flagging a data-quality issue in the mock application data worth raising with the team.

---

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

*(Note: `loan_product.csv` uses a separate, broader product catalog with different codes, e.g. `CC-STD-02`, `AUTO-NEW-01` — those do not map 1:1 to this project's 3×3 tier structure and are a different reference table, not a contradiction of it.)*

---

## 1. Mortgage

| Tier | Code | Min. Credit Score | Max. DTI | Down Payment | Loan Limit | Notes |
|---|---|---|---|---|---|---|
| **FHA** | `MTG-FH` | 580 (500–579 w/ 10% down) | ≤ 43–50% (with compensating factors) | 3.5% (10% if score 500–579) | County FHA limit | Requires upfront + annual MIP; owner-occupied primary residence only |
| **Conventional** | `MTG-CV` | 620 | ≤ 45% (up to 50% w/ strong file) | 3–20% | County conforming limit (Fannie/Freddie) | PMI required if <20% down; PMI cancels at 78% LTV |
| **Jumbo** | `MTG-JB` | 700+ (often 740+) | ≤ 43% | 10–20%+ | Above conforming limit | Larger cash reserve requirements (6–12 months PITI); tighter appraisal review |

**Common eligibility items across all mortgage tiers:**
- 2 years of employment/income history (or documented explanation of gaps)
- Property must pass appraisal at or above purchase price/loan amount
- No open collections/judgments that affect title (or must be resolved at closing)
- Bankruptcy seasoning: typically 2 years post-Chapter 7 discharge, 1–2 years into a Chapter 13 plan with trustee approval

---

## 2. Credit Card

| Tier | Code | Min. Credit Score | Income Requirement | Credit Limit Range | Notes |
|---|---|---|---|---|---|
| **Secured** | `CRD-SC` | No minimum / building credit | Sufficient income to make min. payments | Equal to security deposit ($200–$2,500 typical) | Deposit held as collateral; graduates to unsecured after 6–12 months of on-time payments |
| **Standard** | `CRD-ST` | 640–689 (fair to good) | Verifiable income, debt-to-income within issuer policy | $500–$5,000 typical | Standard APR range; may include intro APR promos |
| **Elite (720+)** | `CRD-EL` | 720+ | Higher income threshold, strong revolving utilization history | $5,000–$25,000+ | Premium rewards/travel benefits; often requires low overall utilization (<30%) across existing tradelines |

**Common eligibility items across all credit card tiers:**
- No recent charge-offs on similar unsecured tradelines (varies by tier tolerance)
- Applicant must be 18+ (21+ if income alone doesn't support repayment, per CARD Act)
- Existing relationship/deposit history with the institution may be weighted favorably

---

## 3. Auto Loan

| Tier | Code | Min. Credit Score | Max. DTI | Max. LTV | Term Range | Notes |
|---|---|---|---|---|---|---|
| **Subprime** | `AUT-SP` | <620 (often 500–619) | ≤ 50% | Up to 125% (incl. taxes/fees/GAP) | 60–75 months | Higher rate; often requires proof of income/residence stability; may require larger down payment on older/high-mileage vehicles |
| **Traditional** | `AUT-TR` | 620–719 | ≤ 45% | Up to 110% | 48–72 months | Standard documentation; vehicle age/mileage caps typically apply (e.g., ≤10 years, ≤120K miles) |
| **Top-tier credit** | `AUT-TT` | 720+ | ≤ 40% | Up to 100–105% | 36–72 months | Best available rate; minimal stipulations; may qualify for manufacturer/dealer incentive rate stacking |

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

---

## 5. Data Notes — Findings from `loan_application.csv`

Cross-checking the tier thresholds above against actual approved/declined applications (`loan_application.csv`, n=600) surfaced a **data-quality issue worth raising with the team**: the mock `preliminary_decision` field does not appear to differentiate approval FICO thresholds by product tier the way the policy table above implies it should.

| Product Code | Approved FICO (min / median / max) | Declined FICO (min / median / max) |
|---|---|---|
| `AUT-SP` (Subprime) | 744 / 779 / 840 | 302 / 431 / 608 |
| `AUT-TR` (Traditional) | 747 / 799 / 847 | 371 / 549 / 619 |
| `AUT-TT` (Top-tier) | 745 / 798 / 842 | 369 / 477 / 772 |
| `CRD-SC` (Secured) | 740 / 791 / 847 | 378 / 507 / 611 |
| `CRD-ST` (Standard) | 742 / 794 / 843 | 325 / 429 / 526 |
| `CRD-EL` (Elite) | 745 / 792 / 850 | 316 / 504 / 604 |
| `MTG-FH` (FHA) | 745 / 771 / 825 | 371 / 536 / 618 |
| `MTG-CV` (Conventional) | 742 / 782 / 850 | 346 / 481 / 577 |
| `MTG-JB` (Jumbo) | 752 / 793 / 838 | 336 / 499 / 576 |

**The issue:** approved-FICO minimums cluster around 740–752 for *every single product*, including `AUT-SP` (Subprime) and `CRD-SC` (Secured) — tiers that are specifically supposed to serve *lower*-credit borrowers below these policy thresholds. This suggests the mock dataset's decision field was likely generated from a single uniform FICO cutoff (~700–740) rather than tier-specific logic, and should **not** be used as-is to derive or validate per-tier eligibility thresholds — doing so would (incorrectly) suggest Subprime and Top-tier products require the same credit score.

**Recommendation for the team:** flag this in the capstone writeup as a known limitation of the mock data, and continue using the policy-based thresholds in §1–3 above (industry-standard ranges) rather than thresholds derived from `preliminary_decision` outcomes, unless/until the mock data generation logic is revised to be tier-differentiated.

---

## 6. Open Items / TBD

- [ ] Confirm exact DTI/LTV thresholds against current investor/agency guidelines (Fannie Mae/Freddie Mac/FHA handbooks) — these are illustrative industry-standard ranges, not confirmed program guidelines.
- [ ] Confirm current credit card issuer-specific underwriting matrix (if this doc maps to a specific institution's actual card products).
- [ ] Confirm auto lender-specific vehicle age/mileage caps by tier.
- [ ] Add compensating-factor list (reserves, low LTV, etc.) that allows exceptions to standard thresholds.
- [ ] Raise the mock-data tier-differentiation issue (§5) with the team/instructor — may affect other parts of the project relying on `preliminary_decision`.

---

*This document is a working knowledge-base draft using representative industry-standard criteria. It must be validated against actual program guidelines/investor overlays before use in production underwriting.*
