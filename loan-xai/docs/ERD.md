# Entity-Relationship Diagram (ERD)
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

---

## Database Entity-Relationship Model (Mermaid)

```mermaid
erDiagram
    APPLICATION ||--|| DECISION : "results in"
    DECISION ||--|{ RULE_EXECUTION : "contains step trace"
    
    APPLICATION {
        string id PK "Unique Applicant ID e.g. APP_1001"
        datetime created_at "Submission Timestamp"
        int age "Applicant Age (18-100)"
        float monthly_income "Verified Gross Monthly Income (INR)"
        float existing_monthly_debt "Existing Debt Commitments (INR)"
        int credit_score "Bureau Credit Score (300-900)"
        float employment_years "Continuous Employment Duration"
        string repayment_history "Rating: Excellent, Good, Fair, Poor"
        boolean recent_default "Past 24-Month Default Flag"
        float requested_amount "Requested Principal (INR)"
        int requested_tenure_months "Requested Loan Tenure (6-84 Mo)"
        string loan_purpose "Purpose: Personal, Home, Education..."
        string employment_type "Type: Salaried, Self-Employed..."
        json input_warnings "Flagged Unusual Parameters"
    }

    DECISION {
        int id PK "Decision Autoincrement Primary Key"
        string application_id FK "Foreign Key to Application"
        datetime created_at "Decision Generation Timestamp"
        string decision_status "ELIGIBLE, CONDITIONALLY_ELIGIBLE, NOT_ELIGIBLE"
        string risk_class "LOW, MEDIUM, HIGH"
        float interest_rate "Annual Interest Rate e.g. 0.095"
        string interest_rate_band "Illustrative Band Label"
        int suggested_tenure_months "Recommended Tenure"
        float recommended_amount "Recommended Loan Principal (INR)"
        float max_affordable_emi "Permissible Monthly EMI (INR)"
        float requested_emi "Estimated Requested EMI (INR)"
        float recommended_emi "Monthly Installment on Recommended Principal"
        float supportable_principal "Annuity Principal Supportable by Max EMI"
        boolean exceeds_affordability "Flag if Request Exceeds Supportable"
        boolean haircut_applied "Flag if Conditional Haircut (70%) Applied"
        text rationale_summary "Plain English Underwriting Summary"
        json rejection_reasons "Statutory Adverse Action Grounds"
        json conditions "Underwriting Covenants & Stipulations"
        json positive_factors "Prime Positive Attributes"
        json risk_factors "Adverse Risk Attributes"
        json counterfactual_hints "Actionable Remediation Hints"
        json proof_trees "Full FOL Proof Tree Hierarchy"
        string threshold_version "Policy Version String e.g. 1.0.0"
    }

    RULE_EXECUTION {
        int id PK "Execution Step Primary Key"
        int decision_id FK "Foreign Key to Decision"
        int step_number "Chronological Execution Order (1..N)"
        string rule_id "Unique Rule Identifier e.g. DER_CS_01"
        string rule_name "Human-Readable Rule Title"
        string rule_type "hard_knockout, derivation, decision"
        int priority "Salience Priority Integer"
        text fol_form "First-Order Logic Horn Clause String"
        text plain_english "Plain English Rationale"
        json matched_facts "List of Matched Ground Facts"
        json actual_input_values "Observed Numeric Input Values"
        json asserted_facts "List of Ground Facts Asserted to WM"
        json competing_rules "Competing Rules in Conflict Set"
        text resolution_reason "Conflict Resolution Explanation"
    }

    ML_RUN {
        int id PK "Run Autoincrement Primary Key"
        datetime trained_at "Training Timestamp"
        int n_train_samples "Training Set Size"
        int n_test_samples "Held-Out Test Set Size"
        json results_json "Complete Metrics, Matrices & Importances"
    }

    FAIRNESS_REPORT {
        int id PK "Report Autoincrement Primary Key"
        datetime generated_at "Generation Timestamp"
        json report_json "Group Parity Metrics, DIR, and Proxy Analyses"
    }
```
