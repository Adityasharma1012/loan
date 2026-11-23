import React from "react";
import { ArrowRight, Lightbulb, Target } from "lucide-react";

export default function CounterfactualCard({ hint }) {
  const featureLabel = (hint.feature || "").replace(/_/g, " ").toUpperCase();

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm hover:border-finblue-300 dark:hover:border-finblue-700 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[11px] font-mono font-bold tracking-wider text-finblue-600 dark:text-finblue-400 bg-finblue-50 dark:bg-finblue-950/40 px-2 py-0.5 rounded border border-finblue-200 dark:border-finblue-800">
          {featureLabel}
        </span>
        <span className="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
          <Target className="w-3.5 h-3.5" />
          {hint.impact}
        </span>
      </div>

      <div className="flex items-center gap-3 my-2 text-xs">
        <div className="bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded text-slate-700 dark:text-slate-300 font-medium">
          Current: <span className="font-semibold">{String(hint.current_value)}</span>
        </div>
        <ArrowRight className="w-3.5 h-3.5 text-slate-400 shrink-0" />
        <div className="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 px-2.5 py-1 rounded font-medium">
          Target: <span className="font-semibold">{String(hint.target_value)}</span>
        </div>
      </div>

      <p className="text-xs text-slate-600 dark:text-slate-300 mt-2 flex items-start gap-1.5 leading-relaxed">
        <Lightbulb className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
        <span>{hint.delta_description}</span>
      </p>
    </div>
  );
}
