import requests
from report_generator import generate_pdf_report


# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("• User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("• Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"• User with id {user_id} has been deleted")

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"• Task with id {task_id} has been deleted")

def integration_test():
    log = []
    status = "PASSED ✓"

    print("TEST START")

    try:
        log.append("=============================================")
        log.append("                TEST START                   ")
        log.append("=============================================")

        log.append("------------ Data Creation -----------------")
        user_id = create_user("Camilo")
        log.append(f"• User created with ID {user_id}")

        task_id = create_task(user_id, "Prepare presentation")
        log.append(f"• Task created with ID {task_id} for user {user_id}")

        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "Task was not correctly registered"
        log.append("✓ Task was successfully registered and linked to the user")

        log.append("------------ Data Cleanup -----------------")
        delete_task(task_id)

        tasks = get_tasks()
        assert all(t["id"] != task_id for t in tasks), "Task was not deleted correctly"
        log.append(f"• Task with ID {task_id} deleted")

        delete_user(user_id)

        user_response = requests.get(f"{USERS_URL}/{user_id}")
        assert user_response.status_code == 404, "User was not deleted correctly"
        log.append(f"• User with ID {user_id} deleted")

        log.append("✓ Data cleanup was completed successfully")

    except Exception as e:
        status = "FAILED ✘"
        log.append(f"✘ Test failed: {e}")

    finally:
        log.append("=============================================")
        log.append("              TEST COMPLETED")
        log.append("=============================================")

    print("TEST END")
    generate_pdf_report(log, status, prefix="backend")

if __name__ == "__main__":
    integration_test()