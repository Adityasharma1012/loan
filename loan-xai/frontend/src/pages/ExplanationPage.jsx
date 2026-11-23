import React, { useState, useEffect } from "react";
import {
  Cpu,
  Layers,
  Binary,
  CheckCircle2,
  XCircle,
  Sliders,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  RefreshCw,
} from "lucide-react";
import ProofTreeView from "../components/ProofTreeView";
import ExecutionTimeline from "../components/ExecutionTimeline";
import CounterfactualCard from "../components/CounterfactualCard";
import { evaluateApplication, fetchApplicationDetail } from "../api/client";

export default function ExplanationPage({ latestEvaluation, selectedAppId }) {
  const [data, setData] = useState(latestEvaluation || null);
  const [loading, setLoading] = useState(false);

  // Counterfactual Interactive Simulator State
  const [simIncome, setSimIncome] = useState(data?.monthly_income || 45000);
  const [simDebt, setSimDebt] = useState(data?.existing_monthly_debt || 12000);
  const [simScore, setSimScore] = useState(data?.credit_score || 720);
  const [simResult, setSimResult] = useState(null);
  const [simLoading, setSimLoading] = useState(false);

  useEffect(() => {
    if (latestEvaluation) {
      setData(latestEvaluation);
    } else if (selectedAppId) {
      setLoading(true);
      fetchApplicationDetail(selectedAppId)
        .then((res) => {
          const dec = res.decision;
          setData({
            application_id: res.application.id,
            monthly_income: res.application.monthly_income,
            existing_monthly_debt: res.application.existing_monthly_debt,
            credit_score: res.application.credit_score,
            decision: dec.decision_status,
            risk_class: dec.risk_class,
            execution_trace: res.execution_trace,
            proof_trees: dec.proof_trees,
            counterfactual_hints: dec.counterfactual_hints,
            positive_factors: dec.positive_factors,
            risk_factors: dec.risk_factors,
          });
          setSimIncome(res.application.monthly_income);
          setSimDebt(res.application.existing_monthly_debt);
          setSimScore(res.application.credit_score);
        })
        .finally(() => setLoading(false));
    }
  }, [latestEvaluation, selectedAppId]);

  const runSimulation = async () => {
    try {
      setSimLoading(true);
      const res = await evaluateApplication({
        age: 32,
        monthly_income: Number(simIncome),
        existing_monthly_debt: Number(simDebt),
        credit_score: Number(simScore),
        employment_years: 3.5,
        repayment_history: "Good",
        recent_default: false,
        requested_amount: 250000,
        requested_tenure_months: 36,
      });
      setSimResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setSimLoading(false);
    }
  };

  if (loading) {
    return <div className="p-12 text-center text-slate-500 animate-pulse">Loading inference trace...</div>;
  }

  if (!data) {
    return (
      <div className="p-10 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-xl mx-auto space-y-4">
        <Cpu className="w-12 h-12 text-slate-400 mx-auto" />
        <h3 className="font-bold text-base text-slate-900 dark:text-slate-100">
          No Inference Trace Available
        </h3>
        <p className="text-xs text-slate-500">
          Please evaluate an application first to inspect its First-Order Logic proof trees and forward chaining step history.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
          Auditing Application: {data.application_id}
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
          Rule Engine Explainability & Proof Trees
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Deterministic formal logic proofs, step-by-step firing history with conflict resolution, and counterfactual sensitivity simulator.
        </p>
      </div>

      {/* Positive Indicators & Risk Factors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm space-y-2">
          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            Positive Credit Indicators ({data.positive_factors?.length || 0})
          </h4>
          <div className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
            {data.positive_factors && data.positive_factors.length > 0 ? (
              data.positive_factors.map((p, idx) => (
                <div key={idx} className="flex items-start gap-2 bg-emerald-50/50 dark:bg-emerald-950/20 p-2 rounded-lg border border-emerald-100 dark:border-emerald-900/40">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>{p}</span>
                </div>
              ))
            ) : (
              <div className="text-slate-400 italic">No strong prime positive indicators flagged.</div>
            )}
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm space-y-2">
          <h4 className="text-xs font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
            <XCircle className="w-4 h-4" />
            Underwriting Risk Factors ({data.risk_factors?.length || 0})
          </h4>
          <div className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
            {data.risk_factors && data.risk_factors.length > 0 ? (
              data.risk_factors.map((r, idx) => (
                <div key={idx} className="flex items-start gap-2 bg-rose-50/50 dark:bg-rose-950/20 p-2 rounded-lg border border-rose-100 dark:border-rose-900/40">
                  <span className="text-rose-600 font-bold">•</span>
                  <span>{r}</span>
                </div>
              ))
            ) : (
              <div className="text-emerald-600 italic">Zero adverse underwriting risk factors detected.</div>
            )}
          </div>
        </div>
      </div>

      {/* Interactive Counterfactual Simulator */}
      <div className="bg-gradient-to-r from-slate-900 to-navy-950 text-white rounded-2xl p-6 shadow-md border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Sliders className="w-4 h-4 text-finblue-400" />
              Interactive Counterfactual Simulator
            </h3>
            <p className="text-[11px] text-slate-400">
              Adjust parameters below to simulate counterfactual outcomes live through the rule engine.
            </p>
          </div>

          <button
            onClick={runSimulation}
            disabled={simLoading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-finblue-600 hover:bg-finblue-500 text-white rounded-lg text-xs font-semibold shadow transition-all disabled:opacity-50"
          >
            {simLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
            Simulate Verdict
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono">
          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-700">
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Monthly Income:</span>
              <span className="font-bold text-finblue-400">₹{Number(simIncome).toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="15000"
              max="150000"
              step="5000"
              value={simIncome}
              onChange={(e) => setSimIncome(e.target.value)}
              className="w-full accent-finblue-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500">
              <span>₹15k</span>
              <span>Threshold: ₹30k</span>
              <span>₹150k</span>
            </div>
          </div>

          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-700">
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Existing Debt:</span>
              <span className="font-bold text-amber-400">₹{Number(simDebt).toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="0"
              max="60000"
              step="2000"
              value={simDebt}
              onChange={(e) => setSimDebt(e.target.value)}
              className="w-full accent-amber-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500">
              <span>₹0</span>
              <span>DTI: {simIncome > 0 ? ((simDebt / simIncome) * 100).toFixed(1) : 0}%</span>
              <span>₹60k</span>
            </div>
          </div>

          <div className="bg-slate-800/60 p-3 rounded-xl border border-slate-700">
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Credit Score:</span>
              <span className="font-bold text-emerald-400">{simScore}</span>
            </div>
            <input
              type="range"
              min="500"
              max="850"
              step="10"
              value={simScore}
              onChange={(e) => setSimScore(e.target.value)}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500">
              <span>Floor: 550</span>
              <span>Prime: 750</span>
              <span>850</span>
            </div>
          </div>
        </div>

        {simResult && (
          <div className="p-3 bg-slate-800/90 rounded-xl border border-slate-700 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <span className="text-slate-400">Simulated Verdict:</span>
              <span className={`font-bold px-2.5 py-0.5 rounded text-xs ${
                simResult.decision === "ELIGIBLE" ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40" :
                simResult.decision === "CONDITIONALLY_ELIGIBLE" ? "bg-amber-500/20 text-amber-300 border border-amber-500/40" :
                "bg-rose-500/20 text-rose-300 border border-rose-500/40"
              }`}>
                {simResult.decision}
              </span>
              <span className="text-slate-400">• Risk: <b>{simResult.risk_class}</b></span>
            </div>

            <div className="text-slate-300">
              Recommended: <b>₹{simResult.recommended_amount?.toLocaleString()}</b> @ {simResult.interest_rate_percent}%
            </div>
          </div>
        )}
      </div>

      {/* First-Order Logic Proof Trees Component */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
        <ProofTreeView trees={data.proof_trees} />
      </div>

      {/* Step-by-Step Execution Timeline Component */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
        <ExecutionTimeline trace={data.execution_trace} />
      </div>
    </div>
  );
}
