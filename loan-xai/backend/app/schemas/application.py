"""Pydantic v2 validation models, request/response contracts,
and warning detection logic.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator


class RepaymentHistoryEnum(str, Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"


class LoanPurposeEnum(str, Enum):
    PERSONAL = "Personal"
    DEBT_CONSOLIDATION = "Debt Consolidation"
    HOME_IMPROVEMENT = "Home Improvement"
    EDUCATION = "Education"
    BUSINESS = "Business"
    MEDICAL = "Medical"
    OTHER = "Other"


class EmploymentTypeEnum(str, Enum):
    SALARIED = "Salaried"
    SELF_EMPLOYED = "Self-Employed"
    BUSINESS_OWNER = "Business Owner"
    CONTRACTOR = "Contractor"


class EvaluateApplicationRequest(BaseModel):
    applicant_id: Optional[str] = Field(default=None, description="Optional custom applicant ID")
    age: int = Field(..., ge=18, le=100, description="Applicant age (must be between 18 and 100)")
    monthly_income: float = Field(..., gt=0.0, description="Verified monthly gross income in INR (must be > 0)")
    existing_monthly_debt: float = Field(..., ge=0.0, description="Existing monthly debt commitments in INR (>= 0)")
    credit_score: int = Field(..., ge=300, le=900, description="Bureau credit score (300 to 900)")
    employment_years: float = Field(..., ge=0.0, le=60.0, description="Continuous employment duration in years")
    repayment_history: RepaymentHistoryEnum = Field(..., description="Historical repayment rating")
    recent_default: bool = Field(default=False, description="Whether applicant defaulted within past 24 months")
    requested_amount: float = Field(..., ge=1000.0, le=10000000.0, description="Requested loan amount in INR")
    requested_tenure_months: int = Field(..., ge=6, le=84, description="Requested tenure in months (6 to 84)")
    loan_purpose: LoanPurposeEnum = Field(default=LoanPurposeEnum.PERSONAL, description="Purpose of the loan")
    employment_type: EmploymentTypeEnum = Field(default=EmploymentTypeEnum.SALARIED, description="Type of employment")

    def detect_warnings(self) -> List[str]:
        """Flags unusual-but-valid inputs for underwriter review."""
        warnings = []
        if self.existing_monthly_debt > self.monthly_income:
            warnings.append(
                f"High Financial Strain: Existing monthly debt (₹{self.existing_monthly_debt:,.0f}) exceeds total monthly income (₹{self.monthly_income:,.0f})."
            )
        if self.requested_amount > (self.monthly_income * 50):
            warnings.append(
                f"Disproportionate Request: Requested loan (₹{self.requested_amount:,.0f}) exceeds 50x monthly gross income."
            )
        if self.requested_amount < 10000.0:
            warnings.append(
                f"Micro-loan Threshold: Requested amount is below typical institutional unsecured ticket size (₹10,000)."
            )
        return warnings


class CounterfactualHintSchema(BaseModel):
    feature: str
    current_value: Any
    target_value: Any
    delta_description: str
    impact: str


class RuleExecutionStepSchema(BaseModel):
    step: int
    rule_id: str
    rule_name: str
    rule_type: str
    priority: int
    fol_form: Optional[str] = None
    plain_english: Optional[str] = None
    matched_facts: List[Dict[str, Any]] = []
    actual_input_values: Dict[str, Any] = {}
    asserted_facts: List[Dict[str, Any]] = []
    conflict_set_size: int = 1
    competing_rules: List[Dict[str, Any]] = []
    resolution_reason: Optional[str] = None


class DecisionResponseSchema(BaseModel):
    application_id: str
    decision: str
    risk_class: str
    interest_rate: float
    interest_rate_percent: float
    interest_rate_band: str
    suggested_tenure_months: int
    requested_amount: float
    recommended_amount: float
    max_affordable_emi: float
    requested_emi: float
    recommended_emi: float
    supportable_principal: float
    exceeds_affordability: bool
    haircut_applied: bool
    conditions: List[str] = []
    rejection_reasons: List[str] = []
    positive_factors: List[str] = []
    risk_factors: List[str] = []
    counterfactual_hints: List[CounterfactualHintSchema] = []
    rationale_summary: str
    execution_trace: List[RuleExecutionStepSchema] = []
    proof_trees: List[Dict[str, Any]] = []
    threshold_version: str
    input_warnings: List[str] = []
    ml_comparison: Optional[Dict[str, Any]] = None


class ApplicationListItemSchema(BaseModel):
    id: str
    created_at: str
    age: int
    monthly_income: float
    existing_monthly_debt: float
    credit_score: int
    employment_years: float
    requested_amount: float
    requested_tenure_months: int
    decision_status: Optional[str] = None
    risk_class: Optional[str] = None
    recommended_amount: Optional[float] = None
    interest_rate_band: Optional[str] = None
    input_warnings_count: int = 0
