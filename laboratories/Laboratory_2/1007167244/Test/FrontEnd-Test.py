import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_generator import TestReportGenerator

# Endpoints de API para limpieza
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def delete_user_api(user_id):
    """Eliminar un usuario mediante llamada API"""
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"✅ Usuario {user_id} eliminado via API")
            return True
        else:
            print(f"❌ Error al eliminar usuario {user_id} via API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al eliminar usuario {user_id} via API: {str(e)}")
        return False

def delete_task_api(task_id):
    """Eliminar una tarea mediante llamada API"""
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"✅ Tarea {task_id} eliminada via API")
            return True
        else:
            print(f"❌ Error al eliminar tarea {task_id} via API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al eliminar tarea {task_id} via API: {str(e)}")
        return False

def verify_user_deleted_api(user_id):
    """Verificar que un usuario ha sido eliminado via API"""
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        return response.status_code == 404
    except:
        return False

def verify_task_deleted_api(task_id):
    """Verificar que una tarea ha sido eliminada via API"""
    try:
        response = requests.get(f"{TASKS_URL}/{task_id}")
        return response.status_code == 404
    except:
        return False

def abrir_frontend(driver):
    # Abre la aplicación frontend en el navegador
    driver.get("http://localhost:5000")
    time.sleep(2)  # Dar tiempo a que la página cargue

def crear_usuario(driver, wait):
    # Llena el formulario de creación de usuario y lo envía
    # Luego recupera y retorna el ID del usuario recién creado
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extraer ID numérico del resultado
    return user_id

def crear_tarea(driver, wait, user_id):
    # Llena el formulario de creación de tarea con una tarea y ID de usuario, luego lo envía
    # Espera hasta que aparezca el texto de confirmación y asevera el resultado
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Forzar salida del foco del input para activar validación
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
    
    # Extraer ID de tarea del resultado
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Hace clic en el botón para actualizar la lista de tareas y verifica que aparece la nueva tarea
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def main():
    test_results = {
        'status': 'PASS',
        'user_id': None,
        'task_id': None,
        'user_created': False,
        'task_created': False,
        'user_deleted': False,
        'task_deleted': False,
        'cleanup_verified': False
    }
    
    # Ejecutor principal de pruebas que inicializa el navegador y ejecuta el flujo completo E2E
    options = Options()
    # options.add_argument('--headless')  # Descomentar para modo headless
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        
        # Crear usuario a través del frontend
        user_id = crear_usuario(driver, wait)
        test_results['user_id'] = user_id
        test_results['user_created'] = True
        
        # Crear tarea a través del frontend
        task_id = crear_tarea(driver, wait, user_id)
        test_results['task_id'] = task_id
        test_results['task_created'] = True
        
        # Verificar que la tarea aparece en la lista
        ver_tareas(driver)
        
        time.sleep(3)  # Demora final para observar resultados si no está en modo headless
        
        # Limpieza mediante llamadas API
        print("\n🧹 Iniciando proceso de limpieza via API...")
        
        # Eliminar tarea primero (para evitar problemas de clave foránea)
        if delete_task_api(task_id):
            test_results['task_deleted'] = True
        
        # Eliminar usuario
        if delete_user_api(user_id):
            test_results['user_deleted'] = True
        
        # Verificar limpieza
        print("\n🔍 Verificando limpieza via API...")
        user_deleted = verify_user_deleted_api(user_id)
        task_deleted = verify_task_deleted_api(task_id)
        
        if user_deleted and task_deleted:
            print("✅ Verificación de limpieza exitosa: Todos los datos de prueba han sido eliminados correctamente")
            test_results['cleanup_verified'] = True
        else:
            print("❌ Verificación de limpieza falló: Algunos datos de prueba permanecen")
            test_results['status'] = 'FAIL'
            test_results['cleanup_verified'] = False
            
    except Exception as e:
        print(f"❌ La prueba falló con error: {str(e)}")
        test_results['status'] = 'FAIL'
        test_results['error'] = str(e)
    finally:
        driver.quit()  # Siempre cerrar el navegador al final
    
    # Generar reporte PDF
    print("\n📄 Generando reporte PDF...")
    generator = TestReportGenerator("Frontend")
    generator.generate_report(test_results)
    
    return test_results

if __name__ == "__main__":
    main()
