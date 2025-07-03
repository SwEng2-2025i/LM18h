# LAB 2: Limpieza Automática de Datos de Prueba y Generación de Reportes PDF

Este documento explica cómo funciona la limpieza automática de datos después de ejecutar los tests y la nueva funcionalidad de generación de reportes PDF.

## 🎉 RESUMEN

Se han implementado todas las funcionalidades solicitadas:

1. ✅ **Limpieza Selectiva de Datos**: Los tests solo borran los datos que ellos mismos crean
2. ✅ **Generación Automática de PDFs**: Reportes numerados secuencialmente sin sobreescritura
3. ✅ **Interfaz de Administración Web**: Botones para limpieza manual desde el frontend

**Archivos Modificados:** 4 | **Archivos Nuevos:** 1 | **Directorios Nuevos:** 1 | **Endpoints Agregados:** 4

---

## ¿Qué se agregó?

### 1. Endpoints de Limpieza en los Servicios

Se agregaron nuevos endpoints en ambos servicios para permitir la eliminación de todos los datos:

- **Users Service**: `DELETE /users/clear` - Elimina todos los usuarios
- **Users Service**: `DELETE /users/{id}` - Elimina un usuario específico
- **Tasks Service**: `DELETE /tasks/clear` - Elimina todas las tareas  
- **Tasks Service**: `DELETE /tasks/{id}` - Elimina una tarea específica

### 2. Limpieza Automática en Tests

Ambos tests ahora incluyen limpieza selectiva automática:

#### BackEnd-Test.py

- Rastrea los IDs de datos que crea durante el test
- Limpia solo los datos que él mismo creó
- Genera reporte PDF automáticamente al finalizar

#### FrontEnd-Test.py

- Rastrea los IDs de datos que crea durante el test  
- Limpia solo los datos que él mismo creó
- Genera reporte PDF automáticamente al finalizar

#### Interfaz de Administración Web

- Se agregó una sección administrativa con botones para limpieza manual
- Botones claramente marcados como peligrosos
- Confirmaciones de seguridad para evitar borrados accidentales

### 3. Sistema de Reportes PDF

Se agregó un sistema completo de generación de reportes en PDF:

#### Características:

- **Numeración secuencial**: Los PDFs se numeran automáticamente (001, 002, 003...)
- **No sobreescritura**: Cada reporte se conserva permanentemente
- **Información detallada**: Incluye resultados, tiempos, errores y estadísticas
- **Formato profesional**: PDFs bien formateados con tablas y colores

#### Archivos del sistema:

- `pdf_generator.py` - Módulo principal para generar PDFs
- `Reports/` - Directorio donde se almacenan todos los PDFs

## Cómo Usar

### Ejecutar Tests Individuales (con PDF automático)

```bash
# Test del backend (genera PDF automáticamente)
python Test/BackEnd-Test.py

# Test del frontend (genera PDF automáticamente)  
python Test/FrontEnd-Test.py
```

### Usar la Interfaz Web

En la interfaz web, navega a la sección "Administración - Zona Peligrosa":

- **Borrar Todas las Tareas**: Elimina todas las tareas del sistema
- **Borrar Todos los Usuarios**: Elimina todos los usuarios del sistema
- **Borrar Todo**: Elimina todos los datos (tareas y usuarios) con confirmación doble

## Estructura de Reportes PDF

Los reportes PDF incluyen:

- **Información general**: Fecha, número de reporte, estadísticas
- **Detalle por test**: Estado, duración, salida, errores
- **Resumen final**: Tasa de éxito, estadísticas globales

### Ubicación de PDFs

Todos los reportes se guardan en: `Test/Reports/`

Formato de nombres: `test_report_001.pdf`, `test_report_002.pdf`, etc.

## Orden de Limpieza

**Importante**: Las tareas se eliminan antes que los usuarios debido a la dependencia de clave foránea.

1. 🗑️ Eliminar tareas específicas (`DELETE /tasks/{id}`)
2. 🗑️ Eliminar usuarios específicos (`DELETE /users/{id}`)

## Requisitos

