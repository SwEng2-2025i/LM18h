# Laboratory 2 – Integration Test, Data Cleanup & Report

Este laboratorio extiende el ejemplo anterior de pruebas de integración añadiendo dos mejoras importantes:

## ✅ Objetivos cumplidos

1. **Limpieza de datos:**  
   Todos los datos creados por los tests (usuarios y tareas) son eliminados después de cada ejecución.  
   Se verifica además que hayan sido eliminados correctamente mediante peticiones `GET`.

2. **Generación automática de reportes en PDF:**  
   Cada test genera un reporte en la carpeta `Test/reports/`, indicando el resultado detallado de cada paso.

## 🛠 Secciones agregadas o modificadas

### `Test/BackEnd-Test.py`

- Registro del estado inicial (`baseline_users`, `baseline_tasks`) y verificación al final.
- Funciones `delete_user()` y `delete_task()` añadidas.
- Generación de reporte PDF con `generate_pdf_report()` (requiere `report_utils.py`).
- Cada paso relevante del test agrega resultados a la lista `results`.

### `Test/FrontEnd-Test.py`

- Añadido soporte para `delete_user()` y `delete_task()` usando `requests`.
- Función `ver_tareas()` ahora retorna el texto, permitiendo validación directa.
- Se agregó una estructura `results` para registrar el éxito/falla de cada paso.
- Se captura la excepción final para incluirla en el reporte PDF.
- Se genera un archivo PDF automático del resultado (`generate_pdf_report()`).

### `Test/report_utils.py` (nuevo archivo)

- Función `generate_pdf_report(test_name, results)` que crea un reporte PDF con timestamp y resultado de cada paso.
- Guarda los reportes en `Test/reports/`.

| Archivo | Cambios clave |
|---------|---------------|
| **Users_Service/main.py** | Endpoint `DELETE /users/&lt;id>` |
| **Task_Service/main.py**  | Endpoints `GET` y `DELETE /tasks/&lt;id>` |
| **Test/report_utils.py** *(nuevo)* | `generate_pdf_report()` – crea PDF con `[OK]/[FAIL]` |
| **Test/BackEnd-Test.py**  | Baseline de datos, limpieza selectiva, llamadas a `generate_pdf_report()` |
| **Test/FrontEnd-Test.py** | Igual que el back-end + extracción de IDs en Selenium y validación en la UI |


## 🧪 Cómo ejecutar las pruebas

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Levantar los microservicios (cada uno en su terminal)**
   ```bash
   # Ventana 1 – Users_Service
    cd Users_Service
    python main.py           # corre en http://localhost:5001

    # Ventana 2 – Task_Service
    cd Task_Service
    python main.py           # corre en http://localhost:5002

    # Ventana 3 – Front-End
    cd Front-End
    python main.py           # corre en http://localhost:5000
   ```
3. **Ejecutar los tests (en una cuarta ventana, desde la raíz del laboratorio)**
   ```bash
   python Test/BackEnd-Test.py
   python Test/FrontEnd-Test.py
   ```

4. **Ver los reportes**
    ```bash
    Test/reports/report_001.pdf
    Test/reports/report_002.pdf
    ...
    ```
## Autor
**Gabriel Castiblanco - ID 1001219707**