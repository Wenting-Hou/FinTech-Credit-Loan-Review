# DSBA 6171: FinTech Credit & Loan Review Data & Knowledge Microcosm

## 1. Team Information & Roles

- **Team Number / Name:** Team 03 - FinTech
- **Team Lead / Liaison:** Tim Goncharov
- **Data & Ingestion Lead:** Evan De Guzman
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

- Contains **[X]** total documents (**[Y]** PDFs, **[Z]** TXT/MD files).
- Includes structural challenges (tables, hierarchical headers) and version state diversity (e.g., Current vs. Superseded).

---

## 4. Structured Signal to Knowledge Linkage

- **Signal Example 1:** [Structured Field / Event] -> [Policy Document ID]
  - _Why it matters:_ [Explanation of business impact]
- **Signal Example 2:** [Structured Field / Event] -> [Policy Document ID]
  - _Why it matters:_ [Explanation of business impact]

---

## 5. Controlled Quality Issues & Risk Matrix Summary

| Quality Problem | Affected Layer           | AI Impact                         | Business Consequence | Future Control     |
| :-------------- | :----------------------- | :-------------------------------- | :------------------- | :----------------- |
| [Issue 1]       | Ingestion / Vector Store | Incorrect context retrieve        | Flawed decisioning   | Deduplication gate |
| [Issue 2]       | Knowledge Corpus         | Hallucination on superseded rules | Compliance failure   | Authority filter   |
| [Issue 3]       | Data Quality             | Null keys during join             | Partial analytics    | Schema contract    |

---

## 6. How to Run & Environment Setup

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
