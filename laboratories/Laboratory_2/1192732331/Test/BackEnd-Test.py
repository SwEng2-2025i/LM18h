import requests
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

class TestDataTracker:
    """Class to track test data for cleanup"""
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = []
    
    def add_user(self, user_id):
        self.created_users.append(user_id)
    
    def add_task(self, task_id):
        self.created_tasks.append(task_id)
    
    def add_result(self, test_name, status, message):
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

# Global tracker instance
tracker = TestDataTracker()

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    tracker.add_user(user_data["id"])
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    tracker.add_task(task_data["id"])
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

def delete_user(user_id):
    """Delete a specific user"""
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ User {user_id} deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete user {user_id}: {response.text}")
        return False

def delete_task(task_id):
    """Delete a specific task"""
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Task {task_id} deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete task {task_id}: {response.text}")
        return False

def cleanup_test_data():
    """Clean up all test data and verify deletion"""
    print("\n🧹 Starting data cleanup...")
    
    # Delete all created tasks
    cleanup_success = True
    for task_id in tracker.created_tasks:
        if not delete_task(task_id):
            cleanup_success = False
    
    # Delete all created users
    for user_id in tracker.created_users:
        if not delete_user(user_id):
            cleanup_success = False
    
    # Verify all data was deleted
    verification_success = verify_cleanup()
    
    overall_success = cleanup_success and verification_success
    tracker.add_result("Data Cleanup", "PASS" if overall_success else "FAIL", 
                      "All test data cleaned up successfully" if overall_success else "Some test data cleanup failed")
    
    return overall_success

def verify_cleanup():
    """Verify that all test data has been properly deleted"""
    print("\n🔍 Verifying data cleanup...")
    
    try:
        # Check if any of our test users still exist
        users = get_users()
        remaining_users = [u for u in users if u['id'] in tracker.created_users]
        
        # Check if any of our test tasks still exist
        tasks = get_tasks()
        remaining_tasks = [t for t in tasks if t['id'] in tracker.created_tasks]
        
        if remaining_users:
            print(f"❌ Found {len(remaining_users)} users that should have been deleted: {remaining_users}")
            return False
        
        if remaining_tasks:
            print(f"❌ Found {len(remaining_tasks)} tasks that should have been deleted: {remaining_tasks}")
            return False
        
        print("✅ All test data successfully deleted and verified")
        return True
        
    except Exception as e:
        print(f"❌ Error during cleanup verification: {str(e)}")
        return False

def generate_pdf_report():
    """Generate a PDF report with test results"""
    print("\n📄 Generating PDF report...")
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Find the next sequential number
    existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("backend_test_report_") and f.endswith(".pdf")]
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
    
    filename = f"backend_test_report_{next_num:03d}.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    # Create PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Backend Integration Test Report")
    
    # Report info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Report Number: {next_num:03d}")
    c.drawString(50, height - 100, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test results
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "Test Results:")
    
    y_position = height - 170
    c.setFont("Helvetica", 11)
    
    for result in tracker.test_results:
        status_color = "green" if result['status'] == 'PASS' else "red"
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
    print(f"✅ PDF report generated: {filepath}")
    return filepath

def integration_test():
    """Main integration test with data cleanup"""
    print("🚀 Starting Backend Integration Test...")
    
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        tracker.add_result("User Creation", "PASS", f"User created successfully with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        tracker.add_result("Task Creation", "PASS", f"Task created successfully with ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        if any(t["id"] == task_id for t in user_tasks):
            print("✅ Test completed: task was successfully registered and linked to the user.")
            tracker.add_result("Task Association", "PASS", "Task correctly associated with user")
        else:
            print("❌ The task was not correctly registered")
            tracker.add_result("Task Association", "FAIL", "Task not correctly associated with user")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        tracker.add_result("Integration Test", "FAIL", f"Test failed with error: {str(e)}")
    
    # Step 4: Clean up test data
    cleanup_success = cleanup_test_data()
    
    # Step 5: Generate PDF report
    generate_pdf_report()
    
    print("\n✅ Backend Integration Test completed with cleanup and reporting!")
    return cleanup_success

if __name__ == "__main__":
    integration_test()