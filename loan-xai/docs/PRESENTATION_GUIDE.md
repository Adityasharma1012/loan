# Presentation & Viva Voce Defense Guide
**Project:** Explainable Rule-Based Loan Eligibility & Credit Decision System  
**Course:** Artificial Intelligence Foundations (Section K4P25AT, Group 5)  
**Team Members:**  
- **Pilli Sreeja** (Reg. No. 12515392)  
- **Harshit Kumar Singh** (Reg. No. 12519334)  
- **Inaganti Hajmeer Vali** (Reg. No. 12521593)  
**Mentor:** Sheveta  
**Artifact Location:** `loan-xai/loan-xai-presentation.pptx`

---

## 1. Presentation Structure & 10–12 Minute Timing Budget

| Slide # | Slide Title | Speaker / Owner | Target Duration |
|:---:|:---|:---|:---:|
| **1** | Title & Project Statement | Pilli Sreeja | 0:45 min |
| **2** | Background & Problem Motivation | Pilli Sreeja | 0:45 min |
| **3** | End-to-End System Pipeline | Harshit Kumar Singh | 0:45 min |
| **4** | Project Objectives & Milestones | Harshit Kumar Singh | 0:45 min |
| **5** | Scope & System Boundaries | Harshit Kumar Singh | 0:40 min |
| **6** | Literature Review & Research Gap | Harshit Kumar Singh | 0:45 min |
| **7** | System Architecture & Tech Stack | Inaganti Hajmeer Vali | 0:50 min |
| **8** | Symbolic AI Core: Forward Chaining & FOL | Inaganti Hajmeer Vali | 1:15 min |
| **9** | Actuarial Loan Sizing & Counterfactuals | Inaganti Hajmeer Vali | 1:00 min |
| **10** | Live Application Storyboard (Screenshots) | Pilli Sreeja | 1:10 min |
| **11** | Empirical ML Comparison Benchmark | Harshit Kumar Singh | 1:05 min |
| **12** | Algorithmic Demographic Fairness Audit | Inaganti Hajmeer Vali | 1:00 min |
| **13** | Verification: 37/37 Pytest & Invariant Tests | Pilli Sreeja | 0:45 min |
| **14** | Conclusions & Core AI Takeaways | Pilli Sreeja | 0:45 min |
| **15** | Roadmap & Acknowledgements | All Team Members | 0:40 min |
| **16–18** | Appendix (Viva Defense, UI Gallery, Glossary) | Team (On demand during Q&A) | 3:00+ min |
| **TOTAL** | **Core Presentation (Slides 1–15)** | **Team Group 5** | **~11:00 min** |

---

## 2. Slide-by-Slide Delivery Script & Animation Plan

### Slide 1: Title Slide
- **Visuals:** Dark navy aesthetic (`#0B1B3F`), course header, project title, complete team table with registration numbers, mentor Sheveta, academic demonstration disclaimer.
- **Animation Entrance Plan:**
  - `[Load]`: Dark navy background with course banner and title.
  - `[Click 1]`: Fade in project team table and mentor card.
  - `[Click 2]`: Fade in institutional placeholders and academic disclaimer.
- **Spoken Script (Pilli Sreeja):**
  > "Good morning esteemed faculty evaluators and our project mentor Sheveta. Today, our team—Pilli Sreeja, Harshit Kumar Singh, and Inaganti Hajmeer Vali—is proud to present our capstone project for Artificial Intelligence Foundations: *Explainable Rule-Based Loan Eligibility and Credit Decision System*. In regulated consumer credit, black-box AI often fails because lenders are legally required to provide exact, auditable reasons for adverse credit decisions. Our system addresses this by combining production-rule expert systems and first-order predicate logic with empirical ML benchmarks and fairness auditing."
- **Hinglish Delivery Tip:**
  > *Yahan confident tone me shuru karein aur clearly state karein ki core system symbolic AI hai, aur ML comparison baseline hai.*

