import requests
import time
from pdf_generator import generate_backend_test_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("[OK] User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("[OK] Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    return response.status_code

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    return response.status_code

def user_exists(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    return response.status_code == 200

def task_exists(task_id):
    response = requests.get(f"{TASKS_URL}")
    response.raise_for_status()
    tasks = response.json()
    return any(t["id"] == task_id for t in tasks)

def integration_test():
    # Lista para capturar resultados
    test_results = []
    start_time = time.time()
    
    try:
        # Step 1: Create user
        test_results.append("Paso 1: Creando usuario...")
        user_id = create_user("Camilo")
        test_results.append(f"[OK] Usuario creado con ID: {user_id}")

        # Step 2: Create task for that user
        test_results.append("Paso 2: Creando tarea...")
        task_id = create_task(user_id, "Prepare presentation")
        test_results.append(f"[OK] Tarea creada con ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        test_results.append("Paso 3: Verificando integracion...")
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "[ERROR] The task was not correctly registered"
        test_results.append("[OK] Tarea correctamente registrada y asociada al usuario")
        print("[OK] Test completed: task was successfully registered and linked to the user.")

        # Cleanup
        test_results.append("Paso 4: Limpiando datos de prueba...")
        delete_task(task_id)
        delete_user(user_id)

        # Verificación de borrado
        assert not task_exists(task_id), "[ERROR] La tarea no fue eliminada correctamente"
        assert not user_exists(user_id), "[ERROR] El usuario no fue eliminado correctamente"
        test_results.append("[OK] Datos de prueba eliminados correctamente")
        print("[OK] Datos de prueba eliminados correctamente.")
        
        # Resultado final
        test_results.append("[EXITO] PRUEBA EXITOSA: Integracion backend funcionando correctamente")
        
    except Exception as e:
        error_msg = f"[ERROR] ERROR EN LA PRUEBA: {str(e)}"
        test_results.append(error_msg)
        print(error_msg)
        raise
    
    finally:
        # Generar reporte PDF
        execution_time = time.time() - start_time
        generate_backend_test_report(test_results, execution_time)


if __name__ == "__main__":
    integration_test()