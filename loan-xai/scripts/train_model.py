"""Script to generate synthetic training dataset and train/persist ML benchmark models."""

import os
import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.db.database import SessionLocal, Base, engine
from app.api.endpoints import retrain_ml_models


def main():
    print("[1/2] Initializing SQLite database...")
    Base.metadata.create_all(bind=engine)
    
    print("[2/2] Generating synthetic data and training Decision Tree & Logistic Regression...")
    db = SessionLocal()
    try:
        res = retrain_ml_models(db)
        print("Success! Results summary:")
        models = res["results"]["models"]
        for m_key, m_val in models.items():
            print(f" - {m_val['name']}: Accuracy = {m_val['metrics']['accuracy']:.4f}, F1 = {m_val['metrics']['f1_score']:.4f}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
