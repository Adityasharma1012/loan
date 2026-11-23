import React, { useEffect, useState } from "react";
import {
  Users,
  CheckCircle,
  AlertTriangle,
  XCircle,
  IndianRupee,
  TrendingUp,
  FileText,
  ArrowRight,
  RefreshCw,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { fetchDashboardStats } from "../api/client";
import DecisionBadge from "../components/DecisionBadge";

export default function DashboardPage({ setCurrentPage, setSelectedAppId }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchDashboardStats();
      setStats(data);
    } catch (err) {
      setError(err.message || "Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 max-w-6xl mx-auto animate-pulse">
        <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-28 bg-slate-200 dark:bg-slate-800 rounded-xl"></div>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-72 bg-slate-200 dark:bg-slate-800 rounded-xl"></div>
          <div className="h-72 bg-slate-200 dark:bg-slate-800 rounded-xl"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-rose-50 dark:bg-rose-950/40 text-rose-800 dark:text-rose-200 rounded-xl border border-rose-300 dark:border-rose-800">
        <h3 className="font-bold">Error loading dashboard</h3>
        <p className="text-sm mt-1">{error}</p>
        <button
          onClick={loadData}
          className="mt-3 px-3 py-1.5 bg-rose-600 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Retry
        </button>
      </div>
    );
  }

  const decisionData = stats?.decision_distribution || [];
  const riskData = stats?.risk_distribution || [];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
            Executive Underwriting Dashboard
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Real-time portfolio metrics evaluated strictly through the production rule engine.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 text-xs font-medium flex items-center gap-1.5"
            title="Refresh metrics"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
          <button
            onClick={() => setCurrentPage("new-application")}
            className="px-4 py-2 bg-finblue-600 hover:bg-finblue-500 text-white text-xs font-semibold rounded-lg shadow-sm shadow-finblue-600/30"
          >
            + New Application
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-medium">Total Evaluated</span>
            <Users className="w-4 h-4 text-finblue-600" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            {stats?.total_applications?.toLocaleString() || 0}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">Underwritten via forward chaining</div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-medium">Overall Approval Rate</span>
            <CheckCircle className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            {stats?.approval_rate_percent || 0}%
          </div>
          <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-1 flex items-center gap-1">
            <span>Eligible ({stats?.eligible_count}) + Conditional ({stats?.conditional_count})</span>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-medium">Avg. Requested Loan</span>
            <IndianRupee className="w-4 h-4 text-slate-500" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            ₹{stats?.average_requested_amount ? stats.average_requested_amount.toLocaleString(undefined, { maximumFractionDigits: 0 }) : 0}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">Borrower demand ticket</div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-medium">Avg. Recommended Sizing</span>
            <TrendingUp className="w-4 h-4 text-finblue-600" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            ₹{stats?.average_recommended_amount ? stats.average_recommended_amount.toLocaleString(undefined, { maximumFractionDigits: 0 }) : 0}
          </div>
          <div className="text-[11px] text-finblue-600 dark:text-finblue-400 mt-1">Affordability & annuity-capped</div>
        </div>
      </div>

      {/* Visual Charts: Decision Distribution & Risk Tier Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Decision Breakdown Doughnut Chart */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div className="mb-2">
            <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
              Underwriting Verdict Breakdown
            </h3>
            <p className="text-[11px] text-slate-500">Classification distribution across eligible, conditional, and decline tiers.</p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={decisionData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={4}
                >
                  {decisionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val, name) => [`${val} applications`, name]}
                  contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", borderColor: "#334155", color: "#f8fafc", fontSize: "12px" }}
                />
                <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: "12px" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution Bar Chart */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div className="mb-2">
            <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
              Risk Tier Distribution
            </h3>
            <p className="text-[11px] text-slate-500">Prudential risk classes derived from prime credit, DTI, and tenure rules.</p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskData} margin={{ top: 20, right: 20, left: 0, bottom: 5 }}>
                <XAxis dataKey="tier" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip
                  formatter={(val) => [`${val} applications`, "Volume"]}
                  contentStyle={{ backgroundColor: "#0f172a", borderRadius: "8px", borderColor: "#334155", color: "#f8fafc", fontSize: "12px" }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {riskData.map((entry, index) => (
                    <Cell key={`bar-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Applications Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
              Recent Underwritten Applications
            </h3>
            <p className="text-[11px] text-slate-500">Latest decisions executed through the production engine.</p>
          </div>

          <button
            onClick={() => setCurrentPage("history")}
            className="text-xs font-semibold text-finblue-600 dark:text-finblue-400 hover:underline flex items-center gap-1"
          >
            View All Applications <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-slate-600 dark:text-slate-400">
                <th className="py-2.5 px-3 font-semibold">Application ID</th>
                <th className="py-2.5 px-3 font-semibold">Bureau Score</th>
                <th className="py-2.5 px-3 font-semibold">Monthly Income</th>
                <th className="py-2.5 px-3 font-semibold">Requested Principal</th>
                <th className="py-2.5 px-3 font-semibold">Verdict</th>
                <th className="py-2.5 px-3 font-semibold">Risk Class</th>
                <th className="py-2.5 px-3 font-semibold">Recommended Sizing</th>
                <th className="py-2.5 px-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
              {stats?.recent_applications && stats.recent_applications.length > 0 ? (
                stats.recent_applications.map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/70 dark:hover:bg-slate-850/50 transition-colors">
                    <td className="py-3 px-3 font-mono font-bold text-finblue-600 dark:text-finblue-400">
                      {app.id}
                    </td>
                    <td className="py-3 px-3 font-medium">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-mono ${
                        app.credit_score >= 750 ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300" :
                        app.credit_score >= 650 ? "bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300" :
                        "bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300"
                      }`}>
                        {app.credit_score}
                      </span>
                    </td>
                    <td className="py-3 px-3">₹{app.monthly_income?.toLocaleString()}</td>
                    <td className="py-3 px-3">₹{app.requested_amount?.toLocaleString()}</td>
                    <td className="py-3 px-3">
                      <DecisionBadge status={app.decision_status} size="sm" />
                    </td>
                    <td className="py-3 px-3">
                      <span className="font-mono text-[11px]">{app.risk_class}</span>
                    </td>
                    <td className="py-3 px-3 font-semibold text-slate-900 dark:text-slate-100">
                      {app.recommended_amount > 0 ? `₹${app.recommended_amount.toLocaleString()}` : "—"}
                    </td>
                    <td className="py-3 px-3 text-right">
                      <button
                        onClick={() => {
                          setSelectedAppId(app.id);
                          setCurrentPage("audit-report");
                        }}
                        className="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded font-medium text-[11px] transition-colors"
                      >
                        Audit Memo
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-slate-400">
                    No applications evaluated yet. Click '+ New Application' to evaluate.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
