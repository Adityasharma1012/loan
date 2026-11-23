# Declarative Production Rules Catalogue
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

Source Configuration: [`config/rules.yaml`](file:///c:/bava/loan-xai/backend/app/config/rules.yaml)  
Policy Version: `1.0.0`

---

## 1. Hard Knock-Out Rules (Priority: 100)
Hard knock-outs are statutory or legal floors evaluated with highest precedence in conflict resolution. If any premise matches, an adverse action atom is asserted immediately.

| Rule ID | Rule Name | FOL Horn Clause | Rationale & Explanation |
| :--- | :--- | :--- | :--- |
| **`HKO_001`** | Legal Age Capacity Knock-Out | $\forall x: \text{Applicant}(x) \land \text{AgeLessThan}(x, 18) \to \text{HardKnockout}(x, \text{UnderLegalAge})$ | Applicants under 18 years of age lack legal contracting capacity for credit agreements. |
| **`HKO_002`** | Non-Positive Income Knock-Out | $\forall x: \text{Applicant}(x) \land \text{MonthlyIncomeAtMost}(x, 0) \to \text{HardKnockout}(x, \text{ZeroOrNegativeIncome})$ | Applicants with zero or negative verified income cannot service ongoing credit debt. |
| **`HKO_003`** | Severe Credit Impairment Knock-Out | $\forall x: \text{Applicant}(x) \land \text{CreditScoreLessThan}(x, 550) \to \text{HardKnockout}(x, \text{SevereCreditImpairment})$ | Credit scores below 550 indicate severe delinquency, charge-offs, or active bankruptcy. |
| **`HKO_004`** | Recent Default Knock-Out | $\forall x: \text{Applicant}(x) \land \text{RecentDefaultOnRecord}(x) \to \text{HardKnockout}(x, \text{ActiveDefaultRecord})$ | Bureau records indicating active default within the past 24 months disqualify unsecured lending. |

---

## 2. Derivation Rules - Layer 1: Financial Attributes (Priority: 70-80)
Derives intermediate atomic facts regarding debt capacity, credit score tiers, employment stability, and repayment behavior.

| Rule ID | Rule Name | Priority | FOL Horn Clause | Action Asserted |
| :--- | :--- | :--- | :--- | :--- |
| **`DER_INC_01`** | Income Baseline Qualified | 80 | $\forall x: \text{Applicant}(x) \land \text{MonthlyIncomeAtLeast}(x, 30000) \to \text{IncomeSufficient}(x)$ | $\text{IncomeSufficient}(x)$ |
| **`DER_INC_02`** | Income Marginal Qualified | 75 | $\forall x: \text{Applicant}(x) \land \text{MonthlyIncomeBetween}(x, 20000, 30000) \to \text{IncomeMarginal}(x)$ | $\text{IncomeMarginal}(x)$ |
| **`DER_INC_03`** | Income Inadequate | 75 | $\forall x: \text{Applicant}(x) \land \text{MonthlyIncomeBetween}(x, 0.01, 20000) \to \text{IncomeInadequate}(x)$ | $\text{IncomeInadequate}(x)$ |
| **`DER_DTI_01`** | Prime DTI (&le; 40%) | 80 | $\forall x: \text{Applicant}(x) \land \text{DTIAtMost}(x, 0.40) \to \text{DTIOK}(x)$ | $\text{DTIOK}(x)$ |
| **`DER_DTI_02`** | Marginal DTI (40-50%) | 75 | $\forall x: \text{Applicant}(x) \land \text{DTIBetween}(x, 0.40, 0.50) \to \text{DTIMarginal}(x)$ | $\text{DTIMarginal}(x)$ |
| **`DER_DTI_03`** | Excessive DTI (> 50%) | 75 | $\forall x: \text{Applicant}(x) \land \text{DTIGreaterThan}(x, 0.50) \to \text{DTIExcessive}(x)$ | $\text{DTIExcessive}(x)$ |
| **`DER_CS_01`** | Prime Credit Score (&ge; 750) | 80 | $\forall x: \text{Applicant}(x) \land \text{CreditScoreAtLeast}(x, 750) \to \text{CreditPrime}(x)$ | $\text{CreditPrime}(x)$ |
| **`DER_CS_02`** | Near-Prime Score (650-749) | 75 | $\forall x: \text{Applicant}(x) \land \text{CreditScoreBetween}(x, 650, 749) \to \text{CreditNearPrime}(x)$ | $\text{CreditNearPrime}(x)$ |
| **`DER_CS_03`** | Subprime Score (550-649) | 75 | $\forall x: \text{Applicant}(x) \land \text{CreditScoreBetween}(x, 550, 649) \to \text{CreditSubprime}(x)$ | $\text{CreditSubprime}(x)$ |
| **`DER_EMP_01`** | Stable Employment (&ge; 2 yrs) | 80 | $\forall x: \text{Applicant}(x) \land \text{EmploymentYearsAtLeast}(x, 2.0) \to \text{EmploymentStable}(x)$ | $\text{EmploymentStable}(x)$ |
| **`DER_EMP_02`** | Short Employment (< 2 yrs) | 75 | $\forall x: \text{Applicant}(x) \land \text{EmploymentYearsLessThan}(x, 2.0) \to \text{EmploymentShort}(x)$ | $\text{EmploymentShort}(x)$ |
| **`DER_REP_01`** | Positive Repayment History | 80 | $\forall x: \text{Applicant}(x) \land \text{RepaymentPositive}(x) \to \text{RepaymentPositive}(x)$ | $\text{RepaymentPositive}(x)$ |
| **`DER_REP_02`** | Fair Repayment History | 75 | $\forall x: \text{Applicant}(x) \land \text{RepaymentIs}(x, \text{Fair}) \to \text{RepaymentFair}(x)$ | $\text{RepaymentFair}(x)$ |
| **`DER_REP_03`** | Poor Repayment History | 75 | $\forall x: \text{Applicant}(x) \land \text{RepaymentIs}(x, \text{Poor}) \to \text{RepaymentPoor}(x)$ | $\text{RepaymentPoor}(x)$ |
| **`DER_AFF_01`** | Requested EMI Affordable | 70 | $\forall x: \text{Applicant}(x) \land \text{RequestedEMILessThanMaxEMI}(x) \to \text{EMIAffordable}(x)$ | $\text{EMIAffordable}(x)$ |
| **`DER_AFF_02`** | Requested EMI Unaffordable | 70 | $\forall x: \text{Applicant}(x) \land \text{RequestedEMIGreaterThanMaxEMI}(x) \to \text{EMIUnaffordable}(x)$ | $\text{EMIUnaffordable}(x)$ |

---

## 3. Derivation Rules - Layer 2: Risk Classification (Priority: 50-60)

| Rule ID | Rule Name | Priority | FOL Horn Clause | Action Asserted |
| :--- | :--- | :--- | :--- | :--- |
| **`RSK_001`** | Low Risk Tier | 60 | $\forall x: \text{CreditPrime}(x) \land \text{DTIOK}(x) \land \text{EmploymentStable}(x) \land \text{RepaymentPositive}(x) \land \text{IncomeSufficient}(x) \to \text{RiskLevel}(x, \text{LOW})$ | $\text{RiskLevel}(x, \text{LOW})$ |
| **`RSK_002`** | Medium Risk Tier | 55 | $\forall x: \sim\text{RiskLevel}(x, \text{LOW}) \land \sim\text{CreditSubprime}(x) \land \sim\text{DTIExcessive}(x) \land \sim\text{RepaymentPoor}(x) \land \sim\text{IncomeInadequate}(x) \to \text{RiskLevel}(x, \text{MEDIUM})$ | $\text{RiskLevel}(x, \text{MEDIUM})$ |
| **`RSK_003`** | High Risk Tier | 50 | $\forall x: \sim\text{RiskLevel}(x, \text{LOW}) \land \sim\text{RiskLevel}(x, \text{MEDIUM}) \to \text{RiskLevel}(x, \text{HIGH})$ | $\text{RiskLevel}(x, \text{HIGH})$ |

---

## 4. Decision Rules - Layer 3: Terminal Eligibility (Priority: 20-40)

| Rule ID | Rule Name | Priority | FOL Horn Clause | Action Asserted |
| :--- | :--- | :--- | :--- | :--- |
| **`DEC_001`** | Hard Knockout Decision | 40 | $\forall x: \text{HardKnockout}(x, r) \to \text{FinalDecision}(x, \text{NOT\_ELIGIBLE})$ | $\text{FinalDecision}(x, \text{NOT\_ELIGIBLE})$ |
| **`DEC_002`** | Full Eligibility Decision | 30 | $\forall x: \sim\text{FinalDecision}(x) \land \sim\text{HardKnockout}(x) \land \text{IncomeSufficient}(x) \land \text{CreditPrime}(x) \land \text{DTIOK}(x) \land \text{EmploymentStable}(x) \land \text{RepaymentPositive}(x) \to \text{FinalDecision}(x, \text{ELIGIBLE})$ | $\text{FinalDecision}(x, \text{ELIGIBLE})$ |
| **`DEC_003`** | Conditional Eligibility Decision | 25 | $\forall x: \sim\text{HardKnockout}(x) \land \sim\text{FinalDecision}(x, \text{ELIGIBLE}) \land \text{CreditScoreAtLeast}(x, 650) \land \text{DTIAtMost}(x, 0.50) \land \text{MonthlyIncomeAtLeast}(x, 20000) \land \sim\text{RepaymentPoor}(x) \to \text{FinalDecision}(x, \text{CONDITIONALLY\_ELIGIBLE})$ | $\text{FinalDecision}(x, \text{CONDITIONALLY\_ELIGIBLE})$ |
| **`DEC_004`** | Fallback Decline Decision | 20 | $\forall x: \sim\text{FinalDecision}(x, \text{ELIGIBLE}) \land \sim\text{FinalDecision}(x, \text{CONDITIONALLY\_ELIGIBLE}) \to \text{FinalDecision}(x, \text{NOT\_ELIGIBLE})$ | $\text{FinalDecision}(x, \text{NOT\_ELIGIBLE})$ |
