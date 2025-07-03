import requests

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ User {user_id} deleted.")
    else:
        print(f"⚠️ Could not delete user {user_id} (may not exist). Status: {response.status_code}")
    return response.status_code == 200

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Task {task_id} deleted.")
    else:
        print(f"⚠️ Could not delete task {task_id} (may not exist). Status: {response.status_code}")
    return response.status_code == 200

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def get_users():
    response = requests.get(USERS_URL)
    response.raise_for_status()
    return response.json()

def integration_test():

    report_lines = []
    user_id = None
    task_id = None
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        report_lines.append(f"User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        report_lines.append(f"Task created with ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        report_lines.append("Task was successfully registered and linked to the user.")

    except Exception as e:
        report_lines.append(f"❌ Test failed: {e}")
        raise
    finally:
        # Cleanup: Delete created task and user
        cleanup_ok = True
        if task_id:
            if delete_task(task_id):
                report_lines.append(f"Task {task_id} deleted.")
            else:
                report_lines.append(f"⚠️ Task {task_id} could not be deleted.")
                cleanup_ok = False
        if user_id:
            if delete_user(user_id):
                report_lines.append(f"User {user_id} deleted.")
            else:
                report_lines.append(f"⚠️ User {user_id} could not be deleted.")
                cleanup_ok = False

        # Verify deletion
        tasks = get_tasks()
        users = get_users()
        if task_id and not any(t["id"] == task_id for t in tasks):
            report_lines.append(f"✅ Task {task_id} properly deleted.")
        else:
            report_lines.append(f"❌ Task {task_id} still present after deletion!")
            cleanup_ok = False
        if user_id and not any(u["id"] == user_id for u in users):
            report_lines.append(f"✅ User {user_id} properly deleted.")
        else:
            report_lines.append(f"❌ User {user_id} still present after deletion!")
            cleanup_ok = False

        # Generate PDF report
        generate_pdf_report(report_lines)
        if cleanup_ok:
            print("✅ Data cleanup verified.")
        else:
            print("❌ Data cleanup failed.")

def generate_pdf_report(lines):
    # Find next report number
    existing = [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in existing if f.split("_")[1].split(".")[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(REPORTS_DIR, f"report_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Integration Test Report #{next_num}")
    y -= 30
    for line in lines:
        c.drawString(40, y, line)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    print(f"PDF report generated: {filename}")


if __name__ == "__main__":
    integration_test()