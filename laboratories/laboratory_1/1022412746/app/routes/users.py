from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

users_bp = Blueprint('users', __name__)
user_service = UserService()

@users_bp.route('/users', methods=['POST'])
def register_user():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
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
              example: ["email", "sms"]
    responses:
      200:
        description: Usuario registrado con éxito
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Faltan datos
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    name = data.get("name")
    preferred = data.get("preferred_channel")
    channels = data.get("available_channels")
    
    if not all([name, preferred, channels]):
        return jsonify({"error": "Faltan datos"}), 400

    user_service.register_user(name, preferred, channels)
    return jsonify({"message": f"Usuario {name} registrado con éxito"}), 200

@users_bp.route('/users', methods=['GET'])
def list_users():
    """
    Listar todos los usuarios registrados
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios registrados
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              preferred_channel:
                type: string
              available_channels:
                type: array
                items:
                  type: string
    """
    return jsonify(user_service.get_users()), 200