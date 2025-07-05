import requests
from test_utils import TestDataTracker, PDFReportGenerator
import traceback
import sys
import os

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Initialize test utilities
tracker = TestDataTracker()
report_generator = PDFReportGenerator()

def create_user(name):
    try:
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()
        user_data = response.json()
        print("[SUCCESS] User created:", user_data)
        
        # Track the created user for cleanup
        tracker.track_user(user_data["id"])
        tracker.add_test_result("create_user", "PASSED", f"User '{name}' created with ID {user_data['id']}")
        
        return user_data["id"]
    except Exception as e:
        tracker.add_test_result("create_user", "FAILED", f"Error creating user '{name}': {str(e)}")
        raise

def create_task(user_id, description):
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        response.raise_for_status()
        task_data = response.json()
        print("[SUCCESS] Task created:", task_data)
        
        # Track the created task for cleanup
        tracker.track_task(task_data["id"])
        tracker.add_test_result("create_task", "PASSED", f"Task '{description}' created with ID {task_data['id']}")
        
        return task_data["id"]
    except Exception as e:
        tracker.add_test_result("create_task", "FAILED", f"Error creating task '{description}': {str(e)}")
        raise

def get_tasks():
    try:
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        tasks = response.json()
        tracker.add_test_result("get_tasks", "PASSED", f"Retrieved {len(tasks)} tasks")
        return tasks
    except Exception as e:
        tracker.add_test_result("get_tasks", "FAILED", f"Error retrieving tasks: {str(e)}")
        raise

def verify_task_user_association(user_id, task_id):
    try:
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        
        if any(t["id"] == task_id for t in user_tasks):
            tracker.add_test_result("verify_task_user_association", "PASSED", 
                                  f"Task {task_id} correctly associated with user {user_id}")
            return True
        else:
            tracker.add_test_result("verify_task_user_association", "FAILED", 
                                  f"Task {task_id} not found for user {user_id}")
            return False
    except Exception as e:
        tracker.add_test_result("verify_task_user_association", "FAILED", 
                              f"Error verifying task-user association: {str(e)}")
        raise

def integration_test():
    print("Starting Integration Test...")
    
    try:
        # Step 1: Create user
        print("\nStep 1: Creating user...")
        user_id = create_user("Camilo")

        # Step 2: Create task for that user
        print("\nStep 2: Creating task...")
        task_id = create_task(user_id, "Prepare presentation")

        # Step 3: Verify that the task is registered and associated with the user
        print("\nStep 3: Verifying task-user association...")
        if verify_task_user_association(user_id, task_id):
            print("SUCCESS: Test completed: task was successfully registered and linked to the user.")
            tracker.add_test_result("integration_test", "PASSED", "Full integration test completed successfully")
        else:
            print("FAILED: Test failed: task was not correctly registered")
            tracker.add_test_result("integration_test", "FAILED", "Task-user association verification failed")
            
    except Exception as e:
        print(f"FAILED: Test failed with error: {str(e)}")
        tracker.add_test_result("integration_test", "FAILED", f"Test failed with error: {str(e)}")
        traceback.print_exc()

def cleanup_and_verify():
    print("\n[CLEANUP] Starting data cleanup...")
    
    try:
        # Perform cleanup
        cleanup_results = tracker.cleanup_all_data()
        
        print(f"[SUCCESS] Cleanup completed:")
        print(f"   - Users deleted: {cleanup_results['users_deleted']}")
        print(f"   - Tasks deleted: {cleanup_results['tasks_deleted']}")
        
        if cleanup_results['errors']:
            print(f"   - Errors: {len(cleanup_results['errors'])}")
            for error in cleanup_results['errors']:
                print(f"     {error}")
        
        # Verify cleanup
        print("\n[VERIFY] Verifying cleanup...")
        verification_results = tracker.verify_cleanup()
        
        if verification_results['cleanup_verified']:
            print("[SUCCESS] Cleanup verification successful: All test data has been properly deleted")
            tracker.add_test_result("cleanup_verification", "PASSED", "All test data successfully deleted")
        else:
            print("[FAILED] Cleanup verification failed:")
            if verification_results['users_still_exist']:
                print(f"   - Users still exist: {verification_results['users_still_exist']}")
            if verification_results['tasks_still_exist']:
                print(f"   - Tasks still exist: {verification_results['tasks_still_exist']}")
            tracker.add_test_result("cleanup_verification", "FAILED", 
                                  f"Cleanup incomplete. Users: {verification_results['users_still_exist']}, Tasks: {verification_results['tasks_still_exist']}")
        
        return cleanup_results, verification_results
        
    except Exception as e:
        print(f"[FAILED] Cleanup failed with error: {str(e)}")
        tracker.add_test_result("cleanup_verification", "FAILED", f"Cleanup failed with error: {str(e)}")
        traceback.print_exc()
        return {'users_deleted': 0, 'tasks_deleted': 0, 'errors': [str(e)]}, {'cleanup_verified': False}

def generate_report(cleanup_results, verification_results):
    print("\n[REPORT] Generating PDF report...")
    
    try:
        report_path = report_generator.generate_report(
            test_results=tracker.test_results,
            cleanup_results=cleanup_results,
            verification_results=verification_results,
            test_type="Backend Integration Test"
        )
        print(f"[SUCCESS] Report generated successfully: {report_path}")
        return report_path
    except Exception as e:
        print(f"[FAILED] Report generation failed: {str(e)}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        # Run the integration test
        integration_test()
        
        # Cleanup and verify
        cleanup_results, verification_results = cleanup_and_verify()
        
        # Generate PDF report
        generate_report(cleanup_results, verification_results)
        
        print("\n[COMPLETE] Test execution completed!")
        
    except Exception as e:
        print(f"[FAILED] Test execution failed: {str(e)}")
        traceback.print_exc()