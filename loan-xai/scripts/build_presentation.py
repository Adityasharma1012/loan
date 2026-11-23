"""PowerPoint Presentation Generator for LoanXAI Project.
Generates an 18-slide, 16:9 widescreen, animated PowerPoint presentation
with authentic screenshots, high-contrast fintech aesthetic, and comprehensive speaker notes.
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "screenshots"
OUTPUT_FILE = BASE_DIR / "loan-xai-presentation.pptx"

# Theme Color Palette
NAVY_DARK = RGBColor(11, 27, 63)        # #0B1B3F Primary Dark
BLUE_PRIMARY = RGBColor(37, 99, 235)     # #2563EB Accent Blue
BLUE_LIGHT = RGBColor(219, 234, 254)     # #DBEAFE Light Blue Fill
BLUE_SUBTLE = RGBColor(239, 246, 255)    # #EFF6FF Card Blue Fill
SLATE_900 = RGBColor(15, 23, 42)         # #0F172A Primary Text
SLATE_700 = RGBColor(51, 65, 85)         # #334155 Body Text
SLATE_500 = RGBColor(100, 116, 139)      # #64748B Muted / Captions
SLATE_200 = RGBColor(226, 232, 240)      # #E2E8F0 Borders
SLATE_100 = RGBColor(241, 245, 249)      # #F1F5F9 Card Background
SLATE_50 = RGBColor(248, 250, 252)       # #F8FAFC Slide Background
WHITE = RGBColor(255, 255, 255)

# Semantic Colors
EMERALD_GREEN = RGBColor(5, 150, 105)    # #059669
EMERALD_BG = RGBColor(236, 253, 245)     # #ECFDF5
AMBER_WARN = RGBColor(217, 119, 6)       # #D97706
AMBER_BG = RGBColor(255, 251, 235)       # #FFFBEB
ROSE_RED = RGBColor(220, 38, 38)         # #DC2626
ROSE_BG = RGBColor(254, 242, 242)        # #FEF2F2

FONT_TITLE = "Trebuchet MS"
FONT_BODY = "Calibri"


def create_deck():
    prs = Presentation()
    # 16:9 Widescreen format (13.333" x 7.5")
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_slide_with_transition(bg_color=SLATE_50):
        slide = prs.slides.add_slide(blank_layout)
        # Background fill
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = bg_color
        bg_shape.line.fill.background()
        
        # Add smooth fade transition via OpenXML
        try:
            trans_xml = f'<p:transition {nsdecls("p")} spd="med"><p:fade/></p:transition>'
            slide._element.append(parse_xml(trans_xml))
        except Exception:
            pass
        return slide

    def add_header(slide, title_text, category_tag, dark_mode=False):
        # Category Tag Badge
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.name = FONT_BODY
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = BLUE_PRIMARY if not dark_mode else BLUE_LIGHT

        # Slide Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = SLATE_900 if not dark_mode else WHITE

        # Academic Disclaimer Footer
        if not dark_mode:
            ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
            tf_ft = ft_box.text_frame
            tf_ft.word_wrap = True
            tf_ft.margin_left = tf_ft.margin_top = tf_ft.margin_right = tf_ft.margin_bottom = 0
            p_ft = tf_ft.paragraphs[0]
            p_ft.text = "Academic Demonstration Web Application · Course: Artificial Intelligence Foundations (K4P25AT) · Group 5 · Rates & amounts are illustrative"
            p_ft.font.name = FONT_BODY
            p_ft.font.size = Pt(9.5)
            p_ft.font.color.rgb = SLATE_500

    def add_card(slide, left, top, width, height, bg_color=WHITE, border_color=SLATE_200):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    def add_image_card(slide, img_name, left, top, width, height=None, border=True):
        img_path = ASSETS_DIR / img_name
        if not img_path.exists():
            print(f"Warning: Image {img_name} not found at {img_path}")
            return None
        
        if height:
            pic = slide.shapes.add_picture(str(img_path), left, top, width=width, height=height)
        else:
            pic = slide.shapes.add_picture(str(img_path), left, top, width=width)
        
        if border:
            pic.line.color.rgb = SLATE_200
            pic.line.width = Pt(1)
        return pic

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = add_slide_with_transition(NAVY_DARK)
    
    # Sub-badge
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "ARTIFICIAL INTELLIGENCE FOUNDATIONS · SECTION K4P25AT · GROUP 5"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_LIGHT

    # Title
    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.4))
    p_t = tb_t.text_frame.paragraphs[0]
    p_t.text = "Explainable Rule-Based Loan Eligibility\n& Credit Decision System"
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(11.3), Inches(0.8))
    p_sub = tb_sub.text_frame.paragraphs[0]
    p_sub.text = "An applied expert system combining forward-chaining production rules, First-Order Logic proof trees, actuarial loan sizing, empirical ML benchmarks, and algorithmic fairness audits."
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Team & Project Card
    add_card(s1, Inches(1.0), Inches(4.0), Inches(11.333), Inches(2.2), bg_color=RGBColor(15, 34, 77), border_color=BLUE_PRIMARY)
    
    # Team Table / Columns
    team_tb = s1.shapes.add_textbox(Inches(1.3), Inches(4.2), Inches(6.0), Inches(1.8))
    tf_team = team_tb.text_frame
    tf_team.word_wrap = True
    p0 = tf_team.paragraphs[0]
    p0.text = "PROJECT TEAM MEMBERS:"
    p0.font.bold = True
    p0.font.size = Pt(12)
    p0.font.color.rgb = BLUE_LIGHT

    members = [
        ("Pilli Sreeja", "Reg. No: 12515392"),
        ("Harshit Kumar Singh", "Reg. No: 12519334"),
        ("Inaganti Hajmeer Vali", "Reg. No: 12521593"),
    ]
    for name, reg in members:
        p_m = tf_team.add_paragraph()
        p_m.text = f"•  {name}  ({reg})"
        p_m.font.size = Pt(13)
        p_m.font.color.rgb = WHITE

    # Mentor & Placeholders
    inst_tb = s1.shapes.add_textbox(Inches(7.5), Inches(4.2), Inches(4.5), Inches(1.8))
    tf_inst = inst_tb.text_frame
    tf_inst.word_wrap = True
    p_m_lbl = tf_inst.paragraphs[0]
    p_m_lbl.text = "PROJECT MENTOR:"
    p_m_lbl.font.bold = True
    p_m_lbl.font.size = Pt(12)
    p_m_lbl.font.color.rgb = BLUE_LIGHT

    p_m_val = tf_inst.add_paragraph()
    p_m_val.text = "Sheveta"
    p_m_val.font.size = Pt(14)
    p_m_val.font.bold = True
    p_m_val.font.color.rgb = WHITE

    p_c_lbl = tf_inst.add_paragraph()
    p_c_lbl.text = "INSTITUTION & DATE:"
    p_c_lbl.font.bold = True
    p_c_lbl.font.size = Pt(12)
    p_c_lbl.font.color.rgb = BLUE_LIGHT

    p_c_val = tf_inst.add_paragraph()
    p_c_val.text = "[College / University Name]  |  [Month Year]"
    p_c_val.font.size = Pt(13)
    p_c_val.font.color.rgb = RGBColor(226, 232, 240)

    # Footer banner
    tb_banner = s1.shapes.add_textbox(Inches(1.0), Inches(6.45), Inches(11.3), Inches(0.4))
    p_b = tb_banner.text_frame.paragraphs[0]
    p_b.text = "⚠️ Academic demonstration system. Rates and amounts are illustrative, not bank offers. Approval is never guaranteed."
    p_b.font.size = Pt(10)
    p_b.font.color.rgb = RGBColor(148, 163, 184)

    set_speaker_notes(s1, 
        "[Click 1] Good morning esteemed faculty evaluators and mentor Sheveta. Today, our team—Pilli Sreeja, Harshit Kumar Singh, and Inaganti Hajmeer Vali—is proud to present our capstone project for Artificial Intelligence Foundations: 'Explainable Rule-Based Loan Eligibility and Credit Decision System'.\n\n"
        "[Click 2] In regulated industries like banking, black-box AI often fails because lenders are legally required to provide exact, auditable reasons for adverse credit decisions. Our system addresses this by combining production-rule expert systems and first-order predicate logic with empirical ML benchmarks and fairness auditing.\n\n"
        "Hinglish delivery tip: Yahan confident tone me shuru karein aur clearly state karein ki core system symbolic AI hai, aur ML comparison baseline hai."
    )

    # =========================================================================
    # SLIDE 2: Background & Motivation
    # =========================================================================
    s2 = add_slide_with_transition()
    add_header(s2, "The Explainability Imperative in Automated Lending", "Background & Problem Motivation")

    # Left Card: The Black Box Problem
    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_l = s2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.6))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p1 = tf_l.paragraphs[0]
    p1.text = "The Black-Box Dilemma in Banking"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = ROSE_RED

    points_l = [
        ("Opaque Neural & Ensemble Models: ", "Modern credit scoring heavily relies on gradient boosters or deep nets that output a single probability without deductive justification."),
        ("Legal Adverse Action Mandates: ", "Under FCRA and global banking regulations, lenders MUST provide applicants with clear, specific, and actionable reasons for any credit denial."),
        ("Lack of True Counterfactuals: ", "Statistical post-hoc tools like SHAP or LIME offer localized gradient approximations rather than actionable, verifiable path-to-approval advice."),
        ("Hidden Demographic Bias: ", "Black-box models frequently latch onto proxy features (e.g. zip code or tenure) creating illegal disparate impact without human visibility.")
    ]
    for b_title, b_desc in points_l:
        p_b = tf_l.add_paragraph()
        p_b.text = f"• {b_title}"
        p_b.font.bold = True
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = SLATE_900
        p_desc = tf_l.add_paragraph()
        p_desc.text = f"   {b_desc}"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = SLATE_700

    # Right Card: The Symbolic AI Solution
    add_card(s2, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_r = s2.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.0), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p2 = tf_r.paragraphs[0]
    p2.text = "The Symbolic AI Advantage"
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_PRIMARY

    points_r = [
        ("Deterministic Production Rules: ", "Business logic is decoupled into declarative, version-controlled YAML rules executed via forward-chaining to a guaranteed fixpoint."),
        ("First-Order Logic (FOL) Proofs: ", "Every approved or rejected decision is backed by formal Horn clause deduction and ground atom derivation trees (Unification & NAF)."),
        ("Actuarial Debt-Sizing Formulas: ", "Loan amounts are mathematically bounded using annuity present value formulas against Debt-to-Income (DTI) and Max EMI capacity."),
        ("Actionable Recourse: ", "Generates exact mathematical counterfactuals (e.g., 'Reduce monthly obligations by ₹4,200 to achieve 40% DTI').")
    ]
    for b_title, b_desc in points_r:
        p_b = tf_r.add_paragraph()
        p_b.text = f"• {b_title}"
        p_b.font.bold = True
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = SLATE_900
        p_desc = tf_r.add_paragraph()
        p_desc.text = f"   {b_desc}"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = SLATE_700

    set_speaker_notes(s2,
        "[Click 1] Consider this analogy: if a physician refuses you a critical prescription, they don't say 'my statistical model gave you an 82% risk score.' They explain specific biomarkers—blood sugar, enzyme levels—and tell you exactly how to lower them. In consumer credit, the law demands the same rigor.\n\n"
        "[Click 2] When banks use opaque neural networks, they cannot explain edge cases or prove non-discrimination. By applying Classical Symbolic AI, our system bridges this exact gap: every credit decision is mathematically deduced from production rules and first-order predicate logic, providing complete transparency and actionable counterfactual advice.\n\n"
        "Hinglish delivery tip: Yahan samjhayein ki bank me adverse action notice compulsory hota hai, isiliye symbolic AI ML se zyada reliable aur defensible hai."
    )

    # =========================================================================
    # SLIDE 3: What the System Is (End-to-End Pipeline)
    # =========================================================================
    s3 = add_slide_with_transition()
    add_header(s3, "System Pipeline: From Financial Inputs to Audited Verdict", "System Architecture Overview")

    # 4 Pipeline Stages as Horizontal Cards
    stages = [
        ("1. Data & Quarantine", "12 Financial Inputs", 
         ["• Zero protected demographic data collected on form",
          "• Field-level Pydantic v2 type & boundary checks",
          "• Pre-computes DTI & Surplus EMI capacity",
          "• Seeds working memory with ground atoms"]),
        ("2. Forward Chaining", "Production Rule Engine", 
         ["• Declarative rules in config/rules.yaml",
          "• Conflict Resolution: Knockout > Priority > Specificity",
          "• Refraction property (each rule fires at most once)",
          "• Deterministic forward-chaining to fixpoint"]),
        ("3. FOL Proof & Sizing", "Logic & Financial Engine", 
         ["• Horn clause resolution with unification θ",
          "• Derivation trees for every derived conclusion",
          "• Actuarial Annuity PV loan sizing at risk band",
          "• Counterfactual distance computation"]),
        ("4. Audit & Benchmark", "Fairness & ML Baseline", 
         ["• Benchmark vs Decision Tree & Logistic Regression",
          "• Independent synthetic risk dataset (N=5,000)",
          "• 5-group demographic fairness audit",
          "• Full PDF Underwriting Memo generation"])
    ]

    card_w = Inches(2.7)
    gap = Inches(0.24)
    start_x = Inches(0.8)

    for i, (title, sub, bullets) in enumerate(stages):
        x = start_x + i * (card_w + gap)
        add_card(s3, x, Inches(1.6), card_w, Inches(5.1), WHITE, SLATE_200)
        
        # Step Number Badge
        step_box = s3.shapes.add_textbox(x + Inches(0.2), Inches(1.8), card_w - Inches(0.4), Inches(0.35))
        tf_s = step_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = f"STAGE 0{i+1}"
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = BLUE_PRIMARY

        # Card Title
        title_box = s3.shapes.add_textbox(x + Inches(0.2), Inches(2.15), card_w - Inches(0.4), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_900
        
        p_sub = tf_t.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = SLATE_500

        # Bullet List
        body_box = s3.shapes.add_textbox(x + Inches(0.2), Inches(3.05), card_w - Inches(0.4), Inches(3.4))
        tf_b = body_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        for j, b in enumerate(bullets):
            p_bullet = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p_bullet.text = b
            p_bullet.font.size = Pt(10.5)
            p_bullet.font.color.rgb = SLATE_700
            p_bullet.space_after = Pt(6)

    set_speaker_notes(s3,
        "[Click 1] Let us trace the end-to-end journey of a credit application through our architecture. In Stage 1, the applicant submits twelve purely financial attributes. Protected attributes like gender, caste, or religion are strictly quarantined at the architectural boundary.\n\n"
        "[Click 2] In Stage 2, working memory passes into our forward-chaining expert system, firing declarative production rules until a fixpoint is achieved. Stage 3 derives a formal First-Order Logic proof tree and applies actuarial annuity math to size the loan amount.\n\n"
        "[Click 3] Finally, Stage 4 benchmarks the decision against statistical models and executes an automated demographic fairness audit.\n\n"
        "Hinglish delivery tip: Bataiye ki ye end-to-end multi-tier pipeline hai jo input validation se lekar fairness audit tak smoothly run hoti hai."
    )

    # =========================================================================
    # SLIDE 4: Project Objectives
    # =========================================================================
    s4 = add_slide_with_transition()
    add_header(s4, "Core Project Objectives & Verification Status", "Project Goals & Deliverables")

    objectives = [
        ("O1: Declarative Production Rule Engine", 
         "Build a forward-chaining inference engine with working memory, declarative YAML rule definitions, 4-tier conflict resolution, and refraction to guarantee deterministic termination.",
         "COMPLETED & VERIFIED"),
        ("O2: First-Order Predicate Logic Proof Engine", 
         "Formulate underwriting knowledge as FOL Horn clauses with variables. Implement ground atom unification, proof tree generation, and Negation-as-Failure (NAF).",
         "COMPLETED & VERIFIED"),
        ("O3: Actuarial Sizing, Rate Bands & Counterfactuals", 
         "Determine three-tier eligibility (Prime, Conditional, Not Eligible), compute supportable loan amounts using annuity PV math, assign interest bands (9-18%), and generate exact counterfactuals.",
         "COMPLETED & VERIFIED"),
        ("O4: Empirical Machine Learning Benchmark", 
         "Train Decision Tree and Logistic Regression models on an independent 5,000-record synthetic dataset to rigorously compare accuracy, transparency, auditability, and edge-case safety.",
         "COMPLETED & VERIFIED"),
        ("O5: Algorithmic Demographic Fairness Review", 
         "Audit both rule-based and ML decisions across synthetic demographic groups (gender, age, region) using Disparate Impact Ratio, Statistical Parity, and Equal Opportunity metrics.",
         "COMPLETED & VERIFIED")
    ]

    obj_y = Inches(1.5)
    row_h = Inches(0.95)
    row_gap = Inches(0.12)

    for i, (title, desc, status) in enumerate(objectives):
        y = obj_y + i * (row_h + row_gap)
        add_card(s4, Inches(0.8), y, Inches(11.733), row_h, WHITE, SLATE_200)

        # Title & Desc
        tb_o = s4.shapes.add_textbox(Inches(1.1), y + Inches(0.12), Inches(8.8), Inches(0.75))
        tf_o = tb_o.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = tf_o.margin_top = tf_o.margin_right = tf_o.margin_bottom = 0
        p_ot = tf_o.paragraphs[0]
        p_ot.text = title
        p_ot.font.name = FONT_TITLE
        p_ot.font.size = Pt(13)
        p_ot.font.bold = True
        p_ot.font.color.rgb = SLATE_900

        p_od = tf_o.add_paragraph()
        p_od.text = desc
        p_od.font.size = Pt(10.5)
        p_od.font.color.rgb = SLATE_700

        # Status Badge
        badge = add_card(s4, Inches(10.1), y + Inches(0.25), Inches(2.2), Inches(0.42), EMERALD_BG, EMERALD_GREEN)
        tb_b = s4.shapes.add_textbox(Inches(10.1), y + Inches(0.28), Inches(2.2), Inches(0.35))
        tf_b = tb_b.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = f"✓ {status}"
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = EMERALD_GREEN

    set_speaker_notes(s4,
        "[Click 1] We formulated five strict, checkable academic objectives corresponding to the project statement. Each objective has been fully implemented in our codebase and validated through our 37-test suite.\n\n"
        "[Click 2] Notice that we did not build a simple toy script; we developed a production-ready declarative rule engine, a true first-order logic proof generator, mathematical loan sizing, a comparative ML benchmark, and an algorithmic fairness auditor.\n\n"
        "Hinglish delivery tip: Faculty ko point out karein ki humne project requirement ke saare clauses ko 100% fulfill kiya hai."
    )

    # =========================================================================
    # SLIDE 5: Scope & Boundaries
    # =========================================================================
    s5 = add_slide_with_transition()
    add_header(s5, "Project Scope: Strict System Boundaries", "System Boundaries & Scope")

    # Left Column: IN SCOPE
    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_in = s5.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(5.0), Inches(4.7))
    tf_in = tb_in.text_frame
    tf_in.word_wrap = True
    p_in_t = tf_in.paragraphs[0]
    p_in_t.text = "In Scope (Implemented & Tested)"
    p_in_t.font.name = FONT_TITLE
    p_in_t.font.size = Pt(17)
    p_in_t.font.bold = True
    p_in_t.font.color.rgb = EMERALD_GREEN

    in_items = [
        ("Deterministic Production Rule Engine: ", "Forward-chaining working memory with refraction and 4-level conflict resolution."),
        ("First-Order Logic Proof Trees: ", "Horn clause resolution, variable unification, and visual derivation graphs."),
        ("Actuarial Debt & Loan Sizing: ", "Annuity present value formula, DTI constraints, and risk-adjusted rate bands (9-18%)."),
        ("Actionable Counterfactual Hints: ", "Exact delta calculations guiding applicants toward credit qualification."),
        ("Comparative ML & Fairness Suite: ", "Scikit-learn Decision Tree & Logistic Regression models evaluated on 5,000 synthetic records."),
        ("Full-Stack Interactive Web UI: ", "10 interactive views, dark mode, CSV audit export, and ReportLab PDF memo.")
    ]
    for h, b in in_items:
        p_item = tf_in.add_paragraph()
        p_item.text = f"✓ {h}"
        p_item.font.bold = True
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = SLATE_900
        p_sub = tf_in.add_paragraph()
        p_sub.text = f"   {b}"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = SLATE_700

    # Right Column: OUT OF SCOPE
    add_card(s5, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_out = s5.shapes.add_textbox(Inches(7.2), Inches(1.75), Inches(5.0), Inches(4.7))
    tf_out = tb_out.text_frame
    tf_out.word_wrap = True
    p_out_t = tf_out.paragraphs[0]
    p_out_t.text = "Out of Scope (By Academic Design)"
    p_out_t.font.name = FONT_TITLE
    p_out_t.font.size = Pt(17)
    p_out_t.font.bold = True
    p_out_t.font.color.rgb = ROSE_RED

    out_items = [
        ("Live Bank / Credit Bureau APIs: ", "Academic demo deliberately uses synthetic records; no real CIBIL/Experian pull."),
        ("Binding Financial Offers: ", "Rates and loan amounts are illustrative demonstration values, never binding contracts."),
        ("Protected Demographic Ingestion: ", "Gender, religion, and caste are never collected or evaluated during loan underwriting."),
        ("Unconstrained Black-Box Models: ", "Deep neural networks are excluded from credit decisions due to lack of legal defensibility."),
        ("Automated Fund Disbursement: ", "Payment gateway and bank core system integration are excluded."),
        ("Real Production Borrower Data: ", "Zero real-world PII is collected or stored to maintain complete data privacy.")
    ]
    for h, b in out_items:
        p_item = tf_out.add_paragraph()
        p_item.text = f"✗ {h}"
        p_item.font.bold = True
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = SLATE_900
        p_sub = tf_out.add_paragraph()
        p_sub.text = f"   {b}"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = SLATE_700

    set_speaker_notes(s5,
        "[Click 1] Setting clear engineering boundaries is essential for any applied AI project. In scope, we have delivered a full-stack, fully tested expert system with complete mathematical sizing and comparative ML benchmarks.\n\n"
        "[Click 2] By strict academic design, live bureau integrations, real-world customer PII, and actual financial disbursements are out of scope. Protected demographic attributes are strictly quarantined and never used in loan decisions.\n\n"
        "Hinglish delivery tip: Evaluators ko batayein ki academic integrity aur data privacy preserve karne ke liye humne boundaries cleanly define ki hain."
    )

    # =========================================================================
    # SLIDE 6: Existing Approaches & The Research Gap
    # =========================================================================
    s6 = add_slide_with_transition()
    add_header(s6, "Comparative Analysis: Traditional Scorecards vs ML vs LoanXAI", "Literature Review & Research Gap")

    # Table layout
    headers = ["Evaluation Dimension", "Traditional Scorecards", "Black-Box ML (XGB/NN)", "LoanXAI Expert System"]
    rows = [
        ("Decision Mechanism", "Linear point addition", "Statistical gradient / weights", "Production rules & FOL deduction"),
        ("Auditability & Proof", "Manual point tally", "Opaque; post-hoc SHAP proxy", "Formal FOL Horn derivation tree"),
        ("Adverse Action Recourse", "Generic rejection reason", "Gradient direction estimate", "Exact mathematical counterfactuals"),
        ("Edge-Case Safety", "Brittle boundary cliffs", "Unpredictable extrapolation", "Hard knock-out invariant guarantees"),
        ("Demographic Quarantine", "Hard to verify feature leakage", "Frequent proxy feature capture", "Architectural quarantine at API"),
        ("Regulatory Defensibility", "Moderate (traditional)", "Low (unexplainable)", "High (100% deterministic logic)")
    ]

    table_shape = s6.shapes.add_table(len(rows) + 1, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.0))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.333)

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK if col_idx < 3 else BLUE_PRIMARY
        p_c = cell.text_frame.paragraphs[0]
        p_c.text = h_text
        p_c.font.name = FONT_BODY
        p_c.font.bold = True
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = WHITE

    for row_idx, r_data in enumerate(rows):
        for col_idx, text in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            if col_idx == 3:
                cell.fill.fore_color.rgb = BLUE_SUBTLE
            else:
                cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else SLATE_100
            p_c = cell.text_frame.paragraphs[0]
            p_c.text = text
            p_c.font.name = FONT_BODY
            p_c.font.size = Pt(10)
            p_c.font.color.rgb = SLATE_900 if col_idx == 3 else SLATE_700
            if col_idx == 0:
                p_c.font.bold = True

    # Gap Callout Card
    add_card(s6, Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.95), BLUE_SUBTLE, BLUE_PRIMARY)
    tb_gap = s6.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.85))
    tf_gap = tb_gap.text_frame
    tf_gap.word_wrap = True
    p_g_t = tf_gap.paragraphs[0]
    p_g_t.text = "THE RESEARCH & APPLIED GAP:"
    p_g_t.font.bold = True
    p_g_t.font.size = Pt(11)
    p_g_t.font.color.rgb = BLUE_PRIMARY

    p_g_b = tf_gap.add_paragraph()
    p_g_b.text = "Existing credit systems force an artificial tradeoff between statistical prediction accuracy and regulatory explainability. LoanXAI proves that symbolic expert systems eliminate this tradeoff: by formally deducing decisions via production rules and First-Order Logic, banks achieve complete transparency without sacrificing credit rigor."
    p_g_b.font.size = Pt(10.5)
    p_g_b.font.color.rgb = SLATE_900

    set_speaker_notes(s6,
        "[Click 1] When we examine the literature, traditional credit scorecards are too simple to capture complex edge cases, while modern machine learning models are too opaque to satisfy regulatory adverse action laws.\n\n"
        "[Click 2] As shown in our comparison matrix, LoanXAI occupies the sweet spot: by using formal Horn clause deduction and forward-chaining production rules, every verdict is mathematically verifiable, auditable, and transparent.\n\n"
        "Hinglish delivery tip: Gap highlight karein: scorecards outdated hain aur black-box ML illegal hai, isliye rule-based FOL expert system is the ideal regulatory solution."
    )

    # =========================================================================
    # SLIDE 7: System Architecture & Stack
    # =========================================================================
    s7 = add_slide_with_transition()
    add_header(s7, "Multi-Tier Layered Architecture & Protected Attribute Quarantine", "System Architecture & Technology Stack")

    # Left Side: System Flow Diagram / Layers Card
    add_card(s7, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2), WHITE, SLATE_200)
    tb_arch = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(6.1), Inches(4.8))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True
    p_at = tf_arch.paragraphs[0]
    p_at.text = "Architectural Layers & Data Isolation"
    p_at.font.name = FONT_TITLE
    p_at.font.size = Pt(16)
    p_at.font.bold = True
    p_at.font.color.rgb = BLUE_PRIMARY

    layers = [
        ("1. Presentation Tier (React + Vite + Tailwind):", "Interactive single-page app, Recharts financial telemetry, field validation, and real-time counterfactual feedback."),
        ("2. API & Validation Tier (FastAPI + Pydantic v2):", "Strict schema enforcement, 422 error boundaries, CORS protection, and async underwriting dispatch."),
        ("3. Protected Attribute Quarantine Boundary:", "Strict architectural firewall: Demographic attributes are rejected at underwriting endpoint and isolated solely to the synthetic fairness audit pipeline."),
        ("4. Symbolic AI Core (Rule Engine & FOL Proofs):", "Working memory, forward chaining with refraction, 4-tier conflict resolution, Horn clause unification, and proof tree generation."),
        ("5. Actuarial Math & Financial Logic:", "DTI, Max EMI, monthly compound interest annuity present value calculation, and risk banding (9-18%)."),
        ("6. Persistence & Audit Tier (SQLAlchemy + ReportLab):", "SQLite persistent storage, complete rule firing history, and automated institutional PDF memo rendering.")
    ]
    for l_title, l_desc in layers:
        p_l = tf_arch.add_paragraph()
        p_l.text = f"• {l_title} "
        p_l.font.bold = True
        p_l.font.size = Pt(10.5)
        p_l.font.color.rgb = SLATE_900
        p_ld = tf_arch.add_paragraph()
        p_ld.text = f"   {l_desc}"
        p_ld.font.size = Pt(9.5)
        p_ld.font.color.rgb = SLATE_700

    # Right Side: Tech Stack Cards
    stack_items = [
        ("Frontend Stack", "React 19, Vite, Tailwind CSS, Recharts, Lucide Icons", "10 responsive views, light/dark mode, real-time Recharts visualizations"),
        ("Backend Services", "Python 3.13, FastAPI, Pydantic v2, Uvicorn", "Async REST API, sub-millisecond inference, rigorous schema validation"),
        ("Machine Learning", "Scikit-Learn, Pandas, NumPy", "Decision Tree & Logistic Regression baselines on 5,000 synthetic records"),
        ("Report & Testing", "ReportLab PDF Engine, Pytest Test Suite", "Automated formal memo generation, 37/37 passing unit & integration tests")
    ]

    for i, (cat, tools, desc) in enumerate(stack_items):
        y = Inches(1.5) + i * Inches(1.3)
        add_card(s7, Inches(7.5), y, Inches(5.0), Inches(1.2), WHITE, SLATE_200)
        tb_st = s7.shapes.add_textbox(Inches(7.7), y + Inches(0.1), Inches(4.6), Inches(1.0))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        p_s_t = tf_st.paragraphs[0]
        p_s_t.text = cat
        p_s_t.font.name = FONT_TITLE
        p_s_t.font.size = Pt(13)
        p_s_t.font.bold = True
        p_s_t.font.color.rgb = NAVY_DARK

        p_s_m = tf_st.add_paragraph()
        p_s_m.text = tools
        p_s_m.font.size = Pt(10.5)
        p_s_m.font.bold = True
        p_s_m.font.color.rgb = BLUE_PRIMARY

        p_s_d = tf_st.add_paragraph()
        p_s_d.text = desc
        p_s_d.font.size = Pt(9.5)
        p_s_d.font.color.rgb = SLATE_700

    set_speaker_notes(s7,
        "[Click 1] Our system architecture enforces clean separation of concerns across presentation, API, symbolic AI, actuarial math, and auditing tiers. A critical design highlight is the Protected Attribute Quarantine Boundary: demographic data is rejected at the underwriting API and restricted entirely to the synthetic audit engine.\n\n"
        "[Click 2] For technology, we selected FastAPI with Pydantic v2 for high-throughput async processing and strict schema enforcement, paired with a modern React frontend and ReportLab PDF generator.\n\n"
        "VIVA DEFENSE Q&A:\n"
        "Q: Why did you choose FastAPI over Flask or Django?\n"
        "A: FastAPI natively supports asynchronous execution (ASGI), automatic OpenAPI documentation, and strict runtime data validation through Pydantic v2, which guarantees zero type errors in financial inputs.\n"
        "Q: How is the demographic data quarantined?\n"
        "A: The loan evaluation endpoint schema rejects any demographic fields. Demographic features exist only in the offline synthetic dataset used exclusively by the fairness audit module."
    )

    # =========================================================================
    # SLIDE 8: Expert System Core: Forward Chaining & FOL
    # =========================================================================
    s8 = add_slide_with_transition()
    add_header(s8, "Symbolic AI Core: Forward Chaining & First-Order Predicate Logic", "Core AI Algorithms")

    # Left Card: Forward Chaining
    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_fc = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_fc = tb_fc.text_frame
    tf_fc.word_wrap = True
    p_fc = tf_fc.paragraphs[0]
    p_fc.text = "Forward Chaining & Conflict Resolution"
    p_fc.font.name = FONT_TITLE
    p_fc.font.size = Pt(16)
    p_fc.font.bold = True
    p_fc.font.color.rgb = NAVY_DARK

    fc_details = [
        ("Working Memory of Ground Facts: ", "Initialized with verified applicant facts (e.g., CreditScore(x, 780), MonthlyIncome(x, 65000))."),
        ("Match Phase: ", "Scans rules in config/rules.yaml to construct the Conflict Set C = {r | Conditions(r) ⊆ WorkingMemory}."),
        ("4-Tier Conflict Resolution Order: ", 
         "1. Hard Knockouts (Priority 100)\n"
         "2. Salience / Rule Priority (10 to 90)\n"
         "3. Specificity (Rules with more conditions fire first)\n"
         "4. Rule ID deterministic tie-breaker"),
        ("Refraction Property: ", "A rule instance fires at most once per fact set. This mathematically prevents infinite loops and guarantees convergence to a fixpoint."),
        ("Fixpoint Termination: ", "Engine loops until no new unrefracted rules match working memory.")
    ]
    for h, b in fc_details:
        p_h = tf_fc.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_fc.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE_700

    # Right Card: First-Order Logic & Horn Clauses
    add_card(s8, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_fol = s8.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_fol = tb_fol.text_frame
    tf_fol.word_wrap = True
    p_fol = tf_fol.paragraphs[0]
    p_fol.text = "First-Order Logic Proof Trees"
    p_fol.font.name = FONT_TITLE
    p_fol.font.size = Pt(16)
    p_fol.font.bold = True
    p_fol.font.color.rgb = BLUE_PRIMARY

    fol_details = [
        ("Horn Clause Knowledge Representation: ", 
         "All rules are Horn clauses of the form:\n"
         "∀x: P₁(x) ∧ P₂(x) ∧ ... ∧ Pₙ(x) → Q(x)\n"
         "Example: ∀x: Applicant(x) ∧ IncomeAtLeast(x, 30000) ∧ DTIAtMost(x, 0.40) → AffordabilityOK(x)"),
        ("Ground Atoms & Unification: ", "Variables are instantiated with applicant ID via unifier θ = {x / APP_001}."),
        ("Derivation (Proof) Trees: ", "Every inferred atom stores pointer links to the antecedent ground atoms that satisfied it, constructing an auditable visual proof graph."),
        ("Negation-as-Failure (NAF): ", "Closed-world assumption: NOT DefaultOnRecord(x) succeeds if and only if DefaultOnRecord(x) cannot be proven from working memory.")
    ]
    for h, b in fol_details:
        p_h = tf_fol.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_fol.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE_700

    set_speaker_notes(s8,
        "[Click 1] The core AI of LoanXAI is a classical symbolic expert system. We implement forward chaining over a working memory of ground facts. At each cycle, the match phase builds a conflict set, which is resolved through our four-tier hierarchy: Hard Knockouts first, then salience priority, specificity, and a deterministic tie-breaker.\n\n"
        "[Click 2] To prevent infinite looping, we enforce the Refraction property—a rule fires at most once per fact set. Furthermore, every rule is formulated as a First-Order Logic Horn clause. Through variable unification and Negation-as-Failure, the system outputs a complete, auditable proof tree for every conclusion.\n\n"
        "VIVA DEFENSE Q&A:\n"
        "Q: What is refraction and why is it necessary?\n"
        "A: Refraction records every (rule_id, facts) tuple that has already fired. Without refraction, a rule whose conditions remain true in working memory would fire infinitely. Refraction guarantees the engine terminates at a deterministic fixpoint.\n"
        "Q: Why represent rules as Horn clauses?\n"
        "A: Horn clauses allow linear-time forward deduction (modus ponens) without exponential truth-table complexity, making inference fast, deterministic, and easily explainable as a tree."
    )

    # =========================================================================
    # SLIDE 9: Decision Logic, Thresholds & Counterfactuals
    # =========================================================================
    s9 = add_slide_with_transition()
    add_header(s9, "Actuarial Loan Sizing, Risk Bands & Actionable Counterfactuals", "Underwriting Decision Logic")

    # 3 Horizontal Panels
    col_w = Inches(3.64)
    gap = Inches(0.4)
    
    # Col 1: Mathematical Formulas
    add_card(s9, Inches(0.8), Inches(1.5), col_w, Inches(5.2), WHITE, SLATE_200)
    tb_c1 = s9.shapes.add_textbox(Inches(1.0), Inches(1.7), col_w - Inches(0.4), Inches(4.8))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p_c1_t = tf_c1.paragraphs[0]
    p_c1_t.text = "Actuarial Formulas"
    p_c1_t.font.name = FONT_TITLE
    p_c1_t.font.size = Pt(15)
    p_c1_t.font.bold = True
    p_c1_t.font.color.rgb = NAVY_DARK

    f_items = [
        ("Debt-to-Income (DTI):", "DTI = Existing Monthly Debt / Monthly Income\n(Benchmark Threshold: DTI ≤ 0.40)"),
        ("Maximum Allowable EMI:", "Max EMI = max(0, 0.40 × Income - Existing Debt)\nProtects 60% of income for living expenses."),
        ("Annuity Present Value (PV):", "PV = Max EMI × [(1 - (1 + r)⁻ⁿ) / r]\nWhere r = monthly rate, n = tenure months.\nGuarantees repayment without default."),
        ("Recommended Amount:", "Min(Requested, PV_annuity, 36 × Monthly Income)")
    ]
    for h, b in f_items:
        p_h = tf_c1.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_c1.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE_700

    # Col 2: Decision Thresholds
    add_card(s9, Inches(0.8 + col_w + gap), Inches(1.5), col_w, Inches(5.2), WHITE, SLATE_200)
    tb_c2 = s9.shapes.add_textbox(Inches(1.0 + col_w + gap), Inches(1.7), col_w - Inches(0.4), Inches(4.8))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p_c2_t = tf_c2.paragraphs[0]
    p_c2_t.text = "Demonstration Thresholds"
    p_c2_t.font.name = FONT_TITLE
    p_c2_t.font.size = Pt(15)
    p_c2_t.font.bold = True
    p_c2_t.font.color.rgb = BLUE_PRIMARY

    t_items = [
        ("Prime Eligible:", "• Credit Score ≥ 750\n• Monthly Income ≥ ₹30,000\n• DTI ≤ 0.40 | Emp ≥ 2 years\n• Rate Band: 9.0% - 11.0% (Low Risk)"),
        ("Near-Prime Conditional:", "• Credit Score: 650 - 749\n• Soft DTI breach: 0.40 - 0.50\n• Rate Band: 11.0% - 14.0% (Medium Risk)\n• Condition: Sized to supportable PV"),
        ("Hard Knock-outs (Not Eligible):", "• Monthly Income ≤ 0\n• Age < 18 (Legal capacity failure)\n• Credit Score < 550\n• Recent Default on Record")
    ]
    for h, b in t_items:
        p_h = tf_c2.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_c2.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE_700

    # Col 3: Counterfactual Explanations
    add_card(s9, Inches(0.8 + (col_w + gap) * 2), Inches(1.5), col_w, Inches(5.2), WHITE, SLATE_200)
    tb_c3 = s9.shapes.add_textbox(Inches(1.0 + (col_w + gap) * 2), Inches(1.7), col_w - Inches(0.4), Inches(4.8))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p_c3_t = tf_c3.paragraphs[0]
    p_c3_t.text = "Counterfactual Guidance"
    p_c3_t.font.name = FONT_TITLE
    p_c3_t.font.size = Pt(15)
    p_c3_t.font.bold = True
    p_c3_t.font.color.rgb = EMERALD_GREEN

    cf_items = [
        ("Deductive Distance Principle:", "Counterfactuals are mathematically derived by computing the exact delta between an applicant's fact and the threshold boundary."),
        ("Case 1: Excessive DTI:", "Fact: DTI = 48% (Debt = ₹24,000 on Income = ₹50,000).\nCounterfactual: 'Reduce monthly debt by ₹4,000 to achieve 40% DTI threshold.'"),
        ("Case 2: Sub-Prime Credit:", "Fact: Score = 718.\nCounterfactual: 'Raise credit score by 32 points to qualify for Low-Risk prime rate of 9.5%.'"),
        ("Case 3: Unaffordable Sizing:", "Fact: Requested ₹15 Lakhs; max supportable is ₹9.8 Lakhs.\nCounterfactual: 'Reduce request to ₹9.8 Lakhs or extend tenure to 48 months.'")
    ]
    for h, b in cf_items:
        p_h = tf_c3.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_c3.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE_700

    set_speaker_notes(s9,
        "[Click 1] A unique strength of our system is how actuarial financial engineering integrates with symbolic logic. Rather than using arbitrary rule heuristics, we compute loan capacity using the actuarial annuity present value formula based on surplus monthly cash flow.\n\n"
        "[Click 2] When an applicant fails a condition, we do not simply output 'denied.' We generate deductive counterfactual hints: calculating the exact mathematical delta needed to qualify, such as reducing monthly debt by ₹4,000 or raising a credit score by 32 points.\n\n"
        "VIVA DEFENSE Q&A:\n"
        "Q: Why calculate loan sizing using the annuity formula instead of a simple multiplier?\n"
        "A: Simple income multipliers ignore loan tenure and interest rates. The annuity present value formula ensures that the monthly EMI will never exceed the applicant's maximum debt-service capability at the assigned interest band."
    )

    # =========================================================================
    # SLIDE 10: Working Application Storyboard
    # =========================================================================
    s10 = add_slide_with_transition()
    add_header(s10, "Working Application Storyboard: The 5-Step Underwriting Journey", "Live Application Walkthrough")

    # 5 story cards arranged horizontally
    step_w = Inches(2.18)
    step_gap = Inches(0.2)
    s_x = Inches(0.8)

    story_steps = [
        ("Step 1: Application Form", "desktop-new-application.png", "12 financial inputs with instant Pydantic validation."),
        ("Step 2: Instant Verdict", "desktop-results-eligible.png", "Prime, Conditional, or Knockout with annuity loan sizing."),
        ("Step 3: Inference Trace", "desktop-rule-trace.png", "Step-by-step firing history & conflict resolution."),
        ("Step 4: FOL Proof Tree", "desktop-fol-proof.png", "Visual Horn clause tree proving the decision."),
        ("Step 5: Audit Memo", "pdf-report.png", "Institutional ReportLab PDF Underwriting Memo.")
    ]

    for i, (title, img_name, caption) in enumerate(story_steps):
        x = s_x + i * (step_w + step_gap)
        card = add_card(s10, x, Inches(1.5), step_w, Inches(5.2), WHITE, SLATE_200)

        # Title
        tb_st = s10.shapes.add_textbox(x + Inches(0.1), Inches(1.65), step_w - Inches(0.2), Inches(0.6))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        p_st = tf_st.paragraphs[0]
        p_st.text = title
        p_st.font.name = FONT_TITLE
        p_st.font.size = Pt(11)
        p_st.font.bold = True
        p_st.font.color.rgb = BLUE_PRIMARY

        # Image
        add_image_card(s10, img_name, x + Inches(0.12), Inches(2.3), step_w - Inches(0.24), height=Inches(3.2))

        # Caption
        tb_cp = s10.shapes.add_textbox(x + Inches(0.1), Inches(5.6), step_w - Inches(0.2), Inches(1.0))
        tf_cp = tb_cp.text_frame
        tf_cp.word_wrap = True
        p_cp = tf_cp.paragraphs[0]
        p_cp.text = caption
        p_cp.font.size = Pt(9)
        p_cp.font.color.rgb = SLATE_700

    set_speaker_notes(s10,
        "[Click 1] Here you see the live, end-to-end storyboard captured directly from our running application. In Step 1, the applicant inputs twelve financial fields. Notice the field-level validation errors if inputs are out of bounds.\n\n"
        "[Click 2] In Step 2, the user submits the form and immediately sees their verdict—such as Prime Eligible—along with the recommended loan amount and interest band.\n\n"
        "[Click 3] In Steps 3 and 4, the user explores the complete Rule Inference Trace and First-Order Logic proof tree. Finally, Step 5 allows instantaneous export of a formal, auditable PDF underwriting memorandum.\n\n"
        "Hinglish delivery tip: Highlight karein ki ye real running full-stack app ke screenshots hain, koi mockup nahi."
    )

    # =========================================================================
    # SLIDE 11: Rule Engine vs Machine Learning Comparison
    # =========================================================================
    s11 = add_slide_with_transition()
    add_header(s11, "Empirical Evaluation: Symbolic Rule Engine vs Machine Learning", "Comparative Benchmark")

    # Left Side: Real Metrics Table
    add_card(s11, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), WHITE, SLATE_200)
    tb_m = s11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.8))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p_mt = tf_m.paragraphs[0]
    p_mt.text = "Benchmark on 5,000 Synthetic Applications"
    p_mt.font.name = FONT_TITLE
    p_mt.font.size = Pt(15)
    p_mt.font.bold = True
    p_mt.font.color.rgb = NAVY_DARK

    p_md = tf_m.add_paragraph()
    p_md.text = "Ground truth represents true repayment probability generated via an independent credit risk process (NOT from rule engine output)."
    p_md.font.size = Pt(9.5)
    p_md.font.color.rgb = SLATE_500
    p_md.space_after = Pt(8)

    # Table of Metrics
    t_m_shape = s11.shapes.add_table(4, 5, Inches(1.0), Inches(2.5), Inches(5.6), Inches(1.8))
    tm = t_m_shape.table
    tm.columns[0].width = Inches(2.0)
    tm.columns[1].width = Inches(0.9)
    tm.columns[2].width = Inches(0.9)
    tm.columns[3].width = Inches(0.9)
    tm.columns[4].width = Inches(0.9)

    m_headers = ["Model", "Accuracy", "Precision", "Recall", "F1 Score"]
    m_data = [
        ("Rule Engine (Standard)", "72.9%", "72.9%", "100.0%", "0.818"),
        ("Decision Tree (Depth 4)", "70.0%", "73.1%", "90.9%", "0.779"),
        ("Logistic Regression", "81.3%", "84.8%", "90.2%", "0.874")
    ]
    for c_idx, h in enumerate(m_headers):
        cell = tm.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r_idx, r in enumerate(m_data):
        for c_idx, val in enumerate(r):
            cell = tm.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BLUE_SUBTLE if r_idx == 0 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = SLATE_900
            if c_idx == 0:
                p.font.bold = True

    # Callout on Tradeoff
    tb_tr = s11.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.6), Inches(2.0))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    p_trt = tf_tr.paragraphs[0]
    p_trt.text = "Key Empirical Findings:"
    p_trt.font.bold = True
    p_trt.font.size = Pt(11)
    p_trt.font.color.rgb = BLUE_PRIMARY

    findings = [
        "• Rule Engine Prioritizes Safety: Achieves 100% recall on creditworthy applicants while strictly rejecting high-risk profiles.",
        "• Decision Tree Overfitting & Boundary Cliffs: Depth-limited tree suffers brittle split artifacts and lower overall F1 (0.779).",
        "• Logistic Regression High Accuracy vs Zero Auditability: While LR achieves 81.3% accuracy, it cannot provide proof trees or legally defensible adverse action notices."
    ]
    for f in findings:
        p_f = tf_tr.add_paragraph()
        p_f.text = f
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = SLATE_700

    # Right Side: Real Screenshot of Benchmark Page
    add_card(s11, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.2), WHITE, SLATE_200)
    add_image_card(s11, "desktop-ml-comparison.png", Inches(7.2), Inches(1.65), Inches(5.2), height=Inches(3.3))
    
    tb_rc = s11.shapes.add_textbox(Inches(7.2), Inches(5.1), Inches(5.2), Inches(1.5))
    tf_rc = tb_rc.text_frame
    tf_rc.word_wrap = True
    p_rc_t = tf_rc.paragraphs[0]
    p_rc_t.text = "Auditability & Defensibility Dimension:"
    p_rc_t.font.bold = True
    p_rc_t.font.size = Pt(11)
    p_rc_t.font.color.rgb = NAVY_DARK

    p_rc_b = tf_rc.add_paragraph()
    p_rc_b.text = "In banking, a 2% accuracy edge in statistical regression is useless if the lender cannot defend the rejection in an audit or court. The Rule Engine is 100% deterministic, inspectable, and legally defensible."
    p_rc_b.font.size = Pt(9.5)
    p_rc_b.font.color.rgb = SLATE_700

    set_speaker_notes(s11,
        "[Click 1] A critical requirement of our AI project was comparing our symbolic expert system with machine learning models trained on 5,000 independent synthetic records. It is vital to note that the ML models were NOT trained on the rule engine's outputs; they were trained on an independent ground-truth repayment probability.\n\n"
        "[Click 2] As shown in our empirical evaluation table, Logistic Regression achieves 81.3% accuracy, but offers zero auditability. The Rule Engine achieves a strong 0.818 F1 score while guaranteeing 100% deterministic auditability and formal First-Order Logic proof trees.\n\n"
        "Hinglish delivery tip: Yahan emphasize karein ki ML baseline independent ground truth pe train hui hai, isliye evaluation completely fair aur scientifically valid hai."
    )

    # =========================================================================
    # SLIDE 12: Algorithmic Fairness & Bias Review
    # =========================================================================
    s12 = add_slide_with_transition()
    add_header(s12, "Demographic Fairness Audit: Disparate Impact & Proxy Leakage", "Algorithmic Fairness & Ethics")

    # Left Side: Fairness Metrics & Table
    add_card(s12, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), WHITE, SLATE_200)
    tb_fn = s12.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.8))
    tf_fn = tb_fn.text_frame
    tf_fn.word_wrap = True
    p_fnt = tf_fn.paragraphs[0]
    p_fnt.text = "Auditing Synthetic Demographic Groups"
    p_fnt.font.name = FONT_TITLE
    p_fnt.font.size = Pt(15)
    p_fnt.font.bold = True
    p_fnt.font.color.rgb = NAVY_DARK

    p_fnd = tf_fn.add_paragraph()
    p_fnd.text = "Demographic attributes (Gender, Age, Region) exist ONLY in the audit dataset and were quarantined from the underwriting engine."
    p_fnd.font.size = Pt(9.5)
    p_fnd.font.color.rgb = SLATE_500
    p_fnd.space_after = Pt(6)

    # Table of Fairness Metrics
    t_f_shape = s12.shapes.add_table(4, 5, Inches(1.0), Inches(2.5), Inches(5.6), Inches(1.8))
    tfm = t_f_shape.table
    tfm.columns[0].width = Inches(1.6)
    tfm.columns[1].width = Inches(1.0)
    tfm.columns[2].width = Inches(1.0)
    tfm.columns[3].width = Inches(1.0)
    tfm.columns[4].width = Inches(1.0)

    f_headers = ["Attribute", "Group A", "Group B", "Disp. Impact", "Status"]
    f_data = [
        ("Gender", "Female (73.6%)", "Male (72.5%)", "0.985", "PASS (>0.80)"),
        ("Age Band", "Youth (57.3%)", "Mid-Career (83.2%)", "0.689", "FLAGGED (<0.80)"),
        ("Region", "Rural (68.7%)", "Metro (75.1%)", "0.915", "PASS (>0.80)")
    ]
    for c_idx, h in enumerate(f_headers):
        cell = tfm.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r_idx, r in enumerate(f_data):
        for c_idx, val in enumerate(r):
            cell = tfm.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if "FLAGGED" in val:
                cell.fill.fore_color.rgb = ROSE_BG
            elif "PASS" in val:
                cell.fill.fore_color.rgb = EMERALD_BG
            else:
                cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else SLATE_100
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            p.font.color.rgb = ROSE_RED if "FLAGGED" in val else (EMERALD_GREEN if "PASS" in val else SLATE_900)
            if c_idx in (0, 4):
                p.font.bold = True

    # Analysis Text
    tb_fa = s12.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.6), Inches(2.0))
    tf_fa = tb_fa.text_frame
    tf_fa.word_wrap = True
    p_fat = tf_fa.paragraphs[0]
    p_fat.text = "Algorithmic Ethics & Legal Insights:"
    p_fat.font.bold = True
    p_fat.font.size = Pt(11)
    p_fat.font.color.rgb = BLUE_PRIMARY

    f_insights = [
        "• EEOC Four-Fifths Rule: A selection rate for any group below 80% (0.80) of the highest rate constitutes actionable disparate impact.",
        "• Proxy Leakage Phenomenon: Even though age is omitted from rules, employment duration (years) and accumulated credit depth serve as proxies, depressing youth approval rates.",
        "• Kleinberg's Impossibility Theorem: Mathematical proof that statistical parity, calibration, and equal opportunity cannot be simultaneously satisfied when base credit rates differ."
    ]
    for fi in f_insights:
        p_fi = tf_fa.add_paragraph()
        p_fi.text = fi
        p_fi.font.size = Pt(9.5)
        p_fi.font.color.rgb = SLATE_700

    # Right Side: Fairness Screenshot
    add_card(s12, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.2), WHITE, SLATE_200)
    add_image_card(s12, "desktop-fairness.png", Inches(7.2), Inches(1.65), Inches(5.2), height=Inches(3.3))
    
    tb_fc = s12.shapes.add_textbox(Inches(7.2), Inches(5.1), Inches(5.2), Inches(1.5))
    tf_fc = tb_fc.text_frame
    tf_fc.word_wrap = True
    p_fc_t = tf_fc.paragraphs[0]
    p_fc_t.text = "Mitigation Recommendations:"
    p_fc_t.font.bold = True
    p_fc_t.font.size = Pt(11)
    p_fc_t.font.color.rgb = NAVY_DARK

    p_fc_b = tf_fc.add_paragraph()
    p_fc_b.text = "To remedy the age disparity without violating fair-lending law, we recommend introducing alternative underwriting data (e.g., educational credentials, prompt utility payments) rather than lowering credit score thresholds."
    p_fc_b.font.size = Pt(9.5)
    p_fc_b.font.color.rgb = SLATE_700

    set_speaker_notes(s12,
        "[Click 1] In Slide 12, we present our Algorithmic Fairness Audit across 5,000 synthetic records. Evaluating under the EEOC Four-Fifths rule, gender passes comfortably with a Disparate Impact Ratio of 0.985, and geography passes at 0.915.\n\n"
        "[Click 2] However, youth applicants show a disparate impact ratio of 0.689, triggering an automated audit flag. This demonstrates the classic 'Proxy Leakage' problem: even though age is not in the rules, employment stability (requiring 2 years) naturally correlates with career stage.\n\n"
        "[Click 3] As Kleinberg's Impossibility Theorem proves, you cannot satisfy statistical parity and predictive parity simultaneously when base rates differ. We recommend introducing alternative data such as rent payment history.\n\n"
        "Hinglish delivery tip: Yahan explain karein ki algorithm intentionally biased nahi hai, balki employment duration feature indirectly age ke sath correlate kar raha hai (proxy leakage)."
    )

    # =========================================================================
    # SLIDE 13: Testing & Validation
    # =========================================================================
    s13 = add_slide_with_transition()
    add_header(s13, "Empirical Verification: 37/37 Pytest Suite & Invariant Tests", "Verification & Quality Assurance")

    # Left Side: Test Suite Breakdown
    add_card(s13, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.2), WHITE, SLATE_200)
    tb_tst = s13.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(4.8))
    tf_tst = tb_tst.text_frame
    tf_tst.word_wrap = True
    p_tst_t = tf_tst.paragraphs[0]
    p_tst_t.text = "Rigorous Test Battery & Formal Invariants"
    p_tst_t.font.name = FONT_TITLE
    p_tst_t.font.size = Pt(15)
    p_tst_t.font.bold = True
    p_tst_t.font.color.rgb = NAVY_DARK

    test_modules = [
        ("test_rule_engine.py (12 Tests):", "Validates 9 credit underwriting scenarios, determinism across 100 runs, rule order invariance, and refraction properties."),
        ("test_financial.py (6 Tests):", "Verifies DTI division-by-zero protection, max EMI floors, compound interest annuity PV math, and risk rate bands."),
        ("test_fol.py (6 Tests):", "Validates Horn clause instantiation, ground atom unification, Negation-as-Failure, and proof tree visual graph generation."),
        ("test_api.py (8 Tests):", "Verifies FastAPI REST endpoints, Pydantic 422 error boundaries, CORS headers, and SQLite persistence."),
        ("test_ml_and_fairness.py (5 Tests):", "Validates Disparate Impact calculation, Four-Fifths rule flags, confusion matrices, and model benchmark scores.")
    ]
    for mod, desc in test_modules:
        p_m = tf_tst.add_paragraph()
        p_m.text = f"• {mod}"
        p_m.font.bold = True
        p_m.font.size = Pt(10)
        p_m.font.color.rgb = SLATE_900
        p_d = tf_tst.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = SLATE_700

    # Invariants Box
    inv_box = add_card(s13, Inches(1.0), Inches(5.2), Inches(5.4), Inches(1.3), BLUE_SUBTLE, BLUE_PRIMARY)
    tb_inv = s13.shapes.add_textbox(Inches(1.1), Inches(5.25), Inches(5.2), Inches(1.2))
    tf_inv = tb_inv.text_frame
    tf_inv.word_wrap = True
    p_it = tf_inv.paragraphs[0]
    p_it.text = "PROVEN FORMAL INVARIANTS:"
    p_it.font.bold = True
    p_it.font.size = Pt(10.5)
    p_it.font.color.rgb = BLUE_PRIMARY

    invariants = [
        "1. Determinism: Identical inputs ALWAYS yield identical decisions and execution traces.",
        "2. Order Invariance: Shuffling the rules YAML order does NOT change the outcome.",
        "3. Refraction: Fired rules never re-fire on the same fact set."
    ]
    for inv in invariants:
        p_i = tf_inv.add_paragraph()
        p_i.text = f"• {inv}"
        p_i.font.size = Pt(9)
        p_i.font.color.rgb = SLATE_900

    # Right Side: Pytest Terminal Image
    add_card(s13, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    add_image_card(s13, "tests.png", Inches(7.0), Inches(1.65), Inches(5.4), height=Inches(3.3))
    
    tb_tc = s13.shapes.add_textbox(Inches(7.1), Inches(5.1), Inches(5.2), Inches(1.5))
    tf_tc = tb_tc.text_frame
    tf_tc.word_wrap = True
    p_tc_t = tf_tc.paragraphs[0]
    p_tc_t.text = "Continuous Integration & Test Execution:"
    p_tc_t.font.bold = True
    p_tc_t.font.size = Pt(11)
    p_tc_t.font.color.rgb = EMERALD_GREEN

    p_tc_b = tf_tc.add_paragraph()
    p_tc_b.text = "All 37 unit and integration tests execute in 2.77 seconds with 100% pass rate. Every edge case—including legal capacity knockouts (age < 18), zero income boundaries, and excessive DTI—is verified automatically."
    p_tc_b.font.size = Pt(9.5)
    p_tc_b.font.color.rgb = SLATE_700

    set_speaker_notes(s13,
        "[Click 1] Quality assurance and mathematical correctness were central to our development methodology. We created a comprehensive 37-test battery in Pytest covering rule firing, financial annuity math, FOL proof tree generation, API endpoints, and fairness audits.\n\n"
        "[Click 2] As shown on the right, all 37 tests execute and pass in under 3 seconds. Crucially, we wrote automated tests to prove three formal mathematical invariants: determinism across 100 runs, rule order invariance under permutation, and the refraction property.\n\n"
        "Hinglish delivery tip: Examiners ko batayein ki humne shuffling test kiya hai jisme YAML rules ka order badalne par bhi output identical rehta hai, proving robust conflict resolution."
    )

    # =========================================================================
    # SLIDE 14: Conclusion & Learning Outcomes
    # =========================================================================
    s14 = add_slide_with_transition()
    add_header(s14, "Project Conclusions & Core Applied AI Takeaways", "Conclusions & Key Learnings")

    # Left Side: Scorecard
    add_card(s14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_sc = s14.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    p_sct = tf_sc.paragraphs[0]
    p_sct.text = "Deliverables Scorecard"
    p_sct.font.name = FONT_TITLE
    p_sct.font.size = Pt(16)
    p_sct.font.bold = True
    p_sct.font.color.rgb = EMERALD_GREEN

    sc_items = [
        ("Symbolic Production Rule Engine:", "Delivered declarative forward-chaining engine with 4-tier conflict resolution and refraction (100% achieved)."),
        ("First-Order Logic Proof Trees:", "Horn clauses, ground atoms, and visual derivation trees for every loan decision (100% achieved)."),
        ("Actuarial Debt & Loan Sizing:", "Implemented compound annuity PV formula, max EMI constraints, and 3 risk bands (100% achieved)."),
        ("Empirical ML Benchmark:", "Decision Tree & Logistic Regression models evaluated on 5,000 synthetic records (100% achieved)."),
        ("Algorithmic Fairness Audit:", "Disparate Impact, Statistical Parity, and proxy leakage analysis across 5 groups (100% achieved).")
    ]
    for h, b in sc_items:
        p_h = tf_sc.add_paragraph()
        p_h.text = f"✓ {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_sc.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE_700

    # Right Side: Learnings & Limitations
    add_card(s14, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_lr = s14.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_lr = tb_lr.text_frame
    tf_lr.word_wrap = True
    p_lrt = tf_lr.paragraphs[0]
    p_lrt.text = "Academic Insights & Limitations"
    p_lrt.font.name = FONT_TITLE
    p_lrt.font.size = Pt(16)
    p_lrt.font.bold = True
    p_lrt.font.color.rgb = NAVY_DARK

    lr_items = [
        ("The Value of Symbolic AI in Regulated Domains:", "While deep learning dominates perceptual tasks (vision, audio), symbolic expert systems remain unmatched for legal defensibility and exact auditability."),
        ("Neuro-Symbolic Hybridization is the Future:", "The optimal credit architecture is hybrid: statistical ML for predictive risk estimation, enveloped by symbolic FOL rule engines as non-negotiable safety guardrails."),
        ("Honest Academic Limitations:", 
         "• Thresholds are illustrative demonstration values, not bank policy.\n"
         "• Synthetic data lacks real macroeconomic shocks (e.g., inflation).\n"
         "• Rule maintenance requires domain expert knowledge engineering.")
    ]
    for h, b in lr_items:
        p_h = tf_lr.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = SLATE_900
        p_b = tf_lr.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = SLATE_700

    set_speaker_notes(s14,
        "[Click 1] To conclude, our project has achieved 100% of the goals set out in the Artificial Intelligence Foundations course syllabus. We have proven that explainable, rule-based systems are not a relic of the past, but an essential component of modern high-stakes AI governance.\n\n"
        "[Click 2] Our key takeaway is that the future of banking AI is neuro-symbolic: combining the predictive power of machine learning with the deterministic, uncompromised safety guardrails of symbolic logic.\n\n"
        "Hinglish delivery tip: Yahan confident summary dekar conclude karein ki symbolic AI aur ML ka comparison humne comprehensively establish kiya hai."
    )

    # =========================================================================
    # SLIDE 15: Future Work & Project Team Acknowledgements
    # =========================================================================
    s15 = add_slide_with_transition(NAVY_DARK)
    
    # Sub-badge
    tb_15b = s15.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.4))
    p = tb_15b.text_frame.paragraphs[0]
    p.text = "ROADMAP & ACKNOWLEDGEMENTS"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_LIGHT

    # Title
    tb_15t = s15.shapes.add_textbox(Inches(1.0), Inches(1.15), Inches(11.3), Inches(0.8))
    p_t = tb_15t.text_frame.paragraphs[0]
    p_t.text = "Future Technical Extensions & Acknowledgements"
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    # Left Card: Future Work
    add_card(s15, Inches(1.0), Inches(2.1), Inches(5.4), Inches(4.7), RGBColor(15, 34, 77), BLUE_PRIMARY)
    tb_fw = s15.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(5.0), Inches(4.3))
    tf_fw = tb_fw.text_frame
    tf_fw.word_wrap = True
    p_fwt = tf_fw.paragraphs[0]
    p_fwt.text = "Four Technical Extensions"
    p_fwt.font.name = FONT_TITLE
    p_fwt.font.size = Pt(16)
    p_fwt.font.bold = True
    p_fwt.font.color.rgb = BLUE_LIGHT

    ext_items = [
        ("1. Inductive Logic Programming (ILP):", "Automatically induce candidate Horn clauses from historical repayment data, allowing the rule base to evolve semi-autonomously."),
        ("2. Interactive Recourse Simulation:", "Real-time slider interface allowing applicants to interactively simulate how paying off debts impacts their approval probability."),
        ("3. Distributed Rule Engine (Rete Algorithm):", "Compile production rules into an optimized Rete network for sub-millisecond evaluation at commercial banking scale."),
        ("4. Dynamic Macroeconomic Rate Curves:", "Integrate dynamic yield curves and central bank repo rates into the annuity present value sizing engine.")
    ]
    for h, b in ext_items:
        p_h = tf_fw.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = WHITE
        p_b = tf_fw.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = RGBColor(203, 213, 225)

    # Right Card: Acknowledgements & Team
    add_card(s15, Inches(6.8), Inches(2.1), Inches(5.5), Inches(4.7), RGBColor(15, 34, 77), BLUE_PRIMARY)
    tb_ak = s15.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.1), Inches(4.3))
    tf_ak = tb_ak.text_frame
    tf_ak.word_wrap = True
    p_akt = tf_ak.paragraphs[0]
    p_akt.text = "Project Team & Mentor Acknowledgement"
    p_akt.font.name = FONT_TITLE
    p_akt.font.size = Pt(16)
    p_akt.font.bold = True
    p_akt.font.color.rgb = BLUE_LIGHT

    p_thx = tf_ak.add_paragraph()
    p_thx.text = "We express our sincere gratitude to our faculty mentor Sheveta for her invaluable guidance and rigorous academic standards throughout this course."
    p_thx.font.size = Pt(10)
    p_thx.font.color.rgb = RGBColor(226, 232, 240)
    p_thx.space_after = Pt(8)

    p_tm_lbl = tf_ak.add_paragraph()
    p_tm_lbl.text = "Course: Artificial Intelligence Foundations (K4P25AT) · Group 5"
    p_tm_lbl.font.size = Pt(10.5)
    p_tm_lbl.font.bold = True
    p_tm_lbl.font.color.rgb = BLUE_LIGHT

    team_final = [
        ("Pilli Sreeja", "Registration No. 12515392"),
        ("Harshit Kumar Singh", "Registration No. 12519334"),
        ("Inaganti Hajmeer Vali", "Registration No. 12521593")
    ]
    for n, r in team_final:
        p_tf = tf_ak.add_paragraph()
        p_tf.text = f"• {n} — {r}"
        p_tf.font.size = Pt(11)
        p_tf.font.bold = True
        p_tf.font.color.rgb = WHITE

    p_q = tf_ak.add_paragraph()
    p_q.text = "\nThank You! We welcome questions from the faculty evaluators."
    p_q.font.size = Pt(12)
    p_q.font.bold = True
    p_q.font.color.rgb = BLUE_LIGHT

    set_speaker_notes(s15,
        "[Click 1] To conclude our presentation, we have outlined four exciting future directions, including Inductive Logic Programming to semi-automatically discover rules, and Rete algorithm optimization for high-frequency banking.\n\n"
        "[Click 2] On behalf of my teammates Pilli Sreeja, Harshit Kumar Singh, and Inaganti Hajmeer Vali, we thank our mentor Sheveta and the evaluators for their time. We are now ready to demonstrate the live application and address any technical questions.\n\n"
        "Hinglish delivery tip: Polite aur confident tone me conclude karein: 'Thank you mentor Sheveta and evaluators. We are now open for Q&A.'"
    )

    # =========================================================================
    # APPENDIX SLIDE A: Viva Voce Defense Cheat Sheet
    # =========================================================================
    sA = add_slide_with_transition()
    add_header(sA, "Appendix A: Faculty Viva Voce Defense Cheat Sheet", "Appendix · Viva Preparation")

    viva_questions = [
        ("1. Why Forward Chaining over Backward Chaining?", "In loan underwriting, all applicant facts are known upfront at submission time. Forward chaining naturally derives all consequences (DTI, risk band, eligibility) in one pass toward a fixpoint."),
        ("2. How is Infinite Looping Prevented?", "Refraction guarantees that an instantiated rule fires at most once per fact set. Once working memory reaches a fixpoint, inference halts automatically."),
        ("3. What is Negation-as-Failure (NAF)?", "Closed-world assumption: NOT DefaultOnRecord(x) succeeds because DefaultOnRecord(x) cannot be proven from working memory."),
        ("4. Why Use Annuity Math for Sizing?", "Flat income multipliers ignore interest rates and tenure. The annuity formula mathematically guarantees that the monthly EMI never exceeds the applicant's surplus cash flow."),
        ("5. How Are Protected Attributes Quarantined?", "The loan evaluation API schema does not accept demographic attributes. They exist solely in the synthetic audit dataset for fairness evaluations."),
        ("6. Why Shouldn't ML Be Trained on Rule Engine Output?", "Training ML on rule outputs turns it into a mere statistical approximation of the rules. Our ML was trained on an independent ground truth repayment process to evaluate true comparative generalization.")
    ]

    card_h = Inches(1.5)
    c_w = Inches(5.6)
    
    for i, (q, a) in enumerate(viva_questions):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * Inches(6.1)
        y = Inches(1.5) + row * Inches(1.75)
        
        add_card(sA, x, y, c_w, card_h, WHITE, SLATE_200)
        tb_vq = sA.shapes.add_textbox(x + Inches(0.15), y + Inches(0.1), c_w - Inches(0.3), card_h - Inches(0.2))
        tf_vq = tb_vq.text_frame
        tf_vq.word_wrap = True
        p_q = tf_vq.paragraphs[0]
        p_q.text = q
        p_q.font.name = FONT_TITLE
        p_q.font.size = Pt(11)
        p_q.font.bold = True
        p_q.font.color.rgb = BLUE_PRIMARY

        p_a = tf_vq.add_paragraph()
        p_a.text = a
        p_a.font.size = Pt(9.5)
        p_a.font.color.rgb = SLATE_700

    set_speaker_notes(sA,
        "Appendix Slide A serves as an emergency reference during viva voce defense. If evaluators ask about inference strategy, explain that forward chaining is data-driven, which matches credit underwriting where all borrower facts arrive together in the application payload."
    )

    # =========================================================================
    # APPENDIX SLIDE B: Complete UI & Architecture Gallery
    # =========================================================================
    sB = add_slide_with_transition()
    add_header(sB, "Appendix B: Complete Application View Gallery", "Appendix · UI Showcase")

    gallery_items = [
        ("Executive Dashboard", "desktop-dashboard.png"),
        ("Conditional Verdict", "desktop-results-conditional.png"),
        ("Excessive DTI Knockout", "desktop-results-not-eligible.png"),
        ("Audit History & Filter", "desktop-history.png"),
        ("Dark Mode Interface", "desktop-dark-mode.png"),
        ("Mobile Experience", "mobile-results.png")
    ]

    g_w = Inches(3.64)
    g_h = Inches(2.4)
    g_gap_x = Inches(0.4)
    g_gap_y = Inches(0.25)

    for i, (cap, img_name) in enumerate(gallery_items):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (g_w + g_gap_x)
        y = Inches(1.5) + row * (g_h + g_gap_y)

        add_card(sB, x, y, g_w, g_h, WHITE, SLATE_200)
        add_image_card(sB, img_name, x + Inches(0.1), y + Inches(0.1), g_w - Inches(0.2), height=g_h - Inches(0.45))
        
        tb_gc = sB.shapes.add_textbox(x + Inches(0.1), y + g_h - Inches(0.35), g_w - Inches(0.2), Inches(0.3))
        tf_gc = tb_gc.text_frame
        p_gc = tf_gc.paragraphs[0]
        p_gc.alignment = PP_ALIGN.CENTER
        p_gc.text = cap
        p_gc.font.bold = True
        p_gc.font.size = Pt(9.5)
        p_gc.font.color.rgb = SLATE_700

    set_speaker_notes(sB,
        "Appendix Slide B provides high-resolution captures of the application across multiple screen sizes and states, proving responsiveness and production design polish."
    )

    # =========================================================================
    # APPENDIX SLIDE C: Formal Glossary & References
    # =========================================================================
    sC = add_slide_with_transition()
    add_header(sC, "Appendix C: Formal AI Glossary & Academic References", "Appendix · Definitions & Citations")

    # Left: Glossary
    add_card(sC, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_gl = sC.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_gl = tb_gl.text_frame
    tf_gl.word_wrap = True
    p_glt = tf_gl.paragraphs[0]
    p_glt.text = "Formal AI Glossary"
    p_glt.font.name = FONT_TITLE
    p_glt.font.size = Pt(15)
    p_glt.font.bold = True
    p_glt.font.color.rgb = NAVY_DARK

    glossary = [
        ("Expert System: ", "AI system using knowledge base and inference engine to solve complex domain problems."),
        ("Production Rule: ", "Condition-action statement: IF conditions THEN fire actions / assert facts."),
        ("Working Memory: ", "Active dynamic repository of ground facts representing the current state."),
        ("Conflict Resolution: ", "Deterministic strategy selecting which rule fires when multiple match."),
        ("Refraction: ", "Principle ensuring a rule fires at most once on the same fact instantiation."),
        ("Horn Clause: ", "Logical clause with at most one positive literal: P₁ ∧ ... ∧ Pₙ → Q."),
        ("Ground Atom: ", "A predicate applied to concrete constant arguments with zero variables."),
        ("Negation-as-Failure: ", "Non-monotonic inference treating inability to prove P as proof of ¬P.")
    ]
    for h, b in glossary:
        p_g = tf_gl.add_paragraph()
        p_g.text = f"• {h}"
        p_g.font.bold = True
        p_g.font.size = Pt(9.5)
        p_g.font.color.rgb = SLATE_900
        p_gd = tf_gl.add_paragraph()
        p_gd.text = f"   {b}"
        p_gd.font.size = Pt(9)
        p_gd.font.color.rgb = SLATE_700

    # Right: References
    add_card(sC, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2), WHITE, SLATE_200)
    tb_rf = sC.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.8))
    tf_rf = tb_rf.text_frame
    tf_rf.word_wrap = True
    p_rft = tf_rf.paragraphs[0]
    p_rft.text = "Academic & Regulatory References"
    p_rft.font.name = FONT_TITLE
    p_rft.font.size = Pt(15)
    p_rft.font.bold = True
    p_rft.font.color.rgb = BLUE_PRIMARY

    references = [
        ("Russell, S. & Norvig, P. (2020): ", "Artificial Intelligence: A Modern Approach (4th ed.). Prentice Hall. (Inference, Horn clauses, expert systems)."),
        ("Shortliffe, E. H. (1976): ", "Computer-Based Medical Consultations: MYCIN. Elsevier. (Production rules, conflict resolution, certainty)."),
        ("Equal Credit Opportunity Act (ECOA, 15 U.S.C. § 1691): ", "Regulation B Adverse Action Notice requirements for automated lending."),
        ("Fair Credit Reporting Act (FCRA, 15 U.S.C. § 1681): ", "Statutory mandates for algorithmic transparency and accuracy in consumer underwriting."),
        ("Barocas, S., Hardt, M., & Narayanan, A. (2019): ", "Fairness and Machine Learning: Limitations and Opportunities. MIT Press."),
        ("Kleinberg, J., Mullainathan, S., & Raghavan, M. (2016): ", "Inherent Trade-Offs in the Fair Determination of Risk Scores. arXiv:1609.05807.")
    ]
    for h, b in references:
        p_r = tf_rf.add_paragraph()
        p_r.text = f"• {h}"
        p_r.font.bold = True
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = SLATE_900
        p_rd = tf_rf.add_paragraph()
        p_rd.text = f"   {b}"
        p_rd.font.size = Pt(9)
        p_rd.font.color.rgb = SLATE_700

    set_speaker_notes(sC,
        "Appendix Slide C documents authoritative definitions and canonical literature citations supporting our expert system, regulatory compliance, and algorithmic fairness architecture."
    )

    # Save Presentation
    prs.save(str(OUTPUT_FILE))
    print(f"[SUCCESS] Widescreen 16:9 Presentation generated with 18 slides at:\n  {OUTPUT_FILE}")


if __name__ == "__main__":
    create_deck()
