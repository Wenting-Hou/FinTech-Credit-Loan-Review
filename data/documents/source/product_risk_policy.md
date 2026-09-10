# Product Risk Management Policy

**Policy ID:** PRODUCT-RISK  
**Version:** V1.0  
**Status:** active  
**Prepared:** September 10, 2026  
**Proposed owner:** Quality & Governance Lead: Wenting Hou  
**Proposed approver:** Credit Risk Committee  
**Review cycle:** Annually and following a material product or policy change

## 1. Purpose and scope

This policy defines how product features and lending structures affect risk and what controls are required for Mortgage, Credit Card, and Auto Loan products in the project microcosm. It covers application review, product changes, and portfolio monitoring.

Applicant credit risk, product eligibility, and product risk are separate assessments. A low-risk applicant does not automatically qualify for every product. Collateral or a security deposit does not automatically establish repayment capacity. Product names such as “Elite” or “Subprime” are not substitutes for an applicant's calculated T1–T5 risk tier.

This document is a supporting policy under the proposed `enterprise_risk_policy.md` (ERM-001). 
New controls and routing rules below are project design assumptions, not existing approved rules or real lender requirements. 
Numerical eligibility criteria remain in the eligibility document and require the validation already identified there.

### 1.1 Approved-scope catalog for this draft

The scope contains exactly the following nine products

| Product code | Product name | Product family | Catalog summary |
|---|---|---|---|
| MTG-FH | Mortgage FHA | Mortgage | Owner-occupied property; documented income |
| MTG-CV | Mortgage Conventional | Mortgage | Income and employment verification required |
| MTG-JB | Mortgage Jumbo | Mortgage | High-balance loan; reserves required |
| CRD-SC | Credit Card Secured | Credit Card | Security deposit required |
| CRD-ST | Credit Card Standard | Credit Card | Standard unsecured revolving credit card |
| CRD-EL | Credit Card Elite 720+ | Credit Card | Premium rewards product |
| AUT-SP | Auto Loan Subprime | Auto Loan | Vehicle collateral required |
| AUT-TR | Auto Loan Traditional | Auto Loan | Standard auto financing |
| AUT-TT | Auto Loan Top-Tier | Auto Loan | Preferred borrower program |


## 2. Product-specific risks and controls

The following controls supplement the eligibility rules. They do not create new FICO, DTI, LTV, amount or term thresholds.

| Product | Principal risk drivers | Proposed required controls | Additional review trigger |
|---|---|---|---|
| Mortgage FHA — `MTG-FH` | Small borrower equity; repayment stress; program and insurance conditions | Verify repayment capacity, down-payment source, occupancy, valuation and applicable program/insurance conditions | Compensating factors required; non-traditional history; unresolved program or property issue |
| Mortgage Conventional — `MTG-CV` | Repayment stress; collateral shortfall; investor eligibility | Verify income, payment DTI, valuation, applicable loan limit, and mortgage-insurance conditions where relevant | DTI/LTV exception; appraisal concern; uncertain investor eligibility |
| Mortgage Jumbo — `MTG-JB` | Large individual exposure; property concentration; collateral liquidity | Verify reserves, income stability, independent valuation and total borrower exposure | Senior Underwriter / Underwriting Manager review under existing procedures; higher-level routing for exposure or policy exceptions |
| Credit Card Secured — `CRD-SC` | Repayment failure; deposit shortfall; fraud; deposit administration errors | Verify repayment capacity and cleared deposit; reconcile deposit coverage against the authorized limit; review before deposit release or unsecured conversion | Deposit discrepancy; proposed unsecured conversion; proposed limit above deposit coverage |
| Credit Card Standard — `CRD-ST` | Unsecured loss; revolving exposure growth; promotional payment changes | Verify repayment capacity and limit; assess existing exposure; document promotional and subsequent payment terms | Borderline eligibility; derogatory history; limit above standard authority |
| Credit Card Elite 720+ — `CRD-EL` | Larger unsecured exposure; concentration; rapid utilization growth | Verify repayment capacity and aggregate exposure; assess utilization evidence; apply delegated limit authority | High exposure; limit above authority; exception to qualification criteria |
| Auto Loan Subprime — `AUT-SP` | Repayment stress; negative equity; depreciation; dealer/add-on risk | Verify income, vehicle value and condition, financed add-ons, insurance and lien readiness | Layered repayment/collateral risks; LTV/term exception; dealer-requested waiver |
| Auto Loan Traditional — `AUT-TR` | Depreciation; collateral/documentation defects; repayment stress | Verify payment DTI, LTV, vehicle age/mileage, insurance and title/lien documentation | Vehicle outside eligibility; DTI/LTV exception; missing funding documentation |
| Auto Loan Top-Tier — `AUT-TT` | Collateral loss despite strong credit; incentive or pricing errors | Verify collateral, term, repayment capacity and incentive conditions; retain insurance and lien controls | Unverified incentive; term/LTV exception; collateral or documentation defect |

Fraud and sanctions concerns follow the dedicated cross-product routes in `approval_escalation_procedures.md`. They must not be resolved through an ordinary credit exception.

