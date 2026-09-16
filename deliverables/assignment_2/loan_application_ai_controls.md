# AI Context / Quality Controls — `loan_application.csv`

**Dataset ID:** `fintech.origination.loan_application`
**Schema version:** `1.0.0` · **Contract version:** `1.0.0`
**Owner role:** Knowledge & Retrieval Lead
**Last updated:** 2026-09-14

Three controls governing what an AI consumer receives from this dataset. Each addresses a failure that **passes schema validation** — the row is well-formed and the value is correct, but the meaning does not survive the trip into a prompt.

| ID | Control | Failure class |
|---|---|---|
| `C-01` | Point-in-time integrity | Temporal / contextual correctness |
| `C-02` | Semantic disambiguation | Semantic meaning |
| `C-03` | Decision-state qualification | Semantic meaning + compliance |

---

## C-01 — Point-in-time integrity

| | |
|---|---|
| **Rule / Expectation** | Every field in a row is as-of `date`. All joins to event data filter `event_date <= date`. Future-dated rows are handled by an explicit, documented decision. |
| **What Goes Wrong** | 71 of 600 rows are dated after the 2026-09-14 extract, running to 2026-12-31. Credit-pull joins written without a date filter pull events that post-date the application. |
| **What AI Receives** | A row carrying no as-of marker, which reads as settled history, and features containing facts generated after the decision it is being asked to explain. |
| **Possible AI Impact** | Answers in the past tense about applications that have not happened. Target leakage inflates model accuracy against a future the model was shown. Volume and approval-rate metrics are silently wrong in either direction, depending on whether the pipeline dropped the future rows or counted them. |
| **Control / Response** | Stamp `as_of` and `temporal_status` (`FUTURE_DATED` where applicable) on every chunk. Enforce `event_date <= date` as a join predicate, not a convention. Assert `MAX(date)` against the extract date at load; route exceptions to the data owner rather than filtering silently. |

Contract references: `point_in_time_semantics.no_lookahead_rule`, `BI-05`. Validation: `V-023`.

---

## C-02 — Semantic disambiguation

| | |
|---|---|
| **Rule / Expectation** | `credit_risk_tier` and `dti_pct` carry file-specific definitions and must never be merged, substituted, or reconciled with same-named fields in other datasets. |
| **What Goes Wrong** | `credit_risk_tier` is a deterministic FICO band and agrees with `applicant_risk_features.risk_tier` — the policy tier under `RISK-TIER` v1.0 — on only 28% of applicants. `dti_pct` is a percent bounded 8.2–59.8; `debt_to_income_ratio` is an unbounded debt-stock ratio of 0.115–2.376. Both pairs share a name and, in the tier case, a value domain. |
| **What AI Receives** | Two retrieved chunks using the same field name with different values, and nothing in either one indicating which definition applies or which source governs. |
| **Possible AI Impact** | Contradictory answers to "what is this applicant's tier / DTI". Invented reconciliation between the two figures — most commonly multiplying the ratio by 100 and presenting it as the percent. A wrong tier carried into eligibility reasoning, where it changes which products the applicant appears to qualify for. |
| **Control / Response** | Rename at ingest: `app_credit_risk_tier`, `policy_risk_tier`, `payment_dti_pct`. Carry the definition and the source document in chunk metadata, not only in the contract. Report the tier disagreement rate on every load and alert on material movement. |

Contract references: `source_of_truth.not_authoritative_for`, `BI-02`, `BI-06`. Validation: `V-024`.

---

## C-03 — Decision-state qualification

| | |
|---|---|
| **Rule / Expectation** | `preliminary_decision` is a preliminary routing state. Every rendering of it carries the stage, the fact that no final decision exists, and the meaning of `Review`. |
| **What Goes Wrong** | The bare value is emitted into a chunk. `Review` — 310 of 600 rows, 52% — reads as pending or as a soft rejection. `Declined` reads as a final adverse action. |
| **What AI Receives** | "Preliminary decision: Review" or "Preliminary decision: Declined", with no stage, no next action, and no indication that the final outcome is not captured anywhere in the corpus. |
| **Possible AI Impact** | Tells a user their loan was rejected when it was routed to an underwriter — an adverse-action misstatement with ECOA accuracy exposure. Approval rate computed as 216/(216+74) = 77%, discarding the majority of applications from the denominator. |
| **Control / Response** | Template the decision with `stage`, `is_terminal = false`, and `next_action`. Block chunks where the value appears without the qualifier. Require metric definitions to treat `Review` as a third state rather than folding it into either outcome. |

Contract references: `decision.meaning`, `BI-01`, `BI-10`. Policy: `approval_escalation_procedures.md`.

---

## Notes

These three are the controls that need enforcement in the pipeline. Two further interpretation rules in the semantic contract are compliance obligations rather than pipeline controls, and belong in review rather than in code:

- `military_scra_flag` must never be used as a risk input or segmentation variable (`BI-07`).
- `requested_amount_usd` must never be aggregated as originated volume or exposure (`BI-04`).

**Related artifacts:** `loan_application_schema_expectations.md` · `loan_application_semantic_contract.json` · `loan_application_schema_summary.docx` (§6)
