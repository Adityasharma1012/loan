# Forward-Chaining Inference & Conflict Resolution Flowchart
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

---

## Complete Forward-Chaining Inference Flowchart

```mermaid
flowchart TD
    Start(["Start Application Evaluation"]) --> Ingest["Ingest Raw Inputs:<br/>Income, Debt, Score, Age, Tenure, Repayment, Default"]
    Ingest --> Validate{"Pydantic v2 Bounds Check:<br/>Age &ge; 18, Income &gt; 0, Score &in; [300, 900]"}
    
    Validate -- Invalid --> Return422["Return HTTP 422 Unprocessable Entity with Field Errors"]
    Validate -- Valid --> WarningCheck{"Detect Warnings:<br/>Debt &gt; Income OR Request &gt; 50x Income?"}
    
    WarningCheck -- Yes --> FlagWarning["Add Input Warnings to Decision Payload"]
    WarningCheck -- No --> InitWM
    FlagWarning --> InitWM["Initialize Working Memory Facts:<br/>Applicant(x), Age(x), Income(x), Score(x), DTI(x), MaxEMI(x)"]
    
    InitWM --> MatchRules["MATCH PHASE:<br/>Evaluate Conditions of All Rules in rules.yaml against Working Memory"]
    MatchRules --> FilterRefract["REFRACTION FILTER:<br/>Exclude Rules that Already Fired in this Cycle"]
    FilterRefract --> CheckConflict{"Conflict Set Empty?"}
    
    CheckConflict -- Yes --> Synthesize["SYNTHESIS PHASE:<br/>Extract Verdict (Eligible / Conditional / Decline), Risk Class, Rate Band"]
    
    CheckConflict -- No --> ConflictResolve["CONFLICT RESOLUTION HIERARCHY:<br/>1. Hard Knock-Outs (rule_type == 'hard_knockout')<br/>2. Salience / Priority Descending<br/>3. Condition Specificity Descending<br/>4. Rule ID Ascending (Deterministic Tie-Break)"]
    
    ConflictResolve --> SelectWinner["Select Winner & Record Resolution Reason"]
    SelectWinner --> FireRule["FIRE PHASE:<br/>Assert Action Atoms to Working Memory<br/>e.g. IncomeSufficient(x), DTIOK(x), CreditPrime(x)"]
    FireRule --> AppendTrace["Append Step to Execution Trace & Update FOL Proof Tree Lineage"]
    AppendTrace --> AddRefract["Add Winning Rule ID to Fired Set"]
    AddRefract --> MatchRules
    
    Synthesize --> ComputeAnnuity["COMPUTE SIZING (Annuity Math):<br/>Principal = Max EMI &times; [1 - (1+r)^-n] / r<br/>Recommended = min(Requested, Supportable, 36x Income)"]
    ComputeAnnuity --> GenerateCF["Generate Counterfactual Hints from Threshold Deltas"]
    GenerateCF --> PersistDB["Persist Application, Decision, and Step Trace to SQLite"]
    PersistDB --> ReturnResponse(["Return Full Decision Response & Proof Trees"])
```
