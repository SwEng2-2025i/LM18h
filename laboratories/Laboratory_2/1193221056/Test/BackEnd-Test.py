import requests
import time
from report_generator import PDFReportGenerator

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks


def integration_test():
    start_time = time.time()
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
        print("Starting integration test...")
        
        # Step 1: Create user
        try:
            created_user_id = create_user("Camilo")
            test_results['steps'].append({
                'step_number': 1,
                'description': 'Create User',
                'success': True,
                'details': f'User created with ID: {created_user_id}'
            })
        except Exception as e:
            test_results['steps'].append({
                'step_number': 1,
                'description': 'Create User',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise

        # Step 2: Create task
        try:
            created_task_id = create_task(created_user_id, "Prepare presentation")
            test_results['steps'].append({
                'step_number': 2,
                'description': 'Create Task',
                'success': True,
                'details': f'Task created with ID: {created_task_id}'
            })
        except Exception as e:
            test_results['steps'].append({
                'step_number': 2,
                'description': 'Create Task',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise

        # Step 3: Verify task registration
        try:
            tasks = get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == created_user_id]
            task_found = any(t["id"] == created_task_id for t in user_tasks)
            
            if task_found:
                test_results['steps'].append({
                    'step_number': 3,
                    'description': 'Verify Task Registration',
                    'success': True,
                    'details': 'Task successfully linked to user'
                })
                print("Test completed: task was successfully registered and linked to the user.")
                test_results['overall_success'] = True
            else:
                raise AssertionError("Task was not correctly registered")
                
        except Exception as e:
            test_results['steps'].append({
                'step_number': 3,
                'description': 'Verify Task Registration',
                'success': False,
                'details': f'Error: {str(e)}'
            })
            raise

    except Exception as e:
        print(f"Test failed: {e}")
        test_results['overall_success'] = False
        
    finally:
        # Step 4: Cleanup
        if created_task_id or created_user_id:
            print(f"\n Starting cleanup of test data...")
            
            # Delete task first
            if created_task_id:
                try:
                    delete_task(created_task_id)
                    test_results['cleanup'].append({
                        'action': f'Delete Task {created_task_id}',
                        'success': True,
                        'details': 'Task deleted successfully'
                    })
                except Exception as e:
                    test_results['cleanup'].append({
                        'action': f'Delete Task {created_task_id}',
                        'success': False,
                        'details': f'Error: {str(e)}'
                    })
            
            # Delete user
            if created_user_id:
                try:
                    delete_user(created_user_id)
                    test_results['cleanup'].append({
                        'action': f'Delete User {created_user_id}',
                        'success': True,
                        'details': 'User deleted successfully'
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
                test_type="Backend Integration Test",
                test_results=test_results,
                execution_time=execution_time
            )
            print(f"PDF Report saved to: {report_path}")
        except Exception as e:
            print(f"Error generating PDF report: {e}")        
            


def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print("✅ User deleted successfully")
    
def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print("✅ Task deleted successfully")
    
    
if __name__ == "__main__":
    integration_test()