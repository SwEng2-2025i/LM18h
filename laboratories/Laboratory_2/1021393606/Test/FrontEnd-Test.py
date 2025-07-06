import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from generate_pdf_report import save_pdf_report

def main():
    steps = []
    user_id = "N/A"
    options = Options()
    # options.add_argument("--headless")  # Descomenta si no quieres ver el navegador
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)

        # Paso 1: abrir aplicación
        driver.get("http://localhost:5000")
        steps.append({"step": "Open frontend application", "status": "PASS", "details": "Successfully opened http://localhost:5000"})

        # Paso 2: crear usuario
        try:
            username_input = driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys("Ana")
            driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
            wait.until(EC.presence_of_element_located((By.ID, "user-result")))
            user_result = driver.find_element(By.ID, "user-result").text
            assert "Usuario creado con ID" in user_result, f"Unexpected result: {user_result}"
            user_id = ''.join(filter(str.isdigit, user_result))
            steps.append({"step": "Create user via frontend", "status": "PASS", "details": f'User "Ana" created with ID {user_id}'})
        except Exception as e:
            steps.append({"step": "Create user via frontend", "status": "FAIL", "details": str(e)})
            raise

        # Paso 3: crear tarea
        try:
            task_input = driver.find_element(By.ID, "task")
            task_input.clear()
            task_input.send_keys("Terminar laboratorio")

            userid_input = driver.find_element(By.ID, "userid")
            userid_input.clear()
            userid_input.send_keys(user_id)

            crear_tarea_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']")))
            crear_tarea_btn.click()

            wait.until(EC.presence_of_element_located((By.ID, "task-result")))
            task_result = driver.find_element(By.ID, "task-result").text
            assert "Tarea creada con ID" in task_result, f"Unexpected result: {task_result}"
            steps.append({"step": "Create task via frontend", "status": "PASS", "details": f'Task "Terminar laboratorio" created for user {user_id}'})
        except Exception as e:
            steps.append({"step": "Create task via frontend", "status": "FAIL", "details": str(e)})
            raise

        # Paso 4: verificar que la tarea aparece
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
            time.sleep(2)
            tasks = driver.find_element(By.ID, "tasks").text
            assert "Terminar laboratorio" in tasks, f"Tarea no encontrada en lista: {tasks}"
            steps.append({"step": "Verify task in list", "status": "PASS", "details": 'Task "Terminar laboratorio" found in task list'})
        except Exception as e:
            steps.append({"step": "Verify task in list", "status": "FAIL", "details": str(e)})
            raise

    except Exception as e:
        steps.append({"step": "Test execution", "status": "FAIL", "details": str(e)})

    finally:
        driver.quit()

    report_data = {
        "test_steps": steps,
        "users_created": f"[{user_id}]",
        "tasks_created": "[1]" if any("Create task via frontend" in s["step"] and s["status"] == "PASS" for s in steps) else "[]",
        "cleanup_steps": []  # No implementado en UI
    }
    save_pdf_report(report_data, report_title="Test Report", report_type="Frontend E2E Test")

if __name__ == "__main__":
    main()
