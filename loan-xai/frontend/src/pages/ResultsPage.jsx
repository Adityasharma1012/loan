import React, { useEffect, useState } from "react";
import {
  FileCheck,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  IndianRupee,
  Layers,
  FileText,
  GitCompare,
  ArrowRight,
  ShieldCheck,
  Clock,
  Sparkles,
  Download,
} from "lucide-react";
import DecisionBadge from "../components/DecisionBadge";
import CounterfactualCard from "../components/CounterfactualCard";
import { fetchApplicationDetail, getPDFExportUrl } from "../api/client";

export default function ResultsPage({
  latestEvaluation,
  selectedAppId,
  setCurrentPage,
  setSelectedAppId,
}) {
  const [data, setData] = useState(latestEvaluation || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (latestEvaluation) {
      setData(latestEvaluation);
    } else if (selectedAppId) {
      setLoading(true);
      fetchApplicationDetail(selectedAppId)
        .then((res) => {
          // Format response into evaluation-like structure
          const dec = res.decision;
          setData({
            application_id: res.application.id,
            decision: dec.decision_status,
            risk_class: dec.risk_class,
            interest_rate: dec.interest_rate,
            interest_rate_percent: dec.interest_rate_percent,
            interest_rate_band: dec.interest_rate_band,
            suggested_tenure_months: dec.suggested_tenure_months,
            requested_amount: res.application.requested_amount,
            recommended_amount: dec.recommended_amount,
            max_affordable_emi: dec.max_affordable_emi,
            requested_emi: dec.requested_emi,
            recommended_emi: dec.recommended_emi,
            supportable_principal: dec.supportable_principal,
            exceeds_affordability: dec.exceeds_affordability,
            haircut_applied: dec.haircut_applied,
            conditions: dec.conditions,
            rejection_reasons: dec.rejection_reasons,
            positive_factors: dec.positive_factors,
            risk_factors: dec.risk_factors,
            counterfactual_hints: dec.counterfactual_hints,
            rationale_summary: dec.rationale_summary,
            execution_trace: res.execution_trace,
            proof_trees: dec.proof_trees,
            threshold_version: dec.threshold_version,
            input_warnings: res.application.input_warnings,
            ml_comparison: res.ml_comparison,
          });
        })
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [latestEvaluation, selectedAppId]);

  if (loading) {
    return (
      <div className="p-12 text-center text-slate-500 animate-pulse">
        Loading evaluation results...
      </div>
    );
  }

  if (!data) {
    return (
      <div className="p-10 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-xl mx-auto space-y-4">
        <FileCheck className="w-12 h-12 text-slate-400 mx-auto" />
        <h3 className="font-bold text-base text-slate-900 dark:text-slate-100">
          No Active Decision Loaded
        </h3>
        <p className="text-xs text-slate-500">
          Please submit a new loan application or select an existing record from the dashboard.
        </p>
        <button
          onClick={() => setCurrentPage("new-application")}
          className="px-4 py-2 bg-finblue-600 text-white rounded-lg text-xs font-semibold"
        >
          Evaluate New Application
        </button>
      </div>
    );
  }

  const isApproved = data.decision === "ELIGIBLE";
  const isConditional = data.decision === "CONDITIONALLY_ELIGIBLE";
  const isDeclined = data.decision === "NOT_ELIGIBLE";

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Top Verdict Card */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
              Application ID: {data.application_id} • Policy v{data.threshold_version}
            </div>
            <div className="flex items-center gap-3 mt-1.5">
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
                Underwriting Decision
              </h2>
              <DecisionBadge status={data.decision} size="md" />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <a
              href={getPDFExportUrl(data.application_id)}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-semibold rounded-lg transition-colors border border-slate-200 dark:border-slate-700"
            >
              <Download className="w-3.5 h-3.5" />
              Download PDF Memo
            </a>
            <button
              onClick={() => {
                setSelectedAppId(data.application_id);
                setCurrentPage("explanation");
              }}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-finblue-600 hover:bg-finblue-500 text-white text-xs font-semibold rounded-lg shadow-sm shadow-finblue-600/30 transition-all"
            >
              <Layers className="w-3.5 h-3.5" />
              View FOL Trace
            </button>
          </div>
        </div>

        {/* Input Warnings Alert */}
        {data.input_warnings && data.input_warnings.length > 0 && (
          <div className="p-3.5 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800 rounded-xl text-xs text-amber-900 dark:text-amber-200 space-y-1">
            <div className="font-bold flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              Flagged Input Notice (Unusual-but-Valid Parameters):
            </div>
            {data.input_warnings.map((w, idx) => (
              <div key={idx} className="ml-5 text-[11px]">• {w}</div>
            ))}
          </div>
        )}

        {/* Financial Sizing Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-slate-50 dark:bg-slate-850 p-5 rounded-xl border border-slate-200 dark:border-slate-800">
          <div>
            <div className="text-[11px] text-slate-500">Recommended Principal</div>
            <div className="text-xl font-extrabold text-slate-900 dark:text-slate-100">
              {data.recommended_amount > 0 ? `₹${data.recommended_amount.toLocaleString()}` : "₹0"}
            </div>
            <div className="text-[10px] text-slate-400">
              Requested: ₹{data.requested_amount?.toLocaleString()}
            </div>
          </div>

          <div>
            <div className="text-[11px] text-slate-500">Interest Rate Band</div>
            <div className="text-xl font-extrabold text-finblue-600 dark:text-finblue-400">
              {data.interest_rate_percent}%
            </div>
            <div className="text-[10px] text-slate-400">{data.interest_rate_band}</div>
          </div>

          <div>
            <div className="text-[11px] text-slate-500">Recommended EMI</div>
            <div className="text-xl font-extrabold text-slate-900 dark:text-slate-100">
              ₹{data.recommended_emi ? data.recommended_emi.toLocaleString(undefined, { maximumFractionDigits: 0 }) : 0}
            </div>
            <div className="text-[10px] text-slate-400">
              Max Permissible: ₹{data.max_affordable_emi?.toLocaleString(undefined, { maximumFractionDigits: 0 })}
            </div>
          </div>

          <div>
            <div className="text-[11px] text-slate-500">Suggested Tenure</div>
            <div className="text-xl font-extrabold text-slate-900 dark:text-slate-100">
              {data.suggested_tenure_months} Mo.
            </div>
            <div className="text-[10px] text-slate-400">Risk Class: {data.risk_class}</div>
          </div>
        </div>

        {/* Affordability Exceeded Alert */}
        {data.exceeds_affordability && (
          <div className="p-3.5 bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 rounded-xl text-xs text-blue-900 dark:text-blue-200 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">Affordability Sizing Adjustment:</span> The requested loan amount (₹{data.requested_amount?.toLocaleString()}) exceeds the maximum supportable debt capacity (₹{data.supportable_principal?.toLocaleString()}) based on 40% DTI disposable cashflow. The engine approved a downsized principal of <b>₹{data.recommended_amount?.toLocaleString()}</b>.
            </div>
          </div>
        )}

        {/* Plain English Rationale */}
        <div className="space-y-1.5">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Decision Rationale Summary
          </h4>
          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed bg-white dark:bg-slate-950 p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 font-medium">
            {data.rationale_summary}
          </p>
        </div>

        {/* Adverse Action Reasons or Conditional Stipulations */}
        {data.rejection_reasons && data.rejection_reasons.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
              <XCircle className="w-4 h-4" />
              Adverse Action Notice (Statutory Declination Reasons)
            </h4>
            <div className="bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl p-3.5 space-y-1 text-xs text-rose-800 dark:text-rose-300">
              {data.rejection_reasons.map((r, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="font-bold">•</span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {data.conditions && data.conditions.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" />
              Conditional Underwriting Stipulations & Covenants
            </h4>
            <div className="bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50 rounded-xl p-3.5 space-y-1 text-xs text-amber-800 dark:text-amber-300">
              {data.conditions.map((c, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="font-bold">•</span>
                  <span>{c}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Counterfactual Explainability Section */}
      {data.counterfactual_hints && data.counterfactual_hints.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-finblue-600" />
              Counterfactual Recommendations (Pathways to Approval / Better Terms)
            </h3>
            <span className="text-[11px] text-slate-400">Minimum parametric adjustments derived from threshold boundaries</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.counterfactual_hints.map((hint, idx) => (
              <CounterfactualCard key={idx} hint={hint} />
            ))}
          </div>
        </div>
      )}

      {/* Machine Learning Comparison Snippet */}
      {data.ml_comparison && (
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                <GitCompare className="w-4 h-4 text-purple-600" />
                Cross-Paradigm Machine Learning Comparison
              </h3>
              <p className="text-[11px] text-slate-500">
                How independent statistical ML models scored the exact same applicant features.
              </p>
            </div>
            <button
              onClick={() => setCurrentPage("ml-comparison")}
              className="text-xs font-semibold text-finblue-600 dark:text-finblue-400 hover:underline flex items-center gap-1"
            >
              Full ML Benchmark <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="p-3.5 rounded-xl border border-finblue-200 dark:border-finblue-900 bg-finblue-50/40 dark:bg-finblue-950/20">
              <div className="text-[11px] font-semibold text-finblue-700 dark:text-finblue-300">Expert Rule Engine</div>
              <div className="text-base font-extrabold text-slate-900 dark:text-slate-100 mt-1">
                {data.decision.replace(/_/g, " ")}
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">Deterministic FOL logic</div>
            </div>

            <div className="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850">
              <div className="text-[11px] font-semibold text-slate-600 dark:text-slate-400">Decision Tree (depth=4)</div>
              <div className="text-base font-extrabold text-slate-900 dark:text-slate-100 mt-1">
                {data.ml_comparison.decision_tree?.prediction}
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">
                Repayment Prob: {(data.ml_comparison.decision_tree?.repayment_probability * 100).toFixed(1)}%
              </div>
            </div>

            <div className="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850">
              <div className="text-[11px] font-semibold text-slate-600 dark:text-slate-400">Logistic Regression</div>
              <div className="text-base font-extrabold text-slate-900 dark:text-slate-100 mt-1">
                {data.ml_comparison.logistic_regression?.prediction}
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">
                Repayment Prob: {(data.ml_comparison.logistic_regression?.repayment_probability * 100).toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
