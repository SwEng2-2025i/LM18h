import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF
import os
from datetime import datetime

# API endpoints
USERS_API = "http://localhost:5001/users"
TASKS_API = "http://localhost:5002/tasks"

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Frontend Test Report', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

def create_report(test_results):
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)


    report_number = 1
    while os.path.exists(os.path.join(REPORTS_DIR, f'frontend_report_{report_number}.pdf')):
        report_number += 1

    pdf = PDFReport()
    pdf.add_page()
    pdf.chapter_title(f'Frontend Test Report #{report_number}')
    pdf.chapter_body(f'Test Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    pdf.chapter_title('Test Results:')
    for step, result in test_results.items():
        pdf.chapter_body(f'{step}: {result}')

    pdf.output(os.path.join(REPORTS_DIR, f'frontend_report_{report_number}.pdf'))
    print(f"✅ Frontend report saved as reports/frontend_report_{report_number}.pdf")

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
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

    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def task_exists(task_id):
    try:
        response = requests.get(f"{TASKS_API}/{task_id}")
        return response.status_code == 200
    except Exception:
        return False

def user_exists(user_id):
    try:
        response = requests.get(f"{USERS_API}/{user_id}")
        return response.status_code == 200
    except Exception:
        return False

def delete_task(task_id):
    try:
        response = requests.delete(f"{TASKS_API}/{task_id}")
        return response.status_code == 200
    except Exception:
        return False

def delete_user(user_id):
    try:
        response = requests.delete(f"{USERS_API}/{user_id}")
        return response.status_code == 200
    except Exception:
        return False

def main():
    test_results = {}
    user_id = None
    task_id = None
    driver = None

    try:
        options = Options()
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        abrir_frontend(driver)
        test_results["Frontend Load"] = "Success"

        user_id = crear_usuario(driver, wait)
        test_results["User Creation"] = f"Success (ID: {user_id})"

        task_id = crear_tarea(driver, wait, user_id)
        test_results["Task Creation"] = f"Success (ID: {task_id})"

        if user_exists(user_id):
            test_results["User Exists"] = "Success (User found)"
        else:
            test_results["User Exists"] = "Failed (User not found)"

        if task_exists(task_id):
            test_results["Task Exists"] = "Success (Task found)"
        else:
            test_results["Task Exists"] = "Failed (Task not found)"

        if delete_user(user_id):
            test_results["User Deletion"] = "Success"
        else:
            test_results["User Deletion"] = "Failed"

        if delete_task(task_id):
            test_results["Task Deletion"] = "Success"
        else:
            test_results["Task Deletion"] = "Failed"

        if not user_exists(user_id):
            test_results["User Not Exists"] = "Success (User no longer exists)"
        else:
            test_results["User Not Exists"] = "Failed (User still exists)"

        if not task_exists(task_id):
            test_results["Task Not Exists"] = "Success (Task no longer exists)"
        else:
            test_results["Task Not Exists"] = "Failed (Task still exists)"

        test_results["Overall Result"] = "SUCCESS"
        print("✅ Frontend test completed successfully")

    except Exception as e:
        test_results["Overall Result"] = f"FAILED: {str(e)}"
        print(f"❌ Frontend test failed: {str(e)}")

    finally:
        if driver:
            driver.quit()

    create_report(test_results)

if __name__ == "__main__":
    main()