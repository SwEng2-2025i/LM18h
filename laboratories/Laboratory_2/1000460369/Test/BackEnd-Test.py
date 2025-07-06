import requests
from report_generator import generate_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

resultados = [
    
]

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

def get_users():
    response = requests.get(USERS_URL)
    response.raise_for_status()
    users = response.json()
    return users

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Task with ID {task_id} deleted")
    return response.status_code

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"✅ User with ID {user_id} deleted")
    return response.status_code

def integration_test():
    # Step 1: Create user
    user_id = create_user("Camilo")

    resultados.append(
        {
            "descripcion": "Crear usuario",
            "resultado": True if user_id else False
        }
    )

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    resultados.append(
        {
            "descripcion": "Crear tarea",
            "resultado": True if task_id else False
        }
    )

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"

    if any(t["id"] == task_id for t in user_tasks):
        resultados.append(
        {
            "descripcion": "Verificar que la tarea existe y está asociada a un usuario",
            "resultado": True
        }
    )
    else:
        resultados.append(
            {
                "descripcion": "Verificar que la tarea existe y está asociada a un usuario",
                "resultado": False
            }
        )
    
    delete_task(task_id)
    tasks_after_delete = get_tasks()
    user_tasks_after_delete = [t for t in tasks_after_delete if t["user_id"] == user_id]

    if not any(t["id"] == task_id for t in user_tasks_after_delete):
        resultados.append(
        {
            "descripcion": "Verificar que la tarea se borró correctamente",
            "resultado": True
        }
    )
    else:
        resultados.append(
            {
                "descripcion": "Verificar que la tarea se borró correctamente",
                "resultado": False
            }
        )

    assert not any(t["id"] == task_id for t in user_tasks_after_delete), "❌ The task was not correctly deleted"

    delete_user(user_id)
    users_after_delete = get_users()
    if not any(u["id"] == user_id for u in users_after_delete):
        resultados.append(
            {
                "descripcion": "Verificar que el usuario se borró correctamente",
                "resultado": True
            }
        )
    else:
        resultados.append(
            {
                "descripcion": "Verificar que el usuario se borró correctamente",
                "resultado": False
            }
        )
    
    assert not any(u["id"] == user_id for u in users_after_delete), "❌ The user was not correctly deleted"
    print("✅ Test completed: task was successfully registered and linked to the user and the user and task was correctly deleted after the test.")

    generate_report("Test/Back End Test Reports", resultados, "Resultados test Back End", "Back_End_Report")


if __name__ == "__main__":
    integration_test()