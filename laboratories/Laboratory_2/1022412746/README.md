# Sistema Avanzado de Pruebas de Integración

## Descripción General

Este proyecto implementa un sistema avanzado de pruebas de integración para una aplicación distribuida de gestión de tareas utilizando microservicios Flask. El sistema incluye limpieza automática de datos, generación de reportes en PDF y manejo integral de errores con fines educativos.

## Características Principales

- **Limpieza Automática de Datos**: Seguimiento automático y limpieza de datos de prueba
- **Generación de Reportes PDF**: Generación automática de reportes detallados de pruebas
- **Manejo Mejorado de Errores**: Gestión robusta de errores y manejo de excepciones
- **Seguimiento de Pruebas**: Monitoreo detallado y registro de resultados de pruebas
- **Compatibilidad Multiplataforma**: Optimizado para entornos Windows con manejo adecuado de codificación

## Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Servicio de    │    │  Servicio de    │
│   (Puerto 5000) │    │  Usuarios       │    │  Tareas         │
│                 │    │  (Puerto 5001)  │    │  (Puerto 5002)  │
│  HTML/CSS/JS    │◄──►│  Flask + SQLite │◄──►│  Flask + SQLite │
│                 │    │   users.db      │    │   tasks.db      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         │                       ▼                       ▼
         │                [DELETE /users]         [DELETE /tasks]
         │                [DELETE /users/cleanup] [DELETE /tasks/cleanup]
         │
         ▼
┌─────────────────┐                        ┌─────────────────┐
│ Pruebas E2E     │                        │ Pruebas de      │
│ (Selenium)      │                        │ Integración     │
│ + Limpieza      │                        │ (API)           │
│ + Reportes PDF  │                        │ + Limpieza      │
└─────────────────┘                        │ + Reportes PDF  │
                                           └─────────────────┘
