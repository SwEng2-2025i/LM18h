# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

**Autor:** Laura Daniela Agudelo Cruz

## Explicación del sistema y documentación de endpoints

El sistema desarrollado es una **API RESTful** que permite registrar usuarios y enviar notificaciones a través de canales múltiples: `email`, `sms` y `console`.

Cada usuario puede tener un canal preferido y una lista de canales disponibles. Si el envío falla en el canal preferido, el sistema intentará de forma automática los canales alternativos, usando una **Cadena de Responsabilidad (Chain of Responsibility)**. Además, se utiliza un **Singleton** para la gestión centralizada del log.

Toda la lógica de envío es simulada usando `random.choice([True, False])`, lo que permite que los canales fallen aleatoriamente para poner a prueba el sistema de tolerancia a fallos.

---

### Endpoints disponibles

| Método | Endpoint              | Descripción                                                   |
|--------|-----------------------|---------------------------------------------------------------|
| POST   | `/users`              | Registra un nuevo usuario con nombre, canal preferido y lista de canales disponibles |
| GET    | `/users`              | Devuelve todos los usuarios registrados                      |
| POST   | `/notifications/send` | Envía una notificación a un usuario usando lógica de fallback |

---

### POST `/users` – Registrar usuario

**Request Body**
```json
{
  "name": "Laura",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console"]
}
```

**Respuestas**
- `201 Created`: Usuario registrado correctamente
- `200 OK`: El usuario ya existe
- `400 Bad Request`: Faltan campos requeridos

---

### GET `/users` – Obtener usuarios

**Respuesta exitosa**
```json
[
  {
    "name": "Laura",
    "preferred_channel": "email",
    "available_channels": ["email", "sms", "console"]
  }
]
```

- `200 OK`: Lista de usuarios en memoria

---

### POST `/notifications/send` – Enviar notificación

**Request Body**
```json
{
  "user_name": "Laura",
  "message": "Tu cita es mañana.",
  "priority": "high"
}
```

**Respuestas posibles**

Envío exitoso:
```json
{
  "result": "Notification sent successfully",
  "channel_used": "email",
  "attempts": [
    {
      "channel": "email",
      "success": true
    }
  ]
}
```

Fallo en todos los canales:
```json
{
  "result": "Notification failed on all channels",
  "attempts": [
    {
      "channel": "email",
      "success": false
    },
    {
      "channel": "sms",
      "success": false
    },
    {
      "channel": "console",
      "success": false
    }
  ]
}
```

Errores comunes:
- `400 Bad Request`: Campos requeridos ausentes
- `404 Not Found`: Usuario no encontrado

---

### Documentación Swagger

La documentación de la API está disponible en:

http://localhost:5000/docs

Esta interfaz permite probar los endpoints directamente desde el navegador usando Swagger.

---

## Justificación de patrones de diseño

En este laboratorio se implementó un sistema de notificaciones multicanal siguiendo buenas prácticas de diseño de software para garantizar modularidad, escalabilidad y mantenibilidad. Para ello, se aplicaron dos patrones de diseño principales:

### 1. Cadena de Responsabilidad (Chain of Responsibility)

- **Motivación:** El envío de notificaciones debe intentar primero el canal preferido por el usuario y, en caso de fallo, intentar canales alternativos sin acoplar el sistema a canales específicos.
- **Beneficios:**  
  - Permite encadenar múltiples objetos (canales) que procesan la solicitud (envío) hasta que uno tenga éxito.  
  - Facilita la incorporación o eliminación de canales sin modificar la lógica central.  
  - Proporciona tolerancia a fallos mediante el reintento automático en otros canales.  
- **Implementación:** Cada canal implementa un método `send` que intenta enviar la notificación y, si falla, delega al siguiente canal de la cadena.

### 2. Singleton

- **Motivación:** Centralizar el registro de logs para todas las operaciones del sistema mediante una única instancia compartida.
- **Beneficios:**  
  - Evita la creación de múltiples instancias del logger, manteniendo un punto único de control.  
  - Facilita la trazabilidad y seguimiento de los intentos de envío en todo el sistema.  
  - Simplifica la gestión y el mantenimiento del logging.  
- **Implementación:** La clase `LoggerSingleton` garantiza que solo exista una instancia del logger en todo el ciclo de vida de la aplicación.

---

Ambos patrones en conjunto permiten construir un sistema modular y resiliente que puede escalar y adaptarse fácilmente, manteniendo el código limpio y desacoplado.

---

# Diagrama de Clase/Modulos

(Imagen no incluida: diagramas/Clase UML.png)

En el sistema, las clases presentan varias relaciones clave que se representan en UML para reflejar su estructura y comportamiento. Primero, las clases `EmailChannel`, `SMSChannel` y `ConsoleChannel` heredan de la clase abstracta `Channel`, una relación de herencia que se muestra con una línea continua y una flecha hueca apuntando a la superclase. La clase `Notification` tiene una asociación directa con la clase `User`, ya que cada notificación está vinculada a un usuario. Además, la clase `Channel` implementa el patrón Chain of Responsibility, manteniendo una referencia al siguiente canal mediante una agregación. Finalmente, el patrón Singleton, utilizado para el `Logger`, no se representa con una relación específica en UML.

# Instrucciones para Setup y Testing

## Requisitos de Instalación

Para ejecutar esta API, necesitas tener instalado Python 3.7+ y pip.

1. Clonar el repositorio o descarga el código fuente.
2. Navegar al directorio raíz del proyecto.
3. Crear y activar un entorno virtual:

    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

4. Instalar las dependencias:

    pip install -r requirements.txt

5. Ejecutar la aplicación Flask:

    python app.py

Por defecto, la API estará disponible en:

    http://127.0.0.1:5000

---

## Pruebas con curl

Desde una terminal, se pueden probar los endpoints con los siguientes comandos:

### Registrar un usuario

    curl -X POST http://127.0.0.1:5000/users \
    -H "Content-Type: application/json" \
    -d '{"name":"Juan","preferred_channel":"email","available_channels":["email","sms"]}'

### Listar usuarios registrados

    curl http://127.0.0.1:5000/users

### Enviar una notificación

    curl -X POST http://127.0.0.1:5000/notifications/send \
    -H "Content-Type: application/json" \
    -d '{"user_name":"Juan","message":"Your appointment is tomorrow.","priority":"high"}'

---

## Pruebas con Postman

Para usar Postman:

1. Abrir Postman y crear una nueva colección llamada **Multichannel Notification API**.
2. Añadir una nueva solicitud:

- Método: `POST`
- URL: `http://127.0.0.1:5000/users`
- En la pestaña *Body*, selecciona *raw* y elige formato *JSON*.
- Copia el siguiente JSON:

```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

3. Enviar la solicitud y revisar que la respuesta sea un código `201` y un mensaje de éxito.
4. Añadir otra solicitud:

- Método: `GET`
- URL: `http://127.0.0.1:5000/users`

5. Añadir otra solicitud:

- Método: `POST`
- URL: `http://127.0.0.1:5000/notifications/send`
- En *Body* (raw, JSON):

```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

---

## Documentación Swagger

La API cuenta con documentación Swagger interactiva se puede consultar y usar para probar los endpoints desde un navegador. 

http://127.0.0.1:5000/docs