# Improvement, before: Scenario 3 dated 2026-10-15 with the metadata filter OFF (section 4D)

Final setup C: Recursive Character Text Splitter in Markdown mode, 2,000 characters, 200 overlap. `FILTER_BY_METADATA` set to false for this run.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** Can an applicant with risk tier T2, FICO 740, payment DTI 42%, $30,000 requested, no bankruptcy and no collections qualify for the Elite card? Application date 2026-10-15.

**Expected (written before the run):** ELIG-001 V1.0 and the CRD-EL catalog row. Exclude every V2.0 chunk (in force from 2027-01-01) and other products' rows.

**Result:** Answer correct (meets all six V1.0 gates), but 3 of the 6 chunks sent to the LLM did not apply: CRD-ST (#2), CRD-SC (#3) and the ELIG-001 V2.0 card section (#6), which outscored its V1.0 twin (#7, cut off) 0.729 to 0.725. In filter-off mode, chunks past the 6-chunk limit are labelled "in force" even when the filter would drop them: other products' rows (#8 to #10, #13, #14) and V2.0 (#11, #15). None of them were sent to the LLM.

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

**Answer (from the chat):**

> The applicant meets the eligibility criteria for the Elite card (CRD-EL). The applicant's risk tier T2 and FICO score of 740, payment debt-to-income ratio of 42%, requested amount of $30,000, and lack of bankruptcy and collections all comply with the catalog gates defined for the Elite card as of the application date of 2026-10-15. Therefore, the applicant passes all the necessary catalog gates and qualifies for the Elite card.
>
> Sources: ELIG-001 V1.0, loan_product.csv

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | CRD-EL catalog row | Directly relevant | all six V1.0 gates |
| 2 | CRD-ST catalog row | Irrelevant | another product, which this applicant would pass |
| 3 | CRD-SC catalog row | Irrelevant | another product, which this applicant would pass |
| 4 | PRODUCT-RISK tier overlay | Partly relevant | how tiers are applied |
| 5 | RISK-TIER title and purpose | Partly relevant | defines tier order |
| 6 | ELIG-001 V2.0 credit card section | Irrelevant | not in force until 2027; contradicts V1.0 |

**Important evidence missing:** The ELIG-001 V1.0 credit card section (#7) was cut by its V2.0 twin.

**Retrieved evidence (top 15 by similarity, judged as of 2026-10-15; METADATA FILTER OFF):**

```text
1. USED loan_product.csv V1.0 CRD-EL, score 0.804: "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
2. USED loan_product.csv V1.0 CRD-ST, score 0.762 (filter off; would be dropped: catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
3. USED loan_product.csv V1.0 CRD-SC, score 0.756 (filter off; would be dropped: catalog row for another product): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
4. USED PRODUCT-RISK V1.0, score 0.739: "3. Applicant-tier overlay The applicant tier in this overlay, and the ..."
5. USED RISK-TIER V1.0, score 0.731: "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
6. USED ELIG-001 V2.0, score 0.729 (filter off; would be dropped: not yet in force on 2026-10-15): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
7. NOT USED ELIG-001 V1.0, score 0.725 (in force, but over the 6-chunk limit): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
8. NOT USED loan_product.csv V1.0 MTG-FH, score 0.718 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
9. NOT USED loan_product.csv V1.0 AUT-TR, score 0.718 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
10. NOT USED loan_product.csv V1.0 AUT-TT, score 0.717 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
11. NOT USED ELIG-001 V2.0, score 0.715 (in force, but over the 6-chunk limit): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V2.0 ..."
12. NOT USED ELIG-001 V1.0, score 0.713 (in force, but over the 6-chunk limit): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V1.0 ..."
13. NOT USED loan_product.csv V1.0 MTG-CV, score 0.708 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
14. NOT USED loan_product.csv V1.0 AUT-SP, score 0.706 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
15. NOT USED ELIG-001 V2.0, score 0.703 (in force, but over the 6-chunk limit): "Catalog Gates, V2.0 (system of record: `loan_product.csv` from January..."
```
