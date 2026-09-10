# Enterprise Risk Management Policy

**Policy ID:** ERM-001  
**Version:** V1.0  
**Status:** active  
**Prepared:** September 10, 2026   
**Proposed owner:** Head of Risk 
**Proposed approver:** Board 
**Review cycle:** At least annually and following material changes

## 1. Purpose

This policy establishes the enterprise-wide framework for identifying, assessing, controlling, monitoring and 
reporting risks arising from the business. 
It governs the supporting applicant risk, product eligibility, product risk, approval and 
geographic requirements documents without duplicating their detailed rules.

The enterprise shall pursue lending objectives within approved risk appetite, maintain clear accountability 
and ensure decisions can be explained and reproduced from dated evidence.
Meeting a credit-score threshold or product eligibility rule alone does not constitute final approval.

This is a synthetic policy for the academic project. 
Roles, approval arrangements, and controls introduced here are proposed project assumptions. 


## 2. Scope and product catalog

This framework applies to product design, origination, underwriting, approval, funding or 
card activation, servicing, collections, portfolio oversight, supporting technology, data and third parties. 
Functions outside the available project data remain governance requirements to be implemented or explicitly scoped by the governing body

| Product code | Product name | Product family |
|---|---|---|
| MTG-FH | Mortgage FHA | Mortgage |
| MTG-CV | Mortgage Conventional | Mortgage |
| MTG-JB | Mortgage Jumbo | Mortgage |
| CRD-SC | Credit Card Secured | Credit Card |
| CRD-ST | Credit Card Standard | Credit Card |
| CRD-EL | Credit Card Elite 720+ | Credit Card |
| AUT-SP | Auto Loan Subprime | Auto Loan |
| AUT-TR | Auto Loan Traditional | Auto Loan |
| AUT-TT | Auto Loan Top-Tier | Auto Loan |


## 3. Policy hierarchy and rule ownership

Applicable law and binding contractual requirements constrain internal policy. 

Within the internal framework, this policy establishes governance and boundaries. 
Supporting documents own their respective detailed rules and procedures.

| Supporting document | Subject it owns | Required alignment with this policy |
|---|---|---|
| `risk_policy.md` | Applicant risk factors, lookback, score, T1–T5 classification and missing-data rules | Reproducibility, approved changes, input restrictions and independent review |
| `product_eligibility_rules.md` | Product qualification, numerical criteria, amounts, terms and collateral requirements | Clear authoritative rules, validated sources and controlled exceptions |
| `product_risk_policy.md` | Product risk drivers, safeguards, additional review and monitoring | Enterprise appetite, aggregate exposure and product change governance |
| `approval_escalation_procedures.md` | Lending authority, referrals and exception decisions | Documented delegation, separation of duties and escalation beyond authority |
| `regional_state_lending_requirements.md` | Geographic requirements reference | Compliance ownership, source validation and effective-date control |

Note: Drafts do not override effective policies. 
If effective requirements conflict, hold the affected action and obtain documented resolution from the relevant owners, 
with Risk and Compliance involvement where appropriate. 
Do not select the more permissive rule or assume a newer draft is authoritative.

This policy does not itself change applicant scoring, numerical eligibility thresholds or existing lending authority. 

## 4. Governance and accountability

| Proposed role | Accountability |
|---|---|
| Board / project governing body | Approve this framework, enterprise appetite and material changes; oversee aggregate risk and unresolved material breaches |
| Senior management / project sponsor | Implement the framework, allocate resources and assign named owners and delegated authority |
| Head of Risk / risk lead | Maintain the risk register and appetite schedule; independently challenge assessments; consolidate reporting and escalate breaches |
| Credit Risk Committee | Exercise lending and exception authority expressly delegated to it; review credit concentrations and material product risks; refer enterprise matters outside its mandate |
| Product owners, underwriting and operations | Own risks and controls in their activities; retain evidence; identify incidents and remediate deficiencies |
| Compliance / designated compliance reviewer | Validate applicable requirements; oversee conduct, disclosure and fair-treatment controls; advise on legal conflicts and specialist referrals |
| Finance / designated finance lead | Assess funding, liquidity, interest-rate exposure and capacity to absorb losses, proportionate to the project scope |
| Technology, data and model owners | Maintain access, data quality, change control, resilience and model/rule documentation |
| Internal Audit / independent project reviewer | Assess governance and control effectiveness independently of control operation and approval |


