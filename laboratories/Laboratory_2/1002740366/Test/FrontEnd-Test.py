import time
import os
import re
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

#----------------------------------------------------------
#---------------------- FRONTEND-TEST ---------------------
#----------------------------------------------------------

# --- CONFIGURATION ---
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
FRONTEND_URL = "http://localhost:5003"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')

# --- FUNCTIONS FOR PDF REPORT GENERATION ---
def get_next_report_filename(base_name="Frontend_Test_Report"):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    
    files = [f for f in os.listdir(REPORTS_DIR) if f.startswith(base_name) and f.endswith('.pdf')]
    if not files:
        return os.path.join(REPORTS_DIR, f"{base_name}_1.pdf")

    max_num = 0
    for f in files:
        match = re.search(r'_(\d+)\.pdf$', f)
        if match:
            max_num = max(max_num, int(match.group(1)))
            
    return os.path.join(REPORTS_DIR, f"{base_name}_{max_num + 1}.pdf")

def generate_pdf_report(filename, logs, test_name="Frontend E2E Test"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, test_name)
    
    c.setFont("Helvetica", 10)
    c.drawString(inch, height - inch - 20, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    c.line(inch, height - inch - 30, width - inch, height - inch - 30)
    
    text = c.beginText(inch, height - inch - 50)
    text.setFont("Courier", 9)
    
    for log in logs:
        text.textLine(log)
    
    c.drawText(text)
    c.save()
    print(f"✅ Report generated: {filename}")

# --- SELENIUM SETUP ---
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    return webdriver.Chrome(options=chrome_options)

# --- FRONTEND E2E TEST ---
def frontend_e2e_test():
    logs = []
    driver = None
    created_user_ids = []
    created_task_ids = []
    
    try:
        # Step 1: Setup Selenium WebDriver
        logs.append("STEP 1: Setting up Selenium WebDriver...")
        driver = setup_driver()
        logs.append("  -> SUCCESS: WebDriver initialized.")
        
        # Step 2: Navigate to frontend
        logs.append(f"\nSTEP 2: Navigating to frontend at {FRONTEND_URL}...")
        driver.get(FRONTEND_URL)
        wait = WebDriverWait(driver, 10)
        logs.append("  -> SUCCESS: Frontend loaded.")
        
        # Step 3: Create user through frontend
        logs.append(f"\nSTEP 3: Creating user through frontend...")
        user_name = "Frontend_Test_User_Lab2"
        
        user_name_input = wait.until(EC.presence_of_element_located((By.ID, "userName")))
        user_name_input.clear()
        user_name_input.send_keys(user_name)
        
        create_user_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]")
        create_user_btn.click()
        
        # Wait for result message
        time.sleep(2)
        result_div = driver.find_element(By.ID, "result")
        result_text = result_div.text
        
        if "✅" in result_text and "ID" in result_text:
            # Extract user ID from result message
            import re
            match = re.search(r'ID (\d+)', result_text)
            if match:
                user_id = int(match.group(1))
                created_user_ids.append(user_id)
                logs.append(f"  -> SUCCESS: User created with ID {user_id}")
            else:
                logs.append(f"  -> WARNING: User created but couldn't extract ID from: {result_text}")
        else:
            logs.append(f"  -> FAILED: User creation failed. Result: {result_text}")
            raise Exception(f"User creation failed: {result_text}")
        
        # Step 4: Create task through frontend
        logs.append(f"\nSTEP 4: Creating task through frontend...")
        task_title = "Frontend Test Task - Lab 2"
        
        task_title_input = driver.find_element(By.ID, "taskTitle")
        task_title_input.clear()
        task_title_input.send_keys(task_title)
        
        task_user_id_input = driver.find_element(By.ID, "taskUserId")
        task_user_id_input.clear()
        task_user_id_input.send_keys(str(user_id))
        
        create_task_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Tarea')]")
        create_task_btn.click()
        
        # Wait for result message
        time.sleep(2)
        result_div = driver.find_element(By.ID, "result")
        result_text = result_div.text
        
        if "✅" in result_text and "ID" in result_text:
            # Extract task ID from result message
            match = re.search(r'ID (\d+)', result_text)
            if match:
                task_id = int(match.group(1))
                created_task_ids.append(task_id)
                logs.append(f"  -> SUCCESS: Task created with ID {task_id}")
            else:
                logs.append(f"  -> WARNING: Task created but couldn't extract ID from: {result_text}")
        else:
            logs.append(f"  -> FAILED: Task creation failed. Result: {result_text}")
            raise Exception(f"Task creation failed: {result_text}")
        
        # Step 5: Verify task appears in task list
        logs.append(f"\nSTEP 5: Verifying task appears in task list...")
        load_tasks_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Cargar Tareas')]")
        load_tasks_btn.click()
        
        time.sleep(2)
        tasks_list = driver.find_element(By.ID, "tasksList")
        
        if str(task_id) in tasks_list.text and task_title in tasks_list.text:
            logs.append(f"  -> SUCCESS: Task ID {task_id} found in task list.")
        else:
            logs.append(f"  -> FAILED: Task ID {task_id} not found in task list.")
            logs.append(f"     Task list content: {tasks_list.text}")
            raise Exception("Task not found in task list")
        
        logs.append("\n✅ ALL FRONTEND TESTS PASSED")
        
    except Exception as e:
        logs.append(f"\n❌ FRONTEND TEST FAILED: {e}")
        
    finally:
        # Step 6: Cleanup WebDriver
        if driver:
            driver.quit()
            logs.append("\nWebDriver closed.")
        
        # Step 7: Data Cleanup via API calls
        logs.append("\n--- CLEANUP PHASE ---")
        
        # Clean up tasks first (foreign key dependency)
        for task_id in created_task_ids:
            logs.append(f"CLEANUP: Deleting task ID {task_id}...")
            try:
                response = requests.delete(f"{TASKS_URL}/{task_id}")
                if response.status_code == 200:
                    logs.append("  -> SUCCESS: Task deleted.")
                    # Verify deletion
                    verify_resp = requests.get(f"{TASKS_URL}/{task_id}")
                    if verify_resp.status_code == 404:
                         logs.append("  -> VERIFIED: Task no longer exists (404).")
                    else:
                         logs.append(f"  -> FAILED VERIFICATION: Task still exists (Status {verify_resp.status_code}).")
                else:
                    logs.append(f"  -> FAILED: Could not delete task (Status {response.status_code}).")
            except Exception as e:
                logs.append(f"  -> ERROR during task deletion: {e}")
        
        # Clean up users
        for user_id in created_user_ids:
            logs.append(f"CLEANUP: Deleting user ID {user_id}...")
            try:
                response = requests.delete(f"{USERS_URL}/{user_id}")
                if response.status_code == 200:
                    logs.append("  -> SUCCESS: User deleted.")
                    # Verify deletion
                    verify_resp = requests.get(f"{USERS_URL}/{user_id}")
                    if verify_resp.status_code == 404:
                         logs.append("  -> VERIFIED: User no longer exists (404).")
                    else:
                         logs.append(f"  -> FAILED VERIFICATION: User still exists (Status {verify_resp.status_code}).")
                else:
                    logs.append(f"  -> FAILED: Could not delete user (Status {response.status_code}).")
            except Exception as e:
                logs.append(f"  -> ERROR during user deletion: {e}")
        
        # Generate PDF Report (always executed)
        logs.append("\n--- REPORT GENERATION ---")
        try:
            report_filename = get_next_report_filename()
            generate_pdf_report(report_filename, logs)
            logs.append(f"PDF report saved: {report_filename}")
        except Exception as e:
            logs.append(f"ERROR generating PDF report: {e}")
            print(f"ERROR generating PDF report: {e}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("FRONTEND E2E TEST COMPLETED")
        print("="*60)
        for log in logs:
            print(log)
        print("="*60)

if __name__ == "__main__":
    print("Starting Frontend E2E Test with Data Cleanup and PDF Reporting...")
    print("Ensure that Users_Service (port 5001), Task_Service (port 5002), and Frontend (port 5003) are running.")
    print("Chrome WebDriver is required for this test.")
    frontend_e2e_test()
