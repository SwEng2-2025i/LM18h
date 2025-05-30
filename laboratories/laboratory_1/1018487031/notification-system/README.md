
# 🧪 Sistema de Notificaciones Multicanal

**Autor:** Sergio Esteban Rendón Umbarila

## 📋 Descripción General

Este proyecto implementa una REST API completa para un sistema de notificaciones multicanal que demuestra patrones avanzados de diseño de software. El sistema permite a los usuarios registrarse con múltiples canales de comunicación y envía notificaciones con mecanismos inteligentes de respaldo.

## 🏗️ Arquitectura del Sistema

### Patrones de Diseño Implementados

1. **Patrón Cadena de Responsabilidad** 🔗  
   - Maneja intentos de entrega de notificaciones a través de diferentes canales  
   - Cambia automáticamente a canales alternativos si la entrega falla  
   - Cada handler (Email, SMS, Consola) puede procesar o pasar la solicitud al siguiente

2. **Patrón Fábrica** 🏭  
   - Crea manejadores de canal de notificación dinámicamente  
   - Encapsula la lógica de creación para diferentes tipos de canal  
   - Proporciona una interfaz limpia para agregar nuevos canales

3. **Patrón Singleton** 🎯  
   - Asegura una única instancia del Logger en toda la aplicación  
   - Mantiene un registro consistente en todos los componentes  
   - Proporciona gestión centralizada de registros

4. **Patrón Estrategia** 📋  
   - Cada canal de notificación implementa una estrategia de entrega distinta  
   - Permite seleccionar algoritmos de entrega en tiempo de ejecución  
   - Facilita agregar nuevos métodos de notificación

## 📁 Estructura del Proyecto

```
notification-system/
├── app.py                          # Aplicación principal de Flask
├── models/
│   ├── user.py                     # Modelo de usuario y UserManager
│   └── notification.py             # Modelo de notificación
├── patterns/
│   ├── chain_of_responsibility.py  # Implementación del patrón cadena de responsabilidad
│   └── factory.py                  # Patrón fábrica para crear canales
├── utils/
│   └── logger.py                   # Implementación del logger Singleton
├── test_api.py                     # Script de pruebas de API
└── README.md                       # Este archivo
```

## 🔧 Endpoints de la API

### Gestión de Usuarios

| Método | Endpoint     | Descripción                              |
|--------|--------------|------------------------------------------|
| `GET`  | `/users`     | Lista todos los usuarios registrados     |
| `POST` | `/users`     | Registra un nuevo usuario con preferencias |

### Notificaciones

| Método | Endpoint               | Descripción                               |
|--------|------------------------|-------------------------------------------|
| `POST` | `/notifications/send`  | Envía una notificación con canales de respaldo |

### Sistema

| Método | Endpoint     | Descripción                          |
|--------|--------------|--------------------------------------|
| `GET`  | `/logs`      | Recupera los registros del sistema   |
| `GET`  | `/docs/`     | Documentación interactiva (Swagger)  |

## 📝 Ejemplos de Uso de la API

### Registrar un Usuario

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms", "console"]
  }'
```

### Enviar una Notificación

```bash
curl -X POST http://localhost:5000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Juan",
    "message": "Tu cita es mañana.",
    "priority": "high"
  }'
```

### Listar Todos los Usuarios

```bash
curl -X GET http://localhost:5000/users
```

### Obtener Registros del Sistema

```bash
curl -X GET http://localhost:5000/logs
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar los archivos del proyecto**

2. **Instalar las dependencias necesarias:**
   ```bash
   pip install flask flask-restx
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

4. **Acceder a la API:**
   - URL base: `http://localhost:5000`
   - Documentación interactiva: `http://localhost:5000/docs/`

## 🧪 Pruebas

### Pruebas Automatizadas

Ejecutar la suite de pruebas:

```bash
python test_api.py
```

Este script prueba:
- Registro de usuarios
- Envío de notificaciones en diferentes escenarios
- Manejo de errores
- Mecanismo de respaldo de la cadena
- Registro de actividad del sistema

### Pruebas Manuales con Postman

1. Importar la colección o crear solicitudes manualmente:

**Colección: API del Sistema de Notificaciones**

- **Registrar Usuario**: `POST /users`
- **Listar Usuarios**: `GET /users`
- **Enviar Notificación**: `POST /notifications/send`
- **Obtener Registros**: `GET /logs`

### Datos de Prueba

```json
// Usuarios de ejemplo
{
  "name": "Alice",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console"]
}

{
  "name": "Bob",
  "preferred_channel": "sms",
  "available_channels": ["sms", "console"]
}

// Notificación de ejemplo
{
  "user_name": "Alice",
  "message": "¡Tu pedido ha sido enviado!",
  "priority": "high"
}
```

## 🎯 Funcionalidades Clave

### Flujo Lógico de Notificación

1. **Registro de Usuario**  
2. **Solicitud de Notificación**  
3. **Configuración de Canales**  
4. **Intento de Entrega**  
5. **Mecanismo de Respaldo**  
6. **Registro**  
7. **Respuesta**

### Simulación de Fallas

- **Fallas Aleatorias**
- **Entrega Garantizada**
- **Registro Detallado**

## 🔍 Justificación de Patrones de Diseño

### Cadena de Responsabilidad  
### Patrón Fábrica  
### Logger Singleton  
### Patrón Estrategia

## 📊 Diagrama de Clases

\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      User       │    │  Notification   │    │     Logger      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - name          │    │ - id            │    │ - _instance     │
│ - preferred_ch  │    │ - user_name     │    │ - _logs         │
│ - available_ch  │    │ - message       │    ├─────────────────┤
└─────────────────┘    │ - priority      │    │ + log()         │
                       │ - status        │    │ + get_logs()    │
                       └─────────────────┘    └─────────────────┘
                                                      ▲
                                                      │ (Singleton)
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  UserManager    │    │NotificationChain│    │ChannelFactory   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - _users        │    │ - chain_root    │    │                 │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ + add_user()    │    │ + setup_chain() │    │ + create_ch()   │
│ + get_user()    │    │ + send_notif()  │    └─────────────────┘
└─────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │NotificationHandler│ (Abstract)
                    ├─────────────────┤
                    │ - _next_handler │
                    ├─────────────────┤
                    │ + set_next()    │
                    │ + handle()      │
                    └─────────────────┘
                            ▲
                ┌───────────┼───────────┐
                │           │           │
        ┌───────────┐ ┌───────────┐ ┌───────────┐
        │EmailHandler│ │SMSHandler │ │ConsoleHandler│
        └───────────┘ └───────────┘ └───────────┘
\`\`\`


## 🔧 Configuración

- **Host**: `0.0.0.0`
- **Puerto**: `5000`
- **Debug**: `True`

## 🚨 Manejo de Errores

- 400, 404, 409, 500 con mensajes adecuados

## 📈 Mejoras Futuras

- Base de datos, autenticación, webhooks, plantillas, analítica

## 🤝 Contribuciones

- Nuevos canales, pruebas, documentación, patrones adicionales

## 📄 Licencia

Proyecto con fines educativos para laboratorio de patrones de diseño.

