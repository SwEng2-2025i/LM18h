import time

import requests

from pdf_report import pdf_report
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_API = "http://localhost:5001/users"
TASK_API = "http://localhost:5002/tasks"

user_id_created = None
task_id_created = None



def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    global user_id_created
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    user_id_created = user_id
    return user_id_created

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
    #print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result
    return ''.join(filter(str.isdigit, task_result))


def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def delete_user(user_id):
    response = requests.delete(f"{USER_API}/{user_id}")
    assert response.status_code == 204

def delete_task(task_id):
    response = requests.delete(f"{TASK_API}/{task_id}")
    assert response.status_code == 204

def verify_delete(task_id):
    tasks = requests.get(TASK_API).json()
    assert all(t["id"] != int(task_id) for t in tasks)

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 10)

    test_results = []

    try:
        abrir_frontend(driver)
        test_results.append("FrontEnd opened successfully.")
        user_id = crear_usuario(driver, wait)
        test_results.append(f"User created from FrontEnd: {user_id}.")
        task_id_created = crear_tarea(driver, wait, user_id)
        test_results.append(f"Task created from FrontEnd: {task_id_created}.")
        ver_tareas(driver)
        test_results.append("Task list verified successfully.")
        time.sleep(3)  # Final delay to observe results if not running headless

    except Exception as e:
        test_results.append(f"Error during FrontEnd testing: {str(e)}.")

    finally:
        driver.quit()  # Always close the browser at the end

        try:
            if task_id_created:
                delete_task(task_id_created)
                test_results.append(f"Task {task_id_created} deleted successfully.")
            if user_id_created:
                delete_user(user_id_created)
                test_results.append(f"User {user_id_created} deleted successfully.")
            if task_id_created:
                verify_delete(task_id_created)
                test_results.append(f"Verification completed successfully.")
        except Exception as e:
            test_results.append(f"Error verifying: {str(e)}.")

        pdf_report(test_results)

if __name__ == "__main__":
    main()
