import time
import requests
import os
from TestLogger import TestLogger
from fpdf import FPDF

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name, logger):
    logger.add_log(f"Creating user: {name}")
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    user_id = user_data["id"]
    logger.add_log(f"User created: ID {user_id}", "PASS")
    return user_id

def create_task(user_id, description, logger):
    logger.add_log(f"Creating task: '{description}' for user {user_id}")
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    task_id = task_data["id"]
    logger.add_log(f"Task created: ID {task_id}", "PASS")
    return task_id

def get_tasks(logger):
    logger.add_log("Fetching all tasks")
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_user(user_id, logger):
    logger.add_log(f"Deleting user {user_id}")
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        logger.add_log(f"User {user_id} deleted", "PASS")
        return True
    logger.add_log(f"Failed to delete user {user_id}", "FAIL")
    return False

def delete_task(task_id, logger):
    logger.add_log(f"Deleting task {task_id}")
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        logger.add_log(f"Task {task_id} deleted", "PASS")
        return True
    logger.add_log(f"Failed to delete task {task_id}", "FAIL")
    return False

def generate_report(test_result):
    # Create reports directory if not exists
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # Find next available report number
    report_num = 1
    while os.path.exists(f"reports/report_{report_num}.pdf"):
        report_num += 1
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Test Report #{report_num}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Result: {'PASS' if test_result else 'FAIL'}", ln=True)
    pdf.output(f"reports/report_{report_num}.pdf")

def integration_test():
    logger = TestLogger("Backend Integration Test")
    logger.start_test()
    user_id = None
    task_id = None
    
    try:
        # Step 1: Create user
        user_id = create_user("Camilo", logger)
        
        # Step 2: Create task
        task_id = create_task(user_id, "Prepare presentation", logger)
        
        # Step 3: Verify task
        logger.add_log("Verifying task registration")
        tasks = get_tasks(logger)
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        
        if any(t["id"] == task_id for t in user_tasks):
            logger.add_log("Task verified in user's tasks", "PASS")
        else:
            logger.add_log("Task not found in user's tasks", "FAIL")
            raise Exception("Verification failed")
            
        logger.add_log("Test completed: task successfully registered", "PASS")
        
    except Exception as e:
        logger.add_log(f"Test failed: {str(e)}", "FAIL")
        
    finally:
        # Cleanup with verification
        if task_id:
            if delete_task(task_id, logger):
                # Add delay for DB sync
                time.sleep(1)
                
                # Verify deletion using the new endpoint
                response = requests.get(f"{TASKS_URL}/{task_id}")
                if response.status_code == 404:
                    logger.add_log(f"Verified task {task_id} deleted", "PASS")
                else:
                    logger.add_log(f"Task {task_id} still exists (status: {response.status_code})", "FAIL")
        
        if user_id:
            if delete_user(user_id, logger):
                # Verify deletion
                response = requests.get(f"{USERS_URL}/{user_id}")
                if response.status_code == 404:
                    logger.add_log(f"Verified user {user_id} deleted", "PASS")
                else:
                    logger.add_log(f"User {user_id} still exists", "FAIL")
        
        logger.end_test()
        report_num = logger.generate_pdf()
        print(f"Report generated: reports/report_{report_num:03d}.pdf")

if __name__ == "__main__":
    integration_test()