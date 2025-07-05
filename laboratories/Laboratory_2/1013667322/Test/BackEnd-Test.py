import requests
from pdf_report_generator import PDFReportGenerator

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
    print(f"✅ User {user_id} deleted.")

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Task {task_id} deleted.")

def get_user(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    return response

def get_task(task_id):
    response = requests.get(f"{TASKS_URL}/{task_id}")
    return response

def integration_test():
    report = PDFReportGenerator("Backend Integration Test Report")
    user_id = None
    task_id = None
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        report.add_line(f"User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        report.add_line(f"Task created with ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        report.add_line("Test completed: task was successfully registered and linked to the user.")

    finally:
        if task_id:
            delete_task(task_id)
            report.add_line(f"Task {task_id} deleted.")
            # Verify task deletion
            response = get_task(task_id)
            assert response.status_code == 404, f"❌ Task {task_id} was not deleted correctly."
            report.add_line(f"Verified task {task_id} deletion.")

        if user_id:
            delete_user(user_id)
            report.add_line(f"User {user_id} deleted.")
            # Verify user deletion
            response = get_user(user_id)
            assert response.status_code == 404, f"❌ User {user_id} was not deleted correctly."
            report.add_line(f"Verified user {user_id} deletion.")
        
        report.generate("d:\\01_Actuales\\unal\\Laboratory2\\Laboratory_2\\1013667322\\Test\\reports")
        print("✅ PDF report generated.")


if __name__ == "__main__":
    integration_test()