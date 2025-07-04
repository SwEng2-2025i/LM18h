import requests
from pdf_report_generator import PDFReportGenerator

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Test data tracking
test_data = {
    'created_users': [],
    'created_tasks': []
}

# Test results tracking
test_results = []

def create_user(name):
    try:
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()
        user_data = response.json()
        print("✅ User created:", user_data)
        test_data['created_users'].append(user_data["id"])
        test_results.append({
            'step': f'Create user "{name}"',
            'status': 'PASS',
            'details': f'User created with ID {user_data["id"]}'
        })
        return user_data["id"]
    except Exception as e:
        test_results.append({
            'step': f'Create user "{name}"',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def create_task(user_id, description):
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        response.raise_for_status()
        task_data = response.json()
        print("✅ Task created:", task_data)
        test_data['created_tasks'].append(task_data["id"])
        test_results.append({
            'step': f'Create task "{description}"',
            'status': 'PASS',
            'details': f'Task created with ID {task_data["id"]} for user {user_id}'
        })
        return task_data["id"]
    except Exception as e:
        test_results.append({
            'step': f'Create task "{description}"',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def get_tasks():
    try:
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        tasks = response.json()
        test_results.append({
            'step': 'Get tasks list',
            'status': 'PASS',
            'details': f'Retrieved {len(tasks)} tasks'
        })
        return tasks
    except Exception as e:
        test_results.append({
            'step': 'Get tasks list',
            'status': 'FAIL',
            'details': f'Error: {str(e)}'
        })
        raise

def cleanup_test_data():
    """Clean up only the test data created during this test run and verify deletion"""
    cleanup_results = []
    
    # Clean up specific tasks first (due to foreign key relationship)
    if test_data['created_tasks']:
        try:
            response = requests.delete(f"{TASKS_URL}/cleanup-specific", 
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
            response = requests.delete(f"{USERS_URL}/cleanup-specific", 
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
                user_response = requests.get(f"{USERS_URL}/{user_id}")
                if user_response.status_code == 200:
                    remaining_users.append(user_id)
            except:
                pass  # User doesn't exist, which is what we want
        
        # Check if our specific tasks still exist
        for task_id in test_data['created_tasks']:
            try:
                # Get all tasks and check if our task ID is still there
                tasks_response = requests.get(TASKS_URL)
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

def integration_test():
    """Main integration test with cleanup and PDF reporting"""
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        if any(t["id"] == task_id for t in user_tasks):
            test_results.append({
                'step': 'Verify task registration',
                'status': 'PASS',
                'details': f'Task {task_id} correctly registered and linked to user {user_id}'
            })
            print("✅ Test completed: task was successfully registered and linked to the user.")
        else:
            test_results.append({
                'step': 'Verify task registration',
                'status': 'FAIL',
                'details': 'Task was not correctly registered or linked to user'
            })
            raise AssertionError("❌ The task was not correctly registered")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        # Always perform cleanup and generate report
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
            test_type="Backend Integration Test",
            test_results=test_results,
            created_data=created_data,
            cleanup_results=cleanup_results
        )
        
        print("✅ Cleanup and reporting completed!")


if __name__ == "__main__":
    integration_test()