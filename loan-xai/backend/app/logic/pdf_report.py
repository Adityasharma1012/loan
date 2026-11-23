"""Generates an institutional PDF credit decision and explainability audit memo
using ReportLab.
"""

import io
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)


def generate_credit_audit_pdf(app_dict: Dict[str, Any], dec_dict: Dict[str, Any]) -> bytes:
    """Renders a complete regulatory and explainability audit memo into PDF bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0B1B3F"),
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#475569"),
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0B1B3F"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
    )
    banner_style = ParagraphStyle(
        "BannerText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#9A3412"),
        alignment=1,
    )
    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )
    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1E293B"),
    )

    story = []

    # 1. Academic Disclaimer Top Banner
    disclaimer_text = (
        "ACADEMIC DEMONSTRATION ONLY. Rates and amounts are illustrative, not bank offers. "
        "Approval is never guaranteed. Synthetic data only."
    )
    banner_data = [[Paragraph(disclaimer_text, banner_style)]]
    banner_table = Table(banner_data, colWidths=[540])
    banner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFEDD5")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#FDBA74")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 10))

    # 2. Header
    story.append(Paragraph("CREDIT UNDERWRITING EXPLAINABILITY MEMORANDUM", title_style))
    story.append(Paragraph(
        f"Application ID: <b>{app_dict.get('id', 'N/A')}</b> | "
        f"Generated: <b>{dec_dict.get('created_at', 'N/A')}</b> | "
        f"Ruleset Version: <b>{dec_dict.get('threshold_version', '1.0.0')}</b>",
        subtitle_style
    ))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=10))

    # 3. Decision Status Callout Box
    status = dec_dict.get("decision_status", "UNKNOWN")
    bg_color = colors.HexColor("#DCFCE7") if status == "ELIGIBLE" else (
        colors.HexColor("#FEF9C3") if status == "CONDITIONALLY_ELIGIBLE" else colors.HexColor("#FEE2E2")
    )
    border_color = colors.HexColor("#22C55E") if status == "ELIGIBLE" else (
        colors.HexColor("#EAB308") if status == "CONDITIONALLY_ELIGIBLE" else colors.HexColor("#EF4444")
    )
    status_text_color = colors.HexColor("#166534") if status == "ELIGIBLE" else (
        colors.HexColor("#854D0E") if status == "CONDITIONALLY_ELIGIBLE" else colors.HexColor("#991B1B")
    )

    status_title_style = ParagraphStyle(
        "StatusTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=status_text_color,
    )
    callout_data = [
        [
            Paragraph(f"VERDICT: {status.replace('_', ' ')}", status_title_style),
            Paragraph(f"Risk Tier: <b>{dec_dict.get('risk_class', 'N/A')}</b>", body_style),
            Paragraph(f"Recommended Amount: <b>₹{dec_dict.get('recommended_amount', 0):,.2f}</b>", body_style),
            Paragraph(f"Interest Band: <b>{dec_dict.get('interest_rate_band', 'N/A')}</b>", body_style),
        ]
    ]
    callout_table = Table(callout_data, colWidths=[180, 100, 140, 120])
    callout_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # 4. Financial Profile Summary Table
    story.append(Paragraph("1. Borrower Financial & Debt Service Profile", section_heading))
    monthly_inc = app_dict.get("monthly_income", 0.0)
    existing_debt = app_dict.get("existing_monthly_debt", 0.0)
    dti = existing_debt / monthly_inc if monthly_inc > 0 else 0.0

    profile_data = [
        [
            Paragraph("<b>Verified Monthly Income:</b>", table_cell_style),
            Paragraph(f"₹{monthly_inc:,.2f}", table_cell_style),
            Paragraph("<b>Existing Monthly Debt:</b>", table_cell_style),
            Paragraph(f"₹{existing_debt:,.2f}", table_cell_style),
        ],
        [
            Paragraph("<b>Debt-to-Income (DTI):</b>", table_cell_style),
            Paragraph(f"{dti*100:.1f}%", table_cell_style),
            Paragraph("<b>Credit Bureau Score:</b>", table_cell_style),
            Paragraph(f"{app_dict.get('credit_score', 0)}", table_cell_style),
        ],
        [
            Paragraph("<b>Employment Duration:</b>", table_cell_style),
            Paragraph(f"{app_dict.get('employment_years', 0):.1f} yrs ({app_dict.get('employment_type', 'Salaried')})", table_cell_style),
            Paragraph("<b>Repayment History:</b>", table_cell_style),
            Paragraph(f"{app_dict.get('repayment_history', 'N/A')} (Default: {app_dict.get('recent_default', False)})", table_cell_style),
        ],
        [
            Paragraph("<b>Requested Principal:</b>", table_cell_style),
            Paragraph(f"₹{app_dict.get('requested_amount', 0):,.2f}", table_cell_style),
            Paragraph("<b>Requested Tenure:</b>", table_cell_style),
            Paragraph(f"{app_dict.get('requested_tenure_months', 0)} months", table_cell_style),
        ],
        [
            Paragraph("<b>Max Affordable EMI:</b>", table_cell_style),
            Paragraph(f"₹{dec_dict.get('max_affordable_emi', 0):,.2f}", table_cell_style),
            Paragraph("<b>Supportable Principal:</b>", table_cell_style),
            Paragraph(f"₹{dec_dict.get('supportable_principal', 0):,.2f}", table_cell_style),
        ],
    ]
    t_profile = Table(profile_data, colWidths=[135, 135, 135, 135])
    t_profile.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 10))

    # 5. Plain English Rationale & Conditions / Reasons
    story.append(Paragraph("2. Decision Rationale & Adverse Action Analysis", section_heading))
    story.append(Paragraph(f"<b>Summary:</b> {dec_dict.get('rationale_summary', 'N/A')}", body_style))
    story.append(Spacer(1, 4))

    reasons = dec_dict.get("rejection_reasons", [])
    if reasons:
        story.append(Paragraph("<b>Adverse Action Grounds:</b>", body_style))
        for r in reasons:
            story.append(Paragraph(f"• {r}", body_style))
        story.append(Spacer(1, 4))

    conditions = dec_dict.get("conditions", [])
    if conditions:
        story.append(Paragraph("<b>Underwriting Stipulations & Covenants:</b>", body_style))
        for c in conditions:
            story.append(Paragraph(f"• {c}", body_style))
        story.append(Spacer(1, 4))

    # 6. Counterfactual Hints Table
    hints = dec_dict.get("counterfactual_hints", [])
    if hints:
        story.append(Spacer(1, 4))
        story.append(Paragraph("3. Counterfactual Explainability (Pathways to Approval)", section_heading))
        cf_rows = [[
            Paragraph("Underwriting Metric", table_header_style),
            Paragraph("Current Value", table_header_style),
            Paragraph("Target Benchmark", table_header_style),
            Paragraph("Prescribed Counterfactual Adjustment", table_header_style),
        ]]
        for h in hints:
            cf_rows.append([
                Paragraph(str(h.get("feature", "")).replace("_", " ").title(), table_cell_style),
                Paragraph(str(h.get("current_value", "")), table_cell_style),
                Paragraph(str(h.get("target_value", "")), table_cell_style),
                Paragraph(str(h.get("delta_description", "")), table_cell_style),
            ])
        t_cf = Table(cf_rows, colWidths=[110, 90, 90, 250])
        t_cf.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B3F")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t_cf)

    # 7. Step-by-Step Production Rule Execution Trace
    exec_trace = dec_dict.get("rule_executions", [])
    if exec_trace:
        story.append(Spacer(1, 8))
        story.append(Paragraph("4. Complete Production Rule Execution Trace (Inference Proof)", section_heading))
        trace_rows = [[
            Paragraph("Step", table_header_style),
            Paragraph("Rule ID & Name", table_header_style),
            Paragraph("First-Order Logic Horn Clause", table_header_style),
            Paragraph("Plain-English Rationale", table_header_style),
        ]]
        for step in exec_trace:
            trace_rows.append([
                Paragraph(str(step.get("step_number", "")), table_cell_style),
                Paragraph(f"<b>{step.get('rule_id')}</b><br/>{step.get('rule_name')}", table_cell_style),
                Paragraph(f"<code>{step.get('fol_form', '')}</code>", table_cell_style),
                Paragraph(str(step.get("plain_english", "")), table_cell_style),
            ])
        t_trace = Table(trace_rows, colWidths=[35, 125, 200, 180])
        t_trace.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t_trace)

    # Build document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
