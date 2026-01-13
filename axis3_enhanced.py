"""
Enhanced Selenium Script with Defect Injection
Collects rich telemetry and feeds into alert engine
"""

import re
import time
import threading
import os
import requests
import json
import uuid
from datetime import datetime
from openpyxl import Workbook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from defect_injector import DefectInjector, DefectConfiguration
from database import AlertDatabase


def check_link(url):
    """Check if URL is accessible"""
    try:
        response = requests.get(url, timeout=10)
        return response.status_code, "Success" if response.status_code == 200 else "Failed"
    except requests.exceptions.RequestException as e:
        return None, str(e)


def run_check(activity_url, check_id, report_data, alert_events, execution_id, defect_injector):
    """
    Run single activity check with defect injection
    
    Args:
        activity_url: URL of activity page
        check_id: Activity ID (1-7)
        report_data: Shared list for Excel report
        alert_events: Shared list for alerts
        execution_id: Unique execution identifier
        defect_injector: DefectInjector instance
    """
    
    check_start_time = time.time()
    
    # Create headless Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(activity_url)
    
    wait = WebDriverWait(driver, 10)
    
    target_url = None
    
    try:
        # Extract textarea content
        textarea = wait.until(EC.presence_of_element_located((By.ID, "detail-text")))
        text = textarea.get_attribute("value")
        
        # Extract URL
        urls = re.findall(r'https?://[^\s"]+', text)
        if not urls:
            raise RuntimeError("No URL found in textarea")
        
        target_url = urls[0]
        activity_name = extract_activity_name(activity_url)
        
        print(f"✓ Check {check_id}: {activity_name}")
        
        # Check link status
        status_code, reason = check_link(target_url)
        
        # Inject defect if applicable
        injected_defect = defect_injector.get_defect(check_id, activity_name)
        
        if injected_defect:
            # Override with injected defect
            original_status_code = status_code
            status_code = injected_defect.get("status_code")
            reason = injected_defect.get("message")
            is_simulated = True
        else:
            original_status_code = status_code
            is_simulated = False
        
        response_time = time.time() - check_start_time
        
        # Create rich alert event
        alert_event = {
            "alert_id": str(uuid.uuid4()),
            "execution_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "check_id": check_id,
            "activity_name": activity_name,
            "url": target_url,
            "status": "success" if status_code == 200 else "failure",
            "response_code": status_code,
            "original_response_code": original_status_code,
            "response_time": response_time,
            "error_message": reason if status_code != 200 else "",
            "is_simulated": is_simulated,
            "severity": injected_defect.get("severity", 5) if is_simulated else 5,
            "retry_count": 0,
            "source": "selenium"
        }
        
        alert_events.append(alert_event)
        report_data.append([target_url, status_code, "Checked" if status_code == 200 else "Failed", reason])
        
        # Open URL in new tab and take screenshot
        driver.execute_script("window.open(arguments[0], '_blank');", target_url)
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(lambda d: d.title is not None)
        time.sleep(1)
        
        screenshot_path = f"screenshots/screenshot_{check_id}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        
        # Switch back
        driver.switch_to.window(driver.window_handles[0])
        
        # Fill form
        screenshot_element = wait.until(EC.presence_of_element_located((By.ID, "screenshot")))
        screenshot_element.send_keys(os.path.abspath(screenshot_path))
        
        # Select radio button based on status
        radio_id = "green" if status_code == 200 else "red"
        radio_btn = wait.until(EC.element_to_be_clickable((By.ID, radio_id)))
        driver.execute_script("arguments[0].click();", radio_btn)
        
        # Enter name
        name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_field.send_keys("PyBot-AlertEngine")
        
        # Submit
        driver.execute_script("document.querySelector('.submit-btn').classList.add('enabled');")
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'submit-btn')]")))
        driver.execute_script("arguments[0].click();", submit_btn)
        
        print(f"  ├─ Status: {status_code}")
        print(f"  ├─ Time: {response_time:.2f}s")
        print(f"  └─ Simulated: {'✓ Yes' if is_simulated else '✗ No'}")
        
    except Exception as e:
        print(f"✗ Check {check_id} Error: {e}")
        alert_event = {
            "alert_id": str(uuid.uuid4()),
            "execution_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "check_id": check_id,
            "activity_name": "Unknown",
            "url": target_url or "N/A",
            "status": "error",
            "response_code": None,
            "response_time": time.time() - check_start_time,
            "error_message": str(e),
            "is_simulated": False,
            "severity": 7,
            "retry_count": 0,
            "source": "selenium"
        }
        alert_events.append(alert_event)
        report_data.append([target_url or "N/A", None, "Error", str(e)])
    
    finally:
        driver.quit()


