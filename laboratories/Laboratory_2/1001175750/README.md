# Laboratorio 2 - Integración y Pruebas

**Estudiante:** Laura Valentina Pabón Cabezas 

## Resumen de Implementación

Este proyecto implementa las funcionalidades requeridas para el Laboratorio 2, extendiendo el ejemplo de pruebas de integración con las siguientes características:

### ✅ Requerimientos Implementados

1. **Limpieza de datos después de las pruebas** 
2. **Verificación automática de eliminación** 
3. **Funcionalidad tanto en Backend como Frontend** 
4. **Generación automática de reportes PDF** 

---

## Cambios Realizados

### 1. **Users_Service/main.py**
**Archivo:** `laboratories/Laboratory_2/1001175750/Users_Service/main.py`

**Cambios agregados:**
- **Nuevo endpoint DELETE:** `/users/<int:user_id>`
- **Funcionalidad:** Permite eliminar usuarios por ID
- **Respuesta:** Retorna mensaje de confirmación o error 404 si no existe

```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404
```

### 2. **Task_Service/main.py**
**Archivo:** `laboratories/Laboratory_2/1001175750/Task_Service/main.py`

**Cambios agregados:**
- **Nuevo endpoint DELETE:** `/tasks/<int:task_id>`
- **Funcionalidad:** Permite eliminar tareas por ID
- **Respuesta:** Retorna mensaje de confirmación o error 404 si no existe

```python
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404
```

### 3. **Front-End/main.py**
**Archivo:** `laboratories/Laboratory_2/1001175750/Front-End/main.py`

**Cambios agregados:**
- **Nueva sección "Usuarios":** Muestra lista de usuarios con botones de eliminar
- **Botones de eliminar:** Agregados a cada tarea en la lista
- **Funciones JavaScript nuevas:**
  - `eliminarUsuario(userId)`: Elimina usuario por ID
  - `verUsuarios()`: Muestra lista actualizada de usuarios
  - `eliminarTarea(taskId)`: Elimina tarea por ID
  - `verTareas()`: Modificada para incluir botones de eliminar

**Funcionalidades agregadas:**
- Interfaz visual para eliminar usuarios y tareas
- Actualización automática de listas después de eliminación
- Manejo de confirmaciones mediante alerts

### 4. **Test/BackEnd-Test.py**
**Archivo:** `laboratories/Laboratory_2/1001175750/Test/BackEnd-Test.py`

**Cambios agregados:**
- **Funciones de eliminación:**
  - `delete_user(user_id)`: Elimina usuario usando endpoint DELETE
  - `delete_task(task_id)`: Elimina tarea usando endpoint DELETE
- **Funciones de verificación:**
  - `user_exists(user_id)`: Verifica si usuario existe
  - `task_exists(task_id)`: Verifica si tarea existe
- **Limpieza automática:** Al final de la prueba, elimina datos creados y verifica eliminación
- **Generación de reporte PDF:** Captura resultados y tiempo de ejecución, genera PDF automáticamente

**Flujo de prueba:**
1. Crear usuario
2. Crear tarea asociada al usuario
3. Verificar que la tarea está correctamente registrada
4. **ELIMINAR** tarea y usuario creados
5. **VERIFICAR** que ya no existen en el sistema
6. **GENERAR** reporte PDF con resultados

### 5. **Test/FrontEnd-Test.py**
**Archivo:** `laboratories/Laboratory_2/1001175750/Test/FrontEnd-Test.py`

**Cambios agregados:**
- **Nuevas funciones de eliminación:**
  - `eliminar_tarea(driver, wait, task_title)`: Elimina tarea usando interfaz web
  - `eliminar_usuario(driver, wait, user_name)`: Elimina usuario usando interfaz web
- **Manejo de alerts:** Acepta confirmaciones de eliminación automáticamente
- **Verificación visual:** Confirma que elementos eliminados no aparecen en la interfaz
- **Generación de reporte PDF:** Captura resultados y tiempo de ejecución, genera PDF automáticamente

