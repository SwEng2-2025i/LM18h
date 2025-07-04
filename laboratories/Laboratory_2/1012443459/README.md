Lab 2 Julio Cesar Albadan Sarmiento

### 1. Services and Modified Code

**`Test/BackEnd-Test.py`**

**New Functions Added:**

1. `task_exists(task_id)` - Verifies if a task exists via API

2. `user_exists(user_id)` - Checks user existence via API

3. `delete_task(task_id)` - Deletes a task through API call

4. `delete_user(user_id)` - Removes a user through API call

5. `create_report(test_results)` - Generates PDF reports with:

    - PDFReport helper class for formatting

    - Automatic report numbering

    - Timestamped results

**Modified Flow:**

- Expanded `integration_test()` to include:

    - Pre-deletion verification

    - Cleanup operations

    - Post-deletion validation

    - Detailed result tracking

**`Test/FrontEnd-Test.py`**

**New Functions Added:**

1. `task_exists(task_id)` - API check for task existence

2. `user_exists(user_id)` - API check for user existence

3. `delete_task(task_id)` - API task deletion

4. `delete_user(user_id)` - API user deletion

5. `create_report(test_results)` - PDF generation with:

   -  Dynamic report paths

    - Consistent formatting

    - Error state tracking

**Enhanced Functions:**

- crear_tarea() now returns task ID from UI

- main() includes full test lifecycle:

    - Creation → Verification → Deletion → Final check

**`Users_Service/main.py`**

**New Endpoint:**
```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted successfully'}), 200
```
**Behavior:**

- Validates user existence

- Atomic deletion with session commit

- Returns appropriate HTTP status codes

- Clear success/error messages

**`Task_Service/main.py`**

**New Endpoints:**

1. Task Retrieval:
```python
@service_b.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    with Session(db.engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id})
```

2. Task Deletion:
```python
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task_id} deleted successfully'}), 200
```
**Key Features:**

- Session-managed database operations

- Consistent error handling (404 for missing resources)

- Transaction safety with explicit commits

- Detailed response messages


### 2. Enhanced Test Suites
##### FrontEnd-Test Changes:

- Added PDF report generation capability
- Implemented comprehensive test data cleanup
- Added verification steps for created/deleted resources
- Improved error handling and reporting
- Added API endpoints for direct service communication

##### BackEnd-Test Changes:

- Added PDF report generation matching FrontEnd-Test format
- Implemented the same test data cleanup pattern
- Added verification steps for all operations
- Improved test structure with clear phases

### 3. New Dependencies
Updated `requirements.txt`

### 4. Report Generation System
Both test scripts now generate PDF reports with:

- Sequential numbering (prevents overwrites)
- Timestamp of test execution
- Detailed results of each test step
- Clear success/failure indicators
- Organized sections for different test phases
Reports are saved in a reports/ directory with filenames:

- frontend_report_[N].pdf
- backend_report_[N].pdf

### Test Execution Flow

1) FrontEnd-Test:

- Opens web interface
- Creates test user
- Creates test task
- Verifies resources exist
- Deletes test data
- Verifies deletion
- Generates PDF report
2) BackEnd-Test:

- Creates test user via API
- Creates test task via API
- Verifies task-user association
- Deletes test data via API
- Verifies deletion
- Generates PDF report
### Verification System
Both test suites now verify:

- Successful creation of resources

- Proper association between users and tasks

- Successful deletion of test data

- Complete cleanup (resources no longer exist after deletion)

### How to Run
1. Install dependencies:

```bash
pip install -r requirements.txt
```
2. Start services in separate terminals.
3. Run tests.
4. View generated reports in the reports/ directory.