- Los servicios deben estar ejecutándose:
  - Users Service en puerto 5001
  - Tasks Service en puerto 5002  
  - Frontend en puerto 5000 (para tests de frontend)
- Bibliotecas requeridas: `flask`, `flask_sqlalchemy`, `requests`, `reportlab`, `selenium`

```bash
pip install flask flask_sqlalchemy requests reportlab selenium
```

## Mensajes de Estado

- ✅ = Operación exitosa
- ⚠️ = Advertencia o error parcial
- ❌ = Error crítico
- 🧹 = Limpieza en progreso
- 🗑️ = Eliminando datos
- 🎉 = Completado exitosamente

---

### 🔧 Modificaciones Realizadas por Archivo

#### **Servicios Backend**

##### `Users_Service/main.py`

```python
# ✅ AGREGADO: Endpoint para eliminar usuario específico
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Elimina un usuario por ID sin afectar otros datos

# ✅ AGREGADO: Endpoint para limpiar todos los usuarios  
@service_a.route('/users/clear', methods=['DELETE'])
def clear_users():
    # Elimina todos los usuarios (solo para testing)
```

##### `Task_Service/main.py`

```python
# ✅ AGREGADO: Endpoint para eliminar tarea específica
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Elimina una tarea por ID sin afectar otras datos

# ✅ AGREGADO: Endpoint para limpiar todas las tareas
@service_b.route('/tasks/clear', methods=['DELETE'])
def clear_tasks():
    # Elimina todas las tareas (solo para testing)
```

#### **Frontend Web Interface**

##### `Front-End/main.py`

```python
# ✅ AGREGADO: Sección administrativa con botones de limpieza
<div class="admin-section">
    <h3>⚠️ Administración - Zona Peligrosa</h3>
    <button class="danger-button" onclick='borrarTodasLasTareas()'>
    <button class="danger-button" onclick='borrarTodosLosUsuarios()'>
    <button class="danger-button" onclick='borrarTodo()'>
</div>

# ✅ AGREGADO: Funciones JavaScript para limpieza
function borrarTodasLasTareas()    // Elimina todas las tareas
function borrarTodosLosUsuarios()  // Elimina todos los usuarios  
function borrarTodo()              // Elimina todo con confirmación doble
```

#### **Sistema de Tests**

##### `Test/BackEnd-Test.py`

```python
# ✅ AGREGADO: Sistema de rastreo de IDs
created_user_ids = []     # Rastrea usuarios creados
created_task_ids = []     # Rastrea tareas creadas

# ✅ MODIFICADO: Limpieza selectiva en lugar de total
def clear_test_data():
    # Solo elimina datos creados por este test

# ✅ AGREGADO: Captura de resultados para PDF
test_results = []         # Almacena resultados del test
test_output = []          # Captura salida del test

# ✅ AGREGADO: Generación automática de PDF
from pdf_generator import create_test_result, generate_test_report
```

##### `Test/FrontEnd-Test.py`

```python
# ✅ AGREGADO: Sistema de rastreo de IDs
created_user_ids = []     # Rastrea usuarios creados
created_task_ids = []     # Rastrea tareas creadas

# ✅ MODIFICADO: Funciones que rastrean IDs creados
def crear_usuario():      # Ahora rastrea user_id creado
def crear_tarea():        # Ahora rastrea task_id creado

# ✅ AGREGADO: Generación automática de PDF
test_results = []         # Almacena resultados del test
test_output = []          # Captura salida del test
```

#### **Sistema de Reportes PDF**

##### `Test/pdf_generator.py` - ✅ ARCHIVO NUEVO

```python
class TestReportGenerator:
    # Genera PDFs numerados secuencialmente
    # Formato profesional con tablas y colores
    # No sobreescribe reportes anteriores
    
def create_test_result():     # Crea estructura de resultado
def generate_test_report():   # Función de conveniencia
```

#### **Directorio de Reportes**

##### `Test/Reports/` - ✅ DIRECTORIO NUEVO

- Almacena todos los PDFs generados
- Numeración secuencial: `test_report_001.pdf`, `test_report_002.pdf`, etc.
- Conserva historial completo de tests
