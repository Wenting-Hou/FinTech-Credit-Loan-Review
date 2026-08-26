# DSBA 6171: [Domain Name] Data & Knowledge Microcosm

## 1. Team Information & Roles
* **Team Number / Name:** [e.g., Team 01 - FinTech]
* **Team Lead / Liaison:** [Student Name]
* **Data & Ingestion Lead:** [Student Name]
* **Database & Analytics Lead:** [Student Name]
* **Knowledge & Retrieval Lead:** [Student Name]
* **Quality & Governance Lead:** [Student Name]

---

## 2. Business Context & Problem Framing
* **Assigned Domain:** [FinTech: Credit & Loan Review | HealthTech: Medical Claims & Payer Auditing]
* **Business Function / Process:** [e.g., Streamlining credit review & compliance audit]
* **Target Stakeholders:** [e.g., Underwriting officers, Compliance auditors]
* **Primary Decision Question:** [Insert primary decision question]
* **Supporting Business Questions:**
  1. [Supporting question 1]
  2. [Supporting question 2]
  3. [Supporting question 3]

---

## 3. Microcosm Assets Overview

### Structured Operational Datasets (`data/structured/raw/`)
* `file_1.csv` - [Brief description, row count, primary key]
* `file_2.csv` - [Brief description, row count, primary key]
* `file_3.csv` - [Brief description, row count, primary key & foreign keys]

### Knowledge Corpus (`data/documents/source/`)
* Contains **[X]** total documents (**[Y]** PDFs, **[Z]** TXT/MD files).
* Includes structural challenges (tables, hierarchical headers) and version state diversity (e.g., Current vs. Superseded).

---

## 4. Structured Signal to Knowledge Linkage
* **Signal Example 1:** [Structured Field / Event] -> [Policy Document ID]
  * *Why it matters:* [Explanation of business impact]
* **Signal Example 2:** [Structured Field / Event] -> [Policy Document ID]
  * *Why it matters:* [Explanation of business impact]

---

## 5. Controlled Quality Issues & Risk Matrix Summary
| Quality Problem | Affected Layer | AI Impact | Business Consequence | Future Control |
| :--- | :--- | :--- | :--- | :--- |
| [Issue 1] | Ingestion / Vector Store | Incorrect context retrieve | Flawed decisioning | Deduplication gate |
| [Issue 2] | Knowledge Corpus | Hallucination on superseded rules | Compliance failure | Authority filter |
| [Issue 3] | Data Quality | Null keys during join | Partial analytics | Schema contract |

---

## 6. How to Run & Environment Setup
1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
