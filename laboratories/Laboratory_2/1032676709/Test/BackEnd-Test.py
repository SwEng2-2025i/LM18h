import requests
import traceback
from generate_report import generate_pdf_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    assert response.status_code == 204

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    assert response.status_code == 204

def integration_test():
    results = []
    user_id = None
    task_id = None

    try:
        user_id = create_user("Camilo")
        results.append(f"✅ Usuario creado con ID: {user_id}")

        task_id = create_task(user_id, "Prepare presentation")
        results.append(f"✅ Tarea creada con ID: {task_id}")

        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "Tarea no registrada"
        results.append("✅ Asociación tarea-usuario verificada")

    except Exception as e:
        results.append(f"❌ Error durante la prueba: {str(e)}")

    finally:
        try:
            if task_id:
                delete_task(task_id)
                results.append(f"✅ Tarea {task_id} eliminada")

            if user_id:
                delete_user(user_id)
                results.append(f"✅ Usuario {user_id} eliminado")

            tasks_final = get_tasks()
            if task_id and any(t["id"] == task_id for t in tasks_final):
                results.append("❌ La tarea no fue eliminada")
            else:
                results.append("✅ Verificación de limpieza exitosa")

        except Exception as e:
            results.append(f"❌ Error al limpiar datos: " + traceback.format_exc())

        generate_pdf_report(results)

if __name__ == "__main__":
    integration_test()