from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from abc import ABC, abstractmethod
import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional

app = Flask(__name__)
api = Api(app)

# Configuración de Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Sistema de Notificaciones - Factory Method",
        "description": "API REST para gestión de notificaciones utilizando el patrón Factory Method. "
                      "Permite registrar usuarios, enviar notificaciones con respaldo automático "
                      "y mantener historial completo de entregas.",
        "contact": {
            "name": "Maria Paula Carvajal Martinez",
            "email": "marcarvajalma@unal.edu.co"
        },
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# ------------------------
# APLICACIÓN DE FACTORY METHOD
# ------------------------

class NotificationHandler(ABC):
    """
    Clase abstracta para handlers de notificación.
    Define la interfaz común para todos los tipos de canales.
    """
    
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
    
    @abstractmethod
    def send_notification(self, user: Dict, message: str, notification_id: int, 
                         priority: str, attempt_number: int) -> bool:
        """Método abstracto para enviar notificaciones"""
        pass
    
    def _simulate_delivery(self) -> bool:
        """Simula la entrega de notificación con 70% de probabilidad de éxito"""
        return random.random() > 0.3


class EmailHandler(NotificationHandler):
    """Handler concreto para notificaciones por email"""
    
    def __init__(self):
        super().__init__("email")
    
    def send_notification(self, user: Dict, message: str, notification_id: int, 
                         priority: str, attempt_number: int) -> bool:
        """Envía notificación por email"""
        print(f"Enviando email a {user['name']}: {message}")
        success = self._simulate_delivery()
        
        # Registrar en historial
        history_entry = {
            "id": len(notification_history) + 1,
            "notification_id": notification_id,
            "user_name": user['name'],
            "message": message,
            "priority": priority,
            "channel": self.channel_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "attempt_number": attempt_number
        }
        notification_history.append(history_entry)
        
        return success


class SmsHandler(NotificationHandler):
    """Handler concreto para notificaciones por SMS"""
    
    def __init__(self):
        super().__init__("sms")
    
    def send_notification(self, user: Dict, message: str, notification_id: int, 
                         priority: str, attempt_number: int) -> bool:
        """Envía notificación por SMS"""
        print(f"Enviando SMS a {user['name']}: {message}")
        success = self._simulate_delivery()
        
        # Registrar en historial
        history_entry = {
            "id": len(notification_history) + 1,
            "notification_id": notification_id,
            "user_name": user['name'],
            "message": message,
            "priority": priority,
            "channel": self.channel_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "attempt_number": attempt_number
        }
        notification_history.append(history_entry)
        
        return success


class WhatsAppHandler(NotificationHandler):
    """Handler concreto para notificaciones por WhatsApp"""
    
    def __init__(self):
        super().__init__("whatsapp")
    
    def send_notification(self, user: Dict, message: str, notification_id: int, 
                         priority: str, attempt_number: int) -> bool:
        """Envía notificación por WhatsApp"""
        print(f"Enviando WhatsApp a {user['name']}: {message}")
        success = self._simulate_delivery()
        
        # Registrar en historial
        history_entry = {
            "id": len(notification_history) + 1,
            "notification_id": notification_id,
            "user_name": user['name'],
            "message": message,
            "priority": priority,
            "channel": self.channel_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "attempt_number": attempt_number
        }
        notification_history.append(history_entry)
        
        return success


class NotificationHandlerFactory:
    """
    Factory para crear handlers de notificación dinámicamente.
    Implementa el patrón Factory Method.
    """
    
    def __init__(self):
        self._handlers = {
            "email": EmailHandler,
            "sms": SmsHandler,
            "whatsapp": WhatsAppHandler
        }
    
    def create_handler(self, channel_type: str) -> NotificationHandler:
        """
        Crea un handler para el tipo de canal especificado.
        
        Args:
            channel_type: Tipo de canal ("email", "sms", "whatsapp")
            
        Returns:
            NotificationHandler: Instancia del handler correspondiente
            
        Raises:
            ValueError: Si el tipo de canal no es soportado
        """
        handler_class = self._handlers.get(channel_type)
        if not handler_class:
            raise ValueError(f"Canal no soportado: {channel_type}")
        return handler_class()
    
    def get_supported_channels(self) -> List[str]:
        """Retorna lista de canales soportados"""
        return list(self._handlers.keys())
    
    def register_handler(self, channel_type: str, handler_class):
        """Registra un nuevo tipo de handler"""
        self._handlers[channel_type] = handler_class


