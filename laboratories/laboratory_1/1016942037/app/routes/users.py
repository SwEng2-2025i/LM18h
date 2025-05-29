from flask import Blueprint, request, jsonify
from app.models.user import User

# Creamos un Blueprint para las rutas relacionadas con usuarios
users_bp = Blueprint('users', __name__)

# Lista en memoria para guardar los usuarios registrados (no se usa base de datos)
users = []

# Ruta para registrar un nuevo usuario
@users_bp.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
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
              example: Juan
            preferred_channel:
              type: string
              example: email
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms", "console"]
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing fields
    """
    data = request.get_json()  # Obtenemos el JSON enviado en la solicitud
    name = data.get('name')
    preferred_channel = data.get('preferred_channel')
    available_channels = data.get('available_channels')

    # Validamos que todos los campos estén presentes
    if not all([name, preferred_channel, available_channels]):
        return jsonify({"error": "Faltan campos"}), 400

    # Creamos y guardamos el nuevo usuario
    user = User(name, preferred_channel, available_channels)
    users.append(user)

    return jsonify({"message": f"Usuario {name} registrado con éxito"}), 201


# Ruta para listar todos los usuarios registrados
@users_bp.route('/users', methods=['GET'])
def list_users():
    """
    List all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of registered users
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  preferred_channel:
                    type: string
                  available_channels:
                    type: array
                    items:
                      type: string
    """
    # Lista con los datos de cada usuario como diccionario
    result = [
        {
            "name": user.name,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }
        for user in users
    ]
    return jsonify(result)
