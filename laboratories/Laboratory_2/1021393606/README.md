# 🧪 Laboratorio 2 — Testing de Integración

## 📁 Estructura del Proyecto

```bash
Laboratory_2/
├── <TU_ID>/
│   ├── Task_service/
│   │   └── main.py
│   ├── User_service/
│   │   └── main.py
│   ├── Front-end/
│   │   └── main.py
│   ├── Test/
│   │   ├── BackEnd-Test.py
│   │   ├── FrontEnd-Test.py
│   │   └── generate_pdf_report.py
│   ├── pdf_reports/
│   │   ├── report_001.pdf
│   │   ├── ...
│   ├── requirements.txt
│   └── README.md
```

## ✅ Funcionalidades implementadas

1. Creación automática de usuarios y tareas.
2. Validación de relaciones entre entidades.
3. Limpieza automática de datos generados por las pruebas.
4. Verificación de la eliminación de datos.
5. Generación automática de reportes PDF con resultados paso a paso.

## 🧪 Pruebas Implementadas

### 🔹 BackEnd-Test.py

Prueba vía API los servicios de usuarios y tareas:

- Crea un usuario mediante POST `/users`.
- Crea una tarea asignada mediante POST `/tasks`.
- Verifica con GET `/tasks` que la tarea esté asociada al usuario.
- Elimina con DELETE los datos creados.
- Verifica que hayan sido correctamente eliminados.
- Genera un PDF con los resultados.

**Resultado esperado:** reporte indicando todos los pasos en estado `PASS` o `SUCCESS`.

### 🔹 FrontEnd-Test.py

Automatiza con Selenium la interacción con la UI:

- Abre la aplicación Flask.
- Crea un usuario usando la UI.
- Crea una tarea desde la UI para ese usuario.
- Verifica visualmente que la tarea aparece en la lista.
- Genera automáticamente un PDF con los resultados.

**Resultado esperado:** se abre el navegador, se ve el flujo completo y se genera un reporte con todos los pasos `PASS`.

## 📄 Generación de Reportes PDF

Todos los resultados se guardan automáticamente como archivos `.pdf` en la carpeta:

```bash
pdf_reports/
├── report_001.pdf
├── report_002.pdf
└── ...
```

Cada archivo contiene:

- Tipo y número de reporte.
- Fecha y hora de ejecución.
- Pasos ejecutados y su estado (PASS/FAIL).
- Datos creados.
- Resultados de limpieza (cuando aplica).

## 🔧 Archivos modificados

### 📝 BackEnd-Test.py

- Agregado flujo completo de pruebas vía API.
- Agregadas funciones `delete_user` y `delete_task`.
- Se agregó importación de `save_pdf_report(...)`.

### 📝 FrontEnd-Test.py

- Creado completamente desde cero.
- Usa Selenium con `WebDriverWait` y validación robusta.
- Agrega cada paso con validación de errores.
- Genera PDF con resultados claros.

### 📝 generate_pdf_report.py

- Utiliza `reportlab` para crear un PDF estructurado.
- Recibe un diccionario `report_data` que documenta:
  - Pasos del test.
  - Usuarios/tareas creados.
  - Resultados de limpieza.

### 📝 Task_service/main.py y User_service/main.py

- Agregados endpoints `DELETE` para eliminar usuarios y tareas.
- Agregado manejo de errores con `try-except`.
- Validaciones de existencia de usuario/tarea.

## ⚙️ Instalación y ejecución paso a paso

### 1. Instala dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecuta los servicios en tres terminales

```bash
# Terminal 1
cd User_service
python main.py

# Terminal 2
cd Task_service
python main.py

# Terminal 3
cd Front-end
python main.py
```

### 3. Ejecuta las pruebas

```bash
# Test BackEnd
cd Test
python BackEnd-Test.py

# Test FrontEnd
python FrontEnd-Test.py
```

## 📌 Consideraciones

- Cada ejecución genera un nuevo PDF (no se sobrescriben).
- El sistema usa SQLite (archivos locales `users.db` y `tasks.db`).
- Se puede ejecutar localmente sin necesidad de conexión externa.
- La limpieza de datos se hace solo en `BackEnd-Test.py` por API.

## 📅 Fecha límite de entrega

**Sábado 5 de julio**

## 🧾 Autor

Carlos Julián Reyes Piraligua
Universidad Nacional de Colombia  
C.C.: 1021393606