### 2.1 Product risk assessment method

This assessment evaluates the product offering, not an individual borrower or application. 
Rate each risk dimension separately using the scale below. 
The assessment considers the designed product and intended delivery model before relying on evidence that operating controls work. 

| Rating | Qualitative assessment basis |
|---|---|
| Low (L) | Limited plausible impact and low likelihood under documented exposure and delivery assumptions; simple, transparent design |
| Moderate (M) | Meaningful potential loss, disruption or customer harm, or recurring exposure requiring active controls |
| High (H) | Potentially severe impact, elevated likelihood, or material complexity/exposure under the stated assumptions; focused oversight required |
| Not assessed (NA) | Evidence or assumptions are insufficient for a defensible assessment; this is not a low-risk result |

Document **likelihood, impact and rationale** for each dimension. For example, either severe impact or elevated likelihood may justify High. 

Term Definition: 
- **Credit loss:** Repayment failure and potential loss after considering exposure structure and uncertainty in recovery.
- **Fraud:** Identity, application, transaction and intermediary fraud exposure.
- **Operational:** Processing, collateral/deposit administration, servicing and third-party complexity.
- **Compliance:** Complexity and consequences of meeting applicable product requirements and treating customers fairly. A rating does not establish any particular legal obligation.
- **Funding:** Funding commitments, exposure duration, liquidity and repricing uncertainty under the assumed product design.

### 2.2 Initial product risk assessment matrix 

These starting assessments use catalog characteristics plus the explicitly illustrative structures in the existing eligibility draft. 
They must be reviewed when actual product terms, limits, channels, volumes and control evidence become available. 


| Product code | Credit loss | Fraud | Operational | Compliance | Funding | Basis for provisional profile |
|---|---|---|---|---|---|---|
| MTG-FH | H | M | H | H | H | Assumed small down payments and long duration; property, occupancy and program/insurance administration add complexity |
| MTG-CV | M | M | H | H | H | Assumed collateralized repayment structure; property/investor documentation and long-duration funding remain material |
| MTG-JB | H | M | H | H | H | Catalog specifies high balance and reserves; large exposure, valuation complexity and assumed long duration increase risk |
| CRD-SC | M | M | H | H | M | Deposit is required but coverage and enforceability are unverified; collection, reconciliation and release add operational risk |
| CRD-ST | H | M | M | H | M | Catalog identifies unsecured revolving credit; losses and changing utilization require attention |
| CRD-EL | H | M | H | H | H | Assumed larger unsecured limits create funding commitments; premium rewards add administration complexity |
| AUT-SP | H | M | H | M | M | Assumed higher LTV/longer terms and dealer/add-on exposure; vehicle depreciation can weaken recovery |
| AUT-TR | M | M | M | M | M | Vehicle-backed financing with recurring valuation, repayment, title and servicing risks |
| AUT-TT | M | M | M | M | M | Preferred borrower positioning does not eliminate depreciation, lien, pricing or repayment risks |

Note: 
- A uniform fraud rating reflects the absence of channel-specific evidence, not proof of equivalent fraud rates.
- The absence of M/L entries reflects conservative initial assumptions, not a conclusion that no product could qualify as Low after assessment.
- Ratings are not a ranking of products' observed default rates.

### 2.3 Control evidence and residual risk matrix

Residual risk is the remaining risk after considering evidence of control design and operation. 

| Product code | Priority controls to evidence | Proposed evidence for review | Control effectiveness | Residual risk | Proposed assessment owner |
|---|---|---|---|---|---|
| MTG-FH | Repayment, occupancy, down-payment and program/insurance checks | Completed review records, valuation and condition-closure evidence | Not verified | NA | Mortgage owner + Credit Risk |
| MTG-CV | Income, payment DTI, valuation and investor eligibility | Verified inputs, calculation records and exception/insurance checks where relevant | Not verified | NA | Mortgage owner + Credit Risk |
| MTG-JB | Reserves, independent valuation and borrower exposure limits | Reserve verification, valuation review and exposure report | Not verified | NA | Mortgage owner + Credit Risk |
| CRD-SC | Deposit clearance, coverage reconciliation and release restrictions | Deposit ledger reconciliation, limit checks and release approvals | Not verified | NA | Card owner + Operations |
| CRD-ST | Repayment assessment, limit authority and revolving exposure monitoring | Income assessment, limit approvals and utilization reports | Not verified | NA | Card owner + Credit Risk |
| CRD-EL | Aggregate exposure, delegated limits, funding and rewards controls | Exposure/funding review, limit approvals and rewards reconciliation | Not verified | NA | Card owner + Credit Risk / Finance |
| AUT-SP | Income, LTV/add-ons, dealer oversight, insurance and lien checks | Verified inputs, valuation, dealer review and title exception reports | Not verified | NA | Auto Loan owner + Credit Risk |
| AUT-TR | Payment DTI, collateral eligibility, insurance and lien processing | Calculation records, vehicle checks and funding-condition closure | Not verified | NA | Auto Loan owner + Operations |
| AUT-TT | Collateral, term, incentive/pricing and lien controls | Valuation, approved terms, incentive validation where used and lien evidence | Not verified | NA | Auto Loan owner + Operations |

