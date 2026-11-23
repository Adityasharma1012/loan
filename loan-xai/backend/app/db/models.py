"""SQLAlchemy ORM models for Applications, Decisions, Rule Executions,
ML Runs, and Fairness Reports.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(50), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Financial and Employment inputs
    age = Column(Integer, nullable=False)
    monthly_income = Column(Float, nullable=False)
    existing_monthly_debt = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)
    employment_years = Column(Float, nullable=False)
    repayment_history = Column(String(20), nullable=False)
    recent_default = Column(Boolean, default=False)
    requested_amount = Column(Float, nullable=False)
    requested_tenure_months = Column(Integer, nullable=False)
    loan_purpose = Column(String(50), default="Personal")
    employment_type = Column(String(50), default="Salaried")

    # Flagged input warnings (e.g. debt > income)
    input_warnings = Column(JSON, default=list)

    # Relationships
    decision = relationship("Decision", back_populates="application", uselist=False, cascade="all, delete-orphan")


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(String(50), ForeignKey("applications.id"), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    decision_status = Column(String(30), nullable=False, index=True)  # ELIGIBLE, CONDITIONALLY_ELIGIBLE, NOT_ELIGIBLE
    risk_class = Column(String(20), nullable=False, index=True)       # LOW, MEDIUM, HIGH
    interest_rate = Column(Float, nullable=False)
    interest_rate_band = Column(String(50), nullable=False)
    suggested_tenure_months = Column(Integer, nullable=False)
    recommended_amount = Column(Float, nullable=False)
    max_affordable_emi = Column(Float, nullable=False)
    requested_emi = Column(Float, nullable=False)
    recommended_emi = Column(Float, nullable=False)
    supportable_principal = Column(Float, nullable=False)
    exceeds_affordability = Column(Boolean, default=False)
    haircut_applied = Column(Boolean, default=False)

    rationale_summary = Column(Text, nullable=False)
    rejection_reasons = Column(JSON, default=list)
    conditions = Column(JSON, default=list)
    positive_factors = Column(JSON, default=list)
    risk_factors = Column(JSON, default=list)
    counterfactual_hints = Column(JSON, default=list)
    proof_trees = Column(JSON, default=list)
    threshold_version = Column(String(20), default="1.0.0")

    # Relationship to execution trace steps
    application = relationship("Application", back_populates="decision")
    rule_executions = relationship("RuleExecution", back_populates="decision", cascade="all, delete-orphan")


class RuleExecution(Base):
    __tablename__ = "rule_executions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"), index=True)
    step_number = Column(Integer, nullable=False)
    rule_id = Column(String(50), nullable=False, index=True)
    rule_name = Column(String(100), nullable=False)
    rule_type = Column(String(30), nullable=False)
    priority = Column(Integer, nullable=False)
    fol_form = Column(Text, nullable=True)
    plain_english = Column(Text, nullable=True)

    matched_facts = Column(JSON, default=list)
    actual_input_values = Column(JSON, default=dict)
    asserted_facts = Column(JSON, default=list)
    competing_rules = Column(JSON, default=list)
    resolution_reason = Column(Text, nullable=True)

    decision = relationship("Decision", back_populates="rule_executions")


class MLRun(Base):
    __tablename__ = "ml_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trained_at = Column(DateTime, default=datetime.utcnow)
    n_train_samples = Column(Integer, nullable=False)
    n_test_samples = Column(Integer, nullable=False)
    results_json = Column(JSON, nullable=False)


class FairnessReport(Base):
    __tablename__ = "fairness_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    report_json = Column(JSON, nullable=False)