class NotificationService:
    """Servicio principal para gestionar el envío de notificaciones"""
    
    def __init__(self):
        self.factory = NotificationHandlerFactory()
    
    def send_notification(self, user: Dict, message: str, notification_id: int, 
                         priority: str) -> Tuple[bool, str, int]:
        """
        Envía notificación usando Factory Method con respaldo automático.
        
        Args:
            user: Datos del usuario
            message: Mensaje a enviar
            notification_id: ID de la notificación
            priority: Prioridad del mensaje
            
        Returns:
            Tuple[bool, str, int]: (éxito, canal_usado, total_intentos)
        """
        # Construir lista de canales a intentar
        channels_to_try = [user['preferred_channel']]
        for channel in user['available_channels']:
            if channel not in channels_to_try:
                channels_to_try.append(channel)
        
        attempt_number = 0
        
        for channel in channels_to_try:
            attempt_number += 1
            try:
                # Usar Factory Method para crear el handler
                handler = self.factory.create_handler(channel)
                success = handler.send_notification(user, message, notification_id, 
                                                  priority, attempt_number)
                
                if success:
                    return True, channel, attempt_number
                    
            except ValueError as e:
                print(f"Error creando handler para {channel}: {e}")
                continue
        
        return False, "none", attempt_number


# ------------------------
# ALMACENAMIENTO EN MEMORIA
# ------------------------

# Base de datos simulada
users_db = []
notifications_db = []
notification_history = []

# Servicio de notificaciones
notification_service = NotificationService()

# ------------------------
# RECURSOS DE LA API
# ------------------------

class Users(Resource):
    """Recurso para gestión de usuarios"""
    
    def get(self):
        """
        Obtener todos los usuarios
        ---
        tags:
          - Usuarios
        summary: Listar todos los usuarios registrados
        description: Retorna una lista con todos los usuarios registrados en el sistema, incluyendo sus preferencias de canales de comunicación.
        responses:
          200:
            description: Lista de usuarios obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID único del usuario
                    example: 1
                  name:
                    type: string
                    description: Nombre completo del usuario
                    example: "Juan Pérez"
                  preferred_channel:
                    type: string
                    enum: [email, sms, whatsapp]
                    description: Canal preferido para recibir notificaciones
                    example: "email"
                  available_channels:
                    type: array
                    items:
                      type: string
                      enum: [email, sms, whatsapp]
                    description: Lista de canales disponibles para el usuario
                    example: ["email", "sms", "whatsapp"]
        """
        return users_db, 200
    
    def post(self):
        """
        Crear un nuevo usuario
        ---
        tags:
          - Usuarios
        summary: Registrar un nuevo usuario en el sistema
        description: |
          Crea un nuevo usuario con sus preferencias de canales de comunicación.
          El canal preferido debe estar incluido en la lista de canales disponibles.
        parameters:
          - in: body
            name: usuario
            description: Datos del usuario a crear
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
                  description: Nombre completo del usuario
                  example: "María García"
                  minLength: 1
                preferred_channel:
                  type: string
                  enum: [email, sms, whatsapp]
                  description: Canal preferido para notificaciones
                  example: "email"
                available_channels:
                  type: array
                  items:
                    type: string
                    enum: [email, sms, whatsapp]
                  description: Lista de canales disponibles (sin duplicados)
                  example: ["email", "sms", "whatsapp"]
                  minItems: 1
                  uniqueItems: true
        responses:
          201:
            description: Usuario creado exitosamente
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Usuario creado exitosamente"
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "María García"
                    preferred_channel:
                      type: string
                      example: "email"
                    available_channels:
                      type: array
                      items:
                        type: string
                      example: ["email", "sms", "whatsapp"]
          400:
            description: Error en los datos enviados
            schema:
              type: object
              properties:
                error:
                  type: string
                  examples:
                    canal_invalido: "Canal preferido no válido. Use: email, sms, whatsapp"
                    canal_no_disponible: "El canal preferido debe estar en la lista de canales disponibles"
                    duplicados: "No se permiten canales duplicados"
                    campos_requeridos: "Faltan campos requeridos: name, preferred_channel, available_channels"
        """
        data = request.get_json()
        
        # Validación de campos requeridos
        required_fields = ['name', 'preferred_channel', 'available_channels']
        for field in required_fields:
            if field not in data:
                return {'error': f'Campo requerido: {field}'}, 400
        
        # Validación de canal preferido
        valid_channels = ["email", "sms", "whatsapp"]
        if data['preferred_channel'] not in valid_channels:
            return {'error': f'Canal preferido no válido. Use: {", ".join(valid_channels)}'}, 400
        
        # Validación de canales disponibles
        if not isinstance(data['available_channels'], list):
            return {'error': 'available_channels debe ser una lista'}, 400
        
        for channel in data['available_channels']:
            if channel not in valid_channels:
                return {'error': f'Canal no válido: {channel}. Use: {", ".join(valid_channels)}'}, 400
        
        # Verificar que no haya duplicados
        if len(data['available_channels']) != len(set(data['available_channels'])):
            return {'error': 'No se permiten canales duplicados'}, 400
        
        # Verificar que el canal preferido esté en la lista disponible
        if data['preferred_channel'] not in data['available_channels']:
            return {'error': 'El canal preferido debe estar en la lista de canales disponibles'}, 400
        
        # Crear usuario
        user = {
            'id': len(users_db) + 1,
            'name': data['name'],
            'preferred_channel': data['preferred_channel'],
            'available_channels': data['available_channels']
        }
        
        users_db.append(user)
        
        return {
            'message': 'Usuario creado exitosamente',
            'user': user
        }, 201


