import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from report_generator import generate_report

resultados = []

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

    if "Usuario creado con ID" in user_result:
        resultados.append(
            {
                "descripcion": "Crear usuario desde el Front End",
                "resultado": True
            }
        )
    else:
        resultados.append(
            {
                "descripcion": "Crear usuario desde el Front End",
                "resultado": False
            }
        )

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

    if "Tarea creada con ID" in task_result.text:
        resultados.append(
            {
                "descripcion": "Crear tarea desde el Front End",
                "resultado": True
            }
        )
    else:
        resultados.append(
            {
                "descripcion": "Crear tarea desde el Front End",
                "resultado": False
            }
        )

    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id


def eliminar_tarea(driver, wait, task_id):
    task_input = driver.find_element(By.ID, "task_id")
    task_input.send_keys(task_id)
    time.sleep(1)

    eliminar_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Eliminar Tarea']"))
    )
    eliminar_tarea_btn.click()

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-delete-result"), "Tarea eliminada")
    )
    task_delete_result = driver.find_element(By.ID, "task-delete-result")
    print("Texto en task_delete_result:", task_delete_result.text)
    assert "Tarea eliminada" in task_delete_result.text

def eliminar_usuario(driver, wait, user_id):
    user_input = driver.find_element(By.ID, "user_id")
    user_input.send_keys(user_id)
    time.sleep(1)

    eliminar_usuario_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Eliminar Usuario']"))
    )
    eliminar_usuario_btn.click()

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "user-delete-result"), "Usuario eliminado")
    )
    user_delete_result = driver.find_element(By.ID, "user-delete-result")
    print("Texto en user_delete_result:", user_delete_result.text)
    assert "Usuario eliminado" in user_delete_result.text

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

    if "Terminar laboratorio" in tasks:
        resultados.append(
            {
                "descripcion": "Visualizar tarea creada desde el Front End",
                "resultado": True
            }
        )
    else:
        resultados.append(
            {
                "descripcion": "Visualizar tarea creada desde el Front End",
                "resultado": False
            }
        )

def verificar_tarea_eliminada(task_id):
    tasks = requests.get(f"http://localhost:5002/tasks").json()

    if not any(t["id"] == task_id for t in tasks):
        return True
    return False  

def verificar_usuario_eliminado(user_id):
    users = requests.get(f"http://localhost:5001/users").json()

    if not any(u["id"] == user_id for u in users):
        return True
    return False 

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        eliminar_tarea(driver, wait, task_id)
        eliminar_usuario(driver, wait, user_id)

        resultados.append(
            {
                "descripcion": "Eliminación de la tarea creada",
                "resultado": True if verificar_tarea_eliminada(task_id) else False 
            }
        )

        resultados.append(
            {
                "descripcion": "Eliminación del usuario creado",
                "resultado": True if verificar_usuario_eliminado(user_id) else False 
                
            }
        )

        time.sleep(3)  # Final delay to observe results if not running headless

        generate_report("Test/Front End Test Reports", resultados, "Resultados test Front End", "Front_End_Report")
    finally:
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
