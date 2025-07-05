import sys
import os
import time
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_utils import TestDataTracker, PDFReportGenerator

# Initialize test utilities
tracker = TestDataTracker()
report_generator = PDFReportGenerator()

def abrir_frontend(driver):
    """Opens the frontend application in the browser"""
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)  # Give the page time to load
        tracker.add_test_result("abrir_frontend", "PASSED", "Frontend opened successfully")
        return True
    except Exception as e:
        tracker.add_test_result("abrir_frontend", "FAILED", f"Error opening frontend: {str(e)}")
        return False

def crear_usuario(driver, wait):
    """Fills out the user creation form and submits it"""
    try:
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("Ana")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
        time.sleep(2)

        user_result = driver.find_element(By.ID, "user-result").text
        # Filter out Unicode characters for console output
        user_result_clean = ''.join(char for char in user_result if ord(char) < 128)
        print("Resultado usuario:", user_result_clean)
        
        if "Usuario creado con ID" in user_result:
            user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
            
            # Track the created user for cleanup
            tracker.track_user(int(user_id))
            tracker.add_test_result("crear_usuario", "PASSED", f"User 'Ana' created with ID {user_id}")
            return user_id
        else:
            tracker.add_test_result("crear_usuario", "FAILED", f"User creation failed: {user_result}")
            return None
            
    except Exception as e:
        tracker.add_test_result("crear_usuario", "FAILED", f"Error creating user: {str(e)}")
        raise

def crear_tarea(driver, wait, user_id):
    """Fills out the task creation form with a task and user ID, then submits it"""
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
        # Filter out Unicode characters for console output
        task_result_clean = ''.join(char for char in task_result.text if ord(char) < 128)
        print("Texto en task_result:", task_result_clean)
        
        if "Tarea creada con ID" in task_result.text:
            task_id = ''.join(filter(str.isdigit, task_result.text))
            
            # Track the created task for cleanup
            tracker.track_task(int(task_id))
            tracker.add_test_result("crear_tarea", "PASSED", f"Task 'Terminar laboratorio' created with ID {task_id}")
            return task_id
        else:
            tracker.add_test_result("crear_tarea", "FAILED", f"Task creation failed: {task_result.text}")
            return None
            
    except Exception as e:
        tracker.add_test_result("crear_tarea", "FAILED", f"Error creating task: {str(e)}")
        raise

def ver_tareas(driver):
    """Clicks the button to refresh the task list and verifies the new task appears"""
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)

        tasks = driver.find_element(By.ID, "tasks").text
        # Filter out Unicode characters for console output
        tasks_clean = ''.join(char for char in tasks if ord(char) < 128)
        print("Tareas:", tasks_clean)
        
        if "Terminar laboratorio" in tasks:
            tracker.add_test_result("ver_tareas", "PASSED", "Task 'Terminar laboratorio' found in task list")
            return True
        else:
            tracker.add_test_result("ver_tareas", "FAILED", "Task 'Terminar laboratorio' not found in task list")
            return False
            
    except Exception as e:
        tracker.add_test_result("ver_tareas", "FAILED", f"Error viewing tasks: {str(e)}")
        raise

def cleanup_and_verify():
    """Clean up all tracked test data and verify cleanup"""
    print("\n[CLEANUP] Starting data cleanup...")
    
    try:
        # Perform cleanup
        cleanup_results = tracker.cleanup_all_data()
        
        print(f"[OK] Cleanup completed:")
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
            print("[OK] Cleanup verification successful: All test data has been properly deleted")
            tracker.add_test_result("cleanup_verification", "PASSED", "All test data successfully deleted")
        else:
            print("[ERROR] Cleanup verification failed:")
            if verification_results['users_still_exist']:
                print(f"   - Users still exist: {verification_results['users_still_exist']}")
            if verification_results['tasks_still_exist']:
                print(f"   - Tasks still exist: {verification_results['tasks_still_exist']}")
            tracker.add_test_result("cleanup_verification", "FAILED", 
                                  f"Cleanup incomplete. Users: {verification_results['users_still_exist']}, Tasks: {verification_results['tasks_still_exist']}")
        
        return cleanup_results, verification_results
        
    except Exception as e:
        print(f"[ERROR] Cleanup failed with error: {str(e)}")
        tracker.add_test_result("cleanup_verification", "FAILED", f"Cleanup failed with error: {str(e)}")
        traceback.print_exc()
        return {'users_deleted': 0, 'tasks_deleted': 0, 'errors': [str(e)]}, {'cleanup_verified': False}

def generate_report(cleanup_results, verification_results):
    """Generate PDF report with test results"""
    print("\n[REPORT] Generating PDF report...")
    
    try:
        report_path = report_generator.generate_report(
            test_results=tracker.test_results,
            cleanup_results=cleanup_results,
            verification_results=verification_results,
            test_type="Frontend E2E Test"
        )
        print(f"[OK] Report generated successfully: {report_path}")
        return report_path
    except Exception as e:
        print(f"[ERROR] Report generation failed: {str(e)}")
        traceback.print_exc()
        return None

def main():
    """Main test runner that initializes the browser and runs the full E2E flow"""
    print("[START] Starting Frontend E2E Test...")
    
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    
    cleanup_results = {'users_deleted': 0, 'tasks_deleted': 0, 'errors': []}
    verification_results = {'cleanup_verified': False}

    try:
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Open frontend
        print("\n[STEP 1] Opening frontend...")
        if not abrir_frontend(driver):
            raise Exception("Failed to open frontend")
        
        # Step 2: Create user
        print("\n[STEP 2] Creating user...")
        user_id = crear_usuario(driver, wait)
        if not user_id:
            raise Exception("Failed to create user")
        
        # Step 3: Create task
        print("\n[STEP 3] Creating task...")
        task_id = crear_tarea(driver, wait, user_id)
        if not task_id:
            raise Exception("Failed to create task")
        
        # Step 4: Verify task appears in list
        print("\n[STEP 4] Verifying task in list...")
        if ver_tareas(driver):
            print("[OK] Frontend E2E test completed successfully!")
            tracker.add_test_result("frontend_e2e_test", "PASSED", "Complete E2E test flow successful")
        else:
            print("[ERROR] Frontend E2E test failed!")
            tracker.add_test_result("frontend_e2e_test", "FAILED", "Task verification failed")
        
        time.sleep(3)  # Final delay to observe results if not running headless
        
    except Exception as e:
        print(f"[ERROR] Frontend E2E test failed with error: {str(e)}")
        tracker.add_test_result("frontend_e2e_test", "FAILED", f"E2E test failed with error: {str(e)}")
        traceback.print_exc()
        
    finally:
        driver.quit()  # Always close the browser at the end
        
        # Cleanup and verify
        cleanup_results, verification_results = cleanup_and_verify()
        
        # Generate PDF report
        generate_report(cleanup_results, verification_results)
        
        print("\n[COMPLETE] Test execution completed!")

if __name__ == "__main__":
    main()
