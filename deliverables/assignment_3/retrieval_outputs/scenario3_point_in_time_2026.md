# Scenario 3: Point-in-Time, application dated 2026-10-15 (V1.0 in force; also the section 4D after run)

Final setup C: Recursive Character Text Splitter in Markdown mode, 2,000 characters, 200 overlap. `FILTER_BY_METADATA = true` unless stated otherwise.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** Can an applicant with risk tier T2, FICO 740, payment DTI 42%, $30,000 requested, no bankruptcy and no collections qualify for the Elite card? Application date 2026-10-15.

**Expected (written before the run):** ELIG-001 V1.0 and the CRD-EL catalog row. Exclude every V2.0 chunk and other products' rows.

**Result:** Correct: meets all six V1.0 gates. 0 of the 5 chunks sent were inapplicable, and the ELIG-001 V1.0 card section (#7) was used.

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

**Answer (from the chat):**

> The applicant can qualify for the Elite card (CRD-EL) as they meet all the catalog gates for this product. The applicant's risk tier T2, FICO score of 740, payment DTI of 42%, requested amount of $30,000, and the absence of bankruptcy and collections all comply with the product requirements. According to the gate results, the applicant passes the minimum risk tier, minimum FICO score, payment DTI, credit limit, bankruptcy history, and collections history gates.
>
> Sources: ELIG-001 V1.0, loan_product.csv, PRODUCT-RISK V1.0, RISK-TIER V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | CRD-EL catalog row | Directly relevant | all six V1.0 gates |
| 4 | PRODUCT-RISK tier overlay | Partly relevant | how tiers are applied |
| 5 | RISK-TIER title and purpose | Partly relevant | defines tier order |
| 7 | ELIG-001 V1.0 credit card section | Directly relevant | the Elite card rules in force |
| 12 | ELIG-001 V1.0 title | Partly relevant | version and effective date |

**Important evidence missing:** None.

**Retrieved evidence (top 15 by similarity, judged as of 2026-10-15):**

```text
1. USED loan_product.csv V1.0 CRD-EL, score 0.804: "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
2. DROPPED loan_product.csv V1.0 CRD-ST, score 0.762 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
3. DROPPED loan_product.csv V1.0 CRD-SC, score 0.756 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
4. USED PRODUCT-RISK V1.0, score 0.739: "3. Applicant-tier overlay The applicant tier in this overlay, and the ..."
5. USED RISK-TIER V1.0, score 0.731: "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
6. DROPPED ELIG-001 V2.0, score 0.729 (not yet in force on 2026-10-15): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
7. USED ELIG-001 V1.0, score 0.725: "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
8. DROPPED loan_product.csv V1.0 MTG-FH, score 0.718 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
9. DROPPED loan_product.csv V1.0 AUT-TR, score 0.718 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
10. DROPPED loan_product.csv V1.0 AUT-TT, score 0.717 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
11. DROPPED ELIG-001 V2.0, score 0.715 (not yet in force on 2026-10-15): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V2.0 ..."
12. USED ELIG-001 V1.0, score 0.713: "# Product Eligibility Rules Policy ID: ELIG-001 Version: V1.0 ..."
13. DROPPED loan_product.csv V1.0 MTG-CV, score 0.708 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
14. DROPPED loan_product.csv V1.0 AUT-SP, score 0.706 (catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
15. DROPPED ELIG-001 V2.0, score 0.703 (not yet in force on 2026-10-15): "Catalog Gates, V2.0 (system of record: `loan_product.csv` from January..."
```
