# Modular Notification API

**Autor:** Cristian Barrera

## Descripción del Sistema

Este proyecto es una API REST modular desarrollada con Flask para gestionar usuarios y enviar notificaciones a través de múltiples canales (email, SMS, console ,etc) usando patrones de diseño avanzados.

Se simulan intentos de entrega de notificaciones con una cadena de responsabilidad (Chain of Responsibility), permitiendo reintentos en canales alternativos si uno falla. Además, todas las notificaciones se registran con un logger implementado con el patrón Singleton.

## Endpoints

### Usuarios

- **POST /users**  
  Registra un usuario nuevo.  
  **Payload:**
  ```json
  {
    "name": "Cristian",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }
  ```

  **GET /users**
  Lista todos los usuarios registrados.

### Notificaciones
  **POST /notifications/send**
  Envia una notificación a un usuario.
  **Payload:**  
  ```json
  {
    "user_name": "Juan",
    "message": "Your appointment is tomorrow.",
    "priority": "high"
  }
  ```
  **GET /logs**
  Obtiene el historial de todos los intentos de notificación.

### Diseño y patrones usados

## Chain of Responsibility:
  Para manejar los intentos de envío a través de diferentes canales, pasando al siguiente si uno falla.

## Singleton
  Para el logger que registra todas las notificaciones, asegurando una única instancia global.

### Estructura del Proyecto
  app/
  ├── __init__.py
  ├── models/
  │   └── models.py
  ├── patterns/
  │   └── channel_handlers.py
  ├── routes/
  │   ├── notification_routes.py
  │   └── user_routes.py
  ├── services/
  │   └── user_service.py
  │   └── notification_service.py
  └── utils/
      └── logger.py
  main.py
  README.md
  requirements.txt


### Instalación y ejecución

## 1. Clonar el repositorio
## 2. Crear y activar un entorno virtual
  ```bash
  python -m venv venv
  venv\Scripts\activate    
  ```

## 3. Instalar dependencias:

  ```bash
  pip install -r requirements.txt
  ```

## 4. Ejecuta la aplicación:

  ```bash
  python main.py
  ```

## 5. Abrir el navegador y colocar la siguiente URL para la documetnación Swagger:

  ```bash
  http://127.0.0.1:5000/apidocs/
  ```

### Ejemplos de pruebas con POSTMAN

## Registrar Usuario

  ```bash
    POST http://localhost:5000/users
  ```

  ```json
  {
  "name": "Cristian",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
  }  
  ```

  ![Registrar Usuario](1000984833\notification_api\images\POST\users.png)


## Enviar notificación

  ```bash
    POST http://localhost:5000/notifications/send
  ```
  
  ```json
  {
    "user_name": "Cristian",
    "message": "Your appointment is tomorrow.",
    "priority": "high"
  }
  ```

  ## Notificacion exitosa en el canal principal
  ![Enviar via Email](1000984833\notification_api\images\POST\notifications_send_good.png)

  ## Notificacion exitosa en el canal secundario
  ![Enviar via SMS](1000984833\notification_api\images\POST\notifications_send.png)

  ## Notificación fallida en cualquier canal 
  ![Todos los canales fallaron](1000984833\notification_api\images\POST\notifications_failure.png)

## Lista Usuarios

  ```bash
    GET http://localhost:5000/users
  ```

  ```json
  {
    "user_name": "Cristian",
    "message": "Your appointment is tomorrow.",
    "priority": "high"
  }
  ```
  ![Todos los canales fallaron](1000984833\notification_api\images\GET\users.png)
  
## Ver logs 

  ```bash
    GET http://localhost:5000/logs
  ```

  ![Todos los canales fallaron](1000984833\notification_api\images\GET\logs.png)

  
### Diagramas

+------------------+
|      User        |
+------------------+
| - name: str      |
| - preferred_channel: str |
| - available_channels: List[str] |
+------------------+

+---------------------------+
|   ChannelHandler (abstract) |
+---------------------------+
| - next_handler: ChannelHandler |
| + set_next(handler): ChannelHandler |
| + handle(user, message): dict |
+---------------------------+

+---------------------------+
|   EmailHandler            |
+---------------------------+
| + handle(user, message): dict |
+---------------------------+

+---------------------------+
|   SMSHandler              |
+---------------------------+
| + handle(user, message): dict |
+---------------------------+

+---------------------------+
|   WhatsAppHandler         |
+---------------------------+
| + handle(user, message): dict |
+---------------------------+

+---------------------------+
| NotificationLogger        |
+---------------------------+
| - logs: List[dict]        |
| + log(user, channel, status): void |
| + get_logs(): List[dict]  |
+---------------------------+


### Patroens de diseño usados

Patrón
# Chain of Responsibility	Implementado en channel_handlers.py. Permite que múltiples canales (email, SMS, WhatsApp) manejen una notificación uno tras otro hasta que uno tenga éxito.

# MVC simplificado (API)	Separación en routes (controlador), services (lógica de negocio), patterns (estrategia de canal), y models (datos del usuario).

# Singleton simple	NotificationLogger actúa como pseudo-singleton guardando logs en memoria durante la ejecución.


                ┌────────────┐
                │  Cliente   │
                └────┬───────┘
                     │
                     ▼
            ┌─────────────────┐
            │send_notification│
            └────┬────────────┘
                 │ construye cadena
                 ▼
        ┌─────────────┐
        │ EmailHandler│◄────────┐
        └────┬────────┘         │
             ▼                  │ canal preferido
        ┌────────────┐          │
        │ SMSHandler │          │
        └────┬───────┘          │
             ▼                  │
        ┌───────────────┐       │
        │WhatsAppHandler│───────┘
        └───────────────┘


## Documentación Swagger

![Todos los canales fallaron](1000984833\notification_api\images\swagger.png)