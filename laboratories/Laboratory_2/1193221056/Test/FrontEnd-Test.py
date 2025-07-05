import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_generator import PDFReportGenerator

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.clear() # Limpiar campo antes de escribir
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.clear()  # Limpiar campo antes de escribir
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
    # Extraer y retornar el task_id
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def eliminar_tarea_api(task_id):
    """Delete task using direct API call"""
    try:
        response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
        if response.status_code == 200:
            print(f"Task {task_id} deleted successfully via API")
            return True
        else:
            print(f"Error deleting task {task_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")
        return False

def eliminar_usuario_api(user_id):
    """Delete user using direct API call"""
    try:
        response = requests.delete(f"http://localhost:5001/users/{user_id}")
        if response.status_code == 200:
            print(f"User {user_id} deleted successfully via API")
            return True
        else:
            print(f"Error deleting user {user_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")
        return False 


def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    start_time = time.time()
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    
    created_user_id = None
    created_task_id = None
    report_generator = PDFReportGenerator()
    
    # Initialize test results structure
    test_results = {
        'overall_success': False,
        'steps': [],
        'cleanup': []
    }

    try:
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Open frontend
        try:
            abrir_frontend(driver)
            test_results['steps'].append({
                'step_number': 1,
                'description': 'Open Frontend Application',
                'success': True,
                'details': 'Frontend loaded successfully at http://localhost:5000'
            })
        except Exception as e:
            test_results['steps'].append({
                'step_number': 1,
                'description': 'Open Frontend Application',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise
        
        # Step 2: Create user
        try:
            created_user_id = crear_usuario(driver, wait)
            test_results['steps'].append({
                'step_number': 2,
                'description': 'Create User via UI',
                'success': True,
                'details': f'User "Ana" created with ID: {created_user_id}'
            })
            print(f"Created user with ID: {created_user_id}")
        except Exception as e:
            test_results['steps'].append({
                'step_number': 2,
                'description': 'Create User via UI',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise
        
        # Step 3: Create task
        try:
            created_task_id = crear_tarea(driver, wait, created_user_id)
            test_results['steps'].append({
                'step_number': 3,
                'description': 'Create Task via UI',
                'success': True,
                'details': f'Task "Terminar laboratorio" created with ID: {created_task_id}'
            })
            print(f"Created task with ID: {created_task_id}")
        except Exception as e:
            test_results['steps'].append({
                'step_number': 3,
                'description': 'Create Task via UI',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise
        
        # Step 4: Verify task display
        try:
            ver_tareas(driver)
            test_results['steps'].append({
                'step_number': 4,
                'description': 'Verify Task Display in UI',
                'success': True,
                'details': 'Task appears correctly in task list'
            })
            print("Frontend test completed successfully")
            test_results['overall_success'] = True
        except Exception as e:
            test_results['steps'].append({
                'step_number': 4,
                'description': 'Verify Task Display in UI',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise
        
    except Exception as e:
        print(f"Test failed: {e}")
        test_results['overall_success'] = False
        
    finally:
        # Step 5: Cleanup
        if created_task_id or created_user_id:
            print(f"\n🧹 Starting cleanup of test data...")
            
            # Delete task first (foreign key constraint) via API
            if created_task_id:
                try:
                    success = eliminar_tarea_api(created_task_id)
                    test_results['cleanup'].append({
                        'action': f'Delete Task {created_task_id}',
                        'success': success,
                        'details': 'Task deleted via API' if success else 'Failed to delete task via API'
                    })
                except Exception as e:
                    test_results['cleanup'].append({
                        'action': f'Delete Task {created_task_id}',
                        'success': False,
                        'details': f'Error: {str(e)}'
                    })
            
            # Delete user via API
            if created_user_id:
                try:
                    success = eliminar_usuario_api(created_user_id)
                    test_results['cleanup'].append({
                        'action': f'Delete User {created_user_id}',
                        'success': success,
                        'details': 'User deleted via API' if success else 'Failed to delete user via API'
                    })
                except Exception as e:
                    test_results['cleanup'].append({
                        'action': f'Delete User {created_user_id}',
                        'success': False,
                        'details': f'Error: {str(e)}'
                    })
        
        # Generate PDF Report
        execution_time = time.time() - start_time
        try:
            report_path = report_generator.generate_report(
                test_type="Frontend Integration Test",
                test_results=test_results,
                execution_time=execution_time
            )
            print(f"PDF Report saved to: {report_path}")
        except Exception as e:
            print(f"Error generating PDF report: {e}")
        
        time.sleep(3)  # Final delay to observe results
        driver.quit()  # Always close the browser

if __name__ == "__main__":
    main()