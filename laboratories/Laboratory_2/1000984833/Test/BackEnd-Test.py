# import requests

# #----------------------------------------------------------
# #---------------------- BACKEND-TEST ----------------------
# #----------------------------------------------------------

# # Endpoints
# USERS_URL = "http://localhost:5001/users"
# TASKS_URL = "http://localhost:5002/tasks"

# def create_user(name):
#     response = requests.post(USERS_URL, json={"name": name})
#     response.raise_for_status()
#     user_data = response.json()
#     print("✅ User created:", user_data)
#     return user_data["id"]

# def create_task(user_id, description):
#     response = requests.post(TASKS_URL, json={
#         "title": description,
#         "user_id": user_id
#     })
#     response.raise_for_status()
#     task_data = response.json()
#     print("✅ Task created:", task_data)
#     return task_data["id"]

# def get_tasks():
#     response = requests.get(TASKS_URL)
#     response.raise_for_status()
#     tasks = response.json()
#     return tasks

# def integration_test():
#     # Step 1: Create user
#     user_id = create_user("Camilo")

#     # Step 2: Create task for that user
#     task_id = create_task(user_id, "Prepare presentation")

#     # Step 3: Verify that the task is registered and associated with the user
#     tasks = get_tasks()
#     user_tasks = [t for t in tasks if t["user_id"] == user_id]

#     assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
#     print("✅ Test completed: task was successfully registered and linked to the user.")


# if __name__ == "__main__":
#     integration_test()


# ./Test/BackEnd-Test.py

import requests
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

#----------------------------------------------------------
#---------------------- BACKEND-TEST ----------------------
#----------------------------------------------------------

# --- CONFIGURACIÓN ---
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')

# --- FUNCIONES PARA GENERAR REPORTES PDF ---
def get_next_report_filename(base_name="Backend_Test_Report"):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    
    files = [f for f in os.listdir(REPORTS_DIR) if f.startswith(base_name) and f.endswith('.pdf')]
    if not files:
        return os.path.join(REPORTS_DIR, f"{base_name}_1.pdf")

    max_num = 0
    for f in files:
        match = re.search(r'_(\d+)\.pdf$', f)
        if match:
            max_num = max(max_num, int(match.group(1)))
            
    return os.path.join(REPORTS_DIR, f"{base_name}_{max_num + 1}.pdf")

def generate_pdf_report(filename, logs, test_name="Backend Integration Test"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, test_name)
    
    c.setFont("Helvetica", 10)
    c.drawString(inch, height - inch - 20, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    c.line(inch, height - inch - 30, width - inch, height - inch - 30)
    
    text = c.beginText(inch, height - inch - 50)
    text.setFont("Courier", 9)
    
    for log in logs:
        text.textLine(log)
    
    c.drawText(text)
    c.save()
    print(f"✅ Report generated: {filename}")

# --- LÓGICA DEL TEST ---
def integration_test():
    logs = []
    created_user_id = None
    created_task_id = None
    
    try:
        # Step 1: Create user
        user_name = "Camilo"
        logs.append(f"STEP 1: Creating user '{user_name}'...")
        response = requests.post(USERS_URL, json={"name": user_name})
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        user_data = response.json()
        created_user_id = user_data["id"]
        logs.append(f"  -> SUCCESS: User created with ID {created_user_id}")

        # Step 2: Create task for that user
        task_description = "Prepare presentation"
        logs.append(f"\nSTEP 2: Creating task '{task_description}' for user ID {created_user_id}...")
        response = requests.post(TASKS_URL, json={"title": task_description, "user_id": created_user_id})
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        task_data = response.json()
        created_task_id = task_data["id"]
        logs.append(f"  -> SUCCESS: Task created with ID {created_task_id}")

        # Step 3: Verify that the task is registered
        logs.append(f"\nSTEP 3: Verifying task registration...")
        response = requests.get(TASKS_URL)
        assert response.status_code == 200
        tasks = response.json()
        user_tasks = [t for t in tasks if t.get("user_id") == created_user_id]
        assert any(t["id"] == created_task_id for t in user_tasks), "Task was not correctly registered"
        logs.append("  -> SUCCESS: Task is correctly registered and linked to the user.")
        
        logs.append("\n✅ ALL TESTS PASSED")

    except AssertionError as e:
        logs.append(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        logs.append(f"\n❌ AN UNEXPECTED ERROR OCCURRED: {e}")

    finally:
        # Step 4: Data Cleanup
        logs.append("\n--- CLEANUP ---")
        if created_task_id:
            logs.append(f"CLEANUP: Deleting task ID {created_task_id}...")
            response = requests.delete(f"{TASKS_URL}/{created_task_id}")
            if response.status_code == 200:
                logs.append("  -> SUCCESS: Task deleted.")
                # Verify deletion
                verify_resp = requests.get(f"{TASKS_URL}/{created_task_id}")
                if verify_resp.status_code == 404:
                     logs.append("  -> VERIFIED: Task no longer exists (404).")
                else:
                     logs.append(f"  -> FAILED VERIFICATION: Task still exists (Status {verify_resp.status_code}).")
            else:
                logs.append(f"  -> FAILED: Could not delete task (Status {response.status_code}).")

        if created_user_id:
            logs.append(f"CLEANUP: Deleting user ID {created_user_id}...")
            response = requests.delete(f"{USERS_URL}/{created_user_id}")
            if response.status_code == 200:
                logs.append("  -> SUCCESS: User deleted.")
                # Verify deletion
                verify_resp = requests.get(f"{USERS_URL}/{created_user_id}")
                if verify_resp.status_code == 404:
                     logs.append("  -> VERIFIED: User no longer exists (404).")
                else:
                     logs.append(f"  -> FAILED VERIFICATION: User still exists (Status {verify_resp.status_code}).")
            else:
                logs.append(f"  -> FAILED: Could not delete user (Status {response.status_code}).")

        # Generate PDF Report
        report_filename = get_next_report_filename()
        generate_pdf_report(report_filename, logs)

if __name__ == "__main__":
    integration_test()