# Laboratorio 2 - Extensiones de Pruebas de Integración

**Autor:** Manuel Castiblanco  
**Fecha:** Julio 2025

## Introducción

En este laboratorio se extiende el ejemplo original de pruebas de integración revisado en clase. El enfoque principal se centra en implementar dos funcionalidades esenciales para un sistema de pruebas robusto:

1. **Limpieza Inteligente de Datos**: Se desarrolla un sistema que elimina automáticamente solo los datos creados durante cada prueba, sin afectar información existente.
2. **Reportes PDF Automáticos**: Se crea un generador de reportes que documenta cada ejecución de pruebas con numeración secuencial.

## Implementación Realizada

### 1. Mejoras en requirements.txt

Se reorganiza el archivo de dependencias para mejorar la legibilidad. Cada paquete se coloca en su propia línea, facilitando el mantenimiento y la lectura.

### 2. Nuevos Endpoints en Users_Service/main.py

Se agregan tres nuevos endpoints para el manejo de usuarios:

```python
DELETE /users/<int:user_id>          # Elimina un usuario específico
DELETE /users/cleanup                # Elimina TODOS los usuarios (¡cuidado!)
DELETE /users/cleanup-specific       # Elimina solo usuarios específicos por ID
```

**Nota importante:** El endpoint `/users/cleanup` elimina TODOS los usuarios de la base de datos. Se mantiene para casos donde se necesite limpiar completamente la BD, pero normalmente se debe usar `/users/cleanup-specific` que solo elimina los usuarios especificados.

#### Cómo usar /users/cleanup-specific:

```bash
# Ejemplo con curl
curl -X DELETE http://localhost:5001/users/cleanup-specific \
  -H "Content-Type: application/json" \
  -d '{"user_ids": [1, 2, 3]}'
```

También se reordenan las rutas porque Flask confundía `/users/cleanup` con `/users/<int:user_id>` y generaba errores 404.

### 3. Nuevos Endpoints en Task_Service/main.py

Similar a los usuarios, se agregan tres endpoints para las tareas:

```python
DELETE /tasks/<int:task_id>          # Elimina una tarea específica
DELETE /tasks/cleanup                # Elimina TODAS las tareas (¡cuidado!)
DELETE /tasks/cleanup-specific       # Elimina solo tareas específicas por ID
```

#### Cómo usar /tasks/cleanup y /tasks/cleanup-specific:

```bash
# Eliminar todas las tareas (usar con cuidado)
curl -X DELETE http://localhost:5002/tasks/cleanup

# Eliminar tareas específicas (más seguro)
curl -X DELETE http://localhost:5002/tasks/cleanup-specific \
  -H "Content-Type: application/json" \
  -d '{"task_ids": [1, 2, 3]}'
```

**Tip:** Se debe eliminar las tareas antes que los usuarios por las relaciones de clave foránea.

### 4. Test/pdf_report_generator.py (ARCHIVO NUEVO)

**Características:**

- Generación automática de reportes PDF con numeración secuencial
- Seguimiento integral de resultados de pruebas
- Diseño de reportes con tablas y formato
- Rastrea datos creados y resultados de limpieza
- Previene sobrescritura de reportes anteriores

### 4. El Generador de Reportes PDF (Test/pdf_report_generator.py)

Esta fue probablemente la parte más interesante de implementar. Se crea una clase que genera reportes PDF automáticamente:

- **Numeración secuencial**: Los reportes se numeran como 001, 002, 003, etc.
- **Nunca sobrescribe**: Cada reporte se guarda por separado
- **Formato**: Se usa ReportLab para crear PDFs que se ven bien
- **Información completa**: Incluye qué datos se crearon, qué se limpió, y si todo funcionó correctamente

### 5. Mejoras en las Pruebas (BackEnd-Test.py y FrontEnd-Test.py)

Se realizan cambios significativos para hacer las pruebas más inteligentes:

**Antes:** Las pruebas creaban datos y los dejaban en la base de datos
**Ahora:** Las pruebas:

- Rastrean exactamente qué datos crean (guardan los IDs)
- Al final, eliminan SOLO esos datos específicos
- Verifican que efectivamente se eliminaron
- Generan un reporte PDF con todo lo que ocurrió

**Beneficio principal:** Ya no es necesario preocuparse por limpiar la base de datos manualmente entre pruebas.

### 6. Directorio de Reportes (Test/reports/)

Se crea este directorio para mantener todos los PDFs organizados. Cada vez que se ejecuta una prueba, se genera un nuevo reporte aquí.

## Cómo Funciona el Sistema

### El Sistema de Limpieza Inteligente

Se desarrollan dos tipos de limpieza:

1. **Limpieza completa** (`/cleanup`): Elimina TODO de la base de datos
2. **Limpieza específica** (`/cleanup-specific`): Elimina solo lo que se especifique

Las pruebas automáticamente usan la limpieza específica, pero si se necesita limpiar todo, se pueden usar:

```bash
# Limpiar todas las tareas
curl -X DELETE http://localhost:5002/tasks/cleanup

# Limpiar todos los usuarios
curl -X DELETE http://localhost:5001/users/cleanup
```

