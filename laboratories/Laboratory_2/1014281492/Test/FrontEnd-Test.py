import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_report_generator import GeneradorReportePDF

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "nombre_usuario")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "resultado_usuario").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id):
    task_description = "Terminar laboratorio"
    task_input = driver.find_element(By.ID, "titulo_tarea")
    task_input.send_keys(task_description)
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "id_usuario")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "resultado_tarea"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "resultado_tarea").text
    print("Texto en resultado_tarea:", task_result)
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    return task_id, task_description

def ver_tareas(driver, task_description):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "lista_tareas").text
    print("Tareas:", tasks)
    assert task_description in tasks

def eliminar_datos_prueba(driver, wait, user_id, task_id, reporte):
    # Eliminar tarea
    task_delete_input = driver.find_element(By.ID, "tarea-id-eliminar")
    task_delete_input.send_keys(task_id)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Eliminar Tarea']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "resultado-eliminar-tarea"), "✅"))
    delete_task_result = driver.find_element(By.ID, "resultado-eliminar-tarea").text
    assert "✅" in delete_task_result
    reporte.agregar_linea(f"Limpieza: Tarea {task_id} eliminada exitosamente.")
    print(f"✅ Limpieza: Tarea {task_id} eliminada.")

    # Eliminar usuario
    user_delete_input = driver.find_element(By.ID, "usuario-id-eliminar")
    user_delete_input.send_keys(user_id)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Eliminar Usuario']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "resultado-eliminar-usuario"), "✅"))
    delete_user_result = driver.find_element(By.ID, "resultado-eliminar-usuario").text
    assert "✅" in delete_user_result
    reporte.agregar_linea(f"Limpieza: Usuario {user_id} eliminado exitosamente.")
    print(f"✅ Limpieza: Usuario {user_id} eliminado.")

def verificar_eliminacion(driver, task_description, reporte):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "lista_tareas").text
    assert task_description not in tasks
    reporte.agregar_linea(f"Verificación: Tarea '{task_description}' confirmada como eliminada.")
    print(f"✅ Verificación: Tarea '{task_description}' ya no está en la lista.")

def main():
    options = Options()
    driver = webdriver.Chrome(options=options)
    reporte = GeneradorReportePDF("Reporte de Prueba E2E Frontend")
    user_id = None
    task_id = None
    task_description = ""

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        reporte.agregar_linea("Frontend abierto.")

        user_id = crear_usuario(driver, wait)
        reporte.agregar_linea(f"Usuario creado con ID: {user_id}")

        task_id, task_description = crear_tarea(driver, wait, user_id)
        reporte.agregar_linea(f"Tarea '{task_description}' creada con ID: {task_id} para usuario {user_id}")

        ver_tareas(driver, task_description)
        reporte.agregar_linea(f"Verificación: Tarea '{task_description}' encontrada en la lista.")

        reporte.agregar_linea("Flujo de prueba completado exitosamente antes de la limpieza.")

    finally:
        if user_id and task_id:
            eliminar_datos_prueba(driver, wait, user_id, task_id, reporte)
            verificar_eliminacion(driver, task_description, reporte)

        reporte.generar("reportes")
        print("✅ Reporte PDF generado.")
        driver.quit()

if __name__ == "__main__":
    main()
