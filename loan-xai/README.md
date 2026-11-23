# Explainable Rule-Based Loan Eligibility & Credit Decision System (`LoanXAI`)
**Course**: Artificial Intelligence Foundations  
**Academic Demonstration**: *Rates and amounts are illustrative, not bank offers. Approval is never guaranteed. Synthetic data only.*

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
&nbsp;
[![Tests](https://img.shields.io/badge/pytest-37%20passed-success?logo=pytest)](file:///c:/bava/loan-xai/tests.png)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-blue?logo=python)](file:///c:/bava/loan-xai/backend/requirements.txt)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](file:///c:/bava/loan-xai/frontend/package.json)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](file:///c:/bava/loan-xai/backend/app/main.py)

> 🚀 **Ready to Deploy on Render:** See [`docs/DEPLOY_RENDER.md`](./docs/DEPLOY_RENDER.md) for 1-click Render Blueprint and Docker deployment instructions.

---

## 1. Project Statement & Objectives

> "Develop an expert system that evaluates loan applications using production rules and first-order predicate logic. The system should determine eligibility, recommend a loan amount and interest band, and provide a complete rule-based decision rationale. Compare it with a simple ML classifier on transparency, auditability, edge cases, and regulatory defensibility, along with a fairness review to identify potential group-level disadvantages."

`LoanXAI` is an institutional-grade, full-stack expert system designed to bring **deterministic explainability**, **formal first-order logic proofs**, and **algorithmic fairness audits** to automated credit underwriting.

---

## 2. Key Capabilities & Core Innovations

1. **Declarative Production Rule Engine**:
   - Declarative rules specified in versioned YAML [`backend/app/config/rules.yaml`](file:///c:/bava/loan-xai/backend/app/config/rules.yaml).
   - Forward-chaining inference to a fixpoint with strict conflict resolution:
     1. Hard knock-outs first (statutory legal floors, severe credit impairment).
     2. Salience / priority descending.
     3. Condition specificity descending.
     4. Deterministic tie-breaking (Rule ID ascending).
   - Refraction: Each rule instance activates at most once per applicant run.
   - 100% Deterministic and order-invariant.

2. **First-Order Predicate Logic (FOL) & Derivation Proof Trees**:
   - Rules formulated as definite Horn clauses with variables:
     $$\forall x: \text{Applicant}(x) \land \text{IncomeSufficient}(x) \land \text{CreditPrime}(x) \land \text{DTIOK}(x) \land \text{EmploymentStable}(x) \land \text{RepaymentPositive}(x) \to \text{FinalDecision}(x, \text{ELIGIBLE})$$
   - Ground atomic facts with substitution, unification, and negation-as-failure (NAF).
   - Generates interactive derivation proof trees tracing from final eligibility verdicts down to leaf ground facts.

3. **Financial Affordability & Annuity Sizing**:
   - Debt-to-Income (DTI) computation and disposable debt capacity ($40\%$ gross income ceiling).
   - Maximum supportable principal sizing derived via the standard annuity present value formula:
     $$\text{PV} = \text{Max EMI} \times \frac{1 - (1 + r)^{-n}}{r}$$
   - Prudent income-multiple caps ($36\times$ monthly income) and conditional risk-mitigation haircuts ($70\%$).
   - Actionable counterfactual explanations calculating exact parametric deltas required to reach eligibility.

4. **Independent Machine Learning Benchmarks**:
   - Ground-truth label (`repaid`) generated via an **independent probabilistic logistic data-generating process** incorporating financial capacity, behavioral history, and stochastic shocks (not rule engine outputs).
   - White-box Decision Tree (`max_depth=4`) and regularized Logistic Regression.
   - Comprehensive comparative benchmarking on accuracy, precision, recall, F1, ROC-AUC, confusion matrices, Cohen's Kappa agreement ($\kappa$), and 9 canonical edge cases.

5. **Fairness & Demographic Bias Review**:
   - **Fairness-safe input design**: Protected demographic attributes (gender, age bracket, regional setting) are strictly quarantined from the application form and underwriting feature matrix.
   - Group-level algorithmic audit calculating Disparate Impact Ratios (flagging EEOC Four-Fifths violations $DIR < 0.80$), Statistical Parity Differences (SPD), Equal Opportunity Differences (EOD), and false positive/negative rates.
   - Detection of proxy feature leakage (thin-file rural credit penalties and historical wage gaps).
   - Small sample size censoring ($n < 30$) to prevent spurious inferences.

6. **Institutional PDF Audit Memoranda & CSV Export**:
   - Automatic generation of formal credit underwriting memoranda with adverse action notices and complete chronological rule execution traces via ReportLab.
   - One-click CSV export of applications and decision outcomes.

---

## 3. Technology Stack

- **Backend**: Python 3.13+, FastAPI, Pydantic v2, SQLAlchemy, SQLite, PyYAML, ReportLab.
- **Machine Learning**: scikit-learn, pandas, numpy.
- **Testing**: pytest (37 passing automated tests).
- **Frontend**: React 18, Vite, Tailwind CSS (Navy/Blue fintech palette, light/dark mode), Lucide Icons, Recharts.

---

## 4. Quickstart: Launching the Application

The system is configured to launch with **one documented command per side (or one script for both)** across Windows, macOS, and Linux.

### Option A: Single-Script Launch (Recommended)

#### On Windows:
```cmd
cd loan-xai
run.bat
```

#### On Linux / macOS:
```bash
cd loan-xai
chmod +x run.sh
./run.sh
```

---

### Option B: Individual Terminal Commands

#### 1. Backend Server (Terminal 1):
```bash
cd loan-xai/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Interactive Swagger API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- API Root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#### 2. Frontend Web Application (Terminal 2):
```bash
cd loan-xai/frontend
npm run dev
```
- Local Web Application: [http://127.0.0.1:5173/](http://127.0.0.1:5173/)

---

### Option C: Seeding and Training Utilities

To seed the SQLite database with diverse demo applicants evaluated through the real rule engine:
```bash
python loan-xai/scripts/seed_demo.py
```

To generate synthetic datasets and train/benchmark the ML models:
```bash
python loan-xai/scripts/train_model.py
```

---

## 5. Running the Test Suite

Run the full automated test suite containing 37 tests across unit, logic, financial math, ML, fairness, and API endpoints:

```bash
cd loan-xai
python -m pytest backend/tests -v
```

All 37 test cases define expected outputs upfront and verify 100% compliance with underwriting rules, mathematical invariants, determinism, refraction, and schema validation.

---

## 6. Directory Structure

```
loan-xai/
  backend/
    app/
      api/          # FastAPI REST route handlers & endpoints
      schemas/      # Pydantic v2 validation contracts & warnings
      rule_engine/  # Forward-chaining engine, conflict resolution, refraction
      logic/        # Financial math, annuity sizing, FOL atoms & proof trees, PDF reports
      ml/           # Independent synthetic data generator & ML benchmarks
      fairness/     # Disparate impact, statistical parity, and proxy analysis
      db/           # SQLAlchemy models & SQLite database session
      config/       # Declarative rules.yaml and thresholds.yaml
      main.py       # FastAPI application entry point
    tests/          # Comprehensive pytest test suite (37 tests)
    requirements.txt
  frontend/
    src/
      api/          # REST client wrapper
      components/   # Persistent banner, sidebar, DecisionBadge, proof tree, timeline
      pages/        # 10 pages: Landing, Dashboard, NewApp, Results, Trace, ML, Fairness, History, Audit, Specs
      App.jsx       # Root layout & routing
      main.jsx      # React entry point
    package.json
    tailwind.config.js
    vite.config.js
  scripts/
    seed_demo.py    # Seeds SQLite database via real rule engine
    train_model.py  # Trains Decision Tree & Logistic Regression models
  docs/             # Complete project documentation suite
    ARCHITECTURE.md
    ASSUMPTIONS.md
    DFD.md
    ERD.md
    FLOWCHART.md
    FOL.md
    ML_METHODOLOGY.md
    FAIRNESS_METHODOLOGY.md
    RULES.md
    TEST_CASES.md
    USE_CASES.md
    FUTURE_WORK.md
    REQUIREMENTS_TRACEABILITY.md
  run.bat           # Windows single-command launcher
  run.sh            # Linux/macOS single-command launcher
  README.md
```

---

## 7. Documentation Suite Index

- [`docs/ARCHITECTURE.md`](file:///c:/bava/loan-xai/docs/ARCHITECTURE.md): Architectural components, responsibilities, and system interaction diagrams.
- [`docs/DFD.md`](file:///c:/bava/loan-xai/docs/DFD.md): Level 0, Level 1, and Level 2 Data Flow Diagrams.
- [`docs/FLOWCHART.md`](file:///c:/bava/loan-xai/docs/FLOWCHART.md): Complete forward chaining and conflict resolution flowchart.
- [`docs/USE_CASES.md`](file:///c:/bava/loan-xai/docs/USE_CASES.md): Actor use case diagram and workflow specifications.
- [`docs/ERD.md`](file:///c:/bava/loan-xai/docs/ERD.md): Database schema entity-relationship diagram.
- [`docs/RULES.md`](file:///c:/bava/loan-xai/docs/RULES.md): Complete declarative production rules catalogue.
- [`docs/FOL.md`](file:///c:/bava/loan-xai/docs/FOL.md): First-Order Logic specifications, Horn clauses, NAF, and proof tree semantics.
- [`docs/ML_METHODOLOGY.md`](file:///c:/bava/loan-xai/docs/ML_METHODOLOGY.md): Data generating process, ML architectures, metrics, and edge-case comparisons.
- [`docs/FAIRNESS_METHODOLOGY.md`](file:///c:/bava/loan-xai/docs/FAIRNESS_METHODOLOGY.md): Demographic parity, disparate impact ratios, proxy feature analysis, and legal caveats.
- [`docs/TEST_CASES.md`](file:///c:/bava/loan-xai/docs/TEST_CASES.md): Verification matrix for all 9 scenarios, boundary tests, and hand-computed checks.
- [`docs/ASSUMPTIONS.md`](file:///c:/bava/loan-xai/docs/ASSUMPTIONS.md): Complete record of design choices, defaults, and financial assumptions.
- [`docs/FUTURE_WORK.md`](file:///c:/bava/loan-xai/docs/FUTURE_WORK.md): Scaling optimizations, Rete algorithm, and neuro-symbolic extensions.
- [`docs/REQUIREMENTS_TRACEABILITY.md`](file:///c:/bava/loan-xai/docs/REQUIREMENTS_TRACEABILITY.md): Clause-by-clause traceability matrix mapping project requirements to code, tests, and pages.

---

## 8. License & Academic Integrity Notice

This project was developed for the **Artificial Intelligence Foundations** course. It demonstrates production expert systems, automated theorem proving via First-Order Logic, and comparative machine learning audits under fair lending principles. All data, credit scores, interest rates, and loan amounts are synthetic and illustrative.
