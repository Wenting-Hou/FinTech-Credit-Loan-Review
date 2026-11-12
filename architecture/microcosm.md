# Loan Credit Review Domain Microcosm


<img width="1017" height="1021" alt="image" src="https://github.com/user-attachments/assets/1319c120-0364-40ed-87e7-11e7c4f45e55" />

#### Pillar A: Structured Data / Analytical Features
Built from five datasets:
1.  **Applicants + Loan Applications + Credit Pull Events + Applicant Risk Features**
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

The structured layer contains 5 datasets:

| Dataset | File | Primary Key | Description |
| :--- | :--- | :--- | :--- |
| **Applicants** | `applicant.csv` | `applicant_id` | One row per person: synthetic identity and contact details only. No scores or amounts |
| **Loan Applications** | `loan_application.csv` | `application_id` | Core application record: applicant, date, requested product/amount, income, FICO, payment DTI, state, SCRA/bankruptcy/collections flags, preliminary and final decision. FK: `applicant_id`, `product_code` |
| **Applicant Risk Features** | `applicant_risk_features.csv` | `application_id` | Derived point-in-time risk snapshot, one per application (`appli_risk_id` is a unique surrogate). Contains credit history, delinquency, debt measures, risk score and tier |
| **Credit Pull Events** | `credit_pull_event.csv` | `event_id` | One observation per bureau pull. FK: `application_id`. Contains event date, FICO score, bureau, status and reason |
| **Loan Products** | `loan_product.csv` | `product_code` | Reference table: product family, eligibility, minimum risk tier and FICO, no-score acceptance, base rate, maximum amount and DTI, rate adjustments |

See the [detailed ERD](./erd_diagram.md).

**Relationships:**
- `Applicant (1) -> Loan_application (1..N)`: via `applicant_id`. One applicant per application, no co-applicants; a move requires a new application
- `Loan_product (1) -> Loan_application (0..N)`: via `product_code`
- `Loan_application (1) -> Applicant_risk_feature (1)`: via `application_id` with UNIQUE constraint - preserves audit trail
- `Loan_application (1) -> Credit_pull_event (0..N)`: via `application_id` - tracks re-pulls and bureau changes

> **Critical Logic:** Risk features are calculated ONLY from information available on or before the `as_of_date` / assessment timestamp, within a defined lookback period.

