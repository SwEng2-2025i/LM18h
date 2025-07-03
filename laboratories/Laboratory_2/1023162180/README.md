# Extensión de Pruebas de Integración

## Funcionalidades Agregadas

- **Limpieza de Datos (Data Cleanup):**  
  Ahora, tanto la prueba de backend como la de frontend eliminan todos los usuarios y tareas que crean durante la ejecución. Después de la eliminación, verifican que los datos realmente hayan sido borrados del sistema. Esto asegura que los datos de prueba no contaminen el entorno ni afecten futuras ejecuciones.

- **Generación Automática de Reportes PDF:**  
  Al finalizar cada ejecución de prueba, se genera automáticamente un reporte en PDF en la carpeta `Test/reports/`. Cada reporte tiene un número secuencial y nunca se sobrescriben los anteriores. El reporte incluye los resultados de la prueba y el estado de la limpieza de datos.

## Cambios Realizados en el Código

- **BackEnd-Test.py:**  
  - Se agregaron las funciones `delete_user` y `delete_task` para eliminar usuarios y tareas creados por la prueba.
  - Se implementó la verificación de que los datos hayan sido eliminados correctamente tras la limpieza.
  - Se añadió la función `generate_pdf_report`, que genera un reporte PDF con los resultados de la prueba y la limpieza.
  - Se creó la función `sanitize_line` para reemplazar caracteres Unicode (como emojis) por texto ASCII antes de escribir en el PDF, evitando errores de codificación.
  - Se modificó la lógica para que los IDs de usuario y tarea creados sean almacenados y eliminados específicamente al final de la prueba.

- **FrontEnd-Test.py:**  
  - Se implementó la creación y eliminación de usuario y tarea desde la interfaz web usando Selenium.
  - Se verifica que los elementos creados por la prueba desaparecen de la interfaz tras la eliminación.
  - Se agregó la generación de reportes PDF secuenciales para los resultados de la prueba de frontend, usando la misma lógica de sanitización de caracteres.

- **Users_Service/main.py:**  
  - Se añadió el endpoint `DELETE /users/<id>` para permitir la eliminación de usuarios desde las pruebas.

- **Task_Service/main.py:**  
  - Se añadió el endpoint `DELETE /tasks/<id>` para permitir la eliminación de tareas desde las pruebas.

- **requirements.txt:**  
  - Se agregó la dependencia `fpdf` para la generación de PDFs y `selenium` para las pruebas de frontend.

## Instrucciones Detalladas de Ejecución

1. **Instalar dependencias del proyecto:**

   Abrir una terminal en la carpeta raíz del proyecto y ejecuta:
   ```
   pip install -r requirements.txt
   ```

2. **Iniciar los servicios Flask:**

   Se deben abrir **tres terminales independientes** (una para cada servicio) y ejecutar los siguientes comandos en cada una:

   - **Servicio de Usuarios:**
     ```
     cd Users_Service
     python main.py
     ```

   - **Servicio de Tareas:**
     ```
     cd Task_Service
     python main.py
     ```

   - **Front-End:**
     ```
     cd Front-End
     python main.py
     ```

   Debe asegurarse de que cada servicio esté corriendo en su propia terminal y que no haya errores de inicio.

3. **Ejecutar la prueba de integración de backend:**

   Abrir una nueva terminal, navegar a la carpeta raíz y ejecutar:
   ```
   python Test/BackEnd-Test.py
   ```

   El resultado de la prueba y la limpieza de datos se guardará en un archivo PDF dentro de la carpeta `Test/reports/` con un número secuencial.

4. **Ejecutar la prueba de integración de frontend (opcional):**

   En la misma o en una nueva terminal, ejecutar:
   ```
   python Test/FrontEnd-Test.py
   ```

   También se generará un PDF con los resultados en la misma carpeta de reportes.

5. **Verificar los reportes:**

   Los reportes PDF generados se encuentran en:
   ```
   Test/reports/
   ```
   Cada archivo tiene un nombre secuencial y contiene el detalle de los pasos ejecutados, los resultados y el estado de la limpieza de datos.

## Notas

- Las pruebas solo eliminan los datos que ellas mismas crean, no afectan datos previos del sistema.
- Los reportes PDF nunca se sobrescriben; cada ejecución genera un archivo nuevo con un número incremental.

---