class Notifications(Resource):
    """Recurso para gestión de notificaciones"""
    
    def __init__(self):
        self.notification_service = notification_service
    
    def get(self):
        """
        Obtener todas las notificaciones enviadas
        ---
        tags:
          - Notificaciones
        summary: Listar todas las notificaciones enviadas
        description: |
          Retorna una lista con todas las notificaciones que han sido procesadas por el sistema,
          incluyendo información sobre el canal utilizado y el estado de entrega.
        responses:
          200:
            description: Lista de notificaciones obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID único de la notificación
                    example: 1
                  user_name:
                    type: string
                    description: Nombre del usuario destinatario
                    example: "María García"
                  message:
                    type: string
                    description: Contenido del mensaje enviado
                    example: "Su pedido ha sido enviado"
                  priority:
                    type: string
                    enum: [high, medium, low]
                    description: Prioridad de la notificación
                    example: "medium"
                  delivered_via:
                    type: string
                    description: Canal por el cual se entregó la notificación
                    example: "sms"
                  timestamp:
                    type: string
                    format: date-time
                    description: Fecha y hora de procesamiento
                    example: "2025-05-30T10:30:00"
                  total_attempts:
                    type: integer
                    description: Número total de intentos realizados
                    example: 2
                  success:
                    type: boolean
                    description: Indica si la notificación fue entregada exitosamente
                    example: true
        """
        return notifications_db, 200
    
    def post(self):
        """
        Enviar una notificación usando Factory Method
        ---
        tags:
          - Notificaciones
        summary: Enviar notificación a un usuario
        description: |
          Envía una notificación a un usuario utilizando el patrón Factory Method.
          El sistema intentará entregar la notificación usando el canal preferido del usuario.
          Si falla, automáticamente intentará con los otros canales disponibles como respaldo.
          
          **Proceso interno:**
          1. Busca al usuario por nombre
          2. Crea dinámicamente el handler usando Factory Method
          3. Intenta entrega con canal preferido
          4. Si falla, prueba con canales de respaldo
          5. Registra cada intento en el historial
        parameters:
          - in: body
            name: notificacion
            description: Datos de la notificación a enviar
            required: true
            schema:
              type: object
              required:
                - user_name
                - message
                - priority
              properties:
                user_name:
                  type: string
                  description: Nombre del usuario destinatario (debe existir)
                  example: "María García"
                  minLength: 1
                message:
                  type: string
                  description: Contenido del mensaje a enviar
                  example: "Su pedido ha sido enviado"
                  minLength: 1
                priority:
                  type: string
                  enum: [high, medium, low]
                  description: Prioridad de la notificación
                  example: "medium"
        responses:
          200:
            description: Notificación procesada exitosamente
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Notificación enviada exitosamente"
                notification_id:
                  type: integer
                  example: 1
                delivered_via:
                  type: string
                  example: "sms"
                total_attempts:
                  type: integer
                  example: 2
                timestamp:
                  type: string
                  format: date-time
                  example: "2025-05-30T10:30:00"
          400:
            description: Error en los datos enviados
            schema:
              type: object
              properties:
                error:
                  type: string
                  examples:
                    campos_requeridos: "Faltan campos requeridos: user_name, message, priority"
                    prioridad_invalida: "Prioridad no válida. Use: high, medium, low"
          404:
            description: Usuario no encontrado
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Usuario no encontrado"
          500:
            description: Error al enviar la notificación
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "No fue posible entregar la notificación por ningún canal"
                notification_id:
                  type: integer
                  example: 1
                total_attempts:
                  type: integer
                  example: 3
        """
        data = request.get_json()
        
        # Validación de campos requeridos
        required_fields = ['user_name', 'message', 'priority']
        for field in required_fields:
            if field not in data:
                return {'error': f'Campo requerido: {field}'}, 400
        
        # Validación de prioridad
        valid_priorities = ["high", "medium", "low"]
        if data['priority'] not in valid_priorities:
            return {'error': f'Prioridad no válida. Use: {", ".join(valid_priorities)}'}, 400
        
        # Buscar usuario
        user = None
        for u in users_db:
            if u['name'] == data['user_name']:
                user = u
                break
        
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        
        # Crear notificación
        notification_id = len(notifications_db) + 1
        timestamp = datetime.now().isoformat()
        
        # Enviar notificación usando Factory Method
        success, delivered_via, total_attempts = self.notification_service.send_notification(
            user, data['message'], notification_id, data['priority']
        )
        
        # Crear registro de notificación
        notification = {
            'id': notification_id,
            'user_name': data['user_name'],
            'message': data['message'],
            'priority': data['priority'],
            'delivered_via': delivered_via,
            'timestamp': timestamp,
            'total_attempts': total_attempts,
            'success': success
        }
        
        notifications_db.append(notification)
        
        if success:
            return {
                'message': 'Notificación enviada exitosamente',
                'notification_id': notification_id,
                'delivered_via': delivered_via,
                'total_attempts': total_attempts,
                'timestamp': timestamp
            }, 200
        else:
            return {
                'error': 'No fue posible entregar la notificación por ningún canal',
                'notification_id': notification_id,
                'total_attempts': total_attempts
            }, 500


