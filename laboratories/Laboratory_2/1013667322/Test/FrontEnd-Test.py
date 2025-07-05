import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_report_generator import PDFReportGenerator

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
    task_description = "Terminar laboratorio"
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys(task_description)
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
    task_result = driver.find_element(By.ID, "task-result").text
    print("Texto en task_result:", task_result)
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    return task_id, task_description

def ver_tareas(driver, task_description):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert task_description in tasks

def eliminar_datos_prueba(driver, wait, user_id, task_id, report):
    # Delete task
    task_delete_input = driver.find_element(By.ID, "task-id-to-delete")
    task_delete_input.send_keys(task_id)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Eliminar Tarea']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "delete-task-result"), "✅"))
    delete_task_result = driver.find_element(By.ID, "delete-task-result").text
    assert "✅" in delete_task_result
    report.add_line(f"Cleanup: Task {task_id} deleted successfully.")
    print(f"✅ Cleanup: Task {task_id} deleted.")

    # Delete user
    user_delete_input = driver.find_element(By.ID, "user-id-to-delete")
    user_delete_input.send_keys(user_id)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Eliminar Usuario']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "delete-user-result"), "✅"))
    delete_user_result = driver.find_element(By.ID, "delete-user-result").text
    assert "✅" in delete_user_result
    report.add_line(f"Cleanup: User {user_id} deleted successfully.")
    print(f"✅ Cleanup: User {user_id} deleted.")

def verificar_eliminacion(driver, task_description, report):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    assert task_description not in tasks
    report.add_line(f"Verification: Task '{task_description}' confirmed to be deleted.")
    print(f"✅ Verification: Task '{task_description}' no longer in list.")

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    report = PDFReportGenerator("Frontend E2E Test Report")
    user_id = None
    task_id = None
    task_description = ""

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        report.add_line("Frontend opened.")

        user_id = crear_usuario(driver, wait)
        report.add_line(f"User created with ID: {user_id}")

        task_id, task_description = crear_tarea(driver, wait, user_id)
        report.add_line(f"Task '{task_description}' created with ID: {task_id} for user {user_id}")

        ver_tareas(driver, task_description)
        report.add_line(f"Verification: Task '{task_description}' found in the list.")

        report.add_line("Test flow completed successfully before cleanup.")

    finally:
        if user_id and task_id:
            eliminar_datos_prueba(driver, wait, user_id, task_id, report)
            verificar_eliminacion(driver, task_description, report)

        report.generate("d:\\01_Actuales\\unal\\Laboratory2\\Laboratory_2\\1013667322\\Test\\reports")
        print("✅ PDF report generated.")
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