**Flujo de prueba E2E:**
1. Abrir frontend
2. Crear usuario "Ana"
3. Crear tarea "Terminar laboratorio"
4. Verificar que la tarea aparece en la lista
5. **ELIMINAR** tarea usando botón de la interfaz
6. **VERIFICAR** que la tarea ya no aparece
7. **ELIMINAR** usuario usando botón de la interfaz
8. **VERIFICAR** que el usuario ya no aparece
9. **GENERAR** reporte PDF con resultados

### 6. **Test/pdf_generator.py** 
**Archivo:** `laboratories/Laboratory_2/1001175750/Test/pdf_generator.py`

**Funcionalidad agregada:**
- **Clase TestReportGenerator:** Maneja la generación de reportes PDF
- **Numeración secuencial automática:** Cada reporte tiene un número único (test_report_1.pdf, test_report_2.pdf, etc.)
- **Carpeta de reportes:** Crea automáticamente la carpeta `reports/` si no existe
- **Información detallada:** Incluye fecha, tiempo de ejecución y resultados paso a paso
- **Funciones helper:** `generate_backend_test_report()` y `generate_frontend_test_report()`

**Características del PDF:**
- **Encabezado profesional:** Título principal con fondo azul oscuro, nombre de prueba con fondo azul
- **Tabla de resumen:** Métricas organizadas (tiempo de ejecución, total de pasos, pasos exitosos/fallidos)
- **Tabla de resultados detallados:** Cada paso con número, descripción y estado visual
- **Colores automáticos:** Verde para [OK], rojo para [ERROR], azul para [INFO]
- **Estadísticas automáticas:** Cálculo automático de pasos exitosos y fallidos
- **Pie de página:** Información del sistema y datos del estudiante
- **Formato profesional:** Diseño uniforme y fácil de leer
- **Manejo de caracteres especiales:** Conversión automática de emojis a texto ASCII compatible

### 7. **requirements.txt**
**Archivo:** `laboratories/Laboratory_2/1001175750/requirements.txt`

**Dependencias agregadas:**
- `fpdf`: Para generación de reportes PDF
- `selenium`: Para pruebas E2E (ya estaba implícito)

---

## Estructura del Proyecto

```
1001175750/
├── Users_Service/
│   └── main.py              # Servicio de usuarios con endpoint DELETE
├── Task_Service/
│   └── main.py              # Servicio de tareas con endpoint DELETE
├── Front-End/
│   └── main.py              # Interfaz web con funcionalidad de eliminación
├── Test/
│   ├── BackEnd-Test.py      # Pruebas de backend con limpieza y reporte PDF
│   ├── FrontEnd-Test.py     # Pruebas E2E con eliminación y reporte PDF
│   └── pdf_generator.py     # Generador de reportes PDF
├── reports/                 # Carpeta con reportes PDF generados 
└── requirements.txt         # Dependencias del proyecto (actualizado)
```

---

## Cómo Ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar servicios
```bash
# Terminal 1 - Users Service
cd Users_Service
python main.py

# Terminal 2 - Task Service  
cd Task_Service
python main.py

# Terminal 3 - Frontend
cd Front-End
python main.py
```

### 3. Ejecutar pruebas
```bash
# Pruebas de Backend (genera reporte PDF automáticamente)
cd Test
python BackEnd-Test.py

# Pruebas E2E (genera reporte PDF automáticamente)
python FrontEnd-Test.py
```

### 4. Ver reportes generados
```bash
# Los reportes se guardan en la carpeta reports/
ls reports/
# Ejemplo: test_report_1.pdf, test_report_2.pdf, etc.
```

---

## Resultados

✅ **Limpieza de datos implementada correctamente**  
✅ **Verificación automática funcionando**  
✅ **Funcionalidad en Backend y Frontend**  
✅ **Pruebas automatizadas completas**  
✅ **Generación automática de reportes PDF**

Todos los datos creados durante las pruebas son eliminados automáticamente al finalizar, y las pruebas verifican que la eliminación fue exitosa tanto desde el backend como desde la interfaz web. **Además, cada ejecución de prueba genera automáticamente un reporte PDF con numeración secuencial que incluye todos los resultados y métricas de la ejecución.**
