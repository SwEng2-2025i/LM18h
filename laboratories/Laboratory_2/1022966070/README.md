# 🧪 Laboratorio 2 - Pruebas de Integración de Sistemas

## 📋 Descripción

Este laboratorio expande el proyecto base de integración visto en clase, incorporando las siguientes características clave:

### ✅ Limpieza automática de datos

Después de ejecutar los tests, se eliminan automáticamente todos los datos creados durante la prueba (usuarios y tareas), asegurando que el sistema quede en un estado limpio.  
Además, se verifica que estos datos ya no existan en el sistema.

### ✅ Generación de reportes en PDF

Cada ejecución de prueba genera un archivo PDF con los resultados.  
Los reportes se almacenan en la carpeta `reports/` y no se sobrescriben:  
Se guardan con formato de fecha y hora (`frontend_test_report_YYYY-MM-DD_HH-MM-SS.pdf`).

---

## 🧪 Resultados de Prueba

Las pruebas ejecutadas cubren:

- ✔️ Creación de un nuevo usuario
- ✔️ Creación de una tarea asociada a ese usuario
- ✔️ Verificación de la relación tarea-usuario
- ✔️ Eliminación de la tarea y del usuario
- ✔️ Confirmación de que los datos fueron removidos correctamente

📄 **Ejemplo de contenido del reporte PDF generado**:

Frontend Test Report

- ✅ Frontend opened successfully
- ✅ User created with ID: 23
- ✅ Task created with ID: 47
- ✅ Tasks verified successfully
- ✅ Data cleanup completed successfully
- ✅ Test passed



---

## 🔧 Modificaciones y Funcionalidades Agregadas

### `Test/FrontEnd-Test.py`

- Se agregó lógica para eliminar usuario y tarea creados durante el test.
- Se implementó control de errores y verificación post-eliminación.
- Se integró con `PDFReport` para generar automáticamente el reporte.

### `Test/report_generator.py`

- Nuevo módulo que encapsula la lógica de creación de reportes PDF.
- Incluye numeración secuencial basada en fecha/hora.
- Usa la biblioteca `fpdf`.

### `Backend/app.py`

- Se agregaron los endpoints:
  - `DELETE /users/<id>`
  - `DELETE /tasks/<id>`

Para permitir que los tests eliminen los datos creados.

### `Frontend/frontend.py`

- Interfaz web desarrollada con Flask.
- Adaptada para funcionar con los servicios de usuarios y tareas.
- Soporta la creación y consulta de tareas/usuarios desde la UI.



▶️ Cómo Ejecutar
Requisitos:
Python 3.10 o superior

Google Chrome instalado

ChromeDriver compatible

Dependencias de Python:

pip install flask selenium fpdf requests


# Backend (usuarios y tareas)
cd Task_Service
python main.py

# Frontend (interfaz web)
cd ../Front-End
python main.py


# Desde Test/
cd ../Test

# Prueba Backend (opcional)
python BackEnd-Test.py

# Prueba Frontend
python FrontEnd-Test.py


✅ Estado
✔️ Requerimientos cumplidos en su totalidad
✔️ Limpieza automatizada de datos implementada
✔️ Reportes PDF generados sin sobrescribir archivos previos
✔️ Repositorio organizado por carpeta de estudiante (1022966070/)
✔️ Instrucciones claras incluidas en este README
