# Integration Test Report — BackEnd & FrontEnd

Este documento describe las modificaciones realizadas a los archivos de prueba de integración del sistema, tanto del **BackEnd** como del **FrontEnd**, en cumplimiento de los requisitos ampliados del laboratorio de pruebas. Los cambios incluyen limpieza de datos, verificación de eliminaciones y generación automática de reportes en PDF.

---

## 🖥 BackEnd — `BackEnd-Test.py`

### Funcionalidades Implementadas

#### 1. Limpieza de Datos (Data Cleanup)
Al finalizar el test:
- Se elimina la **tarea** creada usando `DELETE /tasks/<task_id>`.
- Se elimina el **usuario** creado usando `DELETE /users/<user_id>`.

#### 2. Verificación de Eliminación
Posteriormente:
- Se consulta nuevamente la lista completa de tareas y usuarios.
- Se valida que las entidades eliminadas no estén presentes en el sistema.

#### 3. Generación de Reporte en PDF
- Se genera un archivo PDF con un registro paso a paso del test.
- Los reportes se almacenan en la carpeta `/backend_reports/`.
- Cada archivo se numera secuencialmente (`report_1.pdf`, `report_2.pdf`, etc.).
- Los reportes anteriores **no se sobrescriben**.

---

### Secciones de Código Agregadas o Modificadas

- `delete_task(task_id)` y `delete_user(user_id)`  
  Envía peticiones `DELETE` a los servicios correspondientes.

- `get_next_report_number()` y `generate_pdf_report()`  
  Gestionan la numeración secuencial y la generación del PDF con la librería `fpdf`.

- `integration_test()`  
  Ampliado para incluir:
  - Limpieza de datos creados durante la prueba.
  - Validación de eliminaciones exitosas.
  - Registro detallado de cada paso.
  - Generación del reporte en PDF.
  - Opción de impresión en consola para depuración.

- Registro de Logs (`logs`)  
  Todos los eventos y errores se almacenan en una lista `logs` que se imprime en consola y se incluye en el PDF.

---

### Requisitos Previos

Para ejecutar el test de backend, asegúrate de que:
- Los servicios `users_service` y `task_service` implementen los endpoints:
  - `DELETE /users/<user_id>`
  - `DELETE /tasks/<task_id>`

---

## 🌐 FrontEnd — `FrontEnd-Test.py`

### Funcionalidades Implementadas

#### 1. Limpieza de Datos (Data Cleanup)

Se implementó la función `eliminar_datos()` que elimina los datos creados desde la interfaz web:

```python
requests.delete(f"http://localhost:5002/tasks/{task_id}")
requests.delete(f"http://localhost:5001/users/{user_id}")
```

#### 2. Verificación de Eliminación

Se comprueba que los elementos fueron eliminados correctamente:

```python
assert requests.get(f"http://localhost:5001/users/{user_id}").status_code == 404
assert requests.get(f"http://localhost:5002/tasks/{task_id}").status_code == 404
```

#### 3. Generación de Reporte en PDF

* Se implementó `generate_pdf_report(logs)`, que guarda un registro de la ejecución en un archivo PDF.
* Los archivos se guardan secuencialmente en la carpeta `frontend_reports/`.

Para evitar errores con caracteres especiales:

```python
pdf.multi_cell(0, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'))
```

---

### Notas Técnicas

* Se utiliza `logs.append(...)` para capturar cada paso importante.
* Se manejan excepciones para imprimir errores tanto en consola como en el PDF.

---