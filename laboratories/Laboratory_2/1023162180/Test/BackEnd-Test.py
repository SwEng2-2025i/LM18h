import requests
import os
from datetime import datetime
from fpdf import FPDF

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

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
    if response.status_code not in (200, 204):
        print(f"Warning: Failed to delete task {task_id}")
    return response.status_code

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code not in (200, 204):
        print(f"Warning: Failed to delete user {user_id}")
    return response.status_code

def next_report_number():
    files = [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in files if f.split("_")[1].split(".")[0].isdigit()]
    return max(nums, default=0) + 1

def sanitize_line(line):
    return (
        line.replace("✅", "[OK]")
            .replace("❌", "[FAIL]")
    )

def generate_pdf_report(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Integration Test Report", ln=True, align="C")
    pdf.cell(0, 10, f"Date: {datetime.now()}", ln=True)
    pdf.ln(5)
    for line in results:
        pdf.multi_cell(0, 10, sanitize_line(line))
    report_num = next_report_number()
    filename = os.path.join(REPORTS_DIR, f"report_{report_num}.pdf")
    pdf.output(filename)
    print(f"PDF report generated: {filename}")

def integration_test():
    results = []
    user_id = None
    task_id = None
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        results.append(f"User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        results.append(f"Task created with ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        results.append("Task was successfully registered and linked to the user.")

    except Exception as e:
        results.append(f"❌ Test failed: {str(e)}")
    finally:
        # Cleanup: Delete created task and user
        cleanup_ok = True
        if task_id:
            status = delete_task(task_id)
            results.append(f"Task {task_id} deletion status: {status}")
        if user_id:
            status = delete_user(user_id)
            results.append(f"User {user_id} deletion status: {status}")

        # Verify cleanup
        tasks = get_tasks()
        users = get_users()
        if task_id and any(t["id"] == task_id for t in tasks):
            results.append(f"❌ Task {task_id} was NOT deleted.")
            cleanup_ok = False
        else:
            results.append(f"✅ Task {task_id} was deleted.")

        if user_id and any(u["id"] == user_id for u in users):
            results.append(f"❌ User {user_id} was NOT deleted.")
            cleanup_ok = False
        else:
            results.append(f"✅ User {user_id} was deleted.")

        if cleanup_ok:
            results.append("✅ Data cleanup verified.")
        else:
            results.append("❌ Data cleanup failed.")

        generate_pdf_report(results)

if __name__ == "__main__":
    integration_test()