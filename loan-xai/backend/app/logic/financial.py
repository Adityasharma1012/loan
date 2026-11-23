"""Financial mathematics and affordability logic for loan underwriting."""

from typing import Dict, Any, List, Optional
import math


def calculate_dti(existing_monthly_debt: float, monthly_income: float) -> float:
    """Calculate Debt-To-Income (DTI) ratio.
    Returns 0.0 if income <= 0 to avoid division by zero (income <= 0 is caught by knockout).
    """
    if monthly_income <= 0:
        return 0.0
    return round(existing_monthly_debt / monthly_income, 4)


def calculate_max_emi(
    monthly_income: float,
    existing_monthly_debt: float,
    multiplier: float = 0.40,
) -> float:
    """Calculate maximum affordable Equated Monthly Installment (EMI).
    Standard capacity: 40% of gross income minus existing commitments, floored at 0.
    """
    if monthly_income <= 0:
        return 0.0
    disposable_debt_capacity = (multiplier * monthly_income) - existing_monthly_debt
    return max(0.0, round(disposable_debt_capacity, 2))


def calculate_monthly_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> float:
    """Calculate standard monthly EMI using the annuity formula:
    EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    
    monthly_rate = annual_interest_rate / 12.0
    if monthly_rate == 0:
        return round(principal / tenure_months, 2)
    
    numerator = principal * monthly_rate * math.pow(1.0 + monthly_rate, tenure_months)
    denominator = math.pow(1.0 + monthly_rate, tenure_months) - 1.0
    if denominator == 0:
        return 0.0
    
    return round(numerator / denominator, 2)


def calculate_annuity_principal(
    max_emi: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> float:
    """Calculate maximum principal supportable by a given EMI over tenure:
    PV = EMI * [1 - (1 + r)^(-n)] / r
    """
    if max_emi <= 0 or tenure_months <= 0:
        return 0.0
    
    monthly_rate = annual_interest_rate / 12.0
    if monthly_rate == 0:
        return round(max_emi * tenure_months, 2)
    
    pv = max_emi * (1.0 - math.pow(1.0 + monthly_rate, -tenure_months)) / monthly_rate
    return max(0.0, round(pv, 2))


def calculate_recommended_loan(
    requested_amount: float,
    monthly_income: float,
    existing_monthly_debt: float,
    annual_interest_rate: float,
    tenure_months: int,
    is_conditional: bool = False,
    income_multiplier_cap: float = 36.0,
    conditional_haircut: float = 0.70,
) -> Dict[str, Any]:
    """Computes recommended loan sizing, affordability bounds, and flags."""
    max_emi = calculate_max_emi(monthly_income, existing_monthly_debt, multiplier=0.40)
    requested_emi = calculate_monthly_emi(requested_amount, annual_interest_rate, tenure_months)
    
    principal_by_max_emi = calculate_annuity_principal(max_emi, annual_interest_rate, tenure_months)
    income_cap_amount = round(monthly_income * income_multiplier_cap, 2) if monthly_income > 0 else 0.0
    
    effective_requested = requested_amount
    haircut_applied = False
    if is_conditional:
        effective_requested = round(requested_amount * conditional_haircut, 2)
        haircut_applied = True

    # Supportable amount is bounded by max EMI and income cap
    supportable_amount = min(principal_by_max_emi, income_cap_amount)
    recommended_amount = min(effective_requested, supportable_amount)
    recommended_amount = max(0.0, round(recommended_amount, 2))

    recommended_emi = calculate_monthly_emi(recommended_amount, annual_interest_rate, tenure_months)
    
    exceeds_affordability = requested_amount > (supportable_amount + 1.0)
    
    return {
        "requested_amount": requested_amount,
        "recommended_amount": recommended_amount,
        "max_emi": max_emi,
        "requested_emi": requested_emi,
        "recommended_emi": recommended_emi,
        "supportable_principal": supportable_amount,
        "income_cap_amount": income_cap_amount,
        "exceeds_affordability": exceeds_affordability,
        "haircut_applied": haircut_applied,
        "haircut_factor": conditional_haircut if haircut_applied else 1.0,
    }


def generate_counterfactual_hints(
    monthly_income: float,
    existing_monthly_debt: float,
    credit_score: int,
    employment_years: float,
    recent_default: bool,
    requested_amount: float,
    supportable_amount: float,
    thresholds: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Generates actionable counterfactual explanations showing minimum necessary
    changes to transition towards eligibility.
    """
    hints = []
    elig = thresholds.get("eligibility", {})
    min_income = elig.get("min_income_eligible", 30000.0)
    max_dti = elig.get("max_dti_eligible", 0.40)
    min_score = elig.get("min_credit_score_eligible", 750)
    min_emp = elig.get("min_employment_years_eligible", 2.0)

    # 1. Recent Default
    if recent_default:
        hints.append({
            "feature": "recent_default",
            "current_value": "Recent default on record",
            "target_value": "No default within past 24 months",
            "delta_description": "Maintain unblemished repayment for 24 months to clear statutory default knock-out.",
            "impact": "Eliminates hard knock-out disqualification.",
        })

    # 2. Credit Score
    if credit_score < min_score:
        diff = min_score - credit_score
        hints.append({
            "feature": "credit_score",
            "current_value": credit_score,
            "target_value": min_score,
            "delta_description": f"Improve credit score by {diff} points (from {credit_score} to {min_score}).",
            "impact": "Qualifies for Prime tier and lowest interest band.",
        })

    # 3. Monthly Income
    if monthly_income < min_income:
        diff_inc = round(min_income - monthly_income, 2)
        hints.append({
            "feature": "monthly_income",
            "current_value": f"₹{monthly_income:,.2f}",
            "target_value": f"₹{min_income:,.2f}",
            "delta_description": f"Increase verified monthly income by ₹{diff_inc:,.2f}.",
            "impact": "Satisfies primary income sufficiency baseline.",
        })

    # 4. Debt-to-Income / Monthly Debt
    current_dti = calculate_dti(existing_monthly_debt, monthly_income)
    if current_dti > max_dti and monthly_income > 0:
        target_debt = round(monthly_income * max_dti, 2)
        debt_reduction = max(0.0, round(existing_monthly_debt - target_debt, 2))
        hints.append({
            "feature": "existing_monthly_debt",
            "current_value": f"₹{existing_monthly_debt:,.2f} (DTI: {current_dti*100:.1f}%)",
            "target_value": f"₹{target_debt:,.2f} (DTI: {max_dti*100:.1f}%)",
            "delta_description": f"Pay down existing monthly debt service by ₹{debt_reduction:,.2f} to reduce DTI to {max_dti*100:.0f}%.",
            "impact": "Re-establishes uncommitted cashflow headroom.",
        })

    # 5. Employment Duration
    if employment_years < min_emp:
        years_needed = round(min_emp - employment_years, 1)
        hints.append({
            "feature": "employment_years",
            "current_value": f"{employment_years:.1f} years",
            "target_value": f"{min_emp:.1f} years",
            "delta_description": f"Accumulate additional {years_needed} years of continuous employment tenure.",
            "impact": "Satisfies employment stability prerequisite.",
        })

    # 6. Affordability / Requested Amount
    if requested_amount > (supportable_amount + 1.0) and supportable_amount > 0:
        reduction = round(requested_amount - supportable_amount, 2)
        hints.append({
            "feature": "requested_amount",
            "current_value": f"₹{requested_amount:,.2f}",
            "target_value": f"₹{supportable_amount:,.2f}",
            "delta_description": f"Reduce loan request by ₹{reduction:,.2f} to match maximum supportable capacity.",
            "impact": "Brings monthly EMI within permissible debt service limit.",
        })

    return hints
