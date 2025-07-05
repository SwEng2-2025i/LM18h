import time
import os
import requests
import re
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestLogger import TestLogger

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

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

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

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

def main():
    logger = TestLogger("Frontend Integration Test")
    logger.start_test()
    user_id = None
    task_id = None
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        # Initialize WebDriverWait immediately after creating driver
        wait = WebDriverWait(driver, 10)  # <-- ADD THIS LINE
        
        # Step 1: Open frontend
        logger.add_log("Navigated to frontend application")
        driver.get("http://localhost:5000")
        
        # Wait for page to load completely
        wait.until(EC.presence_of_element_located((By.ID, "username")))
        
        # Step 2: Create user - ENHANCED USER ID EXTRACTION
        logger.add_log("Entered user name: Ana")
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys("Ana")
        
        logger.add_log("Clicked create user button")
        crear_usuario_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Crear Usuario')]"))
        )
        crear_usuario_btn.click()
        
        # Wait for user creation result
        wait.until(
            lambda driver: "creado" in driver.find_element(By.ID, "user-result").text.lower() or 
                          "error" in driver.find_element(By.ID, "user-result").text.lower()
        )
        
        user_result = driver.find_element(By.ID, "user-result").text
        logger.add_log(f"User creation result: {user_result}")
        
        # Extract user ID more reliably
        if "Usuario creado con ID" in user_result:
            # Try to find the ID number in the result text
            id_match = re.search(r'ID (\d+)', user_result)
            if id_match:
                user_id = id_match.group(1)
                logger.add_log(f"User created successfully with ID: {user_id}", "PASS")
            else:
                # Fallback to digit extraction
                digits = re.findall(r'\d+', user_result)
                if digits:
                    user_id = digits[0]
                    logger.add_log(f"Extracted user ID using fallback: {user_id}", "WARN")
                else:
                    logger.add_log("Failed to extract user ID", "FAIL")
                    raise Exception("User ID extraction failed")
        else:
            logger.add_log(f"Error creating user: {user_result}", "FAIL")
            raise Exception(f"User creation failed: {user_result}")
        
        # Now we have a valid user_id, proceed to task creation
        logger.add_log(f"Attempting to create task: 'Terminar laboratorio' for user: {user_id}")
        
        # Step 3: Create task - ENHANCED VERSION
        logger.add_log(f"Attempting to create task: 'Terminar laboratorio' for user: {user_id}")
        task_input = driver.find_element(By.ID, "task")
        task_input.clear()
        task_input.send_keys("Terminar laboratorio")
        
        userid_input = driver.find_element(By.ID, "userid")
        userid_input.clear()
        userid_input.send_keys(user_id)
        
        # Add delay to ensure input is processed
        time.sleep(0.5)
        
        logger.add_log("Clicked create task button")
        crear_tarea_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
        )
        crear_tarea_btn.click()
        
        # Wait for either success or error message
        wait.until(
            lambda driver: "Tarea creada" in driver.find_element(By.ID, "task-result").text or 
                          "Error" in driver.find_element(By.ID, "task-result").text
        )
        
        task_result = driver.find_element(By.ID, "task-result").text
        logger.add_log(f"Task creation result: {task_result}")
        
        if "Tarea creada con ID" in task_result:
            task_id = ''.join(filter(str.isdigit, task_result))
            logger.add_log(f"Task created successfully with ID: {task_id}", "PASS")
        else:
            # Capture detailed error
            error_details = driver.find_element(By.ID, "task-result").text
            logger.add_log(f"Error creating task: {error_details}", "FAIL")
            
            # Check if user exists in backend
            user_check = requests.get(f"{USERS_URL}/{user_id}")
            if user_check.status_code != 200:
                logger.add_log(f"User {user_id} not found in backend", "FAIL")
            
            # Take screenshot for debugging
            driver.save_screenshot("task_creation_error.png")
            raise Exception(f"Task creation failed: {error_details}")
        
        # Step 4: Verify tasks
        logger.add_log("Clicked refresh tasks button")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)
        
        tasks_element = driver.find_element(By.ID, "tasks")
        tasks_text = tasks_element.text
        logger.add_log(f"Current tasks list content: '{tasks_text}'")
        
        expected_text = f"Terminar laboratorio (Usuario ID: {user_id})"
        if expected_text in tasks_text:
            logger.add_log(f" Task verified in the list: {expected_text}", "PASS")
        else:
            logger.add_log(f"Task not found in list. Expected: {expected_text}", "FAIL")
            raise Exception("Task verification failed")
        
        logger.add_log("Test completed successfully", "PASS")

        # Wait for task creation to complete
        wait.until(
            lambda driver: "Tarea creada" in driver.find_element(By.ID, "task-result").text or 
                          "Error" in driver.find_element(By.ID, "task-result").text
        )
        
        task_result = driver.find_element(By.ID, "task-result").text
        if "Tarea creada con ID" in task_result:
            task_id = ''.join(filter(str.isdigit, task_result))
            logger.add_log(f"Task created successfully with ID: {task_id}", "PASS")
            return task_id
        else:
            # Capture detailed error
            error_details = driver.find_element(By.ID, "task-result").text
            logger.add_log(f"Error creating task: {error_details}", "FAIL")
            raise Exception(f"Task creation failed: {error_details}")
        
    except Exception as e:
        driver.save_screenshot("task_creation_error.png")
        logger.add_log(f"Task creation failed: {str(e)}", "FAIL")
        raise
        
    finally:
        # Cleanup data
        if user_id:
            logger.add_log("Cleaning up test data")
            # Delete tasks first
            tasks = requests.get(TASKS_URL).json()
            for task in tasks:
                if task['user_id'] == int(user_id):
                    response = requests.delete(f"{TASKS_URL}/{task['id']}")
                    if response.status_code == 200:
                        logger.add_log(f"Task {task['id']} deleted", "PASS")
                    else:
                        logger.add_log(f"Failed to delete task {task['id']}", "FAIL")
            
            # Delete user
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                logger.add_log(f"User {user_id} deleted", "PASS")
            else:
                logger.add_log(f"Failed to delete user {user_id}", "FAIL")
            
            # Verify deletion
            response = requests.get(f"{USERS_URL}/{user_id}")
            if response.status_code == 404:
                logger.add_log(f"Verified user {user_id} deleted", "PASS")
            else:
                logger.add_log(f"User {user_id} still exists", "FAIL")
        
        driver.quit()
        logger.end_test()
        report_num = logger.generate_pdf()
        print(f"Report generated: reports/report_{report_num:03d}.pdf")

if __name__ == "__main__":
    main()
