import React, { useState, useEffect } from "react";
import {
  Scale,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ShieldAlert,
  FileCheck,
  TrendingDown,
  Layers,
  Info,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Cell,
} from "recharts";
import { fetchFairnessReport } from "../api/client";

export default function FairnessPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Selected audit views
  const [selectedSystem, setSelectedSystem] = useState("Rule Engine (Standard)");
  const [selectedAttribute, setSelectedAttribute] = useState("gender");

  useEffect(() => {
    fetchFairnessReport()
      .then((res) => setData(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500 animate-pulse">Running algorithmic fairness & bias audit...</div>;
  }

  if (error || !data) {
    return (
      <div className="p-6 bg-rose-50 text-rose-800 rounded-xl border border-rose-300">
        <h3 className="font-bold">Error loading fairness audit</h3>
        <p className="text-sm mt-1">{error}</p>
      </div>
    );
  }

  const systemAudit = data.systems_audit?.[selectedSystem] || {};
  const currentAttrData = systemAudit[selectedAttribute] || { subgroups: [] };
  const subgroups = currentAttrData.subgroups || [];

  const chartData = subgroups.map((g) => ({
    name: g.group_name,
    dir: g.disparate_impact_ratio,
    approval_rate: g.approval_rate_percent,
    is_privileged: g.is_privileged,
    violation: g.four_fifths_violation,
    small_sample: g.small_sample_warning,
  }));

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
          Algorithmic Fairness • Equal Opportunity & Disparate Impact
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
          Fairness, Demographic Parity & Bias Audit
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Independent group-level audit auditing Disparate Impact (EEOC 80% rule), False Positive/Negative rates, and proxy feature leakage.
        </p>
      </div>

      {/* System & Demographic Selectors */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        {/* System Tabs */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-xs font-semibold text-slate-500 mr-2">Audit System:</span>
          {Object.keys(data.systems_audit || {}).map((sys) => (
            <button
              key={sys}
              onClick={() => setSelectedSystem(sys)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selectedSystem === sys
                  ? "bg-finblue-600 text-white shadow-sm"
                  : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200"
              }`}
            >
              {sys}
            </button>
          ))}
        </div>

        {/* Demographic Tabs */}
        <div className="flex items-center gap-1.5">
          <span className="text-xs font-semibold text-slate-500 mr-2">Protected Attribute:</span>
          {[
            { id: "gender", label: "Gender" },
            { id: "region_type", label: "Region" },
            { id: "age_band", label: "Age Bracket" },
          ].map((attr) => (
            <button
              key={attr.id}
              onClick={() => setSelectedAttribute(attr.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selectedAttribute === attr.id
                  ? "bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 shadow-sm"
                  : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200"
              }`}
            >
              {attr.label}
            </button>
          ))}
        </div>
      </div>

      {/* Disparate Impact Ratio Chart */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
          <div>
            <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <Scale className="w-4 h-4 text-finblue-600" />
              Disparate Impact Ratio (DIR) vs. EEOC 80% Benchmark
            </h3>
            <p className="text-[11px] text-slate-500">
              Ratio of group approval rate to privileged reference (<b>{currentAttrData.privileged_reference}</b> = 1.0). Ratios below 0.80 indicate potential adverse impact.
            </p>
          </div>
          <span className="text-xs font-mono bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-slate-600 dark:text-slate-300">
            Four-Fifths Rule Threshold = 0.80
          </span>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 1.2]} tick={{ fontSize: 11 }} />
              <Tooltip
                formatter={(val, name, props) => [
                  `${val.toFixed(2)} (Approval Rate: ${props.payload.approval_rate}%)`,
                  "Disparate Impact Ratio",
                ]}
                contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", borderColor: "#334155", color: "#f8fafc", fontSize: "11px" }}
              />
              <ReferenceLine y={0.80} stroke="#EF4444" strokeDasharray="4 4" label={{ value: "EEOC 0.80 Threshold", fill: "#EF4444", fontSize: 10, position: "top" }} />
              <ReferenceLine y={1.00} stroke="#94A3B8" strokeDasharray="2 2" />
              <Bar dataKey="dir" radius={[6, 6, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.is_privileged ? "#2563EB" : entry.violation ? "#EF4444" : "#10B981"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Subgroups Metric Audit Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
          Subgroup Fairness Metrics ({selectedSystem})
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse font-mono">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-slate-600 dark:text-slate-400 font-sans">
                <th className="py-2.5 px-3 font-semibold">Subgroup</th>
                <th className="py-2.5 px-3 font-semibold">Sample (n)</th>
                <th className="py-2.5 px-3 font-semibold">Approval Rate</th>
                <th className="py-2.5 px-3 font-semibold">DIR (Ratio)</th>
                <th className="py-2.5 px-3 font-semibold">SPD (Diff)</th>
                <th className="py-2.5 px-3 font-semibold">TPR (Recall)</th>
                <th className="py-2.5 px-3 font-semibold">FPR (Error)</th>
                <th className="py-2.5 px-3 font-semibold">Four-Fifths Flag</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
              {subgroups.map((grp, idx) => (
                <tr key={idx} className={grp.four_fifths_violation ? "bg-rose-50/20 dark:bg-rose-950/10" : ""}>
                  <td className="py-3 px-3 font-sans font-bold">
                    <span className="flex items-center gap-1.5">
                      {grp.group_name}
                      {grp.is_privileged && (
                        <span className="text-[10px] font-mono text-finblue-600 bg-finblue-50 dark:bg-finblue-950/60 px-1.5 py-0.2 rounded border border-finblue-200 dark:border-finblue-800 font-normal">
                          Ref
                        </span>
                      )}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    {grp.sample_size} ({grp.sample_share_percent}%)
                    {grp.small_sample_warning && (
                      <span className="block text-[10px] text-amber-500 font-sans font-medium">Caveat: n &lt; 30</span>
                    )}
                  </td>
                  <td className="py-3 px-3 font-bold">{grp.approval_rate_percent}%</td>
                  <td className="py-3 px-3">
                    <span className={grp.four_fifths_violation ? "text-rose-600 font-bold" : "text-slate-700 dark:text-slate-300"}>
                      {grp.disparate_impact_ratio.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3 px-3">{grp.statistical_parity_difference > 0 ? `+${grp.statistical_parity_difference.toFixed(2)}` : grp.statistical_parity_difference.toFixed(2)}</td>
                  <td className="py-3 px-3">{(grp.true_positive_rate * 100).toFixed(1)}%</td>
                  <td className="py-3 px-3">{(grp.false_positive_rate * 100).toFixed(1)}%</td>
                  <td className="py-3 px-3 font-sans">
                    {grp.four_fifths_violation ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-700 bg-rose-50 dark:bg-rose-950/40 border border-rose-300 dark:border-rose-800 px-2 py-0.5 rounded-full">
                        <AlertTriangle className="w-3 h-3 text-rose-600" /> Breached (&lt;0.80)
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 px-2 py-0.5 rounded-full">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Compliant
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Proxy Discrimination Leakage Findings */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-500" />
            Proxy Discrimination & Feature Leakage Analysis
          </h3>
          <p className="text-[11px] text-slate-500">
            Even when protected attributes are quarantined from underwriting, correlation with neutral financial variables can introduce proxy bias.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.proxy_findings?.map((p, idx) => (
            <div key={idx} className="bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono font-bold text-slate-700 dark:text-slate-300">
                  {p.proxy_feature.toUpperCase()} &rarr; {p.demographic_target.toUpperCase()}
                </span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800">
                  {p.proxy_risk_level} RISK
                </span>
              </div>
              <div className="text-xs font-semibold text-slate-900 dark:text-slate-100">{p.observation}</div>
              <div className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed italic">
                "{p.risk_mechanism}"
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Automated Narrative Findings & Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
            Automated Audit Findings
          </h3>
          <div className="space-y-2 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
            {data.narrative_findings?.map((f, idx) => (
              <div key={idx} className="p-3 bg-slate-50 dark:bg-slate-850 rounded-lg border border-slate-200 dark:border-slate-800">
                • {f}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
            Remediation & Governance Guidance
          </h3>
          <div className="space-y-2 text-xs">
            {data.recommendations?.map((r, idx) => (
              <div key={idx} className="p-3 bg-slate-50 dark:bg-slate-850 rounded-lg border border-slate-200 dark:border-slate-800 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 dark:text-slate-100">{r.title}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-finblue-50 text-finblue-700 dark:bg-finblue-950/40 dark:text-finblue-300 border border-finblue-200">
                    {r.priority}
                  </span>
                </div>
                <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">{r.action}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Methodology Limitations Card */}
      <div className="p-5 bg-slate-100 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-2 text-xs text-slate-600 dark:text-slate-400">
        <div className="font-bold text-slate-800 dark:text-slate-200 flex items-center gap-2">
          <Info className="w-4 h-4 text-finblue-600" />
          Methodological Constraints & Legal Caveats
        </div>
        <ul className="list-disc pl-5 space-y-1 text-[11px]">
          {data.methodology_limitations?.map((lim, idx) => (
            <li key={idx}>{lim}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
