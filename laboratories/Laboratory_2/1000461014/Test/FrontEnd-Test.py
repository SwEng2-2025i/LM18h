import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from report_generator import generate_pdf_report

TASK_DESCRIPTION = "Terminar laboratorio"
USER_NAME = "Ana"

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(USER_NAME)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result, "The user was not correctly registered"
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys(TASK_DESCRIPTION)
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
    assert "Tarea creada con ID" in task_result.text, "The task was not correctly registered"
    task_id = ''.join(filter(str.isdigit, task_result.text))  # Extract numeric ID from result
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert TASK_DESCRIPTION in tasks, "Task is not displayed in task list"

def eliminar_usuario(user_id):
    response = requests.delete(f"http://localhost:5001/users/{user_id}")
    response.raise_for_status()
    print(f"• User with ID {user_id} deleted")

def eliminar_tarea(task_id):
    response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    response.raise_for_status()
    print(f"• Task with ID {task_id} deleted")

def verificar_eliminacion_usuario_ui(driver, wait, user_id):
    # Fills out the task creation form with a task and the deleted user ID, then submits it
    # Waits until a text appears and verifies that the error indicates that the ID is invalid
    task_input = driver.find_element(By.ID, "task")
    task_input.clear()
    task_input.send_keys("Aprender la canción")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.clear()
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(5)

    try:
        wait.until(lambda d: d.find_element(By.ID, "task-result").text.strip() != "")
    except TimeoutException:
        raise AssertionError("There was no message when creating the task")
    
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)

    assert "ID de usuario inválido" in task_result.text, "User was not deleted correctly"


def verificar_eliminacion_tarea_ui(driver):
    # Clicks the button to refresh the task list and verifies that the test task is gone
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(5)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert TASK_DESCRIPTION not in tasks, "Task was not deleted from the list"

def verificar_eliminacion_usuario_api(user_id):
    response = requests.get(f"http://localhost:5001/users/{user_id}")
    assert response.status_code == 404, "User was not deleted correctly."

def verificar_eliminacion_tarea_api(task_id):
    response = requests.get(f"http://localhost:5001/tasks")

    if response.status_code == 200:
        tasks = response.json()
        assert all(t["id"] != task_id for t in tasks), "Task was not deleted correctly"

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    log = []
    status = "PASSED ✓"

    try:
        wait = WebDriverWait(driver, 10)
        log.append("=============================================")
        log.append("                TEST START                   ")
        log.append("=============================================")
        abrir_frontend(driver)
        log.append("• Frontend loaded")

        log.append("------------ Data Creation -----------------")
        user_id = crear_usuario(driver, wait)
        log.append(f"User created with ID {user_id}")

        task_id = crear_tarea(driver, wait, user_id)
        log.append(f"Task created with ID {task_id} for user {user_id}")

        ver_tareas(driver)
        log.append("✓ Task displayed successfully in task list")

        
        log.append("------------ Data Cleanup -----------------")
        eliminar_tarea(task_id)
        verificar_eliminacion_tarea_ui(driver)
        log.append(f"• Task with ID {task_id} is not displayed in the list")
        
        verificar_eliminacion_tarea_api(task_id)
        log.append(f"Task with ID {task_id} deleted")

        eliminar_usuario(user_id)
        verificar_eliminacion_usuario_api(user_id)
        log.append(f"User with ID {user_id} deleted")

        verificar_eliminacion_usuario_ui(driver, wait, user_id)
        log.append(f"• ID ({task_id}) of deleted user is not valid anymore")
        
        log.append("✓ Data cleanup was completed successfully")

        time.sleep(3)  # Final delay to observe results if not running headless
    
    except Exception as e:
        status = "FAILED ✘"
        log.append(f"✘ Test failed: {e}")
    
    finally:
        log.append("=============================================")
        log.append("              TEST COMPLETED")
        log.append("=============================================")
        driver.quit()  # Always close the browser at the end
        generate_pdf_report(log, status, prefix="frontend")

if __name__ == "__main__":
    main()
