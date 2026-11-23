"""Production Rule Engine with Forward Chaining, Conflict Resolution,
Refraction, First-Order Logic Integration, and Full Execution Tracing.
"""

from typing import Dict, Any, List, Set, Optional, Tuple
import os
import copy
import yaml
from pathlib import Path

from app.logic.financial import (
    calculate_dti,
    calculate_max_emi,
    calculate_monthly_emi,
    calculate_annuity_principal,
    calculate_recommended_loan,
    generate_counterfactual_hints,
)
from app.logic.fol import GroundAtom, ProofNode, FOLProofTreeBuilder


class RuleEngine:
    """Deterministic forward-chaining expert system engine."""

    def __init__(self, rules_path: Optional[str] = None, thresholds_path: Optional[str] = None):
        base_dir = Path(__file__).resolve().parent.parent / "config"
        self.rules_path = Path(rules_path) if rules_path else base_dir / "rules.yaml"
        self.thresholds_path = Path(thresholds_path) if thresholds_path else base_dir / "thresholds.yaml"
        
        self.rules_config: Dict[str, Any] = {}
        self.thresholds_config: Dict[str, Any] = {}
        self.rules_list: List[Dict[str, Any]] = []
        self.load_configurations()

    def load_configurations(self):
        """Loads and parses the YAML declarative configurations."""
        with open(self.thresholds_path, "r", encoding="utf-8") as f:
            self.thresholds_config = yaml.safe_load(f)

        with open(self.rules_path, "r", encoding="utf-8") as f:
            self.rules_config = yaml.safe_load(f)
            self.rules_list = self.rules_config.get("rules", [])

    def evaluate(self, applicant_data: Dict[str, Any], shuffle_rules: bool = False) -> Dict[str, Any]:
        """Evaluates an applicant payload through forward-chaining to a fixpoint.
        
        Guarantees:
        - Determinism: identical outputs and trace across invocations.
        - Order invariance: rule order shuffling does not alter the conflict resolution or outcome.
        - Refraction: each rule fires at most once per applicant run.
        """
        applicant_id = applicant_data.get("applicant_id", "applicant_1")
        proof_builder = FOLProofTreeBuilder(applicant_id)

        # 1. Initialize Working Memory Facts
        working_memory_facts: Set[str] = set()
        working_memory_atoms: Dict[str, GroundAtom] = {}

        def assert_fact(atom: GroundAtom, is_input: bool = False, desc: str = "Input Fact"):
            key = f"{atom.predicate}:{','.join(str(a) for a in atom.args)}"
            working_memory_facts.add(key)
            working_memory_atoms[key] = atom
            if is_input:
                proof_builder.add_ground_fact(atom, desc)

        # Extract numerical & categorical inputs
        age = int(applicant_data.get("age", 0))
        monthly_income = float(applicant_data.get("monthly_income", 0.0))
        existing_debt = float(applicant_data.get("existing_monthly_debt", 0.0))
        credit_score = int(applicant_data.get("credit_score", 300))
        employment_years = float(applicant_data.get("employment_years", 0.0))
        repayment_history = str(applicant_data.get("repayment_history", "Fair"))
        recent_default = bool(applicant_data.get("recent_default", False))
        requested_amount = float(applicant_data.get("requested_amount", 100000.0))
        requested_tenure = int(applicant_data.get("requested_tenure_months", 36))

        # Computed derived financial inputs
        dti = calculate_dti(existing_debt, monthly_income)
        max_emi = calculate_max_emi(monthly_income, existing_debt)
        
        # Initial estimate rate (using Medium rate for initial EMI check)
        initial_rate = self.thresholds_config.get("interest_rate_bands", {}).get("MEDIUM", {}).get("base_rate", 0.125)
        requested_emi = calculate_monthly_emi(requested_amount, initial_rate, requested_tenure)

        # Assert raw ground facts into working memory
        assert_fact(GroundAtom("Applicant", (applicant_id,)), True, "Applicant Registration")
        assert_fact(GroundAtom("Age", (applicant_id, age)), True, "Verified Applicant Age")
        assert_fact(GroundAtom("MonthlyIncome", (applicant_id, monthly_income)), True, "Verified Monthly Gross Income")
        assert_fact(GroundAtom("ExistingMonthlyDebt", (applicant_id, existing_debt)), True, "Existing Monthly Debt Obligations")
        assert_fact(GroundAtom("CreditScore", (applicant_id, credit_score)), True, "Bureau Credit Score")
        assert_fact(GroundAtom("EmploymentYears", (applicant_id, employment_years)), True, "Continuous Employment Duration")
        assert_fact(GroundAtom("RepaymentHistory", (applicant_id, repayment_history)), True, "Historical Repayment Rating")
        assert_fact(GroundAtom("RequestedAmount", (applicant_id, requested_amount)), True, "Requested Loan Principal")
        assert_fact(GroundAtom("RequestedTenureMonths", (applicant_id, requested_tenure)), True, "Requested Loan Tenure in Months")
        assert_fact(GroundAtom("CalculatedDTI", (applicant_id, dti)), True, "Computed Debt-to-Income Ratio")
        assert_fact(GroundAtom("CalculatedMaxEMI", (applicant_id, max_emi)), True, "Computed Maximum Affordable EMI")

        if recent_default:
            assert_fact(GroundAtom("RecentDefaultOnRecord", (applicant_id,)), True, "Bureau Default Flag Active")

        # Working context dictionary for dynamic condition checks
        context = {
            "applicant_id": applicant_id,
            "age": age,
            "monthly_income": monthly_income,
            "existing_debt": existing_debt,
            "credit_score": credit_score,
            "employment_years": employment_years,
            "repayment_history": repayment_history,
            "recent_default": recent_default,
            "requested_amount": requested_amount,
            "requested_tenure": requested_tenure,
            "dti": dti,
            "max_emi": max_emi,
            "requested_emi": requested_emi,
        }

        # 2. Forward Chaining Cycle with Refraction & Conflict Resolution
        fired_rules: Set[str] = set()
        execution_trace: List[Dict[str, Any]] = []
        step_number = 1

        active_rules = list(self.rules_list)
        if shuffle_rules:
            # Used for testing rule order independence
            import random
            random.Random(42).shuffle(active_rules)

        max_iterations = 50  # Fixpoint safety bound

        for _ in range(max_iterations):
            # A. Match Phase: Build Conflict Set
            conflict_set = []

            for rule in active_rules:
                rule_id = rule["id"]
                if rule_id in fired_rules:
                    continue  # Refraction: rule fires at most once

                matches, matched_ground_atoms, actual_values = self._check_conditions(
                    rule["conditions"], context, working_memory_facts, applicant_id
                )

                if matches:
                    conflict_set.append({
                        "rule": rule,
                        "matched_atoms": matched_ground_atoms,
                        "actual_values": actual_values,
                    })

            if not conflict_set:
                break  # Fixpoint reached: no active rule premises match

            # B. Conflict Resolution Phase
            # Hierarchy:
            # 1. Rule category: hard_knockout first (type == 'hard_knockout' -> priority 0 in sort)
            # 2. Priority/salience descending
            # 3. Specificity: number of conditions descending
            # 4. Rule ID ascending (deterministic tie-break)
            def conflict_sort_key(item):
                r = item["rule"]
                is_hko = 0 if r.get("rule_type") == "hard_knockout" else 1
                priority = -int(r.get("priority", 0))
                specificity = -len(r.get("conditions", []))
                rule_id = str(r.get("id", ""))
                return (is_hko, priority, specificity, rule_id)

            conflict_set.sort(key=conflict_sort_key)

            # Pick winner
            winner = conflict_set[0]
            winning_rule = winner["rule"]
            rule_id = winning_rule["id"]

            # Record why this rule was chosen over competing candidates in the conflict set
            competitors_info = []
            for candidate in conflict_set:
                cand_r = candidate["rule"]
                competitors_info.append({
                    "rule_id": cand_r["id"],
                    "rule_type": cand_r.get("rule_type"),
                    "priority": cand_r.get("priority"),
                    "condition_count": len(cand_r.get("conditions", [])),
                })

            resolution_reason = (
                f"Selected '{rule_id}' ({winning_rule['name']}) based on: "
                f"type='{winning_rule.get('rule_type')}', priority={winning_rule.get('priority')}, "
                f"specificity={len(winning_rule.get('conditions', []))} conditions, "
                f"tie-break id='{rule_id}'."
            )

            # C. Fire Phase: Assert Actions
            asserted_atoms_for_step = []
            for action in winning_rule.get("actions", []):
                assert_name = action["assert"]
                raw_args = action.get("args", [])
                
                # Substitute 'x' with applicant_id
                bound_args = tuple(applicant_id if a == "x" else a for a in raw_args)
                new_atom = GroundAtom(predicate=assert_name, args=bound_args)
                
                assert_fact(new_atom)
                asserted_atoms_for_step.append(new_atom)

                # Link into FOL derivation proof tree
                proof_builder.add_derivation(
                    conclusion=new_atom,
                    rule_id=rule_id,
                    rule_name=winning_rule["name"],
                    fol_form=winning_rule.get("fol_form", ""),
                    plain_english=winning_rule.get("plain_english", ""),
                    premise_atoms=winner["matched_atoms"],
                )

            # Mark fired (refraction)
            fired_rules.add(rule_id)

            # Record step in execution history trace
            execution_trace.append({
                "step": step_number,
                "rule_id": rule_id,
                "rule_name": winning_rule["name"],
                "rule_type": winning_rule.get("rule_type"),
                "priority": winning_rule.get("priority"),
                "fol_form": winning_rule.get("fol_form"),
                "plain_english": winning_rule.get("plain_english"),
                "matched_facts": [a.to_dict() for a in winner["matched_atoms"]],
                "actual_input_values": winner["actual_values"],
                "asserted_facts": [a.to_dict() for a in asserted_atoms_for_step],
                "conflict_set_size": len(conflict_set),
                "competing_rules": competitors_info,
                "resolution_reason": resolution_reason,
            })

            step_number += 1

        # 3. Derive Final Synthesis & Product Recommendations
        return self._build_final_synthesis(
            context=context,
            working_memory_facts=working_memory_facts,
            execution_trace=execution_trace,
            proof_builder=proof_builder,
        )

    def _check_conditions(
        self,
        conditions: List[Dict[str, Any]],
        context: Dict[str, Any],
        facts: Set[str],
        applicant_id: str,
    ) -> Tuple[bool, List[GroundAtom], Dict[str, Any]]:
        """Evaluates condition list against working memory and applicant context.
        Supports Negation-As-Failure (NOT_HAS / absence of fact).
        """
        matched_atoms: List[GroundAtom] = []
        actual_values: Dict[str, Any] = {}

        for cond in conditions:
            pred = cond["predicate"]
            args = cond.get("args", [])

            # Check special meta-predicates
            if pred == "HAS":
                target_pred = args[0]
                target_args = [applicant_id if a == "x" else a for a in args[1:]]
                prefix = f"{target_pred}:{','.join(str(a) for a in target_args)}" if target_args else f"{target_pred}:"
                has_match = any(f == prefix or f.startswith(f"{prefix},") or f.startswith(f"{prefix}:") or (len(target_args) == 0 and f.startswith(f"{target_pred}:")) for f in facts)
                if not has_match:
                    return False, [], {}
                matched_atoms.append(GroundAtom("FactPresent", (target_pred,)))

            elif pred == "NOT_HAS":
                target_pred = args[0]
                target_args = [applicant_id if a == "x" else a for a in args[1:]]
                prefix = f"{target_pred}:{','.join(str(a) for a in target_args)}" if target_args else f"{target_pred}:"
                has_match = any(f == prefix or f.startswith(f"{prefix},") or f.startswith(f"{prefix}:") or (len(target_args) == 0 and f.startswith(f"{target_pred}:")) for f in facts)
                if has_match:
                    return False, [], {}  # Negation failed
                # Negation-as-failure succeeds
                matched_atoms.append(GroundAtom("NegationAsFailure", (target_pred,)))

            # Evaluated Predicates
            elif pred == "AgeLessThan":
                threshold = args[1]
                actual_values["age"] = context["age"]
                if not (context["age"] < threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("AgeLessThan", (applicant_id, threshold), context["age"]))

            elif pred == "MonthlyIncomeAtMost":
                threshold = args[1]
                actual_values["monthly_income"] = context["monthly_income"]
                if not (context["monthly_income"] <= threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("MonthlyIncomeAtMost", (applicant_id, threshold), context["monthly_income"]))

            elif pred == "MonthlyIncomeAtLeast":
                threshold = args[1]
                actual_values["monthly_income"] = context["monthly_income"]
                if not (context["monthly_income"] >= threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("MonthlyIncomeAtLeast", (applicant_id, threshold), context["monthly_income"]))

            elif pred == "MonthlyIncomeBetween":
                low, high = args[1], args[2]
                actual_values["monthly_income"] = context["monthly_income"]
                if not (low <= context["monthly_income"] < high):
                    return False, [], {}
                matched_atoms.append(GroundAtom("MonthlyIncomeBetween", (applicant_id, low, high), context["monthly_income"]))

            elif pred == "CreditScoreLessThan":
                threshold = args[1]
                actual_values["credit_score"] = context["credit_score"]
                if not (context["credit_score"] < threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("CreditScoreLessThan", (applicant_id, threshold), context["credit_score"]))

            elif pred == "CreditScoreAtLeast":
                threshold = args[1]
                actual_values["credit_score"] = context["credit_score"]
                if not (context["credit_score"] >= threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("CreditScoreAtLeast", (applicant_id, threshold), context["credit_score"]))

            elif pred == "CreditScoreBetween":
                low, high = args[1], args[2]
                actual_values["credit_score"] = context["credit_score"]
                if not (low <= context["credit_score"] <= high):
                    return False, [], {}
                matched_atoms.append(GroundAtom("CreditScoreBetween", (applicant_id, low, high), context["credit_score"]))

            elif pred == "RecentDefaultOnRecord":
                actual_values["recent_default"] = context["recent_default"]
                if not context["recent_default"]:
                    return False, [], {}
                matched_atoms.append(GroundAtom("RecentDefaultOnRecord", (applicant_id,), True))

            elif pred == "DTIAtMost":
                threshold = args[1]
                actual_values["dti"] = context["dti"]
                if not (context["dti"] <= threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("DTIAtMost", (applicant_id, threshold), context["dti"]))

            elif pred == "DTIBetween":
                low, high = args[1], args[2]
                actual_values["dti"] = context["dti"]
                if not (low < context["dti"] <= high):
                    return False, [], {}
                matched_atoms.append(GroundAtom("DTIBetween", (applicant_id, low, high), context["dti"]))

            elif pred == "DTIGreaterThan":
                threshold = args[1]
                actual_values["dti"] = context["dti"]
                if not (context["dti"] > threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("DTIGreaterThan", (applicant_id, threshold), context["dti"]))

            elif pred == "EmploymentYearsAtLeast":
                threshold = args[1]
                actual_values["employment_years"] = context["employment_years"]
                if not (context["employment_years"] >= threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("EmploymentYearsAtLeast", (applicant_id, threshold), context["employment_years"]))

            elif pred == "EmploymentYearsLessThan":
                threshold = args[1]
                actual_values["employment_years"] = context["employment_years"]
                if not (context["employment_years"] < threshold):
                    return False, [], {}
                matched_atoms.append(GroundAtom("EmploymentYearsLessThan", (applicant_id, threshold), context["employment_years"]))

            elif pred == "RepaymentHistoryIn":
                allowed = args[1]
                actual_values["repayment_history"] = context["repayment_history"]
                if context["repayment_history"] not in allowed:
                    return False, [], {}
                matched_atoms.append(GroundAtom("RepaymentHistoryIn", (applicant_id, tuple(allowed)), context["repayment_history"]))

            elif pred == "RepaymentHistoryIs":
                target = args[1]
                actual_values["repayment_history"] = context["repayment_history"]
                if context["repayment_history"] != target:
                    return False, [], {}
                matched_atoms.append(GroundAtom("RepaymentHistoryIs", (applicant_id, target), context["repayment_history"]))

            elif pred == "RequestedEMILessThanMaxEMI":
                actual_values["requested_emi"] = context["requested_emi"]
                actual_values["max_emi"] = context["max_emi"]
                if not (context["requested_emi"] <= context["max_emi"]):
                    return False, [], {}
                matched_atoms.append(GroundAtom("RequestedEMILessThanMaxEMI", (applicant_id,), True))

            elif pred == "RequestedEMIGreaterThanMaxEMI":
                actual_values["requested_emi"] = context["requested_emi"]
                actual_values["max_emi"] = context["max_emi"]
                if not (context["requested_emi"] > context["max_emi"]):
                    return False, [], {}
                matched_atoms.append(GroundAtom("RequestedEMIGreaterThanMaxEMI", (applicant_id,), True))

            else:
                # General atom check in working memory
                bound_args = tuple(applicant_id if a == "x" else a for a in args)
                exact_key = f"{pred}:{','.join(str(a) for a in bound_args)}"
                if exact_key in facts:
                    matched_atoms.append(GroundAtom(pred, bound_args))
                else:
                    return False, [], {}

        return True, matched_atoms, actual_values

    def _build_final_synthesis(
        self,
        context: Dict[str, Any],
        working_memory_facts: Set[str],
        execution_trace: List[Dict[str, Any]],
        proof_builder: FOLProofTreeBuilder,
    ) -> Dict[str, Any]:
        """Synthesizes final loan recommendation, interest band, conditions,
        ranked reasons, and counterfactual explanations.
        """
        applicant_id = context["applicant_id"]
        
        # 1. Decision Status
        decision = "NOT_ELIGIBLE"
        has_knockout = any(f.startswith(f"HardKnockout:{applicant_id}") for f in working_memory_facts)
        if has_knockout or f"FinalDecision:{applicant_id},NOT_ELIGIBLE" in working_memory_facts:
            decision = "NOT_ELIGIBLE"
        elif f"FinalDecision:{applicant_id},ELIGIBLE" in working_memory_facts:
            decision = "ELIGIBLE"
        elif f"FinalDecision:{applicant_id},CONDITIONALLY_ELIGIBLE" in working_memory_facts:
            decision = "CONDITIONALLY_ELIGIBLE"
        else:
            decision = "NOT_ELIGIBLE"

        # 2. Risk Tier
        risk_class = "HIGH"
        if f"RiskLevel:{applicant_id},LOW" in working_memory_facts:
            risk_class = "LOW"
        elif f"RiskLevel:{applicant_id},MEDIUM" in working_memory_facts:
            risk_class = "MEDIUM"
        elif f"RiskLevel:{applicant_id},HIGH" in working_memory_facts:
            risk_class = "HIGH"

        # 3. Interest Rate Band
        bands = self.thresholds_config.get("interest_rate_bands", {})
        band_info = bands.get(risk_class, bands.get("HIGH", {}))
        annual_rate = band_info.get("base_rate", 0.14)
        rate_band_label = band_info.get("label", "14.0% - 18.0%")

        # 4. Tenure Recommendation
        suggested_tenure = context["requested_tenure"]
        conditions_list = []
        if decision == "CONDITIONALLY_ELIGIBLE":
            cond_max_tenure = self.thresholds_config.get("tenure_constraints", {}).get("conditional_max_tenure_months", 36)
            if suggested_tenure > cond_max_tenure:
                suggested_tenure = cond_max_tenure
                conditions_list.append(f"Tenure capped at {cond_max_tenure} months due to near-prime risk tier.")
            
            if context["dti"] > 0.40:
                conditions_list.append("Mandatory secondary guarantor or co-borrower required due to DTI exceeding 40%.")
            if context["credit_score"] < 750:
                conditions_list.append("30% haircut applied on requested principal to maintain prudent debt coverage.")
            if context["employment_years"] < 2.0:
                conditions_list.append("Employer verification certificate and 6-month continuous bank statement required.")

        # 5. Loan Amount Calculations
        is_conditional = (decision == "CONDITIONALLY_ELIGIBLE")
        calc_result = calculate_recommended_loan(
            requested_amount=context["requested_amount"],
            monthly_income=context["monthly_income"],
            existing_monthly_debt=context["existing_debt"],
            annual_interest_rate=annual_rate,
            tenure_months=suggested_tenure,
            is_conditional=is_conditional,
            income_multiplier_cap=self.thresholds_config.get("affordability", {}).get("max_income_loan_multiplier", 36.0),
            conditional_haircut=self.thresholds_config.get("affordability", {}).get("conditional_amount_multiplier", 0.70),
        )

        recommended_amount = calc_result["recommended_amount"] if decision != "NOT_ELIGIBLE" else 0.0
        recommended_emi = calc_result["recommended_emi"] if decision != "NOT_ELIGIBLE" else 0.0

        # 6. Extract Knock-outs & Rejection Reasons
        rejection_reasons = []
        for fact in working_memory_facts:
            if fact.startswith("NotEligibleReason:"):
                # e.g. NotEligibleReason:applicant_1,Reason text
                parts = fact.split(":", 1)[1].split(",", 1)
                if len(parts) > 1:
                    rejection_reasons.append(parts[1])

        if decision == "NOT_ELIGIBLE" and not rejection_reasons:
            if context["credit_score"] < 650:
                rejection_reasons.append("Credit score does not meet minimum conditional threshold of 650.")
            if context["dti"] > 0.50:
                rejection_reasons.append("Debt-to-Income ratio exceeds maximum permissible cap of 50%.")
            if context["monthly_income"] < 20000:
                rejection_reasons.append("Verified monthly income is below minimum conditional cutoff of ₹20,000.")
            if context["repayment_history"] == "Poor":
                rejection_reasons.append("History of past credit delinquency or charge-offs.")

        # 7. Positive Factors & Risk Factors
        positive_factors = []
        risk_factors = []

        if context["credit_score"] >= 750:
            positive_factors.append(f"Excellent credit score of {context['credit_score']} (Prime tier).")
        elif context["credit_score"] >= 650:
            positive_factors.append(f"Acceptable credit score of {context['credit_score']} (Near-prime tier).")
        else:
            risk_factors.append(f"Subprime credit score of {context['credit_score']}.")

        if context["dti"] <= 0.40:
            positive_factors.append(f"Conservative Debt-to-Income ratio of {context['dti']*100:.1f}%.")
        elif context["dti"] <= 0.50:
            risk_factors.append(f"Elevated Debt-to-Income ratio of {context['dti']*100:.1f}%.")
        else:
            risk_factors.append(f"Excessive Debt-to-Income ratio of {context['dti']*100:.1f}%.")

        if context["employment_years"] >= 2.0:
            positive_factors.append(f"Stable employment tenure of {context['employment_years']:.1f} years.")
        else:
            risk_factors.append(f"Short employment duration of {context['employment_years']:.1f} years (< 2 years required for prime).")

        if context["repayment_history"] in ["Good", "Excellent"]:
            positive_factors.append("Consistent, on-time historical debt repayment record.")
        else:
            risk_factors.append(f"Repayment history rating is {context['repayment_history']}.")

        if calc_result["exceeds_affordability"]:
            risk_factors.append(
                f"Requested loan (₹{context['requested_amount']:,.0f}) exceeds maximum supportable debt capacity (₹{calc_result['supportable_principal']:,.0f})."
            )

        # 8. Counterfactual Hints
        counterfactual_hints = generate_counterfactual_hints(
            monthly_income=context["monthly_income"],
            existing_monthly_debt=context["existing_debt"],
            credit_score=context["credit_score"],
            employment_years=context["employment_years"],
            recent_default=context["recent_default"],
            requested_amount=context["requested_amount"],
            supportable_amount=calc_result["supportable_principal"],
            thresholds=self.thresholds_config,
        )

        # 9. Plain English Rationale Summary
        if decision == "ELIGIBLE":
            summary = (
                f"Application APPROVED for recommended principal of ₹{recommended_amount:,.0f} at {rate_band_label}. "
                f"The applicant demonstrates prime creditworthiness (Score: {context['credit_score']}), "
                f"healthy debt coverage (DTI: {context['dti']*100:.1f}%), and reliable repayment history."
            )
        elif decision == "CONDITIONALLY_ELIGIBLE":
            summary = (
                f"Application CONDITIONALLY APPROVED for a reduced principal of ₹{recommended_amount:,.0f} "
                f"at {rate_band_label} over {suggested_tenure} months. Subject to {len(conditions_list)} underwriting conditions."
            )
        else:
            summary = (
                f"Application DECLINED. Key disqualifying factor(s): {'; '.join(rejection_reasons) if rejection_reasons else 'Multiple underwriting thresholds breached'}."
            )

        return {
            "decision": decision,
            "risk_class": risk_class,
            "interest_rate": annual_rate,
            "interest_rate_percent": round(annual_rate * 100, 2),
            "interest_rate_band": rate_band_label,
            "suggested_tenure_months": suggested_tenure,
            "requested_amount": context["requested_amount"],
            "recommended_amount": recommended_amount,
            "max_affordable_emi": calc_result["max_emi"],
            "requested_emi": calc_result["requested_emi"],
            "recommended_emi": recommended_emi,
            "supportable_principal": calc_result["supportable_principal"],
            "exceeds_affordability": calc_result["exceeds_affordability"],
            "haircut_applied": calc_result["haircut_applied"],
            "conditions": conditions_list,
            "rejection_reasons": rejection_reasons,
            "positive_factors": positive_factors,
            "risk_factors": risk_factors,
            "counterfactual_hints": counterfactual_hints,
            "rationale_summary": summary,
            "execution_trace": execution_trace,
            "proof_trees": proof_builder.get_all_trees(),
            "threshold_version": self.thresholds_config.get("version", "1.0.0"),
            "derived_metrics": {
                "dti": context["dti"],
                "max_emi": calc_result["max_emi"],
                "requested_emi": calc_result["requested_emi"],
                "income_cap": calc_result["income_cap_amount"],
            }
        }
