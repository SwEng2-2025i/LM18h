## 🧪 Taller de Pruebas Automatizadas: Backend y Frontend con Logs y Reportes en PDF
GABRIEL FELIPE FONSECA GUERRERO
Este proyecto implementa pruebas de integración y extremo-a-extremo (E2E) para una aplicación distribuida con microservicios. Se han incorporado funcionalidades adicionales de auditoría mediante logs y generación de reportes PDF.

---

### ✅ Métodos Agregados

Se incluyeron dos métodos importantes para pruebas completas:

- `delete_user(user_id)`  
  Permite eliminar un usuario específico del sistema y deja registro detallado en los logs.

- `delete_task(task_id)`  
  Permite eliminar una tarea específica. Esto permite mantener limpia la base de datos luego de pruebas.

Estos métodos son utilizados tanto en el backend (`BackEnd-Test.py`) como en el frontend (`FrontEnd-Test.py`) para mantener la integridad del entorno después de ejecutar los casos de prueba.

---

### 📄 Módulo `LogSaver.py`

Este módulo contiene dos clases principales:

- `Logger`:  
  Un logger personalizado que escribe mensajes estructurados (tipo, mensaje, URL de la petición, método, etc.) en el archivo `Logs/app.log`.

- `DuplicadorSalida`:  
  Una clase que permite duplicar la salida estándar (`stdout`) para capturar simultáneamente lo que se imprime en consola y almacenarlo en una variable. Esto es útil para generar reportes PDF con toda la salida relevante.

---

### 📁 Generación de Reportes PDF

Tanto el backend como el frontend generan automáticamente un PDF con el resultado de las pruebas. Esto se hace con las siguientes funciones:

- `capturar_y_guardar_pdf()`:  
  Ejecuta el flujo de prueba, captura la salida de consola y los logs, y los guarda en un PDF estructurado.

- `guardar_en_pdf(texto, nombre_pdf)`:  
  Usa `reportlab` para crear un PDF legible con saltos de línea, sangrías, y salto de página si es necesario.

- `obtener_siguiente_numero()`:  
  Genera un nombre único e incremental para cada reporte generado (por ejemplo: `reporteBackEnd_1.pdf`, `reporteFrontEnd_2.pdf`), almacenándolos en la carpeta `reportes/`.

---

### 🧰 Dependencias (instalar con `pip install`)

```bash
pip install flask requests reportlab selenium 
```

Además, asegúrate de tener el `ChromeDriver` configurado si usarás Selenium.

