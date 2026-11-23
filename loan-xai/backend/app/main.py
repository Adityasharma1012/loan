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