- The residual_risk column is a summary placeholder. 
- When completed, retain residual L/M/H assessments for each of the five dimensions. 
- Document the evidence reviewed, effectiveness conclusion, rationale, assessor, independent reviewer, assessment date and next review date. 
- Any unassessed dimension keeps the summary NA while retaining known High flags for escalation.
- Control effectiveness is recorded as **Effective**, **Partially effective**, **Ineffective**, or **Not verified**,
  with evidence and assessment scope.
- Credit Risk coordinates the review, Compliance reviews compliance,
  Operations reviews operational controls, and Finance reviews funding assumptions.
- Owners must be named before adoption.

### 2.4 Assessment outcomes and review requirements

- Initial High dimensions require focused assessment and an action plan. They do not automatically disqualify the product or its applicants.
- Residual High requires documented acceptance within enterprise appetite and delegated authority,
   or remediation before new launch/material expansion. Report matters to the governing body.
- NA means the assessment is incomplete.
  For a new launch or material expansion, complete required assessment and controls before release.
  For an existing product, refer to Risk for documented interim restrictions or suspension under the enterprise policy;
  do not silently treat NA as acceptable.

     
- Review this matrix at least annually and after material term, exposure, channel, legal, funding or control changes, or significant incidents.
- Product ratings inform oversight, controls and limits.
  Individual applications continue through eligibility and approval procedures. Never add these ratings to the applicant T1–T5 score.

## 3. Applicant-tier overlay

| Applicant tier / history | Proposed treatment across all nine products |
|---|---|
| T1–T2 | Follow the normal product route if every other requirement is met; product-specific mandatory reviews still apply |
| T3 with established history | Follow the normal product route, checking repayment capacity and any additional product triggers |
| T3 with NO_HISTORY | Require documented manual assessment of available repayment evidence; retain the NO_HISTORY basis and null numeric score |
| Any tier with LIMITED_HISTORY | Record the limited-history flag and require manual review of evidence sufficiency |
| T4 | Require the relevant senior product reviewer: Senior Underwriter / Underwriting Manager for mortgages, Underwriting Supervisor for cards, Underwriting Manager for auto |
| T5 | Refer to the Credit Risk Committee for assessment within its confirmed authority; no automatic approval or decline solely from this draft |

Application rules:
- Where multiple triggers apply, use the highest applicable review level.  
- Fraud/sanctions routing takes priority. 
- A referral is not approval, and a favorable risk tier does not override a failed eligibility requirement.
  

## 4. Decision sequence and records
Decision sequence:  
1. Resolve product code, relevant jurisdiction and policy versions. Check identity/fraud controls and required data.
2. Derive the applicant tier using the application-date methodology.
3. Evaluate product eligibility and validated jurisdiction requirements separately.
4. Apply product controls and the adopted tier overlay. Record every failed, pending or exception rule.
5. Route to the authority defined in the approval procedures. Complete required conditions before funding or card activation.

Records requirements:  
- Keep the product risk assessment result separate from the final lending decision.
- Suggested assessment results are **CONTROLS_MET**, **REVIEW_REQUIRED**, **DATA_HOLD**, and **REQUIREMENT_NOT_MET**. CONTROLS_MET does not itself mean the loan is approved. If several conditions apply, retain all flags and prevent release until blocking issues are resolved.
- Exceptions must identify the exact rule, justification, compensating evidence, approving authority, conditions and decision timestamp.
- Missing delegated authority is grounds for referral, not assumed permission.

## 5. Portfolio monitoring and product changes

Monthly monitoring by the product owner and Credit Risk, quarterly committee review, and immediate escalation of material control failures.

| Coverage | Measures to review |
|---|---|
| All products | Exposure, delinquency, losses, exception frequency, concentration, complaints, fraud and data completeness |
| Mortgages | LTV and payment-DTI distributions, large borrower exposures, valuation issues and property concentrations |
| Cards | Authorized limits, drawn balances, utilization, deposit coverage for secured cards and losses following limit increases |
| Auto | LTV and term distributions, vehicle/dealer concentrations, lien defects, repossessions and recovery shortfalls |

Before a new product or material change to limits, terms, pricing structure, eligibility, collateral or distribution channel, 
document the risk assessment, operational readiness, Compliance review, approval, implementation checks and monitoring plan. 
Record who may suspend new originations and who may authorize resumption. 

Note: The authorities remain to be assigned. In this policy version, all authorizations remain with the Board.


## 6. Reference
For an external governance reference, [OCC Bulletin 2017-43: New, Modified, or Expanded Bank Products and Services](https://www.occ.treas.gov/news-issuances/bulletins/2017/bulletin-2017-43.html) 
describes due diligence and approval, policies and controls, change management, and ongoing monitoring for new activities. 
It supports the lifecycle structure used here; it does not prescribe these filenames, the project's nine products, or the proposed tier overlay. 

