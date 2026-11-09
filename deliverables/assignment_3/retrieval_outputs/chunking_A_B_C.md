# Chunking experiment (A3 section 2)

Same 6 policy files (ELIG-001 V1.0 and V2.0, RISK-TIER, PRODUCT-RISK, APPR-001, REG-001), same question, same embedding model and same top-K. Only the splitter changes. Sizes are in characters, as the n8n splitter counts them.

Environment: n8n 2.43 on a local laptop; Ollama with `nomic-embed-text` (embeddings) and `qwen2.5:14b` (context 8,192). Retrieve chunks: Simple Vector Store, Get Many, top-K 15. Build context keeps up to 6 chunks for the LLM. Workflow: [`n8n/RAG_Lab_guardrail_v2.json`](../n8n/RAG_Lab_guardrail_v2.json). Runs made 2026-11-09.

**Question:** How does RISK-TIER assign a risk tier to an applicant with no credit history, and which products take an applicant with no credit score?

**Expected evidence:** RISK-TIER "No Credit History" (tier T3, basis NO_CREDIT_HISTORY), and the rule naming MTG-FH, CRD-SC and AUT-SP (ELIG-001 section 4, or the PRODUCT-RISK tier overlay row).

| Setup | n8n splitter | Policy chunks (Simple Vector Store items) | Result |
|---|---|---|---|
| A | Recursive Character Text Splitter, 1,000 characters, 150 overlap | 81 | Tier part correct. Products guessed: the chunks naming MTG-FH, CRD-SC and AUT-SP ranked #10 and #12, past the 6-chunk limit. |
| B | Recursive Character Text Splitter, 500 characters, 75 overlap | 170 | Tier part correct. Products wrong and attributed to PRODUCT-RISK: the no-history rule was split into three chunks (#3, #5, #6), the overlay chunk (#4) lost the row that names the products, and the ELIG-001 no-score paragraph ranked #15. |
| C | Recursive Character Text Splitter, Markdown mode, 2,000 characters, 200 overlap | 46 | Both parts correct and complete. The whole PRODUCT-RISK tier overlay section (#1) and the whole RISK-TIER No Credit History section (#2) reached the LLM. |
| C0 | Character Text Splitter on `\n## ` (one chunk per section), up to 4,000 characters | none | Ingest failed in the Embeddings Ollama node: "the input length exceeds the context length". Some sections are about 10,700 characters, over nomic-embed-text's 2,048-token input limit in Ollama. A copy of the model with a larger num_ctx did not help. |

The 9 catalog rows from loan_product.csv are stored by a separate node (Simple Vector Store2) and are the same in every run.

Labels: **USED** = sent to the LLM; **DROPPED** = removed by the metadata filter, with the reason; **NOT USED** = applicable but past the 6-chunk limit. Chunk previews are the first 70 characters.

## Setup A: Recursive Character Text Splitter, 1,000 characters, 150 overlap (81 policy chunks)

**Answer (from the chat):**

> According to RISK-TIER V1.0, an applicant with no observable credit history during the 24-month lookback period is assigned a risk tier of T3, which is classified as Moderate Risk. This classification is based on the uncertainty caused by insufficient historical information rather than demonstrated delinquency. As for the products that accept applicants with no credit score, the eligibility rules defined in ELIG-001 V1.0 determine that a minimum risk tier is tested against the applicant's `risk_tier` as defined by RISK-TIER V1.0. Thus, products that permit applicants with no credit history would need to have a minimum risk tier that accommodates a T3 classification.
>
> Sources: RISK-TIER V1.0, ELIG-001 V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | RISK-TIER title and purpose | Partly relevant | defines the T1 to T5 tiers |
| 2 | RISK-TIER No Credit History | Directly relevant | the tier rule itself |
| 3 | RISK-TIER Established Credit History | Irrelevant | a different history class |
| 4 | PRODUCT-RISK review cycle | Irrelevant | not about eligibility |
| 5 | RISK-TIER risk score calculation | Irrelevant | scoring is skipped for no history |
| 6 | ELIG-001 V1.0 gate definitions | Partly relevant | how the tier gate is tested, but no products |

**Important evidence missing:** The rule naming MTG-FH, CRD-SC and AUT-SP (ELIG-001 V1.0 section 4 at #12, PRODUCT-RISK overlay row at #10) did not reach the AI.

**Retrieved evidence (top 15 by similarity, judged as of 2026-11-09):**

```text
1. USED RISK-TIER V1.0, score 0.82: "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
2. USED RISK-TIER V1.0, score 0.82: "## Special Credit History Rules ### No Credit History Applicants with ..."
3. USED RISK-TIER V1.0, score 0.81: "### Established Credit History Applicants with at least six months of ..."
4. USED PRODUCT-RISK V1.0, score 0.806: "- Review this matrix at least annually and after material term, exposu..."
5. USED RISK-TIER V1.0, score 0.798: "For applicants eligible for standard scoring: **Risk Score = Delinquen..."
6. USED ELIG-001 V1.0, score 0.786: "- Minimum risk tier is tested against the applicant's `risk_tier` ..."
7. DROPPED ELIG-001 V2.0, score 0.786 (not yet in force on 2026-11-09): "- Minimum risk tier is tested against the applicant's `risk_tier` ..."
8. NOT USED RISK-TIER V1.0, score 0.777 (in force, but over the 6-chunk limit): "### Applicant Financial Information * Annual income ### Credit History..."
9. NOT USED RISK-TIER V1.0, score 0.763 (in force, but over the 6-chunk limit): "## Policy Output The risk-classification process should produce, at mi..."
10. NOT USED PRODUCT-RISK V1.0, score 0.762 (in force, but over the 6-chunk limit): "| Applicant tier / history | Proposed treatment across all nine produc..."
11. NOT USED RISK-TIER V1.0, score 0.757 (in force, but over the 6-chunk limit): "The methodology is designed solely for this academic microcosm. The th..."
12. NOT USED ELIG-001 V1.0, score 0.751 (in force, but over the 6-chunk limit): "Applicants with no credit score (NO_HISTORY): `MTG-FH`, `CRD-SC` a..."
13. DROPPED ELIG-001 V2.0, score 0.751 (not yet in force on 2026-11-09): "Applicants with no credit score (NO_HISTORY): `MTG-FH`, `CRD-SC` a..."
14. NOT USED RISK-TIER V1.0, score 0.744 (in force, but over the 6-chunk limit): "| Observed Credit History | Classification | | -----------------------..."
15. NOT USED PRODUCT-RISK V1.0, score 0.729 (in force, but over the 6-chunk limit): "# Product Risk Management Policy Policy ID: PRODUCT-RISK **Version..."
```

## Setup B: Recursive Character Text Splitter, 500 characters, 75 overlap (170 policy chunks)

**Answer (from the chat):**

> RISK-TIER V1.0 assigns applicants with no observable credit history during the 24-month lookback period a risk tier of T3, which indicates a Moderate Risk classification. For products, the eligibility rules are determined by PRODUCT-RISK V1.0, but specific product names are not substitutes for the applicant's calculated T1-T5 risk tier. Therefore, products that accept applicants with no credit score must be identified by their ability to accommodate a T3 risk tier applicant rather than relying on a specific product name like “Elite” or “Subprime.”
>
> Sources: RISK-TIER V1.0, PRODUCT-RISK V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | RISK-TIER Established Credit History | Irrelevant | a different history class |
| 2 | PRODUCT-RISK purpose | Partly relevant | says tier and eligibility are separate |
| 3 | RISK-TIER NO_HISTORY is T3 | Directly relevant | part of the tier rule |
| 4 | PRODUCT-RISK overlay intro | Partly relevant | heading without the row that names the products |
| 5 | RISK-TIER uncertainty sentence | Directly relevant | part of the tier rule |
| 6 | RISK-TIER No Credit History heading | Directly relevant | part of the tier rule |

**Important evidence missing:** The product rule: ELIG-001 V1.0 section 4 ranked #15 and the overlay's NO_HISTORY row was not in the top 15.

**Retrieved evidence (top 15 by similarity, judged as of 2026-11-09):**

```text
1. USED RISK-TIER V1.0, score 0.837: "### Established Credit History Applicants with at least six months of ..."
2. USED PRODUCT-RISK V1.0, score 0.828: "Applicant credit risk, product eligibility, and product risk are separ..."
3. USED RISK-TIER V1.0, score 0.819: "Applicants with NO_HISTORY are assigned T3 - Moderate Risk rat..."
4. USED PRODUCT-RISK V1.0, score 0.817: "## 3. Applicant-tier overlay The applicant tier in this overlay, and t..."
5. USED RISK-TIER V1.0, score 0.813: "This classification reflects uncertainty caused by insufficient histor..."
6. USED RISK-TIER V1.0, score 0.813: "## Special Credit History Rules ### No Credit History Applicants with ..."
7. NOT USED RISK-TIER V1.0, score 0.796 (in force, but over the 6-chunk limit): "## Policy Purpose This policy establishes a standardized methodology f..."
8. NOT USED ELIG-001 V1.0, score 0.79 (in force, but over the 6-chunk limit): "- Minimum risk tier is tested against the applicant's `risk_tier` ..."
9. DROPPED ELIG-001 V2.0, score 0.79 (not yet in force on 2026-11-09): "- Minimum risk tier is tested against the applicant's `risk_tier` ..."
10. NOT USED RISK-TIER V1.0, score 0.789 (in force, but over the 6-chunk limit): "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
11. NOT USED APPR-001 V1.0, score 0.781 (in force, but over the 6-chunk limit): "6. Applicant risk tier routing applies first. T4 applicants go to ..."
12. NOT USED RISK-TIER V1.0, score 0.77 (in force, but over the 6-chunk limit): "Information generated after the application date, including subsequent..."
13. NOT USED RISK-TIER V1.0, score 0.768 (in force, but over the 6-chunk limit): "The following information must not be used in calculating the risk tie..."
14. NOT USED RISK-TIER V1.0, score 0.766 (in force, but over the 6-chunk limit): "## Risk Score Calculation For applicants eligible for standard scoring..."
15. NOT USED ELIG-001 V1.0, score 0.766 (in force, but over the 6-chunk limit): "Applicants with no credit score (NO_HISTORY): `MTG-FH`, `CRD-SC` a..."
```

## Setup C: Recursive Character Text Splitter, Markdown mode, 2,000 characters, 200 overlap (46 policy chunks)

**Answer (from the chat):**

> RISK-TIER assigns applicants with no credit history a risk tier of T3, classified as Moderate Risk, with the risk tier basis set to NO_CREDIT_HISTORY. According to the policy, applicants with no observable credit history within the 24-month lookback period are automatically assigned this tier without calculating a numeric risk score. Products that can accommodate applicants with no credit score include MTG-FH, CRD-SC, and AUT-SP, as these products have the `allow_no_score_flag` set to TRUE. These products require a documented manual assessment of repayment evidence, such as verified income, reserves, or down payment, and non-traditional credit history like rent and utility payments.
>
> Sources: RISK-TIER V1.0, PRODUCT-RISK V1.0

**Classification of the chunks sent to the AI** (judged by reading the text, not by score):

| Rank | Chunk | Classification | Why |
|---|---|---|---|
| 1 | PRODUCT-RISK tier overlay (whole section) | Directly relevant | its NO_HISTORY row names MTG-FH, CRD-SC and AUT-SP |
| 2 | RISK-TIER No Credit History (whole section) | Directly relevant | the tier rule and basis |
| 3 | RISK-TIER title and purpose | Partly relevant | defines the tiers |
| 4 | RISK-TIER risk score calculation | Partly relevant | shows scoring is skipped |
| 5 | RISK-TIER policy output | Partly relevant | lists risk_tier_basis |
| 6 | RISK-TIER credit history classification | Partly relevant | defines NO_HISTORY |

**Important evidence missing:** None for the answer. ELIG-001 section 4, the owning rule, did not reach the AI; the same facts arrived through the PRODUCT-RISK overlay.

**Retrieved evidence (top 15 by similarity, judged as of 2026-11-09):**

```text
1. USED PRODUCT-RISK V1.0, score 0.829: "3. Applicant-tier overlay The applicant tier in this overlay, and the ..."
2. USED RISK-TIER V1.0, score 0.81: "Special Credit History Rules ### No Credit History Applicants with no ..."
3. USED RISK-TIER V1.0, score 0.806: "# Applicant Credit Risk Classification Policy Policy ID: RISK-TIER..."
4. USED RISK-TIER V1.0, score 0.79: "Risk Score Calculation For applicants eligible for standard scoring: *..."
5. USED RISK-TIER V1.0, score 0.773: "Policy Output The risk-classification process should produce, at minim..."
6. USED RISK-TIER V1.0, score 0.763: "Credit History Classification Before calculating a risk score, the app..."
7. NOT USED RISK-TIER V1.0, score 0.749 (in force, but over the 6-chunk limit): "Prohibited Risk Factors The following information must not be used in ..."
8. NOT USED PRODUCT-RISK V1.0, score 0.706 (in force, but over the 6-chunk limit): "1. Purpose and scope This policy defines how product features and lend..."
9. NOT USED loan_product.csv V1.0 CRD-EL, score 0.705 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
10. NOT USED loan_product.csv V1.0 CRD-ST, score 0.701 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
11. NOT USED APPR-001 V1.0, score 0.697 (in force, but over the 6-chunk limit): "1. General Escalation Principles 1. **Automated/system decision first...."
12. NOT USED loan_product.csv V1.0 CRD-SC, score 0.696 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
13. NOT USED ELIG-001 V1.0, score 0.694 (in force, but over the 6-chunk limit): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V1.0 ..."
14. DROPPED ELIG-001 V2.0, score 0.694 (not yet in force on 2026-11-09): "# Product Eligibility Rules Policy ID: ELIG-001 Version: V2.0 ..."
15. NOT USED loan_product.csv V1.0 MTG-CV, score 0.673 (in force, but over the 6-chunk limit): "[loan_product.csv | catalog for ELIG-001 V1.0 | in force 2024-01-01 to..."
```
