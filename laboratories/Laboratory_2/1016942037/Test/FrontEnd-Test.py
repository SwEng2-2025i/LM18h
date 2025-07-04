from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
from test_report import TestReport

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_text_in_element(driver, by, value, text, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((by, value), text)
    )

def create_user(driver, name, report):
    try:
        # Navigate to users page
        driver.get("http://localhost:5000")
        report.add_log("Navigated to frontend application")
        
        # Find and fill the name input
        name_input = wait_for_element(driver, By.ID, "username")
        name_input.clear()
        name_input.send_keys(name)
        report.add_log(f"Entered user name: {name}")
        
        # Click the create button
        create_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]")
        create_button.click()
        report.add_log("Clicked create user button")
        
        # Wait for the user to be created and get its ID
        result = wait_for_element(driver, By.ID, "user-result")
        wait_for_text_in_element(driver, By.ID, "user-result", "Usuario creado con ID")
        
        user_id = ''.join(filter(str.isdigit, result.text))
        report.add_log(f"User created successfully with ID: {user_id}")
        return user_id
    except Exception as e:
        report.add_log(f"Error creating user: {str(e)}", success=False)
        raise

def create_task(driver, user_id, description, report):
    try:
        report.add_log(f"Attempting to create task: '{description}' for user: {user_id}")
        
        # Find and fill the task description input
        task_input = wait_for_element(driver, By.ID, "task")
        task_input.clear()
        task_input.send_keys(description)
        report.add_log("Task description entered")
        
        # Find and fill the user ID input
        user_id_input = wait_for_element(driver, By.ID, "userid")
        user_id_input.clear()
        user_id_input.send_keys(str(user_id))
        report.add_log("User ID entered")
        
        # Click the create button
        create_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Tarea')]")
        create_button.click()
        report.add_log("Create task button clicked")
        
        # Wait for the task result to appear and contain success message
        result = wait_for_element(driver, By.ID, "task-result")
        wait_for_text_in_element(driver, By.ID, "task-result", "Tarea creada con ID")
        
        task_id = ''.join(filter(str.isdigit, result.text))
        report.add_log(f"Task created successfully with ID: {task_id}")
        return task_id
        
    except Exception as e:
        # Get the error message if it exists
        try:
            error_text = driver.find_element(By.ID, "task-result").text
            report.add_log(f"Task creation failed. Result text: {error_text}", success=False)
        except:
            report.add_log("No error message found in task-result element", success=False)
        
        report.add_log(f"Error during task creation: {str(e)}", success=False)
        raise

def verify_task_exists(driver, task_id, description, user_id, report):
    try:
        report.add_log(f"Verifying task existence: ID={task_id}, Description='{description}', User ID={user_id}")
        
        # Click the refresh button
        refresh_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]")
        refresh_button.click()
        report.add_log("Clicked refresh tasks button")
        
        # Wait for the tasks list to be present
        tasks_list = wait_for_element(driver, By.ID, "tasks")
        expected_text = f"{description} (Usuario ID: {user_id})"
        
        # Wait a bit for the list to update
        time.sleep(1)
        
        tasks_content = tasks_list.text
        report.add_log(f"Current tasks list content: '{tasks_content}'")
        
        if expected_text not in tasks_content:
            report.add_log(f"Task not found in the list: {expected_text}", success=False)
            raise Exception(f"Task not found in the list: {expected_text}")
            
        report.add_log("Task verified in the list")
    except Exception as e:
        report.add_log(f"Error verifying task: {str(e)}", success=False)
        raise

def delete_task(driver, task_id, report):
    try:
        # For now, we'll use the backend API to delete tasks since the frontend doesn't have delete functionality
        response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
        response.raise_for_status()
        report.add_log(f"Task {task_id} deleted")
    except Exception as e:
        report.add_log(f"Error deleting task: {str(e)}", success=False)
        raise

def delete_user(driver, user_id, report):
    try:
        # For now, we'll use the backend API to delete users since the frontend doesn't have delete functionality
        response = requests.delete(f"http://localhost:5001/users/{user_id}")
        response.raise_for_status()
        report.add_log(f"User {user_id} deleted")
    except Exception as e:
        report.add_log(f"Error deleting user: {str(e)}", success=False)
        raise

def verify_task_deleted(driver, task_id, report):
    try:
        report.add_log(f"Verifying task deletion: ID={task_id}")
        
        # Click the refresh button to update the list
        refresh_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]")
        refresh_button.click()
        report.add_log("Clicked refresh tasks button")
        
        # Wait for the tasks list to be present and check its content
        tasks_list = wait_for_element(driver, By.ID, "tasks")
        tasks_content = tasks_list.text
        report.add_log(f"Current tasks list content: '{tasks_content}'")
        
        if str(task_id) in tasks_content:
            report.add_log(f"Task {task_id} was not deleted", success=False)
            raise Exception(f"Task {task_id} was not deleted")
            
        report.add_log(f"Verified: Task {task_id} was successfully deleted")
    except Exception as e:
        report.add_log(f"Error verifying task deletion: {str(e)}", success=False)
        raise

def verify_user_deleted(driver, user_id, report):
    try:
        # We'll verify through the backend API since the frontend doesn't show users list
        response = requests.get("http://localhost:5001/users")
        users = response.json()
        if any(u["id"] == int(user_id) for u in users):
            report.add_log(f"User {user_id} was not deleted", success=False)
            raise Exception(f"User {user_id} was not deleted")
        report.add_log(f"Verified: User {user_id} was successfully deleted")
    except Exception as e:
        report.add_log(f"Error verifying user deletion: {str(e)}", success=False)
        raise

def integration_test():
    report = TestReport("Frontend Integration Test")
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    created_data = {"user_id": None, "task_id": None}
    
    try:
        # Step 1: Create user
        created_data["user_id"] = create_user(driver, "Camilo", report)
        
        # Step 2: Create task for that user
        created_data["task_id"] = create_task(driver, created_data["user_id"], "Terminar laboratorio", report)
        
        # Step 3: Verify the task appears in the list
        verify_task_exists(driver, created_data["task_id"], "Terminar laboratorio", created_data["user_id"], report)
        
        report.add_log("Test completed successfully: task was registered and linked to the user")
        
    except Exception as e:
        report.add_log(f"Test failed with error: {str(e)}", success=False)
        raise
        
    finally:
        try:
            # Cleanup: Delete created data in reverse order
            if created_data["task_id"]:
                delete_task(driver, created_data["task_id"], report)
                verify_task_deleted(driver, created_data["task_id"], report)
            
            if created_data["user_id"]:
                delete_user(driver, created_data["user_id"], report)
                verify_user_deleted(driver, created_data["user_id"], report)
        except Exception as e:
            report.add_log(f"Error during cleanup: {str(e)}", success=False)
        finally:
            # Close the browser
            driver.quit()
            report.end_test()
            report.generate_pdf()

if __name__ == "__main__":
    integration_test()
