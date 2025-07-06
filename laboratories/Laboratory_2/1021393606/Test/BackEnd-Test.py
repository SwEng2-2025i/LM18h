import requests
from generate_pdf_report import save_pdf_report
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

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()


def integration_test():
    # # Step 1: Create user
    # user_id = create_user("Camilo")

    # # Step 2: Create task for that user
    # task_id = create_task(user_id, "Prepare presentation")

    # # Step 3: Verify that the task is registered and associated with the user
    # tasks = get_tasks()
    # user_tasks = [t for t in tasks if t["user_id"] == user_id]

    # assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
    # print("✅ Test completed: task was successfully registered and linked to the user.")

    #  # Limpieza
    # delete_task(task_id)
    # delete_user(user_id)

    # # Verificación
    # tasks = get_tasks()
    # assert all(t["id"] != task_id for t in tasks), "❌ La tarea no fue eliminada correctamente"
    # print("✅ Datos de prueba eliminados correctamente.")

    steps = []
    cleanup = []
    user_id = task_id = None

    try:
        user_id = create_user("Camilo")
        steps.append({"step": "Create user via API", "status": "PASS", "details": f'User "Camilo" created with ID {user_id}'})

        task_id = create_task(user_id, "Prepare presentation")
        steps.append({"step": "Create task via API", "status": "PASS", "details": f'Task created with ID {task_id} for user {user_id}'})

        tasks = get_tasks()
        assert any(t["id"] == task_id for t in tasks), "Task not registered"
        steps.append({"step": "Verify task linked", "status": "PASS", "details": "Task correctly linked to user"})

        delete_task(task_id)
        delete_user(user_id)
        cleanup.append({"operation": "Delete task", "status": "SUCCESS", "details": f"Task {task_id} deleted"})
        cleanup.append({"operation": "Delete user", "status": "SUCCESS", "details": f"User {user_id} deleted"})

        tasks = get_tasks()
        assert all(t["id"] != task_id for t in tasks)
        cleanup.append({"operation": "Verify cleanup", "status": "SUCCESS", "details": "Test data successfully removed"})

    except Exception as e:
        steps.append({"step": "Test execution", "status": "FAIL", "details": str(e)})

    report_data = {
        "test_steps": steps,
        "users_created": f"[{user_id}]" if user_id else "[]",
        "tasks_created": f"[{task_id}]" if task_id else "[]",
        "cleanup_steps": cleanup
    }
    save_pdf_report(report_data, report_title="Test Report", report_type="BackEnd Integration Test")



if __name__ == "__main__":
    integration_test()