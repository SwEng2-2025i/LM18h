# Integration Test Report — BackEnd

This document describes the modifications made to the original backend integration test script (`BackEnd-Test.py`) to fulfill the extended requirements of the testing lab. The updated script now includes data cleanup, validation of deletions, and automatic PDF report generation.

---

## Features Implemented on BackEnd-Test

### 1. Data Cleanup
At the end of the test:
- The **task** created during testing is deleted using a `DELETE /tasks/<task_id>` request.
- The **user** created during testing is deleted using a `DELETE /users/<user_id>` request.

### 2. Verification of Deletion
After deletion:
- The test fetches the full list of tasks and users again.
- It verifies that the created entries no longer exist in the system.

### 3. PDF Report Generation
- The script generates a PDF file with a step-by-step log of the test execution.
- Reports are stored in the `/reports/` directory.
- Each report is assigned a unique sequential number (e.g., `report_1.pdf`, `report_2.pdf`, etc.).
- Previous reports are never overwritten.

---

## code Sections Added or Modified

###  `delete_task(task_id)` and `delete_user(user_id)`
Located in the test script, these helper functions send `DELETE` requests to the corresponding services.

### `get_next_report_number()` and `generate_pdf_report()`
These functions handle sequential numbering and PDF generation using the `fpdf` library.

### Updated `integration_test()` logic
- Extended to include:
  - Cleanup of test data
  - Validation that data is successfully deleted
  - Logging of every step in the process
  - Generation of the PDF report
  - Optional console printing of logs for debugging

### Logging
All relevant steps and errors are saved in a `logs` list and written to both the PDF file and the console.

---

## Requirements

To run the updated test:
- Ensure both services (`users_service` and `task_service`) implement `DELETE` endpoints:
  - `DELETE /users/<user_id>`
  - `DELETE /tasks/<task_id>`
- Install the `fpdf` library:


```bash
pip install fpdf
```
## Features Implemented on FrontEnd-Test

# Laboratorio de Pruebas de Integración

Se documentan los cambios realizados a los archivos de prueba de integración para los servicios Front-End del sistema, según los requisitos del laboratorio. Las modificaciones aseguran limpieza de datos, verificación de eliminación, y generación automática de reportes PDF para cada ejecución.

---

Cambios en el archivo FrontEnd-Test.py
1. Limpieza de Datos (Data Cleanup)
Se implementó una función eliminar_datos() que elimina el usuario y la tarea creados desde la interfaz web usando requests.


requests.delete(f"http://localhost:5002/tasks/{task_id}")
requests.delete(f"http://localhost:5001/users/{user_id}")

2. Verificación de Eliminación

Se agregó una verificación para comprobar que los datos ya no existen después de ser eliminados.

assert requests.get(f"http://localhost:5001/users/{user_id}").status_code == 404
assert requests.get(f"http://localhost:5002/tasks/{task_id}").status_code == 404

3. Generación de Reporte PDF
Se generó una función generate_pdf_report(logs) que guarda los pasos del test y resultados en un archivo PDF secuencial en la carpeta reports_frontend/.

Para evitar errores con caracteres especiales, se codifican las líneas en latin-1:

python
Copiar
Editar
pdf.multi_cell(0, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'))

### Notas técnicas:
Se eliminaron los emojis del contenido textual para evitar errores de codificación.

Se agregaron logs (logs.append(...)) en cada paso para capturar el historial en el PDF.

Se manejaron excepciones para imprimir errores específicos en consola y en el PDF.
```