---

### Slide 2: The Explainability Imperative in Automated Lending
- **Visuals:** Split comparison: Left card (Black-Box Dilemma in Banking) vs Right card (Symbolic AI Advantage).
- **Animation Entrance Plan:**
  - `[Load]`: Slide header and container cards.
  - `[Click 1]`: Fade in left card detailing FCRA adverse action mandates, opaque neural nets, and lack of true counterfactuals.
  - `[Click 2]`: Fade in right card highlighting deterministic production rules, FOL proofs, and actuarial sizing.
- **Spoken Script (Pilli Sreeja):**
  > "Consider this analogy: if a physician refuses you a critical prescription, they don't say 'my neural network gave you an 82% risk score.' They explain specific biomarkers—blood sugar, enzyme levels—and tell you exactly how to lower them. In consumer credit, the law demands the same rigor under the Equal Credit Opportunity Act and FCRA. When banks use opaque neural networks, they cannot explain edge cases or prove non-discrimination. By applying Classical Symbolic AI, our system bridges this exact gap: every credit decision is mathematically deduced from production rules and first-order predicate logic, providing complete transparency and actionable counterfactual advice."
- **Hinglish Delivery Tip:**
  > *Yahan samjhayein ki bank me adverse action notice compulsory hota hai, isiliye symbolic AI ML se zyada reliable aur defensible hai.*

---

### Slide 3: System Pipeline: From Financial Inputs to Audited Verdict
- **Visuals:** 4 horizontal process cards: Stage 1 (Data & Quarantine), Stage 2 (Forward Chaining), Stage 3 (FOL Proof & Sizing), Stage 4 (Audit & Benchmark).
- **Animation Entrance Plan:**
  - `[Load]`: Header and 4 card outlines.
  - `[Click 1]`: Fade in Stage 1 & Stage 2 (Input sanitization and forward-chaining fixpoint).
  - `[Click 2]`: Fade in Stage 3 & Stage 4 (FOL Horn clause unification, annuity sizing, ML benchmark, and fairness audit).
- **Spoken Script (Harshit Kumar Singh):**
  > "Let us trace the end-to-end journey of a credit application through our architecture. In Stage 1, the applicant submits twelve purely financial attributes. Protected attributes like gender, caste, or religion are strictly quarantined at the architectural boundary. In Stage 2, working memory passes into our forward-chaining expert system, firing declarative production rules until a fixpoint is achieved. Stage 3 derives a formal First-Order Logic proof tree and applies actuarial annuity math to size the loan amount. Finally, Stage 4 benchmarks the decision against statistical models and executes an automated demographic fairness audit."
- **Hinglish Delivery Tip:**
  > *Bataiye ki ye end-to-end multi-tier pipeline hai jo input validation se lekar fairness audit tak smoothly run hoti hai.*

---

### Slide 4: Core Project Objectives & Verification Status
- **Visuals:** 5 structured cards with green verified badges `[✓ COMPLETED & VERIFIED]` for O1 through O5.
- **Animation Entrance Plan:**
  - `[Load]`: Slide header.
  - `[Click 1]`: Fly in Objectives O1, O2, O3 with their formal AI definitions.
  - `[Click 2]`: Fly in Objectives O4 and O5 with green completion checkmarks.
- **Spoken Script (Harshit Kumar Singh):**
  > "We formulated five strict, checkable academic objectives corresponding to the course project statement. Each objective has been fully implemented in our codebase and validated through our 37-test suite. Notice that we did not build a simple toy script; we developed a production-ready declarative rule engine, a true first-order logic proof generator, mathematical loan sizing, a comparative ML benchmark, and an algorithmic fairness auditor."
- **Hinglish Delivery Tip:**
  > *Faculty ko point out karein ki humne project requirement ke saare clauses ko 100% fulfill kiya hai.*

---