```

## Guía de Inicio Rápido

Para usuarios principiantes, siga estos pasos en orden:

### 1. Verificar Requisitos del Sistema
```bash
python --version  # Debe ser 3.7 o superior
```

### 2. Instalar Dependencias
```bash
python setup.py
```

### 3. Verificar Instalación
```bash
python verify_project.py
```

### 4. Inicializar Bases de Datos
```bash
python init_db.py
# Elija la opción 2 cuando se le solicite
```

### 5. Iniciar Servicios
```bash
python quick_start.py
```

### 6. Ejecutar Pruebas
```bash
python run_tests.py
```

### 7. Verificar Resultados
- Ver salida de consola para resultados de pruebas
- Revisar directorio `test_reports/` para reportes PDF

## Cumplimiento de Requerimientos Principales

Este proyecto cumple específicamente con los dos requerimientos principales establecidos:

### Requerimiento 1: Limpieza de Datos (Data Cleanup)

**Especificación**: Todos los datos agregados al sistema durante la ejecución de pruebas deben ser eliminados posteriormente (solo los datos agregados por las pruebas). Además, las pruebas deben verificar que los datos han sido eliminados correctamente. Este comportamiento debe implementarse tanto en BackEnd como en FrontEnd.

**Implementación en el Proyecto**:

1. **Seguimiento Automático de Datos**:
   - La clase `TestDataTracker` en `test_utils.py` registra automáticamente todos los IDs de usuarios y tareas creados durante las pruebas
   - Métodos `track_user(user_id)` y `track_task(task_id)` mantienen listas de datos creados

2. **Endpoints de Limpieza Específicos**:
   - `DELETE /users/cleanup-specific`: Elimina únicamente los usuarios creados durante las pruebas
   - `DELETE /tasks/cleanup-specific`: Elimina únicamente las tareas creadas durante las pruebas
   - Estos endpoints reciben listas de IDs específicos, garantizando que solo se eliminen datos de prueba

3. **Verificación de Limpieza**:
   - Método `verify_cleanup()` confirma que todos los datos tracked fueron eliminados
   - Realiza consultas GET para verificar que los datos ya no existen en el sistema
   - Reporta cualquier dato que no fue eliminado correctamente

4. **Implementación en BackEnd y FrontEnd**:
   - **BackEnd Test** (`BackEnd-Test.py`): Implementa limpieza completa con verificación
   - **FrontEnd Test** (`FrontEnd-Test.py`): Implementa el mismo sistema de tracking y limpieza
   - Ambos tests utilizan la misma infraestructura de `TestDataTracker`

### Requerimiento 2: Generación Automática de Reportes PDF

**Especificación**: Los resultados de las pruebas deben guardarse automáticamente en un archivo PDF generado por el sistema. Cada reporte debe tener un número secuencial y no debe sobrescribir reportes anteriores: todos los PDFs generados previamente deben preservarse.

**Implementación en el Proyecto**:

1. **Generación Automática**:
   - La clase `PDFReportGenerator` en `test_utils.py` genera automáticamente reportes PDF al finalizar cada prueba
   - No requiere intervención manual del usuario

2. **Numeración Secuencial**:
   - Método `get_next_report_number()` busca automáticamente el siguiente número disponible
   - Formato: `test_report_001.pdf`, `test_report_002.pdf`, etc.
   - Garantiza numeración consecutiva sin duplicados

3. **Preservación de Reportes Anteriores**:
   - El sistema nunca sobrescribe reportes existentes
   - Cada ejecución genera un nuevo archivo con número único
   - Directorio `test_reports/` mantiene historial completo

4. **Contenido Completo del Reporte**:
   - Resumen ejecutivo con estadísticas de pruebas
   - Resultados detallados de cada test individual
   - Métricas de limpieza (usuarios/tareas eliminados)
   - Estado de verificación de limpieza
   - Timestamp y metadata del test

**Evidencia de Cumplimiento**:
- Código fuente en `test_utils.py` líneas 200-280 (generación PDF)
- Código fuente en `test_utils.py` líneas 120-180 (limpieza y verificación)
- Directorio `test_reports/` con múltiples reportes numerados secuencialmente
- Logs de consola mostrando confirmación de limpieza y generación de reportes

## Características Mejoradas

### 1. Limpieza Automática de Datos
- **Seguimiento automático**: Todos los datos creados durante las pruebas son rastreados automáticamente
- **Limpieza automatizada**: Los datos se eliminan automáticamente al final de cada prueba
- **Verificación**: Confirma que todos los datos de prueba fueron eliminados correctamente
- **Nuevos endpoints**:
  - `DELETE /users/{id}` - Eliminar usuario específico
  - `DELETE /users/cleanup` - Eliminar todos los usuarios
  - `DELETE /tasks/{id}` - Eliminar tarea específica
  - `DELETE /tasks/cleanup` - Eliminar todas las tareas

### 2. Generación de Reportes PDF
- **Reportes secuenciales**: Numeración automática (test_report_001.pdf, test_report_002.pdf...)
- **Contenido completo**: Resultados de pruebas, información de limpieza y verificaciones
- **Preservación**: Los reportes anteriores nunca se sobrescriben
- **Ubicación**: Directorio `test_reports/`
- **Formato mejorado**: Texto limpio sin etiquetas HTML, colores apropiados para estado

### 3. Utilidades de Prueba Mejoradas
- **TestDataTracker**: Clase para rastrear datos de prueba
- **PDFReportGenerator**: Clase para generar reportes
- **Manejo mejorado de errores**: Gestión robusta de errores y manejo de excepciones

## Instalación y Configuración

### Prerrequisitos
- Python 3.7 o superior
- Navegador Google Chrome
- ChromeDriver (debe estar en el PATH del sistema)

### Paso 1: Verificar Dependencias
```bash
python setup.py
```

### Paso 2: Verificar Estructura del Proyecto
```bash
python verify_project.py
```

### Paso 3: Instalación Manual (si es necesario)
```bash
pip install flask flask-sqlalchemy flask-cors requests reportlab selenium pytest
```

### Paso 4: Inicialización de Base de Datos
```bash
python init_db.py
```
**Importante**: Al ejecutar este script, elija la opción 2 (Creación manual de base de datos) para asegurar que las bases de datos se creen correctamente.

## Ejecución

### Opción 1: Inicio Rápido (Recomendado)
```bash
python quick_start.py
```
Este script iniciará automáticamente todos los servicios y esperará hasta que estén listos.

### Opción 2: Inicio Manual

#### 1. Iniciar Microservicios
Abra tres terminales separadas y ejecute:

**Terminal 1 - Servicio de Usuarios:**
```bash
cd Users_Service
python main.py
```

**Terminal 2 - Servicio de Tareas:**
```bash
cd Task_Service
python main.py
```

**Terminal 3 - Frontend:**
```bash
cd Front-End
python main.py
```

#### 2. Ejecutar Pruebas

**Pruebas de Backend:**
```bash
python Test/BackEnd-Test.py
```

**Pruebas de Frontend:**
```bash
python Test/FrontEnd-Test.py
```

**Suite Completa de Pruebas:**
```bash
python run_tests.py
```

## Resultados de Pruebas

### Salida de Consola
Las pruebas muestran información detallada en la consola:
- Resultados de pruebas para cada paso
- Información de limpieza
- Verificación de limpieza
- Estado de generación de reportes

### Reportes PDF
Cada reporte incluye:
- **Resumen ejecutivo** con estadísticas
- **Resultados detallados** para cada prueba
- **Información de limpieza** (usuarios/tareas eliminados)
- **Verificación de limpieza** (confirmación de eliminación)
- **Timestamp** y numeración secuencial

## Estructura del Proyecto

```
├── Front-End/
│   └── main.py                 # Aplicación web frontend
├── Users_Service/
│   ├── main.py                 # Microservicio de usuarios (mejorado)
│   └── instance/               # Directorio de instancia (buena práctica Flask)
│       └── users.db            # Base de datos SQLite
├── Task_Service/
│   ├── main.py                 # Microservicio de tareas (mejorado)
│   └── instance/               # Directorio de instancia (buena práctica Flask)
│       └── tasks.db            # Base de datos SQLite
├── Test/
│   ├── BackEnd-Test.py         # Pruebas de integración backend (mejorado)
│   ├── FrontEnd-Test.py        # Pruebas E2E frontend (mejorado)
│   └── test_utils.py           # Utilidades de prueba (NUEVO)
├── test_reports/               # Directorio de reportes PDF (NUEVO)
│   ├── test_report_001.pdf
│   ├── test_report_002.pdf
│   └── ...
├── requirements.txt            # Dependencias (actualizado)
├── setup.py                    # Script de configuración (NUEVO)
├── init_db.py                  # Script de inicialización de BD (NUEVO)
├── verify_project.py           # Script de verificación de proyecto (NUEVO)
├── quick_start.py              # Script de inicio rápido (NUEVO)
├── run_tests.py                # Script ejecutor de pruebas (NUEVO)
└── README.md                   # Esta documentación
```

## Endpoints de API

### Servicio de Usuarios (Puerto 5001)
- `GET /users` - Listar todos los usuarios
- `POST /users` - Crear nuevo usuario
- `GET /users/{id}` - Obtener usuario específico
- `DELETE /users/{id}` - **[NUEVO]** Eliminar usuario específico
- `DELETE /users/cleanup` - **[NUEVO]** Eliminar todos los usuarios
- `DELETE /users/cleanup-specific` - **[NUEVO]** Eliminar usuarios específicos por lista de IDs

### Servicio de Tareas (Puerto 5002)
- `GET /tasks` - Listar todas las tareas
- `POST /tasks` - Crear nueva tarea
- `DELETE /tasks/{id}` - **[NUEVO]** Eliminar tarea específica
- `DELETE /tasks/cleanup` - **[NUEVO]** Eliminar todas las tareas
- `DELETE /tasks/cleanup-specific` - **[NUEVO]** Eliminar tareas específicas por lista de IDs

## Flujo de Pruebas

### Prueba de Integración Backend
1. **Crear usuario** → Rastrear ID
2. **Crear tarea** → Rastrear ID
3. **Verificar asociación** entre usuario y tarea
4. **Limpieza** → Eliminar datos rastreados
5. **Verificar limpieza** → Confirmar eliminación
6. **Generar reporte PDF**

### Prueba E2E Frontend
1. **Abrir frontend** en navegador
2. **Crear usuario** via UI → Rastrear ID
3. **Crear tarea** via UI → Rastrear ID
4. **Verificar tarea** aparece en lista
5. **Limpieza** → Eliminar datos rastreados
6. **Verificar limpieza** → Confirmar eliminación
7. **Generar reporte PDF**

## Métricas de Reportes

Cada reporte PDF incluye:
- **Resumen de Pruebas**: Conteo de Aprobadas/Fallidas y porcentajes
- **Resultados Detallados**: Timestamp, estado y detalles para cada prueba
- **Métricas de Limpieza**: Número de usuarios/tareas eliminados
- **Estado de Verificación**: Confirmación de éxito de limpieza
- **Detalles de Errores**: Información sobre cualquier error encontrado

## Solución de Problemas

### Problemas Comunes

1. **ChromeDriver no encontrado**
   - Descargar ChromeDriver desde https://chromedriver.chromium.org/
   - Agregar al PATH del sistema
   - Asegurar compatibilidad de versión con su navegador Chrome

2. **Puerto ya en uso**
   - Verificar que los puertos 5000, 5001, 5002 estén disponibles
   - Usar `netstat -ano | findstr :5000` para verificar (Windows)
   - Cerrar cualquier servicio existente que use estos puertos

3. **Errores de importación de paquetes**
   - Ejecutar `python setup.py` para instalar dependencias
   - Verificar versión de Python (3.7 o superior requerido)
   - Verificar que todos los paquetes en requirements.txt estén instalados

4. **Errores de base de datos bloqueada**
   - Cerrar todos los servicios antes de ejecutar pruebas
   - Eliminar archivos `.db` si es necesario y reinicializar con `python init_db.py`
   - Asegurar que solo una instancia de cada servicio esté ejecutándose

5. **Errores Unicode/Codificación (Windows)**
   - Los reportes PDF y salida de consola han sido optimizados para Windows
   - Los caracteres Unicode de respuestas del servidor se filtran automáticamente
   - No se requiere configuración adicional de codificación

## Mejores Prácticas

1. **Siempre ejecutar limpieza** después de las pruebas para mantener consistencia de base de datos
2. **Verificar que los servicios estén ejecutándose** antes de ejecutar pruebas
3. **Revisar reportes PDF** para análisis detallado y depuración
4. **Usar modo headless** para pruebas automatizadas en entornos CI/CD
5. **Mantener reportes históricos** para análisis de tendencias y detección de regresiones
6. **Verificar formato de reporte**: Los nuevos reportes muestran estado como texto limpio (PASSED/FAILED) sin etiquetas HTML

## Guías de Desarrollo

Para extender este proyecto:
1. Agregar nuevas pruebas en el directorio `Test/`
2. Usar `TestDataTracker` para rastreo automático de datos de prueba
3. Implementar endpoints de limpieza para nuevos servicios
4. Actualizar `PDFReportGenerator` para nuevas métricas
5. Seguir los patrones establecidos de manejo de errores
6. Mantener compatibilidad con entornos Windows

## Contexto Educativo

Este proyecto está diseñado con fines educativos en la Universidad Nacional de Colombia, demostrando:
- Arquitectura de microservicios con Flask
- Metodologías de pruebas de integración
- Gestión automática de datos de prueba
- Generación de reportes y documentación
- Técnicas de manejo de errores y depuración
- Mejores prácticas para automatización de pruebas

## Licencia

Este proyecto es para fines educativos - Universidad Nacional de Colombia
