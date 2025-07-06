# 🧪 Test de integración

**Autor:** Sergio Esteban Rendón Umbarila

## Descripción general
Este proyecto implementa una arquitectura de microservicios con capacidades de prueba integrales, incluyendo limpieza de datos y generación automática de informes en PDF.

## Estructura del proyecto
```
IntegrationTest/
├── scripts/
│   ├── Front-End/
│   │   └── main.py              # Aplicación frontend en Flask
│   ├── Users_Service/
│   │   └── main.py              # Microservicio de gestión de usuarios
│   ├── Task_Service/
│   │   └── main.py              # Microservicio de gestión de tareas
│   └── Test/
│       ├── BackEnd-Test.py      # Pruebas de integración del backend
│       └── FrontEnd-Test.py     # Pruebas E2E del frontend
│   ├── requirements.txt         # Archivo requirements.txt para instalar las librerias necesarias
├── reports/                     # Informes PDF generados (se crean automáticamente)
└── README.md                    # Este archivo
```

## Nuevas funcionalidades implementadas

### 1. Funcionalidad de limpieza de datos

#### Prueba de Backend (`BackEnd-Test.py`)
**Secciones añadidas:**
- Clase `BackEndTestRunner` con gestión completa de pruebas
- Listas `created_users` y `created_tasks` para rastrear datos de prueba
- Método `cleanup_test_data()` para eliminar los datos generados por las pruebas
- Método `verify_cleanup()` para asegurar que los datos fueron eliminados correctamente
- Manejo de errores y registros mejorados en todo el flujo de pruebas

**Cambios clave:**
- Todas las operaciones de prueba están estructuradas dentro de una clase
- Seguimiento de todas las entidades creadas (usuarios y tareas)
- Verificación de limpieza mediante la comprobación de endpoints de API
- Registro detallado para cada paso de prueba

#### Prueba de Frontend (`FrontEnd-Test.py`)
**Secciones añadidas:**
- Clase `FrontEndTestRunner` para gestionar el ciclo de vida de las pruebas E2E
- Rastreo de datos similar al de las pruebas de backend
- Método `cleanup_test_data()` usando llamadas a API
- Método `verify_cleanup()` para confirmar la eliminación exitosa de datos
- Gestión mejorada de WebDriver con configuración y cierre adecuados

**Cambios clave:**
- Código de prueba procedural convertido a una arquitectura basada en clases
- Integración de API para verificación de limpieza
- Manejo robusto de errores en operaciones con Selenium
- Seguimiento de datos creados por la interfaz para su posterior limpieza

#### Servicio de usuarios (`Users_Service/main.py`)
**Secciones añadidas:**
- Método `delete_user()` para borrar usuarios
- Endpoint @service_a.route('/users/<int:user_id>', methods=['DELETE']) para eliminar usuarios

**Cambios clave:**
- Función de borrar usuarios con endpoint DELETE para hacerla efectiva

#### Servicio de usuarios (`Tasks_Service/main.py`)
**Secciones añadidas:**
- Método `delete_task()` para borrar usuarios
- Endpoint @service_b.route('/tasks/<int:task_id>', methods=['DELETE']) para eliminar tareas

**Cambios clave:**
- Función de borrar tareas con endpoint DELETE para hacerla efectiva

### 2. Generación automática de informes PDF

#### Características del informe:
- **Numeración secuencial:** Los informes se numeran secuencialmente (001, 002, 003, etc.)
- **Sin sobrescritura:** Los informes anteriores se conservan automáticamente
- **Contenido completo:** Cada informe incluye:
  - Metadatos de ejecución de pruebas (fecha, hora, número de informe)
  - Resumen de pruebas (total, aprobadas, fallidas)
  - Resultados detallados con marcas de tiempo
  - Resultados de verificación de limpieza de datos
  - Información de seguimiento de datos de prueba

#### Detalles de implementación:
- Método `generate_pdf_report()` en ambas clases de prueba
- Uso de la biblioteca `reportlab` para generación de PDF
- Informes almacenados en el directorio `reports/` (creado automáticamente)
- Formato de nombres: `backend_test_report_XXX.pdf` / `frontend_test_report_XXX.pdf`

### 3. Arquitectura de pruebas mejorada

#### Nuevas clases y métodos:
**BackEndTestRunner:**
- `log_result()` - Registro centralizado de resultados
- `create_user()` / `create_task()` - Creación con seguimiento
- `cleanup_test_data()` - Implementación de limpieza de datos
- `verify_cleanup()` - Verificación de limpieza
- `generate_pdf_report()` - Generación de informe PDF
- `run_full_test()` - Orquestación de toda la suite de pruebas

**FrontEndTestRunner:**
- Estructura similar a `BackEndTestRunner`
- `setup_driver()` - Inicialización de WebDriver
- `abrir_frontend()` / `crear_usuario()` / `crear_tarea()` - Interacciones mejoradas con la UI
- Llamadas a API integradas para verificación de limpieza

## Requisitos de instalación

### Dependencias de Python
```bash
pip install flask flask-sqlalchemy flask-cors requests selenium reportlab
```

### Requisitos adicionales
- Chrome WebDriver (para las pruebas con Selenium)
- Navegador Chrome instalado

## Instrucciones de uso

### 1. Iniciar los servicios
Ejecutar en terminales separadas:
```bash
# Terminal 1 - Servicio de Usuarios
python scripts/Users_Service/main.py

# Terminal 2 - Servicio de Tareas  
python scripts/Task_Service/main.py

# Terminal 3 - Frontend
python scripts/Front-End/main.py
```

### 2. Ejecutar las pruebas
```bash
# Pruebas de integración del backend
python scripts/Test/BackEnd-Test.py

# Pruebas E2E del frontend
python scripts/Test/FrontEnd-Test.py
```

### 3. Ver informes
- Los informes PDF se generan automáticamente en el directorio `reports/`
- Cada ejecución de prueba crea un nuevo informe numerado
- Los informes incluyen resultados completos y verificación de limpieza

## Resumen de resultados de pruebas

### Implementación de limpieza de datos
✅ **Pruebas de Backend:** Rastrean y eliminan todos los usuarios y tareas creados  
✅ **Pruebas de Frontend:** Rastrean los datos creados por UI y verifican limpieza vía API  
✅ **Verificación:** Ambas suites de prueba confirman la eliminación exitosa de datos  

### Generación de informes PDF
✅ **Numeración secuencial:** Los informes se numeran automáticamente (001, 002, ...)  
✅ **Sin sobrescritura:** Se preservan todos los informes anteriores  
✅ **Contenido completo:** Resultados detallados, tiempos y estado de limpieza  
✅ **Generación automática:** Los informes se crean después de cada ejecución de prueba  

### Arquitectura mejorada
✅ **Estructura basada en clases:** Mejor organización y mantenibilidad  
✅ **Registro detallado:** Seguimiento de cada paso de prueba  
✅ **Manejo de errores:** Gestión robusta de errores durante todas las pruebas  
✅ **Integración con API:** Las pruebas de frontend usan API para verificación de limpieza  

## Notas

- **Implementación real:** En producción, se implementaron endpoints DELETE en `Users_Service` y `Task_Service`
- **Almacenamiento de informes:** Todos los informes PDF se conservan y se encuentran en el directorio `reports/`
- **Modo del navegador:** Las pruebas de frontend se ejecutan en modo visible por defecto (descomentar la opción headless si se desea ocultar)

