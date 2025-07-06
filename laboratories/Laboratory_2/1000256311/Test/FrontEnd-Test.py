import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from LogSaver import Logger, DuplicadorSalida
from reportlab.pdfgen import canvas
import textwrap
import sys
import io
import os
import requests

# Endpoints
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
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))  # Extract numeric ID from result
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def obtener_siguiente_numero(nombre_base="reporteFrontEnd", carpeta="reportes", extension=".pdf"):
    os.makedirs(carpeta, exist_ok=True)  # Crea carpeta si no existe
    existentes = [f for f in os.listdir(carpeta) if f.startswith(nombre_base) and f.endswith(extension)]

    numeros = []
    for f in existentes:
        try:
            num = int(f.replace(nombre_base + "_", "").replace(extension, ""))
            numeros.append(num)
        except ValueError:
            pass  # Ignora archivos con nombres no estándar

    siguiente = max(numeros, default=0) + 1
    return os.path.join(carpeta, f"{nombre_base}_{siguiente}{extension}")
def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    Logger.add_to_log("info", "Task deleted: " + str(task_id) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    print("✅ Task deleted:", task_id)

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    Logger.add_to_log("info", "User deleted: " + str(user_id) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    print("✅ User deleted:", user_id)

def guardar_en_pdf(texto, nombre_pdf):
    c = canvas.Canvas(nombre_pdf)
    y = 800
    margen_izquierdo = 40
    alto_linea = 15

    for linea in texto.split('\n'):
        # Divide la línea si es demasiado larga (wrap)
        sublineas = textwrap.wrap(linea, width=100)
        for sublinea in sublineas:
            c.drawString(margen_izquierdo, y, sublinea)
            y -= alto_linea
            if y < 50:  # Cambia de página si se llega al final
                c.showPage()
                y = 800

    c.save()

def limpiar_archivo(nombre_archivo):
    with open(nombre_archivo, "w", encoding="utf-8"):
        pass
def capturar_y_guardar_pdf():

    captura = io.StringIO()
    sys.stdout = DuplicadorSalida(sys.__stdout__, captura)
    limpiar_archivo("Logs/app.log")

    try:
        main()
    finally:
        # Obtener texto de consola
        sys.stdout = sys.__stdout__
        # Obtener texto de logs

    

    with open("Logs/app.log", "r", encoding="utf-8") as f:
        contenido_existente = f.read()
        
    


    # 🔀 Combinar todo (puedes incluir encabezados si quieres)
    contenido_total = (
        "=== SALIDA DE CONSOLA ===\n"
        + captura.getvalue() +
        "\n\n=== LOGS DE PETICIONES ===\n"
        + contenido_existente
    )


    nombre_pdf = obtener_siguiente_numero()
    guardar_en_pdf(contenido_total, nombre_pdf)
    print(f"PDF generado: {nombre_pdf}")
    limpiar_archivo("Logs/app.log")

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
        time.sleep(3)  # Final delay to observe results if not running headless
        delete_user(user_id)
        delete_task(task_id)
    finally:
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
#    main()
    capturar_y_guardar_pdf()