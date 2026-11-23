import React from "react";
import { CheckCircle2, ShieldCheck, Flame, GitCommit, Layers } from "lucide-react";

export default function ExecutionTimeline({ trace = [] }) {
  if (!trace || trace.length === 0) {
    return (
      <div className="p-6 text-center text-xs text-slate-500 bg-slate-50 dark:bg-slate-900 rounded-lg border border-dashed border-slate-300 dark:border-slate-800">
        No execution trace recorded.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-800">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
          <Layers className="w-4 h-4 text-finblue-600 dark:text-finblue-400" />
          Chronological Forward-Chaining Inference Trace ({trace.length} Steps)
        </h4>
        <span className="text-[11px] text-slate-400">Refraction Enforced • Conflict Resolution Applied</span>
      </div>

      <div className="relative border-l-2 border-slate-200 dark:border-slate-800 ml-4 space-y-6">
        {trace.map((step, idx) => {
          const isHKO = step.rule_type === "hard_knockout";
          const isDec = step.rule_type === "decision";

          let badgeColor = "bg-finblue-50 text-finblue-700 border-finblue-200 dark:bg-finblue-950/40 dark:text-finblue-300 dark:border-finblue-800";
          if (isHKO) {
            badgeColor = "bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800";
          } else if (isDec) {
            badgeColor = "bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/40 dark:text-purple-300 dark:border-purple-800";
          }

          return (
            <div key={idx} className="relative pl-6">
              {/* Step Marker Dot */}
              <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-white dark:bg-slate-900 border-2 border-finblue-600 dark:border-finblue-400 flex items-center justify-center">
                <div className="w-1.5 h-1.5 rounded-full bg-finblue-600 dark:bg-finblue-400" />
              </div>

              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm hover:shadow transition-shadow">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded">
                      Step #{step.step}
                    </span>
                    <span className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded border ${badgeColor}`}>
                      {step.rule_id}
                    </span>
                    <span className="text-sm font-bold text-slate-900 dark:text-slate-100">
                      {step.rule_name}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-[11px] text-slate-500 font-mono">
                    <span>Priority: {step.priority}</span>
                    <span>•</span>
                    <span>Conflict Set: {step.conflict_set_size}</span>
                  </div>
                </div>

                {/* Conflict Resolution Reason */}
                {step.resolution_reason && (
                  <div className="text-[11px] text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-850 p-2 rounded mb-2 border border-slate-200/50 dark:border-slate-800">
                    <span className="font-semibold text-slate-700 dark:text-slate-300">Conflict Resolution:</span>{" "}
                    {step.resolution_reason}
                  </div>
                )}

                {/* FOL Horn Clause Notation */}
                {step.fol_form && (
                  <div className="font-mono text-xs text-slate-800 dark:text-slate-200 bg-finblue-50/50 dark:bg-finblue-950/20 border border-finblue-100 dark:border-finblue-900/40 p-2 rounded mb-2">
                    <span className="text-[10px] uppercase font-bold text-finblue-600 dark:text-finblue-400 mr-2 select-none">
                      FOL Clause:
                    </span>
                    <code>{step.fol_form}</code>
                  </div>
                )}

                {/* Plain English explanation */}
                {step.plain_english && (
                  <p className="text-xs text-slate-600 dark:text-slate-300 italic mb-3">
                    "{step.plain_english}"
                  </p>
                )}

                {/* Facts Asserted in this Step */}
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-semibold text-slate-400">Asserted Facts:</span>
                  {step.asserted_facts && step.asserted_facts.map((fact, fIdx) => (
                    <span
                      key={fIdx}
                      className="text-[11px] font-mono bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 px-2 py-0.5 rounded flex items-center gap-1"
                    >
                      <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                      {fact.display || fact.predicate}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
