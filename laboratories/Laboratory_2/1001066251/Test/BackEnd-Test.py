import requests
import os
import io
import contextlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

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
    response = requests.post(TASKS_URL, json={"title": description, "user_id": user_id})
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"Task with ID {task_id} deleted.")
    verify_response = requests.get(f"{TASKS_URL}/{task_id}")
    assert verify_response.status_code == 404, "Task was not correctly deleted."
    print(f"✅ Verification: Task {task_id} has been deleted.")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"User with ID {user_id} deleted.")
    verify_response = requests.get(f"{USERS_URL}/{user_id}")
    assert verify_response.status_code == 404, "User was not correctly deleted."
    print(f"✅ Verification: User {user_id} has been deleted.")

def generate_pdf_report(content, test_name="Backend_Test"):
    report_num = 1
    while os.path.exists(f"{test_name}_Report_{report_num}.pdf"):
        report_num += 1
    file_name = f"{test_name}_Report_{report_num}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, f"Test Report: {test_name}")
    c.setFont("Helvetica", 10)
    text = c.beginText(inch, height - 1.5 * inch)
    text.setFont("Courier", 9)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()
    print(f"Report saved as: {file_name}")

def integration_test():
    user_id = None
    task_id = None
    output_capture = io.StringIO()

    with contextlib.redirect_stdout(output_capture):
        try:
            
            user_id = create_user("Camilo")
            task_id = create_task(user_id, "Prepare presentation")
            tasks = get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == user_id]
            assert any(t["id"] == task_id for t in user_tasks), "Task was not correctly registered"
            print("\n✅ Test completed: task was successfully registered.")

        except Exception as e:
            print(f"\n❌ TEST FAILED with error: {e}")

        finally:
            print("\n--- Starting cleanup ---")
            if task_id:
                try:
                    delete_task(task_id)
                except Exception as e:
                    print(f"❌ FAILED to delete task {task_id}: {e}")

            if user_id:
                try:
                    delete_user(user_id)
                except Exception as e:
                    print(f"❌ FAILED to delete user {user_id}: {e}")

            print("Cleanup phase finished.")

    test_output = output_capture.getvalue()
    print(test_output)
    generate_pdf_report(test_output)

if __name__ == "__main__":
    integration_test()