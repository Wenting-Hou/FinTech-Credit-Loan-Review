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
2. Which product requirements, such as minimum credit tier, FICO, DTI, loan amount, bankruptcy, and collections rules, affect applicant eligibility?
3. Which lending and compliance documents apply when reviewing the application?


---

## 3. Microcosm Assets Overview

### Structured Operational Datasets (`data/structured/raw/`)

- `loan_application.csv` - [represents the primary applicant profile used in the loan review process, 600, application_id]
- `applicant_risk_features.csv` - [the applicant’s credit-risk profile at the time of each loan application, 600, application_id]
- `loan_product.csv` - [defines the available loan products and their associated eligibility, risk, and pricing requirements, 9, product_code]
- `credit_pull_event.csv` - [represents the applicant’s historical credit-related events and changes over time, 1835, event_id & applicant_id]

### Knowledge Corpus (`data/documents/source/`)

- Contains **14** total documents (**3** PDFs, **6** TXT/MD files, **5** YAML).
- Includes structural challenges (tables, hierarchical headers) and version state diversity (e.g., Current vs. Superseded).

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
| Unstructured Data | enterprise_risk_policy.md states that tiering rules are in risk_policy.md, but the actual filename is applicant_risk_policy.md | Create a document registry that maps “Policy ID” in the metadata headers to the respective filenames |
| Unstructured Data | applicant_risk_policy.md has an effective date of September 1st, 2026, which is prior to its “prepared” date of September 10th, 2026.         | Require a standardized metadata header on every document | 
| Structured Data      | Format inconsistencies across loan_application.csv and credit_pull_events.csv Dates: M/D/YYYY vs ISO Booleans: TRUE vs Trueloan_product.csv stores maximum_amount_usd as a string, so can’t be compared to request_amount_usd in loan_application.csv | Write a schema contract that fixes types and formats for each column | 

---

## 6. How to Run & Environment Setup

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
