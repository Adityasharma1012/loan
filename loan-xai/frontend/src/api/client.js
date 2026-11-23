// Dynamic API base resolution:
// 1. If VITE_API_URL is configured (e.g. Render production URL), use it.
// 2. In Vite development mode, default to local backend on http://127.0.0.1:8000/api.
// 3. In production with unified serving / reverse proxy, default to /api.
const rawApiUrl = import.meta.env.VITE_API_URL;
const API_BASE = rawApiUrl
  ? `${rawApiUrl.replace(/\/$/, "")}/api`
  : (import.meta.env.DEV ? "http://127.0.0.1:8000/api" : "/api");

export async function evaluateApplication(payload) {
  const res = await fetch(`${API_BASE}/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ? (typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail)) : "Evaluation failed");
  }
  return res.json();
}

export async function fetchApplications({ limit = 50, offset = 0, search = "", status = "", risk = "" } = {}) {
  const params = new URLSearchParams();
  params.append("limit", limit);
  params.append("offset", offset);
  if (search) params.append("search", search);
  if (status) params.append("status", status);
  if (risk) params.append("risk", risk);

  const res = await fetch(`${API_BASE}/applications?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch applications list");
  return res.json();
}

export async function fetchApplicationDetail(id) {
  const res = await fetch(`${API_BASE}/applications/${encodeURIComponent(id)}`);
  if (!res.ok) throw new Error(`Application ${id} not found`);
  return res.json();
}

export async function fetchDashboardStats() {
  const res = await fetch(`${API_BASE}/dashboard/stats`);
  if (!res.ok) throw new Error("Failed to fetch dashboard stats");
  return res.json();
}

export async function fetchMLMetrics() {
  const res = await fetch(`${API_BASE}/ml/metrics`);
  if (!res.ok) throw new Error("Failed to fetch ML metrics");
  return res.json();
}

export async function retrainMLModels() {
  const res = await fetch(`${API_BASE}/ml/retrain`, { method: "POST" });
  if (!res.ok) throw new Error("Retraining failed");
  return res.json();
}

export async function fetchFairnessReport() {
  const res = await fetch(`${API_BASE}/fairness/report`);
  if (!res.ok) throw new Error("Failed to fetch fairness report");
  return res.json();
}

export async function fetchRulesCatalogue() {
  const res = await fetch(`${API_BASE}/rules`);
  if (!res.ok) throw new Error("Failed to fetch rules catalogue");
  return res.json();
}

export function getPDFExportUrl(id) {
  return `${API_BASE}/applications/${encodeURIComponent(id)}/pdf`;
}

export function getCSVExportUrl() {
  return `${API_BASE}/applications/export/csv`;
}
