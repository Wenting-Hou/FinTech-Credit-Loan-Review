# Loan Credit Review Domain Microcosm


<img width="1017" height="1021" alt="image" src="https://github.com/user-attachments/assets/1319c120-0364-40ed-87e7-11e7c4f45e55" />

#### Pillar A: Structured Data / Analytical Features
Derived from 3 sources:
1.  **Loan Applications + Credit Pull Events + Applicant Risk Features**
2.  **+ Loan Products**
3.  **= Structured Data / Analytical Features**

This layer provides all quantitative, point-in-time features for underwriting.

#### Pillar B: Knowledge Corpus -> Document Metadata
Represents the unstructured layer:
- **Knowledge Corpus:** Source policies, product guidelines, compliance docs
- **Document Metadata:** Parsed, indexed, and embedded representation of the corpus

#### Outcome: AI-Assisted Loan Review
The fusion of both pillars enables:
- Unified applicant review
- Decision support (approve/deny/refer)
- Explainable, auditable output

## 2. Structured Data Layer (Detailed ERD)

The structured layer contains 4 primary datasets:

| Dataset | File | Primary Key | Description |
| :--- | :--- | :--- | :--- |
| **Loan Applications** | `loan_applicantion.csv` | `application_id` | Core application record: date, requested product/amount, income, FICO, DTI, region, SCRA/bankruptcy flags |
| **Applicant Risk Features** | `applicant_risk_features.csv` | `appli_risk_id` | Derived point-in-time risk snapshot. FK: `application_id` (UNIQUE). Contains credit history, delinquency, debt measures, risk score/tier |
| **Credit Pull Events** | `credit_events.csv` | `event_id` | Historical credit changes. FK: `application_id`. Contains prior/new FICO/tier, bureau source, event status/reason |
| **Loan Products** | `loan_products.csv` | `product_code` | Reference table: product family, eligibility, min credit tier/FICO, base rate, max amount/DTI, rate adjustments |

![Detailed ERD](./architecture/erd_diagram.md) 

**Relationships:**
- `Loan_product (1) -> Loan_application (0..N)`: via `product_code`
- `Loan_application (1) -> Applicant_risk_feature (1)`: via `application_id` with UNIQUE constraint - preserves audit trail
- `Loan_application (1) -> Credit_pull_event (0..N)`: via `application_id` - tracks re-pulls and bureau changes

> **Critical Logic:** Risk features are calculated ONLY from information available on or before the `as_of_date` / assessment timestamp, within a defined lookback period.

