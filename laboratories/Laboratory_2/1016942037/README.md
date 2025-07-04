# Laboratorio 2 - Sistema de Microservicios con Limpieza de Datos y Reportes PDF

## Descripción del Proyecto

Este proyecto implementa un sistema de microservicios con tres componentes principales:
- **Frontend**: Interfaz web en Flask (puerto 5000)
- **Users Service**: Microservicio para gestión de usuarios (puerto 5001)
- **Tasks Service**: Microservicio para gestión de tareas (puerto 5002)

## Características Implementadas

### 1. Limpieza Automática de Datos
Se implementó un sistema de limpieza automática que elimina los datos creados durante las pruebas, tanto en el backend como en el frontend.

**Archivos modificados:**
- `Test/BackEnd-Test.py`: Agregadas funciones `delete_task()`, `delete_user()`, `verify_task_deleted()`, `verify_user_deleted()`
- `Test/FrontEnd-Test.py`: Agregadas funciones de eliminación y verificación a través de la interfaz web
- `Front-End/main.py`: Mejorado el manejo de errores y validación de datos

**Funcionalidades agregadas:**
- Endpoints DELETE en ambos microservicios
- Verificación automática de eliminación
- Limpieza en orden inverso (tareas antes que usuarios)
- Manejo de errores durante la limpieza

### 2. Generación Automática de Reportes PDF
Se implementó un sistema completo de generación de reportes PDF con numeración secuencial y preservación de reportes anteriores.

**Archivos nuevos:**
- `Test/test_report.py`: Módulo principal para generación de reportes

**Archivos modificados:**
- `Test/BackEnd-Test.py`: Integrado sistema de reportes
- `Test/FrontEnd-Test.py`: Integrado sistema de reportes
- `requirements.txt`: Agregada dependencia `reportlab==3.6.8`

**Características del sistema de reportes:**
- Numeración secuencial automática (test_report_001.pdf, test_report_002.pdf, etc.)
- Preservación de reportes anteriores
- Registro detallado de tiempos de ejecución
- Logs con timestamps de cada operación
- Indicadores visuales de éxito/error
- Formato profesional con tablas y estilos
- Almacenamiento en directorio `Test/reports/`

## Estructura del Proyecto

```
1016942037/
├── Front-End/
│   └── main.py                 # Frontend Flask
├── Task_Service/
│   └── main.py                 # Microservicio de tareas
├── Users_Service/
│   └── main.py                 # Microservicio de usuarios
├── Test/
│   ├── BackEnd-Test.py         # Pruebas de backend con reportes
│   ├── FrontEnd-Test.py        # Pruebas de frontend con reportes
│   ├── test_report.py          # Módulo de generación de reportes
│   └── reports/                # Directorio de reportes PDF
└── requirements.txt            # Dependencias del proyecto
```

## Instalación y Uso

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar los servicios
```bash
# Terminal 1 - Frontend
cd Front-End
python main.py

# Terminal 2 - Users Service
cd Users_Service
python main.py

# Terminal 3 - Tasks Service
cd Task_Service
python main.py
```

### 3. Ejecutar las pruebas
```bash
# Pruebas de Backend
python Test/BackEnd-Test.py

# Pruebas de Frontend
python Test/FrontEnd-Test.py
```

## Resultados de las Pruebas

### Pruebas de Backend
- ✅ Creación exitosa de usuarios
- ✅ Creación exitosa de tareas
- ✅ Verificación de asociación usuario-tarea
- ✅ Eliminación exitosa de tareas
- ✅ Eliminación exitosa de usuarios
- ✅ Verificación de limpieza de datos
- ✅ Generación automática de reportes PDF

### Pruebas de Frontend
- ✅ Navegación a la aplicación web
- ✅ Creación de usuarios a través de la interfaz
- ✅ Creación de tareas a través de la interfaz
- ✅ Verificación de tareas en la lista
- ✅ Limpieza de datos a través de APIs
- ✅ Verificación de eliminación
- ✅ Generación automática de reportes PDF

## Características Técnicas

### Sistema de Reportes
- **Librería**: ReportLab 3.6.8
- **Formato**: PDF profesional con tablas
- **Numeración**: Secuencial automática
- **Preservación**: Todos los reportes anteriores se mantienen
- **Contenido**: Tiempos, logs, estados, errores

### Limpieza de Datos
- **Backend**: Eliminación directa via APIs
- **Frontend**: Eliminación via APIs con verificación visual
- **Orden**: Tareas antes que usuarios (dependencias)
- **Verificación**: Confirmación de eliminación exitosa

### Manejo de Errores
- Captura y registro de errores en reportes
- Mensajes descriptivos de fallos
- Continuación de limpieza incluso con errores
- Logs detallados para depuración

## Archivos de Código Agregados/Modificados

### Nuevos Archivos
1. `Test/test_report.py` - Sistema completo de reportes PDF

### Archivos Modificados
1. `Test/BackEnd-Test.py` - Integración de reportes y limpieza
2. `Test/FrontEnd-Test.py` - Integración de reportes y limpieza
3. `Front-End/main.py` - Mejoras en validación y manejo de errores
4. `requirements.txt` - Agregada dependencia reportlab

### Funcionalidades Agregadas
- Sistema de limpieza automática de datos
- Generación automática de reportes PDF
- Numeración secuencial de reportes
- Preservación de reportes anteriores
- Logs detallados con timestamps
- Manejo robusto de errores
- Verificación de eliminación de datos

## Conclusión

El proyecto ha sido exitosamente implementado con todas las características requeridas:
- ✅ Sistema de microservicios funcional
- ✅ Limpieza automática de datos
- ✅ Generación automática de reportes PDF
- ✅ Numeración secuencial y preservación de reportes
- ✅ Pruebas completas de backend y frontend
- ✅ Manejo robusto de errores

Todos los componentes funcionan correctamente y generan reportes detallados que facilitan el análisis y depuración de las pruebas.
