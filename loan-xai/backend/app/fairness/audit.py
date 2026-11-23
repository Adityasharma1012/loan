"""Fairness, algorithmic bias auditing, disparate impact analysis,
and proxy feature detection engine.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


PRIVILEGED_GROUPS = {
    "gender": "Male",
    "region_type": "Urban",
    "age_band": "26-40",
}


def compute_group_metrics(
    df: pd.DataFrame,
    group_col: str,
    pred_col: str,
    truth_col: str = "repaid",
    min_sample_threshold: int = 30,
) -> Dict[str, Any]:
    """Computes standard algorithmic fairness metrics for each subgroup within an attribute."""
    privileged_val = PRIVILEGED_GROUPS.get(group_col)
    unique_groups = df[group_col].unique().tolist()
    
    # Privileged baseline metrics
    priv_mask = df[group_col] == privileged_val
    priv_df = df[priv_mask]
    priv_n = len(priv_df)
    
    priv_approval_rate = float(priv_df[pred_col].mean()) if priv_n > 0 else 0.0
    priv_tp = ((priv_df[pred_col] == 1) & (priv_df[truth_col] == 1)).sum()
    priv_fn = ((priv_df[pred_col] == 0) & (priv_df[truth_col] == 1)).sum()
    priv_fp = ((priv_df[pred_col] == 1) & (priv_df[truth_col] == 0)).sum()
    priv_tn = ((priv_df[pred_col] == 0) & (priv_df[truth_col] == 0)).sum()

    priv_tpr = float(priv_tp / (priv_tp + priv_fn)) if (priv_tp + priv_fn) > 0 else 0.0
    priv_fpr = float(priv_fp / (priv_fp + priv_tn)) if (priv_fp + priv_tn) > 0 else 0.0
    priv_fnr = float(priv_fn / (priv_tp + priv_fn)) if (priv_tp + priv_fn) > 0 else 0.0

    groups_data = []

    for grp in unique_groups:
        grp_mask = df[group_col] == grp
        grp_df = df[grp_mask]
        n_samples = len(grp_df)

        small_sample = n_samples < min_sample_threshold

        approval_rate = float(grp_df[pred_col].mean()) if n_samples > 0 else 0.0
        
        tp = int(((grp_df[pred_col] == 1) & (grp_df[truth_col] == 1)).sum())
        fn = int(((grp_df[pred_col] == 0) & (grp_df[truth_col] == 1)).sum())
        fp = int(((grp_df[pred_col] == 1) & (grp_df[truth_col] == 0)).sum())
        tn = int(((grp_df[pred_col] == 0) & (grp_df[truth_col] == 0)).sum())

        tpr = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (tp + fn)) if (tp + fn) > 0 else 0.0

        # Disparate Impact Ratio: Approval Rate / Privileged Approval Rate
        if priv_approval_rate > 0:
            dir_ratio = approval_rate / priv_approval_rate
        else:
            dir_ratio = 1.0

        # Statistical Parity Difference: Approval Rate - Privileged Approval Rate
        spd = approval_rate - priv_approval_rate

        # Equal Opportunity Difference: TPR - Privileged TPR
        eod = tpr - priv_tpr

        four_fifths_flag = (dir_ratio < 0.80) and not small_sample

        groups_data.append({
            "group_name": str(grp),
            "is_privileged": (grp == privileged_val),
            "sample_size": n_samples,
            "sample_share_percent": round((n_samples / len(df)) * 100, 2),
            "small_sample_warning": small_sample,
            "approval_rate": round(approval_rate, 4),
            "approval_rate_percent": round(approval_rate * 100, 2),
            "disparate_impact_ratio": round(dir_ratio, 4),
            "statistical_parity_difference": round(spd, 4),
            "equal_opportunity_difference": round(eod, 4),
            "true_positive_rate": round(tpr, 4),
            "false_positive_rate": round(fpr, 4),
            "false_negative_rate": round(fnr, 4),
            "four_fifths_violation": four_fifths_flag,
        })

    # Sort groups with privileged first, then alphabetically
    groups_data.sort(key=lambda x: (not x["is_privileged"], x["group_name"]))

    return {
        "attribute": group_col,
        "privileged_reference": privileged_val,
        "subgroups": groups_data,
    }


def analyze_proxy_correlations(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Evaluates whether neutral financial features encode demographic proxies."""
    proxy_findings = []
    
    # 1. Region vs Credit Score & Income
    region_stats = df.groupby("region_type")[["credit_score", "monthly_income"]].mean().to_dict()
    rural_cs = region_stats["credit_score"].get("Rural", 0)
    urban_cs = region_stats["credit_score"].get("Urban", 0)
    cs_diff = round(urban_cs - rural_cs, 1)

    proxy_findings.append({
        "proxy_feature": "credit_score",
        "demographic_target": "region_type",
        "observation": f"Urban applicants average credit score {urban_cs:.0f} vs Rural {rural_cs:.0f} (gap: {cs_diff} pts).",
        "proxy_risk_level": "MODERATE",
        "risk_mechanism": (
            "Thin credit files in rural regions lower formal credit bureau scores, "
            "causing credit score minimum thresholds to function as a regional proxy."
        ),
    })

    # 2. Gender vs Income
    gender_income = df.groupby("gender")["monthly_income"].mean().to_dict()
    m_inc = gender_income.get("Male", 0)
    f_inc = gender_income.get("Female", 0)
    inc_diff_pct = round(((m_inc - f_inc) / m_inc) * 100, 1) if m_inc > 0 else 0

    proxy_findings.append({
        "proxy_feature": "monthly_income",
        "demographic_target": "gender",
        "observation": f"Male applicants average ₹{m_inc:,.0f} vs Female ₹{f_inc:,.0f} (historical wage gap: {inc_diff_pct}%).",
        "proxy_risk_level": "MODERATE",
        "risk_mechanism": (
            "Historical societal income differentials in older cohorts mean absolute income "
            "hurdles (₹30,000 threshold) exert mild disparate impact against female applicants."
        ),
    })

    return proxy_findings


