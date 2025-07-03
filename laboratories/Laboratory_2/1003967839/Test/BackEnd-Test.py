import requests
import os
from fpdf import FPDF
from datetime import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# ========== Funciones básicas ==========
def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def get_users():
    response = requests.get(USERS_URL)
    response.raise_for_status()
    return response.json()

# ========== Limpieza ==========
def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    return response.status_code == 200

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    return response.status_code == 200

# ========== Reporte en PDF ==========
def get_next_report_number(report_dir="reports"):
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        return 1
    existing = [f for f in os.listdir(report_dir) if f.startswith("report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in existing if f.split("_")[1].split(".")[0].isdigit()]
    return max(nums, default=0) + 1

def generate_pdf_report(lines, report_dir="reports"):
    num = get_next_report_number(report_dir)
    filename = os.path.join(report_dir, f"report_{num}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Integration Test Report #{num}", ln=True, align='C')
    pdf.cell(200, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    for line in lines:
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(filename)

# ========== Test principal ==========
def integration_test():
    logs = []
    try:
        logs.append("Starting integration test...")

        user_id = create_user("Camilo")
        logs.append(f"User created with ID {user_id}")

        task_id = create_task(user_id, "Prepare presentation danny")
        logs.append(f"Task created with ID {task_id}")

        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "Task not found after creation"
        logs.append("Task successfully linked to the user")

        # Limpieza
        if delete_task(task_id):
            logs.append(f"Task {task_id} deleted")
        else:
            logs.append(f"Failed to delete task {task_id}")

        if delete_user(user_id):
            logs.append(f"User {user_id} deleted")
        else:
            logs.append(f"Failed to delete user {user_id}")

        # Verificar que no existen
        remaining_tasks = get_tasks()
        remaining_users = get_users()
        assert all(t["id"] != task_id for t in remaining_tasks), "Task was not deleted"
        assert all(u["id"] != user_id for u in remaining_users), "User was not deleted"
        logs.append("Data cleanup verified")

        logs.append("Test completed successfully")

    except Exception as e:
        logs.append(f"Test failed: {str(e)}")

    # Generar el PDF
    generate_pdf_report(logs)

if __name__ == "__main__":
    integration_test()