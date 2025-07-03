
## Informe de Resultados

El script de prueba de integración (`BackEnd-Test.py`) fue ampliado para incluir:

- **Limpieza de datos:**
  - Todos los datos (usuario y tarea) creados por la prueba se eliminan al finalizar.
  - El script verifica que los datos hayan sido eliminados correctamente.
- **Generación automática de reporte PDF:**
  - Después de cada ejecución, se genera un reporte PDF en la carpeta `reports`.
  - Cada reporte tiene un número secuencial y los anteriores se conservan.

## Secciones de código agregadas/modificadas

- **Generación de reporte PDF:**
  - Se agregaron los imports `from reportlab.lib.pagesizes import letter` y `from reportlab.pdfgen import canvas`.
  - Se agregó la configuración de `REPORTS_DIR` y la función `generate_pdf_report`.
  - El reporte PDF se genera en el bloque `finally` de `integration_test()`.
- **Limpieza y verificación de datos:**
  - Se agregaron las funciones `delete_user`, `delete_task`, `get_users` y se mejoró `get_tasks`.
  - El bloque `finally` ahora elimina el usuario y tarea creados y verifica su eliminación.



## Cómo ejecutar

### 1. Crear y activar un entorno virtual 

Abre PowerShell en la carpeta `Example 5 - Integration Test` y ejecuta:
```powershell
python -m venv venv
./venv/Scripts/Activate
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 3. Iniciar los servicios necesarios

Abre tres terminales y ejecuta en cada una:

- **Servicio de usuarios:**
  ```powershell
  cd "Users_Service"
  python main.py
  ```
- **Servicio de tareas:**
  ```powershell
  cd "Task_Service"
  python main.py
  ```
- **Front-End:**
  ```powershell
  cd "Front-End"
  python main.py
  ```

### 4. Ejecutar las pruebas de integración

En una terminal nueva (con el entorno virtual activado):
```powershell
cd Test
python BackEnd-Test.py
python FrontEnd-Test.py
```

