"""Synthetic loan applicant dataset generator with independent ground-truth repayment
and quarantined protected demographic attributes for fairness auditing.
"""

from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd


def generate_synthetic_dataset(n_samples: int = 6000, seed: int = 42) -> pd.DataFrame:
    """Generates a reproducible synthetic dataset of loan applicants.
    
    IMPORTANT DESIGN CHOICE - INDEPENDENT GROUND TRUTH:
    The ground-truth label 'repaid' is generated via an independent probabilistic
    logistic process representing true retail credit economic performance.
    It is NOT generated from the rule engine output.
    
    Rationale:
    If 'repaid' were generated from the rule engine, the machine learning models
    would simply be learning to imitate/distill the rule engine rather than modeling
    actual credit default risk. By generating 'repaid' from an independent structural
    equation incorporating financial capacity, behavioral history, and stochastic shocks,
    both the rule engine and the ML models can be objectively benchmarked against
    the same underlying economic reality.
    """
    rng = np.random.default_rng(seed)

    # 1. Demographic Protected Attributes (Quarantined for Fairness Audit Only)
    # Gender distribution: 48% Male, 46% Female, 6% Non-binary
    genders = rng.choice(["Male", "Female", "Non-binary"], size=n_samples, p=[0.48, 0.46, 0.06])
    
    # Region distribution: 55% Urban, 30% Semi-Urban, 15% Rural
    regions = rng.choice(["Urban", "Semi-Urban", "Rural"], size=n_samples, p=[0.55, 0.30, 0.15])
    
    # Age distribution: 18 to 72 years
    ages = rng.integers(18, 72, size=n_samples)
    
    age_bands = []
    for a in ages:
        if a <= 25:
            age_bands.append("18-25")
        elif a <= 40:
            age_bands.append("26-40")
        elif a <= 60:
            age_bands.append("41-60")
        else:
            age_bands.append("60+")

    # 2. Structural Demographic Disparities (Intentional historical bias modeling)
    # To enable meaningful fairness auditing, we simulate known historical disparities:
    # - Rural applicants historically experience lower formal credit penetration (slightly lower baseline score)
    # - Legacy gender pay gap in older cohorts (slight median income difference)
    base_incomes = rng.lognormal(mean=10.6, sigma=0.55, size=n_samples)  # Median ~ 40,000 INR
    
    # Adjust for region (rural median wage lower, cost of living lower)
    region_multiplier = np.where(regions == "Rural", 0.78, np.where(regions == "Semi-Urban", 0.90, 1.05))
    
    # Adjust for historical gender pay differential (e.g. 10% in older cohorts)
    gender_multiplier = np.where((genders == "Female") & (ages > 35), 0.90, 1.0)
    
    monthly_incomes = np.round(base_incomes * region_multiplier * gender_multiplier, -2)
    monthly_incomes = np.maximum(8000.0, monthly_incomes)  # Floor at minimum living wage

    # Existing debt service: typically 10% to 45% of income with noise
    debt_ratios = rng.beta(a=2.0, b=5.0, size=n_samples) * 0.70
    existing_debts = np.round(monthly_incomes * debt_ratios, -2)

    # Employment duration: correlated with age
    max_possible_work_years = np.maximum(0.5, ages - 20)
    employment_years = np.round(rng.uniform(0.2, 0.7, size=n_samples) * max_possible_work_years, 1)

    # Credit score: Normal distribution centered around 700, range 350 - 850
    # Rural thin-file effect: slight downward shift of 20 points
    rural_cs_penalty = np.where(regions == "Rural", 25, 0)
    raw_scores = rng.normal(loc=710 - rural_cs_penalty, scale=75, size=n_samples)
    credit_scores = np.clip(np.round(raw_scores), 300, 900).astype(int)

    # Repayment history categorical: correlated with credit score
    repayment_histories = []
    recent_defaults = []
    for cs in credit_scores:
        if cs >= 750:
            rep = rng.choice(["Excellent", "Good", "Fair"], p=[0.70, 0.26, 0.04])
            default = rng.choice([False, True], p=[0.98, 0.02])
        elif cs >= 650:
            rep = rng.choice(["Good", "Fair", "Poor"], p=[0.55, 0.38, 0.07])
            default = rng.choice([False, True], p=[0.93, 0.07])
        elif cs >= 550:
            rep = rng.choice(["Fair", "Poor"], p=[0.50, 0.50])
            default = rng.choice([False, True], p=[0.80, 0.20])
        else:
            rep = rng.choice(["Fair", "Poor"], p=[0.15, 0.85])
            default = rng.choice([False, True], p=[0.45, 0.55])
        
        repayment_histories.append(rep)
        recent_defaults.append(default)

    # Requested loan amount: roughly 3x to 15x monthly income
    multipliers = rng.uniform(3.0, 12.0, size=n_samples)
    requested_amounts = np.round(monthly_incomes * multipliers, -3)
    requested_amounts = np.clip(requested_amounts, 25000.0, 2000000.0)

    # Requested tenure: 12, 24, 36, 48, 60 months
    tenures = rng.choice([12, 24, 36, 48, 60], size=n_samples, p=[0.15, 0.25, 0.35, 0.15, 0.10])

    # Calculated DTI
    dtis = np.round(existing_debts / monthly_incomes, 4)

    # 3. Independent Ground-Truth Repayment Generation (Logistic Data Generating Process)
    # Log-odds of successful full repayment without default:
    rep_score_bonus = {"Excellent": 1.2, "Good": 0.5, "Fair": -0.6, "Poor": -1.8}
    rep_bonus = np.array([rep_score_bonus[r] for r in repayment_histories])
    default_penalty = np.where(recent_defaults, -2.4, 0.0)

    # Standardized features for stable logistic equation
    norm_income = (monthly_incomes - 40000.0) / 25000.0
    norm_score = (credit_scores - 700.0) / 80.0
    norm_dti = (dtis - 0.35) / 0.15
    norm_emp = (employment_years - 4.0) / 3.0

    stochastic_noise = rng.normal(0.0, 0.75, size=n_samples)

    log_odds = (
        0.85  # Base positive intercept (most retail loans are repaid)
        + 0.50 * norm_income
        + 1.10 * norm_score
        - 1.05 * norm_dti
        + 0.35 * norm_emp
        + rep_bonus
        + default_penalty
        + stochastic_noise
    )

    prob_repaid = 1.0 / (1.0 + np.exp(-log_odds))
    repaid = (rng.uniform(0.0, 1.0, size=n_samples) < prob_repaid).astype(int)

    df = pd.DataFrame({
        "applicant_id": [f"SYNTH_{i:05d}" for i in range(1, n_samples + 1)],
        # Non-protected application features (used in underwriting)
        "age": ages,
        "monthly_income": monthly_incomes,
        "existing_monthly_debt": existing_debts,
        "credit_score": credit_scores,
        "employment_years": employment_years,
        "repayment_history": repayment_histories,
        "recent_default": recent_defaults,
        "requested_amount": requested_amounts,
        "requested_tenure_months": tenures,
        "dti": dtis,
        # Quarantined protected attributes (used ONLY in fairness auditing)
        "gender": genders,
        "region_type": regions,
        "age_band": age_bands,
        # Independent ground truth
        "repaid": repaid,
        "repaid_probability": np.round(prob_repaid, 4),
    })

    return df
