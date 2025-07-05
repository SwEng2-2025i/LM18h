# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# #----------------------------------------------------------
# #------------------ FRONTEND SERVICE ----------------------
# #----------------------------------------------------------


# def abrir_frontend(driver):
#     # Opens the frontend application in the browser
#     driver.get("http://localhost:5000")
#     time.sleep(2)  # Give the page time to load

# def crear_usuario(driver, wait):
#     # Fills out the user creation form and submits it
#     # Then retrieves and returns the newly created user ID
#     username_input = driver.find_element(By.ID, "username")
#     username_input.send_keys("Ana")
#     time.sleep(1)
#     driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
#     time.sleep(2)

#     user_result = driver.find_element(By.ID, "user-result").text
#     print("Resultado usuario:", user_result)
#     assert "Usuario creado con ID" in user_result
#     user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
#     return user_id

# def crear_tarea(driver, wait, user_id):
#     # Fills out the task creation form with a task and user ID, then submits it
#     # Waits until the confirmation text appears and asserts the result
#     task_input = driver.find_element(By.ID, "task")
#     task_input.send_keys("Terminar laboratorio")
#     time.sleep(1)

#     userid_input = driver.find_element(By.ID, "userid")
#     userid_input.send_keys(user_id)
#     userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
#     time.sleep(1)

#     crear_tarea_btn = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
#     )
#     crear_tarea_btn.click()
#     time.sleep(2)

#     wait.until(
#         EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
#     )
#     task_result = driver.find_element(By.ID, "task-result")
#     print("Texto en task_result:", task_result.text)
#     assert "Tarea creada con ID" in task_result.text

# def ver_tareas(driver):
#     # Clicks the button to refresh the task list and verifies the new task appears
#     driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
#     time.sleep(2)

#     tasks = driver.find_element(By.ID, "tasks").text
#     print("Tareas:", tasks)
#     assert "Terminar laboratorio" in tasks

# def main():
#     # Main test runner that initializes the browser and runs the full E2E flow
#     options = Options()
#     # options.add_argument('--headless')  # Uncomment for headless mode
#     driver = webdriver.Chrome(options=options)

#     try:
#         wait = WebDriverWait(driver, 10)
#         abrir_frontend(driver)
#         user_id = crear_usuario(driver, wait)
#         crear_tarea(driver, wait, user_id)
#         ver_tareas(driver)
#         time.sleep(3)  # Final delay to observe results if not running headless
#     finally:
#         driver.quit()  # Always close the browser at the end

# if __name__ == "__main__":
#     main()


# ./Test/FrontEnd-Test.py

# ./Test/FrontEnd-Test.py

import time
import os
import re
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

#----------------------------------------------------------
#------------------ FRONTEND TEST -------------------------
#----------------------------------------------------------

# --- CONFIGURACIÓN ---
FRONTEND_URL = "http://localhost:5000"
USERS_API_URL = "http://localhost:5001/users"
TASKS_API_URL = "http://localhost:5002/tasks"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')

# --- FUNCIONES PARA GENERAR REPORTES PDF ---
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

# --- LÓGICA DEL TEST ---
def run_e2e_test():
    logs = []
    created_user_id = None
    created_task_id = None
    
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Open Frontend
        logs.append("STEP 1: Opening frontend application...")
        driver.get(FRONTEND_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Laboratorio de Integración" in driver.title
        logs.append("  -> SUCCESS: Frontend opened successfully.")

        # Step 2: Create User
        username = "Ana E2E"
        logs.append(f"\nSTEP 2: Creating user '{username}'...")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.XPATH, "//button[text()='Crear Usuario']").click()
        
        wait.until(
            EC.text_to_be_present_in_element((By.ID, "user-result"), "Usuario creado con ID")
        )
        user_result_text = driver.find_element(By.ID, "user-result").text
        created_user_id = ''.join(filter(str.isdigit, user_result_text))
        logs.append(f"  -> SUCCESS: User created with ID {created_user_id}.")

        # Step 3: Create Task
        task_title = "Terminar prueba E2E"
        logs.append(f"\nSTEP 3: Creating task '{task_title}' for user ID {created_user_id}...")
        driver.find_element(By.ID, "task").send_keys(task_title)
        driver.find_element(By.ID, "userid").send_keys(created_user_id)
        driver.find_element(By.XPATH, "//button[text()='Crear Tarea']").click()
        
        wait.until(
            EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
        )
        task_result_text = driver.find_element(By.ID, "task-result").text
        created_task_id = ''.join(filter(str.isdigit, task_result_text))
        logs.append(f"  -> SUCCESS: Task created with ID {created_task_id}.")

        # Step 4: Verify Task in List
        logs.append("\nSTEP 4: Verifying task appears in the list...")
        driver.find_element(By.XPATH, "//button[text()='Actualizar lista de tareas']").click()
        
        tasks_list = wait.until(
            EC.presence_of_element_located((By.ID, "tasks"))
        )
        time.sleep(1) # Wait for list to populate
        
        expected_text = f"{task_title} (Usuario ID: {created_user_id})"
        assert expected_text in tasks_list.text, f"Task '{expected_text}' not found in list."
        logs.append("  -> SUCCESS: Task is visible in the UI list.")

        logs.append("\n✅ ALL TESTS PASSED")

    except Exception as e:
        logs.append(f"\n❌ TEST FAILED: {e}")
        # Tomar captura de pantalla en caso de error
        screenshot_path = os.path.join(REPORTS_DIR, 'error_screenshot.png')
        if not os.path.exists(REPORTS_DIR):
            os.makedirs(REPORTS_DIR)
        driver.save_screenshot(screenshot_path)
        logs.append(f"  -> Screenshot saved to {screenshot_path}")

    finally:
        # Step 5: Data Cleanup via API
        logs.append("\n--- CLEANUP ---")
        if created_task_id:
            logs.append(f"CLEANUP: Deleting task ID {created_task_id} via API...")
            response = requests.delete(f"{TASKS_API_URL}/{created_task_id}")
            if response.status_code == 200:
                logs.append("  -> SUCCESS: Task deleted.")
                # --- FIX: Wait for the database to update ---
                time.sleep(0.5) 
                # --------------------------------------------
                verify_resp = requests.get(f"{TASKS_API_URL}/{created_task_id}")
                assert verify_resp.status_code == 404, f"Task deletion verification failed. Expected 404, got {verify_resp.status_code}"
                logs.append("  -> VERIFIED: Task no longer exists.")
            else:
                logs.append(f"  -> FAILED: Could not delete task (Status {response.status_code}).")

        if created_user_id:
            logs.append(f"CLEANUP: Deleting user ID {created_user_id} via API...")
            response = requests.delete(f"{USERS_API_URL}/{created_user_id}")
            if response.status_code == 200:
                logs.append("  -> SUCCESS: User deleted.")
                # --- FIX: Wait for the database to update ---
                time.sleep(0.5)
                # --------------------------------------------
                verify_resp = requests.get(f"{USERS_API_URL}/{created_user_id}")
                assert verify_resp.status_code == 404, f"User deletion verification failed. Expected 404, got {verify_resp.status_code}"
                logs.append("  -> VERIFIED: User no longer exists.")
            else:
                logs.append(f"  -> FAILED: Could not delete user (Status {response.status_code}).")

        # Close browser and generate report
        driver.quit()
        report_filename = get_next_report_filename()
        generate_pdf_report(report_filename, logs)

if __name__ == "__main__":
    run_e2e_test()