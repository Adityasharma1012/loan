#!/usr/bin/env bash
set -e

echo "========================================================"
echo " Starting LoanXAI: Explainable Rule-Based Credit System "
echo "========================================================"

echo "[1/3] Seeding demo SQLite database..."
python scripts/seed_demo.py

echo "[2/3] Starting FastAPI Backend on http://127.0.0.1:8000..."
(cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload) &
BACKEND_PID=$!

echo "[3/3] Starting Vite Frontend on http://127.0.0.1:5173..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
echo "All services running. Press Ctrl+C to stop."
wait
