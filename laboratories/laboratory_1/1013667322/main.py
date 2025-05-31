"""
Aplicación principal del sistema de notificaciones multicanal
"""
from flask import Flask, request, jsonify
from flasgger import Swagger
from app.services import UserService, NotificationService
from app.models import Notification
from app.patterns import Logger

# Crear aplicación Flask
app = Flask(__name__)

# Configurar Swagger
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Sistema de Notificaciones Multicanal",
        "description": "API REST para gestión de usuarios y envío de notificaciones con múltiples canales",
        "version": "1.0.0"
    }
})

# Servicios
user_service = UserService()
notification_service = NotificationService()
logger = Logger()


@app.route('/users', methods=['POST'])
def register_user():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Users
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
              example: "Juan"
            preferred_channel:
              type: string
              enum: ["email", "sms", "console"]
              example: "email"
            available_channels:
              type: array
              items:
                type: string
                enum: ["email", "sms", "console"]
              example: ["email", "sms"]
    responses:
      201:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
            user:
              type: object
      400:
        description: Error en los datos de entrada
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('name', 'preferred_channel', 'available_channels')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = user_service.register_user(
            data['name'],
            data['preferred_channel'],
            data['available_channels']
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/users', methods=['GET'])
def get_users():
    """
    Obtener todos los usuarios
    ---
    tags:
      - Users
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
    """
    users = user_service.get_all_users()
    return jsonify({
        'users': [user.to_dict() for user in users]
    })


@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Enviar una notificación
    ---
    tags:
      - Notifications
    parameters:
      - name: body
        in: body
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
              example: "Juan"
            message:
              type: string
              example: "Tu cita es mañana."
            priority:
              type: string
              enum: ["low", "medium", "high"]
              example: "high"
    responses:
      200:
        description: Notificación enviada
        schema:
          type: object
          properties:
            success:
              type: boolean
            channel_used:
              type: string
            attempts:
              type: array
            message:
              type: string
      404:
        description: Usuario no encontrado
      400:
        description: Error en los datos de entrada
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('user_name', 'message', 'priority')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = user_service.get_user(data['user_name'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        notification = Notification(
            data['user_name'],
            data['message'],
            data['priority']
        )
        
        result = notification_service.send_notification(user, notification)
        
        return jsonify(result.to_dict())
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Obtener logs del sistema
    ---
    tags:
      - System
    responses:
      200:
        description: Logs del sistema
        schema:
          type: object
          properties:
            logs:
              type: array
              items:
                type: string
    """
    return jsonify({'logs': logger.get_logs()})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Notificaciones Multicanal...")
    print("📖 Documentación disponible en: http://127.0.0.1:5000/apidocs/")
    app.run(debug=True, host='127.0.0.1', port=5000)
