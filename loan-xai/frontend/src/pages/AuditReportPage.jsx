import React, { useState, useEffect } from "react";
import {
  FileText,
  Download,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Binary,
  Layers,
  ArrowLeft,
} from "lucide-react";
import { fetchApplicationDetail, getPDFExportUrl } from "../api/client";
import DecisionBadge from "../components/DecisionBadge";

export default function AuditReportPage({ selectedAppId, setSelectedAppId, setCurrentPage }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedAppId) {
      setLoading(true);
      fetchApplicationDetail(selectedAppId)
        .then((res) => setReport(res))
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [selectedAppId]);

  if (loading) {
    return <div className="p-12 text-center text-slate-500 animate-pulse">Generating credit underwriting memo...</div>;
  }

  if (error || !report) {
    return (
      <div className="p-10 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-xl mx-auto space-y-4">
        <FileText className="w-12 h-12 text-slate-400 mx-auto" />
        <h3 className="font-bold text-base text-slate-900 dark:text-slate-100">
          No Application Selected
        </h3>
        <p className="text-xs text-slate-500">
          Please select an application from the History or Executive Dashboard to review its formal audit memorandum.
        </p>
        <button
          onClick={() => setCurrentPage("history")}
          className="px-4 py-2 bg-finblue-600 text-white rounded-lg text-xs font-semibold"
        >
          Browse Applications History
        </button>
      </div>
    );
  }

  const app = report.application;
  const dec = report.decision;
  const trace = report.execution_trace || [];
  const hints = dec.counterfactual_hints || [];

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-12 font-sans">
      {/* Top Action Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setCurrentPage("history")}
          className="flex items-center gap-1.5 text-xs font-medium text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Applications</span>
        </button>

        <a
          href={getPDFExportUrl(app.id)}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-2 px-4 py-2 bg-finblue-600 hover:bg-finblue-500 text-white text-xs font-semibold rounded-lg shadow-sm shadow-finblue-600/30 transition-all"
        >
          <Download className="w-4 h-4" />
          <span>Download PDF Audit Memorandum</span>
        </a>
      </div>

      {/* Memorandum Paper Container */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 sm:p-10 shadow-sm space-y-8">
        {/* Memo Institutional Header */}
        <div className="border-b border-slate-200 dark:border-slate-800 pb-6 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-navy-900 text-white flex items-center justify-center font-bold font-mono text-sm">
                XAI
              </div>
              <div>
                <h1 className="text-lg font-extrabold text-navy-900 dark:text-slate-100 tracking-tight">
                  CREDIT UNDERWRITING EXPLAINABILITY MEMORANDUM
                </h1>
                <div className="text-[11px] text-slate-500">
                  Course: Artificial Intelligence Foundations • Production Expert System
                </div>
              </div>
            </div>

            <div className="text-right text-[11px] font-mono text-slate-500">
              <div>Policy Version: <b>{dec.threshold_version}</b></div>
              <div>Evaluated: <b>{dec.created_at ? dec.created_at.replace("T", " ").slice(0, 19) : ""}</b></div>
            </div>
          </div>
        </div>

        {/* Verdict Callout Banner */}
        <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-[10px] uppercase font-bold text-slate-400">Application Reference</div>
            <div className="font-mono font-bold text-base text-slate-900 dark:text-slate-100 mt-0.5">
              {app.id}
            </div>
          </div>

          <div>
            <div className="text-[10px] uppercase font-bold text-slate-400">Formal Verdict</div>
            <div className="mt-0.5">
              <DecisionBadge status={dec.decision_status} size="sm" />
            </div>
          </div>

          <div>
            <div className="text-[10px] uppercase font-bold text-slate-400">Risk Class</div>
            <div className="font-bold text-sm text-slate-800 dark:text-slate-200 mt-0.5 font-mono">
              {dec.risk_class}
            </div>
          </div>

          <div>
            <div className="text-[10px] uppercase font-bold text-slate-400">Approved Principal</div>
            <div className="font-bold text-base text-finblue-600 dark:text-finblue-400 mt-0.5 font-mono">
              {dec.recommended_amount > 0 ? `₹${dec.recommended_amount.toLocaleString()}` : "₹0"}
            </div>
          </div>

          <div>
            <div className="text-[10px] uppercase font-bold text-slate-400">Interest Band</div>
            <div className="font-bold text-sm text-slate-800 dark:text-slate-200 mt-0.5 font-mono">
              {dec.interest_rate_percent}% ({dec.interest_rate_band})
            </div>
          </div>
        </div>

        {/* Section 1: Financial & Debt Service Profile */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 pb-1 border-b border-slate-100 dark:border-slate-800">
            1. Borrower Financial & Debt Service Profile
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Monthly Gross Income</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">₹{app.monthly_income?.toLocaleString()}</span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Monthly Debt Obligations</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">₹{app.existing_monthly_debt?.toLocaleString()}</span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Debt-to-Income (DTI)</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">
                {app.monthly_income > 0 ? ((app.existing_monthly_debt / app.monthly_income) * 100).toFixed(1) : 0}%
              </span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Credit Bureau Score</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">{app.credit_score}</span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Employment Tenure</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">{app.employment_years} yrs ({app.employment_type})</span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Repayment Record</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">{app.repayment_history} (Default: {app.recent_default ? "Yes" : "No"})</span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Requested Principal</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">₹{app.requested_amount?.toLocaleString()} ({app.requested_tenure_months} mo)</span>
            </div>
            <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200/60 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-sans">Max Affordable EMI</span>
              <span className="font-bold text-slate-800 dark:text-slate-200">₹{dec.max_affordable_emi?.toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
            </div>
          </div>
        </div>

        {/* Section 2: Rationale & Adverse Action Grounds */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 pb-1 border-b border-slate-100 dark:border-slate-800">
            2. Decision Rationale & Adverse Action Analysis
          </h3>
          <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-slate-950 p-3.5 rounded-xl border border-slate-200/60 dark:border-slate-800">
            {dec.rationale_summary}
          </p>

          {dec.rejection_reasons && dec.rejection_reasons.length > 0 && (
            <div className="bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/40 rounded-xl p-3 text-xs text-rose-800 dark:text-rose-300 space-y-1">
              <div className="font-bold uppercase tracking-wider text-[10px]">Adverse Action Notice (FCRA/ECOA Grounds):</div>
              {dec.rejection_reasons.map((r, i) => (
                <div key={i}>• {r}</div>
              ))}
            </div>
          )}

          {dec.conditions && dec.conditions.length > 0 && (
            <div className="bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 rounded-xl p-3 text-xs text-amber-800 dark:text-amber-300 space-y-1">
              <div className="font-bold uppercase tracking-wider text-[10px]">Conditional Covenants:</div>
              {dec.conditions.map((c, i) => (
                <div key={i}>• {c}</div>
              ))}
            </div>
          )}
        </div>

        {/* Section 3: Counterfactual Explanations */}
        {hints.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 pb-1 border-b border-slate-100 dark:border-slate-800">
              3. Counterfactual Sensitivity & Prescribed Remediation
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-slate-600">
                    <th className="py-2 px-3 font-semibold">Underwriting Parameter</th>
                    <th className="py-2 px-3 font-semibold">Observed</th>
                    <th className="py-2 px-3 font-semibold">Policy Benchmark</th>
                    <th className="py-2 px-3 font-semibold">Prescribed Counterfactual Delta</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                  {hints.map((h, i) => (
                    <tr key={i}>
                      <td className="py-2.5 px-3 font-bold uppercase font-mono text-[11px]">{h.feature}</td>
                      <td className="py-2.5 px-3 font-mono">{String(h.current_value)}</td>
                      <td className="py-2.5 px-3 font-mono text-emerald-600 dark:text-emerald-400 font-bold">{String(h.target_value)}</td>
                      <td className="py-2.5 px-3">{h.delta_description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Section 4: Production Rule Execution Trace */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 pb-1 border-b border-slate-100 dark:border-slate-800">
            4. Production Rule Execution Trace (Inference Proof)
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-slate-600">
                  <th className="py-2 px-2.5 font-semibold">Step</th>
                  <th className="py-2 px-2.5 font-semibold">Rule ID</th>
                  <th className="py-2 px-2.5 font-semibold">Rule Name</th>
                  <th className="py-2 px-2.5 font-semibold">First-Order Logic Horn Clause</th>
                  <th className="py-2 px-2.5 font-semibold">Plain-English Rationale</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                {trace.map((s, i) => (
                  <tr key={i}>
                    <td className="py-2.5 px-2.5 font-mono text-[11px] font-bold">{s.step}</td>
                    <td className="py-2.5 px-2.5 font-mono text-[11px] font-bold text-finblue-600">{s.rule_id}</td>
                    <td className="py-2.5 px-2.5 font-medium">{s.rule_name}</td>
                    <td className="py-2.5 px-2.5 font-mono text-[10px] text-slate-600 dark:text-slate-400">
                      <code>{s.fol_form}</code>
                    </td>
                    <td className="py-2.5 px-2.5 text-[11px] italic">{s.plain_english}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
