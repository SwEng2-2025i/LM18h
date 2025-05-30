from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.notification_service import build_channel_chain
from app.controllers.user_controller import users  # Usamos la lista en memoria de usuarios

# Definición del namespace para las operaciones relacionadas con notificaciones.
# Este namespace agrupa las rutas y operaciones de la API relacionadas con el envío de notificaciones.
api = Namespace('notifications', description='Notification operations')

# Modelo de datos para la validación y documentación de las notificaciones en la API.
# Define los campos requeridos para enviar una notificación.
notification_model = api.model('Notification', {
    'user_name': fields.String(required=True, example="Juan"),  # Nombre del usuario destinatario con ejemplo
    'message': fields.String(required=True, example="Your appointment is tomorrow."),  # Mensaje a enviar con ejemplo
    'priority': fields.String(required=True, example="high")  # Prioridad de la notificación con ejemplo
})

@api.route('/send')
class NotificationSender(Resource):
    @api.expect(notification_model)
    def post(self):
        """
        Envía una notificación a un usuario específico.
        Busca al usuario por su nombre, construye la cadena de canales disponibles
        y delega el manejo del mensaje a la cadena.
        """
        data = request.json

        # Buscar al usuario en la lista de usuarios registrados
        user = next((u for u in users if u.name == data['user_name']), None)
        if not user:
            # Retorna un error si el usuario no existe
            return {'error': 'User not found'}, 404

        # Procesar la notificación
        print(f"Intentando notificar a {user.name}...")
        chain = build_channel_chain(user.available_channels)  # Construir la cadena de canales
        chain.handle(data['message'], user)  # Manejar el mensaje a través de la cadena
        return {'message': 'Notificación procesada'}  # Respuesta exitosa