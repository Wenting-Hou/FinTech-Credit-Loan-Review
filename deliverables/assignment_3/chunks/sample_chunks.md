# Sample chunks and metadata (A3 section 2)

Final setup C: n8n Recursive Character Text Splitter, Markdown mode, 2,000 characters, 200 overlap (46 policy chunks). The chunk text below was produced with the same LangChain splitter outside n8n, which gives the same 46 chunks; in the n8n evidence previews the leading `## ` of a chunk does not appear. Dash characters are shown as hyphens.

Every chunk carries this metadata from the Default Data Loader: `doc_id`, `source_file`, `version`, `effective_date`, `effective_to`. Document-level fields (doc_type, authority_status, owner, confidentiality, access_group, jurisdiction, superseded_by) are kept once per version in [`metadata/document _metadata .csv`](../../../metadata/) and joined on doc_id and version.

## ELIG-001 V1.0: Catalog Gates

| doc_id | source_file | version | effective_date | effective_to | length |
|---|---|---|---|---|---|
| ELIG-001 | product_eligibility_rules.md | V1.0 | 2024-01-01 | 2026-12-31 | 1,310 characters |

```text
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
```

## ELIG-001 V2.0: Catalog Gates

| doc_id | source_file | version | effective_date | effective_to | length |
|---|---|---|---|---|---|
| ELIG-001 | product_eligibility_rules_v2.md | V2.0 | 2027-01-01 | open | 1,336 characters |

```text
## Catalog Gates, V2.0 (system of record: `loan_product.csv` from January 1, 2027)

| Code | Minimum risk tier | Minimum FICO | Accepts no score | Max. payment DTI | Maximum amount | Bankruptcy allowed | Collections allowed |
|---|---|---|---|---|---|---|---|
| `MTG-FH` | T4 | 620 | Yes | 50% | $500,000 | Yes | Yes |
| `MTG-CV` | T3 | 680 | No | 45% | $1,000,000 | No | Yes |
| `MTG-JB` | T2 | 760 | No | 43% | $2,000,000 | No | No |
| `CRD-SC` | T5 | 300 | Yes | 60% | $3,000 | Yes | Yes |
| `CRD-ST` | T4 | 660 | No | 50% | $10,000 | No | No |
| `CRD-EL` | T1 | 760 | No | 40% | $25,000 | No | No |
| `AUT-SP` | T5 | 300 | Yes | 50% | $25,000 | Yes | Yes |
| `AUT-TR` | T3 | 680 | No | 50% | $60,000 | No | Yes |
| `AUT-TT` | T1 | 800 | No | 45% | $100,000 | No | No |

- **Minimum risk tier** is tested against the applicant's `risk_tier` under RISK-TIER (`applicant_risk_policy.md`). It is never tested against a band of the FICO score.
- **Minimum FICO** is tested against the applicant's FICO score: the latest score returned by a credit pull on or before the application date.
- **Max. payment DTI** is tested against `dti_pct` only, never against the applicant risk policy's `debt_burden_ratio`.
- An application that fails any gate is not eligible for that product. A favorable risk tier does not override a failed gate.

---
```

## RISK-TIER V1.0: Special Credit History Rules

| doc_id | source_file | version | effective_date | effective_to | length |
|---|---|---|---|---|---|
| RISK-TIER | applicant_risk_policy.md | V1.0 | 2024-01-01 | open | 1,736 characters |

```text
## Special Credit History Rules

### No Credit History

Applicants with no observable credit history during the 24-month lookback period are assigned:

**Risk Tier:** T3
**Risk Classification:** Moderate Risk
**Risk Tier Basis:** NO_CREDIT_HISTORY

A numeric `risk_tier_score` is not calculated, and the three points fields are left empty, when the applicant has no eligible credit history because the underlying credit-history measures are unavailable.

This classification reflects uncertainty caused by insufficient historical information rather than demonstrated delinquency.

### Limited Credit History

Applicants with 1-5 months of observable credit history are evaluated using the standard risk score.

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
```

## PRODUCT-RISK V1.0: Applicant-tier overlay

| doc_id | source_file | version | effective_date | effective_to | length |
|---|---|---|---|---|---|
| PRODUCT-RISK | product_risk_policy.md | V1.0 | 2024-01-01 | open | 1,872 characters |

```text
## 3. Applicant-tier overlay

The applicant tier in this overlay, and the tier that `loan_product.minimum_risk_tier` is tested against, is `risk_tier` from `applicant_risk_features.csv`, derived under RISK-TIER (`applicant_risk_policy.md`). It describes the applicant, not the product, and it is not a band of the FICO score. The FICO score is tested separately against `minimum_fico`. The product ratings in section 2 describe the product and are never combined with this tier.

| Applicant tier / history | Proposed treatment across all nine products |
|---|---|
| T1-T2 | Follow the normal product route if every other requirement is met; product-specific mandatory reviews still apply |
| T3 with established history | Follow the normal product route, checking repayment capacity and any additional product triggers |
| T3 with NO_HISTORY | Available only on products with `allow_no_score_flag` = TRUE (MTG-FH, CRD-SC, AUT-SP). Require documented manual assessment of available repayment evidence, such as verified income, reserves or down payment, and non-traditional credit such as rent and utility history; keep risk_tier_basis = NO_CREDIT_HISTORY and a null numeric score |
| Any tier with LIMITED_HISTORY | Record the limited-history flag and require manual review of evidence sufficiency |
| T4 | Require the relevant senior product reviewer: Senior Underwriter / Underwriting Manager for mortgages, Underwriting Supervisor for cards, Underwriting Manager for auto |
| T5 | Refer to the Credit Risk Committee for assessment within its confirmed authority; no automatic approval or decline solely from this overlay |

Application rules:
- Where multiple triggers apply, use the highest applicable review level.  
- Fraud/sanctions routing takes priority. 
- A referral is not approval, and a favorable risk tier does not override a failed eligibility requirement.
```

## loan_product.csv: catalog row CRD-EL

One chunk per product, written by the Product rows Code node and stored by Simple Vector Store2.

| doc_id | source_file | product_code | version | effective_date | effective_to |
|---|---|---|---|---|---|
| loan_product.csv | loan_product.csv | CRD-EL | V1.0 | 2024-01-01 | 2026-12-31 |

```text
[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to 2026-12-31] Catalog gate for CRD-EL (Credit Card Elite 720+, Credit Card). Minimum applicant risk tier: T2. Minimum FICO: 720. Accepts applicant with no credit score: No. Maximum payment DTI: 45%. Maximum amount: $50,000. Bankruptcy allowed: No. Collections allowed: No. Base rate: 15.99%. Tier rate adjustments: T1=-2.00;T2=-1.00.
```
