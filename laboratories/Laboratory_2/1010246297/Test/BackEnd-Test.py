import requests
from pdf_report import generate_pdf_report


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
    print(f"✅ User {user_id} deleted successfully.")
    return response.status_code

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Task {task_id} deleted successfully.")
    return response.status_code


def integration_test():
    logs = []
    try:
        user_id = create_user("Camilo")
        logs.append(f"User created with ID: {user_id}")
        task_id = create_task(user_id, "Prepare presentation")
        logs.append(f"Task created with ID: {task_id}")

        tasks = get_tasks()
        assert any(t["id"] == task_id for t in tasks), "❌ Task not registered"
        logs.append("Task registered: OK")

        # clean up 
        logs.append("🧹 Deleting test data...")
        task_del_status = delete_task(task_id)
        user_del_status = delete_user(user_id)
        logs.append(f"Task delete status: {task_del_status}")
        logs.append(f"User delete status: {user_del_status}")

        tasks = get_tasks()
        assert not any(t["id"] == task_id for t in tasks), "❌ Task was not deleted"
        logs.append("Task deleted: OK")
        user_resp = requests.get(f"{USERS_URL}/{user_id}")
        assert user_resp.status_code == 404, "❌ User was not deleted"
        logs.append("User deleted: OK")

        logs.append("✅ Data cleanup verified.")
        logs.append("✅ Test passed.")
    except Exception as e:
        logs.append(f"❌ Test failed: {e}")
    finally:
        generate_pdf_report(
            logs,
            report_title="Integration Test Report",
            file_prefix="backend_report"
        )

if __name__ == "__main__":
    integration_test()