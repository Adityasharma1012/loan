# Project Assumptions and Design Decisions
**Course**: Artificial Intelligence Foundations  
**Project**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

This document records all architectural choices, engineering assumptions, financial defaults, and algorithmic decisions made during development.

---

## 1. Domain & Currency Framework
- **Jurisdiction & Currency**: Currency is **Indian Rupee (INR / ₹)** as specified by the project brief.
- **Credit Scoring System**: Credit scores are modeled on a **300 to 900 scale** (standard for bureaus such as CIBIL, Experian, CRIF High Mark).
- **Loan Category**: Default domain is uncollateralized retail personal/consumer lending.
- **Academic Demonstration Scope**: All decisions, rates, and amounts are synthetic and illustrative; a persistent disclaimer banner is rendered on all application pages.

---

## 2. Financial Metrics & Affordability Rules
- **Debt-to-Income (DTI)**:
  $$\text{DTI} = \frac{\text{Existing Monthly Debt Service}}{\text{Gross Verified Monthly Income}}$$
- **Maximum Permissible EMI (Affordable Debt Capacity)**:
  Standard prudential cap is 40% of monthly gross income earmarked for total debt service:
  $$\text{Max EMI} = \max\left(0, (0.40 \times \text{Monthly Income}) - \text{Existing Debt}\right)$$
- **Recommended Principal Sizing (Annuity Formula)**:
  For an interest rate band with annual interest rate $R$ (monthly rate $r = R / 12$) and tenure $n$ months:
  $$\text{Principal}_{\text{max\_emi}} = \text{Max EMI} \times \frac{1 - (1 + r)^{-n}}{r}$$
  $$\text{Principal}_{\text{income\_cap}} = \text{Monthly Income} \times 36$$
  $$\text{Recommended Amount} = \min\left(\text{Requested Amount}, \text{Principal}_{\text{max\_emi}}, \text{Principal}_{\text{income\_cap}}\right)$$
- **Conditional Eligibility Sizing**:
  When conditionally eligible, an additional risk-mitigation haircut factor of **0.70 (70%)** is applied:
  $$\text{Conditional Amount} = \min\left(\text{Requested Amount} \times 0.70, \text{Principal}_{\text{max\_emi}}\right)$$
  and loan tenure is capped at **36 months** maximum.

---

## 3. Risk Categories & Interest Rate Bands
- **LOW Risk**: 9.0% – 11.0% annual rate (Base: **9.5%**).
  - Conditions: Prime credit score ($\ge 750$), healthy DTI ($\le 0.40$), stable employment ($\ge 2$ years), positive repayment history, sufficient income ($\ge ₹30,000$).
- **MEDIUM Risk**: 11.0% – 14.0% annual rate (Base: **12.5%**).
  - Conditions: Near-prime score ($650 \le \text{score} < 750$), or marginal DTI ($0.40 < \text{DTI} \le 0.50$), or employment $< 2$ years, with no active defaults or subprime marks.
- **HIGH Risk**: 14.0% – 18.0% annual rate (Base: **15.5%**).
  - Conditions: Subprime score ($550 \le \text{score} < 650$), excessive DTI ($> 0.50$), or adverse repayment history without hard knock-out.
- **VERY HIGH / UNACCEPTABLE Risk**: $> 18.0\%$ (Decline).

---

## 4. Rule Engine Working Memory & Conflict Resolution
- **Working Memory**: Dynamic collection of ground atomic facts.
- **Inference Strategy**: Forward chaining to fixpoint (no further rules can activate).
- **Refraction**: Each rule instance activates at most once per execution cycle.
- **Conflict Resolution Hierarchy**:
  1. **Rule Category**: `hard_knockout` rules are prioritized and evaluated first.
  2. **Priority / Salience**: Higher numeric priority executes first.
  3. **Specificity**: Rules with more premise conditions execute before more general rules.
  4. **Deterministic Tie-Break**: Lexicographical order of rule ID (`id` ascending).
- **Order Invariance**: Fact assertion order or YAML parsing order does NOT alter the resulting decision or terminal state.

---

## 5. First-Order Logic (FOL) Derivations
- **Formulation**: Horn clauses $\forall x: P_1(x) \land P_2(x) \land \dots \land P_k(x) \to C(x)$.
- **Negation as Failure (NAF)**: Expressed via `NOT_HAS` / `~Predicate(x)`. If a ground atom cannot be proven from working memory facts, its negation holds.
- **Proof / Derivation Tree**: Each conclusion records its supporting ground atoms, enabling complete tree visualization from leaf inputs to final eligibility verdict.

---

## 6. Synthetic Ground Truth & Machine Learning Separation
- **Ground-Truth Label Independence**: The target label (`repaid`: 0 or 1) is generated via an independent probabilistic logistic process influenced by underlying debt service capacity, income stability, credit score, and stochastic macro shocks. It is **never** derived from the rule engine output.
  - *Rationale*: Evaluating ML against rule engine outputs would measure distillation/imitation rather than credit risk prediction. True comparison requires both paradigms to be evaluated against true repayment performance.
- **Models**:
  1. **Decision Tree Classifier**: Interpretable white-box surrogate with `max_depth=4` and `min_samples_leaf=20`.
  2. **Logistic Regression**: Linear baseline with standard feature scaling and calibrated probabilities.
- **Decision Mapping for Comparison**:
  - *Standard Mapping*: `ELIGIBLE` and `CONDITIONALLY_ELIGIBLE` $\to 1$ (Approve); `NOT_ELIGIBLE` $\to 0$ (Reject).
  - *Strict Mapping*: `ELIGIBLE` $\to 1$ (Approve); `CONDITIONALLY_ELIGIBLE` and `NOT_ELIGIBLE` $\to 0$ (Reject).

---

## 7. Protected Attributes & Fairness Audit Guardrails
- **Input Isolation**: Protected demographic attributes (gender, age bracket, regional setting) are strictly quarantined.
- **Production Exemption**: Neither the Rule Engine nor the ML feature vector consumes protected demographic features.
- **Disparate Impact Threshold**: Standard EEOC 80% Four-Fifths rule threshold (DIR $< 0.80$ flagged as potential disparate impact).
- **Sample Censoring**: Demographic subgroups with $n < 30$ are surfaced with explicit statistical caveat banners to prevent premature inferences from small sample variance.
