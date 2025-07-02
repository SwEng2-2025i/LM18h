import os
import time
from datetime import datetime
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# ========== PDF Report Utils ==========
def get_next_report_number(report_dir="reports_frontend"):
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        return 1
    existing = [f for f in os.listdir(report_dir) if f.startswith("frontend_report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[2].split(".")[0]) for f in existing if f.split("_")[2].split(".")[0].isdigit()]
    return max(nums, default=0) + 1

def generate_pdf_report(lines, report_dir="reports_frontend"):
    num = get_next_report_number(report_dir)
    filename = os.path.join(report_dir, f"frontend_report_{num}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"FrontEnd Integration Test Report #{num}", ln=True, align='C')
    pdf.cell(200, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    for line in lines:
        # Elimina caracteres no compatibles con Latin-1
        safe_line = line.encode("latin-1", "ignore").decode("latin-1")
        pdf.multi_cell(0, 10, txt=safe_line)
    pdf.output(filename)

# ========== Test Steps ==========
def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait, logs):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    logs.append(f"Usuario creado: {user_result}")
    assert "Usuario creado con ID" in user_result
    return ''.join(filter(str.isdigit, user_result))

def crear_tarea(driver, wait, user_id, logs):
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

    # Esperamos hasta que el contenido de task-result no esté vacío
    wait.until(lambda d: d.find_element(By.ID, "task-result").text != "")
    task_result = driver.find_element(By.ID, "task-result").text

    logs.append(f"Texto en task_result: {task_result}")
    print("Texto en task_result:", task_result)
    assert "Tarea creada con ID" in task_result

    logs.append("Tarea creada:")
    return ''.join(filter(str.isdigit, task_result))


def ver_tareas(driver, logs):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    logs.append(f"Lista de tareas mostrada: {tasks}")
    assert "Terminar laboratorio" in tasks

def eliminar_datos(user_id, task_id, logs):
    try:
        r = requests.delete(f"http://localhost:5002/tasks/{task_id}")
        logs.append(f"Eliminación de tarea {task_id}: {r.status_code} {r.text}")
    except Exception as e:
        logs.append(f"Error eliminando tarea: {e}")

    try:
        r = requests.delete(f"http://localhost:5001/users/{user_id}")
        logs.append(f"Eliminación de usuario {user_id}: {r.status_code} {r.text}")
    except Exception as e:
        logs.append(f"Error eliminando usuario: {e}")

def verificar_eliminacion(user_id, task_id, logs):
    r_user = requests.get(f"http://localhost:5001/users/{user_id}")
    r_task = requests.get(f"http://localhost:5002/tasks")
    task_exists = any(str(task_id) == str(t["id"]) for t in r_task.json())

    if r_user.status_code == 404:
        logs.append(f"Verificación usuario eliminado correctamente")
    else:
        logs.append(f"Usuario {user_id} no fue eliminado correctamente")

    if not task_exists:
        logs.append(f"Verificación tarea eliminada correctamente")
    else:
        logs.append(f"Tarea {task_id} no fue eliminada correctamente")

# ========== Test runner ==========
def main():
    logs = ["Iniciando test de integración de Front-End..."]
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait, logs)
        task_id = crear_tarea(driver, wait, user_id, logs)
        ver_tareas(driver, logs)

        eliminar_datos(user_id, task_id, logs)
        verificar_eliminacion(user_id, task_id, logs)

        logs.append("Test de Front-End completado con éxito")

    except Exception as e:
        import traceback
        logs.append(f"Test fallido: {str(e)}")
        print("\u27a1\ufe0f Error dentro de main():")
        traceback.print_exc()
        raise

    finally:
        driver.quit()
        for line in logs:
            print(line)
        generate_pdf_report(logs)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Test fallido:")
        print("\u27a1\ufe0f Error:", e)
    finally:
        print("Test finalizado.")
