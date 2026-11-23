"""Seeds the SQLite database with diverse demo applicants evaluated through the real rule engine.
Every row and statistic in the dashboard is generated through the actual production rules.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.db.database import SessionLocal, Base, engine
from app.db.models import Application, Decision, RuleExecution
from app.rule_engine.engine import RuleEngine
from app.schemas.application import EvaluateApplicationRequest
from app.ml.data import generate_synthetic_dataset


def seed_database(n_applicants: int = 120, seed: int = 42):
    print(f"[Seed] Generating {n_applicants} synthetic applicants and evaluating via real rule engine...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    engine_instance = RuleEngine()

    try:
        # Generate rich synthetic sample
        df = generate_synthetic_dataset(n_samples=n_applicants, seed=seed)
        
        # Purge existing demo data to ensure a fresh clean seed
        db.query(RuleExecution).delete()
        db.query(Decision).delete()
        db.query(Application).delete()
        db.commit()

        purposes = ["Personal", "Debt Consolidation", "Home Improvement", "Education", "Business", "Medical"]
        emp_types = ["Salaried", "Self-Employed", "Business Owner"]

        for i, row in df.iterrows():
            app_id = f"DEMO_{i+1:04d}"
            
            # Stagger creation timestamps over the past 30 days
            created_at = datetime.utcnow() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            # Build request payload
            req = EvaluateApplicationRequest(
                applicant_id=app_id,
                age=int(row["age"]),
                monthly_income=float(row["monthly_income"]),
                existing_monthly_debt=float(row["existing_monthly_debt"]),
                credit_score=int(row["credit_score"]),
                employment_years=float(row["employment_years"]),
                repayment_history=str(row["repayment_history"]),
                recent_default=bool(row["recent_default"]),
                requested_amount=float(row["requested_amount"]),
                requested_tenure_months=int(row["requested_tenure_months"]),
                loan_purpose=random.choice(purposes),
                employment_type=random.choice(emp_types),
            )

            input_dict = req.model_dump()
            input_warnings = req.detect_warnings()

            # Run REAL rule engine
            eval_res = engine_instance.evaluate(input_dict)

            # Persist Application
            app_rec = Application(
                id=app_id,
                created_at=created_at,
                age=req.age,
                monthly_income=req.monthly_income,
                existing_monthly_debt=req.existing_monthly_debt,
                credit_score=req.credit_score,
                employment_years=req.employment_years,
                repayment_history=req.repayment_history.value,
                recent_default=req.recent_default,
                requested_amount=req.requested_amount,
                requested_tenure_months=req.requested_tenure_months,
                loan_purpose=req.loan_purpose.value,
                employment_type=req.employment_type.value,
                input_warnings=input_warnings,
            )
            db.add(app_rec)

            # Persist Decision
            dec_rec = Decision(
                application_id=app_id,
                created_at=created_at,
                decision_status=eval_res["decision"],
                risk_class=eval_res["risk_class"],
                interest_rate=eval_res["interest_rate"],
                interest_rate_band=eval_res["interest_rate_band"],
                suggested_tenure_months=eval_res["suggested_tenure_months"],
                recommended_amount=eval_res["recommended_amount"],
                max_affordable_emi=eval_res["max_affordable_emi"],
                requested_emi=eval_res["requested_emi"],
                recommended_emi=eval_res["recommended_emi"],
                supportable_principal=eval_res["supportable_principal"],
                exceeds_affordability=eval_res["exceeds_affordability"],
                haircut_applied=eval_res["haircut_applied"],
                rationale_summary=eval_res["rationale_summary"],
                rejection_reasons=eval_res["rejection_reasons"],
                conditions=eval_res["conditions"],
                positive_factors=eval_res["positive_factors"],
                risk_factors=eval_res["risk_factors"],
                counterfactual_hints=eval_res["counterfactual_hints"],
                proof_trees=eval_res["proof_trees"],
                threshold_version=eval_res["threshold_version"],
            )
            db.add(dec_rec)
            db.flush()

            # Persist Executions Trace
            for step in eval_res["execution_trace"]:
                db.add(RuleExecution(
                    decision_id=dec_rec.id,
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
                ))

        db.commit()
        print(f"[Seed] Successfully seeded {n_applicants} applications through the real rule engine!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
