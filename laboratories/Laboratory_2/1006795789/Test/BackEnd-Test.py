import requests
import os
from fpdf import FPDF

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
    response = requests.delete(f"http://localhost:5001/users/{user_id}")
    return response

def delete_task(task_id):
    response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    return response

def integration_test():
    # Step 1: Create user
    user_id = create_user("Camilo")

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "\u274c The task was not correctly registered"
    print("\u2705 Test completed: task was successfully registered and linked to the user.")

    # Step 4: Cleanup - delete task and user
    task_del_resp = delete_task(task_id)
    user_del_resp = delete_user(user_id)

    # Step 5: Verify deletion
    tasks_after = get_tasks()
    assert not any(t["id"] == task_id for t in tasks_after), "\u274c Task was not deleted!"
    user_resp = requests.get(f"http://localhost:5001/users/{user_id}")
    assert user_resp.status_code == 404, "\u274c User was not deleted!"
    print("\u2705 Cleanup verified: user and task deleted.")

    # Step 6: PDF report generation
    result_text = "Integration Test Result\n"
    result_text += f"User created: {user_id}\nTask created: {task_id}\n"
    result_text += "Test passed: task registered and linked to user.\n"
    result_text += "Cleanup passed: user and task deleted.\n"

    # Find next report number
    report_dir = "."  # Current directory (Test folder)
    existing = [f for f in os.listdir(report_dir) if f.startswith("BackEnd-report_") and f.endswith(".pdf")]
    nums = [int(f.split('_')[1].split('.')[0]) for f in existing if f.split('_')[1].split('.')[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    pdf_path = os.path.join(report_dir, f"BackEnd-report_{next_num}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in result_text.splitlines():
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.output(pdf_path)
    print(f"PDF report generated: {pdf_path}")

if __name__ == "__main__":
    integration_test()