### Slide 5: Project Scope: Strict System Boundaries
- **Visuals:** Two-column card table: Left (In Scope - 6 green check items) vs Right (Out of Scope - 6 red X items).
- **Animation Entrance Plan:**
  - `[Load]`: Slide header and two column cards.
  - `[Click 1]`: Fade in In-Scope column (production rules, FOL proof trees, annuity sizing, full-stack UI).
  - `[Click 2]`: Fade in Out-of-Scope column (live bureau APIs, binding offers, unconstrained deep learning).
- **Spoken Script (Harshit Kumar Singh):**
  > "Setting clear engineering boundaries is essential for any applied AI project. In scope, we have delivered a full-stack, fully tested expert system with complete mathematical sizing and comparative ML benchmarks. By strict academic design, live bureau integrations, real-world customer PII, and actual financial disbursements are out of scope. Protected demographic attributes are strictly quarantined and never used in loan decisions."
- **Hinglish Delivery Tip:**
  > *Evaluators ko batayein ki academic integrity aur data privacy preserve karne ke liye humne boundaries cleanly define ki hain.*

---

### Slide 6: Comparative Analysis: Scorecards vs ML vs LoanXAI
- **Visuals:** 6-row matrix comparing Scorecards, Black-Box ML, and LoanXAI across Decision Mechanism, Auditability, Recourse, Edge-Cases, Quarantine, and Defensibility, plus Gap Callout Card.
- **Animation Entrance Plan:**
  - `[Load]`: Table headers and traditional columns.
  - `[Click 1]`: Highlight the LoanXAI column with tech accent styling.
  - `[Click 2]`: Fade in the bottom Research & Applied Gap callout.
- **Spoken Script (Harshit Kumar Singh):**
  > "When we examine the literature, traditional credit scorecards are too simple to capture complex edge cases, while modern machine learning models are too opaque to satisfy regulatory adverse action laws. As shown in our comparison matrix, LoanXAI occupies the sweet spot: by using formal Horn clause deduction and forward-chaining production rules, every verdict is mathematically verifiable, auditable, and transparent."
- **Hinglish Delivery Tip:**
  > *Gap highlight karein: scorecards outdated hain aur black-box ML illegal hai, isliye rule-based FOL expert system is the ideal regulatory solution.*

---

### Slide 7: Multi-Tier Layered Architecture & Protected Attribute Quarantine
- **Visuals:** Left card (6 architectural layers with quarantine firewall) and Right cards (Tech stack: React, FastAPI, Scikit-learn, ReportLab).
- **Animation Entrance Plan:**
  - `[Load]`: Left architectural layers container and right stack cards.
  - `[Click 1]`: Highlight Layer 3 (Protected Attribute Quarantine Boundary).
  - `[Click 2]`: Highlight Backend & Machine Learning stack capabilities.
- **Spoken Script (Inaganti Hajmeer Vali):**
  > "Our system architecture enforces clean separation of concerns across presentation, API, symbolic AI, actuarial math, and auditing tiers. A critical design highlight is the Protected Attribute Quarantine Boundary: demographic data is rejected at the underwriting API and restricted entirely to the synthetic audit engine. For technology, we selected FastAPI with Pydantic v2 for high-throughput async processing and strict schema enforcement, paired with a modern React frontend and ReportLab PDF generator."
- **Viva Voce Defense Cheat Sheet (Slide 7):**
  - **Q: Why did you choose FastAPI over Flask or Django?**  
    *A: FastAPI natively supports asynchronous execution (ASGI), automatic OpenAPI documentation, and strict runtime data validation through Pydantic v2, which guarantees zero type errors in financial inputs.*
  - **Q: How is the demographic data quarantined?**  
    *A: The loan evaluation endpoint schema rejects any demographic fields. Demographic features exist only in the offline synthetic dataset used exclusively by the fairness audit module.*

---

