import requests
from report_generator import PDFReport
import os
from datetime import datetime

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
    if response.status_code == 200:
        print("✅ User deleted:", user_id)
        return True
    print("❌ Failed to delete user:", user_id)
    return False

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print("✅ Task deleted:", task_id)
        return True
    print("❌ Failed to delete task:", task_id)
    return False

def verify_cleanup(user_id, task_id):
    # Verify user deletion
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        if response.status_code == 404:
            print(f"✅ Verification: User {user_id} successfully deleted")
        else:
            print(f"❌ Verification: User {user_id} still exists")
    except Exception as e:
        print(f"❌ Error verifying user deletion: {str(e)}")

    # Verify task deletion
    try:
        response = requests.get(f"{TASKS_URL}/{task_id}")
        if response.status_code == 404:
            print(f"✅ Verification: Task {task_id} successfully deleted")
        else:
            print(f"❌ Verification: Task {task_id} still exists")
    except Exception as e:
        print(f"❌ Error verifying task deletion: {str(e)}")

def integration_test():
    report = PDFReport()
    report.add_page()
    report.chapter_title("Backend Integration Test Report")
    test_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        report.log_step(f"User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        report.log_step(f"Task created with ID: {task_id}")

        # Step 3: Verify that the task is registered
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "Task not registered"
        report.log_step("Task successfully registered and linked to user")

        # Step 4: Cleanup
        report.chapter_title("Cleanup Phase")
        task_deleted = delete_task(task_id)
        user_deleted = delete_user(user_id)
        
        report.log_step(f"Task deletion {'successful' if task_deleted else 'failed'}")
        report.log_step(f"User deletion {'successful' if user_deleted else 'failed'}")

        # Step 5: Verify cleanup
        verify_cleanup(user_id, task_id)
        report.log_step("Cleanup verification completed")

        report.log_test_result(True)
        print("✅ Test completed successfully")

    except Exception as e:
        report.log_step(f"Test failed: {str(e)}")
        report.log_test_result(False)
        print(f"❌ Test failed: {str(e)}")
        raise
    finally:
        report.output(f"reports/backend_test_report_{test_start.replace(':', '-')}.pdf")

if __name__ == "__main__":
    integration_test()