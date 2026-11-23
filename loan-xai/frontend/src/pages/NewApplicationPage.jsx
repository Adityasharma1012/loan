import React, { useState } from "react";
import {
  FilePlus2,
  Sparkles,
  AlertCircle,
  HelpCircle,
  CheckCircle,
  IndianRupee,
  Layers,
  ArrowRight,
  ShieldAlert,
} from "lucide-react";
import { evaluateApplication } from "../api/client";

export default function NewApplicationPage({ setCurrentPage, setLatestEvaluation, setSelectedAppId }) {
  const [formData, setFormData] = useState({
    age: 32,
    monthly_income: 65000,
    existing_monthly_debt: 12000,
    credit_score: 780,
    employment_years: 4.5,
    repayment_history: "Good",
    recent_default: false,
    requested_amount: 300000,
    requested_tenure_months: 36,
    loan_purpose: "Personal",
    employment_type: "Salaried",
  });

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [warnings, setWarnings] = useState([]);

  // Presets covering the required scenarios
  const presets = [
    {
      title: "1. Prime Eligible",
      desc: "High income, 820 credit, low DTI",
      data: {
        age: 35,
        monthly_income: 120000,
        existing_monthly_debt: 15000,
        credit_score: 820,
        employment_years: 7.0,
        repayment_history: "Excellent",
        recent_default: false,
        requested_amount: 400000,
        requested_tenure_months: 36,
        loan_purpose: "Home Improvement",
        employment_type: "Salaried",
      },
    },
    {
      title: "2. Near-Prime Conditional",
      desc: "Credit 680, 30% DTI, clean repayment",
      data: {
        age: 31,
        monthly_income: 45000,
        existing_monthly_debt: 13500,
        credit_score: 680,
        employment_years: 3.2,
        repayment_history: "Good",
        recent_default: false,
        requested_amount: 150000,
        requested_tenure_months: 36,
        loan_purpose: "Debt Consolidation",
        employment_type: "Salaried",
      },
    },
    {
      title: "3. Excessive DTI (64%)",
      desc: "Prime credit but over-leveraged debt",
      data: {
        age: 40,
        monthly_income: 50000,
        existing_monthly_debt: 32000,
        credit_score: 760,
        employment_years: 5.0,
        repayment_history: "Good",
        recent_default: false,
        requested_amount: 200000,
        requested_tenure_months: 36,
        loan_purpose: "Personal",
        employment_type: "Salaried",
      },
    },
    {
      title: "4. Short Employment (0.8 Yr)",
      desc: "770 score, employment < 2 years",
      data: {
        age: 26,
        monthly_income: 45000,
        existing_monthly_debt: 10000,
        credit_score: 770,
        employment_years: 0.8,
        repayment_history: "Good",
        recent_default: false,
        requested_amount: 150000,
        requested_tenure_months: 48,
        loan_purpose: "Education",
        employment_type: "Salaried",
      },
    },
    {
      title: "5. Legal Age Knock-out (Age 17)",
      desc: "Minor applicant with high income",
      data: {
        age: 17,
        monthly_income: 500000,
        existing_monthly_debt: 0,
        credit_score: 850,
        employment_years: 2.0,
        repayment_history: "Excellent",
        recent_default: false,
        requested_amount: 100000,
        requested_tenure_months: 12,
        loan_purpose: "Personal",
        employment_type: "Self-Employed",
      },
    },
    {
      title: "6. Exceeds Affordability",
      desc: "Requests ₹25 Lakhs on ₹35k income",
      data: {
        age: 30,
        monthly_income: 35000,
        existing_monthly_debt: 9000,
        credit_score: 780,
        employment_years: 4.0,
        repayment_history: "Good",
        recent_default: false,
        requested_amount: 2500000,
        requested_tenure_months: 36,
        loan_purpose: "Business",
        employment_type: "Business Owner",
      },
    },
  ];

  const applyPreset = (preset) => {
    setFormData({ ...preset.data });
    setErrorMessage(null);
    setWarnings([]);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : type === "number" ? Number(value) : value,
    }));
  };

  // Derived real-time calculations
  const liveDTI = formData.monthly_income > 0 ? (formData.existing_monthly_debt / formData.monthly_income) : 0;
  const liveMaxEMI = Math.max(0, 0.40 * formData.monthly_income - formData.existing_monthly_debt);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage(null);
    setWarnings([]);

    try {
      const result = await evaluateApplication(formData);
      setLatestEvaluation(result);
      setSelectedAppId(result.application_id);
      setCurrentPage("results");
    } catch (err) {
      setErrorMessage(err.message || "Evaluation failed. Please check form parameters.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
          Credit Application & Underwriting Form
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Enter applicant financial parameters or select a pre-configured scenario to trigger the forward-chaining rule engine.
        </p>
      </div>

      {/* Preset Scenarios Carousel/Grid */}
      <div className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-finblue-600" />
            Quick Demo Presets (Test Scenarios)
          </span>
          <span className="text-[11px] text-slate-400">Click to load pre-validated edge cases</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
          {presets.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => applyPreset(p)}
              className="text-left p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 hover:border-finblue-500 dark:hover:border-finblue-500 transition-all shadow-sm hover:scale-[1.02] flex flex-col justify-between"
            >
              <div className="font-bold text-[11px] text-slate-900 dark:text-slate-100 truncate">{p.title}</div>
              <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-1 line-clamp-2 leading-tight">{p.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Form Card */}
      <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
        {errorMessage && (
          <div className="p-4 bg-rose-50 dark:bg-rose-950/40 text-rose-800 dark:text-rose-200 border border-rose-300 dark:border-rose-800 rounded-xl text-xs flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">Validation or Processing Error:</span> {errorMessage}
            </div>
          </div>
        )}

        {/* Real-time Financial Preview Bar */}
        <div className="bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 rounded-xl p-4 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
          <div>
            <div className="text-[11px] text-slate-500 font-sans">Live Debt-to-Income (DTI)</div>
            <div className={`text-base font-bold ${
              liveDTI <= 0.40 ? "text-emerald-600 dark:text-emerald-400" :
              liveDTI <= 0.50 ? "text-amber-600 dark:text-amber-400" :
              "text-rose-600 dark:text-rose-400"
            }`}>
              {(liveDTI * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-400 font-sans">Eligible ceiling: &le; 40%</div>
          </div>

          <div>
            <div className="text-[11px] text-slate-500 font-sans">Affordable Max EMI</div>
            <div className="text-base font-bold text-slate-900 dark:text-slate-100">
              ₹{liveMaxEMI.toLocaleString(undefined, { maximumFractionDigits: 0 })}
            </div>
            <div className="text-[10px] text-slate-400 font-sans">40% income minus debt</div>
          </div>

          <div>
            <div className="text-[11px] text-slate-500 font-sans">Credit Bureau Tier</div>
            <div className={`text-base font-bold ${
              formData.credit_score >= 750 ? "text-emerald-600 dark:text-emerald-400" :
              formData.credit_score >= 650 ? "text-amber-600 dark:text-amber-400" :
              "text-rose-600 dark:text-rose-400"
            }`}>
              {formData.credit_score >= 750 ? "Prime (&ge;750)" : formData.credit_score >= 650 ? "Near-Prime (650-749)" : "Subprime (<650)"}
            </div>
            <div className="text-[10px] text-slate-400 font-sans">Hard floor: 550</div>
          </div>

          <div>
            <div className="text-[11px] text-slate-500 font-sans">Employment Tenure</div>
            <div className={`text-base font-bold ${formData.employment_years >= 2.0 ? "text-emerald-600 dark:text-emerald-400" : "text-amber-600 dark:text-amber-400"}`}>
              {formData.employment_years} Years
            </div>
            <div className="text-[10px] text-slate-400 font-sans">&ge; 2.0 yrs prime threshold</div>
          </div>
        </div>

        {/* Section 1: Financial Capacity */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 pb-1 border-b border-slate-100 dark:border-slate-800">
            1. Income & Existing Obligations
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Verified Monthly Income (₹) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                name="monthly_income"
                value={formData.monthly_income}
                onChange={handleChange}
                min="0"
                step="500"
                required
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              />
              <span className="text-[10px] text-slate-400">Prime standard: &ge; ₹30,000</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Existing Monthly Debt Service (₹) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                name="existing_monthly_debt"
                value={formData.existing_monthly_debt}
                onChange={handleChange}
                min="0"
                step="500"
                required
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              />
              <span className="text-[10px] text-slate-400">Current EMIs + card minimums</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Employment Duration (Years) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                name="employment_years"
                value={formData.employment_years}
                onChange={handleChange}
                min="0"
                max="50"
                step="0.1"
                required
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              />
              <span className="text-[10px] text-slate-400">Continuous verifiable tenure</span>
            </div>
          </div>
        </div>

        {/* Section 2: Credit & Legal Capacity */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 pb-1 border-b border-slate-100 dark:border-slate-800">
            2. Credit Bureau Profile & Legal Capacity
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Bureau Credit Score (300-900) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                name="credit_score"
                value={formData.credit_score}
                onChange={handleChange}
                min="300"
                max="900"
                required
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              />
              <span className="text-[10px] text-slate-400">Prime &ge; 750, Floor = 550</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Applicant Age (Years) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                min="18"
                max="100"
                required
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              />
              <span className="text-[10px] text-slate-400">Legal contract capacity (&ge; 18)</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Repayment Track Record <span className="text-rose-500">*</span>
              </label>
              <select
                name="repayment_history"
                value={formData.repayment_history}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              >
                <option value="Excellent">Excellent (No delays)</option>
                <option value="Good">Good (Occasional &lt; 30d)</option>
                <option value="Fair">Fair (Multiple 30d delays)</option>
                <option value="Poor">Poor (60d+ delinquency)</option>
              </select>
            </div>

            <div className="flex flex-col justify-center">
              <label className="flex items-center gap-2 cursor-pointer mt-2 sm:mt-4">
                <input
                  type="checkbox"
                  name="recent_default"
                  checked={formData.recent_default}
                  onChange={handleChange}
                  className="w-4 h-4 rounded text-rose-600 focus:ring-rose-500 border-slate-300"
                />
                <span className="text-xs font-semibold text-rose-700 dark:text-rose-400">
                  Recent Default on Record
                </span>
              </label>
              <span className="text-[10px] text-slate-400 ml-6">Statutory knockout if true</span>
            </div>
          </div>
        </div>

        {/* Section 3: Loan Sizing Request */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 pb-1 border-b border-slate-100 dark:border-slate-800">
            3. Loan Terms Requested
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Requested Principal (₹) <span className="text-rose-500">*</span>
              </label>
              <input
                type="number"
                name="requested_amount"
                value={formData.requested_amount}
                onChange={handleChange}
                min="10000"
                step="5000"
                required
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Tenure (Months) <span className="text-rose-500">*</span>
              </label>
              <select
                name="requested_tenure_months"
                value={formData.requested_tenure_months}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              >
                <option value={12}>12 Months (1 Year)</option>
                <option value={24}>24 Months (2 Years)</option>
                <option value={36}>36 Months (3 Years)</option>
                <option value={48}>48 Months (4 Years)</option>
                <option value={60}>60 Months (5 Years)</option>
                <option value={84}>84 Months (7 Years)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Loan Purpose
              </label>
              <select
                name="loan_purpose"
                value={formData.loan_purpose}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              >
                <option value="Personal">Personal</option>
                <option value="Debt Consolidation">Debt Consolidation</option>
                <option value="Home Improvement">Home Improvement</option>
                <option value="Education">Education</option>
                <option value="Business">Business</option>
                <option value="Medical">Medical</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Employment Type
              </label>
              <select
                name="employment_type"
                value={formData.employment_type}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg focus:ring-2 focus:ring-finblue-500"
              >
                <option value="Salaried">Salaried</option>
                <option value="Self-Employed">Self-Employed</option>
                <option value="Business Owner">Business Owner</option>
                <option value="Contractor">Contractor</option>
              </select>
            </div>
          </div>
        </div>

        {/* Fairness-safe Notice */}
        <div className="p-3 bg-slate-50 dark:bg-slate-850 rounded-xl border border-slate-200 dark:border-slate-800 text-[11px] text-slate-500 flex items-start gap-2">
          <ShieldAlert className="w-4 h-4 text-finblue-600 shrink-0 mt-0.5" />
          <span>
            <b>Fairness-Safe Design:</b> This application form does NOT solicit protected demographic attributes (gender, religion, caste, ethnicity, or region). Age is captured solely for statutory legal capacity verification (18+).
          </span>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-4 border-t border-slate-100 dark:border-slate-800">
          <button
            type="submit"
            disabled={loading}
            className="flex items-center gap-2 px-6 py-2.5 bg-finblue-600 hover:bg-finblue-500 disabled:bg-slate-400 text-white font-semibold text-sm rounded-xl shadow-md shadow-finblue-600/30 transition-all hover:scale-[1.01]"
          >
            {loading ? (
              <>
                <Layers className="w-4 h-4 animate-spin" />
                <span>Running Inference Engine...</span>
              </>
            ) : (
              <>
                <span>Evaluate Application</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
