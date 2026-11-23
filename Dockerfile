# Multi-stage Dockerfile for unified deployment on Render
# Stage 1: Build React Vite frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY loan-xai/frontend/package*.json ./
RUN npm ci || npm install

COPY loan-xai/frontend/ ./
RUN npm run build

# Stage 2: Python FastAPI backend + Serve built frontend
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY loan-xai/backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY loan-xai/backend ./backend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

WORKDIR /app/backend

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
