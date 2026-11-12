# Entity Relationship Diagram (ERD)

<img width="1600" height="1600" alt="Fintech drawio (1)" src="https://github.com/user-attachments/assets/b82447ed-3fc4-4e8f-8e73-4106a57dd752" />

The image above predates the applicant table. The diagram below is the current model.

```mermaid
erDiagram
    APPLICANT ||--|{ LOAN_APPLICATION : submits
    LOAN_PRODUCT ||--o{ LOAN_APPLICATION : "is requested in"
    LOAN_APPLICATION ||--o{ CREDIT_PULL_EVENT : triggers
    LOAN_APPLICATION ||--|| APPLICANT_RISK_FEATURES : "is scored by"
    APPLICANT {
        string applicant_id PK
        string first_name
        string last_name
        date birth_date
        string state
    }
    LOAN_APPLICATION {
        string application_id PK
        string applicant_id FK
        string product_code FK
        date date
        string region_state
        int fico_score
        decimal dti_pct
        string preliminary_decision
        string final_decision
    }
    CREDIT_PULL_EVENT {
        string event_id PK
        string application_id FK
        date event_date
        int fico_score
        string event_status
    }
    APPLICANT_RISK_FEATURES {
        string application_id "PK, FK"
        string appli_risk_id UK
        date as_of_date
        string credit_history_status
        int risk_tier_score
        string risk_tier
    }
    LOAN_PRODUCT {
        string product_code PK
        string minimum_risk_tier
        int minimum_fico
        decimal maximum_amount_usd
        decimal max_dti_pct
    }
```

## Summary
The structured-data layer contains five datasets: Applicants, Loan Applications, Applicant Risk Features, Credit Pull Events, and Loan Products.

**0. Applicant to Application**

An applicant (person) can submit one or many applications, and each application has exactly one applicant. There are no co-applicants. If an applicant moves or changes details, they submit a new application, so each application keeps the state it was submitted from.
-  Relationship: 1 to 1..N (One-to-Many)
-  Key Link: applicant_id becomes a Foreign Key inside the Application table.

 
**1. Loan Product to Application**

A loan product can be selected by zero, one, or many applications. However, an individual application is typically submitted for exactly one specific loan product.
-  Relationship: 1 to 0..N (One-to-Many)
-  Key Link: product_code becomes a Foreign Key inside the Application table.

**2.  Application to Credit Pull Event**
 
 An application is submitted first, which triggers zero, one, or multiple Credit Pull Events (e.g., pulling from Equifax, Experian, or re-pulling due to delays). Each credit pull event is tied explicitly to that single application instance.
-  Relationship: 1 to 0..N (One-to-Many, Optional)
-  Key Link: application_id becomes a Foreign Key inside the Credit Pull Event table.

**3.  Application to Applicant Risk Features**

A loan application is submitted first, which generates exactly one associated applicant risk feature record to hold the evaluation metrics for that specific request. This single risk feature record is tied explicitly to that single application instance to preserve a point-in-time underwriting audit trail.
-  Relationship: 1 to 1 (One-to-One, Mandatory)
-  Key Link: application_id is both the primary key and a Foreign Key of the Applicant_Risk_Feature table (one row per application), and appli_risk_id is a unique surrogate identifier, as declared in applicant_risk_features.yaml.


Analytically, these datasets can be combined to evaluate applicant eligibility, examine credit-risk changes over time, compare applicant characteristics with product requirements, and create features for downstream analytical or machine-learning applications.
