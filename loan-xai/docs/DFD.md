# Data Flow Diagrams (DFD)
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

---

## 1. DFD Level 0: Context Diagram

The Level 0 Context Diagram depicts the entire LoanXAI system as a single boundary interacting with external entities: the Credit Applicant / Loan Officer and Credit Bureau Data Sources.

```mermaid
graph LR
    User["Credit Applicant / Loan Officer"] -->|1. Submit Financial Application| System["LoanXAI Expert System (Rule Engine + ML Benchmark)"]
    System -->|2. Return Eligibility Verdict & Recommended Sizing| User
    System -->|3. Return FOL Proof Tree & Step Trace| User
    System -->|4. Return Counterfactual Hints & PDF Memo| User
    System -->|5. Return Algorithmic Fairness & Bias Audit| User
```

---

## 2. DFD Level 1: Subsystem Data Flow

Level 1 decomposes the system into its primary computational modules: Input Validation, Production Rule Engine, Financial Sizing, ML Benchmarking, and Audit Logging.

```mermaid
graph TD
    User["Applicant / Underwriter"] -->|Raw JSON Payload| P1["1.0 Input Validation & Warning Detection"]
    
    P1 -->|Validated Clean Inputs| P2["2.0 Working Memory Initialization"]
    P1 -->|Input Warnings Notice| P5["5.0 Response Synthesizer"]
    
    subgraph "Rule Engine Core"
        P2 -->|Assert Ground Atoms| WM[("Working Memory Facts")]
        WM -->|Match Premises| P3["3.0 Forward-Chaining Pattern Matcher"]
        RulesYAML[("config/rules.yaml")] --> P3
        P3 -->|Candidate Rules| P4["4.0 Conflict Resolution Agenda"]
        P4 -->|Winning Rule Execution| WM
        P4 -->|Execution Step History| TraceDB[("Execution Trace")]
        WM -->|Final Derived Atoms| P5
    end
    
    subgraph "Financial Affordability"
        ThresholdsYAML[("config/thresholds.yaml")] --> P6["6.0 Sizing & Annuity Calculator"]
        P2 --> P6
        P6 -->|Recommended Amount & Bands| P5
        P6 -->|Counterfactual Delta Bounds| P5
    end
    
    subgraph "Statistical Machine Learning"
        P2 -->|Non-protected Features| P7["7.0 ML Classifier Benchmark"]
        P7 -->|Decision Tree & Logistic Preds| P5
    end
    
    P5 -->|Complete Audit Record| SQLite[("SQLite Database")]
    P5 -->|Interactive Decision Response| User
```

---

## 3. DFD Level 2: Rule Engine Internal Forward-Chaining Cycle

Level 2 details the exact iterative forward-chaining fixpoint inference loop and conflict resolution pipeline.

```mermaid
graph TD
    Start["Start Execution Cycle"] --> Init["Assert Ground Facts: Applicant(x), Income(x), Score(x), DTI(x)"]
    Init --> FixpointCheck{"Conflict Set Empty or Fixpoint Reached?"}
    
    FixpointCheck -- No --> Match["Pattern Match: Evaluate Rule Premises against Working Memory Facts"]
    Match --> RefractFilter["Refraction Filter: Drop Rules Already Fired"]
    RefractFilter --> BuildCS["Assemble Conflict Set of Candidate Rules"]
    
    BuildCS --> Sort1["Sort Step 1: Prioritize Hard Knock-out Rules (rule_type == 'hard_knockout')"]
    Sort1 --> Sort2["Sort Step 2: Sort by Salience / Priority Descending"]
    Sort2 --> Sort3["Sort Step 3: Sort by Specificity (Condition Count Descending)"]
    Sort3 --> Sort4["Sort Step 4: Deterministic Tie-Break (Rule ID Ascending)"]
    
    Sort4 --> SelectWinner["Select Top Rule Candidate as Winning Rule"]
    SelectWinner --> Fire["Fire Winning Rule Actions: Assert New Ground Atoms to Working Memory"]
    Fire --> LogTrace["Record Step: Rule ID, Matched Facts, Asserted Facts, Conflict Resolution Rationale"]
    LogTrace --> UpdateProof["Update FOL Derivation Proof Tree Lineage"]
    UpdateProof --> MarkFired["Mark Rule ID in Fired Refraction Set"]
    MarkFired --> FixpointCheck
    
    FixpointCheck -- Yes --> SynthesizeVerdict["Synthesize Verdict: Extract Decision Status, Risk Tier, and Rate Band"]
    SynthesizeVerdict --> End["Return Verdict, Proof Trees, and Complete Execution History"]
```
