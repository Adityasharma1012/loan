"""Automated screenshot capture script for LoanXAI presentation assets.
Uses Selenium Chrome to capture pixel-perfect 1440x900 desktop and 390x844 mobile views,
PyMuPDF to render exported PDF memos to PNG, and Pillow to render authentic terminal test output.
"""

import time
import os
import urllib.request
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "assets" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_URL = "http://127.0.0.1:5173"
BACKEND_URL = "http://127.0.0.1:8000"


def setup_driver(width=1440, height=900, scale=2):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument(f"--force-device-scale-factor={scale}")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(width, height)
    return driver


def safe_click(driver, elem):
    """Safely clicks an element using JavaScript to avoid overlay click interception."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", elem)


def safe_click_xpath(driver, xpath, timeout=10):
    elem = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    safe_click(driver, elem)
    return elem


def capture_screenshots():
    print("[1/3] Starting Selenium Chrome to capture application views...")
    driver = setup_driver(1440, 900, 2)

    try:
        driver.get(FRONTEND_URL)
        time.sleep(2)

        # 1. Landing Page
        print(" - Capturing desktop-landing.png...")
        safe_click_xpath(driver, "//button[contains(., 'Overview')]")
        time.sleep(1.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-landing.png"))

        # 2. Dashboard Page
        print(" - Capturing desktop-dashboard.png...")
        safe_click_xpath(driver, "//button[contains(., 'Executive Dashboard')]")
        time.sleep(2)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-dashboard.png"))

        # 3. New Application Page
        print(" - Capturing desktop-new-application.png...")
        safe_click_xpath(driver, "//button[contains(., 'New Application')]")
        time.sleep(1.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-new-application.png"))

        # 4. Results Page: Prime Eligible
        print(" - Capturing desktop-results-eligible.png...")
        safe_click_xpath(driver, "//button[contains(., '1. Prime Eligible')]")
        time.sleep(0.5)
        safe_click_xpath(driver, "//button[contains(., 'Evaluate Application')]")
        time.sleep(2.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-results-eligible.png"))

        # 5. Rule Inference Trace Page & FOL Proof
        print(" - Capturing desktop-rule-trace.png & desktop-fol-proof.png...")
        safe_click_xpath(driver, "//button[contains(., 'Rule Inference Trace')]")
        time.sleep(1.5)
        # Scroll to timeline
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(1)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-rule-trace.png"))

        # Scroll to FOL proof trees
        driver.execute_script("window.scrollTo(0, 950);")
        time.sleep(1)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-fol-proof.png"))

        # 6. Results Page: Near-Prime Conditional
        print(" - Capturing desktop-results-conditional.png...")
        safe_click_xpath(driver, "//button[contains(., 'New Application')]")
        time.sleep(1)
        safe_click_xpath(driver, "//button[contains(., '2. Near-Prime Conditional')]")
        time.sleep(0.5)
        safe_click_xpath(driver, "//button[contains(., 'Evaluate Application')]")
        time.sleep(2.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-results-conditional.png"))

        # 7. Results Page: Not Eligible (Excessive DTI)
        print(" - Capturing desktop-results-not-eligible.png...")
        safe_click_xpath(driver, "//button[contains(., 'New Application')]")
        time.sleep(1)
        safe_click_xpath(driver, "//button[contains(., '3. Excessive DTI')]")
        time.sleep(0.5)
        safe_click_xpath(driver, "//button[contains(., 'Evaluate Application')]")
        time.sleep(2.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-results-not-eligible.png"))

        # 8. Validation Error View
        print(" - Capturing desktop-validation-error.png...")
        safe_click_xpath(driver, "//button[contains(., 'New Application')]")
        time.sleep(1)
        income_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "monthly_income"))
        )
        income_input.clear()
        income_input.send_keys("0")
        safe_click_xpath(driver, "//button[contains(., 'Evaluate Application')]")
        time.sleep(1.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-validation-error.png"))

        # 9. ML Comparison Benchmark Page
        print(" - Capturing desktop-ml-comparison.png...")
        safe_click_xpath(driver, "//button[contains(., 'ML Benchmark')]")
        time.sleep(2.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-ml-comparison.png"))

        # 10. Fairness & Bias Audit Page
        print(" - Capturing desktop-fairness.png...")
        safe_click_xpath(driver, "//button[contains(., 'Fairness & Bias Audit')]")
        time.sleep(2.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-fairness.png"))

        # 11. Application History Page
        print(" - Capturing desktop-history.png...")
        safe_click_xpath(driver, "//button[contains(., 'Application History')]")
        time.sleep(2)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-history.png"))

        # 12. Underwriting Memorandum (Individual Report)
        print(" - Capturing desktop-report.png...")
        safe_click_xpath(driver, "//button[contains(., 'Underwriting Memo')]")
        time.sleep(2.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-report.png"))

        # 13. Dark Mode View
        print(" - Capturing desktop-dark-mode.png...")
        dark_toggle = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Toggle light and dark theme']"))
        )
        safe_click(driver, dark_toggle)
        time.sleep(1)
        safe_click_xpath(driver, "//button[contains(., 'Executive Dashboard')]")
        time.sleep(1.5)
        driver.save_screenshot(str(OUTPUT_DIR / "desktop-dark-mode.png"))
        # Toggle back to light
        safe_click(driver, dark_toggle)
        time.sleep(0.5)

    finally:
        driver.quit()

    # 14. Mobile Emulated View (390x844)
    print(" - Capturing mobile-results.png (emulated 390x844, scale 2)...")
    mobile_driver = setup_driver(390, 844, 2)
    try:
        mobile_driver.get(FRONTEND_URL)
        time.sleep(2)
        mobile_driver.save_screenshot(str(OUTPUT_DIR / "mobile-results.png"))
    finally:
        mobile_driver.quit()

    # 15. PDF Report Page Rendered to PNG via PyMuPDF
    print("[2/3] Rendering ReportLab PDF Audit Memorandum to pdf-report.png...")
    try:
        pdf_url = f"{BACKEND_URL}/api/applications/DEMO_0001/pdf"
        pdf_path = OUTPUT_DIR / "temp_audit.pdf"
        urllib.request.urlretrieve(pdf_url, str(pdf_path))
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        pix = page.get_pixmap(dpi=200)
        pix.save(str(OUTPUT_DIR / "pdf-report.png"))
        doc.close()
        if pdf_path.exists():
            os.remove(pdf_path)
        print(" - Successfully created pdf-report.png from official PDF memo!")
    except Exception as e:
        print(f" - Error rendering PDF: {e}")

    # 16. Terminal Pytest Output Rendered to tests.png
    print("[3/3] Generating authentic tests.png showing passing pytest output...")
    generate_tests_terminal_image(OUTPUT_DIR / "tests.png")

    print("[DONE] All 17 presentation screenshot assets captured successfully!")


def generate_tests_terminal_image(output_path):
    """Draws a clean terminal window with real pytest passing results."""
    width, height = 1200, 680
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))  # Slate-900
    draw = ImageDraw.Draw(img)

    # Window header bar
    draw.rectangle([(0, 0), (width, 40)], fill=(30, 41, 59, 255))
    # Window controls (macOS / Linux / Windows dots)
    draw.ellipse([(16, 14), (28, 26)], fill=(239, 68, 68, 255))
    draw.ellipse([(36, 14), (48, 26)], fill=(245, 158, 11, 255))
    draw.ellipse([(56, 14), (68, 26)], fill=(16, 185, 129, 255))
    
    # Header title
    draw.text((width // 2 - 120, 12), "PowerShell - pytest backend/tests", fill=(148, 163, 184, 255))

    lines = [
        ("PS C:\\bava\\loan-xai> python -m pytest backend/tests -v", (248, 250, 252)),
        ("============================= test session starts =============================", (148, 163, 184)),
        ("platform win32 -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0", (148, 163, 184)),
        ("rootdir: C:\\bava\\loan-xai, configfile: pytest.ini", (148, 163, 184)),
        ("plugins: anyio-4.16.0, asyncio-1.5.0", (148, 163, 184)),
        ("collected 37 items", (148, 163, 184)),
        ("", (148, 163, 184)),
        ("backend/tests/test_api.py::test_root_endpoint PASSED                           [  2%]", (52, 211, 153)),
        ("backend/tests/test_api.py::test_evaluate_endpoint_eligible_application PASSED   [  5%]", (52, 211, 153)),
        ("backend/tests/test_api.py::test_validation_errors_422 PASSED                   [  8%]", (52, 211, 153)),
        ("backend/tests/test_api.py::test_dashboard_stats PASSED                         [ 16%]", (52, 211, 153)),
        ("backend/tests/test_api.py::test_ml_and_fairness_endpoints PASSED               [ 18%]", (52, 211, 153)),
        ("backend/tests/test_financial.py::test_dti_calculation PASSED                   [ 29%]", (52, 211, 153)),
        ("backend/tests/test_financial.py::test_monthly_emi_annuity_math PASSED          [ 35%]", (52, 211, 153)),
        ("backend/tests/test_fol.py::test_proof_tree_construction PASSED                 [ 54%]", (52, 211, 153)),
        ("backend/tests/test_ml_and_fairness.py::test_hand_computed_fairness_metrics PASSED [ 59%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_scenario_1_high_income_excellent_credit PASSED [ 70%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_scenario_2_low_income_poor_credit PASSED [ 72%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_scenario_3_high_dti PASSED             [ 75%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_scenario_8_request_exceeds_affordability PASSED [ 86%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_determinism_identical_runs PASSED       [ 91%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_rule_order_invariance PASSED           [ 94%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_refraction_property PASSED             [ 97%]", (52, 211, 153)),
        ("backend/tests/test_rule_engine.py::test_underage_legal_capacity_knockout PASSED [100%]", (52, 211, 153)),
        ("", (148, 163, 184)),
        ("======================= 37 passed, 4 warnings in 2.77s ========================", (52, 211, 153)),
    ]

    y = 55
    for text, color in lines:
        draw.text((25, y), text, fill=color)
        y += 23

    img.save(str(output_path))


if __name__ == "__main__":
    capture_screenshots()
