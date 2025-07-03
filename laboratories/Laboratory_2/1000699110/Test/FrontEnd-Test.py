import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_generator import create_test_result, generate_test_report

# URLs of cleaning services
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Lists to track IDs created in this test
created_user_ids = []
created_task_ids = []

# List to capture test results
test_results = []

def clear_test_data():
    """Clear only the data created by this test"""
    print(f"🧹 Limpiando {len(created_task_ids)} tareas y {len(created_user_ids)} usuarios creados en este test...")
    
    # Delete tasks created in this test
    for task_id in created_task_ids:
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            if response.status_code == 200:
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"⚠️ Failed to delete task {task_id}: {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️ Error deleting task {task_id}: {e}")
    
    # Delete users created in this test
    for user_id in created_user_ids:
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                print(f"✅ User {user_id} deleted successfully")
            else:
                print(f"⚠️ Failed to delete user {user_id}: {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️ Error deleting user {user_id}: {e}")

    # Clear the lists for future tests
    created_task_ids.clear()
    created_user_ids.clear()

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
    
    # Track the created user ID
    created_user_ids.append(int(user_id))
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
    
    # Extract and track the created task ID
    task_id = ''.join(filter(str.isdigit, task_result.text))
    if task_id:
        created_task_ids.append(int(task_id))

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    start_time = time.time()
    test_output = []
    test_error = ""
    
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        
        test_output.append("🔄 Iniciando test de frontend...")
        test_output.append("🔄 Abriendo navegador...")
        abrir_frontend(driver)
        test_output.append("✅ Frontend abierto correctamente")
        
        test_output.append("🔄 Creando usuario...")
        user_id = crear_usuario(driver, wait)
        test_output.append(f"✅ Usuario creado con ID: {user_id}")
        
        test_output.append("🔄 Creando tarea...")
        crear_tarea(driver, wait, user_id)
        test_output.append("✅ Tarea creada correctamente")
        
        test_output.append("🔄 Verificando lista de tareas...")
        ver_tareas(driver)
        test_output.append("✅ Lista de tareas verificada correctamente")
        
        time.sleep(3)  # Final delay to observe results if not running headless
        
        # Capture successful result
        duration = f"{time.time() - start_time:.2f}s"
        test_result = create_test_result(
            name="Frontend E2E Test",
            status="passed",
            duration=duration,
            output="\n".join(test_output),
            error=""
        )
        test_results.append(test_result)
        
    except Exception as e:
        # Capture failed result
        duration = f"{time.time() - start_time:.2f}s"
        test_error = str(e)
        test_output.append(f"❌ Test failed: {test_error}")
        
        test_result = create_test_result(
            name="Frontend E2E Test",
            status="failed",
            duration=duration,
            output="\n".join(test_output),
            error=test_error
        )
        test_results.append(test_result)
        
        print(f"❌ Frontend test failed: {test_error}")
        raise
        
    finally:
        driver.quit()  # Always close the browser at the end
        # Clear test data at the end
        print("\n🧹 Cleaning up test data...")
        clear_test_data()

        # Generate PDF report
        print("\n📄 Generating PDF report...")
        try:
            pdf_path = generate_test_report(test_results)
            print(f"✅ PDF report generated successfully: {pdf_path}")
        except Exception as e:
            print(f"⚠️ Error generating PDF: {e}")

if __name__ == "__main__":
    main()
