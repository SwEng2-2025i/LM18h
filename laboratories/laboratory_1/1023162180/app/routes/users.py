from flask_restx import Namespace, Resource, fields
from app.routes.shared_data import users  # Lista en memoria donde se almacenan los usuarios
from app.models.user import User          # Modelo de clase para representar un usuario

# Creamos un namespace con prefijo /users para agrupar rutas relacionadas con usuarios
api = Namespace("Users", path="/users")

# Definición del esquema (modelo) para un usuario, usado para validación y documentación Swagger
user_model = api.model('User', {
    'name': fields.String(required=True, description='Nombre del usuario'),
    'preferred_channel': fields.String(required=True, description='Canal preferido (ej. email)'),
    'available_channels': fields.List(fields.String, required=True, description='Canales disponibles')
})

# Modelo para notificaciones (definido pero no usado en estos endpoints)
notification_model = api.model("Notification", {
    "user_name": fields.String(required=True, description="Nombre del usuario que recibirá la notificación"),
    "message": fields.String(required=True, description="Contenido del mensaje"),
    "priority": fields.String(required=True, description="Prioridad del mensaje"),
})

# Ruta /users: gestión del listado general de usuarios
@api.route("")
class UserList(Resource):

    @api.doc("List all users")  # Documenta el método GET para Swagger
    def get(self):
        # Devuelve la lista completa de usuarios en formato JSON,
        # extrayendo solo los atributos relevantes de cada instancia User
        return [
            {
                'name': user.name,
                'preferred_channel': user.preferred_channel,
                'available_channels': user.available_channels
            }
            for user in users
        ]

    @api.expect(user_model)  # Espera recibir un JSON con la estructura definida en user_model
    @api.doc("Register a new user")
    def post(self):
        data = api.payload  # Obtiene el JSON enviado por el cliente
        name = data['name']
        preferred = data['preferred_channel']
        channels = data['available_channels']

        # Valida que el canal preferido esté dentro de la lista de canales disponibles
        if preferred not in channels:
            return {"error": "Preferred channel must be in available channels"}, 400

        # Verifica que no exista otro usuario con el mismo nombre para evitar duplicados
        if any(u.name == name for u in users):
            return {"error": f"User {name} already exists"}, 409

        # Si pasa validaciones, crea una nueva instancia User y la agrega a la lista en memoria
        new_user = User(name, preferred, channels)
        users.append(new_user)
        return {"message": f"User {name} registered successfully"}, 201

# Ruta /users/<name>: gestión de operaciones sobre un usuario específico
@api.route("/<string:name>")
@api.param("name", "The name of the user")  # Parámetro en la URL para identificar usuario
class UserResource(Resource):

    @api.doc("Update a user")  # Documenta el método PUT para Swagger
    @api.expect(user_model)     # Espera un JSON según el esquema user_model para actualizar datos
    def put(self, name):
        data = api.payload
        preferred = data['preferred_channel']
        channels = data['available_channels']

        # Busca el usuario en la lista por nombre
        for user in users:
            if user.name == name:
                # Verifica que el canal preferido esté dentro de los canales disponibles
                if preferred not in channels:
                    return {"error": "Preferred channel must be in available channels"}, 400

                # Actualiza los atributos del usuario
                user.preferred_channel = preferred
                user.available_channels = channels
                return {"message": f"User {name} updated successfully"}, 200

        # Retorna error si no encuentra el usuario para actualizar
        return {"error": f"User {name} not found"}, 404

    @api.doc("Delete a user")  # Documenta el método DELETE para Swagger
    def delete(self, name):
        global users
        # Busca el usuario por nombre y lo elimina si existe
        for user in users:
            if user.name == name:
                users.remove(user)
                return {"message": f"User {name} deleted successfully"}, 200

        # Error si no se encontró el usuario para borrar
        return {"error": f"User {name} not found"}, 404
