import React, { useState, useEffect } from "react";
import {
  BookOpen,
  Binary,
  Layers,
  Cpu,
  ShieldCheck,
  Search,
  Filter,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";
import { fetchRulesCatalogue } from "../api/client";

export default function AboutPage() {
  const [catalogue, setCatalogue] = useState(null);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRulesCatalogue()
      .then((res) => setCatalogue(res))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const rules = catalogue?.rules || [];
  const thresholds = catalogue?.thresholds || {};

  const filteredRules = rules.filter((r) => {
    const matchesSearch =
      r.id.toLowerCase().includes(search.toLowerCase()) ||
      r.name.toLowerCase().includes(search.toLowerCase()) ||
      (r.plain_english && r.plain_english.toLowerCase().includes(search.toLowerCase())) ||
      (r.fol_form && r.fol_form.toLowerCase().includes(search.toLowerCase()));

    const matchesType = typeFilter ? r.rule_type === typeFilter : true;
    return matchesSearch && matchesType;
  });

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
          Course: Artificial Intelligence Foundations
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
          Knowledge Base, FOL Specifications & Production Rules
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Formal First-Order Logic Horn clauses, forward-chaining conflict resolution semantics, and regulatory compliance standards.
        </p>
      </div>

      {/* Formal Foundations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <div className="w-9 h-9 rounded-xl bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 flex items-center justify-center">
            <Binary className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
            First-Order Logic (FOL) & Horn Clauses
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            Every production rule is formulated as a universally quantified definite Horn clause with at most one positive literal in the head:
          </p>
          <div className="bg-slate-50 dark:bg-slate-950 p-3 rounded-xl border border-slate-200 dark:border-slate-800 font-mono text-xs text-slate-800 dark:text-slate-200">
            &forall; x: P<sub>1</sub>(x) &and; P<sub>2</sub>(x) &and; ... &and; P<sub>k</sub>(x) &rarr; C(x)
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            <b>Negation-As-Failure (NAF):</b> Handled via closed-world assumption: if an atom cannot be proven from current working memory facts, its negation &sim;P(x) succeeds.
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-3">
          <div className="w-9 h-9 rounded-xl bg-finblue-50 dark:bg-finblue-950/60 text-finblue-600 dark:text-finblue-400 flex items-center justify-center">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
            Forward-Chaining & Conflict Resolution
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            The inference engine executes a forward-chaining cycle until fixpoint. When multiple rules are simultaneously eligible, the conflict set is resolved by:
          </p>
          <ol className="list-decimal pl-5 text-xs text-slate-600 dark:text-slate-400 space-y-1">
            <li><b>Hard Knock-outs:</b> Immediate disqualification rules fire first.</li>
            <li><b>Priority / Salience:</b> Integer priority descending.</li>
            <li><b>Specificity:</b> Rules with more premises fire before general rules.</li>
            <li><b>Deterministic Tie-Break:</b> Rule ID ascending.</li>
          </ol>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            <b>Refraction:</b> Each rule fires at most once per applicant run, guaranteeing termination.
          </p>
        </div>
      </div>

      {/* Declarative Rules Catalogue Explorer */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-finblue-600" />
              Declarative Production Rules Catalogue ({filteredRules.length} of {rules.length})
            </h3>
            <p className="text-[11px] text-slate-500">
              Live declarative rules loaded from <code>config/rules.yaml</code>.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
              <input
                type="text"
                placeholder="Search rules..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-xs"
              />
            </div>

            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-xs"
            >
              <option value="">All Rule Types</option>
              <option value="hard_knockout">Hard Knock-Out</option>
              <option value="derivation">Derivation</option>
              <option value="decision">Decision</option>
            </select>
          </div>
        </div>

        <div className="space-y-3">
          {filteredRules.map((rule, idx) => {
            const isHKO = rule.rule_type === "hard_knockout";
            const isDec = rule.rule_type === "decision";
            return (
              <div
                key={rule.id}
                className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/30 hover:border-slate-300 dark:hover:border-slate-700 transition-colors space-y-2"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-xs text-finblue-600 dark:text-finblue-400">
                      {rule.id}
                    </span>
                    <span className="font-bold text-xs text-slate-900 dark:text-slate-100">
                      {rule.name}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-[10px] font-mono">
                    <span className={`px-2 py-0.5 rounded border ${
                      isHKO ? "bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800" :
                      isDec ? "bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/40 dark:text-purple-300 dark:border-purple-800" :
                      "bg-finblue-50 text-finblue-700 border-finblue-200 dark:bg-finblue-950/40 dark:text-finblue-300 dark:border-finblue-800"
                    }`}>
                      {rule.rule_type}
                    </span>
                    <span className="bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded text-slate-600 dark:text-slate-300">
                      Priority: {rule.priority}
                    </span>
                  </div>
                </div>

                <div className="font-mono text-xs text-slate-800 dark:text-slate-200 bg-white dark:bg-slate-900 p-2 rounded border border-slate-200/60 dark:border-slate-800">
                  <span className="text-[10px] text-slate-400 mr-2 uppercase select-none">FOL:</span>
                  <code>{rule.fol_form}</code>
                </div>

                <p className="text-xs text-slate-600 dark:text-slate-400 italic">
                  "{rule.plain_english}"
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
