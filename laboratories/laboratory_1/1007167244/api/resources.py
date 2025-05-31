from flask_restful import Resource
from flask import request
from datetime import datetime
import uuid

from patterns.strategy import NotificationContext
from patterns.chain_of_responsibility import (
    ContentValidator,
    LengthValidator,
    PriorityHandler,
    DeliveryHandler
)
from models.storage import (
    add_user,
    get_user_by_name,
    add_notification,
    get_all_users,
    get_all_notifications,
    get_notification_history,
    get_notification_stats
)

class UsersResource(Resource):
    def get(self):
        """
        Obtener todos los usuarios
        ---
        tags:
          - Usuarios
        responses:
          200:
            description: Lista de usuarios
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID único del usuario
                  name:
                    type: string
                    description: Nombre del usuario
                  preferred_channel:
                    type: string
                    description: Canal de notificación preferido
                  available_channels:
                    type: array
                    items:
                      type: string
                    description: Canales de notificación disponibles
        """
        return get_all_users()

    def post(self):
        """
        Crear un nuevo usuario
        ---
        tags:
          - Usuarios
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - name
                - preferred_channel
                - available_channels
              properties:
                name:
                  type: string
                  description: Nombre del usuario
                  example: "Juan Pérez"
                preferred_channel:
                  type: string
                  description: Canal de notificación preferido
                  example: "email"
                available_channels:
                  type: array
                  items:
                    type: string
                  description: Canales de notificación disponibles
                  example: ["email", "sms", "push"]
        responses:
          201:
            description: Usuario creado exitosamente
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: ID del usuario creado
                name:
                  type: string
                  description: Nombre del usuario
                preferred_channel:
                  type: string
                  description: Canal preferido
                available_channels:
                  type: array
                  items:
                    type: string
                  description: Canales disponibles
          400:
            description: Datos inválidos
        """
        data = request.get_json()
        user = {
            "id": len(get_all_users()) + 1,
            "name": data["name"],
            "preferred_channel": data["preferred_channel"],
            "available_channels": data["available_channels"]
        }
        return add_user(user), 201

class NotificationsResource(Resource):
    def __init__(self):
        self.notification_context = NotificationContext()
        
        # Configurar la cadena de responsabilidad
        content_validator = ContentValidator()
        length_validator = LengthValidator()
        priority_handler = PriorityHandler()
        delivery_handler = DeliveryHandler(self.notification_context)
        
        content_validator.set_next(length_validator)
        length_validator.set_next(priority_handler)
        priority_handler.set_next(delivery_handler)
        
        self.message_handler = content_validator

    def get(self):
        """
        Obtener todas las notificaciones
        ---
        tags:
          - Notificaciones
        responses:
          200:
            description: Lista de notificaciones
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: ID único de la notificación
                  user_name:
                    type: string
                    description: Nombre del usuario
                  message:
                    type: string
                    description: Mensaje de la notificación
                  priority:
                    type: string
                    description: Prioridad de la notificación
                  timestamp:
                    type: string
                    description: Fecha y hora de la notificación
                  result:
                    type: object
                    description: Resultado del envío
        """
        return get_all_notifications()

    def post(self):
        """
        Enviar una notificación
        ---
        tags:
          - Notificaciones
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - user_name
                - message
              properties:
                user_name:
                  type: string
                  description: Nombre del usuario destinatario
                  example: "Juan Pérez"
                message:
                  type: string
                  description: Mensaje a enviar
                  example: "¡Hola! Esta es una notificación de prueba."
                priority:
                  type: string
                  description: Prioridad de la notificación (low, medium, high)
                  example: "medium"
        responses:
          200:
            description: Notificación enviada exitosamente
            schema:
              type: object
              properties:
                id:
                  type: string
                  description: ID de la notificación
                user_name:
                  type: string
                  description: Nombre del usuario
                message:
                  type: string
                  description: Mensaje enviado
                priority:
                  type: string
                  description: Prioridad de la notificación
                timestamp:
                  type: string
                  description: Fecha y hora del envío
                result:
                  type: object
                  description: Resultado del envío
          404:
            description: Usuario no encontrado
          400:
            description: Error en el envío de la notificación
        """
        data = request.get_json()
        user = get_user_by_name(data["user_name"])
        
        if not user:
            return {"error": "User not found"}, 404

        message_data = {
            "user": user,
            "message": data["message"],
            "priority": data.get("priority", "medium")
        }

        # Procesar el mensaje a través de la cadena de responsabilidad
        result = self.message_handler.handle(message_data)
        
        if "error" in result:
            return result, 400

        notification = {
            "id": str(uuid.uuid4()),
            "user_name": user["name"],
            "message": data["message"],
            "priority": data.get("priority", "medium"),
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        return add_notification(notification)

class NotificationHistoryResource(Resource):
    def get(self):
        """
        Obtener historial de notificaciones
        ---
        tags:
          - Notificaciones
        responses:
          200:
            description: Historial de notificaciones
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: ID de la notificación
                  user_name:
                    type: string
                    description: Nombre del usuario
                  message:
                    type: string
                    description: Mensaje enviado
                  timestamp:
                    type: string
                    description: Fecha y hora del envío
                  status:
                    type: string
                    description: Estado de la notificación
        """
        return get_notification_history()

class NotificationStatsResource(Resource):
    def get(self):
        """
        Obtener estadísticas de notificaciones
        ---
        tags:
          - Notificaciones
        responses:
          200:
            description: Estadísticas de notificaciones
            schema:
              type: object
              properties:
                total_notifications:
                  type: integer
                  description: Total de notificaciones enviadas
                success_rate:
                  type: number
                  description: Tasa de éxito de envío
                by_priority:
                  type: object
                  description: Notificaciones por prioridad
                by_channel:
                  type: object
                  description: Notificaciones por canal
        """
        return get_notification_stats() 