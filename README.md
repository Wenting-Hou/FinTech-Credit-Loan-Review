# DSBA 6171: FinTech Credit & Loan Review Data & Knowledge Microcosm

## 1. Team Information & Roles

- **Team Number / Name:** Team 03 - FinTech
- **Team Lead / Liaison:** Tim Goncharov
- **Data & Ingestion Lead:** Evan de Guzman
- **Database & Analytics Lead:** Miguel Valenzuela
- **Knowledge & Retrieval Lead:** Ethan Hunter
- **Quality & Governance Lead:** Wenting Hou

---

## 2. Business Context & Problem Framing

- **Assigned Domain:** FinTech: Credit & Loan Review
- **Business Function / Process:** The domain microcosm represents a personal consumer lending credit-review process in which a lender evaluates loan applications using application information, credit history, derived applicant risk features, loan-product requirements, and applicable lending policies.
- **Target Stakeholders:** Underwriters, Credit Analysts, Chief Risk Officer, Credit Risk Committee,Compliance Team, Fair-Lending Team, Data Scientists, Loan Origination System (LOS) Engineers, FinTech Product Managers, Loan Officers, Applicants, Regulators, Credit Bureaus

- **Primary Decision Question:** Should this loan application be approved, denied, or escalated for manual review based on the application information, applicant risk profile, requested product requirements, credit information, and applicable compliance requirements?

- **Supporting Business Questions:**

1. Does the applicant's pre-decision risk profile satisfy the requirements of the requested loan product?
2. Which product requirements, such as minimum risk tier, FICO, DTI, loan amount, bankruptcy, and collections rules, affect applicant eligibility?
3. Which lending and compliance documents apply when reviewing the application?


---

## 3. Microcosm Assets Overview

### Structured Operational Datasets (`data/structured/raw/`)

- `loan_application.csv` - [one row per loan application: the financial profile, requested product and decisions at the application date, 600, application_id]
- `applicant_risk_features.csv` - [the applicant’s credit-risk profile at the time of each loan application, 600, application_id]
- `loan_product.csv` - [defines the available loan products and their associated eligibility, risk, and pricing requirements, 9, product_code]
- `credit_pull_event.csv` - [represents the applicant’s historical credit bureau pulls over time, one score per pull, 1775, event_id & application_id]
- `applicant.csv` - [one row per applicant; an applicant can have more than one application, 480, applicant_id]

### Knowledge Corpus (`data/documents/source/`)

- Contains **11** documents: **4** regulatory PDFs and **7** internal policy Markdown files.
- Includes structural challenges (tables, hierarchical headers) and two versions of one policy: Product Eligibility Rules (ELIG-001) V1.0 is in force from 2024-01-01 to 2026-12-31 (`product_eligibility_rules.md`), and V2.0 takes over on 2027-01-01 (`product_eligibility_rules_v2.md`). `metadata/document _metadata .csv` records each version with `effective_date`, `effective_to` and `superseded_by`.

---

## 4. Structured Signal to Knowledge Linkage

- **Credit_history_status = "NO_HISTORY":** Risk-tier policy
  
  - _Why it matters:_ Determines how applicants without sufficient credit history should be handled without incorrectly treating missing history as zero risk.
- **bankruptcy_last_7y_flag = TRUE joined to allow_bankruptcy_flag = FALSE on the same product_code:** Product eligibility grid in loan_product.csv Reg B counteroffer rules, 12 CFR 1002.9(a)(1)(iv)

  - _Why it matters:_ Determines whether the applicant is ineligible outright or should be moved to a product that permits bankruptcy. MTG-FH and AUT-SP both carry allow_bankruptcy_flag = TRUE with a +2.5% rate adjustment, which makes a counteroffer the correct action rather than a bare decline. A counteroffer carries its own 90-day notice obligation if the applicant does not accept. Without the product row retrieved alongside the applicant row, the system produces a decision that looks defensible but is wrong.

---

## 5. Controlled Quality Issues & Risk Matrix Summary

| Quality Problem | Examples           | Proposed Control                        | 
| :-------------- | :----------------------- | :-------------------------------- | 
| Unstructured Data | In `document _metadata .csv`, the ECOA, FCRA and CCPA rows carry an original effective date (2011-12-30 for Regulation B, 1971-04-25, 2020-01-01) while `version` names a 2026 edition, so a retrieval system could treat a years-old date as the date of the current text | Record the edition's own effective date separately from the original effective date, and review regulatory rows in the metadata audit |
| Structured Data | Format inconsistencies: dates are M/D/YYYY in loan_application.csv and applicant.csv but ISO in credit_pull_event.csv and applicant_risk_features.csv; money is stored as text (`"$147,346 "` in loan_application.csv, `"500,000"` in loan_product.csv), so amounts cannot be compared without parsing | Dataset contracts declare each column's type and input format; ingestion normalizes dates and money before any comparison |
| Structured Data | 71 applications are dated after the 2026-09-14 extract date but still carry a `preliminary_decision` | Ingestion quarantines rows dated after the extract date; the consistency checker confirms they have no final decision |

---

## 6. How to Run & Environment Setup

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check that the source data is consistent with itself and with the policies (68 checks):
   ```bash
   python src/validation/check_source_consistency.py
   ```
4. Build the DuckDB relational model and the quality reports (or run `notebooks/04_relational_model.ipynb`):
   ```bash
   python src/database/build_relational_model.py
   python src/database/generate_quality_reports.py
   ```
5. Only if the synthetic source data needs rebuilding (see `src/synthetic/README.md`):
   ```bash
   python src/synthetic/regenerate_source_data.py
   ```
