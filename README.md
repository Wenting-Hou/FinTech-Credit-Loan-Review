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
- **Business Function / Process:** The function is responsible for maximizing portfolio profitability and minimizing credit losses by establishing structured underwriting standards, executing data-driven loan decisioning, and ensuring absolute adherence to consumer protection and fair-lending regulations.
- **Target Stakeholders:** Underwriters, Credit Analysts, Chief Risk Officer, Credit Risk Committee,Compliance Team, Fair-Lending Team, Data Scientists, Loan Origination System (LOS) Engineers, FinTech Product Managers, Loan Officers, Applicants, Regulators, Credit Bureaus

- **Primary Decision Question:** Should this loan application be approved, denied, or escalated for manual review based on the applicant’s profile, product rules, credit information, and current compliance requirements?

- **Supporting Business Questions:**

1. Were loan decisions based on the underwriting and compliance rules that were current on the decision date?
2. Are approval, denial, and escalation outcomes consistent across regions and comparable risk tiers, or are there patterns that may indicate fair-lending concerns?
3. Which loan products and underwriting rules generate the most manual escalations or denials?

---

## 3. Microcosm Assets Overview

### Structured Operational Datasets (`data/structured/raw/`)

- `loan_application.csv` - [represents the primary applicant profile used in the loan review process, 600, application_id]
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
