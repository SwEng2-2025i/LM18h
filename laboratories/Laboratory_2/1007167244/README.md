# Ejemplo de Pruebas de Integración

Este proyecto demuestra las pruebas de integración entre múltiples microservicios y una aplicación frontend, con características mejoradas para limpieza de datos y generación automática de reportes PDF.

## Estructura del Proyecto

```
1007167244/
├── Front-End/          # Aplicación frontend (aplicación web Flask)
├── Users_Service/      # Microservicio de gestión de usuarios
├── Task_Service/       # Microservicio de gestión de tareas
├── Test/              # Archivos de pruebas de integración
│   ├── BackEnd-Test.py
│   ├── FrontEnd-Test.py
│   └── pdf_generator.py
├── requirements.txt   # Dependencias de Python
└── README.md         # Este archivo
```

## Servicios

### Servicio de Usuarios (Puerto 5001)
- **POST** `/users` - Crear un nuevo usuario
- **GET** `/users` - Listar todos los usuarios
- **GET** `/users/<id>` - Obtener usuario por ID
- **DELETE** `/users/<id>` - Eliminar usuario por ID *(Agregado)*

### Servicio de Tareas (Puerto 5002)
- **POST** `/tasks` - Crear una nueva tarea
- **GET** `/tasks` - Listar todas las tareas
- **GET** `/tasks/<id>` - Obtener tarea por ID *(Agregado para verificación)*
- **DELETE** `/tasks/<id>` - Eliminar tarea por ID *(Agregado)*

### Frontend (Puerto 5000)
- Interfaz web para crear usuarios y tareas
- Muestra lista de tareas

## Archivos de Prueba

### BackEnd-Test.py
Prueba de integración para servicios backend que:
1. Crea un usuario
2. Crea una tarea para ese usuario
3. Verifica que la tarea esté correctamente vinculada al usuario
4. **Elimina la tarea y usuario creados** *(Agregado)*
5. **Verifica que tanto el usuario como la tarea sean eliminados correctamente** *(Agregado)*
6. **Genera un reporte PDF con los resultados de la prueba** *(Agregado)*

### FrontEnd-Test.py
Prueba end-to-end usando Selenium que:
1. Abre la aplicación frontend
2. Crea un usuario a través de la interfaz web
3. Crea una tarea para ese usuario
4. Verifica que la tarea aparezca en la lista de tareas
5. **Elimina el usuario y tarea creados mediante llamadas API** *(Agregado)*
6. **Verifica la eliminación mediante verificación API** *(Agregado)*
7. **Genera un reporte PDF con los resultados de la prueba** *(Agregado)*

### pdf_generator.py
Clase utilitaria para generar reportes PDF con:
- **Numeración secuencial** (report_1.pdf, report_2.pdf, etc.)
- **Preservación de reportes anteriores** - sin sobrescribir
- **Resultados de pruebas completos** incluyendo verificación de limpieza

## Nuevas Características Agregadas

### 1. Limpieza de Datos
- **Endpoints DELETE** agregados a ambos servicios (Users_Service y Task_Service)
- **Endpoint GET específico** agregado a Task_Service para verificación
- **Limpieza automática** después de la ejecución de pruebas en ambos archivos de prueba
- **Verificación** de que los datos de prueba sean eliminados correctamente
- Asegura que las pruebas no dejen datos residuales en el sistema

### 2. Generación de Reportes PDF
- **Generación automática de PDF** después de cada ejecución de prueba
- **Numeración secuencial** (Backend-report_1.pdf, Frontend-report_1.pdf, etc.)
- **Preservación de reportes anteriores** - sin sobrescribir
- Los reportes incluyen:
  - Resultados de pruebas (pass/fail)
  - IDs de usuario y tarea creados
  - Estado de verificación de limpieza
  - Información de fecha y hora

## Resumen de Cambios en el Código

### Servicios Backend
- **Users_Service/main.py**: Agregado endpoint DELETE para eliminación de usuarios
- **Task_Service/main.py**: Agregado endpoint DELETE para eliminación de tareas y GET para verificación

### Archivos de Prueba
- **Test/BackEnd-Test.py**: 
  - Agregadas funciones de limpieza (`delete_user`, `delete_task`)
  - Agregada lógica de verificación mejorada para eliminación de datos
  - Agregada generación de reportes PDF con numeración secuencial
- **Test/FrontEnd-Test.py**:
  - Agregadas funciones de limpieza usando llamadas API
  - Agregada lógica de verificación para eliminación de datos
  - Agregada generación de reportes PDF con numeración secuencial
- **Test/pdf_generator.py**: Nueva utilidad para generación de reportes PDF

### Dependencias
- **requirements.txt**: Agregado paquete `fpdf` para generación de PDF

## Ejecutar las Pruebas

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Iniciar los servicios:
   ```bash
   # Terminal 1
   cd Users_Service
   python main.py
   
   # Terminal 2
   cd Task_Service
   python main.py
   
   # Terminal 3
   cd Front-End
   python main.py
   ```

3. Ejecutar las pruebas:
   ```bash
   # Prueba de integración backend
   cd Test
   python BackEnd-Test.py
   
   # Prueba E2E frontend
   python FrontEnd-Test.py
   ```

## Resultados de las Pruebas

Después de ejecutar las pruebas, encontrarás:
- Salida de consola mostrando ejecución y resultados de las pruebas
- Reportes PDF en el directorio `Test/` (ej., `Backend-report_1.pdf`, `Frontend-report_1.pdf`)
- Estado limpio del sistema sin datos residuales de prueba

## Beneficios

1. **Integridad de Datos**: Las pruebas se limpian después de sí mismas, previniendo contaminación de datos
2. **Reproducibilidad**: Cada ejecución de prueba comienza con un estado limpio
3. **Documentación**: Los reportes PDF proporcionan registros permanentes de la ejecución de pruebas
4. **Trazabilidad**: La numeración secuencial permite el seguimiento del historial de pruebas
5. **Confiabilidad**: La verificación asegura que la limpieza realmente funcionó

Este framework mejorado de pruebas de integración proporciona una base robusta para probar arquitecturas de microservicios con gestión adecuada de datos y reportes completos. 