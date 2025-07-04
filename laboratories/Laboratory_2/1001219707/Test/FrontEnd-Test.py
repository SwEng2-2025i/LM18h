import time, re, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_utils import generate_pdf_report
import traceback

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

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
    # task_result = driver.find_element(By.ID, "task-result")
    task_result_text = driver.find_element(By.ID, "task-result").text
    print("Texto en task_result:", task_result_text)
    assert "Tarea creada con ID" in task_result_text
    task_id = int(re.findall(r'\d+', task_result_text)[0])          # ← EXTRAER ID
    return task_id                                             # ← DEVOLVER ID

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks
    return driver.find_element(By.ID, "tasks").text


def delete_task(task_id: int):
    r = requests.delete(f"{TASKS_URL}/{task_id}")
    assert r.status_code == 200, "No se pudo eliminar la tarea"
    assert requests.get(f"{TASKS_URL}/{task_id}").status_code == 404, \
           "La tarea aún existe tras el borrado"

def delete_user(user_id: int):
    r = requests.delete(f"{USERS_URL}/{user_id}")
    assert r.status_code == 200, "No se pudo eliminar el usuario"
    assert requests.get(f"{USERS_URL}/{user_id}").status_code == 404, \
           "El usuario aún existe tras el borrado"

baseline_users = {u["id"] for u in requests.get(USERS_URL).json()}
baseline_tasks = {t["id"] for t in requests.get(TASKS_URL).json()}

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    results = []

    user_id = task_id = None

    # try:
    #     wait = WebDriverWait(driver, 10)
    #     abrir_frontend(driver)
    #     user_id = crear_usuario(driver, wait)
    #     task_id = crear_tarea(driver, wait, user_id)
    #     ver_tareas(driver)
    #     time.sleep(3)  # Final delay to observe results if not running headless
    # finally:
    #     # ---------- limpieza ----------
    #     if task_id:
    #         delete_task(task_id)
    #         print(f"Task {task_id} eliminada correctamente")
    #     if user_id:
    #         delete_user(user_id)
    #         print(f"User {user_id} eliminado correctamente")
    #     driver.quit()  # Always close the browser at the end

    #     assert {u["id"] for u in requests.get(USERS_URL).json()} == baseline_users
    #     assert {t["id"] for t in requests.get(TASKS_URL).json()} == baseline_tasks
    #     print("✅ Front-end cleanup verified")

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)

        # 1. crear usuario
        user_id = crear_usuario(driver, wait)
        results.append(("create_user", True, None))

        # 2. crear tarea
        task_id = crear_tarea(driver, wait, user_id)
        results.append(("create_task", True, None))

        # 3. verificar aparece en UI
        tasks_text = ver_tareas(driver)
        ok = "Terminar laboratorio" in tasks_text
        results.append(("task_visible_UI", ok, None if ok else "not listed"))
        assert ok

    except Exception as e:
        results.append(("exception", False, str(e)))
        traceback.print_exc()

    finally:
        # --- cleanup selectivo ---
        try:
            if task_id and task_id not in baseline_tasks:
                delete_task(task_id)
                results.append((f"delete_task_{task_id}", True, None))
        except Exception as e:
            results.append((f"delete_task_{task_id}", False, str(e)))

        try:
            if user_id and user_id not in baseline_users:
                delete_user(user_id)
                results.append((f"delete_user_{user_id}", True, None))
        except Exception as e:
            results.append((f"delete_user_{user_id}", False, str(e)))

        driver.quit()

        # --- verificación global ---
        same_users = {u["id"] for u in requests.get(USERS_URL).json()} == baseline_users
        same_tasks = {t["id"] for t in requests.get(TASKS_URL).json()} == baseline_tasks
        results.append(("global_users_ok", same_users, None if same_users else "mismatch"))
        results.append(("global_tasks_ok", same_tasks, None if same_tasks else "mismatch"))

        # --- PDF ---
        generate_pdf_report("FrontEnd-Test", results)

if __name__ == "__main__":
    main()
