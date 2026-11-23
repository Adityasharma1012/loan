import React, { useState, useEffect } from "react";
import {
  History,
  Search,
  Filter,
  Download,
  FileText,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
} from "lucide-react";
import { fetchApplications, getCSVExportUrl, getPDFExportUrl } from "../api/client";
import DecisionBadge from "../components/DecisionBadge";

export default function HistoryPage({ setCurrentPage, setSelectedAppId }) {
  const [applications, setApplications] = useState([]);
  const [total, setTotal] = useState(0);
  const [limit, setLimit] = useState(25);
  const [offset, setOffset] = useState(0);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [riskFilter, setRiskFilter] = useState("");
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await fetchApplications({
        limit,
        offset,
        search,
        status: statusFilter,
        risk: riskFilter,
      });
      setApplications(res.items || []);
      setTotal(res.total || 0);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [offset, limit, statusFilter, riskFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setOffset(0);
    loadData();
  };

  const totalPages = Math.ceil(total / limit) || 1;
  const currentPageNum = Math.floor(offset / limit) + 1;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
            Historical Applications Ledger
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Immutable SQLite records of all underwritten applications, decisions, and execution traces.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <a
            href={getCSVExportUrl()}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 px-3 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-semibold rounded-lg transition-colors border border-slate-200 dark:border-slate-700"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </a>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
        <form onSubmit={handleSearchSubmit} className="flex-1 min-w-[240px] flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search by Application ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:ring-2 focus:ring-finblue-500 text-xs"
            />
          </div>
          <button
            type="submit"
            className="px-3.5 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 rounded-lg font-semibold"
          >
            Search
          </button>
        </form>

        <div className="flex items-center gap-2">
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setOffset(0);
            }}
            className="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-xs"
          >
            <option value="">All Verdicts</option>
            <option value="ELIGIBLE">Eligible</option>
            <option value="CONDITIONALLY_ELIGIBLE">Conditional</option>
            <option value="NOT_ELIGIBLE">Not Eligible</option>
          </select>

          <select
            value={riskFilter}
            onChange={(e) => {
              setRiskFilter(e.target.value);
              setOffset(0);
            }}
            className="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-xs"
          >
            <option value="">All Risk Tiers</option>
            <option value="LOW">Low Risk</option>
            <option value="MEDIUM">Medium Risk</option>
            <option value="HIGH">High Risk</option>
          </select>
        </div>
      </div>

      {/* Applications Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-slate-600 dark:text-slate-400">
                <th className="py-2.5 px-3 font-semibold">Application ID</th>
                <th className="py-2.5 px-3 font-semibold">Date</th>
                <th className="py-2.5 px-3 font-semibold">Bureau Score</th>
                <th className="py-2.5 px-3 font-semibold">Income</th>
                <th className="py-2.5 px-3 font-semibold">Requested</th>
                <th className="py-2.5 px-3 font-semibold">Verdict</th>
                <th className="py-2.5 px-3 font-semibold">Risk Class</th>
                <th className="py-2.5 px-3 font-semibold">Recommended Sizing</th>
                <th className="py-2.5 px-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan={9} className="py-8 text-center text-slate-400">
                    Loading applications...
                  </td>
                </tr>
              ) : applications.length > 0 ? (
                applications.map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/70 dark:hover:bg-slate-850/50 transition-colors">
                    <td className="py-3 px-3 font-mono font-bold text-finblue-600 dark:text-finblue-400">
                      {app.id}
                    </td>
                    <td className="py-3 px-3 text-slate-400 text-[11px]">
                      {app.created_at ? app.created_at.split("T")[0] : ""}
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
                    <td className="py-3 px-3 font-mono">₹{app.monthly_income?.toLocaleString()}</td>
                    <td className="py-3 px-3 font-mono">₹{app.requested_amount?.toLocaleString()}</td>
                    <td className="py-3 px-3">
                      <DecisionBadge status={app.decision_status} size="sm" />
                    </td>
                    <td className="py-3 px-3 font-mono text-[11px]">
                      {app.risk_class || "—"}
                    </td>
                    <td className="py-3 px-3 font-mono font-semibold text-slate-900 dark:text-slate-100">
                      {app.recommended_amount > 0 ? `₹${app.recommended_amount.toLocaleString()}` : "—"}
                    </td>
                    <td className="py-3 px-3 text-right">
                      <div className="inline-flex items-center gap-1.5">
                        <button
                          onClick={() => {
                            setSelectedAppId(app.id);
                            setCurrentPage("audit-report");
                          }}
                          className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded font-medium text-[11px]"
                          title="Open detailed audit memo"
                        >
                          View Memo
                        </button>
                        <a
                          href={getPDFExportUrl(app.id)}
                          target="_blank"
                          rel="noreferrer"
                          className="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 hover:text-slate-700"
                          title="Download PDF"
                        >
                          <Download className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={9} className="py-8 text-center text-slate-400">
                    No matching applications found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-800 text-xs">
          <div className="text-slate-500">
            Showing {Math.min(total, offset + 1)} to {Math.min(total, offset + limit)} of {total} records
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setOffset(Math.max(0, offset - limit))}
              disabled={offset === 0}
              className="px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 disabled:opacity-40 flex items-center gap-1"
            >
              <ChevronLeft className="w-3.5 h-3.5" /> Previous
            </button>
            <span className="font-mono text-slate-600 dark:text-slate-300">
              Page {currentPageNum} of {totalPages}
            </span>
            <button
              onClick={() => setOffset(offset + limit)}
              disabled={offset + limit >= total}
              className="px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 disabled:opacity-40 flex items-center gap-1"
            >
              Next <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
