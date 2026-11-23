import React, { useState, useEffect } from "react";
import {
  GitCompare,
  TrendingUp,
  Cpu,
  RefreshCw,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ShieldCheck,
  Scale,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { fetchMLMetrics, retrainMLModels } from "../api/client";

export default function MLComparisonPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [error, setError] = useState(null);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetchMLMetrics();
      setData(res);
    } catch (err) {
      setError(err.message || "Failed to load ML metrics");
    } finally {
      setLoading(false);
    }
  };

  const handleRetrain = async () => {
    try {
      setRetraining(true);
      const res = await retrainMLModels();
      setData(res.results);
    } catch (err) {
      alert("Retraining failed: " + err.message);
    } finally {
      setRetraining(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500 animate-pulse">Loading ML model metrics and benchmark comparison...</div>;
  }

  if (error) {
    return (
      <div className="p-6 bg-rose-50 text-rose-800 rounded-xl border border-rose-300">
        <h3 className="font-bold">Error loading ML benchmark</h3>
        <p className="text-sm mt-1">{error}</p>
        <button onClick={loadMetrics} className="mt-3 px-3 py-1.5 bg-rose-600 text-white rounded text-xs">
          Retry
        </button>
      </div>
    );
  }

  const models = data?.models || {};
  const dtMetrics = models.decision_tree?.metrics || {};
  const lrMetrics = models.logistic_regression?.metrics || {};
  const ruleStdMetrics = models.rule_engine_standard?.metrics || {};
  const ruleStrictMetrics = models.rule_engine_strict?.metrics || {};

  const dtImportances = models.decision_tree?.feature_importances || [];
  const lrCoefficients = (models.logistic_regression?.coefficients || []).slice(0, 7);

  const agreement = data?.agreement || {};
  const overlap = agreement.overlap_breakdown || {};
  const edgeCases = data?.edge_case_divergences || [];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
            Comparative Benchmark • Held-Out Stratified Test Set
          </div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
            Production Rules vs. Machine Learning Models
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Comparing deterministic production rules with Decision Tree and Logistic Regression classifiers on independent ground truth.
          </p>
        </div>

        <button
          onClick={handleRetrain}
          disabled={retraining}
          className="flex items-center gap-1.5 px-4 py-2 bg-finblue-600 hover:bg-finblue-500 disabled:bg-slate-400 text-white text-xs font-semibold rounded-lg shadow-sm shadow-finblue-600/30 transition-all"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${retraining ? "animate-spin" : ""}`} />
          <span>{retraining ? "Generating & Retraining..." : "Retrain ML Models"}</span>
        </button>
      </div>

      {/* Synthetic Data Disclaimer Banner */}
      <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl text-xs text-amber-900 dark:text-amber-200 flex items-start gap-2.5">
        <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Independent Ground-Truth Notice:</span> The repayment label ("repaid") was generated via an independent probabilistic equation (logistic capacity model + stochastic shocks) rather than the rule engine output. <b>Synthetic-data accuracy does not represent real-world commercial lending performance.</b>
        </div>
      </div>

      {/* Model Performance Comparison Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Rule Engine Standard */}
        <div className="bg-white dark:bg-slate-900 border-2 border-finblue-500 rounded-xl p-4 shadow-sm relative overflow-hidden">
          <div className="text-[10px] uppercase font-bold tracking-wider text-finblue-600 dark:text-finblue-400 bg-finblue-50 dark:bg-finblue-950/60 inline-block px-2 py-0.5 rounded border border-finblue-200 dark:border-finblue-800">
            Expert System
          </div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 mt-2">
            Rule Engine (Standard)
          </h3>
          <div className="text-[11px] text-slate-400">Eligible + Conditional = Approve</div>

          <div className="mt-4 space-y-1.5 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-slate-500">Accuracy:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{ruleStdMetrics.accuracy}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Precision:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{ruleStdMetrics.precision}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Recall:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{ruleStdMetrics.recall}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">F1 Score:</span>
              <span className="font-bold text-emerald-600 dark:text-emerald-400">{ruleStdMetrics.f1_score}</span>
            </div>
          </div>
        </div>

        {/* Rule Engine Strict */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-[10px] uppercase font-bold tracking-wider text-slate-500 bg-slate-100 dark:bg-slate-800 inline-block px-2 py-0.5 rounded">
            Conservative
          </div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 mt-2">
            Rule Engine (Strict)
          </h3>
          <div className="text-[11px] text-slate-400">Only Prime Eligible = Approve</div>

          <div className="mt-4 space-y-1.5 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-slate-500">Accuracy:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{ruleStrictMetrics.accuracy}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Precision:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{ruleStrictMetrics.precision}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Recall:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{ruleStrictMetrics.recall}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">F1 Score:</span>
              <span className="font-bold text-slate-700 dark:text-slate-300">{ruleStrictMetrics.f1_score}</span>
            </div>
          </div>
        </div>

        {/* Decision Tree */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-[10px] uppercase font-bold tracking-wider text-purple-600 bg-purple-50 dark:bg-purple-950/40 inline-block px-2 py-0.5 rounded border border-purple-200 dark:border-purple-800">
            Interpretable ML
          </div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 mt-2">
            Decision Tree
          </h3>
          <div className="text-[11px] text-slate-400">Surrogate Tree (max_depth=4)</div>

          <div className="mt-4 space-y-1.5 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-slate-500">Accuracy:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{dtMetrics.accuracy}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Precision:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{dtMetrics.precision}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Recall:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{dtMetrics.recall}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">F1 / AUC:</span>
              <span className="font-bold text-purple-600 dark:text-purple-400">{dtMetrics.f1_score} / {dtMetrics.roc_auc}</span>
            </div>
          </div>
        </div>

        {/* Logistic Regression */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-[10px] uppercase font-bold tracking-wider text-amber-600 bg-amber-50 dark:bg-amber-950/40 inline-block px-2 py-0.5 rounded border border-amber-200 dark:border-amber-800">
            Parametric Linear
          </div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 mt-2">
            Logistic Regression
          </h3>
          <div className="text-[11px] text-slate-400">L2 Regularized + Scaled</div>

          <div className="mt-4 space-y-1.5 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-slate-500">Accuracy:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{lrMetrics.accuracy}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Precision:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{lrMetrics.precision}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Recall:</span>
              <span className="font-bold text-slate-900 dark:text-slate-100">{lrMetrics.recall}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">F1 / AUC:</span>
              <span className="font-bold text-amber-600 dark:text-amber-400">{lrMetrics.f1_score} / {lrMetrics.roc_auc}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Importance & Coefficients Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-2">
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
            Decision Tree Feature Importances (Gini Impurity Reduction)
          </h3>
          <p className="text-[11px] text-slate-500">Features driving tree split boundaries across the dataset.</p>

          <div className="h-60 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dtImportances} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
                <XAxis type="number" tick={{ fontSize: 10 }} />
                <YAxis dataKey="feature" type="category" tick={{ fontSize: 10 }} width={80} />
                <Tooltip
                  formatter={(val) => [`${(val * 100).toFixed(1)}%`, "Importance"]}
                  contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", borderColor: "#334155", color: "#f8fafc", fontSize: "11px" }}
                />
                <Bar dataKey="importance" fill="#8B5CF6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-2">
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
            Logistic Regression Standardized Coefficients
          </h3>
          <p className="text-[11px] text-slate-500">Relative directional impact on odds of full repayment.</p>

          <div className="h-60 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={lrCoefficients} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
                <XAxis type="number" tick={{ fontSize: 10 }} />
                <YAxis dataKey="feature" type="category" tick={{ fontSize: 10 }} width={80} />
                <Tooltip
                  formatter={(val) => [val, "Log-Odds Coef"]}
                  contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", borderColor: "#334155", color: "#f8fafc", fontSize: "11px" }}
                />
                <Bar dataKey="coefficient" radius={[0, 4, 4, 0]}>
                  {lrCoefficients.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.coefficient >= 0 ? "#10B981" : "#EF4444"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Model Agreement Breakdown */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Scale className="w-4 h-4 text-finblue-600" />
          Model Decision Agreement & Overlap (Rule Engine vs. Decision Tree)
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-3 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900 rounded-xl">
            <div className="text-[11px] text-emerald-700 dark:text-emerald-300 font-sans">Both Approved</div>
            <div className="text-xl font-bold text-emerald-800 dark:text-emerald-200 mt-1">
              {overlap.both_approve || 0}
            </div>
            <div className="text-[10px] text-emerald-600">Consensus Approvals</div>
          </div>

          <div className="p-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl">
            <div className="text-[11px] text-slate-600 dark:text-slate-300 font-sans">Both Declined</div>
            <div className="text-xl font-bold text-slate-800 dark:text-slate-100 mt-1">
              {overlap.both_reject || 0}
            </div>
            <div className="text-[10px] text-slate-500">Consensus Declines</div>
          </div>

          <div className="p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 rounded-xl">
            <div className="text-[11px] text-amber-700 dark:text-amber-300 font-sans">Rule Approved / ML Declined</div>
            <div className="text-xl font-bold text-amber-800 dark:text-amber-200 mt-1">
              {overlap.rule_approve_ml_reject || 0}
            </div>
            <div className="text-[10px] text-amber-600">Conditional Edge Divergences</div>
          </div>

          <div className="p-3 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 rounded-xl">
            <div className="text-[11px] text-rose-700 dark:text-rose-300 font-sans">Rule Declined / ML Approved</div>
            <div className="text-xl font-bold text-rose-800 dark:text-rose-200 mt-1">
              {overlap.rule_reject_ml_approve || 0}
            </div>
            <div className="text-[10px] text-rose-600">Statutory Knock-outs Enforced</div>
          </div>
        </div>

        <div className="text-xs text-slate-500 font-mono bg-slate-50 dark:bg-slate-850 p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 flex flex-wrap gap-4">
          <span>Overall Agreement: <b>{(agreement.agreement_rate_dt_rule * 100).toFixed(1)}%</b></span>
          <span>•</span>
          <span>Cohen's Kappa (&kappa;): <b>{agreement.cohen_kappa_dt_rule}</b> (Substantial inter-paradigm agreement)</span>
        </div>
      </div>

      {/* Edge Cases Divergence Analysis Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div>
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            Edge-Case Benchmark Suite & Divergence Root Causes
          </h3>
          <p className="text-[11px] text-slate-500">
            Running canonical edge cases through both systems exposes critical regulatory and boundary divergences.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-slate-600 dark:text-slate-400">
                <th className="py-2.5 px-3 font-semibold">Scenario</th>
                <th className="py-2.5 px-3 font-semibold">Rule Engine</th>
                <th className="py-2.5 px-3 font-semibold">Decision Tree</th>
                <th className="py-2.5 px-3 font-semibold">Logistic Reg.</th>
                <th className="py-2.5 px-3 font-semibold">Divergence Analysis</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
              {edgeCases.map((ec, idx) => (
                <tr key={idx} className={ec.diverges ? "bg-amber-50/20 dark:bg-amber-950/10" : ""}>
                  <td className="py-3 px-3 font-medium">
                    <div className="font-bold text-slate-900 dark:text-slate-100">{ec.name}</div>
                    <div className="text-[10px] font-mono text-slate-400">{ec.case_id}</div>
                  </td>
                  <td className="py-3 px-3 font-semibold">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-mono ${
                      ec.rule_decision === "ELIGIBLE" ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300" :
                      ec.rule_decision === "CONDITIONALLY_ELIGIBLE" ? "bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300" :
                      "bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300"
                    }`}>
                      {ec.rule_decision}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-medium">
                    <span className={ec.decision_tree_pred === "Approve" ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"}>
                      {ec.decision_tree_pred}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-medium">
                    <span className={ec.logistic_regression_pred === "Approve" ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"}>
                      {ec.logistic_regression_pred}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-[11px] leading-relaxed">
                    {ec.divergence_reason}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
