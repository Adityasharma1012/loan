"""Integration tests for FastAPI endpoints: evaluation, validation,
retrieval, stats, ML, fairness, PDF, and CSV.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_root_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Explainable Rule-Based" in res.json()["system"]


def test_evaluate_endpoint_eligible_application(client):
    payload = {
        "age": 32,
        "monthly_income": 65000.0,
        "existing_monthly_debt": 10000.0,
        "credit_score": 790,
        "employment_years": 4.5,
        "repayment_history": "Excellent",
        "recent_default": False,
        "requested_amount": 200000.0,
        "requested_tenure_months": 36,
        "loan_purpose": "Personal",
        "employment_type": "Salaried",
    }
    res = client.post("/api/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] == "ELIGIBLE"
    assert data["risk_class"] == "LOW"
    assert data["recommended_amount"] == 200000.0
    assert len(data["execution_trace"]) > 0
    assert "proof_trees" in data


def test_validation_errors_422(client):
    # Age under 18
    res_age = client.post("/api/evaluate", json={
        "age": 16,
        "monthly_income": 50000.0,
        "existing_monthly_debt": 5000.0,
        "credit_score": 750,
        "employment_years": 2.0,
        "repayment_history": "Good",
        "requested_amount": 100000.0,
        "requested_tenure_months": 24,
    })
    assert res_age.status_code == 422
    assert "age" in res_age.text.lower()

    # Credit score > 900
    res_cs = client.post("/api/evaluate", json={
        "age": 25,
        "monthly_income": 50000.0,
        "existing_monthly_debt": 5000.0,
        "credit_score": 950,
        "employment_years": 2.0,
        "repayment_history": "Good",
        "requested_amount": 100000.0,
        "requested_tenure_months": 24,
    })
    assert res_cs.status_code == 422

    # Negative monthly income
    res_inc = client.post("/api/evaluate", json={
        "age": 25,
        "monthly_income": -1000.0,
        "existing_monthly_debt": 5000.0,
        "credit_score": 750,
        "employment_years": 2.0,
        "repayment_history": "Good",
        "requested_amount": 100000.0,
        "requested_tenure_months": 24,
    })
    assert res_inc.status_code == 422


def test_unusual_input_warning_flag(client):
    payload = {
        "age": 30,
        "monthly_income": 40000.0,
        "existing_monthly_debt": 45000.0,  # Debt > Income
        "credit_score": 700,
        "employment_years": 3.0,
        "repayment_history": "Good",
        "requested_amount": 3000000.0,  # > 50x income
        "requested_tenure_months": 36,
    }
    res = client.post("/api/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["input_warnings"]) >= 2
    assert any("exceeds total monthly income" in w for w in data["input_warnings"])


def test_list_and_detail_applications(client):
    # List applications
    res_list = client.get("/api/applications?limit=10&offset=0")
    assert res_list.status_code == 200
    data_list = res_list.json()
    assert "items" in data_list
    assert len(data_list["items"]) > 0

    app_id = data_list["items"][0]["id"]
    # Get application detail
    res_detail = client.get(f"/api/applications/{app_id}")
    assert res_detail.status_code == 200
    data_detail = res_detail.json()
    assert data_detail["application"]["id"] == app_id
    assert "decision" in data_detail
    assert len(data_detail["execution_trace"]) > 0


def test_dashboard_stats(client):
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["total_applications"] > 0
    assert "risk_distribution" in data
    assert "decision_distribution" in data


def test_ml_and_fairness_endpoints(client):
    res_ml = client.get("/api/ml/metrics")
    assert res_ml.status_code == 200
    data_ml = res_ml.json()
    assert "models" in data_ml

    res_fn = client.get("/api/fairness/report")
    assert res_fn.status_code == 200
    data_fn = res_fn.json()
    assert "systems_audit" in data_fn
    assert "recommendations" in data_fn


def test_rules_catalogue_endpoint(client):
    res = client.get("/api/rules")
    assert res.status_code == 200
    data = res.json()
    assert data["total_rules"] >= 15
    assert "thresholds" in data


def test_csv_export(client):
    res = client.get("/api/applications/export/csv")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "application_id,created_at" in res.text


def test_pdf_export(client):
    # Grab an application
    res_list = client.get("/api/applications?limit=1")
    app_id = res_list.json()["items"][0]["id"]

    res_pdf = client.get(f"/api/applications/{app_id}/pdf")
    assert res_pdf.status_code == 200
    assert res_pdf.headers["content-type"] == "application/pdf"
    # PDF starts with %PDF-
    assert res_pdf.content.startswith(b"%PDF-")
