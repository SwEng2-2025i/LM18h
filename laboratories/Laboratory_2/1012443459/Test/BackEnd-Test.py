import requests
from fpdf import FPDF
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
    return response.json()

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Backend Test Report', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

def task_exists(task_id):
    try:
        response = requests.get(f"{TASKS_URL}/{task_id}")
        return response.status_code == 200
    except Exception:
        return False

def user_exists(user_id):
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        return response.status_code == 200
    except Exception:
        return False

def create_report(test_results):
    
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)


    report_number = 1
    while os.path.exists(os.path.join(REPORTS_DIR, f'backend_report_{report_number}.pdf')):
        report_number += 1

    pdf = PDFReport()
    pdf.add_page()
    pdf.chapter_title(f'Backend Test Report #{report_number}')
    pdf.chapter_body(f'Test Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    pdf.chapter_title('Test Results:')
    for step, result in test_results.items():
        pdf.chapter_body(f'{step}: {result}')

    pdf.output(os.path.join(REPORTS_DIR, f'backend_report_{report_number}.pdf'))
    print(f"✅ Report saved as reports/backend_report_{report_number}.pdf")

def delete_user(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        return response.status_code == 200
    except Exception:
        return False

def delete_task(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        return response.status_code == 200
    except Exception:
        return False

def integration_test():
    test_results = {}
    user_id = None
    task_id = None

    try:
        # 1. Create user
        user_id = create_user("Camilo")
        test_results["User Creation"] = f"Success (ID: {user_id})"

        # 2. Create task
        task_id = create_task(user_id, "Prepare presentation")
        test_results["Task Creation"] = f"Success (ID: {task_id})"

        # 3. Verify user exists
        if user_exists(user_id):
            test_results["User Exists"] = "Success (User found)"
        else:
            test_results["User Exists"] = "Failed (User not found)"

        # 4. Verify task exists
        if task_exists(task_id):
            test_results["Task Exists"] = "Success (Task found)"
        else:
            test_results["Task Exists"] = "Failed (Task not found)"

        # 5. Delete user
        if delete_user(user_id):
            test_results["User Deletion"] = "Success"
        else:
            test_results["User Deletion"] = "Failed"

        # 6. Delete task
        if delete_task(task_id):
            test_results["Task Deletion"] = "Success"
        else:
            test_results["Task Deletion"] = "Failed"

        # 7. Verify user no longer exists
        if not user_exists(user_id):
            test_results["User Not Exists"] = "Success (User no longer exists)"
        else:
            test_results["User Not Exists"] = "Failed (User still exists)"

        # 8. Verify task no longer exists
        if not task_exists(task_id):
            test_results["Task Not Exists"] = "Success (Task no longer exists)"
        else:
            test_results["Task Not Exists"] = "Failed (Task still exists)"

        test_results["Overall Result"] = "SUCCESS"
        print("✅ Backend test completed successfully")

    except Exception as e:
        test_results["Overall Result"] = f"FAILED: {str(e)}"
        print(f"❌ Backend test failed: {str(e)}")

    create_report(test_results)

if __name__ == "__main__":
    integration_test()