def extract_activity_name(activity_url):
    """Extract activity name from URL"""
    
    mapping = {
        "activity1.html": "Account Verification",
        "activity2.html": "Transaction Review",
        "activity3.html": "Loan Application Check",
        "activity4.html": "Customer Service Check",
        "activity5.html": "Compliance Audit",
        "activity6.html": "Security Scan",
        "activity7.html": "Performance Metrics"
    }
    
    for key, value in mapping.items():
        if key in activity_url:
            return value
    
    return "Unknown Activity"


def main():
    """Main execution"""
    
    print("=" * 60)
    print("🤖 Alert Engine - Enhanced Selenium Health Check")
    print("=" * 60)
    
    # Get execution parameters
    execution_id = os.getenv('EXECUTION_ID', f"exec_{int(time.time())}")
    defects_enabled = os.getenv('DEFECTS_ENABLED', 'true').lower() == 'true'
    
    print(f"\n📊 Execution Configuration:")
    print(f"  ├─ Execution ID: {execution_id}")
    print(f"  ├─ Defects Enabled: {'✓ Yes' if defects_enabled else '✗ No'}")
    print(f"  └─ Start Time: {datetime.now().isoformat()}")
    
    # Initialize components
    defect_injector = DefectInjector(enabled=defects_enabled)
    db = AlertDatabase()
    
    print(f"\n⚙️  Defect Configuration:")
    stats = defect_injector.get_defect_stats()
    print(f"  ├─ Total Injection Percentage: {stats['total_injection_percentage']}%")
    print(f"  ├─ Defect Types: {', '.join(stats['defect_types'][:3])}...")
    
    # Open main page
    main_driver = webdriver.Chrome()
    main_driver.maximize_window()
    main_driver.get("http://127.0.0.1:5502/nvsbank/index.html")
    
    wait = WebDriverWait(main_driver, 10)
    
    print(f"\n🔍 Discovering activities...")
    
    # Get activity URLs
    check_buttons = main_driver.find_elements(By.XPATH, "//a[@class='check-btn']")
    activity_urls = [btn.get_attribute("href") for btn in check_buttons]
    
    print(f"  ├─ Found {len(activity_urls)} activities")
    
    # Shared data structures
    report_data = []
    alert_events = []
    
    # Run checks in parallel
    print(f"\n▶️  Running {len(activity_urls)} health checks...")
    print("=" * 60)
    
    threads = []
    for i, url in enumerate(activity_urls, start=1):
        t = threading.Thread(
            target=run_check,
            args=(url, i, report_data, alert_events, execution_id, defect_injector)
        )
        threads.append(t)
        t.start()
    
    # Wait for completion
    for t in threads:
        t.join()
    
    print("\n" + "=" * 60)
    print(f"✓ All {len(activity_urls)} checks completed")
    print("=" * 60)
    
    # Save alerts to database
    print(f"\n💾 Saving results...")
    for alert in alert_events:
        db.add_alert(alert)
    
    # Generate Excel report
    wb = Workbook()
    ws = wb.active
    ws.title = "Link Check Report"
    ws.append(["Site Name", "Response Code", "Status", "Reason"])
    
    for row in report_data:
        ws.append(row)
    
    try:
        wb.save("link_check_report.xlsx")
        print(f"  ├─ Excel report: ✓")
    except PermissionError:
        wb.save("link_check_report_new.xlsx")
        print(f"  ├─ Excel report (alternate): ✓")
    
    # Save alert events to JSON
    with open("raw_alerts.json", "w") as f:
        json.dump(alert_events, f, indent=2)
    print(f"  ├─ Raw alerts: ✓")
    
    # Refresh main page
    main_driver.refresh()
    print(f"  └─ Dashboard refresh: ✓")
    
    # Summary statistics
    print(f"\n📈 Summary Statistics:")
    stats = db.get_alert_statistics(hours=24)
    print(f"  ├─ Total Alerts: {stats['total']}")
    print(f"  ├─ By Status:")
    for status, count in stats['by_status'].items():
        print(f"  │   ├─ {status.capitalize()}: {count}")
    print(f"  ├─ High Score (>70): {stats['high_score_alerts']}")
    print(f"  └─ Test Defects: {stats['simulated_defects']}")
    
    print(f"\n✅ Health check cycle completed at {datetime.now().isoformat()}")
    
    input("Press Enter to exit...")
    main_driver.quit()


if __name__ == "__main__":
    main()
