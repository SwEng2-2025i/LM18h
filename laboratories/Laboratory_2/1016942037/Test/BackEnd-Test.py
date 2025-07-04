import requests
from test_report import TestReport

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name, report):
    try:
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()
        user_data = response.json()
        report.add_log(f"User created: {user_data}")
        return user_data["id"]
    except Exception as e:
        report.add_log(f"Error creating user: {str(e)}", success=False)
        raise

def create_task(user_id, description, report):
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        response.raise_for_status()
        task_data = response.json()
        report.add_log(f"Task created: {task_data}")
        return task_data["id"]
    except Exception as e:
        report.add_log(f"Error creating task: {str(e)}", success=False)
        raise

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def get_users():
    response = requests.get(USERS_URL)
    response.raise_for_status()
    return response.json()

def delete_task(task_id, report):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        response.raise_for_status()
        report.add_log(f"Task {task_id} deleted")
    except Exception as e:
        report.add_log(f"Error deleting task {task_id}: {str(e)}", success=False)
        raise

def delete_user(user_id, report):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        response.raise_for_status()
        report.add_log(f"User {user_id} deleted")
    except Exception as e:
        report.add_log(f"Error deleting user {user_id}: {str(e)}", success=False)
        raise

def verify_task_deleted(task_id, report):
    tasks = get_tasks()
    if not any(t["id"] == task_id for t in tasks):
        report.add_log(f"Verified: Task {task_id} was successfully deleted")
    else:
        report.add_log(f"Error: Task {task_id} was not deleted", success=False)
        raise AssertionError(f"Task {task_id} was not deleted")

def verify_user_deleted(user_id, report):
    users = get_users()
    if not any(u["id"] == user_id for u in users):
        report.add_log(f"Verified: User {user_id} was successfully deleted")
    else:
        report.add_log(f"Error: User {user_id} was not deleted", success=False)
        raise AssertionError(f"User {user_id} was not deleted")

def integration_test():
    report = TestReport("Backend Integration Test")
    created_data = {"user_id": None, "task_id": None}
    
    try:
        # Step 1: Create user
        created_data["user_id"] = create_user("Camilo", report)

        # Step 2: Create task for that user
        created_data["task_id"] = create_task(created_data["user_id"], "Prepare presentation", report)

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == created_data["user_id"]]

        if any(t["id"] == created_data["task_id"] for t in user_tasks):
            report.add_log("Test completed: task was successfully registered and linked to the user")
        else:
            report.add_log("Error: The task was not correctly registered", success=False)
            raise AssertionError("The task was not correctly registered")

    except Exception as e:
        report.add_log(f"Test failed with error: {str(e)}", success=False)
        raise

    finally:
        # Cleanup: Delete created data in reverse order
        try:
            if created_data["task_id"]:
                delete_task(created_data["task_id"], report)
                verify_task_deleted(created_data["task_id"], report)
            
            if created_data["user_id"]:
                delete_user(created_data["user_id"], report)
                verify_user_deleted(created_data["user_id"], report)
        except Exception as e:
            report.add_log(f"Error during cleanup: {str(e)}", success=False)
        
        # Generate the PDF report
        report.end_test()
        report.generate_pdf()

if __name__ == "__main__":
    integration_test()