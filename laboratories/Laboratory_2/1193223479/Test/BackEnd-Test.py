import requests
import traceback
from pdf_report import pdf_report

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
    assert response.status_code == 204

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    assert response.status_code == 204


def integration_test():
    test_results = []
    user_id= None
    task_id = None

    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        test_results.append(f"User {user_id} created successfully.")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        test_results.append(f"Task {task_id} created successfully.")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "Not registered task."
        test_results.append("User-task association verified successfully.")

    except Exception as e:
        test_results.append(f"Error during test: {str(e)}.")

    finally:
        try:
            if task_id:
                delete_task(task_id)
                test_results.append(f"Task {task_id} deleted successfully.")
            if user_id:
                delete_user(user_id)
                test_results.append(f"User {user_id} deleted successfully.")

            task_list = get_tasks()
            if task_id and any(t["id"] == task_id for t in task_list):
                test_results.append("The task was not deleted.")
            else:
                test_results.append("The data has been deleted successfully.")
        except Exception as e:
            test_results.append(f"Error at deleting data" + traceback.format_exc())

        pdf_report(test_results)



if __name__ == "__main__":
    integration_test()