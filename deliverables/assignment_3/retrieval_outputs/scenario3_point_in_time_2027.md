# Scenario 3: Point-in-Time, application dated 2027-02-01 (V2.0 in force)

Final setup C: Recursive Character Text Splitter in Markdown mode, 2,000 characters, 200 overlap. `FILTER_BY_METADATA = true` unless stated otherwise.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** Can an applicant with risk tier T2, FICO 740, payment DTI 42%, $30,000 requested, no bankruptcy and no collections qualify for the Elite card? Application date 2027-02-01.

**Expected (written before the run):** ELIG-001 V2.0. Exclude every V1.0 chunk and the V1.0 catalog rows.

**Result:** Correct: not eligible under V2.0, fails tier (T2 vs T1), FICO (740 vs 760), payment DTI (42% vs 40%) and credit limit ($30,000 vs $25,000). All V1.0 rows and sections were dropped as superseded; the V2.0 Catalog Gates table (#15) was used.

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

**Answer (from the chat):**

> The applicant with risk tier T2, FICO 740, payment DTI 42%, requesting $30,000, and no recent bankruptcy or collections does not qualify for the Elite card (CRD-EL) on 2027-02-01. The applicant fails the catalog gates for minimum risk tier (T2 is riskier than the required T1), minimum FICO (740 is lower than the required 760), maximum payment DTI (42% exceeds the 40% limit), and maximum credit limit ($30,000 exceeds the $25,000 limit). Only the bankruptcy and collections gates are passed, which are not sufficient for eligibility.
>
> Sources: ELIG-001 V2.0, PRODUCT-RISK V1.0, RISK-TIER V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 4 | PRODUCT-RISK tier overlay | Partly relevant | how tiers are applied |
| 5 | ELIG-001 V2.0 credit card section | Directly relevant | the Elite card rules in force |
| 6 | RISK-TIER title and purpose | Partly relevant | defines tier order |
| 11 | ELIG-001 V2.0 title | Partly relevant | version, effective date, which version applies |
| 15 | ELIG-001 V2.0 Catalog Gates | Directly relevant | the V2.0 gates |

**Important evidence missing:** None.

**Retrieved evidence (top 15 by similarity, judged as of 2027-02-01):**

```text
1. DROPPED loan_product.csv V1.0 CRD-EL, score 0.804 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
2. DROPPED loan_product.csv V1.0 CRD-ST, score 0.762 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
3. DROPPED loan_product.csv V1.0 CRD-SC, score 0.757 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
4. USED PRODUCT-RISK V1.0, score 0.741: "3. Applicant-tier overlay The applicant tier in this overlay, and the ..."
5. USED ELIG-001 V2.0, score 0.731: "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
6. USED RISK-TIER V1.0, score 0.729: "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
7. DROPPED ELIG-001 V1.0, score 0.724 (superseded before 2027-02-01): "2. Credit Card | Product level | Code | Min. Credit Score | Income Req..."
8. DROPPED loan_product.csv V1.0 AUT-TR, score 0.718 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
9. DROPPED loan_product.csv V1.0 MTG-FH, score 0.718 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
10. DROPPED loan_product.csv V1.0 AUT-TT, score 0.718 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
11. USED ELIG-001 V2.0, score 0.716: "# Product Eligibility Rules Policy ID: ELIG-001 Version: V2.0 ..."
12. DROPPED ELIG-001 V1.0, score 0.714 (superseded before 2027-02-01): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V1.0 ..."
13. DROPPED loan_product.csv V1.0 MTG-CV, score 0.709 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
14. DROPPED loan_product.csv V1.0 AUT-SP, score 0.707 (superseded before 2027-02-01): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
15. USED ELIG-001 V2.0, score 0.706: "Catalog Gates, V2.0 (system of record: loan_product.csv from January..."
```
