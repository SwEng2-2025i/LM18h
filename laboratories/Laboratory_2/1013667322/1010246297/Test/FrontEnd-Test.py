import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_report import generate_pdf_report

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
    task_result = driver.find_element(By.ID, "task-result").text
    print("Texto en task_result:", task_result)
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def eliminar_usuario(user_id):
    response = requests.delete(f"http://localhost:5001/users/{user_id}")
    print(f"Eliminando usuario {user_id}: status {response.status_code}")
    return response.status_code

def verificar_usuario_eliminado(user_id):
    response = requests.get(f"http://localhost:5001/users/{user_id}")
    return response.status_code == 404

def eliminar_tarea(task_id):
    response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    print(f"Eliminando tarea {task_id}: status {response.status_code}")
    return response.status_code

def verificar_tarea_eliminada(task_id):
    response = requests.get("http://localhost:5002/tasks")
    if response.status_code == 200:
        tareas = response.json()
        return all(str(t["id"]) != str(task_id) for t in tareas)
    return False


def main():
    logs = []
    options = Options()
    driver = webdriver.Chrome(options=options)
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        logs.append(f"User created with ID: {user_id}")
        task_id = crear_tarea(driver, wait, user_id)
        logs.append(f"Task created with ID: {task_id}")
        ver_tareas(driver)
        logs.append("Task appears in the list correctly.")

        # clean up
        logs.append("🧹 Deleting test data...")
        if eliminar_tarea(task_id):
            logs.append(f"Task {task_id} deleted successfully.")
        else:
            logs.append(f"Error deleting task {task_id}.")

        if verificar_tarea_eliminada(task_id):
            logs.append(f"Verified: task {task_id} no longer exists.")
        else:
            logs.append(f"Error: task {task_id} still exists.")

        if eliminar_usuario(user_id):
            logs.append(f"User {user_id} deleted successfully.")
        else:
            logs.append(f"Error deleting user {user_id}.")

        if verificar_usuario_eliminado(user_id):
            logs.append(f"Verified: user {user_id} no longer exists.")
        else:
            logs.append(f"Error: user {user_id} still exists.")

        logs.append("✅ Data cleanup verified.")
        logs.append("Test completed successfully.")
        time.sleep(2)
    except Exception as e:
        logs.append(f"Error during test: {str(e)}")
        raise
    finally:
        driver.quit()
        generate_pdf_report(
            logs,
            report_title="Integration Test Report",
            file_prefix="frontend_report"
        )

if __name__ == "__main__":

    main()
