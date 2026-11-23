"""FastAPI Route Handlers for Underwriting Evaluation, Analytics,
Model Benchmarking, Fairness Auditing, Rules Catalogue, and Exports.
"""

from typing import List, Optional
import uuid
import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.database import get_db, engine, Base
from app.db.models import Application, Decision, RuleExecution, MLRun, FairnessReport
from app.schemas.application import (
    EvaluateApplicationRequest,
    DecisionResponseSchema,
    ApplicationListItemSchema,
)
from app.rule_engine.engine import RuleEngine
from app.ml.data import generate_synthetic_dataset
from app.ml.models import MLManager
from app.fairness.audit import FairnessAuditor
from app.logic.pdf_report import generate_credit_audit_pdf

router = APIRouter(prefix="/api", tags=["Loan XAI"])

# Global singletons
rule_engine = RuleEngine()
ml_manager = MLManager()
fairness_auditor = FairnessAuditor()

# Ensure DB tables exist on import
Base.metadata.create_all(bind=engine)


@router.post("/evaluate", response_model=DecisionResponseSchema)
def evaluate_application(
    request: EvaluateApplicationRequest,
    db: Session = Depends(get_db),
):
    """Evaluates an application through the production rule engine and logs complete trace."""
    app_id = request.applicant_id or f"APP_{uuid.uuid4().hex[:8].upper()}"
    input_data = request.model_dump(mode="json")
    input_data["applicant_id"] = app_id

    # 1. Detect unusual-but-valid underwriting warnings
    input_warnings = request.detect_warnings()

    # 2. Run deterministic rule engine
    eval_result = rule_engine.evaluate(input_data)

    # 3. Obtain ML comparison prediction if models are loaded
    ml_comparison = None
    try:
        if ml_manager.dt_model:
            ml_comparison = ml_manager.predict_single(input_data)
    except Exception:
        pass

    # 4. Persist Application in DB
    app_record = Application(
        id=app_id,
        created_at=datetime.utcnow(),
        age=request.age,
        monthly_income=request.monthly_income,
        existing_monthly_debt=request.existing_monthly_debt,
        credit_score=request.credit_score,
        employment_years=request.employment_years,
        repayment_history=request.repayment_history.value,
        recent_default=request.recent_default,
        requested_amount=request.requested_amount,
        requested_tenure_months=request.requested_tenure_months,
        loan_purpose=request.loan_purpose.value,
        employment_type=request.employment_type.value,
        input_warnings=input_warnings,
    )
    db.add(app_record)

    # 5. Persist Decision
    dec_record = Decision(
        application_id=app_id,
        created_at=datetime.utcnow(),
        decision_status=eval_result["decision"],
        risk_class=eval_result["risk_class"],
        interest_rate=eval_result["interest_rate"],
        interest_rate_band=eval_result["interest_rate_band"],
        suggested_tenure_months=eval_result["suggested_tenure_months"],
        recommended_amount=eval_result["recommended_amount"],
        max_affordable_emi=eval_result["max_affordable_emi"],
        requested_emi=eval_result["requested_emi"],
        recommended_emi=eval_result["recommended_emi"],
        supportable_principal=eval_result["supportable_principal"],
        exceeds_affordability=eval_result["exceeds_affordability"],
        haircut_applied=eval_result["haircut_applied"],
        rationale_summary=eval_result["rationale_summary"],
        rejection_reasons=eval_result["rejection_reasons"],
        conditions=eval_result["conditions"],
        positive_factors=eval_result["positive_factors"],
        risk_factors=eval_result["risk_factors"],
        counterfactual_hints=eval_result["counterfactual_hints"],
        proof_trees=eval_result["proof_trees"],
        threshold_version=eval_result["threshold_version"],
    )
    db.add(dec_record)
    db.flush()  # assign dec_record.id

    # 6. Persist Rule Executions Trace
    for step in eval_result["execution_trace"]:
        re_step = RuleExecution(
            decision_id=dec_record.id,
            step_number=step["step"],
            rule_id=step["rule_id"],
            rule_name=step["rule_name"],
            rule_type=step.get("rule_type", "derivation"),
            priority=step.get("priority", 0),
            fol_form=step.get("fol_form"),
            plain_english=step.get("plain_english"),
            matched_facts=step.get("matched_facts", []),
            actual_input_values=step.get("actual_input_values", {}),
            asserted_facts=step.get("asserted_facts", []),
            competing_rules=step.get("competing_rules", []),
            resolution_reason=step.get("resolution_reason"),
        )
        db.add(re_step)

    db.commit()

    return DecisionResponseSchema(
        application_id=app_id,
        decision=eval_result["decision"],
        risk_class=eval_result["risk_class"],
        interest_rate=eval_result["interest_rate"],
        interest_rate_percent=eval_result["interest_rate_percent"],
        interest_rate_band=eval_result["interest_rate_band"],
        suggested_tenure_months=eval_result["suggested_tenure_months"],
        requested_amount=eval_result["requested_amount"],
        recommended_amount=eval_result["recommended_amount"],
        max_affordable_emi=eval_result["max_affordable_emi"],
        requested_emi=eval_result["requested_emi"],
        recommended_emi=eval_result["recommended_emi"],
        supportable_principal=eval_result["supportable_principal"],
        exceeds_affordability=eval_result["exceeds_affordability"],
        haircut_applied=eval_result["haircut_applied"],
        conditions=eval_result["conditions"],
        rejection_reasons=eval_result["rejection_reasons"],
        positive_factors=eval_result["positive_factors"],
        risk_factors=eval_result["risk_factors"],
        counterfactual_hints=eval_result["counterfactual_hints"],
        rationale_summary=eval_result["rationale_summary"],
        execution_trace=eval_result["execution_trace"],
        proof_trees=eval_result["proof_trees"],
        threshold_version=eval_result["threshold_version"],
        input_warnings=input_warnings,
        ml_comparison=ml_comparison,
    )