def generate_fairness_narrative(
    audit_results: Dict[str, Any],
    proxy_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Generates automated findings narrative and actionable mitigation recommendations."""
    findings = []
    violations = []

    for system_name, att_dict in audit_results.items():
        for att_name, metrics in att_dict.items():
            for grp in metrics.get("subgroups", []):
                if grp.get("four_fifths_violation"):
                    violations.append({
                        "system": system_name,
                        "attribute": att_name,
                        "group": grp["group_name"],
                        "dir": grp["disparate_impact_ratio"],
                        "rate": grp["approval_rate_percent"],
                    })

    if violations:
        for v in violations:
            findings.append(
                f"Statutory Disparate Impact Flag in {v['system']} for {v['attribute']}='{v['group']}': "
                f"Disparate Impact Ratio is {v['dir']:.2f} (Approval rate {v['rate']:.1f}%), "
                f"which breaches the EEOC 0.80 Four-Fifths benchmark."
            )
    else:
        findings.append(
            "No severe Four-Fifths rule violations (< 0.80 DIR) detected across primary tested demographics."
        )

    recommendations = [
        {
            "priority": "HIGH",
            "title": "Calibrate Regional Credit Score Thresholds",
            "action": (
                "Introduce alternative credit assessment pathways (utility/telecom payment proofs) for rural applicants "
                "to address thin-file bureau penalties without degrading portfolio loss expectations."
            ),
        },
        {
            "priority": "MEDIUM",
            "title": "Review Absolute Income Floor vs Debt-to-Income",
            "action": (
                "Transition underwriting weight from rigid nominal income floors (₹30,000) towards proportional DTI "
                "to mitigate gender and regional wage-scale disparity spillover."
            ),
        },
        {
            "priority": "MEDIUM",
            "title": "Establish Human-in-the-Loop Conditional Tier Review",
            "action": (
                "Route borderline conditional applications from historically underserved cohorts to senior credit officers "
                "with structured discretionary mitigation checklists."
            ),
        },
        {
            "priority": "LOW",
            "title": "Continuous Disparity Auditing & Threshold Versioning",
            "action": (
                "Maintain audit logs with threshold version tracking (thresholds.yaml) to ensure adverse action notices "
                "remain fully contestable and compliant with FCRA/ECOA regulations."
            ),
        },
    ]

    limitations = [
        "Synthetic Data Caveat: Audit is conducted on synthetic demographic distributions and does not reflect actual institutional portfolio risks.",
        "Impossibility Theorem: Mathematical trade-offs dictate that Demographic Parity, Equalized Odds, and Predictive Parity cannot be simultaneously satisfied when base default rates differ.",
        "Small Group Reliability: Subgroups with n < 30 exhibit high sampling variance; metrics should be interpreted as diagnostic rather than conclusive.",
        "Intersectionality Bounds: Single-attribute audits can obscure compound multi-dimensional disadvantages (e.g. young rural applicants).",
        "Regulatory Notice: This fairness audit provides algorithmic parity diagnostics and does not constitute formal legal counsel or regulatory certification.",
    ]

    return {
        "findings": findings,
        "recommendations": recommendations,
        "limitations": limitations,
    }


class FairnessAuditor:
    """Full-spectrum fairness and bias auditor for rule-based and ML systems."""

    def __init__(self):
        pass

    def run_full_audit(self, test_df: pd.DataFrame) -> Dict[str, Any]:
        """Runs fairness analysis across all systems and demographic dimensions."""
        systems = {
            "Rule Engine (Standard)": "rule_pred_standard",
            "Rule Engine (Strict)": "rule_pred_strict",
            "Decision Tree": "dt_pred",
            "Logistic Regression": "lr_pred",
        }

        attributes = ["gender", "region_type", "age_band"]
        audit_by_system: Dict[str, Any] = {}

        for sys_name, pred_col in systems.items():
            if pred_col not in test_df.columns:
                continue
            audit_by_system[sys_name] = {}
            for att in attributes:
                audit_by_system[sys_name][att] = compute_group_metrics(
                    df=test_df,
                    group_col=att,
                    pred_col=pred_col,
                    truth_col="repaid",
                )

        proxy_findings = analyze_proxy_correlations(test_df)
        narrative = generate_fairness_narrative(audit_by_system, proxy_findings)

        return {
            "systems_audit": audit_by_system,
            "proxy_findings": proxy_findings,
            "narrative_findings": narrative["findings"],
            "recommendations": narrative["recommendations"],
            "methodology_limitations": narrative["limitations"],
        }
