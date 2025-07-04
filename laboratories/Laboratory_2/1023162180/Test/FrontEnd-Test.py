import os
from datetime import datetime
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def next_report_number():
    files = [f for f in os.listdir(REPORTS_DIR) if f.startswith("frontend_report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[2].split(".")[0]) for f in files if f.split("_")[2].split(".")[0].isdigit()]
    return max(nums, default=0) + 1

def sanitize_line(line):
    return (
        line.replace("✅", "[OK]")
            .replace("❌", "[FAIL]")
    )

def generate_pdf_report(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Front-End Integration Test Report", ln=True, align="C")
    pdf.cell(0, 10, f"Date: {datetime.now()}", ln=True)
    pdf.ln(5)
    for line in results:
        pdf.multi_cell(0, 10, sanitize_line(line))
    report_num = next_report_number()
    filename = os.path.join(REPORTS_DIR, f"frontend_report_{report_num}.pdf")
    pdf.output(filename)
    print(f"PDF report generated: {filename}")

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def frontend_integration_test():
    results = []
    user_name = "TestUser_FE"
    task_title = "TestTask_FE"
    driver = webdriver.Chrome()  # Or Firefox, Edge, etc.
    driver.get("http://localhost:5000")  # Adjust to your front-end URL

    try:
        # Create user
        user_input = driver.find_element(By.ID, "user-name-input")
        user_input.clear()
        user_input.send_keys(user_name)
        driver.find_element(By.ID, "create-user-btn").click()
        time.sleep(1)
        results.append(f"User '{user_name}' created via UI.")

        # Create task for user
        task_input = driver.find_element(By.ID, "task-title-input")
        task_input.clear()
        task_input.send_keys(task_title)
        # Select user if needed
        # driver.find_element(By.ID, "user-select").select_by_visible_text(user_name)
        driver.find_element(By.ID, "create-task-btn").click()
        time.sleep(1)
        results.append(f"Task '{task_title}' created via UI.")

        # Verify task appears in UI
        tasks = driver.find_elements(By.XPATH, f"//*[contains(text(), '{task_title}')]")
        assert tasks, "❌ Task not found in UI after creation"
        results.append("Task appears in UI after creation.")

    except Exception as e:
        results.append(f"❌ Test failed: {str(e)}")
    finally:
        # Cleanup: Delete created task and user via UI
        cleanup_ok = True
        try:
            # Delete task
            delete_task_btns = driver.find_elements(By.XPATH, f"//tr[td[contains(text(), '{task_title}')]]//button[contains(@class, 'delete-task')]")
            for btn in delete_task_btns:
                btn.click()
                time.sleep(0.5)
            results.append(f"Task '{task_title}' deleted via UI.")

            # Delete user
            delete_user_btns = driver.find_elements(By.XPATH, f"//tr[td[contains(text(), '{user_name}')]]//button[contains(@class, 'delete-user')]")
            for btn in delete_user_btns:
                btn.click()
                time.sleep(0.5)
            results.append(f"User '{user_name}' deleted via UI.")

            # Verify deletion
            driver.refresh()
            time.sleep(1)
            tasks = driver.find_elements(By.XPATH, f"//*[contains(text(), '{task_title}')]")
            users = driver.find_elements(By.XPATH, f"//*[contains(text(), '{user_name}')]")
            if tasks:
                results.append(f"❌ Task '{task_title}' was NOT deleted.")
                cleanup_ok = False
            else:
                results.append(f"✅ Task '{task_title}' was deleted.")

            if users:
                results.append(f"❌ User '{user_name}' was NOT deleted.")
                cleanup_ok = False
            else:
                results.append(f"✅ User '{user_name}' was deleted.")

            if cleanup_ok:
                results.append("✅ Data cleanup verified.")
            else:
                results.append("❌ Data cleanup failed.")

        except Exception as e:
            results.append(f"❌ Cleanup failed: {str(e)}")

        driver.quit()
        generate_pdf_report(results)

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        time.sleep(3)  # Final delay to observe results if not running headless
    finally:
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
    frontend_integration_test()
