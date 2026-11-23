"""FastAPI Application Entry Point for Explainable AI Loan Underwriting."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router, retrain_ml_models
from app.db.database import SessionLocal, engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema
    Base.metadata.create_all(bind=engine)
    # Train initial baseline ML model on startup if table is empty
    db = SessionLocal()
    try:
        from app.db.models import MLRun
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

# Enable CORS for local development (Vite frontend on 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "system": "Explainable Rule-Based Loan Eligibility & Credit Decision System",
        "course": "Artificial Intelligence Foundations",
        "status": "online",
        "api_docs": "/docs",
        "disclaimer": "Academic demo. Rates and amounts are illustrative, not bank offers. Approval is never guaranteed.",
    }
