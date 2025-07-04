import time
import requests
from generate_report import generate_pdf_report
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TASKS_API = "http://localhost:5002/tasks"
USERS_API = "http://localhost:5001/users"

created_task_id = None  # Global variable to track task ID
created_user_id = None

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    global created_user_id
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    created_user_id = ''.join(filter(str.isdigit, user_result))
    return created_user_id

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
    task_id = ''.join(filter(str.isdigit, task_result))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    assert "Terminar laboratorio" in tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_API}/{task_id}")
    assert response.status_code == 204

def delete_user(user_id):
    response = requests.delete(f"{USERS_API}/{user_id}")
    assert response.status_code == 204

def verificar_eliminacion(task_id):
    tasks = requests.get(TASKS_API).json()
    assert all(t["id"] != int(task_id) for t in tasks)

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 10)

    results = []

    try:
        abrir_frontend(driver)
        results.append("✅ Frontend cargado correctamente")

        user_id = crear_usuario(driver, wait)
        results.append(f"✅ Usuario creado desde frontend con ID: {user_id}")

        created_task_id = crear_tarea(driver, wait, user_id)
        results.append(f"✅ Tarea creada desde frontend con ID: {created_task_id}")

        ver_tareas(driver)
        results.append("✅ Lista de tareas verificada")

    except Exception as e:
        results.append(f"❌ Error durante la prueba frontend: {str(e)}")

    finally:
        driver.quit()

        try:
            if created_task_id:
                delete_task(created_task_id)
                results.append(f"✅ Tarea {created_task_id} eliminada")

            if created_user_id:
                delete_user(created_user_id)
                results.append(f"✅ Usuario {created_user_id} eliminado")

            if created_task_id:
                verificar_eliminacion(created_task_id)
                results.append("✅ Verificación de limpieza correcta")
        except Exception as e:
            results.append(f"❌ Error al limpiar/verificar datos: {str(e)}")

        generate_pdf_report(results)

if __name__ == "__main__":
    main()