class NotificationHistory(Resource):
    """Recurso para consultar el historial de notificaciones"""
    
    def get(self):
        """
        Obtener historial completo de intentos de entrega
        ---
        tags:
          - Historial
        summary: Consultar historial de entregas
        description: |
          Retorna el historial completo de todos los intentos de entrega de notificaciones,
          incluyendo intentos fallidos. Cada entrada representa un intento individual
          realizado por el sistema usando el patrón Factory Method.
          
          **Información incluida:**
          - Detalles de cada intento de entrega
          - Canal utilizado en cada intento
          - Resultado del intento (éxito/fallo)
          - Orden de los intentos para cada notificación
        responses:
          200:
            description: Historial obtenido exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID único del registro en el historial
                    example: 1
                  notification_id:
                    type: integer
                    description: ID de la notificación asociada
                    example: 1
                  user_name:
                    type: string
                    description: Nombre del usuario destinatario
                    example: "María García"
                  message:
                    type: string
                    description: Contenido del mensaje
                    example: "Su pedido ha sido enviado"
                  priority:
                    type: string
                    enum: [high, medium, low]
                    description: Prioridad de la notificación
                    example: "medium"
                  channel:
                    type: string
                    enum: [email, sms, whatsapp]
                    description: Canal utilizado en este intento
                    example: "email"
                  success:
                    type: boolean
                    description: Resultado del intento de entrega
                    example: false
                  timestamp:
                    type: string
                    format: date-time
                    description: Fecha y hora del intento
                    example: "2025-05-30T10:30:00"
                  attempt_number:
                    type: integer
                    description: Número de intento para esta notificación
                    example: 1
        """
        return notification_history, 200


# ------------------------
# REGISTRO DE RECURSOS
# ------------------------

api.add_resource(Users, '/users/')
api.add_resource(Notifications, '/notifications/send')
api.add_resource(NotificationHistory, '/notifications/history')


# ------------------------
# PÁGINA PRINCIPAL
# ------------------------

@app.route('/')
def home():
    """
    Página principal de la API
    ---
    tags:
      - Sistema
    summary: Información general del sistema
    description: Página de bienvenida con información sobre la API y enlaces útiles.
    responses:
      200:
        description: Página principal cargada exitosamente
        content:
          text/html:
            schema:
              type: string
    """
    return """
    <h1>Sistema de Notificaciones - Factory Method</h1>
    <p><strong>Presentado por:</strong> Maria Paula Carvajal Martinez</p>
    <p><strong>Email:</strong> marcarvajalma@unal.edu.co</p>
    
    <h2>Endpoints Disponibles</h2>
    <ul>
        <li><strong>GET/POST /users/</strong> - Gestión de usuarios</li>
        <li><strong>GET/POST /notifications/send</strong> - Envío de notificaciones</li>
        <li><strong>GET /notifications/history</strong> - Historial de entregas</li>
    </ul>
    
    <h2>Documentación</h2>
    <ul>
        <li><a href="/swagger/"> Documentación Swagger</a></li>
    </ul>
    
    <h2>Patrón Factory Method</h2>
    <p>Este sistema utiliza el patrón Factory Method para crear handlers de notificación dinámicamente:</p>
    <ul>
        <li><strong>EmailHandler</strong> - Para notificaciones por correo</li>
        <li><strong>SmsHandler</strong> - Para notificaciones por SMS</li>
        <li><strong>WhatsAppHandler</strong> - Para notificaciones por WhatsApp</li>
    </ul>
    
    """


if __name__ == '__main__':
    print("Iniciando Sistema de Notificaciones con Factory Method")
    print("Documentación Swagger disponible en: http://localhost:5000/swagger/")
    print("API principal en: http://localhost:5000/")
    app.run(debug=True)