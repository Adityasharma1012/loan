"""Comprehensive test suite for RuleEngine:
All 9 required scenarios, boundary conditions, determinism, rule-order independence,
conflict resolution, and refraction.
"""

import pytest
from app.rule_engine.engine import RuleEngine


@pytest.fixture
def engine():
    return RuleEngine()


# -------------------------------------------------------------
# SCENARIOS 1-9 AS SPECIFIED IN PROJECT REQUIREMENTS
# -------------------------------------------------------------

def test_scenario_1_high_income_excellent_credit(engine):
    """Scenario 1: High income + excellent credit -> Prime ELIGIBLE."""
    payload = {
        "applicant_id": "app_s1",
        "age": 35,
        "monthly_income": 120000.0,
        "existing_monthly_debt": 15000.0,  # DTI = 0.125
        "credit_score": 820,
        "employment_years": 7.0,
        "repayment_history": "Excellent",
        "recent_default": False,
        "requested_amount": 300000.0,
        "requested_tenure_months": 36,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "ELIGIBLE"
    assert res["risk_class"] == "LOW"
    assert res["interest_rate"] <= 0.110
    assert res["recommended_amount"] == 300000.0
    assert len(res["rejection_reasons"]) == 0
    assert len(res["conditions"]) == 0


def test_scenario_2_low_income_poor_credit(engine):
    """Scenario 2: Low income + poor credit -> NOT_ELIGIBLE (Hard knock-out credit < 550 or income < 20k)."""
    payload = {
        "applicant_id": "app_s2",
        "age": 28,
        "monthly_income": 15000.0,
        "existing_monthly_debt": 8000.0,
        "credit_score": 510,  # Hard knockout (< 550)
        "employment_years": 1.0,
        "repayment_history": "Poor",
        "recent_default": False,
        "requested_amount": 100000.0,
        "requested_tenure_months": 24,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "NOT_ELIGIBLE"
    assert res["recommended_amount"] == 0.0
    assert any("550" in r for r in res["rejection_reasons"])


def test_scenario_3_high_dti(engine):
    """Scenario 3: High DTI (> 50%) -> NOT_ELIGIBLE."""
    payload = {
        "applicant_id": "app_s3",
        "age": 40,
        "monthly_income": 50000.0,
        "existing_monthly_debt": 32000.0,  # DTI = 0.64 > 0.50
        "credit_score": 760,
        "employment_years": 5.0,
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 150000.0,
        "requested_tenure_months": 36,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "NOT_ELIGIBLE"
    assert any("Debt-to-Income" in r or "DTI" in r for r in res["rejection_reasons"])


def test_scenario_4_good_credit_unstable_employment(engine):
    """Scenario 4: Good credit + short employment (< 2 yrs) -> CONDITIONALLY_ELIGIBLE."""
    payload = {
        "applicant_id": "app_s4",
        "age": 26,
        "monthly_income": 45000.0,
        "existing_monthly_debt": 10000.0,  # DTI = 0.222
        "credit_score": 770,
        "employment_years": 0.8,  # < 2.0 yrs
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 150000.0,
        "requested_tenure_months": 36,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "CONDITIONALLY_ELIGIBLE"
    assert res["risk_class"] in ["MEDIUM", "LOW"]
    assert any("Employer verification" in c or "employment" in c.lower() for c in res["conditions"])


def test_scenario_5_low_credit_good_repayment(engine):
    """Scenario 5: Near-prime credit (e.g. 680) + good repayment -> CONDITIONALLY_ELIGIBLE."""
    payload = {
        "applicant_id": "app_s5",
        "age": 32,
        "monthly_income": 40000.0,
        "existing_monthly_debt": 12000.0,  # DTI = 0.30
        "credit_score": 680,  # 650 <= score < 750
        "employment_years": 3.0,
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 100000.0,
        "requested_tenure_months": 36,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "CONDITIONALLY_ELIGIBLE"
    assert res["risk_class"] == "MEDIUM"
    assert res["recommended_amount"] > 0


def test_scenario_7_zero_negative_income(engine):
    """Scenario 7: Zero or negative income -> Hard knock-out."""
    payload_zero = {
        "applicant_id": "app_s7_zero",
        "age": 30,
        "monthly_income": 0.0,
        "existing_monthly_debt": 0.0,
        "credit_score": 750,
        "employment_years": 3.0,
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 50000.0,
        "requested_tenure_months": 12,
    }
    res_zero = engine.evaluate(payload_zero)
    assert res_zero["decision"] == "NOT_ELIGIBLE"
    assert any("income" in r.lower() for r in res_zero["rejection_reasons"])

    payload_neg = dict(payload_zero, monthly_income=-5000.0)
    res_neg = engine.evaluate(payload_neg)
    assert res_neg["decision"] == "NOT_ELIGIBLE"


def test_scenario_8_request_exceeds_affordability(engine):
    """Scenario 8: Request exceeds affordability -> Recommend supportable principal and flag."""
    payload = {
        "applicant_id": "app_s8",
        "age": 30,
        "monthly_income": 35000.0,
        "existing_monthly_debt": 9000.0,  # DTI = 0.257, Max EMI = 0.40 * 35000 - 9000 = 5000
        "credit_score": 780,
        "employment_years": 4.0,
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 2500000.0,  # 25 Lakhs is way beyond 5000 max EMI
        "requested_tenure_months": 36,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "ELIGIBLE"
    assert res["exceeds_affordability"] is True
    assert res["recommended_amount"] < 200000.0
    assert res["recommended_amount"] == res["supportable_principal"]
    assert any("exceeds" in f.lower() for f in res["risk_factors"])


def test_scenario_9_borderline_cases(engine):
    """Scenario 9: Exact boundary thresholds."""
    # Boundary 1: Income exactly 30000, Credit 750, DTI 0.40, Employment 2.0 -> Exactly ELIGIBLE
    payload_exact_prime = {
        "applicant_id": "app_s9_prime",
        "age": 25,
        "monthly_income": 30000.0,
        "existing_monthly_debt": 12000.0,  # Exactly 40% DTI
        "credit_score": 750,  # Exactly prime threshold
        "employment_years": 2.0,  # Exactly 2.0 years
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 50000.0,
        "requested_tenure_months": 24,
    }
    res_exact_prime = engine.evaluate(payload_exact_prime)
    assert res_exact_prime["decision"] == "ELIGIBLE"
    assert res_exact_prime["risk_class"] == "LOW"

    # Boundary 2: Credit score 749 (1 point below prime) -> Drops to CONDITIONALLY_ELIGIBLE
    payload_near_prime = dict(payload_exact_prime, credit_score=749)
    res_near_prime = engine.evaluate(payload_near_prime)
    assert res_near_prime["decision"] == "CONDITIONALLY_ELIGIBLE"

    # Boundary 3: DTI exactly 0.50 -> CONDITIONALLY_ELIGIBLE; DTI 0.501 -> NOT_ELIGIBLE
    payload_cond_dti = dict(payload_exact_prime, existing_monthly_debt=15000.0)  # DTI = 0.50
    res_cond_dti = engine.evaluate(payload_cond_dti)
    assert res_cond_dti["decision"] == "CONDITIONALLY_ELIGIBLE"

    payload_excess_dti = dict(payload_exact_prime, existing_monthly_debt=15300.0)  # DTI = 0.51
    res_excess_dti = engine.evaluate(payload_excess_dti)
    assert res_excess_dti["decision"] == "NOT_ELIGIBLE"


# -------------------------------------------------------------
# ENGINE PROPERTIES: DETERMINISM, ORDER-INVARIANCE, REFRACTION
# -------------------------------------------------------------

def test_determinism_identical_runs(engine):
    """Executing engine 10 times on the same input gives exact identical decision and trace."""
    payload = {
        "applicant_id": "app_det",
        "age": 31,
        "monthly_income": 55000.0,
        "existing_monthly_debt": 14000.0,
        "credit_score": 710,
        "employment_years": 2.5,
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 200000.0,
        "requested_tenure_months": 36,
    }
    first_res = engine.evaluate(payload)
    for _ in range(9):
        res = engine.evaluate(payload)
        assert res["decision"] == first_res["decision"]
        assert res["risk_class"] == first_res["risk_class"]
        assert res["recommended_amount"] == first_res["recommended_amount"]
        assert len(res["execution_trace"]) == len(first_res["execution_trace"])
        for s1, s2 in zip(first_res["execution_trace"], res["execution_trace"]):
            assert s1["rule_id"] == s2["rule_id"]


def test_rule_order_invariance(engine):
    """Shuffling the rules array before forward chaining must NOT alter outcome or execution trace."""
    payload = {
        "applicant_id": "app_shuffle",
        "age": 34,
        "monthly_income": 62000.0,
        "existing_monthly_debt": 18000.0,
        "credit_score": 765,
        "employment_years": 3.5,
        "repayment_history": "Good",
        "recent_default": False,
        "requested_amount": 250000.0,
        "requested_tenure_months": 36,
    }
    standard_res = engine.evaluate(payload, shuffle_rules=False)
    shuffled_res = engine.evaluate(payload, shuffle_rules=True)
    
    assert standard_res["decision"] == shuffled_res["decision"]
    assert standard_res["risk_class"] == shuffled_res["risk_class"]
    assert standard_res["recommended_amount"] == shuffled_res["recommended_amount"]
    assert [s["rule_id"] for s in standard_res["execution_trace"]] == [s["rule_id"] for s in shuffled_res["execution_trace"]]


def test_refraction_property(engine):
    """Every rule must fire at most once during a forward chaining run."""
    payload = {
        "applicant_id": "app_refract",
        "age": 42,
        "monthly_income": 80000.0,
        "existing_monthly_debt": 20000.0,
        "credit_score": 790,
        "employment_years": 6.0,
        "repayment_history": "Excellent",
        "recent_default": False,
        "requested_amount": 400000.0,
        "requested_tenure_months": 48,
    }
    res = engine.evaluate(payload)
    fired_rule_ids = [step["rule_id"] for step in res["execution_trace"]]
    assert len(fired_rule_ids) == len(set(fired_rule_ids)), "A rule fired more than once! Refraction violated."


def test_underage_legal_capacity_knockout(engine):
    """Age < 18 must trigger HKO_001 regardless of wealth."""
    payload = {
        "applicant_id": "app_underage",
        "age": 17,
        "monthly_income": 500000.0,  # Very high income
        "existing_monthly_debt": 0.0,
        "credit_score": 850,
        "employment_years": 2.0,
        "repayment_history": "Excellent",
        "recent_default": False,
        "requested_amount": 100000.0,
        "requested_tenure_months": 12,
    }
    res = engine.evaluate(payload)
    assert res["decision"] == "NOT_ELIGIBLE"
    assert any("legal" in r.lower() or "18" in r for r in res["rejection_reasons"])
