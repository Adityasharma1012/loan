# Algorithmic Fairness & Bias Auditing Methodology
**Course**: Artificial Intelligence Foundations  
**System**: Explainable Rule-Based Loan Eligibility & Credit Decision System (`loan-xai`)

---

## 1. Demographic Groups & Quarantined Attributes

To ensure complete fairness-safe input design in accordance with fair lending principles (e.g. US Equal Credit Opportunity Act, EU AI Act), **no protected attributes are solicited on the credit application form or passed to the underwriting feature matrix**.

Protected demographic attributes exist **exclusively in the synthetic audit dataset** to enable post-hoc algorithmic disparity reviews:
1. **Gender**: `Male` (Privileged reference), `Female`, `Non-binary`.
2. **Region Type**: `Urban` (Privileged reference), `Semi-Urban`, `Rural`.
3. **Age Bracket**: `26-40` (Privileged reference), `18-25`, `41-60`, `60+`.

---

## 2. Intentional Structural Disparities in the Synthetic Generator

To ensure the fairness audit evaluates real demographic disparities rather than trivial uniform noise, realistic historical socio-economic disparities were modeled:
- **Rural Thin-File Bureau Effect**: Rural applicants have historically lower penetration of formal banking credit lines, resulting in a simulated downward shift of approximately 25 points in formal bureau credit scores.
- **Historical Gender Pay Disparity**: Older female cohorts reflect historical legacy wage differentials (~10%), which test whether absolute nominal income floors (₹30,000) introduce disparate impact.

---

## 3. Mathematical Fairness Formulations

Let $A \in \{a, \text{privileged}\}$ denote group membership, $\hat{Y} \in \{0, 1\}$ the model or rule decision (1 = Approved), and $Y \in \{0, 1\}$ the independent true repayment outcome.

### 3.1 Selection Rate (Approval Rate)
$$SR(A=a) = P(\hat{Y}=1 \mid A=a)$$

### 3.2 Disparate Impact Ratio (DIR)
Derived from the US EEOC 80% (Four-Fifths) Rule:
$$DIR(a) = \frac{SR(A=a)}{SR(A=\text{privileged})}$$
- **Statutory Flag**: If $DIR < 0.80$, the system flags a potential disparate impact violation requiring institutional review.

### 3.3 Statistical Parity Difference (SPD)
$$SPD(a) = SR(A=a) - SR(A=\text{privileged})$$
- Measures the absolute gap in selection rates. Ideal parity is $0.0$.

### 3.4 True Positive Rate & Equal Opportunity Difference (EOD)
$$TPR(a) = P(\hat{Y}=1 \mid Y=1, A=a)$$
$$EOD(a) = TPR(A=a) - TPR(A=\text{privileged})$$
- Assesses whether creditworthy individuals across all demographic groups have equal probabilities of being approved.

### 3.5 Error Rates (FPR and FNR)
- **False Positive Rate (FPR)**: $P(\hat{Y}=1 \mid Y=0, A=a)$ (Approving a borrower who defaults).
- **False Negative Rate (FNR)**: $P(\hat{Y}=0 \mid Y=1, A=a)$ (Wrongly denying a creditworthy applicant).

---

## 4. Small Sample Size Censoring ($n < 30$)

Subgroups with sample sizes $n < 30$ (e.g. Non-binary applicants in small test batches) exhibit extreme statistical sampling variance:
- When $n < 30$, the system activates `small_sample_warning = True`.
- Disparate impact violation flags are caveated to prevent misleading inferences from small-sample noise.

---

## 5. Proxy Feature Leakage Analysis

Even when protected demographic attributes are quarantined, non-protected underwriting variables can act as mathematical proxies:
1. **Credit Score as Regional Proxy**: Thin-file penalties in rural areas mean strict credit score minimums (750 prime cutoff) indirectly depress rural selection rates.
2. **Gross Income as Gender Proxy**: Rigid nominal income thresholds (₹30,000) replicate historical wage disparities across gender lines.

---

## 6. Actionable Mitigation Guidance
1. **Calibrate Alternative Underwriting Pathways**: Introduce utility and telecommunications payment histories for rural applicants to build creditworthiness outside traditional bureau files.
2. **Shift Weight from Nominal Income to DTI**: Proportional debt service capacity (DTI $\le 40\%$) avoids penalizing lower-income demographics with sound debt management.
3. **Structured Human-in-the-Loop Review**: Route borderline conditional applications from historically disadvantaged cohorts to senior credit committees with standardized discretionary mitigation checklists.

---

## 7. Theoretical & Regulatory Limitations

- **Impossibility Theorem of Fairness**: Mathematical theorems (Kleinberg et al., 2016; Chouldechova, 2017) prove that Demographic Parity, Equalized Odds, and Predictive Parity are mutually incompatible when base default rates differ across groups.
- **Synthetic Data Disclaimer**: Metrics reflect the synthetic data generating process and do not represent actual institutional lending portfolios.
- **Regulatory Status**: This audit provides diagnostic parity metrics and does not constitute formal legal counsel or statutory non-discrimination certification.
