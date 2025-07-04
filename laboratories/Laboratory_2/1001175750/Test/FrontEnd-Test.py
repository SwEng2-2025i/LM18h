import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_generator import generate_frontend_test_report

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

def eliminar_tarea(driver, wait, task_title):
    # Actualizar lista de tareas
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    
    # Busca el botón de eliminar para la tarea con el título dado
    ul = driver.find_element(By.ID, "tasks")
    items = ul.find_elements(By.TAG_NAME, "li")
    
    for item in items:
        if task_title in item.text:
            try:
                btn = item.find_element(By.TAG_NAME, "button")
                btn.click()
                time.sleep(1)
                
                # Manejar el alert que aparece
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(1)
                break
            except Exception as e:
                print(f"Error al eliminar tarea: {e}")
                continue
    
    # Verifica que la tarea ya no está
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    print(f"Tareas después de eliminar: {tasks}")
    assert task_title not in tasks, f"La tarea '{task_title}' no fue eliminada correctamente"
    print(f"[OK] Tarea '{task_title}' eliminada correctamente")

def eliminar_usuario(driver, wait, user_name):
    # Muestra la lista de usuarios
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de usuarios')]").click()
    time.sleep(2)
    
    ul = driver.find_element(By.ID, "users")
    items = ul.find_elements(By.TAG_NAME, "li")
    
    for item in items:
        if user_name in item.text:
            try:
                btn = item.find_element(By.TAG_NAME, "button")
                btn.click()
                time.sleep(1)
                
                # Manejar el alert que aparece
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(1)
                break
            except Exception as e:
                print(f"Error al eliminar usuario: {e}")
                continue
    
    # Verifica que el usuario ya no está
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de usuarios')]").click()
    time.sleep(2)
    users = driver.find_element(By.ID, "users").text
    print(f"Usuarios después de eliminar: {users}")
    assert user_name not in users, f"El usuario '{user_name}' no fue eliminado correctamente"
    print(f"[OK] Usuario '{user_name}' eliminado correctamente")

def main():
    # Lista para capturar resultados
    test_results = []
    start_time = time.time()
    
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        
        test_results.append("Paso 1: Abriendo aplicacion frontend...")
        abrir_frontend(driver)
        test_results.append("[OK] Frontend cargado correctamente")
        
        test_results.append("Paso 2: Creando usuario...")
        user_id = crear_usuario(driver, wait)
        test_results.append(f"[OK] Usuario 'Ana' creado con ID: {user_id}")
        
        test_results.append("Paso 3: Creando tarea...")
        crear_tarea(driver, wait, user_id)
        test_results.append("[OK] Tarea 'Terminar laboratorio' creada correctamente")
        
        test_results.append("Paso 4: Verificando tarea en lista...")
        ver_tareas(driver)
        test_results.append("[OK] Tarea aparece correctamente en la lista")
        
        test_results.append("Paso 5: Eliminando tarea desde interfaz...")
        eliminar_tarea(driver, wait, "Terminar laboratorio")
        test_results.append("[OK] Tarea eliminada correctamente desde frontend")
        
        test_results.append("Paso 6: Eliminando usuario desde interfaz...")
        eliminar_usuario(driver, wait, "Ana")
        test_results.append("[OK] Usuario eliminado correctamente desde frontend")
        
        test_results.append("[EXITO] PRUEBA EXITOSA: Flujo completo E2E funcionando correctamente")
        time.sleep(2)  # Final delay to observe results if not running headless
        
    except Exception as e:
        error_msg = f"[ERROR] ERROR EN LA PRUEBA E2E: {str(e)}"
        test_results.append(error_msg)
        print(error_msg)
        raise
        
    finally:
        driver.quit()  # Always close the browser at the end
        # Generar reporte PDF
        execution_time = time.time() - start_time
        generate_frontend_test_report(test_results, execution_time)

if __name__ == "__main__":
    main()
