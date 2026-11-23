# Requirements Traceability Matrix (RTM)
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

This document maps every single clause of the project specification to the implementing backend source code, REST API endpoints, frontend UI pages, and automated unit tests.

---

## 1. Project Statement Clause Mapping

| Project Statement Clause | Backend Implementation | REST API Endpoint | Frontend Page | Test Case (Pytest) |
| :--- | :--- | :--- | :--- | :--- |
| **"Develop an expert system that evaluates loan applications using production rules"** | [`app/rule_engine/engine.py`](file:///c:/bava/loan-xai/backend/app/rule_engine/engine.py)<br/>[`config/rules.yaml`](file:///c:/bava/loan-xai/backend/app/config/rules.yaml) | `POST /api/evaluate`<br/>`GET /api/rules` | `NewApplicationPage.jsx`<br/>`AboutPage.jsx` | `test_rule_engine.py::test_scenario_1_high_income_excellent_credit`<br/>`test_refraction_property` |
| **"and first-order predicate logic"** | [`app/logic/fol.py`](file:///c:/bava/loan-xai/backend/app/logic/fol.py) (`GroundAtom`, Horn clauses, unification, proof trees) | `POST /api/evaluate`<br/>`GET /api/applications/{id}` | `ExplanationPage.jsx`<br/>`ProofTreeView.jsx` | `test_fol.py::test_ground_atom_representation`<br/>`test_proof_tree_construction` |
| **"The system should determine eligibility,"** | [`app/rule_engine/engine.py`](file:///c:/bava/loan-xai/backend/app/rule_engine/engine.py) (`DEC_001` to `DEC_004`) | `POST /api/evaluate` | `ResultsPage.jsx`<br/>`DecisionBadge.jsx` | `test_rule_engine.py::test_scenario_1..9` |
| **"recommend a loan amount"** | [`app/logic/financial.py`](file:///c:/bava/loan-xai/backend/app/logic/financial.py) (`calculate_recommended_loan`, annuity PV formula) | `POST /api/evaluate` | `ResultsPage.jsx` | `test_financial.py::test_calculate_recommended_loan_within_affordability`<br/>`test_scenario_8` |
| **"and interest band,"** | [`config/thresholds.yaml`](file:///c:/bava/loan-xai/backend/app/config/thresholds.yaml)<br/>[`app/rule_engine/engine.py`](file:///c:/bava/loan-xai/backend/app/rule_engine/engine.py) (`RSK_001` to `RSK_003`) | `POST /api/evaluate` | `ResultsPage.jsx` | `test_rule_engine.py::test_scenario_1_high_income_excellent_credit` |
| **"and provide a complete rule-based decision rationale."** | [`app/logic/financial.py`](file:///c:/bava/loan-xai/backend/app/logic/financial.py)<br/>[`app/rule_engine/engine.py`](file:///c:/bava/loan-xai/backend/app/rule_engine/engine.py) (reasons, covenants, counterfactual hints) | `POST /api/evaluate`<br/>`GET /api/applications/{id}/pdf` | `ResultsPage.jsx`<br/>`ExplanationPage.jsx`<br/>`AuditReportPage.jsx` | `test_financial.py::test_counterfactual_hints_generation`<br/>`test_api.py::test_pdf_export` |
| **"Compare it with a simple ML classifier on transparency, auditability,"** | [`app/ml/models.py`](file:///c:/bava/loan-xai/backend/app/ml/models.py) (Decision Tree & Logistic Regression benchmarks) | `GET /api/ml/metrics`<br/>`POST /api/ml/retrain` | `MLComparisonPage.jsx` | `test_ml_and_fairness.py::test_ml_model_training_and_comparison` |
| **"edge cases,"** | [`app/ml/models.py`](file:///c:/bava/loan-xai/backend/app/ml/models.py) (`_evaluate_edge_cases_suite` with 9 canonical edge cases) | `GET /api/ml/metrics` | `MLComparisonPage.jsx` | `test_ml_and_fairness.py::test_ml_model_training_and_comparison` |
| **"and regulatory defensibility,"** | Adverse action notice generation, versioned thresholds, ReportLab PDF audit memo | `GET /api/applications/{id}/pdf` | `AuditReportPage.jsx` | `test_api.py::test_pdf_export` |
| **"along with a fairness review to identify potential group-level disadvantages."** | [`app/fairness/audit.py`](file:///c:/bava/loan-xai/backend/app/fairness/audit.py) (DIR, SPD, EOD, proxy features, small-sample warnings) | `GET /api/fairness/report` | `FairnessPage.jsx` | `test_ml_and_fairness.py::test_hand_computed_fairness_metrics`<br/>`test_small_sample_size_flagging` |

---

## 2. Technical Requirements Traceability

| Requirement | Implementation Artifact | Verification Evidence |
| :--- | :--- | :--- |
| **Academic Disclaimer Banner** | [`frontend/src/components/Banner.jsx`](file:///c:/bava/loan-xai/frontend/src/components/Banner.jsx) | Rendered persistently across all 10 pages at top of viewport |
| **Pydantic v2 422 Errors** | [`backend/app/schemas/application.py`](file:///c:/bava/loan-xai/backend/app/schemas/application.py) | `test_api.py::test_validation_errors_422` (PASSED) |
| **Unusual Input Warnings** | [`app/schemas/application.py`](file:///c:/bava/loan-xai/backend/app/schemas/application.py) (`detect_warnings`) | `test_api.py::test_unusual_input_warning_flag` (PASSED) |
| **Determinism Property** | [`app/rule_engine/engine.py`](file:///c:/bava/loan-xai/backend/app/rule_engine/engine.py) | `test_rule_engine.py::test_determinism_identical_runs` (PASSED) |
| **Rule-Order Independence** | [`app/rule_engine/engine.py`](file:///c:/bava/loan-xai/backend/app/rule_engine/engine.py) (`conflict_sort_key`) | `test_rule_engine.py::test_rule_order_invariance` (PASSED) |
| **Refraction Property** | Fired rule tracking in `engine.py` | `test_rule_engine.py::test_refraction_property` (PASSED) |
| **Annuity Loan Sizing** | PV formula in `app/logic/financial.py` | `test_financial.py::test_monthly_emi_annuity_math` (PASSED) |
| **Hand-Computed Fairness** | `compute_group_metrics` mathematical test | `test_ml_and_fairness.py::test_hand_computed_fairness_metrics` (PASSED) |
| **Single-Command Launch** | `loan-xai/run.bat` (Windows), `loan-xai/run.sh` (POSIX) | Successfully launched and tested live in Phase 6 |
