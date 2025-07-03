import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_generator import PDFReport
from datetime import datetime

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)
    return "Frontend opened successfully"

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
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
    task_result = driver.find_element(By.ID, "task-result").text
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result.split("ID")[1]))
    return task_id

def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    assert "Terminar laboratorio" in tasks
    return tasks

def aceptar_alerta(driver):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass  # No alert = no problem

def limpiar_datos(driver, user_id, task_id):
    # Delete task
    driver.find_element(By.ID, "delete-task-id").send_keys(task_id)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Tarea')]").click()
    aceptar_alerta(driver)
    time.sleep(1)

    # Delete user
    driver.find_element(By.ID, "delete-user-id").send_keys(user_id)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Usuario')]").click()
    aceptar_alerta(driver)
    time.sleep(1)

    # Verify cleanup
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    assert str(task_id) not in tasks

def clean_text(text):
    # Elimina emojis no compatibles con latin-1
    return text.replace("✅", "OK").replace("❌", "FAIL")

def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    report = PDFReport()
    report.add_page()
    report.chapter_title("Frontend Test Report")
    test_start = datetime.now().strftime("%Y-%m-%d %H-%M-%S")  # avoid ":" for file paths

    try:
        wait = WebDriverWait(driver, 10)

        # Test steps
        report.log_step(clean_text(abrir_frontend(driver)))
        user_id = crear_usuario(driver, wait)
        report.log_step(clean_text(f"User created with ID: {user_id}"))
        task_id = crear_tarea(driver, wait, user_id)
        report.log_step(clean_text(f"Task created with ID: {task_id}"))
        ver_tareas(driver)
        report.log_step("Tasks verified successfully")

        # Cleanup
        report.chapter_title("Cleanup Phase")
        limpiar_datos(driver, user_id, task_id)
        report.log_step("Data cleanup completed successfully")

        report.log_test_result(True)
        print("OK Frontend test completed successfully")

    except Exception as e:
        report.log_step(f"Test failed: {str(e)}")
        report.log_test_result(False)
        print(f"FAIL Test failed: {str(e)}")
        raise
    finally:
        driver.quit()
        report.output(f"reports/frontend_test_report_{test_start}.pdf")

if __name__ == "__main__":
    main()
