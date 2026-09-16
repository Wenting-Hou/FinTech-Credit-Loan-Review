# Entity Relationship Diagram (ERD)

<img width="1600" height="1600" alt="Fintech drawio (1)" src="https://github.com/user-attachments/assets/b82447ed-3fc4-4e8f-8e73-4106a57dd752" />

## Summary
The structured-data layer contains four primary datasets: Loan Applications, Applicant Risk Features, Credit Pull Events, and Loan Products.

 
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
-  Key Link: Application_ID becomes a Foreign Key with a UNIQUE constraint inside the Applicant_Risk_Feature table, alongside its own independent surrogate primary key (Risk_Feature_ID).


Analytically, these datasets can be combined to evaluate applicant eligibility, examine credit-risk changes over time, compare applicant characteristics with product requirements, and create features for downstream analytical or machine-learning applications.
