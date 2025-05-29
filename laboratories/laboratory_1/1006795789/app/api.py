# api.py
# Autor: Jorge Andres Torres Leal
# Este archivo define la API REST principal para la gestión de usuarios y el envío de notificaciones.
# Utiliza Flask y Flask-RESTX para estructurar los endpoints y la documentación interactiva.

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace

from app.core.user_manager import UserManager
from app.core.notification_handler import send_notification

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la API RESTX, incluyendo la ruta de la documentación interactiva
api = Api(
    app,
    version='1.0',
    title='Notification API',
    description='API for managing users and sending notifications',
    doc='/docs'  # Monta la UI de Swagger en /docs
)

# Definición de un Namespace para agrupar los endpoints bajo /api
ns = Namespace('api', description='API operations')
# Registro del Namespace en la API, todos los endpoints estarán bajo /api
api.add_namespace(ns, path='/api')

# Modelo de usuario para la documentación y validación de entrada
user_model = ns.model('User', {
    'name': fields.String(required=True, description='Nombre del usuario'),
    'preferred_channel': fields.String(required=True, description='Canal de notificación preferido (email, sms, console)'),
    'available_channels': fields.List(fields.String, required=True, description='Lista de canales de notificación disponibles')
})

# Modelo de notificación para la documentación y validación de entrada
notif_model = ns.model('Notification', {
    'user_name': fields.String(required=True, description='Nombre del usuario al que se enviará la notificación'),
    'message': fields.String(required=True, description='Contenido del mensaje de notificación'),
    'priority': fields.String(required=True, description='Nivel de prioridad de la notificación (high, medium, low)')
})

@ns.route('/users')
@ns.doc(tags=['users'])
class Users(Resource):
    """
    Recurso para la gestión de usuarios.
    Permite registrar nuevos usuarios y listar los existentes.
    """
    @ns.doc('create_user',
             description='Registrar un nuevo usuario con sus canales de notificación preferidos y disponibles',
             responses={
                 201: 'Usuario registrado exitosamente',
                 400: 'Datos de entrada inválidos'
             })
    @ns.expect(user_model, validate=True)
    def post(self):
        """
        Registra un nuevo usuario en el sistema.
        Espera un JSON con nombre, canal preferido y canales disponibles.
        """
        data = request.json
        UserManager.add_user(
            data['name'], data['preferred_channel'], data['available_channels']
        )
        return {"message": "User registered"}, 201

    @ns.doc('list_users',
             description='Obtener la lista de todos los usuarios registrados',
             responses={
                 200: 'Lista de usuarios obtenida exitosamente'
             })
    def get(self):
        """
        Devuelve la lista de todos los usuarios registrados en el sistema.
        """
        return jsonify(UserManager.list_users())

@ns.route('/notifications/send')
@ns.doc(tags=['notifications'])
class Notify(Resource):
    """
    Recurso para el envío de notificaciones a usuarios.
    """
    @ns.doc('send_notification',
             description='Enviar una notificación a un usuario a través de su canal preferido',
             responses={
                 200: 'Notificación entregada exitosamente',
                 404: 'Usuario no encontrado',
                 500: 'Fallo en la entrega de la notificación'
             })
    @ns.expect(notif_model, validate=True)
    def post(self):
        """
        Envía una notificación a un usuario específico.
        Si el canal preferido falla, intenta con los canales alternativos.
        """
        data = request.json
        user = UserManager.get_user(data['user_name'])
        if not user:
            # Si el usuario no existe, retorna error 404
            return {"error": "User not found"}, 404

        # Intenta enviar la notificación usando la cadena de canales
        delivered = send_notification(data['user_name'], data['message'], user)
        status = "delivered" if delivered else "failed"
        return {"status": status}, (200 if delivered else 500)