@router.get("/applications")
def list_applications(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    search: Optional[str] = None,
    status: Optional[str] = None,
    risk: Optional[str] = None,
):
    """Lists past evaluated applications with search and filtering."""
    query = db.query(Application).outerjoin(Decision)

    if search:
        query = query.filter(Application.id.ilike(f"%{search}%"))
    if status:
        query = query.filter(Decision.decision_status == status)
    if risk:
        query = query.filter(Decision.risk_class == risk)

    total_count = query.count()
    records = query.order_by(desc(Application.created_at)).offset(offset).limit(limit).all()

    items = []
    for r in records:
        dec = r.decision
        items.append({
            "id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else "",
            "age": r.age,
            "monthly_income": r.monthly_income,
            "existing_monthly_debt": r.existing_monthly_debt,
            "credit_score": r.credit_score,
            "employment_years": r.employment_years,
            "requested_amount": r.requested_amount,
            "requested_tenure_months": r.requested_tenure_months,
            "decision_status": dec.decision_status if dec else None,
            "risk_class": dec.risk_class if dec else None,
            "recommended_amount": dec.recommended_amount if dec else None,
            "interest_rate_band": dec.interest_rate_band if dec else None,
            "input_warnings_count": len(r.input_warnings or []),
        })

    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


@router.get("/applications/{application_id}")
def get_application_detail(application_id: str, db: Session = Depends(get_db)):
    """Retrieves full application inputs, decision verdict, and chronological rule trace."""
    app_record = db.query(Application).filter(Application.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail=f"Application '{application_id}' not found.")

    dec = app_record.decision
    if not dec:
        raise HTTPException(status_code=404, detail="Decision not found for application.")

    executions = (
        db.query(RuleExecution)
        .filter(RuleExecution.decision_id == dec.id)
        .order_by(RuleExecution.step_number.asc())
        .all()
    )

    trace = []
    for ex in executions:
        trace.append({
            "step": ex.step_number,
            "rule_id": ex.rule_id,
            "rule_name": ex.rule_name,
            "rule_type": ex.rule_type,
            "priority": ex.priority,
            "fol_form": ex.fol_form,
            "plain_english": ex.plain_english,
            "matched_facts": ex.matched_facts or [],
            "actual_input_values": ex.actual_input_values or {},
            "asserted_facts": ex.asserted_facts or [],
            "competing_rules": ex.competing_rules or [],
            "resolution_reason": ex.resolution_reason,
        })

    # Optional ML comparison
    ml_comparison = None
    if ml_manager.dt_model:
        try:
            ml_comparison = ml_manager.predict_single({
                "monthly_income": app_record.monthly_income,
                "existing_monthly_debt": app_record.existing_monthly_debt,
                "credit_score": app_record.credit_score,
                "employment_years": app_record.employment_years,
                "repayment_history": app_record.repayment_history,
                "recent_default": app_record.recent_default,
                "requested_amount": app_record.requested_amount,
                "requested_tenure_months": app_record.requested_tenure_months,
            })
        except Exception:
            pass

    return {
        "application": {
            "id": app_record.id,
            "created_at": app_record.created_at.isoformat() if app_record.created_at else "",
            "age": app_record.age,
            "monthly_income": app_record.monthly_income,
            "existing_monthly_debt": app_record.existing_monthly_debt,
            "credit_score": app_record.credit_score,
            "employment_years": app_record.employment_years,
            "repayment_history": app_record.repayment_history,
            "recent_default": app_record.recent_default,
            "requested_amount": app_record.requested_amount,
            "requested_tenure_months": app_record.requested_tenure_months,
            "loan_purpose": app_record.loan_purpose,
            "employment_type": app_record.employment_type,
            "input_warnings": app_record.input_warnings or [],
        },
        "decision": {
            "decision_status": dec.decision_status,
            "risk_class": dec.risk_class,
            "interest_rate": dec.interest_rate,
            "interest_rate_percent": round(dec.interest_rate * 100, 2),
            "interest_rate_band": dec.interest_rate_band,
            "suggested_tenure_months": dec.suggested_tenure_months,
            "recommended_amount": dec.recommended_amount,
            "max_affordable_emi": dec.max_affordable_emi,
            "requested_emi": dec.requested_emi,
            "recommended_emi": dec.recommended_emi,
            "supportable_principal": dec.supportable_principal,
            "exceeds_affordability": dec.exceeds_affordability,
            "haircut_applied": dec.haircut_applied,
            "rationale_summary": dec.rationale_summary,
            "rejection_reasons": dec.rejection_reasons or [],
            "conditions": dec.conditions or [],
            "positive_factors": dec.positive_factors or [],
            "risk_factors": dec.risk_factors or [],
            "counterfactual_hints": dec.counterfactual_hints or [],
            "proof_trees": dec.proof_trees or [],
            "threshold_version": dec.threshold_version,
            "created_at": dec.created_at.isoformat() if dec.created_at else "",
        },
        "execution_trace": trace,
        "ml_comparison": ml_comparison,
    }


