# Scenario 3: Point-in-Time, application dated 2023-11-01 (before any policy)

Final setup C: Recursive Character Text Splitter in Markdown mode, 2,000 characters, 200 overlap. `FILTER_BY_METADATA = true` unless stated otherwise.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** Which policy was authoritative for a CRD-EL application dated 2023-11-01, and can its eligibility be determined from the current corpus?

**Expected (written before the run):** Nothing: no ELIG-001 version was in force on 2023-11-01.

**Result:** Correct: all 15 retrieved chunks were dropped as not yet in force, and the guardrail returned a fixed reply (route to manual review).

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

**Answer (from the chat):**

> No eligibility policy was in force on 2023-11-01. According to document _metadata .csv, the earliest version of the eligibility rules (ELIG-001 V1.0) takes effect on 2024-01-01, so it cannot be applied to this application. Eligibility cannot be determined from the current corpus, and the case should be routed to manual review.
>
> Sources: document _metadata .csv

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

**Important evidence missing:** Not applicable: no policy was in force, so nothing should reach the AI.

**Retrieved evidence (top 15 by similarity, judged as of 2023-11-01):**

```text
1. DROPPED loan_product.csv V1.0 CRD-EL, score 0.774 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
2. DROPPED loan_product.csv V1.0 CRD-SC, score 0.75 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
3. DROPPED ELIG-001 V2.0, score 0.749 (not yet in force on 2023-11-01): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V2.0 ..."
4. DROPPED loan_product.csv V1.0 CRD-ST, score 0.745 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
5. DROPPED ELIG-001 V1.0, score 0.743 (not yet in force on 2023-11-01): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V1.0 ..."
6. DROPPED ELIG-001 V2.0, score 0.742 (not yet in force on 2023-11-01): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
7. DROPPED ELIG-001 V1.0, score 0.726 (not yet in force on 2023-11-01): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
8. DROPPED ELIG-001 V2.0, score 0.697 (not yet in force on 2023-11-01): "Product Code Reference | Product Line | Product level | Product Code (..."
9. DROPPED PRODUCT-RISK V1.0, score 0.694 (not yet in force on 2023-11-01): "1. Purpose and scope This policy defines how product features and lend..."
10. DROPPED RISK-TIER V1.0, score 0.682 (not yet in force on 2023-11-01): "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
11. DROPPED loan_product.csv V1.0 AUT-TR, score 0.674 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
12. DROPPED loan_product.csv V1.0 AUT-SP, score 0.667 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
13. DROPPED RISK-TIER V1.0, score 0.667 (not yet in force on 2023-11-01): "Special Credit History Rules ### No Credit History Applicants with no ..."
14. DROPPED loan_product.csv V1.0 MTG-CV, score 0.666 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
15. DROPPED loan_product.csv V1.0 AUT-TT, score 0.664 (not yet in force on 2023-11-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
```