## 5. Enterprise risk appetite

Definition: Risk appetite means the types and amount of risk the enterprise is willing to accept in pursuing its objectives, 
within its financial and operational capacity. 
Limits translate appetite into measurable boundaries; early-warning thresholds trigger action before a boundary is breached.

The proposed qualitative appetite is to:

- Accept assessed credit risk where repayment capacity, product fit and exposure are supported by evidence and approved rules.
- Keep borrower, product, channel and other relevant concentrations within approved limits.
- Maintain funding, loss-absorption capacity and operational resources appropriate to existing and committed exposures.
- Permit controlled innovation only after assessment, approval and implementation checks.
- Prohibit deliberate rule circumvention, unauthorized approvals, falsified evidence and knowing violations of applicable requirements. This prohibition does not imply that incidents cannot occur; detected incidents require containment and remediation.

The governing body shall approve a dated appetite and limits schedule. 

| Area | Minimum measures to define | Proposed accountable owner |
|---|---|---|
| Credit and concentration | Delinquency and loss rates; borrower/group exposure; product and channel concentration; card drawn and undrawn commitments | Risk and Finance |
| Exceptions | Exception frequency, size, duration, repeat exceptions and overdue conditions | Credit Risk |
| Liquidity and financial capacity | Funding availability, stressed cash needs, maturity mismatch and loss capacity | Finance |
| Operations and technology | Material incidents, downtime, recovery objectives, control failures and third-party dependency | Operations / Technology |
| Data and decision models | Missing critical inputs, rule execution errors, overrides and performance deterioration | Data / Model owner with Risk |
| Compliance and customer treatment | Complaints, substantiated violations, disclosure failures and remediation progress | Compliance |

A missing required limit must be recorded as a governance gap.
Activity dependent on that limit must not proceed automatically or be treated as unlimited; 
it requires a documented interim boundary approved by the governing body or remains on hold.

## 6. Risk identification and assessment

Maintain an enterprise risk register covering the following categories and their interactions:

| Risk category | Risk items | Minimum response |
|---|---|---|
| Credit and collateral | Repayment failure, valuation shortfall, weak collateral recovery | Repayment assessment, collateral verification and portfolio review |
| Product and concentration | Layered risk, large jumbo exposures, dealer dependence, rapid card growth | Product assessment and aggregate exposure limits |
| Liquidity, interest-rate and financial risk | Funding shortfall, repricing mismatch, losses exceeding resources | Cash-flow and rate scenarios, funding and financial-capacity review |
| Operational and third-party | Processing errors, title defects, servicing failures, vendor outage | Documented controls, reconciliation, vendor oversight and continuity plans |
| Technology, cyber and privacy | Unauthorized access, data loss, system disruption | Access controls, secure handling, recovery and incident response |
| Data, model and automated decision | Missing inputs, outcome leakage, unsupported thresholds, incorrect rule execution | Data lineage, validation, version control and review of overrides |
| Compliance, fraud and customer conduct | Identity fraud, unlawful treatment, inaccurate disclosures or decisions | Specialist review, validated requirements and complaint handling |
| Strategic and business | Unsupported expansion, inadequate staffing, unsustainable economics | Business-case review and assessment against capacity and appetite |


## 7. Minimum control requirements

### Lending decisions

Apply applicant classification, product eligibility, product controls and applicable geographic requirements as separate checks. Use only approved versions and retain supporting evidence. Verify relevant conditions before funding or activation. Follow the approval procedures for final decisions and exceptions.

### Data and automated decisions

Do not feed subsequent approvals, approved amounts, outcomes or later credit events into the original applicant score. 
Subsequent outcomes may support separately dated monitoring.

Do not confuse total outstanding debt divided by annual income, used in the applicant risk policy, 
with monthly debt payments divided by monthly income used for product payment DTI. 
Define inputs and treatment of missing values before implementation.   

Unknown information is not zero, and an incomplete extract is not confirmed NO_HISTORY.

Maintain source lineage, calculation definitions, rule versions and change records. 
Check implementations against approved rules and representative boundary cases before release.