**¡Importante!** Estos endpoints eliminan TODO. Solo se deben usar cuando se esté completamente seguro.

- Mejoró todas las funciones de prueba para registrar resultados y rastrear datos creados
- Agregó función `cleanup_test_data()` para limpieza integral
- Agregó verificación de efectividad de limpieza
- Integró generación de reportes PDF
- Agregó manejo de excepciones y reportes adecuados

**Nuevas Características:**

- Rastrea todos los IDs de usuarios y tareas creados a través de interacciones UI
- Registra estado de pase/fallo para cada paso de prueba
- Realiza limpieza automática después de ejecución de pruebas vía llamadas API
- Verifica que la limpieza fue exitosa
- Genera reporte PDF con toda la información de pruebas
- Mantiene automatización del navegador mientras agrega limpieza de backend

**Propósito:**

- Asegurar que no permanezcan datos de prueba después de pruebas UI
- Proporcionar documentación detallada de resultados de pruebas E2E
- Combinar pruebas frontend con capacidades de limpieza backend

### 7. Test/reports/ (DIRECTORIO NUEVO)

**Propósito:**

- Almacenar todos los reportes PDF generados
- Mantener estructura organizada para documentación de pruebas
- Habilitar acceso fácil a resultados históricos de pruebas

### Limpieza Manual de Datos

Si se necesita limpiar datos específicos manualmente, se pueden usar estos endpoints:

```bash
# Para limpiar tareas específicas
curl -X DELETE http://localhost:5002/tasks/cleanup-specific \
  -H "Content-Type: application/json" \
  -d '{"task_ids": [1, 2, 3]}'

# Para limpiar usuarios específicos
curl -X DELETE http://localhost:5001/users/cleanup-specific \
  -H "Content-Type: application/json" \
  -d '{"user_ids": [1, 2, 3]}'
```

**Para limpiar TODO (¡usar con cuidado!):**

```bash
# Primero eliminar todas las tareas
curl -X DELETE http://localhost:5002/tasks/cleanup

# Luego eliminar todos los usuarios
curl -X DELETE http://localhost:5001/users/cleanup
```

## Cómo Usar Este Sistema

### 1. Instalación

```bash
pip install -r requirements.txt
```

### 2. Arrancar los Servicios

Se necesitan 3 terminales:

```bash
# Terminal 1 - Servicio de Usuarios
python Users_Service/main.py

# Terminal 2 - Servicio de Tareas
python Task_Service/main.py

# Terminal 3 - Frontend
python Front-End/main.py
```

### 3. Ejecutar las Pruebas

```bash
# Prueba del backend
python Test/BackEnd-Test.py

# Prueba del frontend (se necesita Chrome)
python Test/FrontEnd-Test.py
```

### 4. Revisar los Reportes

Después de cada prueba, se puede encontrar el reporte PDF en `Test/reports/`. Los archivos se nombran como `test_report_001.pdf`, `test_report_002.pdf`, etc.

## Problemas Resueltos

1. **Error 404 en `/cleanup`**: Las rutas estaban en el orden incorrecto
2. **Eliminación masiva de datos**: Se cambió a limpieza específica por IDs
3. **Falta de documentación**: Los reportes PDF ahora guardan todo automáticamente

## Conclusión

Este laboratorio ayuda a entender mejor cómo crear un sistema de pruebas robusto que no solo funcione, sino que también sea seguro y mantenga un registro detallado de todo lo que hace.

La parte más satisfactoria fue ver cómo las pruebas ahora se limpian automáticamente después de ejecutarse, y tener reportes PDF que documentan cada ejecución.

---

**Manuel Castiblanco**  
_Julio 2025_

```bash
# Prueba Backend
python Test/BackEnd-Test.py

# Prueba Frontend (requiere navegador Chrome)
python Test/FrontEnd-Test.py
```

4. **Verificar Resultados**:
   - Los reportes PDF se generarán en el directorio `Test/reports/`
   - Los reportes se numeran secuencialmente y nunca se sobrescriben
   - Todos los datos de prueba se limpian automáticamente después de cada ejecución

## Beneficios de la Implementación

1. **Integridad de Datos**: No hay contaminación de datos de prueba entre ejecuciones
2. **Protección de Datos Existentes**: Solo se eliminan los datos creados durante las pruebas, preservando información preexistente
3. **Documentación**: Reportes PDF integrales para cada ejecución de prueba
4. **Repetibilidad**: Las pruebas pueden ejecutarse múltiples veces sin conflictos
5. **Limpieza Selectiva**: Sistema inteligente que distingue entre datos de prueba y datos de producción
6. **Trazabilidad**: Historial completo de todas las ejecuciones de pruebas
7. **Reportes**: Reportes PDF limpios y formateados adecuados para documentación
8. **Limpieza Automatizada**: No se requiere intervención manual para limpieza de datos

## Notas Técnicas

- Las operaciones de limpieza eliminan tareas antes que usuarios debido a restricciones de clave foránea
- Los reportes PDF usan numeración secuencial para prevenir sobrescrituras
- Todos los endpoints mantienen compatibilidad hacia atrás
- El manejo de errores asegura que las pruebas se completen incluso con fallas
- Los pasos de verificación confirman limpieza exitosa
