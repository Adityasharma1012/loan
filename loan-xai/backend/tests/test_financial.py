"""Tests for financial mathematics, annuity formulas, and counterfactuals."""

import pytest
import math
from app.logic.financial import (
    calculate_dti,
    calculate_max_emi,
    calculate_monthly_emi,
    calculate_annuity_principal,
    calculate_recommended_loan,
    generate_counterfactual_hints,
)


def test_dti_calculation():
    # Regular valid income
    assert calculate_dti(12000, 40000) == 0.30
    assert calculate_dti(20000, 40000) == 0.50
    # Zero debt
    assert calculate_dti(0, 50000) == 0.0
    # Zero or negative income (returns 0.0, handled by knockout)
    assert calculate_dti(5000, 0) == 0.0
    assert calculate_dti(5000, -1000) == 0.0


def test_max_emi_calculation():
    # 40% of 50,000 = 20,000. Existing debt = 5,000 -> Max EMI = 15,000
    assert calculate_max_emi(50000, 5000, multiplier=0.40) == 15000.0
    # Existing debt exceeds 40% -> floored at 0
    assert calculate_max_emi(50000, 25000, multiplier=0.40) == 0.0
    # Zero income
    assert calculate_max_emi(0, 1000) == 0.0


def test_monthly_emi_annuity_math():
    # Hand-computed reference:
    # Principal = 100,000, Rate = 12% (1% monthly), Tenure = 12 months
    # EMI = 100,000 * 0.01 * (1.01)^12 / ((1.01)^12 - 1)
    # (1.01)^12 = 1.12682503
    # EMI = 1000 * 1.12682503 / 0.12682503 = 8884.88
    computed_emi = calculate_monthly_emi(100000.0, 0.12, 12)
    assert abs(computed_emi - 8884.88) < 0.10

    # Zero interest rate case
    assert calculate_monthly_emi(120000.0, 0.0, 12) == 10000.0


def test_annuity_principal_supportable():
    # Given EMI = 8884.88 at 12% over 12 months, should recover approx 100,000 principal
    pv = calculate_annuity_principal(8884.88, 0.12, 12)
    assert abs(pv - 100000.0) < 1.0


def test_calculate_recommended_loan_within_affordability():
    res = calculate_recommended_loan(
        requested_amount=200000.0,
        monthly_income=60000.0,
        existing_monthly_debt=5000.0,
        annual_interest_rate=0.095,
        tenure_months=36,
        is_conditional=False,
    )
    # Max EMI = 0.40 * 60,000 - 5,000 = 19,000
    # Supportable principal for 19,000 EMI over 36m at 9.5% is > 550,000
    # Requested 200,000 should be fully recommended
    assert res["recommended_amount"] == 200000.0
    assert not res["exceeds_affordability"]
    assert not res["haircut_applied"]


def test_calculate_recommended_loan_exceeds_affordability():
    # Requested 1,000,000 with low income 25,000, existing debt 5,000
    # Max EMI = 0.40 * 25,000 - 5,000 = 5,000
    res = calculate_recommended_loan(
        requested_amount=1000000.0,
        monthly_income=25000.0,
        existing_monthly_debt=5000.0,
        annual_interest_rate=0.14,
        tenure_months=36,
        is_conditional=False,
    )
    assert res["exceeds_affordability"]
    assert res["recommended_amount"] < 200000.0
    assert res["recommended_amount"] == res["supportable_principal"]


def test_counterfactual_hints_generation():
    thresholds = {
        "eligibility": {
            "min_income_eligible": 30000.0,
            "max_dti_eligible": 0.40,
            "min_credit_score_eligible": 750,
            "min_employment_years_eligible": 2.0,
        }
    }
    hints = generate_counterfactual_hints(
        monthly_income=25000.0,
        existing_monthly_debt=12500.0,  # DTI = 0.50
        credit_score=710,
        employment_years=1.0,
        recent_default=True,
        requested_amount=500000.0,
        supportable_amount=200000.0,
        thresholds=thresholds,
    )
    features_hinted = {h["feature"] for h in hints}
    assert "recent_default" in features_hinted
    assert "credit_score" in features_hinted
    assert "monthly_income" in features_hinted
    assert "existing_monthly_debt" in features_hinted
    assert "employment_years" in features_hinted
    assert "requested_amount" in features_hinted
