# Assignment 3: Knowledge Storage & Retrieval Architecture (Team 03)

Supporting artifacts for the A3 report. The report itself is the 3-page PDF submitted on Canvas.

| Path | What it is |
|---|---|
| [`architecture/Team03_A3_Architecture.png`](architecture/Team03_A3_Architecture.png) | Architecture diagram: the seven A3 stages and the n8n node that implements each part (SVG alongside) |
| [`n8n/RAG_Lab_guardrail_v2.json`](n8n/RAG_Lab_guardrail_v2.json) | The n8n workflow used for every run (credential IDs removed) |
| [`n8n/workflow_canvas.png`](n8n/workflow_canvas.png) | Screenshot of the workflow in n8n after the final ingest (46 policy chunks, 9 catalog rows) |
| [`chunks/sample_chunks.md`](chunks/sample_chunks.md) | Representative chunks with their metadata |
| [`retrieval_outputs/chunking_A_B_C.md`](retrieval_outputs/chunking_A_B_C.md) | Chunking experiment: three splitter setups, chunk counts, top-15 evidence, classification and answers |
| [`retrieval_outputs/scenario1_normal.md`](retrieval_outputs/scenario1_normal.md) | Scenario 1, Normal |
| [`retrieval_outputs/scenario2_context_conflict.md`](retrieval_outputs/scenario2_context_conflict.md) | Scenario 2, Context Conflict |
| [`retrieval_outputs/scenario3_point_in_time_2026.md`](retrieval_outputs/scenario3_point_in_time_2026.md) | Scenario 3, Point-in-Time 2026-10-15 (V1.0 in force); also the section 4D after run |
| [`retrieval_outputs/scenario3_point_in_time_2027.md`](retrieval_outputs/scenario3_point_in_time_2027.md) | Scenario 3, Point-in-Time 2027-02-01 (V2.0 in force) |
| [`retrieval_outputs/scenario3_point_in_time_2023.md`](retrieval_outputs/scenario3_point_in_time_2023.md) | Scenario 3, Point-in-Time 2023-11-01 (no policy in force) |
| [`retrieval_outputs/improvement_before_filter_off.md`](retrieval_outputs/improvement_before_filter_off.md) | Section 4D before run: the 2026 question with the metadata filter off |

**Selected documents** (in [`data/documents/source/`](../../data/documents/source/)): `product_eligibility_rules.md` (ELIG-001 V1.0, in force 2024-01-01 to 2026-12-31), `product_eligibility_rules_v2.md` (ELIG-001 V2.0, from 2027-01-01), `applicant_risk_policy.md` (RISK-TIER), `product_risk_policy.md` (PRODUCT-RISK), `approval_escalation_procedures.md` (APPR-001), `regional_state_lending_requirements.md` (REG-001), plus [`data/structured/raw/loan_product.csv`](../../data/structured/raw/loan_product.csv) as the system of record for the gates. Versions and dates come from [`metadata/document _metadata .csv`](../../metadata/).

## How the workflow works

- **Ingest** (manual trigger): Files list reads the document metadata and loads every version of the five policies from GitHub; the Recursive Character Text Splitter (Markdown mode, 2,000 characters, 200 overlap) cuts them into chunks that carry doc_id, source_file, version, effective_date and effective_to; Product rows writes one sentence per catalog product. Everything is embedded with nomic-embed-text into a Simple Vector Store (in memory).
- **Query** (chat): Guardrail (Code) finds the product (code or plain name), the application date, the ELIG-001 version in force and its gates, reads the applicant's inputs, computes the six gate results, and asks for anything missing. Retrieve chunks returns the top 15 by similarity. Build context labels each chunk with its version and dates, drops chunks not in force on the application date and catalog rows for other products, and sends up to 6 to a Basic LLM Chain (qwen2.5:14b). Every reply ends with the retrieved list marked USED, DROPPED or NOT USED.
- **Before/after switch:** `FILTER_BY_METADATA` at the top of the Build context node. `false` sends the top 6 by similarity only.

## How to rerun

1. Install Ollama and pull `nomic-embed-text` and `qwen2.5:14b`. Run n8n locally (tested on n8n 2.43, Node 24).
2. In n8n, import `n8n/RAG_Lab_guardrail_v2.json`, then select an Ollama credential (Base URL `http://127.0.0.1:11434`) in the four Ollama nodes.
3. Run the ingest flow once ("Execute workflow"). The vector store is in memory, so repeat after a restart.
4. Open the chat and ask the questions in the files under `retrieval_outputs/`. Each file also classifies every chunk sent to the AI as directly relevant, partly relevant or irrelevant, and notes any important evidence that was missing.
