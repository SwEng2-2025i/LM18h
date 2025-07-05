# Laboratory 2: Integration Testing with Data Cleanup and Automated Reporting

## 1. Project Summary

This repository contains the solution for Laboratory 2. The objective was to extend a base microservices system and its integration tests to include two critical features: **automatic test data cleanup (Data Cleanup)** and **automatic generation of result reports in PDF format**.

The base system consists of a user service, a task service, and a frontend, along with test scripts for the backend and the frontend (E2E). The modifications ensure that the testing environment is robust, clean, and that its results are well-documented.

---

## 2. Implementation and Added Code Sections

Below are the details of the implementations and the key code snippets that were added to meet the requirements.

### 2.1. Data Cleanup

A cleanup mechanism was implemented to ensure that all data generated during test execution (users and tasks) are deleted upon completion.

#### **Backend Modifications**

`DELETE` endpoints were added to the services to allow for the deletion of resources by their ID.

*Code added to `users_service/main.py` and `task_service/main.py`:*
```python
# Added function to delete users created in tests
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User with id {user_id} deleted.'}), 200

```
```python
# Ruta para borrar una tarea
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': f'Task with id {task_id} deleted.'}), 200
```

#### **Test Script Modifications**

To ensure that cleanup always runs, the `finally` block in both test scripts (`Backend-test.py` and `FrontEnd-test.py`) was restructured. Each delete operation was wrapped in its own `try...except` block to ensure that if one fails, the others still execute.

*Code added to the `integration_test` function in `Test/Backend-test.py`:*
```python
finally:
    print("\n--- Starting cleanup ---")
    
    # Independently try to delete the task
    if task_id:
        try:
            delete_task(task_id) # This function now includes deletion verification (404)
        except Exception as e:
            print(f"❌ FAILED to delete task {task_id}: {e}")

    # Independently try to delete the user, regardless of prior failure
    if user_id:
        try:
            delete_user(user_id) # This function also verifies deletion
        except Exception as e:
            print(f"❌ FAILED to delete user {user_id}: {e}")
```

### 2.2. Automatic PDF Report Generation

A system was implemented for each test run to generate a unique and sequential PDF report with the results.

#### **Output Capturing**

Python's `contextlib` module was used to redirect all console output to an in-memory variable during the test execution.

*Code added to the `main` functions of the test scripts:*
```python
# All output is captured in this variable
output_capture = io.StringIO()

with contextlib.redirect_stdout(output_capture):
    try:
            
        user_id = create_user("Camilo")
        task_id = create_task(user_id, "Prepare presentation")
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "Task was not correctly registered"
        print("\n✅ Test completed: task was successfully registered.")

    except Exception as e:
        print(f"\n❌ TEST FAILED with error: {e}")

    finally:
        print("\n--- Starting cleanup ---")
        if task_id:
            try:
                delete_task(task_id)
            except Exception as e:
                print(f"❌ FAILED to delete task {task_id}: {e}")

        if user_id:
            try:
                delete_user(user_id)
            except Exception as e:
                print(f"❌ FAILED to delete user {user_id}: {e}")

        print("Cleanup phase finished.")
    # At the end, the content is extracted and the PDF is generated
    test_output = output_capture.getvalue()
    print(test_output) # The output is printed to the real console
    generate_pdf_report(test_output)
```

#### **PDF File Generation**

A `generate_pdf_report` function was created using the `reportlab` library. This function checks for existing files to name the new report with a sequential number, avoiding overwrites.

*Function added to both test scripts:*
```python
def generate_pdf_report(content, test_name="Backend_Test"):
    report_num = 1
    while os.path.exists(f"{test_name}_Report_{report_num}.pdf"):
        report_num += 1
    file_name = f"{test_name}_Report_{report_num}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, f"Test Report: {test_name}")
    c.setFont("Helvetica", 10)
    text = c.beginText(inch, height - 1.5 * inch)
    text.setFont("Courier", 9)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()
    print(f"Report saved as: {file_name}")
```
---

## 3. How to Run the Project

1.  **Install Dependencies**:
    ```bash
    pip install flask flask_sqlalchemy flask_cors requests selenium reportlab
    ```
2.  **Start the Services** (each in a separate terminal):
    * `python Users_Service/main.py`
    * `python Task_Service/main.py`
    * `python Front-End/main.py`
3.  **Run the Tests** (in another terminal):
    * `python Test/Backend-test.py`
    * `python Test/FrontEnd-test.py`