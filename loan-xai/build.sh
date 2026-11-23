#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "[1/2] Installing backend Python dependencies..."
cd backend
pip install -r requirements.txt

echo "[2/2] Seeding initial database and training baseline models..."
python -c "from app.db.database import Base, engine, SessionLocal; from app.api.endpoints import retrain_ml_models; Base.metadata.create_all(bind=engine); db = SessionLocal(); retrain_ml_models(db); db.close()"

echo "[DONE] Build completed successfully!"
