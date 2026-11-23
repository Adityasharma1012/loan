# Test Specifications, Scenarios & Verification Matrix
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

---

## 1. Test Suite Summary & Execution

The test suite is implemented in [`backend/tests/`](file:///c:/bava/loan-xai/backend/tests/) using `pytest` and covers 37 automated tests across 4 comprehensive modules:
- [`test_rule_engine.py`](file:///c:/bava/loan-xai/backend/tests/test_rule_engine.py): Production rules, conflict resolution, refraction, determinism, order-invariance, and required scenarios.
- [`test_fol.py`](file:///c:/bava/loan-xai/backend/tests/test_fol.py): First-order logic atoms, unification, substitution, and derivation proof tree construction.
- [`test_financial.py`](file:///c:/bava/loan-xai/backend/tests/test_financial.py): DTI calculations, annuity EMI math, supportable principal sizing, and counterfactual hints.
- [`test_ml_and_fairness.py`](file:///c:/bava/loan-xai/backend/tests/test_ml_and_fairness.py): Synthetic generator, ML models, hand-computed fairness metrics, and proxy detection.
- [`test_api.py`](file:///c:/bava/loan-xai/backend/tests/test_api.py): FastAPI endpoints, Pydantic v2 422 validations, input warnings, CSV streaming, and ReportLab PDF export.

```bash
cd loan-xai
python -m pytest backend/tests -v
```

---

## 2. Pre-Defined Test Scenarios (Prompt Requirements 1-9)

| Scenario No. | Description & Profile | Expected Decision | Expected Risk Tier | Key Rationale / Asserted Rules |
| :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | **High Income + Excellent Credit**<br/>Income ₹1.2L, Debt ₹15k, Credit 820, 7 yrs emp, Good repayment | `ELIGIBLE` | `LOW` | `DER_INC_01`, `DER_CS_01`, `DER_DTI_01`, `RSK_001`, `DEC_002` fire. Full requested amount approved. |
| **Scenario 2** | **Low Income + Poor Credit**<br/>Income ₹15k, Debt ₹8k, Credit 510, Poor repayment | `NOT_ELIGIBLE` | `HIGH` | `HKO_003` (Credit &lt; 550 floor) and `DEC_001` fire. Principal sized to ₹0. |
| **Scenario 3** | **High DTI (> 50%)**<br/>Income ₹50k, Debt ₹32k (64% DTI), Credit 760 | `NOT_ELIGIBLE` | `HIGH` | `DER_DTI_03` (Excessive DTI &gt; 50%) prevents eligibility and conditional approval. |
| **Scenario 4** | **Good Credit + Short Employment**<br/>Income ₹45k, Debt ₹10k, Credit 770, 0.8 yr emp | `CONDITIONALLY_ELIGIBLE` | `MEDIUM` | Core criteria pass but employment &lt; 2 yrs. Capped tenure and employment verification covenant added. |
| **Scenario 5** | **Near-Prime Credit + Good Repayment**<br/>Income ₹40k, Debt ₹12k, Credit 680, 3 yrs emp | `CONDITIONALLY_ELIGIBLE` | `MEDIUM` | Credit in near-prime band [650, 749]. 30% haircut applied on principal; Medium rate band assigned. |
| **Scenario 6** | **Missing Fields & Schema Invalidation**<br/>Missing mandatory parameters or out-of-bound values | `HTTP 422` | N/A | Pydantic v2 rejects request with structured field-level error messages before engine invocation. |
| **Scenario 7** | **Zero or Negative Income**<br/>Income ₹0 or -₹5,000 | `NOT_ELIGIBLE` | `HIGH` | `HKO_002` (Non-positive income knockout) asserts immediate disqualification. |
| **Scenario 8** | **Request Exceeds Affordability**<br/>Income ₹35k, Debt ₹9k, Requests ₹25 Lakhs | `ELIGIBLE` | `LOW` | Borrower approved, but principal downsized to max supportable annuity amount (₹1.8L) and flagged. |
| **Scenario 9** | **Borderline Cases**<br/>Income ₹30k, Score 750, DTI 0.40, Emp 2.0 yrs | `ELIGIBLE` | `LOW` | Exact boundary threshold passes prime criteria; 1-point decrement (Score 749) transitions to Conditional. |

---

## 3. Mathematical Invariance & Safety Tests

### 3.1 Determinism Test
- **Methodology**: Evaluates an identical applicant profile 10 consecutive times.
- **Assertion**: Decisions, risk classes, recommended amounts, and exact rule execution sequences must be identical across all runs.

### 3.2 Rule-Order Invariance Test
- **Methodology**: Shuffles the active rule order in memory before forward chaining.
- **Assertion**: Rule order shuffling does not alter the conflict resolution order, winning rules, or final output.

### 3.3 Refraction Property Test
- **Methodology**: Inspects rule execution trace.
- **Assertion**: Every rule ID appears at most once in the execution trace per evaluation cycle.

### 3.4 Hand-Computed Fairness Metrics Test
- **Methodology**: Compares output of `compute_group_metrics` against hand-calculated expected values on a constructed toy demographic table:
  - Male (Privileged): Selection Rate = $0.80$
  - Female (Unprivileged): Selection Rate = $0.40$
  - Hand-calculated DIR: $0.40 / 0.80 = 0.50$
  - Hand-calculated SPD: $0.40 - 0.80 = -0.40$
  - Hand-calculated EOD: $0.60 - 1.00 = -0.40$
  - Four-Fifths Flag: True ($DIR < 0.80$).

### 3.5 Annuity Formula Test
- **Principal**: ₹100,000, **Annual Rate**: 12% ($r = 0.01$/mo), **Tenure**: 12 months.
- **Hand-computed EMI**:
  $$\text{EMI} = 100000 \times \frac{0.01 \times (1.01)^{12}}{(1.01)^{12} - 1} = ₹8,884.88$$
- **Verification**: Code matches to within $\pm ₹0.05$.
