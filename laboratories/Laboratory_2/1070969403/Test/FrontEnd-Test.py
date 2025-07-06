import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    print("Resultado usuario:")
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
    print("Texto en task_result:")
    assert "Tarea creada con ID" in task_result.text

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def delete_user_api(user_id):
    USERS_URL = "http://localhost:5001/users"
    response = requests.delete(f"{USERS_URL}/{user_id}")
    return response.status_code == 200

def delete_task_api(task_id):
    TASKS_URL = "http://localhost:5002/tasks"
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    return response.status_code == 200

def get_tasks_api():
    TASKS_URL = "http://localhost:5002/tasks"
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def get_users_api():
    USERS_URL = "http://localhost:5001/users"
    response = requests.get(USERS_URL)
    response.raise_for_status()
    return response.json()

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(lines):
    existing = [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in existing if f.split("_")[1].split(".")[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(REPORTS_DIR, f"report_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"FrontEnd Integration Test Report #{next_num}")
    y -= 30
    for line in lines:
        c.drawString(40, y, line)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    print(f"PDF report generated: {filename}")

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    report_lines = []
    user_id = None
    task_id = None
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        report_lines.append(f"User created with ID: {user_id}")
        crear_tarea(driver, wait, user_id)
        report_lines.append("Task created for user.")
        ver_tareas(driver)
        report_lines.append("Task verified in UI.")
        # Find the task ID via API for cleanup
        tasks = get_tasks_api()
        user_tasks = [t for t in tasks if str(t["user_id"]) == str(user_id)]
        if user_tasks:
            task_id = user_tasks[-1]["id"]  # Assume last created
            report_lines.append(f"Task ID for cleanup: {task_id}")
        else:
            report_lines.append("Could not find created task for cleanup.")
        time.sleep(2)
    except Exception as e:
        report_lines.append(f"Test failed: {e}")
        raise
    finally:
        cleanup_ok = True
        # Cleanup: delete task and user via API
        if task_id:
            if delete_task_api(task_id):
                report_lines.append(f"Task {task_id} deleted.")
            else:
                report_lines.append(f"Task {task_id} could not be deleted.")
                cleanup_ok = False
        if user_id:
            if delete_user_api(user_id):
                report_lines.append(f"User {user_id} deleted.")
            else:
                report_lines.append(f"User {user_id} could not be deleted.")
                cleanup_ok = False
        # Verify deletion
        tasks = get_tasks_api()
        users = get_users_api()
        if task_id and not any(t["id"] == int(task_id) for t in tasks):
            report_lines.append(f"Task {task_id} properly deleted.")
        else:
            report_lines.append(f"Task {task_id} still present after deletion!")
            cleanup_ok = False
        if user_id and not any(str(u["id"]) == str(user_id) for u in users):
            report_lines.append(f"User {user_id} properly deleted.")
        else:
            report_lines.append(f"User {user_id} still present after deletion!")
            cleanup_ok = False
        generate_pdf_report(report_lines)
        if cleanup_ok:
            print("Data cleanup verified.")
        else:
            print("Data cleanup failed.")
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
