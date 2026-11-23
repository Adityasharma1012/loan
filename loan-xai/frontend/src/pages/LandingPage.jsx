import React from "react";
import {
  ShieldCheck,
  Cpu,
  GitCompare,
  Scale,
  FilePlus2,
  LayoutDashboard,
  CheckCircle2,
  ArrowRight,
  BookOpen,
  Binary,
  Layers,
  FileCheck,
} from "lucide-react";

export default function LandingPage({ setCurrentPage }) {
  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-navy-900 via-navy-800 to-finblue-700 text-white rounded-2xl p-8 sm:p-10 shadow-xl border border-slate-700/50 relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 bg-finblue-500/20 text-finblue-300 border border-finblue-400/30 px-3 py-1 rounded-full text-xs font-mono font-medium">
            <Binary className="w-3.5 h-3.5" />
            Artificial Intelligence Foundations • Academic Demonstration
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white leading-tight">
            Explainable Rule-Based Loan Eligibility & Credit Decision System
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            An institutional-grade expert system evaluating retail credit applications using <b>production rules</b>,{" "}
            <b>first-order predicate logic (FOL)</b>, and <b>forward-chaining deduction</b>. Benchmarked head-to-head
            against machine learning classifiers for transparency, regulatory defensibility, edge-case safety, and algorithmic fairness.
          </p>

          <div className="flex flex-wrap gap-3 pt-4">
            <button
              onClick={() => setCurrentPage("new-application")}
              className="flex items-center gap-2 bg-finblue-600 hover:bg-finblue-500 text-white px-5 py-2.5 rounded-xl font-semibold text-sm shadow-lg shadow-finblue-600/30 transition-all hover:scale-[1.02]"
            >
              <FilePlus2 className="w-4 h-4" />
              Evaluate New Application
            </button>
            <button
              onClick={() => setCurrentPage("dashboard")}
              className="flex items-center gap-2 bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border border-slate-600/60 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all"
            >
              <LayoutDashboard className="w-4 h-4" />
              Executive Dashboard
            </button>
            <button
              onClick={() => setCurrentPage("fairness")}
              className="flex items-center gap-2 bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border border-slate-600/60 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all"
            >
              <Scale className="w-4 h-4" />
              Fairness & Bias Audit
            </button>
          </div>
        </div>

        {/* Decorative background watermark */}
        <div className="absolute right-[-40px] bottom-[-40px] text-white/5 pointer-events-none select-none">
          <Cpu className="w-96 h-96" />
        </div>
      </div>

      {/* Core Architectural Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-finblue-50 dark:bg-finblue-950/60 text-finblue-600 dark:text-finblue-400 flex items-center justify-center">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-slate-100">
            1. Forward-Chaining Production Rules
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Declarative rules in YAML executed to a fixpoint with strict conflict resolution: 
            hard knock-outs first, priority salience, condition specificity, and deterministic tie-breaking with refraction.
          </p>
          <div className="pt-2">
            <button
              onClick={() => setCurrentPage("about")}
              className="text-xs font-semibold text-finblue-600 dark:text-finblue-400 hover:underline flex items-center gap-1"
            >
              View Rules Catalogue <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 flex items-center justify-center">
            <Binary className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-slate-100">
            2. First-Order Logic Proof Trees
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Horn clauses over ground atoms with substitution, unification, and negation-as-failure. 
            Every decision generates a full derivation proof tree for 100% regulatory contestability.
          </p>
          <div className="pt-2">
            <button
              onClick={() => setCurrentPage("explanation")}
              className="text-xs font-semibold text-purple-600 dark:text-purple-400 hover:underline flex items-center gap-1"
            >
              Explore Inference Engine <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <GitCompare className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-slate-900 dark:text-slate-100">
            3. ML Comparison & Fairness Audit
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Benchmarked against Decision Tree and Logistic Regression models trained on independent synthetic repayment data.
            Audited for disparate impact (EEOC 80% rule), statistical parity, and demographic proxy risks.
          </p>
          <div className="pt-2">
            <button
              onClick={() => setCurrentPage("ml-comparison")}
              className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1"
            >
              Inspect Benchmarks <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Feature Highlights Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
          Paradigm Comparison: Production Rules vs. Machine Learning
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850">
                <th className="py-2.5 px-3 font-semibold text-slate-700 dark:text-slate-300">Criterion</th>
                <th className="py-2.5 px-3 font-semibold text-finblue-600 dark:text-finblue-400">Expert Rule Engine (LoanXAI)</th>
                <th className="py-2.5 px-3 font-semibold text-slate-700 dark:text-slate-300">Statistical ML Classifier</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-600 dark:text-slate-400">
              <tr>
                <td className="py-2.5 px-3 font-medium text-slate-900 dark:text-slate-200">Decision Rationale</td>
                <td className="py-2.5 px-3 text-emerald-700 dark:text-emerald-400 font-medium">Exact FOL Horn deduction path + ground atoms</td>
                <td className="py-2.5 px-3">Surrogate weights or axis-aligned splits</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-medium text-slate-900 dark:text-slate-200">Statutory Knock-outs</td>
                <td className="py-2.5 px-3 text-emerald-700 dark:text-emerald-400 font-medium">Deterministic legal floors (e.g. Age &lt; 18) guaranteed</td>
                <td className="py-2.5 px-3">Can smooth over knockouts if other features compensate</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-medium text-slate-900 dark:text-slate-200">Adverse Action Notices</td>
                <td className="py-2.5 px-3 text-emerald-700 dark:text-emerald-400 font-medium">Directly mapped to breached underwriting policies</td>
                <td className="py-2.5 px-3">Approximated via SHAP/LIME with instability risk</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-medium text-slate-900 dark:text-slate-200">Auditability & Trace</td>
                <td className="py-2.5 px-3 text-emerald-700 dark:text-emerald-400 font-medium">100% reproducible step-by-step conflict history</td>
                <td className="py-2.5 px-3">Score changes with training sample distribution shifts</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-medium text-slate-900 dark:text-slate-200">Counterfactual Explanations</td>
                <td className="py-2.5 px-3 text-emerald-700 dark:text-emerald-400 font-medium">Deterministic delta bounds to reach eligibility</td>
                <td className="py-2.5 px-3">Gradient optimization over high-dimensional manifold</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
