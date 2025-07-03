import requests
import time
from datetime import datetime
from pdf_generator import create_test_result, generate_test_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Listas para rastrear IDs creados en este test
created_user_ids = []
created_task_ids = []

# Lista para capturar resultados de tests
test_results = []

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    # Rastrear el ID del usuario creado
    created_user_ids.append(user_data["id"])
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    # Rastrear el ID de la tarea creada
    created_task_ids.append(task_data["id"])
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def clear_test_data():
    """Clear only the data created by this test"""
    print(f"🧹 Limpiando {len(created_task_ids)} tareas y {len(created_user_ids)} usuarios creados en este test...")
    
    # Delete tasks created in this test
    for task_id in created_task_ids:
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            if response.status_code == 200:
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"⚠️ Failed to delete task {task_id}: {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️ Error deleting task {task_id}: {e}")

    # Delete users created in this test
    for user_id in created_user_ids:
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                print(f"✅ User {user_id} deleted successfully")
            else:
                print(f"⚠️ Failed to delete user {user_id}: {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️ Error deleting user {user_id}: {e}")
    
    # Clear the lists for future tests
    created_task_ids.clear()
    created_user_ids.clear()

def integration_test():
    start_time = time.time()
    test_output = []
    test_error = ""
    
    try:
        # Step 1: Create user
        test_output.append("🔄 Creando usuario...")
        user_id = create_user("Camilo")
        test_output.append(f"✅ Usuario creado con ID: {user_id}")

        # Step 2: Create task for that user
        test_output.append("🔄 Creando tarea...")
        task_id = create_task(user_id, "Prepare presentation")
        test_output.append(f"✅ Tarea creada con ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        test_output.append("🔄 Verificando asociación tarea-usuario...")
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        test_output.append("✅ Test completed: task was successfully registered and linked to the user.")
        
        # Capture successful result
        duration = f"{time.time() - start_time:.2f}s"
        test_result = create_test_result(
            name="Backend Integration Test",
            status="passed",
            duration=duration,
            output="\n".join(test_output),
            error=""
        )
        test_results.append(test_result)
        
    except Exception as e:
        # Capture failed result
        duration = f"{time.time() - start_time:.2f}s"
        test_error = str(e)
        test_output.append(f"❌ Test failed: {test_error}")
        
        test_result = create_test_result(
            name="Backend Integration Test",
            status="failed",
            duration=duration,
            output="\n".join(test_output),
            error=test_error
        )
        test_results.append(test_result)
        
        print(f"❌ Test failed: {test_error}")
        raise
        
    finally:
        # Clear test data at the end
        print("\n🧹 Cleaning up test data...")
        clear_test_data()

        # Generate PDF report
        print("\n📄 Generating PDF report...")
        try:
            pdf_path = generate_test_report(test_results)
            print(f"✅ PDF report generated successfully: {pdf_path}")
        except Exception as e:
            print(f"⚠️ Error generating PDF: {e}")


if __name__ == "__main__":
    integration_test()