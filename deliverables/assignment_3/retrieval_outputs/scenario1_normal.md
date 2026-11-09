# Scenario 1: Normal

Final setup C: Recursive Character Text Splitter in Markdown mode, 2,000 characters, 200 overlap. `FILTER_BY_METADATA = true` unless stated otherwise.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** For CRD-EL, what are the minimum applicant risk tier and FICO, maximum payment DTI and amount, and bankruptcy/collections permissions?

**Expected (written before the run):** CRD-EL catalog row and ELIG-001 V1.0 Catalog Gates (V1.0 is in force today). Exclude ELIG-001 V2.0 and other products' catalog rows.

**Result:** Correct: T2, FICO 720, payment DTI 45%, $50,000, no bankruptcy, no collections. Other products' rows (#2, #3) and V2.0 chunks (#4, #8) were dropped; 5 chunks reached the LLM.

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

**Answer (from the chat):**

> For the CRD-EL product, the minimum applicant risk tier is T2, and the minimum FICO score is 720. The maximum payment debt-to-income (DTI) ratio is 45%, and the maximum credit limit is $50,000. Bankruptcy within the past 7 years and collections within the past 12 months are not permitted.
>
> Sources: ELIG-001 V1.0, loan_product.csv, PRODUCT-RISK V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | CRD-EL catalog row | Directly relevant | all six gates |
| 5 | ELIG-001 V1.0 credit card section | Partly relevant | card limits and notes |
| 6 | ELIG-001 V1.0 Catalog Gates | Directly relevant | the gates table and definitions |
| 7 | PRODUCT-RISK tier overlay | Partly relevant | how tiers are applied |
| 14 | PRODUCT-RISK purpose and scope | Irrelevant | not about CRD-EL gates |

**Important evidence missing:** None.

**Retrieved evidence (top 15 by similarity, judged as of 2026-11-09):**

```text
1. USED loan_product.csv V1.0 CRD-EL, score 0.858: "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
2. DROPPED loan_product.csv V1.0 CRD-SC, score 0.824 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
3. DROPPED loan_product.csv V1.0 CRD-ST, score 0.821 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
4. DROPPED ELIG-001 V2.0, score 0.784 (not yet in force on 2026-11-09): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
5. USED ELIG-001 V1.0, score 0.771: "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
6. USED ELIG-001 V1.0, score 0.753: "Catalog Gates (system of record: loan_product.csv) | Code | Minimum ..."
7. USED PRODUCT-RISK V1.0, score 0.747: "3. Applicant-tier overlay The applicant tier in this overlay, and the ..."
8. DROPPED ELIG-001 V2.0, score 0.743 (not yet in force on 2026-11-09): "Catalog Gates, V2.0 (system of record: loan_product.csv from January..."
9. DROPPED loan_product.csv V1.0 MTG-FH, score 0.737 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
10. DROPPED loan_product.csv V1.0 AUT-TR, score 0.733 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
11. DROPPED loan_product.csv V1.0 AUT-TT, score 0.731 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
12. DROPPED loan_product.csv V1.0 MTG-CV, score 0.729 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
13. DROPPED loan_product.csv V1.0 AUT-SP, score 0.728 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
14. USED PRODUCT-RISK V1.0, score 0.726: "1. Purpose and scope This policy defines how product features and lend..."
15. DROPPED loan_product.csv V1.0 MTG-JB, score 0.716 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
```
