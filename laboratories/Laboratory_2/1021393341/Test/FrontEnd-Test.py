import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import TestResult, generar_reporte_pdf

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

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def eliminar_tarea(driver, user_id):
    task_list = driver.find_elements(By.CSS_SELECTOR, "#tasks li")
    assert task_list, "No hay tareas para eliminar"

    # Extraer ID de la última tarea
    last_task = task_list[-1].text
    task_id = ''.join(filter(str.isdigit, last_task.split("ID: ")[1].split(",")[0]))

    # Limpiar y llenar inputs
    delete_id_input = driver.find_element(By.ID, "delete-task-id")
    delete_user_input = driver.find_element(By.ID, "delete-task-user-id")
    delete_id_input.clear()
    delete_user_input.clear()
    delete_id_input.send_keys(task_id)
    delete_user_input.send_keys(user_id)

    # Hacer clic en botón eliminar
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Tarea')]").click()

    # Esperar hasta que el mensaje aparezca
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "delete-task-result"), "eliminada")
    )

    # Verificar el mensaje
    result = driver.find_element(By.ID, "delete-task-result").text
    print("Texto recibido al eliminar tarea:", repr(result))
    assert "eliminada" in result.lower()


def eliminar_usuario(driver, user_id):
    driver.find_element(By.ID, "delete-user-id").send_keys(user_id)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Usuario')]").click()
    time.sleep(2)

    result = driver.find_element(By.ID, "delete-user-result").text
    print("Eliminar usuario:", result)
    assert f"Usuario con ID {user_id} eliminado correctamente" in result

def main():
    options = Options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    results = []

    try:
        abrir_frontend(driver)

        r1 = TestResult("Crear Usuario", "Se crea un nuevo usuario desde el frontend")
        try:
            user_id = crear_usuario(driver, wait)
            r1.pasar(f"Usuario creado con ID {user_id}")
        except Exception as e:
            r1.fallar("Error al crear usuario", str(e))
        results.append(r1)

        r2 = TestResult("Crear Tarea", "Se crea una tarea para el usuario")
        try:
            crear_tarea(driver, wait, user_id)
            r2.pasar("Tarea creada correctamente")
        except Exception as e:
            r2.fallar("Error al crear tarea", str(e))
        results.append(r2)

        r3 = TestResult("Ver Tareas", "Se verifica que la tarea aparezca en la lista")
        try:
            ver_tareas(driver)
            r3.pasar("Tarea visible en la lista")
        except Exception as e:
            r3.fallar("Error al ver tareas", str(e))
        results.append(r3)

        r4 = TestResult("Eliminar Tarea", "Se elimina la tarea creada por el test")
        try:
            eliminar_tarea(driver, user_id)
            r4.pasar("Tarea eliminada correctamente")
        except Exception as e:
            r4.fallar("Error al eliminar tarea", str(e))
        results.append(r4)

        r5 = TestResult("Eliminar Usuario", "Se elimina el usuario de prueba")
        try:
            eliminar_usuario(driver, user_id)
            r5.pasar("Usuario eliminado correctamente")
        except Exception as e:
            r5.fallar("Error al eliminar usuario", str(e))
        results.append(r5)

    finally:
        generar_reporte_pdf(results)
        driver.quit()

if __name__ == "__main__":
    main()