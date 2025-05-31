# Sistema de Notificaciones con Patrones Strategy y Chain of Responsibility

**Autor:** Brayan Exneyder Galindez Tobo  
**Email:** bgalindez@unal.edu.co  

## Descripción

API REST que implementa un sistema de notificaciones utilizando los patrones Strategy y Chain of Responsibility. El sistema permite enviar notificaciones a través de diferentes canales (email, SMS, WhatsApp) con validación de mensajes y manejo de fallos.

## Estructura del Proyecto

```
laboratory_1/1007167244/
├── api/
│   ├── __init__.py
│   └── resources.py         # Endpoints de la API
├── config/
│   └── app.py              # Configuración de Flask y Swagger
├── models/
│   └── storage.py          # Modelos y almacenamiento de datos
├── patterns/
│   ├── strategy.py         # Implementación del patrón Strategy
│   └── chain_of_responsibility.py  # Implementación del patrón Chain of Responsibility
├── venv/                   # Entorno virtual
├── api.py                  # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## Patrones Implementados

### Strategy
- Manejo de diferentes estrategias de envío (Email, SMS, WhatsApp)
- Intercambio dinámico de estrategias en caso de fallos
- Priorización de canales según preferencias del usuario

### Chain of Responsibility
- Validación de contenido inapropiado
- Validación de longitud de mensajes
- Validación de niveles de prioridad
- Procesamiento de entrega de mensajes

## Endpoints

### Usuarios
- `GET /users/` - Listar usuarios
- `POST /users/` - Crear usuario

### Notificaciones
- `GET /notifications/send` - Listar notificaciones
- `POST /notifications/send` - Enviar notificación
- `GET /notifications/history` - Historial de notificaciones
- `GET /notifications/stats` - Estadísticas del sistema

## Uso de la API

### 1. Crear un Usuario
```bash
# Usando curl
curl -X POST "http://localhost:5000/users/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Juan Pérez",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "whatsapp"]
}'

# Usando Postman
URL: http://localhost:5000/users/
Método: POST
Headers: Content-Type: application/json
Body:
{
    "name": "Juan Pérez",
    "preferred_channel": "email",
    "available_channels": ["email", "sms", "whatsapp"]
}
```

### 2. Listar Usuarios
```bash
# Usando curl
curl -X GET "http://localhost:5000/users/"

# Usando Postman
URL: http://localhost:5000/users/
Método: GET
```

### 3. Enviar Notificación
```bash
# Usando curl
curl -X POST "http://localhost:5000/notifications/send" \
-H "Content-Type: application/json" \
-d '{
  "user_name": "Juan Pérez",
  "message": "Bienvenido al sistema",
  "priority": "high"
}'

# Usando Postman
URL: http://localhost:5000/notifications/send
Método: POST
Headers: Content-Type: application/json
Body:
{
    "user_name": "Juan Pérez",
    "message": "Bienvenido al sistema",
    "priority": "high"
}
```

### 4. Ver Historial de Notificaciones
```bash
# Usando curl
curl -X GET "http://localhost:5000/notifications/history"

# Usando Postman
URL: http://localhost:5000/notifications/history
Método: GET
```

### 5. Ver Estadísticas
```bash
# Usando curl
curl -X GET "http://localhost:5000/notifications/stats"

# Usando Postman
URL: http://localhost:5000/notifications/stats
Método: GET
```

## Instalación y Configuración

1. Crear y activar entorno virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python api.py
```

4. Acceder a la documentación Swagger:
```
http://localhost:5000/apidocs/
```

## Documentación de la API

La documentación completa de la API está disponible en Swagger UI. Para acceder:

1. Inicia el servidor con `python api.py`
2. Abre tu navegador y ve a `http://localhost:5000/apidocs/`
3. En la interfaz de Swagger podrás:
   - Ver todos los endpoints disponibles
   - Probar los endpoints directamente
   - Ver los parámetros requeridos
   - Ver los códigos de respuesta
   - Ejecutar peticiones de prueba

## Notas Adicionales

- Las notificaciones se procesan según la prioridad especificada (low, medium, high)
- El sistema intentará usar el canal preferido del usuario, pero si falla, usará los canales alternativos
- Los mensajes son validados por contenido y longitud antes de ser enviados
- Las estadísticas incluyen información sobre el éxito de envío y uso de canales 