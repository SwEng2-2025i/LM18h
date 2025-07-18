import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

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
    # Extraer el ID de la tarea creada
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def borrar_tarea_via_api(task_id):
    response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    try:
        print("Eliminando tarea:", response.json())
    except Exception:
        print(f"Tarea {task_id} eliminada - Status: {response.status_code}")
    success = response.status_code == 200
    return success

def confirmar_tarea_eliminada(task_id):
    response = requests.get("http://localhost:5002/tasks")
    if response.status_code != 200:
        return False
    
    lista_tareas = response.json()
    for tarea in lista_tareas:
        if str(tarea["id"]) == str(task_id):
            return False
    return True

def borrar_usuario_via_api(user_id):
    response = requests.delete(f"http://localhost:5001/users/{user_id}")
    try:
        print("Eliminando usuario:", response.json())
    except Exception:
        print(f"Usuario {user_id} eliminado - Status: {response.status_code}")
    success = response.status_code == 200
    return success

def confirmar_usuario_eliminado(user_id):
    response = requests.get(f"http://localhost:5001/users/{user_id}")
    usuario_no_encontrado = response.status_code == 404
    return usuario_no_encontrado

def crear_reporte_pdf(lista_resultados):
    # Buscar el siguiente número de reporte disponible
    nombre_base = "frontend_test_report"
    contador = 1
    while True:
        nombre_archivo = f"{nombre_base}_{contador}.pdf"
        if not os.path.exists(nombre_archivo):
            break
        contador += 1
    
    pdf_canvas = canvas.Canvas(nombre_archivo, pagesize=letter)
    ancho, alto = letter
    
    # Configurar título
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(50, alto - 50, "Reporte de Pruebas End-to-End")
    
    # Configurar contenido
    pdf_canvas.setFont("Helvetica", 12)
    posicion_y = alto - 90
    
    for resultado in lista_resultados:
        if posicion_y < 50:  # Nueva página si es necesario
            pdf_canvas.showPage()
            posicion_y = alto - 50
        pdf_canvas.drawString(50, posicion_y, resultado)
        posicion_y -= 20
        
    pdf_canvas.save()
    print(f"Reporte generado: {nombre_archivo}")

def main():
    resultados = []
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        wait = WebDriverWait(driver, 10)
        
        # Ejecutar pruebas principales
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        resultados.append(f"Usuario creado con ID: {user_id}")
        
        task_id = crear_tarea(driver, wait, user_id)
        resultados.append(f"Tarea creada con ID: {task_id}")
        
        ver_tareas(driver)
        resultados.append("La tarea aparece en la lista correctamente.")

        # Proceso de limpieza de datos
        tarea_eliminada = borrar_tarea_via_api(task_id)
        if tarea_eliminada:
            resultados.append(f"Tarea {task_id} eliminada correctamente.")
        else:
            resultados.append(f"Error al eliminar la tarea {task_id}.")

        if confirmar_tarea_eliminada(task_id):
            resultados.append(f"Verificado: la tarea {task_id} ya no existe.")
        else:
            resultados.append(f"Error: la tarea {task_id} aún existe.")

        usuario_eliminado = borrar_usuario_via_api(user_id)
        if usuario_eliminado:
            resultados.append(f"Usuario {user_id} eliminado correctamente.")
        else:
            resultados.append(f"Error al eliminar el usuario {user_id}.")

        if confirmar_usuario_eliminado(user_id):
            resultados.append(f"Verificado: el usuario {user_id} ya no existe.")
        else:
            resultados.append(f"Error: el usuario {user_id} aún existe.")

        resultados.append("Prueba completada exitosamente.")
        time.sleep(2)  # Pausa final para observar resultados
        
    except Exception as error:
        mensaje_error = f"Error durante la prueba: {str(error)}"
        resultados.append(mensaje_error)
        raise
    finally:
        driver.quit()
        crear_reporte_pdf(resultados)

if __name__ == "__main__":
    main()
