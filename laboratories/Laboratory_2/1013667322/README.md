# Laboratorio 2: Pruebas de Integración

Este laboratorio extiende el ejemplo de pruebas de integración visto en clase, añadiendo dos funcionalidades clave: la limpieza de datos después de las pruebas y la generación automática de reportes en PDF.

## ¿Qué se hizo?

### 1. Limpieza de Datos (Data Cleanup)

Para evitar que la base de datos se llene de datos de prueba, modifiqué los tests para que limpien todo lo que crean.

- **Backend (`Users_Service` y `Task_Service`):**
  - Añadí un endpoint `DELETE` a cada servicio (`/users/<id>` y `/tasks/<id>`) para poder borrar usuarios y tareas.
  - En `Test/BackEnd-Test.py`, usé un bloque `finally` para asegurar que, al terminar la prueba (incluso si falla), se llamen a estos endpoints para borrar el usuario y la tarea creados.
  - Después de borrar, el test verifica que los datos ya no existen (esperando una respuesta `404 Not Found`).

- **Frontend:**
  - El test `Test/FrontEnd-Test.py` también fue modificado para generar reportes.
  - **Nota:** No implementé la limpieza de datos desde el frontend porque la aplicación web de ejemplo no tiene botones o funcionalidad para eliminar usuarios o tareas. Esto se dejó anotado en el código.

### 2. Generación de Reportes en PDF

Creé un módulo nuevo, `Test/pdf_report_generator.py`, para manejar la creación de los reportes.

- La clase `PDFReportGenerator` crea un PDF con los resultados de la prueba.
- Para no perder los resultados anteriores, cada reporte se guarda con un número secuencial (ej: `report_1.pdf`, `report_2.pdf`, etc.) en la carpeta `Test/reports/`.
- Ambos tests, el del backend y el del frontend, usan esta clase para generar su reporte al finalizar.

## Archivos Modificados

- **`Users_Service/main.py`**: Añadido el endpoint `DELETE /users/<user_id>`.
- **`Task_Service/main.py`**: Añadido el endpoint `DELETE /tasks/<task_id>`.
- **`Test/BackEnd-Test.py`**: Añadida la lógica de limpieza y la llamada al generador de reportes.
- **`Test/FrontEnd-Test.py`**: Añadida la llamada al generador de reportes, la lógica para interactuar con los nuevos botones de eliminar y la verificación de que los datos fueron borrados.
- **`Test/pdf_report_generator.py`**: (Archivo nuevo) Contiene la lógica para crear los PDF.
- **`README.md`**: Este mismo archivo, para explicar el trabajo hecho.
- **`Front-End/main.py`**: Modificado para añadir las secciones de eliminación de tareas y usuarios en la interfaz web.

## Para ejecutar las pruebas

Asegúrate de tener las dependencias instaladas:

```
pip install requests selenium fpdf
```

Luego, puedes correr los tests:

```bash
# Test del Backend
python Test/BackEnd-Test.py

# Test del Frontend
python Test/FrontEnd-Test.py
```

Los reportes aparecerán en la carpeta `Test/reports/`.
