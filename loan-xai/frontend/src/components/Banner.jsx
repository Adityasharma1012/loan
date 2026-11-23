import React from "react";
import { AlertCircle, ShieldAlert } from "lucide-react";

export default function Banner() {
  return (
    <div className="bg-amber-500/10 border-b border-amber-500/30 px-4 py-2 text-amber-900 dark:text-amber-200 text-xs sm:text-sm font-medium flex items-center justify-between shadow-sm sticky top-0 z-50 backdrop-blur-md">
      <div className="flex items-center gap-2 mx-auto">
        <ShieldAlert className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
        <span className="font-semibold">Academic demo.</span>
        <span>Rates and amounts are illustrative, not bank offers. Approval is never guaranteed. Synthetic data only.</span>
      </div>
    </div>
  );
}
