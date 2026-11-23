import React, { useState } from "react";
import { ChevronRight, ChevronDown, CheckCircle, Database, Sparkles, Binary } from "lucide-react";

function TreeNode({ node, depth = 0 }) {
  const [expanded, setExpanded] = useState(true);
  const hasChildren = node.children && node.children.length > 0;
  const isLeaf = node.is_leaf;

  return (
    <div className={`text-xs ${depth > 0 ? "ml-4 pl-3 border-l-2 border-slate-200 dark:border-slate-800" : ""}`}>
      <div className="py-1.5 flex items-start gap-2">
        {hasChildren ? (
          <button
            onClick={() => setExpanded(!expanded)}
            className="p-0.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 mt-0.5"
            aria-label={expanded ? "Collapse tree node" : "Expand tree node"}
          >
            {expanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
          </button>
        ) : (
          <div className="w-4 h-4 flex items-center justify-center mt-0.5 shrink-0">
            {isLeaf ? (
              <Database className="w-3 h-3 text-slate-400" />
            ) : (
              <CheckCircle className="w-3 h-3 text-emerald-500" />
            )}
          </div>
        )}

        <div className="flex-1 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-2.5 shadow-sm">
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <span className="font-mono font-bold text-finblue-600 dark:text-finblue-400 bg-finblue-50 dark:bg-finblue-950/40 px-2 py-0.5 rounded border border-finblue-200 dark:border-finblue-800 text-[11px]">
              {node.conclusion ? node.conclusion.display : "Atom"}
            </span>

            {node.rule_id && (
              <span className="text-[10px] font-mono bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-1.5 py-0.5 rounded">
                Rule: {node.rule_id}
              </span>
            )}
            {node.rule_name && (
              <span className="text-slate-500 dark:text-slate-400 text-[11px] font-medium">
                ({node.rule_name})
              </span>
            )}
          </div>

          {node.fol_form && (
            <div className="font-mono text-[11px] text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-850 p-1.5 rounded my-1 border border-slate-200/60 dark:border-slate-800">
              <span className="text-slate-400 mr-1.5 select-none">FOL:</span>
              <code>{node.fol_form}</code>
            </div>
          )}

          {node.plain_english && (
            <div className="text-[11px] text-slate-600 dark:text-slate-400 italic">
              "{node.plain_english}"
            </div>
          )}
        </div>
      </div>

      {hasChildren && expanded && (
        <div className="space-y-1">
          {node.children.map((child, idx) => (
            <TreeNode key={idx} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function ProofTreeView({ trees = [] }) {
  if (!trees || trees.length === 0) {
    return (
      <div className="p-6 text-center text-xs text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-900 rounded-lg border border-dashed border-slate-300 dark:border-slate-800">
        No First-Order Logic proof trees recorded for this evaluation.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-800">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
          <Binary className="w-4 h-4 text-finblue-600 dark:text-finblue-400" />
          First-Order Logic Derivation Proof Trees ({trees.length})
        </h4>
        <span className="text-[11px] text-slate-400">Ground Atoms & Horn Clauses</span>
      </div>

      <div className="space-y-3">
        {trees.map((tree, idx) => (
          <div key={idx} className="border border-slate-200 dark:border-slate-800 rounded-xl p-3 bg-slate-50/50 dark:bg-slate-950/30">
            <TreeNode node={tree} />
          </div>
        ))}
      </div>
    </div>
  );
}
