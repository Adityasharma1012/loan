import React from "react";
import {
  LayoutDashboard,
  FilePlus2,
  FileCheck,
  Cpu,
  GitCompare,
  Scale,
  History,
  FileText,
  BookOpen,
  Sun,
  Moon,
  Sparkles,
  Home,
  ShieldCheck,
} from "lucide-react";

export default function Sidebar({ currentPage, setCurrentPage, isDarkMode, setIsDarkMode }) {
  const navItems = [
    { id: "landing", label: "Overview", icon: Home },
    { id: "dashboard", label: "Executive Dashboard", icon: LayoutDashboard },
    { id: "new-application", label: "New Application", icon: FilePlus2 },
    { id: "results", label: "Decision Verdict", icon: FileCheck },
    { id: "explanation", label: "Rule Inference Trace", icon: Cpu },
    { id: "ml-comparison", label: "ML Benchmark", icon: GitCompare },
    { id: "fairness", label: "Fairness & Bias Audit", icon: Scale },
    { id: "history", label: "Application History", icon: History },
    { id: "audit-report", label: "Underwriting Memo", icon: FileText },
    { id: "about", label: "Rules & Logic Specs", icon: BookOpen },
  ];

  return (
    <aside className="w-64 bg-navy-950 text-slate-200 flex flex-col border-r border-slate-800 shrink-0 select-none">
      {/* Branding Header */}
      <div className="p-4 border-b border-slate-800/80 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-finblue-600 flex items-center justify-center text-white shadow-md shadow-finblue-600/30">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <div className="font-bold text-sm text-white tracking-wide flex items-center gap-1.5">
            LoanXAI
            <span className="text-[10px] bg-finblue-500/20 text-finblue-400 font-mono px-1.5 py-0.5 rounded border border-finblue-500/30">
              v1.0
            </span>
          </div>
          <div className="text-[11px] text-slate-400">AI Foundations Expert System</div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto" aria-label="Sidebar Navigation">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                active
                  ? "bg-finblue-600 text-white shadow-sm shadow-finblue-600/40"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-850"
              }`}
            >
              <Icon className={`w-4 h-4 shrink-0 ${active ? "text-white" : "text-slate-400"}`} />
              <span className="truncate">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Footer & Dark Mode Toggle */}
      <div className="p-3 border-t border-slate-800/80 space-y-2">
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-medium border border-slate-800 transition-colors"
          aria-label="Toggle light and dark theme"
        >
          <span className="flex items-center gap-2">
            {isDarkMode ? <Moon className="w-4 h-4 text-amber-400" /> : <Sun className="w-4 h-4 text-amber-500" />}
            <span>{isDarkMode ? "Dark Mode" : "Light Mode"}</span>
          </span>
          <span className="text-[10px] text-slate-500 font-mono">Toggle</span>
        </button>

        <div className="px-2 py-1 text-[11px] text-slate-400 text-center">
          First-Order Logic + Expert Rules
        </div>
      </div>
    </aside>
  );
}
