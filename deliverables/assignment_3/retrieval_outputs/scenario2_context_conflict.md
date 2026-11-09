# Scenario 2: Context Conflict

Final setup C: Recursive Character Text Splitter in Markdown mode, 2,000 characters, 200 overlap. `FILTER_BY_METADATA = true` unless stated otherwise.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** Can an applicant with risk tier T3, FICO 700, payment DTI 44%, debt burden ratio 80%, $12,000 requested, and no bankruptcy or collections qualify for CRD-EL?

**Expected (written before the run):** CRD-EL gates and the gate definitions (payment DTI is dti_pct, not debt_burden_ratio). Exclude the CRD-SC and CRD-ST rows, which this applicant would pass.

**Result:** Correct: not eligible, fails minimum risk tier (T3 vs T2) and minimum FICO (700 vs 720); DTI read as 44%. CRD-SC and CRD-ST (#2, #3) were dropped.

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

**Answer (from the chat):**

> The applicant cannot qualify for the CRD-EL product because they fail the minimum risk tier and minimum FICO score requirements. The applicant's risk tier is T3, which is riskier than the required T2, and their FICO score of 700 is lower than the required minimum of 720. Although the applicant meets the payment DTI and requested amount limits and has no recent bankruptcy or collections, these satisfactory metrics do not compensate for the failed gates.
>
> Sources: ELIG-001 V1.0, RISK-TIER V1.0, PRODUCT-RISK V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | CRD-EL catalog row | Directly relevant | all six gates |
| 5 | ELIG-001 V1.0 credit card section | Partly relevant | card context |
| 6 | PRODUCT-RISK tier overlay | Partly relevant | how tiers are applied |
| 7 | ELIG-001 V1.0 Catalog Gates | Directly relevant | gates plus the rule that DTI means dti_pct |
| 13 | RISK-TIER title and purpose | Partly relevant | defines tier order, T1 best |
| 14 | ELIG-001 V1.0 title | Partly relevant | version and effective date |

**Important evidence missing:** None.

**Retrieved evidence (top 15 by similarity, judged as of 2026-11-09):**

```text
1. USED loan_product.csv V1.0 CRD-EL, score 0.833: "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
2. DROPPED loan_product.csv V1.0 CRD-SC, score 0.797 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
3. DROPPED loan_product.csv V1.0 CRD-ST, score 0.795 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
4. DROPPED ELIG-001 V2.0, score 0.783 (not yet in force on 2026-11-09): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
5. USED ELIG-001 V1.0, score 0.772: "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
6. USED PRODUCT-RISK V1.0, score 0.729: "3. Applicant-tier overlay The applicant tier in this overlay, and the ..."
7. USED ELIG-001 V1.0, score 0.718: "Catalog Gates (system of record: loan_product.csv) | Code | Minimum ..."
8. DROPPED loan_product.csv V1.0 MTG-FH, score 0.71 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
9. DROPPED loan_product.csv V1.0 AUT-TR, score 0.71 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
10. DROPPED ELIG-001 V2.0, score 0.708 (not yet in force on 2026-11-09): "Catalog Gates, V2.0 (system of record: loan_product.csv from January..."
11. DROPPED loan_product.csv V1.0 MTG-CV, score 0.707 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
12. DROPPED loan_product.csv V1.0 AUT-TT, score 0.701 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
13. USED RISK-TIER V1.0, score 0.7: "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
14. USED ELIG-001 V1.0, score 0.699: "# Product Eligibility Rules Policy ID: ELIG-001 Version: V1.0 ..."
15. DROPPED loan_product.csv V1.0 AUT-SP, score 0.696 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
```