An automated or AI-assisted system shall not invent policy, 
resolve ambiguous thresholds through inference or authorize exceptions beyond delegated authority. 
Route unresolved cases to an authorized reviewer.

### Customer, fraud and compliance controls

- Apply approved criteria consistently. 
- Use restricted or sensitive information only for authorized purposes. 
- Applicant scoring retains its existing prohibited-input rules. 
- Review complaints and potential unfair treatment. 
- Jurisdictional information used for compliance does not become an applicant score factor.
- Suspected fraud or sanctions issues follow dedicated specialist escalation.
They must not be waived through a standard credit exception.
- Compliance determines any required notices, reporting and timing under validated applicable requirements.

### Operational safeguards

Use proportionate access controls, reconciliations, change approvals, backup and recovery arrangements, third-party due diligence and incident logging. Assign ownership for servicing and collections controls even where the project presently models origination only.

## 8. Product and material change approval

Before introducing or materially changing a product, channel, underwriting rule, model, provider or system, the owner shall document:

1. Business purpose, affected customers and products, and expected financial and operational effects.
2. Credit, compliance, data, technology, third-party and aggregate risk assessment.
3. Alignment with appetite, limits and applicable requirements.
4. Required controls, resources, implementation checks and responsible owners.
5. Approval under documented delegation, release conditions, rollback or suspension arrangements and post-release monitoring.

Obtain Risk review and relevant Compliance, Finance and Technology review before release. 
Changes to enterprise appetite or this policy require governing-body approval. 
Product or lending changes follow delegated authority. Material unresolved control failures block release.

## 9. Breaches, incidents and exceptions

A breach is a failure to meet an effective rule or limit. An exception is a documented request for a permitted departure; approval must be obtained before the departure and must not disguise an existing breach.

| Event | Required proposed response |
|---|---|
| Missing evidence, ambiguous rule or unresolved document conflict | Hold the affected decision; refer to the relevant owner and record the resolution |
| Early-warning threshold reached | Notify the metric owner and Risk; investigate and establish corrective action before a limit is exceeded |
| Limit breach or unauthorized approval | Promptly notify Risk and management; contain further exposure; document impact and remediation |
| Suspected fraud, sanctions issue or material data/security incident | Immediately use the specialist response route and contain the affected activity |
| Material or repeated breach, or issue beyond management authority | Escalate to the governing body with impact, actions and a recommendation |

Log every material event, including detection time, affected records, affected customers, exposure, owner, 
containment, reporting assessment, root cause, due date and closure evidence.   

Risk shall challenge material closure decisions. 
An independent reviewer shall confirm closure where the owner caused or approved the deficient control.

Permitted exceptions require a rule reference, justification, compensating controls, residual risk, 
named approver, scope and expiry. 
There is no internal exception to applicable law or binding external requirements. 
Repeated exceptions require policy review, not automatic renewal.
The lending committee cannot waive enterprise requirements outside its delegated mandate.

The governing body shall designate suspension and restart authorities before adoption. 
Restart requires evidence that blocking issues are resolved and approval at the authorized level. 
This draft establishes no automatic right to resume.

## 10. Monitoring and assurance

- Operational owners monitor controls as activity requires.
- Risk compiles a monthly dashboard.   
*Note:* The dashboard shall show exposures, appetite and limit status, trends, exceptions, data limitations, 
incidents, complaints, overdue actions and decisions needed.   
Report unavailable metrics as unavailable, not as zero.
- Management and the governing body review enterprise risk at least quarterly.
- Material events are escalated when detected rather than waiting for periodic reporting.
- At least annually assess plausible scenarios.   
*Including:* reduced borrower income, property or vehicle value declines, increased card utilization, 
funding pressure and a critical provider outage.   
*Documentation:* assumptions, affected products, aggregate consequences, limitations and management responses. 
- Independent assurance shall periodically review policy implementation, rule execution, access, decisions and remediation according to a risk-based plan.


## 11. Source reference

External governance reference: [OCC Comptroller's Handbook: Corporate and Risk Governance](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/corporate-risk-governance/index-corporate-and-risk-governance.html), accessed September 10, 2026. 
The OCC overview addresses governance responsibilities and oversight across multiple banking risk categories.
It informs the broad framework only. It does not prescribe these policies' filenames, proposed roles, or synthetic lending rules. 
Applicability to a real institution would require separate assessment.