### Slide 8: Symbolic AI Core: Forward Chaining & FOL
- **Visuals:** Left card (Forward Chaining, 4-tier conflict resolution, Refraction) and Right card (Horn clauses, Ground atoms, Unification $\theta$, Proof trees, Negation-as-Failure).
- **Animation Entrance Plan:**
  - `[Load]`: Container cards.
  - `[Click 1]`: Fade in Forward Chaining inference loop and 4-tier conflict resolution order.
  - `[Click 2]`: Fade in First-Order Logic Horn clause, unification $\theta = \{x / \text{APP\_001}\}$, and Negation-as-Failure.
- **Spoken Script (Inaganti Hajmeer Vali):**
  > "The core AI of LoanXAI is a classical symbolic expert system. We implement forward chaining over a working memory of ground facts. At each cycle, the match phase builds a conflict set, which is resolved through our four-tier hierarchy: Hard Knockouts first, then salience priority, specificity, and a deterministic tie-breaker. To prevent infinite looping, we enforce the Refraction property—a rule fires at most once per fact set. Furthermore, every rule is formulated as a First-Order Logic Horn clause. Through variable unification and Negation-as-Failure, the system outputs a complete, auditable proof tree for every conclusion."
- **Viva Voce Defense Cheat Sheet (Slide 8):**
  - **Q: What is refraction and why is it necessary?**  
    *A: Refraction records every (rule_id, facts) tuple that has already fired. Without refraction, a rule whose conditions remain true in working memory would fire infinitely. Refraction guarantees the engine terminates at a deterministic fixpoint.*
  - **Q: Why represent rules as Horn clauses?**  
    *A: Horn clauses allow linear-time forward deduction (modus ponens) without exponential truth-table complexity, making inference fast, deterministic, and easily explainable as a tree.*

---

### Slide 9: Actuarial Loan Sizing, Risk Bands & Actionable Counterfactuals
- **Visuals:** 3 vertical cards: Actuarial Formulas (DTI, Max EMI, Annuity PV), Demonstration Thresholds (Prime, Conditional, Knockout), and Counterfactual Guidance.
- **Animation Entrance Plan:**
  - `[Load]`: Card outlines.
  - `[Click 1]`: Reveal Actuarial PV Annuity sizing formula and demonstration thresholds.
  - `[Click 2]`: Reveal Counterfactual guidance cases (Excessive DTI delta, Sub-prime delta).
- **Spoken Script (Inaganti Hajmeer Vali):**
  > "A unique strength of our system is how actuarial financial engineering integrates with symbolic logic. Rather than using arbitrary rule heuristics, we compute loan capacity using the actuarial annuity present value formula based on surplus monthly cash flow. When an applicant fails a condition, we do not simply output 'denied.' We generate deductive counterfactual hints: calculating the exact mathematical delta needed to qualify, such as reducing monthly debt by ₹4,000 or raising a credit score by 32 points."
- **Viva Voce Defense Cheat Sheet (Slide 9):**
  - **Q: Why calculate loan sizing using the annuity formula instead of a simple multiplier?**  
    *A: Simple income multipliers ignore loan tenure and interest rates. The annuity present value formula ensures that the monthly EMI will never exceed the applicant's maximum debt-service capability at the assigned interest band.*

---

### Slide 10: Working Application Storyboard
- **Visuals:** 5-step horizontal storyboard featuring real captured screenshots: Step 1 (Form), Step 2 (Results), Step 3 (Trace), Step 4 (FOL Proof), Step 5 (PDF Memo).
- **Animation Entrance Plan:**
  - `[Load]`: Header and 5 story card frames.
  - `[Click 1]`: Fade in Step 1 & Step 2 (Form validation & instant verdict).
  - `[Click 2]`: Fade in Step 3, Step 4 & Step 5 (Rule trace, FOL proof tree, and PDF memo).
