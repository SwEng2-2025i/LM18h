
# Proyecto de Pruebas de Integración - Sistema de Gestión de Usuarios y Tareas

Este proyecto implementa un sistema distribuido basado en microservicios para la gestión de usuarios y tareas. Incluye un conjunto completo de **pruebas automatizadas** de integración y pruebas end-to-end (E2E), junto con generación automática de reportes en PDF y limpieza de datos de prueba tras cada ejecución.

---

## Arquitectura del Sistema

### Servicios Backend

- **Users_Service** (Puerto 5001): Gestión de usuarios.
- **Task_Service** (Puerto 5002): Gestión de tareas.
- **Front-End** (Puerto 5000): Interfaz web para interacción con los servicios.

### Componentes de Prueba

- **BackEnd-Test.py**: Pruebas de integración de APIs (CRUD).
- **FrontEnd-Test.py**: Pruebas E2E usando Selenium.

---

## Funcionalidades Implementadas

### APIs de Usuario (Users_Service)

- ✅ `POST /users` - Crear usuario.  
- ✅ `GET /users/<id>` - Obtener usuario por ID.  
- ✅ `GET /users` - Listar todos los usuarios.  
- ✅ `DELETE /users/<id>` - Eliminar usuario *(implementado para limpieza de pruebas)*.

### APIs de Tareas (Task_Service)

- ✅ `POST /tasks` - Crear tarea.  
- ✅ `GET /tasks` - Obtener todas las tareas.  
- ✅ `DELETE /tasks/<id>` - Eliminar tarea *(implementado para limpieza de pruebas)*.  
- ✅ `GET /tasks/<id>` - Obtener tarea específica (para verificación tras eliminar).

### Front-End Web

- ✅ Formulario para crear usuarios y tareas.  
- ✅ Visualización de lista de tareas.  
- ✅ Validación de campos en formularios.

---

## Cambios y Mejoras Implementadas

### Limpieza de Datos de Prueba

Se agregaron rutas `DELETE` en los servicios backend que permiten eliminar usuarios y tareas creados durante las pruebas.  
Los scripts de prueba implementan bloques `try...finally` para asegurar que la limpieza ocurra incluso si las pruebas fallan.

Ejemplo:
```python
finally:
    if created_user_id:
        requests.delete(f"{USERS_URL}/{created_user_id}")
        verify_resp = requests.get(f"{USERS_URL}/{created_user_id}")
        assert verify_resp.status_code == 404
```

### Generación Automática de Reportes PDF

Se usa la librería `reportlab` para crear reportes PDF secuenciales. Cada ejecución de prueba genera un nuevo archivo numerado automáticamente en el directorio `Test/reports`.

Características:

- Registro detallado de acciones y resultados (creación, verificación, eliminación).
- Títulos, fechas y contenido formateado.
- Reportes separados para pruebas backend y frontend.

Ejemplo de función:
```python
def generate_pdf_report(filename, logs, test_name):
    c = canvas.Canvas(filename, pagesize=letter)
    # ... contenido del PDF ...
    c.save()
```

---

## Instalación y Configuración

### Requisitos

- Python 3.8+
- Google Chrome (para pruebas E2E)
- ChromeDriver

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

Dependencias clave:

- `flask`
- `flask_sqlalchemy`
- `requests`
- `selenium`
- `reportlab`

---

## Ejecución del Proyecto

### 1. Iniciar Servicios

En terminales separadas:

```bash
# Servicio de usuarios
cd Users_Service
python main.py

# Servicio de tareas
cd Task_Service
python main.py

# Frontend
cd Front-End
python main.py
```

### 2. Ejecutar Pruebas

```bash
# Pruebas de backend
cd Test
python BackEnd-Test.py

# Pruebas E2E
cd Test
python FrontEnd-Test.py
```

---

## Resultados de las Pruebas

- Reportes PDF generados automáticamente:
  - `Backend_Test_Report_X.pdf`
  - `Frontend_Test_Report_X.pdf`
- ✅ 100% cobertura de APIs críticas.
- ✅ Verificación automática post-eliminación (status 404).
- ✅ Reportes visuales con ✅ / ❌ según el resultado.

---

## Tecnologías de Pruebas y Reportes

- **Pruebas**: Selenium WebDriver, Requests.
- **Reportes**: ReportLab.

---

## Autor

Cristian Barrera

---

---

## Ejemplos de Resultados de Prueba

### ✅ Frontend E2E Test
**Fecha:** 2025-07-05 19:35:46

```
STEP 1: Opening frontend application...
 -> SUCCESS: Frontend opened successfully.
STEP 2: Creating user 'Ana E2E'...
 -> SUCCESS: User created with ID 1.
STEP 3: Creating task 'Terminar prueba E2E' for user ID 1...
 -> SUCCESS: Task created with ID 1.
STEP 4: Verifying task appears in the list...
 -> SUCCESS: Task is visible in the UI list.
ALL TESTS PASSED
--- CLEANUP ---
CLEANUP: Deleting task ID 1 via API...
 -> SUCCESS: Task deleted.
 -> VERIFIED: Task no longer exists.
CLEANUP: Deleting user ID 1 via API...
 -> SUCCESS: User deleted.
 -> VERIFIED: User no longer exists
```

### ✅ Backend Integration Test
**Fecha:** 2025-07-05 19:34:45

```
STEP 1: Creating user 'Camilo'...
 -> SUCCESS: User created with ID 1
STEP 2: Creating task 'Prepare presentation' for user ID 1...
 -> SUCCESS: Task created with ID 1
STEP 3: Verifying task registration...
 -> SUCCESS: Task is correctly registered and linked to the user.
ALL TESTS PASSED
--- CLEANUP ---
CLEANUP: Deleting task ID 1...
 -> SUCCESS: Task deleted.
 -> VERIFIED: Task no longer exists (404).
CLEANUP: Deleting user ID 1...
 -> SUCCESS: User deleted.
 -> VERIFIED: User no longer exists (404)
```
