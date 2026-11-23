# Deploying LoanXAI on Render

This guide explains how to host the **Explainable Rule-Based Loan Eligibility & Credit Decision System** on [Render](https://render.com).

---

## Method 1: Render Blueprint (Recommended — 1-Click Automated Setup)

The repository includes a ready-to-use [`render.yaml`](./render.yaml) Infrastructure-as-Code blueprint that automatically sets up:
1. **`loan-xai-backend`**: FastAPI Python Web Service.
2. **`loan-xai-frontend`**: React Vite Static Site with client-side SPA routing and automatic `VITE_API_URL` linking.

### Step-by-Step Instructions:
1. **Push your code to GitHub** (already configured to `https://github.com/Adityasharma1012/loan.git`).
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click the **"New +"** button at the top right and select **"Blueprint"**.
4. Connect and select your repository: **`Adityasharma1012/loan`**.
5. Render will automatically parse `render.yaml` and display the two services:
   - `loan-xai-backend` (Web Service, Python 3.11, Free plan)
   - `loan-xai-frontend` (Static Site, Free plan)
6. Click **"Apply"**.
7. Render will build and deploy both services automatically! Once deployed, visit your `loan-xai-frontend.onrender.com` URL.

---

## Method 2: Manual Dashboard Setup (Two Services)

If you prefer configuring services manually via the Render UI:

### Step 1: Deploy Backend Web Service
1. In Render Dashboard, click **"New +"** → **"Web Service"**.
2. Connect your GitHub repository (`Adityasharma1012/loan`).
3. Configure the following fields:
   - **Name:** `loan-xai-backend`
   - **Language:** `Python`
   - **Root Directory:** `loan-xai/backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** `Free`
4. In **Advanced Settings**:
   - Add Environment Variable: `PYTHON_VERSION` = `3.11.9`
   - **Health Check Path:** `/healthz`
5. Click **"Create Web Service"**. Copy the public URL (e.g. `https://loan-xai-backend.onrender.com`).

---

### Step 2: Deploy Frontend Static Site
1. In Render Dashboard, click **"New +"** → **"Static Site"**.
2. Connect your GitHub repository (`Adityasharma1012/loan`).
3. Configure the following fields:
   - **Name:** `loan-xai-frontend`
   - **Root Directory:** `loan-xai/frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. In **Environment Variables**:
   - Add `VITE_API_URL` = `https://loan-xai-backend.onrender.com` *(paste your backend URL from Step 1)*
5. In **Redirects / Rewrites**:
   - Add rule:
     - **Type:** `Rewrite`
     - **Source:** `/*`
     - **Destination:** `/index.html`
6. Click **"Create Static Site"**.

---

## Method 3: Single Unified Container (Docker)

If you want a single URL that hosts both the API and the React frontend on one Free Web Service:

1. Click **"New +"** → **"Web Service"**.
2. Connect your GitHub repo.
3. Select **"Docker"** as the runtime.
4. Render will automatically detect the root [`Dockerfile`](./Dockerfile):
   - Stage 1 compiles the React frontend (`npm run build`).
   - Stage 2 starts FastAPI, which serves the API at `/api/` and the React SPA at `/`.
5. Click **"Create Web Service"**.

---

## Useful Information & Verification

- **API Documentation (Swagger UI):** Available at `https://<your-backend-url>/docs`
- **Health Check Endpoint:** `https://<your-backend-url>/healthz`
- **Render Free Tier Note:** Render spins down free web services after 15 minutes of inactivity. When a request arrives, it takes ~30–45 seconds to spin up, after which it responds at full speed.
