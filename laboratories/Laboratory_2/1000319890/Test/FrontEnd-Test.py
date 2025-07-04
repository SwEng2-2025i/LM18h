import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_report_generator import PDFReportGenerator

# Test data tracking
test_data = {
    'created_users': [],
    'created_tasks': []
}

# Test results tracking
test_results = []

def abrir_frontend(driver):
    """Opens the frontend application in the browser"""
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)  # Give the page time to load
        test_results.append({
            'step': 'Open frontend application',
            'status': 'PASS',
            'details': 'Successfully opened http://localhost:5000'
        })
    except Exception as e:
        test_results.append({
            'step': 'Open frontend application',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def crear_usuario(driver, wait):
    """Fills out the user creation form and submits it
    Then retrieves and returns the newly created user ID"""
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
        
        test_data['created_users'].append(int(user_id))
        test_results.append({
            'step': 'Create user via frontend',
            'status': 'PASS',
            'details': f'User "Ana" created with ID {user_id}'
        })
        
        return user_id
    except Exception as e:
        test_results.append({
            'step': 'Create user via frontend',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def crear_tarea(driver, wait, user_id):
    """Fills out the task creation form with a task and user ID, then submits it
    Waits until the confirmation text appears and asserts the result"""
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
        
        task_id = ''.join(filter(str.isdigit, task_result.text))  # Extract numeric ID from result
        test_data['created_tasks'].append(int(task_id))
        test_results.append({
            'step': 'Create task via frontend',
            'status': 'PASS',
            'details': f'Task "Terminar laboratorio" created with ID {task_id} for user {user_id}'
        })
        
    except Exception as e:
        test_results.append({
            'step': 'Create task via frontend',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def ver_tareas(driver):
    """Clicks the button to refresh the task list and verifies the new task appears"""
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)

        tasks = driver.find_element(By.ID, "tasks").text
        print("Tareas:", tasks)
        assert "Terminar laboratorio" in tasks
        
        test_results.append({
            'step': 'Verify task in list',
            'status': 'PASS',
            'details': f'Task "Terminar laboratorio" found in task list'
        })
        
    except Exception as e:
        test_results.append({
            'step': 'Verify task in list',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def cleanup_test_data():
    """Clean up only the test data created during this test run via API and verify deletion"""
    cleanup_results = []
    
    # Clean up specific tasks first (due to foreign key relationship)
    if test_data['created_tasks']:
        try:
            response = requests.delete("http://localhost:5002/tasks/cleanup-specific", 
                                     json={'task_ids': test_data['created_tasks']})
            if response.status_code == 200:
                cleanup_results.append({
                    'operation': f'Delete specific tasks ({len(test_data["created_tasks"])} tasks)',
                    'status': 'SUCCESS',
                    'details': response.json().get('message', 'Tasks deleted')
                })
            else:
                cleanup_results.append({
                    'operation': f'Delete specific tasks ({len(test_data["created_tasks"])} tasks)',
                    'status': 'FAILED',
                    'details': f'HTTP {response.status_code}: {response.text}'
                })
        except Exception as e:
            cleanup_results.append({
                'operation': f'Delete specific tasks ({len(test_data["created_tasks"])} tasks)',
                'status': 'FAILED',
                'details': f'Error: {str(e)}'
            })
    else:
        cleanup_results.append({
            'operation': 'Delete specific tasks',
            'status': 'SKIPPED',
            'details': 'No tasks were created during this test'
        })
    
    # Clean up specific users
    if test_data['created_users']:
        try:
            response = requests.delete("http://localhost:5001/users/cleanup-specific", 
                                     json={'user_ids': test_data['created_users']})
            if response.status_code == 200:
                cleanup_results.append({
                    'operation': f'Delete specific users ({len(test_data["created_users"])} users)',
                    'status': 'SUCCESS',
                    'details': response.json().get('message', 'Users deleted')
                })
            else:
                cleanup_results.append({
                    'operation': f'Delete specific users ({len(test_data["created_users"])} users)',
                    'status': 'FAILED',
                    'details': f'HTTP {response.status_code}: {response.text}'
                })
        except Exception as e:
            cleanup_results.append({
                'operation': f'Delete specific users ({len(test_data["created_users"])} users)',
                'status': 'FAILED',
                'details': f'Error: {str(e)}'
            })
    else:
        cleanup_results.append({
            'operation': 'Delete specific users',
            'status': 'SKIPPED',
            'details': 'No users were created during this test'
        })
    
    # Verify cleanup by checking if our specific test data is gone
    try:
        verification_failed = False
        remaining_users = []
        remaining_tasks = []
        
        # Check if our specific users still exist
        for user_id in test_data['created_users']:
            try:
                user_response = requests.get(f"http://localhost:5001/users/{user_id}")
                if user_response.status_code == 200:
                    remaining_users.append(user_id)
            except:
                pass  # User doesn't exist, which is what we want
        
        # Check if our specific tasks still exist
        for task_id in test_data['created_tasks']:
            try:
                # Get all tasks and check if our task ID is still there
                tasks_response = requests.get("http://localhost:5002/tasks")
                if tasks_response.status_code == 200:
                    tasks = tasks_response.json()
                    for task in tasks:
                        if task['id'] == task_id:
                            remaining_tasks.append(task_id)
                            break
            except:
                pass
        
        if not remaining_users and not remaining_tasks:
            cleanup_results.append({
                'operation': 'Verify cleanup of test data',
                'status': 'SUCCESS',
                'details': 'All test data successfully removed'
            })
        else:
            cleanup_results.append({
                'operation': 'Verify cleanup of test data',
                'status': 'FAILED',
                'details': f'Test data still exists: {remaining_users} users, {remaining_tasks} tasks'
            })
    except Exception as e:
        cleanup_results.append({
            'operation': 'Verify cleanup of test data',
            'status': 'FAILED',
            'details': f'Verification error: {str(e)}'
        })
    
    return cleanup_results

def main():
    """Main test runner that initializes the browser and runs the full E2E flow"""
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        time.sleep(3)  # Final delay to observe results if not running headless
        
        print("✅ All frontend tests passed!")
        
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        raise
    finally:
        driver.quit()  # Always close the browser at the end
        
        # Perform cleanup and generate report
        print("\n🧹 Performing cleanup...")
        cleanup_results = cleanup_test_data()
        
        # Generate PDF report
        print("\n📄 Generating PDF report...")
        pdf_generator = PDFReportGenerator()
        created_data = {
            'Users Created': test_data['created_users'],
            'Tasks Created': test_data['created_tasks']
        }
        
        pdf_generator.generate_report(
            test_type="Frontend E2E Test",
            test_results=test_results,
            created_data=created_data,
            cleanup_results=cleanup_results
        )
        
        print("✅ Cleanup and reporting completed!")

if __name__ == "__main__":
    main()
