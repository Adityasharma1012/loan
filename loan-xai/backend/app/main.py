"""FastAPI Application Entry Point for Explainable AI Loan Underwriting."""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.endpoints import router as api_router, retrain_ml_models
from app.db.database import SessionLocal, engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema
    Base.metadata.create_all(bind=engine)
    # Train initial baseline ML model on startup if table is empty
    db = SessionLocal()
    try:
        from app.db.models import MLRun, Application, Decision
        # Seed initial demonstration applications if table is empty
        if db.query(Application).count() == 0:
            print("[INFO] Seeding initial demonstration loan applications...")
            from app.rule_engine.engine import RuleEngine
            from app.schemas.application import EvaluateApplicationRequest
            from app.ml.data import generate_synthetic_dataset
            from datetime import datetime, timedelta
            import random

            engine_instance = RuleEngine()
            df = generate_synthetic_dataset(n_samples=25, seed=42)
            purposes = ["Personal", "Debt Consolidation", "Home Improvement"]
            emp_types = ["Salaried", "Self-Employed"]

            for i, row in df.iterrows():
                app_id = f"DEMO_{i+1:04d}"
                created_at = datetime.utcnow() - timedelta(
                    days=random.randint(0, 15),
                    hours=random.randint(0, 23)
                )
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
                    existing_loan_count=int(row["existing_loan_count"]),
                    loan_purpose=purposes[i % len(purposes)],
                    employment_type=emp_types[i % len(emp_types)],
                )
                app_rec = Application(
                    id=app_id,
                    applicant_id=app_id,
                    age=req.age,
                    monthly_income=req.monthly_income,
                    existing_monthly_debt=req.existing_monthly_debt,
                    credit_score=req.credit_score,
                    employment_years=req.employment_years,
                    repayment_history=req.repayment_history,
                    recent_default=req.recent_default,
                    requested_amount=req.requested_amount,
                    requested_tenure_months=req.requested_tenure_months,
                    existing_loan_count=req.existing_loan_count,
                    loan_purpose=req.loan_purpose,
                    employment_type=req.employment_type,
                    created_at=created_at,
                )
                db.add(app_rec)
                eval_res = engine_instance.evaluate(req.model_dump())
                calc = eval_res["financial_calculations"]
                dec = Decision(
                    application_id=app_id,
                    decision_status=eval_res["decision"],
                    risk_class=eval_res["risk_class"],
                    interest_rate=eval_res["interest_rate"],
                    interest_rate_band=eval_res["interest_rate_band"],
                    suggested_tenure_months=eval_res["suggested_tenure_months"],
                    recommended_amount=eval_res["recommended_amount"],
                    max_affordable_emi=calc["max_affordable_emi"],
                    requested_emi=calc["requested_emi"],
                    recommended_emi=calc["recommended_emi"],
                    supportable_principal=calc["supportable_principal"],
                    exceeds_affordability=calc["exceeds_affordability"],
                    haircut_applied=calc["haircut_applied"],
                    rationale_summary=eval_res["rationale_summary"],
                    rejection_reasons=eval_res["rejection_reasons"],
                    conditions=eval_res["conditions"],
                    positive_factors=eval_res["positive_factors"],
                    risk_factors=eval_res["risk_factors"],
                    counterfactual_hints=eval_res["counterfactual_hints"],
                    proof_trees=eval_res["proof_trees"],
                    threshold_version=eval_res["threshold_version"],
                    created_at=created_at,
                )
                db.add(dec)
            db.commit()
            print("[INFO] Initial demonstration applications seeded successfully!")

        if db.query(MLRun).count() == 0:
            print("[INFO] Initializing baseline ML models and fairness metrics...")
            retrain_ml_models(db)
    except Exception as e:
        print(f"[WARN] Startup baseline ML initialization: {e}")
    finally:
        db.close()
    yield


app = FastAPI(
    title="Explainable Rule-Based Loan Eligibility & Credit Decision System",
    description="Academic Demonstration Expert System combining Production Rules, First-Order Logic, and ML Auditing.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend clients (development + production hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(api_router)


# Health check for Render / Cloud monitors
@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "loan-xai-backend"}


# Locate optional compiled frontend assets
backend_dir = Path(__file__).resolve().parent.parent
possible_dist_dirs = [
    backend_dir.parent / "frontend" / "dist",
    backend_dir / "frontend" / "dist",
    Path("/app/frontend/dist"),
]

frontend_dist = None
for dist_candidate in possible_dist_dirs:
    if dist_candidate.exists() and (dist_candidate / "index.html").exists():
        frontend_dist = dist_candidate
        break

if frontend_dist:
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


@app.get("/")
def root(request: Request):
    accept = request.headers.get("accept", "")
    # Serve React SPA index.html to web browsers if frontend is built
    if "text/html" in accept and frontend_dist and (frontend_dist / "index.html").exists():
        return FileResponse(frontend_dist / "index.html")
    
    # Return JSON API root for test clients and API consumers
    return {
        "system": "Explainable Rule-Based Loan Eligibility & Credit Decision System",
        "course": "Artificial Intelligence Foundations",
        "status": "online",
        "api_docs": "/docs",
        "disclaimer": "Academic demo. Rates and amounts are illustrative, not bank offers. Approval is never guaranteed.",
    }


# Catch-all route to serve SPA client-side routes (if frontend is built)
if frontend_dist:
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path in ("docs", "redoc", "openapi.json", "healthz"):
            raise HTTPException(status_code=404, detail="Not Found")
        
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_dist / "index.html")
