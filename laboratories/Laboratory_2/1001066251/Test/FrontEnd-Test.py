import time
import requests
import os
import io
import contextlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

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

    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

# Funciones para limpieza y reporte

# Deletes a user via API and verifies deletion
def delete_user_via_api(user_id):
    url = f"http://localhost:5001/users/{user_id}"
    requests.delete(url).raise_for_status()
    print(f"User with ID {user_id} deleted.")
    # Verification
    response = requests.get(url)
    assert response.status_code == 404, "User cleanup verification failed."
    print(f"✅ Verification: User {user_id} confirmed deleted.")

# Deletes a task via API and verifies deletion
def delete_task_via_api(task_id):
    url = f"http://localhost:5002/tasks/{task_id}"
    requests.delete(url).raise_for_status()
    print(f"Task with ID {task_id} deleted via API")
    # Verification
    response = requests.get(url)
    assert response.status_code == 404, "Task cleanup verification failed."
    print(f"✅ Verification: Task {task_id} confirmed deleted.")

# Generates a PDF report with the test results
def generate_pdf_report(content, test_name="Frontend_Test"):
    report_num = 1
    while os.path.exists(f"{test_name}_Report_{report_num}.pdf"):
        report_num += 1
    file_name = f"{test_name}_Report_{report_num}.pdf"
    
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, f"Test Report: {test_name}")
    c.setFont("Helvetica", 10)
    text = c.beginText(inch, height - 1.5 * inch)
    text.setFont("Courier", 9)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()

    print(f"Report saved as: {file_name}")

def main():
    options = Options()
    # options.add_argument('--headless')
    driver = None
    user_id = None
    task_id = None
    output_capture = io.StringIO()

    with contextlib.redirect_stdout(output_capture):
        try:
            driver = webdriver.Chrome(options=options)
            wait = WebDriverWait(driver, 10)
            abrir_frontend(driver)
            user_id = crear_usuario(driver, wait)
            task_id = crear_tarea(driver, wait, user_id) # Captura el ID de la tarea
            ver_tareas(driver)
            time.sleep(3)
            print("\n✅ Frontend E2E test completed successfully.")
        except Exception as e:
            print(f"\n❌ E2E TEST FAILED: {e}")
        finally:
            if driver:
                driver.quit()
                print("Browser closed.")
            
            # Bloque de limpieza robusto
            print("\n--- Starting cleanup ---")
            if task_id:
                try:
                    delete_task_via_api(task_id)
                except Exception as e:
                    print(f"❌ FAILED to delete task {task_id}: {e}")
            if user_id:
                try:
                    delete_user_via_api(user_id)
                except Exception as e:
                    print(f"❌ FAILED to delete user {user_id}: {e}")
            print("Cleanup phase finished.")

    # Al final, imprime la salida capturada y genera el reporte
    test_output = output_capture.getvalue()
    print(test_output)
    generate_pdf_report(test_output)

if __name__ == "__main__":
    main()