# Proyecto de Pruebas de Integración - Sistema de Gestión de Usuarios y Tareas

## Descripción del Proyecto

Este proyecto implementa un sistema distribuido con microservicios para la gestión de usuarios y tareas, junto con un conjunto completo de pruebas de integración automatizadas que incluyen tanto pruebas de backend como pruebas end-to-end (E2E).

## Arquitectura del Sistema

### Servicios Backend
- **Users_Service** (Puerto 5001): Gestión de usuarios
- **Task_Service** (Puerto 5002): Gestión de tareas
- **Front-End** (Puerto 5000): Interfaz web para interactuar con los servicios

### Componentes de Pruebas
- **BackEnd-Test.py**: Pruebas de integración para APIs
- **FrontEnd-Test.py**: Pruebas end-to-end con Selenium

## Funcionalidades Implementadas

### APIs de Usuario (Users_Service)
- ✅ `POST /users` - Crear usuario
- ✅ `GET /users/<id>` - Obtener usuario por ID
- ✅ `GET /users` - Listar todos los usuarios
- ✅ `DELETE /users/<id>` - Eliminar usuario *(AGREGADO)*

### APIs de Tareas (Task_Service)
- ✅ `POST /tasks` - Crear tarea
- ✅ `GET /tasks` - Obtener todas las tareas
- ✅ `DELETE /tasks/<id>` - Eliminar tarea *(AGREGADO)*

### Frontend Web
- ✅ Formulario de creación de usuarios
- ✅ Formulario de creación de tareas
- ✅ Visualización de lista de tareas
- ✅ Validación de campos

## Cambios y Mejoras Implementadas

### Modificaciones en los Servicios Backend
- Implementación de rutas DELETE para usuarios y tareas
- Validación de existencia de recursos antes de eliminación
- Respuestas JSON consistentes con códigos de estado apropiados

### Sistema de Pruebas Automatizadas
- **Pruebas Backend**: Implementación completa de pruebas CRUD con verificaciones
- **Pruebas E2E**: Automatización del flujo completo usuario-tarea con Selenium
- **Limpieza automática**: Eliminación de datos de prueba después de cada ejecución
- **Generación de reportes**: Creación automática de documentos PDF con resultados

### Detalles de los Tests Implementados

Los tests están diseñados para garantizar la integridad y funcionalidad completa del sistema:

**Tests de Backend (BackEnd-Test.py):**
- Validan las operaciones CRUD completas para usuarios y tareas a nivel de API
- Verifican la correcta asociación entre usuarios y tareas mediante IDs
- Incluyen validaciones de códigos de estado HTTP (200, 404, etc.)
- Implementan limpieza automática para evitar contaminación de datos entre ejecuciones

**Tests End-to-End (FrontEnd-Test.py):**
- Simulan el comportamiento real del usuario final en el navegador web
- Verifican la integración completa entre frontend, backend y base de datos
- Incluyen interacciones con elementos DOM (formularios, botones, listas)
- Garantizan que los datos creados en el frontend se reflejen correctamente en la base de datos

Ambos tipos de tests generan reportes PDF automáticos con resultados detallados, incluyendo marcas visuales de éxito (✅) o fallo (❌) para cada caso de prueba ejecutado.

### Mejoras de Código
- Manejo robusto de errores con try-catch
- Variables descriptivas y nomenclatura consistente
- Validaciones exhaustivas de estado
- Documentación inline mejorada

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Google Chrome (para pruebas E2E)
- ChromeDriver

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Dependencias Incluidas
- `flask` - Framework web
- `flask_sqlalchemy` - ORM para base de datos
- `requests` - Cliente HTTP
- `selenium` - Automatización de navegador
- `reportlab` - Generación de PDFs

## Ejecución del Sistema

### 1. Iniciar Servicios Backend
```bash
# Terminal 1 - Servicio de Usuarios
cd Users_Service
python main.py

# Terminal 2 - Servicio de Tareas
cd Task_Service
python main.py

# Terminal 3 - Frontend
cd Front-End
python main.py
```

### 2. Ejecutar Pruebas

**Pruebas de Backend:**
```bash
cd Test
python BackEnd-Test.py
```

**Pruebas End-to-End:**
```bash
cd Test
python FrontEnd-Test.py
```

## Resultados de las Pruebas

### Reportes Generados
- `backend_report_X.pdf` - Resultados de pruebas de integración backend
- `frontend_test_report_X.pdf` - Resultados de pruebas end-to-end

### Métricas de Cobertura
- ✅ 8 casos de prueba backend (CRUD completo + verificaciones)
- ✅ 7 casos de prueba frontend (flujo completo E2E + limpieza)
- ✅ 100% cobertura de APIs críticas
- ✅ Verificación de integridad de datos
- ✅ Limpieza automática post-pruebas

## Tecnologías de Testing y Reportes

- **Testing**: Selenium WebDriver, Requests
- **Reportes**: ReportLab PDF

## Autor

Carlos Daniel García

---

