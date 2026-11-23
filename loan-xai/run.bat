@echo off
echo ========================================================
echo  Starting LoanXAI: Explainable Rule-Based Credit System
echo ========================================================

echo [1/3] Verifying and seeding demo SQLite database...
python scripts\seed_demo.py

echo [2/3] Starting FastAPI Backend on http://127.0.0.1:8000...
start "LoanXAI Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [3/3] Starting Vite Frontend on http://127.0.0.1:5173...
start "LoanXAI Frontend" cmd /k "cd frontend && npm.cmd run dev"

echo All services launched!
echo Backend API Docs: http://127.0.0.1:8000/docs
echo Frontend Web App: http://127.0.0.1:5173
