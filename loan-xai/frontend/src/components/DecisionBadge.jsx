import React from "react";
import { CheckCircle2, AlertTriangle, XCircle, Clock } from "lucide-react";

export default function DecisionBadge({ status, size = "md" }) {
  const norm = String(status || "").toUpperCase();

  let config = {
    label: "Under Review",
    ariaLabel: "Status: Under Review",
    icon: Clock,
    bg: "bg-slate-100 text-slate-700 border-slate-300 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700",
    iconColor: "text-slate-500",
  };

  if (norm === "ELIGIBLE" || norm === "APPROVED") {
    config = {
      label: "Eligible (Approved)",
      ariaLabel: "Decision Verdict: Fully Eligible and Approved",
      icon: CheckCircle2,
      bg: "bg-emerald-50 text-emerald-800 border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800",
      iconColor: "text-emerald-600 dark:text-emerald-400",
    };
  } else if (norm === "CONDITIONALLY_ELIGIBLE" || norm === "CONDITIONAL") {
    config = {
      label: "Conditionally Eligible",
      ariaLabel: "Decision Verdict: Conditionally Eligible subject to covenants",
      icon: AlertTriangle,
      bg: "bg-amber-50 text-amber-800 border-amber-300 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800",
      iconColor: "text-amber-600 dark:text-amber-400",
    };
  } else if (norm === "NOT_ELIGIBLE" || norm === "REJECTED" || norm === "DECLINED") {
    config = {
      label: "Not Eligible (Declined)",
      ariaLabel: "Decision Verdict: Not Eligible and Declined",
      icon: XCircle,
      bg: "bg-rose-50 text-rose-800 border-rose-300 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800",
      iconColor: "text-rose-600 dark:text-rose-400",
    };
  }

  const IconComponent = config.icon;
  const isSm = size === "sm";

  return (
    <span
      role="status"
      aria-label={config.ariaLabel}
      className={`inline-flex items-center gap-1.5 font-semibold border rounded-full transition-colors ${
        config.bg
      } ${isSm ? "px-2.5 py-0.5 text-xs" : "px-3.5 py-1 text-sm"}`}
    >
      <IconComponent className={`${isSm ? "w-3.5 h-3.5" : "w-4 h-4"} ${config.iconColor} shrink-0`} aria-hidden="true" />
      <span>{config.label}</span>
    </span>
  );
}
