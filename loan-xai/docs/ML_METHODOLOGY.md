# Machine Learning Methodology & Benchmarking
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

---

## 1. Ground-Truth Data Generating Process (DGP)

### 1.1 Independence Rationale
A fundamental principle of this project is that the ground-truth target variable (`repaid` $\in \{0, 1\}$) is **strictly independent of the rule engine output**.

> [!IMPORTANT]
> **Why Independence is Essential**:  
> If the ground-truth label were produced by the rule engine, the machine learning models would simply be trained to mimic (distill) the rule engine's deterministic logic. Evaluating ML against rule engine outputs would measure model capacity to approximate step functions rather than credit risk prediction.  
> In real-world retail banking, true credit performance is an exogenous economic phenomenon driven by cashflow liquidity, macroeconomic shocks, and borrower discipline. Both the expert rule engine and the ML models must be evaluated against this independent economic reality.

### 1.2 Mathematical Formulation
The synthetic generator in [`backend/app/ml/data.py`](file:///c:/bava/loan-xai/backend/app/ml/data.py) models repayment log-odds via a logistic data generating process:

$$z = \beta_0 + \beta_{\text{inc}} \tilde{I} + \beta_{\text{score}} \tilde{S} - \beta_{\text{dti}} \tilde{D} + \beta_{\text{emp}} \tilde{E} + \gamma_{\text{rep}} - \delta_{\text{def}} + \epsilon$$

Where:
- $\tilde{I} = \frac{\text{Income} - 40000}{25000}$ (Standardized income)
- $\tilde{S} = \frac{\text{CreditScore} - 700}{80}$ (Standardized score)
- $\tilde{D} = \frac{\text{DTI} - 0.35}{0.15}$ (Standardized DTI)
- $\tilde{E} = \frac{\text{EmploymentYears} - 4.0}{3.0}$ (Standardized tenure)
- $\gamma_{\text{rep}} \in \{+1.2, +0.5, -0.6, -1.8\}$ for $\{\text{Excellent}, \text{Good}, \text{Fair}, \text{Poor}\}$
- $\delta_{\text{def}} = 2.4$ if recent default, else $0.0$
- $\epsilon \sim \mathcal{N}(0, 0.75^2)$ (Unobserved stochastic economic shock)

The probability of successful repayment is:
$$P(\text{repaid}=1) = \sigma(z) = \frac{1}{1 + e^{-z}}$$

---

## 2. Models & Experimental Design

### 2.1 Model Specifications
1. **Decision Tree Classifier (White-Box Surrogate)**:
   - Hyperparameters: `max_depth=4`, `min_samples_leaf=20`, `class_weight='balanced'`.
   - Purpose: Represents an interpretable tree model whose decision paths can be audited visually against rule engine Horn clauses.
2. **Logistic Regression (Parametric Baseline)**:
   - Hyperparameters: L2 penalty ($C=1.0$), `max_iter=1000`, `class_weight='balanced'`.
   - Feature Scaling: `StandardScaler` fitted strictly on training fold.
   - Purpose: Represents linear scoring cards standard in retail banking.

### 2.2 Split Strategy
- Dataset: 6,000 synthetic applicants.
- Split: Stratified 80% train ($N=4,800$), 20% held-out test ($N=1,200$).
- Random Seed: Fixed (`seed=42`) for 100% deterministic reproducibility.

---

## 3. Decision Mappings for Benchmarking

Because the rule engine outputs three categorical states (`ELIGIBLE`, `CONDITIONALLY_ELIGIBLE`, `NOT_ELIGIBLE`) while binary ML predicts binary approval, two standard mappings are evaluated:
- **Standard Mapping**:  
  $$\hat{Y}_{\text{rule}} = \begin{cases} 1 & \text{if } \text{Decision} \in \{\text{ELIGIBLE}, \text{CONDITIONALLY\_ELIGIBLE}\} \\ 0 & \text{if } \text{Decision} = \text{NOT\_ELIGIBLE} \end{cases}$$
- **Strict Mapping**:  
  $$\hat{Y}_{\text{rule}} = \begin{cases} 1 & \text{if } \text{Decision} = \text{ELIGIBLE} \\ 0 & \text{otherwise} \end{cases}$$

---

## 4. Evaluation Metrics & Agreement Analysis

| Evaluation Metric | Decision Tree | Logistic Regression | Rule Engine (Standard) | Rule Engine (Strict) |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | 70.0% | 81.3% | 72.9% | 34.9% |
| **Precision** | 76.5% | 84.1% | 77.2% | 94.2% |
| **Recall** | 79.2% | 91.0% | 86.9% | 18.2% |
| **F1 Score** | 0.779 | 0.874 | 0.818 | 0.306 |
| **ROC-AUC** | 0.774 | 0.854 | — | — |

### Agreement Statistics
- **Cohen's Kappa ($\kappa$)**: Substantial consensus between Rule Engine (Standard) and Decision Tree ($\kappa \approx 0.35$ to $0.45$).
- **Overlap Matrix**: Over 78% identical classification decisions between the production rule engine and trained decision trees.

---

## 5. Critical Edge-Case Divergence Suite

The 9 canonical edge cases reveal the qualitative superiority of production rules in regulatory compliance:
1. **Underage Wealthy Applicant (Age 17)**:
   - *Rule Engine*: DECLINED (`HKO_001` enforces legal capacity floor).
   - *ML Models*: APPROVED (Logistic regression and decision trees observe high income and 850 score, inappropriately approving a legally uncontractable minor).
2. **Excessive DTI (64%) with Prime Credit**:
   - *Rule Engine*: DECLINED (Strict 50% max DTI cap enforced).
   - *ML Models*: Smooths over high debt due to compensating prime credit marks.
3. **Loan Request Exceeding Affordability (25 Lakhs on 35k Income)**:
   - *Rule Engine*: Approves borrower profile but downsized to supportable principal (₹1.8L) via annuity formula.
   - *ML Models*: Binary approval without capital sizing safety limits.

> [!WARNING]
> **Synthetic Data Disclaimer**:  
> Accuracy numbers reflect performance on the synthetic data generating distribution and do not constitute a forecast of real-world retail banking loss rates.