- **Spoken Script (Pilli Sreeja):**
  > "Here you see the live, end-to-end storyboard captured directly from our running application. In Step 1, the applicant inputs twelve financial fields. Notice the field-level validation errors if inputs are out of bounds. In Step 2, the user submits the form and immediately sees their verdict—such as Prime Eligible—along with the recommended loan amount and interest band. In Steps 3 and 4, the user explores the complete Rule Inference Trace and First-Order Logic proof tree. Finally, Step 5 allows instantaneous export of a formal, auditable PDF underwriting memorandum."
- **Hinglish Delivery Tip:**
  > *Highlight karein ki ye real running full-stack app ke screenshots hain, koi mockup nahi.*

---

### Slide 11: Empirical Evaluation: Rule Engine vs Machine Learning
- **Visuals:** Left side: Real metrics table (Rule Engine 72.9% Acc / 0.818 F1; Decision Tree 70.0% Acc / 0.779 F1; Logistic Regression 81.3% Acc / 0.874 F1) and qualitative findings. Right side: Embedded screenshot of ML Benchmark page.
- **Animation Entrance Plan:**
  - `[Load]`: Slide header and cards.
  - `[Click 1]`: Highlight empirical metrics table comparing Rule Engine, Decision Tree, and Logistic Regression.
  - `[Click 2]`: Reveal qualitative comparison on auditability and regulatory defensibility.
- **Spoken Script (Harshit Kumar Singh):**
  > "A critical requirement of our AI project was comparing our symbolic expert system with machine learning models trained on 5,000 independent synthetic records. It is vital to note that the ML models were NOT trained on the rule engine's outputs; they were trained on an independent ground-truth repayment probability. As shown in our empirical evaluation table, Logistic Regression achieves 81.3% accuracy, but offers zero auditability. The Rule Engine achieves a strong 0.818 F1 score while guaranteeing 100% deterministic auditability and formal First-Order Logic proof trees."
- **Hinglish Delivery Tip:**
  > *Yahan emphasize karein ki ML baseline independent ground truth pe train hui hai, isliye evaluation completely fair aur scientifically valid hai.*

---

### Slide 12: Demographic Fairness Audit: Disparate Impact & Proxy Leakage
- **Visuals:** Left side: Demographic fairness table (Gender DI = 0.985 PASS; Age DI = 0.689 FLAGGED; Region DI = 0.915 PASS) and analysis. Right side: Embedded screenshot of Fairness Audit view.
- **Animation Entrance Plan:**
  - `[Load]`: Slide header and cards.
  - `[Click 1]`: Fade in demographic table and highlight the Age Band FLAGGED status (0.689).
  - `[Click 2]`: Fade in Proxy Leakage explanation and Kleinberg's Impossibility Theorem analysis.
- **Spoken Script (Inaganti Hajmeer Vali):**
  > "In Slide 12, we present our Algorithmic Fairness Audit across 5,000 synthetic records. Evaluating under the EEOC Four-Fifths rule, gender passes comfortably with a Disparate Impact Ratio of 0.985, and geography passes at 0.915. However, youth applicants show a disparate impact ratio of 0.689, triggering an automated audit flag. This demonstrates the classic 'Proxy Leakage' problem: even though age is not in the rules, employment stability naturally correlates with career stage. As Kleinberg's Impossibility Theorem proves, you cannot satisfy statistical parity and predictive parity simultaneously when base rates differ. We recommend introducing alternative data such as rent payment history."
- **Hinglish Delivery Tip:**
  > *Yahan explain karein ki algorithm intentionally biased nahi hai, balki employment duration feature indirectly age ke sath correlate kar raha hai (proxy leakage).*

---

### Slide 13: Empirical Verification: 37/37 Pytest Suite & Invariants
- **Visuals:** Left card: Test suite breakdown across 5 test modules + Proven Formal Invariants box. Right side: Real terminal image showing 37 passed tests in 2.77s.
- **Animation Entrance Plan:**
  - `[Load]`: Test breakdown card.
  - `[Click 1]`: Highlight the 3 Formal Invariants (Determinism, Order Invariance, Refraction).
  - `[Click 2]`: Reveal the authentic terminal screenshot with 37 passed tests.
