from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import random
from datetime import datetime

# Importar modulos personalizados
from models.user import User, UserManager
from models.notification import Notification
from patterns.chain_of_responsibility import NotificationChain
from patterns.factory import NotificationChannelFactory
from utils.logger import Logger

app = Flask(__name__)
api = Api(app, doc='/docs/', title='Multichannel Notification System', 
          description='A REST API for managing users and sending notifications with fallback channels')

# Inicializar managers
user_manager = UserManager()
logger = Logger()
notification_chain = NotificationChain()
channel_factory = NotificationChannelFactory()

# Modelos API para documentación Swagger
user_model = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'preferred_channel': fields.String(required=True, description='Preferred notification channel'),
    'available_channels': fields.List(fields.String, required=True, description='Available notification channels')
})

notification_model = api.model('Notification', {
    'user_name': fields.String(required=True, description='Target user name'),
    'message': fields.String(required=True, description='Notification message'),
    'priority': fields.String(required=True, description='Notification priority (low, medium, high)')
})

@api.route('/users')
class Users(Resource):
    @api.doc('list_users')
    def get(self):
        """List all registered users"""
        users = user_manager.get_all_users()
        return jsonify([{
            'name': user.name,
            'preferred_channel': user.preferred_channel,
            'available_channels': user.available_channels
        } for user in users])
    
    @api.expect(user_model)
    @api.doc('create_user')
    def post(self):
        """Register a new user with notification preferences"""
        data = request.get_json()
        
        # Validar datos de usuario requeridos
        if not all(key in data for key in ['name', 'preferred_channel', 'available_channels']):
            return {'error': 'Missing required fields'}, 400
        
        # Validar canales
        valid_channels = ['email', 'sms', 'console']
        if data['preferred_channel'] not in valid_channels:
            return {'error': f'Invalid preferred channel. Must be one of: {valid_channels}'}, 400
        
        if not all(channel in valid_channels for channel in data['available_channels']):
            return {'error': f'Invalid available channels. Must be from: {valid_channels}'}, 400
        
        # Revisa si el usuario ya existe
        if user_manager.get_user(data['name']):
            return {'error': 'User already exists'}, 409
        
        # Crea el usuario
        user = User(data['name'], data['preferred_channel'], data['available_channels'])
        user_manager.add_user(user)
        
        logger.log(f"User registered: {user.name} with preferred channel: {user.preferred_channel}")
        
        return {
            'message': 'User registered successfully',
            'user': {
                'name': user.name,
                'preferred_channel': user.preferred_channel,
                'available_channels': user.available_channels
            }
        }, 201

@api.route('/notifications/send')
class SendNotification(Resource):
    @api.expect(notification_model)
    @api.doc('send_notification')
    def post(self):
        """Send a notification to a user with fallback channels"""
        data = request.get_json()
        
        # Validar campos requeridos
        if not all(key in data for key in ['user_name', 'message', 'priority']):
            return {'error': 'Missing required fields'}, 400
        
        # Valida la prioridad de notificación, si no es ninguna de las que están listadas arroja error
        valid_priorities = ['low', 'medium', 'high']
        if data['priority'] not in valid_priorities:
            return {'error': f'Invalid priority. Must be one of: {valid_priorities}'}, 400
        
        # Obtiene el usuario, si no aparece arroja error 404
        user = user_manager.get_user(data['user_name'])
        if not user:
            return {'error': 'User not found'}, 404
        
        # Crea la notificación
        notification = Notification(
            user_name=data['user_name'],
            message=data['message'],
            priority=data['priority']
        )
        
        # Notificación de configuración basada en preferencias de usuario
        notification_chain.setup_chain(user, channel_factory)
        
        # Intento de enviar notificación
        result = notification_chain.send_notification(notification)
        
        return {
            'message': 'Notification processing completed',
            'result': result,
            'notification_id': notification.id,
            'timestamp': notification.timestamp.isoformat()
        }, 200

@api.route('/logs')
class Logs(Resource):
    @api.doc('get_logs')
    def get(self):
        """Get system logs"""
        return {'logs': logger.get_logs()}, 200

if __name__ == '__main__':
    # Usuarios de prueba
    sample_users = [
        User("Alice", "email", ["email", "sms", "console"]),
        User("Bob", "sms", ["sms", "console"]),
        User("Charlie", "console", ["console"]),
        User("Vladimir", "console", ["email", "sms", "console"]),
        User("Calamardo", "console", ["console"])
    ]
    
    for user in sample_users:
        user_manager.add_user(user)

    
    logger.log("Application started with sample users")
    print("🚀 Notification System API is running!")
    print("📚 API Documentation available at: http://localhost:5000/docs/")

    
    app.run(debug=True, host='0.0.0.0', port=5000)