@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Computes summary operational and underwriting performance metrics."""
    total_apps = db.query(Application).count()
    if total_apps == 0:
        return {
            "total_applications": 0,
            "eligible_count": 0,
            "conditional_count": 0,
            "not_eligible_count": 0,
            "approval_rate_percent": 0.0,
            "average_requested_amount": 0.0,
            "average_recommended_amount": 0.0,
            "decision_distribution": [
                {"name": "Eligible", "value": 0, "color": "#16A34A"},
                {"name": "Conditional", "value": 0, "color": "#CA8A04"},
                {"name": "Not Eligible", "value": 0, "color": "#DC2626"},
            ],
            "risk_distribution": [
                {"tier": "Low Risk", "count": 0, "color": "#2563EB"},
                {"tier": "Medium Risk", "count": 0, "color": "#F59E0B"},
                {"tier": "High Risk", "count": 0, "color": "#EF4444"},
            ],
            "recent_applications": [],
        }

    decisions = db.query(Decision).all()
    eligible_count = sum(1 for d in decisions if d.decision_status == "ELIGIBLE")
    conditional_count = sum(1 for d in decisions if d.decision_status == "CONDITIONALLY_ELIGIBLE")
    not_eligible_count = sum(1 for d in decisions if d.decision_status == "NOT_ELIGIBLE")

    low_risk = sum(1 for d in decisions if d.risk_class == "LOW")
    med_risk = sum(1 for d in decisions if d.risk_class == "MEDIUM")
    high_risk = sum(1 for d in decisions if d.risk_class == "HIGH")

    apps = db.query(Application).all()
    avg_requested = sum(a.requested_amount for a in apps) / len(apps) if apps else 0.0
    approved_decisions = [d.recommended_amount for d in decisions if d.recommended_amount > 0]
    avg_recommended = sum(approved_decisions) / len(approved_decisions) if approved_decisions else 0.0

    recent_records = (
        db.query(Application)
        .outerjoin(Decision)
        .order_by(desc(Application.created_at))
        .limit(10)
        .all()
    )

    recent_items = []
    for r in recent_records:
        dec = r.decision
        recent_items.append({
            "id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else "",
            "credit_score": r.credit_score,
            "monthly_income": r.monthly_income,
            "requested_amount": r.requested_amount,
            "decision_status": dec.decision_status if dec else "PENDING",
            "risk_class": dec.risk_class if dec else "UNKNOWN",
            "recommended_amount": dec.recommended_amount if dec else 0.0,
        })

    approval_rate = round(((eligible_count + conditional_count) / total_apps) * 100, 2)

    return {
        "total_applications": total_apps,
        "eligible_count": eligible_count,
        "conditional_count": conditional_count,
        "not_eligible_count": not_eligible_count,
        "approval_rate_percent": approval_rate,
        "average_requested_amount": round(avg_requested, 2),
        "average_recommended_amount": round(avg_recommended, 2),
        "decision_distribution": [
            {"name": "Eligible", "value": eligible_count, "color": "#16A34A"},
            {"name": "Conditional", "value": conditional_count, "color": "#CA8A04"},
            {"name": "Not Eligible", "value": not_eligible_count, "color": "#DC2626"},
        ],
        "risk_distribution": [
            {"tier": "Low Risk", "count": low_risk, "color": "#2563EB"},
            {"tier": "Medium Risk", "count": med_risk, "color": "#F59E0B"},
            {"tier": "High Risk", "count": high_risk, "color": "#EF4444"},
        ],
        "recent_applications": recent_items,
    }


@router.get("/ml/metrics")
def get_ml_metrics(db: Session = Depends(get_db)):
    """Returns the latest trained ML metrics, comparison against rule engine, and edge case suite."""
    if not ml_manager.latest_results:
        # Check DB for persisted run
        latest_run = db.query(MLRun).order_by(desc(MLRun.trained_at)).first()
        if latest_run:
            ml_manager.latest_results = latest_run.results_json
        else:
            # Auto-train initial model if not yet trained
            retrain_ml_models(db)

    return ml_manager.latest_results


@router.post("/ml/retrain")
def retrain_ml_models(db: Session = Depends(get_db)):
    """Generates synthetic dataset and retrains Decision Tree and Logistic Regression models."""
    df = generate_synthetic_dataset(n_samples=6000, seed=42)
    results = ml_manager.train_and_evaluate(df, test_size=0.20, seed=42)

    # Persist in DB
    run_record = MLRun(
        trained_at=datetime.utcnow(),
        n_train_samples=results["dataset_summary"]["train_samples"],
        n_test_samples=results["dataset_summary"]["test_samples"],
        results_json=results,
    )
    db.add(run_record)

    # Run and persist fairness report
    fairness_data = fairness_auditor.run_full_audit(ml_manager.test_df)
    fn_record = FairnessReport(
        generated_at=datetime.utcnow(),
        report_json=fairness_data,
    )
    db.add(fn_record)

    db.commit()
    return {
        "status": "success",
        "message": "Models successfully retrained and evaluated on held-out test set.",
        "results": results,
    }


@router.get("/fairness/report")
def get_fairness_report(db: Session = Depends(get_db)):
    """Returns demographic parity, disparate impact ratios, and proxy correlations."""
    if ml_manager.test_df is None or "rule_pred_standard" not in ml_manager.test_df.columns:
        # Load from DB or trigger quick training
        latest_rep = db.query(FairnessReport).order_by(desc(FairnessReport.generated_at)).first()
        if latest_rep:
            return latest_rep.report_json
        retrain_ml_models(db)

    audit_result = fairness_auditor.run_full_audit(ml_manager.test_df)
    return audit_result


@router.get("/rules")
def get_rules_catalogue():
    """Returns the declarative production rules catalogue and active thresholds."""
    return {
        "rules": rule_engine.rules_list,
        "thresholds": rule_engine.thresholds_config,
        "total_rules": len(rule_engine.rules_list),
    }


@router.get("/applications/{application_id}/pdf")
def export_application_pdf(application_id: str, db: Session = Depends(get_db)):
    """Generates and downloads a ReportLab credit underwriting audit memorandum."""
    app_record = db.query(Application).filter(Application.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found.")

    dec = app_record.decision
    if not dec:
        raise HTTPException(status_code=404, detail="Decision not found.")

    executions = (
        db.query(RuleExecution)
        .filter(RuleExecution.decision_id == dec.id)
        .order_by(RuleExecution.step_number.asc())
        .all()
    )

    app_dict = {
        "id": app_record.id,
        "monthly_income": app_record.monthly_income,
        "existing_monthly_debt": app_record.existing_monthly_debt,
        "credit_score": app_record.credit_score,
        "employment_years": app_record.employment_years,
        "repayment_history": app_record.repayment_history,
        "recent_default": app_record.recent_default,
        "requested_amount": app_record.requested_amount,
        "requested_tenure_months": app_record.requested_tenure_months,
        "employment_type": app_record.employment_type,
    }

    dec_dict = {
        "created_at": dec.created_at.strftime("%Y-%m-%d %H:%M:%S") if dec.created_at else "",
        "threshold_version": dec.threshold_version,
        "decision_status": dec.decision_status,
        "risk_class": dec.risk_class,
        "interest_rate_band": dec.interest_rate_band,
        "recommended_amount": dec.recommended_amount,
        "max_affordable_emi": dec.max_affordable_emi,
        "supportable_principal": dec.supportable_principal,
        "rationale_summary": dec.rationale_summary,
        "rejection_reasons": dec.rejection_reasons or [],
        "conditions": dec.conditions or [],
        "counterfactual_hints": dec.counterfactual_hints or [],
        "rule_executions": [
            {
                "step_number": ex.step_number,
                "rule_id": ex.rule_id,
                "rule_name": ex.rule_name,
                "fol_form": ex.fol_form,
                "plain_english": ex.plain_english,
            }
            for ex in executions
        ],
    }

    pdf_bytes = generate_credit_audit_pdf(app_dict, dec_dict)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="Credit_Audit_{application_id}.pdf"'},
    )


@router.get("/applications/export/csv")
def export_applications_csv(db: Session = Depends(get_db)):
    """Exports all applications and underwriting decisions to a CSV file."""
    records = db.query(Application).outerjoin(Decision).order_by(desc(Application.created_at)).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "application_id", "created_at", "age", "monthly_income", "existing_monthly_debt",
        "credit_score", "employment_years", "repayment_history", "recent_default",
        "requested_amount", "requested_tenure_months", "decision_status", "risk_class",
        "recommended_amount", "interest_rate_percent", "supportable_principal", "exceeds_affordability"
    ])

    for r in records:
        dec = r.decision
        writer.writerow([
            r.id,
            r.created_at.isoformat() if r.created_at else "",
            r.age,
            r.monthly_income,
            r.existing_monthly_debt,
            r.credit_score,
            r.employment_years,
            r.repayment_history,
            r.recent_default,
            r.requested_amount,
            r.requested_tenure_months,
            dec.decision_status if dec else "",
            dec.risk_class if dec else "",
            dec.recommended_amount if dec else 0.0,
            round(dec.interest_rate * 100, 2) if dec else 0.0,
            dec.supportable_principal if dec else 0.0,
            dec.exceeds_affordability if dec else False,
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="loan_applications_export.csv"'},
    )
