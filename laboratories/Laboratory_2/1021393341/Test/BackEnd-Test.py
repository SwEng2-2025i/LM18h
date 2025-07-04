import requests
from utils import TestResult, generar_reporte_pdf
import traceback

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(user_id,task_id):
    
    tasks = get_tasks()

    # Buscar la tarea que queremos eliminar
    task_to_delete = next((task for task in tasks if task["id"] == task_id and task["user_id"] == user_id), None)

    if not task_to_delete:
        print(f"❌ Task with ID {task_id} not found or doesn't belong to user {user_id}.")
        return

    # Si la tarea existe y pertenece al usuario, realizar la eliminación
    response = requests.delete(f"{TASKS_URL}/{task_id}", json={"user_id": user_id})
    response.raise_for_status()
    print(f"✅ Task with ID {task_id} deleted successfully.")

def delete_user(user_id):
    user_check = requests.get(f"{USERS_URL}/{user_id}")
    if user_check.status_code != 200:
        print(f"❌ User with ID {user_id} not found.")
        return
    
    # Realizar la solicitud DELETE para eliminar el usuario
    response = requests.delete(f"{USERS_URL}/{user_id}")
    
    if response.status_code == 200:
        print(f"✅ User with ID {user_id} deleted successfully.")
    else:
        print(f"❌ Failed to delete user with ID {user_id}.")

def verify_task_deleted(task_id):
    tasks = get_tasks()
    assert not any(task["id"] == task_id for task in tasks), f"❌ Task with ID {task_id} was not deleted"
    print(f"✅ Task with ID {task_id} has been properly deleted.")

def verify_user_deleted(user_id):
    user_check = requests.get(f"{USERS_URL}/{user_id}")
    assert user_check.status_code == 404, f"❌ User with ID {user_id} was not deleted"
    print(f"✅ User with ID {user_id} has been properly deleted.")

def integration_test():
    results = []

    # Step 1: Create user
    r1 = TestResult("Crear Usuario", "Se crea un usuario")
    try:
        user_id = create_user("Camilo")
        r1.pasar(f"ID obtenido: {user_id}")
    except Exception:
        r1.fallar("Error al crear usuario", excepcion=traceback.format_exc())
    results.append(r1)

    # Step 2: Create task
    r2 = TestResult("Crear Tarea", "Se crea una tarea para el usuario")
    try:
        task_id = create_task(user_id, "Prepare presentation")
        r2.pasar(f"ID obtenido: {task_id}")
    except Exception:
        r2.fallar("Error al crear tarea", excepcion=traceback.format_exc())
    results.append(r2)

    # Step 3: Verify task registration
    r3 = TestResult("Verificar tarea registrada", "Se comprueba que la tarea esté vinculada al usuario")
    try:
        tasks = get_tasks()
        assert any(t["id"] == task_id and t["user_id"] == user_id for t in tasks), "La tarea no está registrada"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        r3.pasar("Tarea correctamente registrada")
    except Exception:
        r3.fallar("Error al verificar la tarea", excepcion=traceback.format_exc())
    results.append(r3)

    # Step 4: Delete task and verify
    r4 = TestResult("Eliminar y verificar tarea", "Se elimina la tarea y se comprueba su ausencia")
    try:
        delete_task(user_id, task_id)
        verify_task_deleted(task_id)
        r4.pasar("Tarea eliminada y verificada")
    except Exception:
        r4.fallar("Error al eliminar o verificar tarea", excepcion=traceback.format_exc())
    results.append(r4)

    # Step 5: Delete user and verify
    r5 = TestResult("Eliminar y verificar usuario", "Se elimina el usuario y se comprueba su ausencia")
    try:
        delete_user(user_id)
        verify_user_deleted(user_id)
        r5.pasar("Usuario eliminado y verificado")
    except Exception:
        r5.fallar("Error al eliminar o verificar usuario", excepcion=traceback.format_exc())
    results.append(r5)

    # Generar reporte PDF al finalizar, pero mantener todos los prints
    generar_reporte_pdf(results)

if __name__ == "__main__":
    integration_test()
