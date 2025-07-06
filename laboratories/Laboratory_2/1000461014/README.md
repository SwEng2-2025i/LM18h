# Laboratory 2 – Integration Testing

**Author:** Sebastián Moreno

## Lab Overview

The goal of this lab was to extend the integration testing system with two main features:

1. **Data Cleanup**: All data created during test execution must be deleted afterward (only the test data), and the tests must verify that the deletion was successful.
2. **Automatic PDF Report Generation**: Test results should be saved in a sequentially numbered PDF report. Previous reports must not be overwritten.

## Implemented Features

### 1. Data Cleanup

Data cleanup was implemented at the end of both backend and frontend integration tests. This ensures that:

- Any user or task created during testing is deleted afterward.
- The system verifies that the deletion was successful.

**Backend verification** was performed using direct calls.  
**Frontend verification** included both:

- **UI-based validation** with Selenium (refreshing the task list and submitting forms).
- **API validation** by checking the responses returned from the API endpoints.

### 2. PDF Report Generation

A shared utility (`report_generator.py`) was created to:

- Generate PDF reports using the `reportlab` library.
- Automatically assign sequential filenames (e.g., `backend_report_1.pdf`, `frontend_report_2.pdf`, etc.).
- Log each test step and result clearly.
- Store all reports in a `reports/` directory without overwriting previous ones.

## Modified and Added Files

| File | Description |
|------|-------------|
| `requirements.txt` | Corrected the file structure and added the missing the dependecies (+ `reportlab`). |
| `Task_Service/main.py` | Added a new `DELETE` endpoint to delete tasks by ID. |
| `User_Service/main.py` | Added a new `DELETE` endpoint to the users by ID. |
| `Test/BackEnd-Test.py` | Added data cleanup logic (`delete_user` and `delete_task`), data cleanup verification and logging in the test function (`integration_test`). Integrated PDF reporting. |
| `Test/FrontEnd-Test.py` | Added API-based data cleanup logic (`eliminar_usuario` and `eliminar_tarea`), UI-based visual data cleanup verification (`verificar_eliminacion_usuario_ui` and `verificar_eliminacion_tarea_ui`) , API-based data cleanup verification (`verificar_eliminacion_usuario_api` and `verificar_eliminacion_tarea_api`) , and logging in the test function (`main`). Integrated PDF reporting. |
| `report_generator.py` | **New file**: contains reusable logic for PDF report generation. |
| `README.md` | **New file**: summarizes lab implementation and highlights code changes. |

---

## How to Run the Tests

1. Make sure the backend services (`Users_Service`, `Task_Service`) and the frontend app are running.
2. Then execute:
```bash
python backend_test.py
python frontend_test.py
```
3. The reports will be saved automatically in the `\reports` folder.
