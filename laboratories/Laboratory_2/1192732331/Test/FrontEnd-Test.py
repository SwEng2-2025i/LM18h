import time
import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# API Endpoints for cleanup
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

class FrontEndTestTracker:
    """Class to track frontend test data for cleanup"""
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = []
        self.user_name = None
        self.task_description = None
    
    def add_user(self, user_id, name=None):
        self.created_users.append(user_id)
        if name:
            self.user_name = name
    
    def add_task(self, task_id, description=None):
        self.created_tasks.append(task_id)
        if description:
            self.task_description = description
    
    def add_result(self, test_name, status, message):
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

# Global tracker instance
tracker = FrontEndTestTracker()

def delete_user_api(user_id):
    """Delete a specific user via API"""
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"✅ User {user_id} deleted successfully via API")
            return True
        else:
            print(f"❌ Failed to delete user {user_id} via API: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error deleting user {user_id}: {str(e)}")
        return False

def delete_task_api(task_id):
    """Delete a specific task via API"""
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"✅ Task {task_id} deleted successfully via API")
            return True
        else:
            print(f"❌ Failed to delete task {task_id} via API: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error deleting task {task_id}: {str(e)}")
        return False

def get_users_api():
    """Get all users via API"""
    try:
        response = requests.get(USERS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting users: {str(e)}")
        return []

def get_tasks_api():
    """Get all tasks via API"""
    try:
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting tasks: {str(e)}")
        return []

def cleanup_frontend_test_data():
    """Clean up all frontend test data and verify deletion"""
    print("\n🧹 Starting frontend data cleanup...")
    
    # Delete all created tasks
    cleanup_success = True
    for task_id in tracker.created_tasks:
        if not delete_task_api(task_id):
            cleanup_success = False
    
    # Delete all created users
    for user_id in tracker.created_users:
        if not delete_user_api(user_id):
            cleanup_success = False
    
    # Verify all data was deleted
    verification_success = verify_frontend_cleanup()
    
    overall_success = cleanup_success and verification_success
    tracker.add_result("Frontend Data Cleanup", "PASS" if overall_success else "FAIL", 
                      "All frontend test data cleaned up successfully" if overall_success else "Some frontend test data cleanup failed")
    
    return overall_success

def verify_frontend_cleanup():
    """Verify that all frontend test data has been properly deleted"""
    print("\n🔍 Verifying frontend data cleanup...")
    
    try:
        # Check if any of our test users still exist
        users = get_users_api()
        remaining_users = [u for u in users if u['id'] in tracker.created_users]
        
        # Check if any of our test tasks still exist
        tasks = get_tasks_api()
        remaining_tasks = [t for t in tasks if t['id'] in tracker.created_tasks]
        
        if remaining_users:
            print(f"❌ Found {len(remaining_users)} users that should have been deleted: {remaining_users}")
            return False
        
        if remaining_tasks:
            print(f"❌ Found {len(remaining_tasks)} tasks that should have been deleted: {remaining_tasks}")
            return False
        
        print("✅ All frontend test data successfully deleted and verified")
        return True
        
    except Exception as e:
        print(f"❌ Error during frontend cleanup verification: {str(e)}")
        return False

def generate_frontend_pdf_report():
    """Generate a PDF report with frontend test results"""
    print("\n📄 Generating frontend PDF report...")
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Find the next sequential number
    existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("frontend_test_report_") and f.endswith(".pdf")]
    if existing_reports:
        numbers = []
        for report in existing_reports:
            try:
                num = int(report.split("_")[-1].split(".")[0])
                numbers.append(num)
            except ValueError:
                continue
        next_num = max(numbers) + 1 if numbers else 1
    else:
        next_num = 1
    
    filename = f"frontend_test_report_{next_num:03d}.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    # Create PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Frontend Integration Test Report")
    
    # Report info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Report Number: {next_num:03d}")
    c.drawString(50, height - 100, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "Test Configuration:")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 160, f"User Name: {tracker.user_name or 'Ana'}")
    c.drawString(50, height - 175, f"Task Description: {tracker.task_description or 'Terminar laboratorio'}")
    c.drawString(50, height - 190, f"Browser: Chrome (Selenium WebDriver)")
    
    # Test results
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 220, "Test Results:")
    
    y_position = height - 250
    c.setFont("Helvetica", 11)
    
    for result in tracker.test_results:
        c.drawString(50, y_position, f"• {result['test']}: {result['status']}")
        c.drawString(70, y_position - 15, f"  {result['message']}")
        c.drawString(70, y_position - 30, f"  Time: {result['timestamp']}")
        y_position -= 50
    
    # Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position - 20, "Summary:")
    c.setFont("Helvetica", 11)
    
    total_tests = len(tracker.test_results)
    passed_tests = len([r for r in tracker.test_results if r['status'] == 'PASS'])
    failed_tests = total_tests - passed_tests
    
    c.drawString(50, y_position - 40, f"Total Tests: {total_tests}")
    c.drawString(50, y_position - 55, f"Passed: {passed_tests}")
    c.drawString(50, y_position - 70, f"Failed: {failed_tests}")
    
    c.save()
    print(f"✅ Frontend PDF report generated: {filepath}")
    return filepath

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)  # Give the page time to load
        tracker.add_result("Frontend Access", "PASS", "Successfully opened frontend application")
        return True
    except Exception as e:
        tracker.add_result("Frontend Access", "FAIL", f"Failed to open frontend: {str(e)}")
        return False

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    try:
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("Ana")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
        time.sleep(2)

        user_result = driver.find_element(By.ID, "user-result").text
        print("Resultado usuario:", user_result)
        assert "Usuario creado con ID" in user_result
        user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
        
        # Track the created user
        tracker.add_user(int(user_id), "Ana")
        tracker.add_result("User Creation via Frontend", "PASS", f"User created successfully with ID: {user_id}")
        
        return user_id
    except Exception as e:
        tracker.add_result("User Creation via Frontend", "FAIL", f"Failed to create user: {str(e)}")
        raise

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    try:
        task_input = driver.find_element(By.ID, "task")
        task_input.send_keys("Terminar laboratorio")
        time.sleep(1)

        userid_input = driver.find_element(By.ID, "userid")
        userid_input.send_keys(user_id)
        userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
        time.sleep(1)

        crear_tarea_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
        )
        crear_tarea_btn.click()
        time.sleep(2)

        wait.until(
            EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
        )
        task_result = driver.find_element(By.ID, "task-result")
        print("Texto en task_result:", task_result.text)
        assert "Tarea creada con ID" in task_result.text
        
        # Extract task ID from result
        task_id = ''.join(filter(str.isdigit, task_result.text.split("ID")[-1]))
        
        # Track the created task
        tracker.add_task(int(task_id), "Terminar laboratorio")
        tracker.add_result("Task Creation via Frontend", "PASS", f"Task created successfully with ID: {task_id}")
        
    except Exception as e:
        tracker.add_result("Task Creation via Frontend", "FAIL", f"Failed to create task: {str(e)}")
        raise

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)

        tasks = driver.find_element(By.ID, "tasks").text
        print("Tareas:", tasks)
        assert "Terminar laboratorio" in tasks
        
        tracker.add_result("Task Verification via Frontend", "PASS", "Task successfully displayed in task list")
        
    except Exception as e:
        tracker.add_result("Task Verification via Frontend", "FAIL", f"Failed to verify task: {str(e)}")
        raise

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    print("🚀 Starting Frontend Integration Test...")
    
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        
        # Execute frontend tests
        if abrir_frontend(driver):
            user_id = crear_usuario(driver, wait)
            crear_tarea(driver, wait, user_id)
            ver_tareas(driver)
            time.sleep(3)  # Final delay to observe results if not running headless
            
        # Clean up test data
        cleanup_success = cleanup_frontend_test_data()
        
        # Generate PDF report
        generate_frontend_pdf_report()
        
        print("\n✅ Frontend Integration Test completed with cleanup and reporting!")
        
    except Exception as e:
        print(f"❌ Frontend test failed: {str(e)}")
        tracker.add_result("Frontend Test Execution", "FAIL", f"Test failed with error: {str(e)}")
        
        # Still try to clean up and generate report
        cleanup_frontend_test_data()
        generate_frontend_pdf_report()
        
    finally:
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
