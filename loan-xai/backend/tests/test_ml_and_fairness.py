"""Unit tests for ML models, synthetic generator, fairness audits, and hand-computed metrics."""

import pytest
import numpy as np
import pandas as pd
from app.ml.data import generate_synthetic_dataset
from app.ml.models import MLManager, prepare_feature_matrix
from app.fairness.audit import compute_group_metrics, FairnessAuditor, analyze_proxy_correlations


def test_synthetic_data_generator_properties():
    df = generate_synthetic_dataset(n_samples=500, seed=42)
    assert len(df) == 500
    expected_cols = [
        "applicant_id", "age", "monthly_income", "existing_monthly_debt",
        "credit_score", "employment_years", "repayment_history", "recent_default",
        "requested_amount", "requested_tenure_months", "dti",
        "gender", "region_type", "age_band", "repaid", "repaid_probability"
    ]
    for c in expected_cols:
        assert c in df.columns, f"Missing expected column {c}"

    # Verify reproducibility with seed
    df2 = generate_synthetic_dataset(n_samples=500, seed=42)
    pd.testing.assert_frame_equal(df, df2)

    # Verify independent target repaid distribution is within reasonable credit bounds (e.g. 50-85%)
    pos_rate = df["repaid"].mean()
    assert 0.50 <= pos_rate <= 0.85


def test_hand_computed_fairness_metrics():
    """Verify hand-computed mathematical values of DIR, SPD, and EOD against synthetic table."""
    # Constructed toy dataset:
    # Male (Privileged): 10 applicants, 8 approved (Approval rate = 0.80)
    # 6 truly repaid, all 6 approved (TPR = 6/6 = 1.0)
    # Female (Unprivileged): 10 applicants, 4 approved (Approval rate = 0.40)
    # 5 truly repaid, 3 approved (TPR = 3/5 = 0.60)
    data = {
        "gender": ["Male"] * 10 + ["Female"] * 10,
        "prediction": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0] + [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        "repaid":     [1, 1, 1, 1, 1, 1, 0, 0, 0, 0] + [1, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    }
    toy_df = pd.DataFrame(data)

    res = compute_group_metrics(toy_df, group_col="gender", pred_col="prediction", truth_col="repaid", min_sample_threshold=5)
    
    subgroups = {g["group_name"]: g for g in res["subgroups"]}
    male = subgroups["Male"]
    female = subgroups["Female"]

    # Verify Male (Privileged)
    assert male["is_privileged"] is True
    assert male["approval_rate"] == 0.80
    assert male["disparate_impact_ratio"] == 1.0
    assert male["statistical_parity_difference"] == 0.0

    # Verify Female (Unprivileged)
    # DIR = 0.40 / 0.80 = 0.50
    assert female["disparate_impact_ratio"] == 0.50
    # SPD = 0.40 - 0.80 = -0.40
    assert female["statistical_parity_difference"] == -0.40
    # EOD = TPR_female (3/5 = 0.60) - TPR_male (6/6 = 1.0) = -0.40
    assert abs(female["equal_opportunity_difference"] - (-0.40)) < 1e-4
    # Four-Fifths violation flag (0.50 < 0.80)
    assert female["four_fifths_violation"] is True


def test_small_sample_size_flagging():
    """Verify that subgroups with n < 30 are flagged with small_sample_warning."""
    data = {
        "region_type": ["Urban"] * 50 + ["Rural"] * 20,
        "prediction": [1] * 50 + [0] * 20,
        "repaid": [1] * 50 + [0] * 20,
    }
    df = pd.DataFrame(data)
    res = compute_group_metrics(df, group_col="region_type", pred_col="prediction", truth_col="repaid", min_sample_threshold=30)
    subgroups = {g["group_name"]: g for g in res["subgroups"]}
    
    assert subgroups["Urban"]["small_sample_warning"] is False
    assert subgroups["Rural"]["small_sample_warning"] is True
    assert subgroups["Rural"]["four_fifths_violation"] is False  # Suppressed when sample is small


def test_ml_model_training_and_comparison():
    df = generate_synthetic_dataset(n_samples=600, seed=42)
    manager = MLManager()
    results = manager.train_and_evaluate(df, test_size=0.25, seed=42)

    assert "models" in results
    assert "decision_tree" in results["models"]
    assert "logistic_regression" in results["models"]
    assert "rule_engine_standard" in results["models"]
    assert "rule_engine_strict" in results["models"]

    dt_metrics = results["models"]["decision_tree"]["metrics"]
    assert 0.60 <= dt_metrics["accuracy"] <= 1.0
    assert len(results["models"]["decision_tree"]["feature_importances"]) > 0

    lr_metrics = results["models"]["logistic_regression"]["metrics"]
    assert 0.60 <= lr_metrics["accuracy"] <= 1.0
    assert len(results["models"]["logistic_regression"]["coefficients"]) > 0

    assert "agreement" in results
    assert 0.0 <= results["agreement"]["agreement_rate_dt_rule"] <= 1.0
    assert len(results["edge_case_divergences"]) == 9


def test_fairness_auditor_pipeline():
    df = generate_synthetic_dataset(n_samples=600, seed=42)
    manager = MLManager()
    manager.train_and_evaluate(df, test_size=0.25, seed=42)

    auditor = FairnessAuditor()
    audit_rep = auditor.run_full_audit(manager.test_df)

    assert "systems_audit" in audit_rep
    assert "Rule Engine (Standard)" in audit_rep["systems_audit"]
    assert "Decision Tree" in audit_rep["systems_audit"]
    assert "proxy_findings" in audit_rep
    assert len(audit_rep["recommendations"]) > 0
    assert len(audit_rep["methodology_limitations"]) > 0