- **Spoken Script (Pilli Sreeja):**
  > "Quality assurance and mathematical correctness were central to our development methodology. We created a comprehensive 37-test battery in Pytest covering rule firing, financial annuity math, FOL proof tree generation, API endpoints, and fairness audits. As shown on the right, all 37 tests execute and pass in under 3 seconds. Crucially, we wrote automated tests to prove three formal mathematical invariants: determinism across 100 runs, rule order invariance under permutation, and the refraction property."
- **Hinglish Delivery Tip:**
  > *Examiners ko batayein ki humne shuffling test kiya hai jisme YAML rules ka order badalne par bhi output identical rehta hai, proving robust conflict resolution.*

---

### Slide 14: Project Conclusions & Core Applied AI Takeaways
- **Visuals:** Left card (Deliverables Scorecard with 5 green checks) vs Right card (Academic Insights & Honest Limitations).
- **Animation Entrance Plan:**
  - `[Load]`: Header and cards.
  - `[Click 1]`: Reveal 5/5 completed milestones on the scorecard.
  - `[Click 2]`: Reveal academic insights on neuro-symbolic hybridization and limitations.
- **Spoken Script (Pilli Sreeja):**
  > "To conclude, our project has achieved 100% of the goals set out in the Artificial Intelligence Foundations course syllabus. We have proven that explainable, rule-based systems are not a relic of the past, but an essential component of modern high-stakes AI governance. Our key takeaway is that the future of banking AI is neuro-symbolic: combining the predictive power of machine learning with the deterministic, uncompromised safety guardrails of symbolic logic."
- **Hinglish Delivery Tip:**
  > *Yahan confident summary dekar conclude karein ki symbolic AI aur ML ka comparison humne comprehensively establish kiya hai.*

---

### Slide 15: Roadmap & Project Team Acknowledgements
- **Visuals:** Dark navy slide (`#0B1B3F`). Left card: Four technical extensions. Right card: Acknowledgement of mentor Sheveta, complete team roster, and Q&A invitation.
- **Animation Entrance Plan:**
  - `[Load]`: Dark background and roadmap title.
  - `[Click 1]`: Fade in Four Technical Extensions card.
  - `[Click 2]`: Fade in Mentor Acknowledgement, Team Members list, and Q&A invite.
- **Spoken Script (All Team Members):**
  > "To conclude our presentation, we have outlined four exciting future directions, including Inductive Logic Programming to semi-automatically discover rules, and Rete algorithm optimization for high-frequency banking. On behalf of my teammates Pilli Sreeja, Harshit Kumar Singh, and Inaganti Hajmeer Vali, we thank our mentor Sheveta and the evaluators for their time. We are now ready to demonstrate the live application and address any technical questions."
- **Hinglish Delivery Tip:**
  > *Polite aur confident tone me conclude karein: 'Thank you mentor Sheveta and evaluators. We are now open for Q&A.'*

---

## 3. Comprehensive Viva Voce Defense Cheat Sheet (10 High-Yield Questions)

