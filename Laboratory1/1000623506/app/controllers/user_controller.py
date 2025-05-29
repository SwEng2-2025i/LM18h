from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.user import User

# Definición del namespace para las operaciones relacionadas con usuarios.
# Este namespace agrupa las rutas y operaciones de la API relacionadas con los usuarios.
api = Namespace('users', description='User operations')

# Modelo de datos para la validación y documentación de usuarios en la API.
# Define los campos requeridos para crear un usuario.
user_model = api.model('User', {
    'name': fields.String(required=True, example="Juan"),  # Nombre del usuario con ejemplo
    'preferred_channel': fields.String(required=True, example="email"),  # Canal preferido con ejemplo
    'available_channels': fields.List(fields.String, required=True, example=["email", "sms"])  # Lista de canales con ejemplo
})

# Lista en memoria para almacenar los usuarios registrados.
# En un entorno real, esto sería reemplazado por una base de datos.
users = []

@api.route('')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """
        Obtiene la lista de usuarios registrados.
        Retorna una lista con los datos de cada usuario, incluyendo su nombre,
        canal preferido y canales disponibles.
        """
        return [{'name': u.name, 'preferred.channel': u.preferred_channel, 'available_channels': u.available_channels} for u in users]

    @api.expect(user_model)
    def post(self):
        """
        Registra un nuevo usuario en el sistema.
        Valida que el nombre del usuario no exista previamente y, si es válido,
        lo agrega a la lista de usuarios.
        """
        data = request.json
        # Verificar si ya existe un usuario con el mismo nombre
        if any(u.name == data['name'] for u in users):
            return {'error': 'El usuario ya existe'}, 400
        
        # Crear un nuevo usuario y agregarlo a la lista
        user = User(data['name'], data['preferred_channel'], data['available_channels'])
        users.append(user)
        return {'message': 'Usuario registrado exitosamente'}, 201