| # | Faculty Question | Comprehensive Technical Answer |
|:---:|:---|:---|
| **1** | **Why forward chaining instead of backward chaining?** | *In consumer loan underwriting, all applicant facts (income, debt, credit score) are submitted upfront simultaneously. Forward chaining is data-driven, deriving all intermediate facts (affordability, risk class) and reaching a final verdict in a single, predictable forward pass without goal backtracking overhead.* |
| **2** | **What is Refraction and why is it critical?** | *Refraction ensures that an instantiated rule instance fires at most once on a given fact set. Without refraction, if rule conditions remain true in working memory, the rule would enter the conflict set repeatedly, causing an infinite loop. Refraction guarantees the engine terminates at a deterministic fixpoint.* |
| **3** | **How do you handle negation in First-Order Logic?** | *We implement Negation-as-Failure (NAF) under the closed-world assumption. For example, `NOT DefaultOnRecord(x)` evaluates to true if and only if no ground atom `DefaultOnRecord(APP_001)` exists or can be derived in working memory.* |
| **4** | **Why use Annuity Present Value instead of a flat income multiple?** | *Flat multipliers (e.g. 10x monthly income) ignore interest rate compounding and tenure duration. The annuity present value formula $PV = \text{Max EMI} \times \frac{1 - (1+r)^{-n}}{r}$ mathematically ensures the resulting monthly installment exactly matches the applicant's surplus cash flow at the approved interest rate band.* |
| **5** | **How do you mathematically guarantee that rule order does not affect the decision?** | *Through our 4-tier conflict resolution hierarchy: (1) Knockouts, (2) Rule Priority, (3) Condition Specificity, and (4) Deterministic Rule ID. The conflict set is sorted according to this total order before the highest-ranked rule is selected. We verify this via pytest by shuffling `rules.yaml` order and confirming identical execution traces.* |
| **6** | **Why didn't you train the ML models directly on the Rule Engine's outputs?** | *If an ML classifier is trained on rule engine outputs, it merely learns to approximate the rules, rendering comparative evaluation tautological. Instead, our synthetic data generator simulates an independent probabilistic repayment process, allowing a genuine comparison between symbolic rules and statistical generalization.* |
| **7** | **What is Disparate Impact and what threshold constitutes legal discrimination?** | *Disparate Impact occurs when a facially neutral policy disproportionately harms a protected group. Under the EEOC Four-Fifths rule, if the selection rate of any demographic group is less than 80% (0.80) of the highest group's rate, it is flagged as potential systemic discrimination.* |
| **8** | **How did your system detect Proxy Leakage?** | *Even though age was quarantined from underwriting rules, the Youth group had a Disparate Impact Ratio of 0.689 (< 0.80). This happened because employment duration ($\ge 2$ years) and credit history depth correlate heavily with age, demonstrating how neutral credit variables leak protected demographic status.* |
| **9** | **What is Kleinberg's Impossibility Theorem?** | *Kleinberg et al. (2016) proved mathematically that three common fairness criteria—statistical parity, predictive parity (calibration), and equal opportunity—cannot be satisfied simultaneously unless base default rates across groups are identical or prediction is 100% perfect.* |
| **10** | **How does your counterfactual generator work?** | *Because our rules are declarative with explicit mathematical boundaries, the counterfactual engine computes the exact distance vector $\vec{\delta} = \vec{\theta}_{\text{threshold}} - \vec{x}_{\text{fact}}$ for every unsatisfied antecedent, returning actionable guidance such as 'Reduce debt by ₹4,000' or 'Raise score by 32 points.'* |

---

## 4. User Fill-in Checklist (Placeholders)
Before presenting, update the bracketed items in Slide 1 and Slide 15:
- `[College / University Name]` (e.g., *Lovely Professional University*, *National Institute of Technology*, etc.)
- `[Presentation Date: Month Year]` (e.g., *November 2026*)

---

## 5. Live Demonstration Instructions
To run the live demonstration during Q&A:
1. **Backend Server:**
   ```bash
   cd loan-xai/backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
2. **Frontend UI:**
   ```bash
   cd loan-xai/frontend
   npm run dev -- --host 127.0.0.1 --port 5173
   ```
3. Open `http://127.0.0.1:5173` in your browser.
4. Use the Preset Buttons on the **New Application** page:
   - Preset 1: *Prime Eligible* (₹500,000 @ 9.5%, Prime rate band).
   - Preset 2: *Near-Prime Conditional* (DTI soft breach, reduced loan sizing).
   - Preset 3: *Excessive DTI Knockout* (Rejection with counterfactual debt reduction guidance).
